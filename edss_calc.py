"""
AutoEDSSguide — EDSS Calculation Engine
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
# Visual FS (already 0-4 in Fouad's algorithm — no conversion needed)
# ============================================================

# Snellen 20/20 → 0, 20/30 → 1, 20/60 → 2, 20/100 → 3, 20/200 → 4, worse → 5
SNELLEN_LOOKUP = {
    "20/20": 0, "20/25": 0, "20/30": 1,
    "20/40": 1, "20/50": 1, "20/60": 2,
    "20/70": 2, "20/80": 2, "20/100": 3,
    "20/200": 4, "20/400": 5, "CF": 5,  # Counting fingers
    "HM": 5, "LP": 5, "NLP": 6,         # Hand motion / Light perception / No LP
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
    # Per-eye worst score from VA / VF / scotoma
    od_score = max(
        snellen_to_score(va_od),
        _safe(vf_od),
        _safe(scotoma_od),
    )
    os_score = max(
        snellen_to_score(va_os),
        _safe(vf_os),
        _safe(scotoma_os),
    )
    worse = max(od_score, os_score)
    better = min(od_score, os_score)

    # Apply Neurostatus rules for the combination
    if worse == 0:
        return 0
    if worse <= 1:
        return 1
    if worse == 2:
        return 2
    if worse == 3:
        return 3
    if worse == 4 and better >= 3:
        return 4
    if worse == 4:
        return 3  # only one eye affected
    if worse == 5 and better >= 4:
        return 5
    if worse == 5:
        return 4
    # worse >= 6
    if better >= 5:
        return 6
    return 5


def visual_fs_converted(visual_fs: int) -> int:
    """Convert Visual FS (0-6) to EDSS-input scale (0-4) per Neurostatus."""
    return [0, 1, 2, 3, 3, 4, 5][min(visual_fs, 6)]


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
# Pyramidal FS (BMRC distribution rules — Fouad Fig 2 + Neurostatus)
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
    1: signs without disability — overall_motor=1 (fatigability)
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

    # Signs without disability (motor fatigability)
    if _safe(overall_motor, 0) >= 1:
        return 1

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
    n_limbs_severe = sum(
        1 for v in [tremor_ue_R, tremor_ue_L, tremor_le_R, tremor_le_L]
        if _safe(v, 0) >= 3
    )

    # Worst rapid alternating
    limb_rapid = _safe(_max_or_none(
        rapid_ue_R, rapid_ue_L, rapid_le_R, rapid_le_L,
    ), 0)
    limb_overall = max(limb_tremor, limb_rapid)

    gait = _safe(gait_ataxia, 0)
    trunc = _safe(truncal_ataxia, 0)

    # Severe in 3+ limbs AND severe gait/truncal → 4
    if n_limbs_severe >= 3 and (gait >= 3 or trunc >= 3):
        return 4
    # Unable to perform coordinated → 5 (max in everything)
    if limb_overall >= 4 and gait >= 4 and trunc >= 4:
        return 5

    # Moderate limb ataxia OR moderate-severe gait/truncal
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
    # Per-region max (UE, trunk, LE) — but for "limb" counting we use UE+LE × R/L
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
    B/B FS (Fouad Table 2):
    Max of subscores. If 4 in urgency + bowel + (one more), score = 5.
    Range 0-5 (already converted, no further conversion needed for EDSS).
    """
    h = _safe(hesitancy, 0)
    u = _safe(urgency, 0)
    c = _safe(catheterisation, 0)
    b = _safe(bowel, 0)

    base_max = max(h, u, c * 2, b)  # catheterisation 2 = grade 4 equivalent

    # Special rule: 4 in urinary urgency + bowel dysfunction → 5
    severe_count = sum(1 for x in [h, u, b] if x >= 4)
    if severe_count >= 2 and c >= 1:
        return 5
    if u >= 4 and b >= 4:
        return 5

    return min(base_max, 5)


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
    Cerebral FS = Mentation score (0-5).
    Fatigue contributes only if mentation = 0:
    - 0 mentation + 0 fatigue → 0
    - 0 mentation + ≥1 fatigue → 1 (signs only)
    - mentation = 1 → 1 (signs only)
    - mentation = 2 → 2 (mild + maybe fatigue)
    - mentation = 3-5 → same value
    Depression / euphoria documented but do not contribute.
    """
    m = _safe(mentation, 0)
    f = _safe(fatigue, 0)
    if m == 0 and f >= 1:
        return 1
    return m


# ============================================================
# Final EDSS step (Fouad Fig 6-8 + Neurostatus + ambulation override)
# ============================================================

@dataclass
class FSScores:
    """Bundle of all FS scores for EDSS calculation."""
    visual: int = 0       # CONVERTED (0-4) — for EDSS step input
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
AS_TO_EDSS_FLOOR = {
    0: 0.0, 1: 4.0, 2: 4.5, 3: 5.0, 4: 5.5,
    5: 6.0, 6: 6.0, 7: 6.0, 8: 6.5, 9: 6.5,
    10: 7.0, 11: 7.5, 12: 8.0,
}


def _fs_only_step(fs_list) -> float:
    """
    Compute EDSS step from FS pattern alone (assumes patient is unrestricted).
    Used when AS == 0. Returns EDSS in range 0.0 - 6.0.
    """
    N = max(fs_list)
    if N == 0:
        return 0.0

    if N == 1:
        n_ones = sum(1 for v in fs_list if v == 1)
        return 1.0 if n_ones == 1 else 1.5

    if N == 2:
        n_fs_2 = sum(1 for v in fs_list if v == 2)
        # Special: 5 FSs of grade 2 → 5.0 (Fouad exception)
        if n_fs_2 >= 5:
            return 5.0
        if n_fs_2 == 1:
            return 2.0
        if n_fs_2 == 2:
            return 2.5
        return 3.0  # 3 or 4

    if N == 3:
        k = sum(1 for v in fs_list if v == 3)
        n_twos = sum(1 for v in fs_list if v == 2)
        if k == 1 and n_twos == 0:
            return 3.0
        if k == 1:
            return 3.5
        if k == 2:
            return 3.5
        return 4.0  # k >= 3

    if N == 4:
        return 4.0

    if N == 5:
        return 5.0

    if N >= 6:
        return 6.0

    return float(N)


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
        return 8.0
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
        # >500m but not unrestricted → EDSS 4.0 floor
        return max(4.0, fs_step)

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
    cerebral_fs = calc_cerebral_fs(
        mentation=g("m_ment"), fatigue=g("m_fat"),
        depression=g("m_depress"), euphoria=g("m_euph"),
    )

    # --- Ambulation ---
    ambulation_score = _safe(g("a_score"), 0)

    # --- Final EDSS ---
    fs_bundle = FSScores(
        visual=visual_fs_conv, brainstem=brainstem_fs,
        pyramidal=pyramidal_fs, cerebellar=cerebellar_fs,
        sensory=sensory_fs, bb=bb_fs_conv, cerebral=cerebral_fs,
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
