"""
AutoEDSSguide - EDSS Calculation Engine
========================================

Pure Python functions to compute Functional System (FS) scores and the final
EDSS step from raw Neurostatus item entries.

Algorithm sources:
- Kappos L. Neurostatus scoring definitions (v04/10.2), 2011
- Fouad et al. 2023 (DOI: 10.1177/20552173231155055):
    - Visual:    Fig 1 (Snellen → 0-4 directly, no conversion needed)
    - Brainstem: Table 1 (max of subscores)
    - Pyramidal: Fig 2 (BMRC distribution rules)
    - Cerebellar: Fig 3 (decision tree)
    - Sensory:   Fig 4+5 (superficial + deep, with combination rule)
    - Bowel/Bladder: Table 2 (max + special rule)
    - EDSS step: Fig 6-8 (FS pattern matching + ambulation override)

Conventions:
- All inputs are integers (or None if missing).
- Per-side items use _R / _L suffixes; the function takes the max.
- Permanent (P) and Temporary (T) flags exclude items from FS calculation.
- All functions return integers in the documented FS range.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass, field


# ============================================================
# Helper utilities
# ============================================================

def _max_or_none(*values) -> Optional[int]:
    """Return max of non-None values, or None if all are None."""
    vals = [v for v in values if v is not None]
    return max(vals) if vals else None


def _safe(v, default=0) -> int:
    """Treat None/missing as default (usually 0)."""
    return default if v is None else v


# ============================================================
# Visual FS (already 0-4 in Fouad's algorithm - no conversion needed)
# ============================================================

# Snellen 20/20 → 0, 20/30 → 1, 20/60 → 2, 20/100 → 3, 20/200 → 4, worse → 5
SNELLEN_LOOKUP = {
    # Aligned with the JS engine (index.html) so both engines produce the same
    # Visual FS. Grades follow Neurostatus 04/10.2 worse-eye VA cut-offs:
    # 20/25 -> 1 (signs only), 20/30-20/50 -> 2 (mild), 20/60-20/80 -> 3
    # (moderate scotoma / VA 20/60-20/99 zone), 20/100-20/200 -> 4, worse -> 5.
    "20/20": 0,
    "20/25": 1,
    "20/30": 2, "20/40": 2, "20/50": 2,
    "20/60": 3, "20/70": 3, "20/80": 3,
    "20/100": 4, "20/200": 4,
    "20/400": 5, "CF": 5, "HM": 5, "LP": 5, "NLP": 5,
}


def snellen_to_score(snellen: str) -> int:
    """Convert Snellen acuity to a 0-6 score (worse-eye scale)."""
    if snellen is None or snellen == "" or snellen == "-":
        return 0
    return SNELLEN_LOOKUP.get(snellen.strip(), 0)


def calc_visual_fs(
    va_od: Optional[str] = None,    # Snellen string for OD
    va_os: Optional[str] = None,    # Snellen string for OS
    vf_od: Optional[int] = None,    # 0-3 visual fields OD
    vf_os: Optional[int] = None,    # 0-3 visual fields OS
    scotoma_od: Optional[int] = None,  # 0-2
    scotoma_os: Optional[int] = None,  # 0-2
    pallor_od: Optional[int] = None,   # 0-1 (optional, doesn't change FS)
    pallor_os: Optional[int] = None,   # 0-1
) -> int:
    """
    Visual FS (0-6) per Neurostatus, then converted (Kurtzke EDSS):
    0→0, 1→1, 2→2, 3→3, 4→3, 5→4, 6→5

    The "worse eye" determines the FS:
    - 0: normal
    - 1: VA 20/30 OR small scotoma OR mild VF defect
    - 2: VA 20/30-20/59 OR moderate VF defect (incomplete hemianopsia)
    - 3: VA 20/60-20/99 OR complete homonymous hemianopsia
    - 4: VA 20/100-20/199 (worse eye) AND grade 3 in better eye
    - 5: VA <20/200 (worse eye) AND grade 4 in better eye
    - 6: VA <20/200 in BOTH eyes
    """
    # Neurostatus conversion of visual-field/scotoma raw grades to the higher
    # FS grade they imply (e.g. moderate field defect = FS 3, marked = FS 4).
    def _field_conv(v):
        return [0, 1, 3, 4][min(_safe(v, 0), 3)]
    def _scotoma_conv(v):
        return [0, 1, 3][min(_safe(v, 0), 2)]

    od_score = max(
        snellen_to_score(va_od),
        _field_conv(vf_od),
        _scotoma_conv(scotoma_od),
        1 if _safe(pallor_od, 0) > 0 else 0,
    )
    os_score = max(
        snellen_to_score(va_os),
        _field_conv(vf_os),
        _scotoma_conv(scotoma_os),
        1 if _safe(pallor_os, 0) > 0 else 0,
    )
    worse = max(od_score, os_score)
    better = min(od_score, os_score)

    # Grades 0-2 depend on the worse eye alone; for grade >= 3 the FS is bumped
    # one grade only when the better eye is also <= 20/60 (raw grade >= 3):
    # 3 -> 4, 4 -> 5, 5 -> 6. Matches calcVisualFS in index.html.
    if worse <= 2:
        return worse
    return min(worse + 1, 6) if better >= 3 else worse


def visual_fs_converted(visual_fs: int) -> int:
    """Convert Visual FS (0-6) to EDSS-input scale per Neurostatus.
    Matches the JS engine's visualFSConverted table: raw 1->1, 2->2, 3->2,
    4->3, 5->3, 6->4.
    """
    return [0, 1, 2, 2, 3, 3, 4][min(visual_fs, 6)]


# ============================================================
# Brainstem FS (max of all CN subscores)
# ============================================================

def calc_brainstem_fs(
    eom: Optional[int] = None,        # 0-4
    nystagmus: Optional[int] = None,  # 0-3
    trigeminal: Optional[int] = None, # 0-4
    facial: Optional[int] = None,     # 0-4
    hearing: Optional[int] = None,    # 0-4
    dysarthria: Optional[int] = None, # 0-5
    dysphagia: Optional[int] = None,  # 0-5
    other_cn: Optional[int] = None,   # 0-4
) -> int:
    """
    Brainstem FS = max of all subscores (Neurostatus + Fouad Table 1).
    Range: 0-5.
    """
    return _safe(_max_or_none(
        eom, nystagmus, trigeminal, facial, hearing,
        dysarthria, dysphagia, other_cn,
    ), 0)


# ============================================================
# Pyramidal FS (BMRC distribution rules - Fouad Fig 2 + Neurostatus)
# ============================================================

# Muscle group keys for strength (BMRC 0-5, with 5 = normal)
MUSCLE_KEYS = [
    "deltoid", "biceps", "triceps", "wflex", "wext",
    "hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant",
]


def calc_pyramidal_fs(
    strength: Optional[Dict[str, Dict[str, int]]] = None,
    # strength = {"deltoid": {"R": 5, "L": 4}, ...}
    overall_motor: Optional[int] = None,  # 0-2 (subjective)
    spast_arms_max: Optional[int] = None, # 0-4
    spast_legs_max: Optional[int] = None, # 0-4
) -> int:
    """
    Pyramidal FS per Neurostatus (Fouad Fig 2):
    0: all 5 (normal), no motor complaint
    1: signs without disability - overall_motor=1 (fatigability)
    2: BMRC 4 in 1-2 muscle groups
    3: BMRC 4 in 3+ groups, OR BMRC 3 in 1-2 groups, OR BMRC ≤2 in 1 group
    4: BMRC 2 in 2 limbs, OR monoplegia (BMRC 0-1 in 1 limb),
       OR BMRC 3 in ≥3 limbs (tetraparesis)
    5: paraplegia (BMRC 0-1 in both LL), OR BMRC ≤2 in ≥3 limbs,
       OR hemiplegia
    6: tetraplegia (BMRC 0-1 in all 4 limbs)

    For the limb-distribution rules, we map muscles to limbs:
    - Upper limb R: deltoid, biceps, triceps, wflex, wext (R side)
    - Upper limb L: same (L side)
    - Lower limb R: hipflex, kneeflex, kneeext, ankdorsi, ankplant (R side)
    - Lower limb L: same (L side)

    A limb is considered "weakest" by the lowest BMRC across its muscles.
    """
    if strength is None:
        strength = {}

    # Collect all BMRC readings for each muscle (worst side per muscle)
    muscle_min = {}
    for m in MUSCLE_KEYS:
        if m in strength:
            r = strength[m].get("R", 5)
            l = strength[m].get("L", 5)
            muscle_min[m] = min(_safe(r, 5), _safe(l, 5))

    # Compute per-limb minimum BMRC
    UE_R = min((strength.get(m, {}).get("R", 5) for m in
                ["deltoid", "biceps", "triceps", "wflex", "wext"]), default=5)
    UE_L = min((strength.get(m, {}).get("L", 5) for m in
                ["deltoid", "biceps", "triceps", "wflex", "wext"]), default=5)
    LE_R = min((strength.get(m, {}).get("R", 5) for m in
                ["hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]),
               default=5)
    LE_L = min((strength.get(m, {}).get("L", 5) for m in
                ["hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]),
               default=5)
    limbs = [UE_R, UE_L, LE_R, LE_L]

    # Tetraplegia: BMRC 0-1 in all 4 limbs
    if all(x <= 1 for x in limbs):
        return 6

    # Paraplegia: BMRC 0-1 in both LL
    if LE_R <= 1 and LE_L <= 1:
        return 5
    # Marked tetraparesis: BMRC ≤2 in ≥3 limbs
    if sum(1 for x in limbs if x <= 2) >= 3:
        return 5
    # Hemiplegia: BMRC 0-1 in UE_R+LE_R OR UE_L+LE_L
    if (UE_R <= 1 and LE_R <= 1) or (UE_L <= 1 and LE_L <= 1):
        return 5

    # Marked: BMRC 2 in 2 limbs OR monoplegia (0-1 in one limb)
    if sum(1 for x in limbs if x <= 2) == 2:
        return 4
    if any(x <= 1 for x in limbs):  # monoplegia
        return 4
    # Moderate tetraparesis: BMRC 3 in ≥3 limbs
    if sum(1 for x in limbs if x <= 3) >= 3:
        return 4

    # Severe monoparesis exceeding the FS-3 limit (matches JS engine):
    # FS 3 "severe monoparesis" is officially "BMRC <=2 in ONE muscle group".
    # A single limb with BMRC <=2 in >=2 muscle groups (but not a full
    # monoplegia, which is already caught above) exceeds that limit ->
    # per the Neurostatus "if you exceed one level, take the next" rule -> FS 4.
    # Forum training case: RLE 2/5 all groups + RUE 3/5 all groups -> FS 4.
    ue_muscles = ["deltoid", "biceps", "triceps", "wflex", "wext"]
    le_muscles = ["hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]
    def _leq2_in_limb(muscles, side):
        return sum(1 for m in muscles
                   if _safe(strength.get(m, {}).get(side, 5), 5) <= 2)
    if (_leq2_in_limb(ue_muscles, "R") >= 2 or
        _leq2_in_limb(ue_muscles, "L") >= 2 or
        _leq2_in_limb(le_muscles, "R") >= 2 or
        _leq2_in_limb(le_muscles, "L") >= 2):
        return 4

    # Mild-to-moderate paraparesis or hemiparesis:
    # BMRC 3 in 1-2 groups OR BMRC ≤2 in 1 muscle group
    n_grade3_or_less = sum(1 for v in muscle_min.values() if v <= 3)
    if n_grade3_or_less >= 1:
        return 3
    # Or BMRC 4 in >2 groups
    n_grade4 = sum(1 for v in muscle_min.values() if v == 4)
    if n_grade4 > 2:
        return 3

    # Minimal disability: BMRC 4 in 1-2 groups
    if n_grade4 >= 1:
        return 2

    # Minimal disability: motor fatigability / reduced performance in
    # strenuous motor tasks (BMRC 5/5 everywhere) -> Pyramidal FS = 2.
    # Per Neurostatus Forum (11.07.2014, 29.11.2007): fatigability alone
    # scores FS 2, not FS 1. Overall motor performance subscore = 1.
    if _safe(overall_motor, 0) >= 1:
        return 2

    return 0


# ============================================================
# Cerebellar FS (Fouad Fig 3 decision tree + Neurostatus)
# ============================================================

def calc_cerebellar_fs(
    head_tremor: Optional[int] = None,    # 0-3
    truncal_ataxia: Optional[int] = None, # 0-4
    tremor_ue_R: Optional[int] = None,    # 0-4
    tremor_ue_L: Optional[int] = None,
    tremor_le_R: Optional[int] = None,
    tremor_le_L: Optional[int] = None,
    rapid_ue_R: Optional[int] = None,
    rapid_ue_L: Optional[int] = None,
    rapid_le_R: Optional[int] = None,
    rapid_le_L: Optional[int] = None,
    tandem: Optional[int] = None,         # 0-2
    gait_ataxia: Optional[int] = None,    # 0-4
    romberg: Optional[int] = None,        # 0-3
    pyr_weakness_interferes: bool = False,
) -> int:
    """
    Cerebellar FS (0-5) per Neurostatus:
    0: normal
    1: signs only (mild abnormality)
    2: mild ataxia OR moderate Romberg OR tandem walking not possible
    3: moderate limb ataxia OR moderate-severe gait/truncal ataxia
    4: severe gait/truncal ataxia AND severe ataxia in 3-4 limbs
    5: unable to perform coordinated movements (severe in all)

    X marker added externally if pyramidal weakness interferes.
    """
    # Worst limb tremor/dysmetria (0-4)
    limb_tremor = _safe(_max_or_none(
        tremor_ue_R, tremor_ue_L, tremor_le_R, tremor_le_L,
    ), 0)

    # Worst rapid alternating
    limb_rapid = _safe(_max_or_none(
        rapid_ue_R, rapid_ue_L, rapid_le_R, rapid_le_L,
    ), 0)
    limb_overall = max(limb_tremor, limb_rapid)

    # Per-limb ataxia severity = worse of tremor/dysmetria and rapid-alternating.
    # "Severe" per Neurostatus 04/10.2 = grade 4 (marked), matching the JS engine.
    def _p(t, r):
        return max(_safe(t, 0), _safe(r, 0))
    per_limb = [
        _p(tremor_ue_R, rapid_ue_R),
        _p(tremor_ue_L, rapid_ue_L),
        _p(tremor_le_R, rapid_le_R),
        _p(tremor_le_L, rapid_le_L),
    ]
    n_limbs_severe = sum(1 for v in per_limb if v >= 4)

    gait = _safe(gait_ataxia, 0)
    trunc = _safe(truncal_ataxia, 0)

    # RULE (Neurostatus 04/10.2 - Cerebellar FS), mirrors calcCerebellarFS in
    # index.html:
    #   5 = unable to perform coordinated movements (proxy: >=3 SEVERE limbs
    #       AND severe gait AND severe truncal)
    #   4 = SEVERE gait/truncal ataxia AND SEVERE ataxia in three or four limbs
    #   3 = moderate limb ataxia and/or moderate-or-severe gait/truncal ataxia
    #       (severe gait/truncal ALONE, without severe ataxia in 3-4 limbs, = 3)
    if n_limbs_severe >= 3 and gait >= 4 and trunc >= 4:
        return 5
    if n_limbs_severe >= 3 and (gait >= 4 or trunc >= 4):
        return 4
    if limb_overall >= 3 or gait >= 3 or trunc >= 3:
        return 3

    # Mild ataxia OR moderate Romberg OR tandem not possible
    if (limb_overall == 2
            or _safe(romberg, 0) >= 2
            or _safe(tandem, 0) >= 2
            or trunc == 2 or gait == 2):
        return 2

    # Signs only (any mild finding)
    if (limb_overall >= 1
            or _safe(romberg, 0) >= 1
            or _safe(tandem, 0) >= 1
            or _safe(head_tremor, 0) >= 1
            or trunc >= 1 or gait >= 1):
        return 1

    return 0


# ============================================================
# Sensory FS (Fouad Fig 4 + Fig 5 + combination rule)
# ============================================================

def _superficial_score(sup_ue_R, sup_ue_L, sup_trunk_R, sup_trunk_L,
                      sup_le_R, sup_le_L) -> int:
    """
    Superficial sensation algorithm (Fouad Fig 4):
    0: all normal
    1: signs only in 1-2 limbs (max=1)
    2: mild decrease (max=2) in 1-2 limbs
    3: moderate (max=3) in 1-2 limbs OR mild in 3-4 limbs
    4: marked (max=4) in 1-2 limbs OR moderate in >2 limbs
    5: complete loss (max=5) in 1-2 limbs OR marked in >2 limbs
    """
    # Per-region max (UE, trunk, LE) - but for "limb" counting we use UE+LE × R/L
    # Treat trunk separately. Assume "limb count" means UE_R, UE_L, LE_R, LE_L.
    limbs = [_safe(sup_ue_R, 0), _safe(sup_ue_L, 0),
             _safe(sup_le_R, 0), _safe(sup_le_L, 0)]
    trunk_max = max(_safe(sup_trunk_R, 0), _safe(sup_trunk_L, 0))
    overall_max = max(*limbs, trunk_max)

    if overall_max == 0:
        return 0
    n_limbs_at_max = sum(1 for x in limbs if x == overall_max)
    n_limbs_above_2 = sum(1 for x in limbs if x >= 2)
    n_limbs_above_3 = sum(1 for x in limbs if x >= 3)

    if overall_max >= 5:
        return 5
    if overall_max == 4:
        return 4 if n_limbs_at_max <= 2 else 5
    if overall_max == 3:
        # moderate in 1-2 → 3; in >2 → 4
        return 3 if n_limbs_at_max <= 2 else 4
    if overall_max == 2:
        # mild in 1-2 → 2; in 3-4 → 3
        return 2 if n_limbs_above_2 <= 2 else 3
    if overall_max == 1:
        return 1
    return 0


def _deep_score(vib_ue_R, vib_ue_L, vib_le_R, vib_le_L,
                pos_ue_R, pos_ue_L, pos_le_R, pos_le_L) -> int:
    """
    Deep sensation algorithm (Fouad Fig 5):
    Considers vibration (0-3) and position (0-3) per limb.
    0: normal
    1: mild vibration loss in 1-2 limbs
    2: moderate vibration in 1-2 OR mild in >2 OR mild position
    3: vibration lost in 1-2 OR moderate in >2 OR moderate position
    4: position loss (proprioception) in 1-2 OR severe vibration in >2
    5: position loss in >2 limbs
    """
    vib_limbs = [_safe(vib_ue_R, 0), _safe(vib_ue_L, 0),
                 _safe(vib_le_R, 0), _safe(vib_le_L, 0)]
    pos_limbs = [_safe(pos_ue_R, 0), _safe(pos_ue_L, 0),
                 _safe(pos_le_R, 0), _safe(pos_le_L, 0)]

    pos_max = max(pos_limbs)
    n_pos_severe = sum(1 for x in pos_limbs if x >= 3)
    n_pos_moderate = sum(1 for x in pos_limbs if x >= 2)

    vib_max = max(vib_limbs)
    n_vib_max = sum(1 for x in vib_limbs if x == vib_max)
    n_vib_severe = sum(1 for x in vib_limbs if x >= 3)

    if pos_max >= 3:
        return 5 if n_pos_severe > 2 else 4
    if pos_max == 2:
        return 3 if n_pos_moderate > 2 else 3
    if pos_max == 1:
        # mild proprioception
        return 2

    # No proprioception loss; rely on vibration
    if vib_max >= 3:
        return 3 if n_vib_severe <= 2 else 4
    if vib_max == 2:
        return 2 if n_vib_max <= 2 else 3
    if vib_max == 1:
        return 1
    return 0


def calc_sensory_fs(
    sup_ue_R: Optional[int] = None, sup_ue_L: Optional[int] = None,
    sup_trunk_R: Optional[int] = None, sup_trunk_L: Optional[int] = None,
    sup_le_R: Optional[int] = None, sup_le_L: Optional[int] = None,
    vib_ue_R: Optional[int] = None, vib_ue_L: Optional[int] = None,
    vib_le_R: Optional[int] = None, vib_le_L: Optional[int] = None,
    pos_ue_R: Optional[int] = None, pos_ue_L: Optional[int] = None,
    pos_le_R: Optional[int] = None, pos_le_L: Optional[int] = None,
) -> int:
    """
    Sensory FS (0-6) per Fouad 2023:
    Superficial subscore (0-5) AND deep subscore (0-5).
    Final = max of the two, with combination exception:
    - if superficial=4 AND deep=4 → final=5
    - if superficial=5 AND deep=5 → final=6
    """
    sup = _superficial_score(sup_ue_R, sup_ue_L, sup_trunk_R, sup_trunk_L,
                             sup_le_R, sup_le_L)
    deep = _deep_score(vib_ue_R, vib_ue_L, vib_le_R, vib_le_L,
                       pos_ue_R, pos_ue_L, pos_le_R, pos_le_L)
    if sup >= 5 and deep >= 5:
        return 6
    if sup == 4 and deep == 4:
        return 5
    return max(sup, deep)


# ============================================================
# Bowel & Bladder FS (Fouad Table 2 + special rule)
# ============================================================

def calc_bb_fs(
    hesitancy: Optional[int] = None,   # 0-4
    urgency: Optional[int] = None,     # 0-4
    catheterisation: Optional[int] = None,  # 0-2 (0=none, 1=intermittent, 2=constant)
    bowel: Optional[int] = None,       # 0-4
) -> int:
    """
    Bowel/Bladder FS (Neurostatus 04/10.2). Matches calcBBFS in index.html.

    Definitions:
      loss of BLADDER function = hesitancy 4 (overflow) OR urgency 4 (loss of control)
      loss of BOWEL   function = bowel 4 (complete loss)

    Grades:
      6 = loss of BOTH bladder and bowel
      5 = loss of EITHER bladder or bowel
      4 = almost constant catheterisation (c=2)
      3 = requires cath / frequent incontinence / needs enemata / intermittent
          self-cath (h/u/b >= 3 or c >= 1)
      2 = moderate hesitancy / urgency / constipation (h/u/b >= 2)
      1 = mild (h/u/b >= 1)
      0 = normal
    """
    h = _safe(hesitancy, 0)
    u = _safe(urgency, 0)
    c = _safe(catheterisation, 0)
    b = _safe(bowel, 0)

    bladder_loss = (h >= 4 or u >= 4)
    bowel_loss = (b >= 4)
    if bladder_loss and bowel_loss:
        return 6
    if bladder_loss or bowel_loss:
        return 5
    if c >= 2:
        return 4
    if h >= 3 or u >= 3 or b >= 3 or c >= 1:
        return 3
    if h >= 2 or u >= 2 or b >= 2:
        return 2
    if h >= 1 or u >= 1 or b >= 1:
        return 1
    return 0


def bb_fs_converted(bb_fs: int) -> int:
    """Convert B/B FS to EDSS-input scale per Neurostatus."""
    # 0→0, 1→1, 2→2, 3→3, 4→3, 5→4, 6→5  (Neurostatus)
    return [0, 1, 2, 3, 3, 4, 5][min(bb_fs, 6)]


# ============================================================
# Cerebral FS
# ============================================================

def calc_cerebral_fs(
    mentation: Optional[int] = None,   # 0-5
    fatigue: Optional[int] = None,     # 0-3
    depression: Optional[int] = None,  # 0-1 (does not contribute)
    euphoria: Optional[int] = None,    # 0-1 (does not contribute)
) -> int:
    """
    Cerebral FS for the EDSS step (Neurostatus manual, cerebral FS):
    = the higher of mentation and fatigue, where mild fatigue = 1 and
    moderate or severe fatigue = 2.
    Depression / euphoria alone give Cerebral FS 1 on the sheet but do not
    contribute to the step (see cerebral_mood_only); they never raise this value.
    """
    m = _safe(mentation, 0)
    f = _safe(fatigue, 0)
    f_grade = 2 if f >= 2 else (1 if f >= 1 else 0)
    return max(m, f_grade)


def cerebral_mood_only(cerebral_fs: int, depression=None, euphoria=None) -> bool:
    """Neurostatus manual: depression and/or euphoria alone -> Cerebral FS 1 on the sheet, not counted in the step."""
    return cerebral_fs == 0 and (_safe(depression, 0) >= 1 or _safe(euphoria, 0) >= 1)


# ============================================================
# Final EDSS step (Fouad Fig 6-8 + Neurostatus + ambulation override)
# ============================================================

@dataclass
class FSScores:
    """Bundle of all FS scores for EDSS calculation."""
    visual: int = 0       # CONVERTED (0-4) - for EDSS step input
    brainstem: int = 0    # 0-5
    pyramidal: int = 0    # 0-6
    cerebellar: int = 0   # 0-5
    sensory: int = 0      # 0-6
    bb: int = 0           # CONVERTED (0-5)
    cerebral: int = 0     # 0-5

    def to_list(self):
        return [self.visual, self.brainstem, self.pyramidal,
                self.cerebellar, self.sensory, self.bb, self.cerebral]


# Ambulation score → EDSS step mapping (Neurostatus)
# AS 0 = unrestricted, AS 1 = >500m fully ambulatory, AS 2 = 300-499m,
# AS 3 = 200-299m, AS 4 = 100-199m, AS 5 = <100m unaided,
# AS 6 = unilateral assistance ≥120m, AS 7 = bilateral ≥120m,
# AS 8 = unilateral <50m, AS 9 = bilateral 5-120m,
# AS 10 = wheelchair (no help), AS 11 = wheelchair (with help),
# AS 12 = bed-bound, can use arms
# AS 13 = in bed much of the day, some arm use; AS 14 = helpless, can communicate and eat;
# AS 15 = cannot communicate effectively or eat/swallow
AS_TO_EDSS_FLOOR = {
    0: 0.0, 1: 2.0, 2: 4.5, 3: 5.0, 4: 5.5,
    5: 6.0, 6: 6.0, 7: 6.0, 8: 6.5, 9: 6.5,
    10: 7.0, 11: 7.5, 12: 8.0, 13: 8.5, 14: 9.0, 15: 9.5,
}


def _fs_only_step(fs_list) -> float:
    """
    EDSS step from the FS pattern alone (Neurostatus 04/10.2 definitions, Kurtzke 1983).
    Mirrors _fsOnlyStep in index.html exactly. The pattern alone never exceeds 5.0
    ("EDSS steps 5.5 to 8.0 are exclusively defined by the ability to ambulate"); a FS
    grade 6 forces 6.0 ("the EDSS step should not be lower than any individual FS",
    visual and bowel/bladder enter already converted).
    """
    N = max(fs_list)
    if N == 0:
        return 0.0
    n_n = sum(1 for v in fs_list if v == N)
    rest = [v for v in fs_list if v != N]
    any_gt1 = any(v > 1 for v in rest)

    if N == 1:
        return 1.5 if n_n >= 2 else 1.0

    if N == 2:
        if n_n >= 5:
            return 3.5           # five FS grade 2 (Neurostatus 3.5)
        if n_n == 1:
            return 2.0
        if n_n == 2:
            return 3.0 if any_gt1 else 2.5
        return 3.5 if any_gt1 else 3.0   # three or four FS grade 2

    if N == 3:
        n_twos = sum(1 for v in rest if v == 2)
        if n_n == 1:
            return 3.0 if n_twos == 0 else (3.5 if n_twos <= 2 else 4.0)
        if n_n == 2:
            return 4.0 if any_gt1 else 3.5
        return 4.5 if any_gt1 else 4.0

    if N == 4:
        if n_n == 1:
            n_gt1 = sum(1 for v in rest if v > 1)
            if n_gt1 == 0:
                return 4.0
            if n_gt1 == 1:
                return 4.5
            return 5.0
        return 5.0

    if N == 5:
        return 5.0

    return 6.0


def calc_edss_step(fs: FSScores, ambulation_score: Optional[int] = None) -> float:
    """
    Calculate the final EDSS step (0.0 to 10.0).

    Algorithm (Neurostatus + Fouad Fig 6-8):

    EDSS 0 - 4.0  → driven primarily by FS pattern (patient fully ambulatory)
    EDSS 4.0-5.5  → BOTH FS scores AND ambulation contribute; the more severe
                    parameter wins (e.g., FS=2 + AS=3 still gives EDSS 5.0)
    EDSS 6.0+     → driven primarily by ambulation/walking aids alone

    Ambulation Score (AS) ranges:
      0  = Unrestricted
      1  = >500m without aid (fully ambulatory but not unrestricted)
      2  = 300-499m
      3  = 200-299m
      4  = 100-199m
      5  = <100m without aid
      6  = Unilateral aid ≥120m
      7  = Bilateral aid ≥120m
      8  = Unilateral aid <50m
      9  = Bilateral aid 5-120m
      10 = Wheelchair without help
      11 = Wheelchair with help
      12 = Bedbound, can use arms

    Returns:
        EDSS step as a float (e.g. 3.5, 6.0)
    """
    fs_list = fs.to_list()
    AS = _safe(ambulation_score, 0)

    # ---------- High AS (6.0+): ambulation alone ----------
    if AS >= 12:
        return AS_TO_EDSS_FLOOR[min(AS, 15)]
    if AS == 11:
        return 7.5
    if AS == 10:
        return 7.0
    if AS in (8, 9):
        return 6.5
    if AS in (6, 7):
        return 6.0
    if AS == 5:
        return 6.0  # walking range <100m, no aid → EDSS 6.0

    # ---------- Mid range (4.0-5.5): FS and AS combine ----------
    # AS dictates a floor; FS pattern can push higher if it implies more disability
    fs_step = _fs_only_step(fs_list)

    if AS == 4:
        # 100-199m → EDSS 5.5 (FS doesn't override down)
        return max(5.5, fs_step)

    if AS == 3:
        # 200-299m → EDSS 5.0 floor; FS can push higher (e.g. FS=6 → 6.0)
        return max(5.0, fs_step)

    if AS == 2:
        # 300-499m → EDSS 4.5 floor
        return max(4.5, fs_step)

    if AS == 1:
        # >=500m without aid but not unrestricted -> FS pattern drives EDSS.
        # Per Neurostatus Forum (20.07.2009, 07.03.2009): fully ambulatory
        # but restricted spans EDSS 2.0-5.0 depending on FS scores; there
        # is no hard 4.0 floor. Floor of 2.0 matches JS engine.
        return max(2.0, fs_step)

    # AS == 0: fully unrestricted → FS pattern alone determines
    return fs_step


# ============================================================
# Top-level convenience function
# ============================================================

def calculate_full_edss(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Take a dict of all raw inputs (matching the PDF field names) and
    return a dict with all FS scores and the final EDSS.

    Expected keys (all optional, default 0/None):
      Visual: v_va_od, v_va_os, v_vf_od, v_vf_os, v_scotoma_R, v_scotoma_L,
              v_pallor_od, v_pallor_os
      Brainstem: b_eom, b_nys, b_trig, b_face, b_hear, b_dysarth, b_dysphag, b_othercn
      Pyramidal: p_str_<muscle>_R/L, p_overall, p_spast_arms_R/L, p_spast_legs_R/L
      Cerebellar: c_head, c_trunc, c_tremor_*_R/L, c_rapid_*_R/L,
                  c_tandem, c_gait_ataxia, c_romberg
      Sensory: s_sup_*_R/L, s_vib_*_R/L, s_pos_*_R/L
      B/B: bb_hes, bb_urg, bb_cath, bb_bowel
      Cerebral: m_ment, m_fat, m_depress, m_euph
      Ambulation: a_score (0-12)

    Returns:
      {
        'visual_fs': raw 0-6,
        'visual_fs_conv': converted 0-4,
        'brainstem_fs': 0-5,
        'pyramidal_fs': 0-6,
        'cerebellar_fs': 0-5,
        'sensory_fs': 0-6,
        'bb_fs': raw 0-5,
        'bb_fs_conv': converted 0-5,
        'cerebral_fs': 0-5,
        'ambulation_score': 0-12,
        'edss_step': 0.0-10.0,
      }
    """
    g = inputs.get  # shorthand

    # --- Visual ---
    visual_fs = calc_visual_fs(
        va_od=g("v_va_od"), va_os=g("v_va_os"),
        vf_od=g("v_vf_od"), vf_os=g("v_vf_os"),
        scotoma_od=g("v_scotoma_R"), scotoma_os=g("v_scotoma_L"),
        pallor_od=g("v_pallor_od"), pallor_os=g("v_pallor_os"),
    )
    visual_fs_conv = visual_fs_converted(visual_fs)

    # --- Brainstem ---
    brainstem_fs = calc_brainstem_fs(
        eom=g("b_eom"), nystagmus=g("b_nys"), trigeminal=g("b_trig"),
        facial=g("b_face"), hearing=g("b_hear"),
        dysarthria=g("b_dysarth"), dysphagia=g("b_dysphag"),
        other_cn=g("b_othercn"),
    )

    # --- Pyramidal ---
    strength = {}
    for m in MUSCLE_KEYS:
        r_key = f"p_str_{m}_R"
        l_key = f"p_str_{m}_L"
        if r_key in inputs or l_key in inputs:
            strength[m] = {"R": _safe(g(r_key), 5), "L": _safe(g(l_key), 5)}
    pyramidal_fs = calc_pyramidal_fs(
        strength=strength,
        overall_motor=g("p_overall"),
        spast_arms_max=max(_safe(g("p_spast_arms_R"), 0),
                           _safe(g("p_spast_arms_L"), 0)),
        spast_legs_max=max(_safe(g("p_spast_legs_R"), 0),
                           _safe(g("p_spast_legs_L"), 0)),
    )

    # --- Cerebellar ---
    cerebellar_fs = calc_cerebellar_fs(
        head_tremor=g("c_head"), truncal_ataxia=g("c_trunc"),
        tremor_ue_R=g("c_tremor_ue_R"), tremor_ue_L=g("c_tremor_ue_L"),
        tremor_le_R=g("c_tremor_le_R"), tremor_le_L=g("c_tremor_le_L"),
        rapid_ue_R=g("c_rapid_ue_R"), rapid_ue_L=g("c_rapid_ue_L"),
        rapid_le_R=g("c_rapid_le_R"), rapid_le_L=g("c_rapid_le_L"),
        tandem=g("c_tandem"), gait_ataxia=g("c_gait_ataxia"),
        romberg=g("c_romberg"),
    )

    # --- Sensory ---
    sensory_fs = calc_sensory_fs(
        sup_ue_R=g("s_sup_ue_R"), sup_ue_L=g("s_sup_ue_L"),
        sup_trunk_R=g("s_sup_trunk_R"), sup_trunk_L=g("s_sup_trunk_L"),
        sup_le_R=g("s_sup_le_R"), sup_le_L=g("s_sup_le_L"),
        vib_ue_R=g("s_vib_ue_R"), vib_ue_L=g("s_vib_ue_L"),
        vib_le_R=g("s_vib_le_R"), vib_le_L=g("s_vib_le_L"),
        pos_ue_R=g("s_pos_ue_R"), pos_ue_L=g("s_pos_ue_L"),
        pos_le_R=g("s_pos_le_R"), pos_le_L=g("s_pos_le_L"),
    )

    # --- B/B ---
    bb_fs = calc_bb_fs(
        hesitancy=g("bb_hes"), urgency=g("bb_urg"),
        catheterisation=g("bb_cath"), bowel=g("bb_bowel"),
    )
    bb_fs_conv = bb_fs_converted(bb_fs)

    # --- Cerebral ---
    cerebral_fs_step = calc_cerebral_fs(
        mentation=g("m_ment"), fatigue=g("m_fat"),
        depression=g("m_depress"), euphoria=g("m_euph"),
    )
    mood_only = cerebral_mood_only(cerebral_fs_step, g("m_depress"), g("m_euph"))
    cerebral_fs = 1 if mood_only else cerebral_fs_step   # sheet value

    # --- Ambulation ---
    ambulation_score = _safe(g("a_score"), 0)

    # --- Final EDSS ---
    fs_bundle = FSScores(
        visual=visual_fs_conv, brainstem=brainstem_fs,
        pyramidal=pyramidal_fs, cerebellar=cerebellar_fs,
        sensory=sensory_fs, bb=bb_fs_conv, cerebral=cerebral_fs_step,
    )
    edss = calc_edss_step(fs_bundle, ambulation_score)

    return {
        "visual_fs": visual_fs,
        "visual_fs_conv": visual_fs_conv,
        "brainstem_fs": brainstem_fs,
        "pyramidal_fs": pyramidal_fs,
        "cerebellar_fs": cerebellar_fs,
        "sensory_fs": sensory_fs,
        "bb_fs": bb_fs,
        "bb_fs_conv": bb_fs_conv,
        "cerebral_fs": cerebral_fs,
        "cerebral_fs_step": cerebral_fs_step,
        "cerebral_mood_only": mood_only,
        "ambulation_score": ambulation_score,
        "edss_step": edss,
    }


if __name__ == "__main__":
    # Quick sanity check
    test_input = {
        "p_str_deltoid_R": 5, "p_str_deltoid_L": 5,
        "p_str_biceps_R": 5,  "p_str_biceps_L": 4,
        "c_gait_ataxia": 1,
        "s_vib_le_R": 1, "s_vib_le_L": 1,
        "m_ment": 0, "m_fat": 1,
        "a_score": 0,
    }
    result = calculate_full_edss(test_input)
    for k, v in result.items():
        print(f"  {k:20s}: {v}")
