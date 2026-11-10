"""
MSpectrum AutoEDSSguide - EDSS calculation engine (Python reference)
====================================================================

Pure Python port of the JavaScript engine in index.html (calculateFullEDSS and
the functions it calls). Kept line-by-line in sync with the JS engine (currently
"MSpectrum scoring rules v3.4", MSpectrum v36) and locked by tests/parity_check.py, which runs
the same inputs through both engines and requires identical results.

Scoring sources:
- Kurtzke JF. Neurology 1983;33:1444-52 (EDSS, Functional Systems).
- Standardized scoring rules as published in Sen 2018 (Arch Neuropsychiatry) and Fouad et al. 2023 (Mult Scler J Exp Transl Clin).
- Fouad AM, Abdel Naseer M, Farghaly M, Hegazy MI. Mult Scler J Exp Transl Clin 2023;9(1):20552173231155055 (algorithmic combination rules).

MSpectrum is independent and is not affiliated with any rating-system owner.

Conventions:
- Inputs are integers (or None / "" when missing). Numeric strings are accepted.
- Per-side items use _R / _L suffixes.
- Findings flagged P (permanent) or T (temporary) as not due to MS must be removed
  from the input dict before calling calculate_full_edss (the web app does the same).
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass

ENGINE_VERSION = "MSpectrum scoring rules v3.4 (Kurtzke EDSS; published standardized rules)"


# ============================================================
# Helpers
# ============================================================

def _num(v):
    """Coerce numeric strings to numbers; leave other values unchanged."""
    if isinstance(v, str):
        t = v.strip()
        if t == "":
            return v
        try:
            f = float(t)
            return int(f) if f.is_integer() else f
        except ValueError:
            return v
    return v


def _is_nan(v) -> bool:
    return isinstance(v, float) and v != v


def _safe(v, default=0):
    """JS _safe: null/undefined/NaN -> default. "" is treated as missing too."""
    if v is None or _is_nan(v) or v == "":
        return default
    return _num(v)


def _max_or_none(*values) -> Optional[int]:
    vals = [_num(v) for v in values if v is not None and v != "" and not _is_nan(v)]
    return max(vals) if vals else None


def _first_val(*values):
    for v in values:
        if v is not None and v != "":
            return v
    return None


# ============================================================
# Visual FS
# ============================================================
SNELLEN_LOOKUP = {
    "20/20": 0,
    "20/25": 1,
    "20/30": 2, "20/40": 2, "20/50": 2,
    "20/60": 3, "20/70": 3, "20/80": 3,
    "20/100": 4, "20/200": 4,
    "20/400": 5, "CF": 5, "HM": 5, "LP": 5, "NLP": 5,
}


def snellen_to_score(snellen) -> int:
    if snellen is None or snellen == "" or snellen == "-":
        return 0
    return SNELLEN_LOOKUP.get(str(snellen).strip(), 0)


def calc_visual_fs(va_od=None, va_os=None, vf_od=None, vf_os=None,
                   scotoma_od=None, scotoma_os=None, pallor_od=None, pallor_os=None) -> int:
    # Fields: 0->0, 1->1, 2->3, 3->4. Scotoma: 0->0, 1->1, 2->3. Disc pallor present -> 1.
    field_conv = lambda v: [0, 1, 3, 4][min(_safe(v), 3)]
    scotoma_conv = lambda v: [0, 1, 3][min(_safe(v), 2)]
    od = max(snellen_to_score(va_od), field_conv(vf_od), scotoma_conv(scotoma_od), 1 if _safe(pallor_od) > 0 else 0)
    os_ = max(snellen_to_score(va_os), field_conv(vf_os), scotoma_conv(scotoma_os), 1 if _safe(pallor_os) > 0 else 0)
    worse = max(od, os_)
    # Kurtzke 1983: the bump depends on the ACUITY (20/60 or less) of the better (less affected) eye only.
    a_od, a_os = snellen_to_score(va_od), snellen_to_score(va_os)
    better_acuity = a_os if od > os_ else a_od if os_ > od else min(a_od, a_os)
    if worse <= 2:
        return worse
    return min(worse + 1, 6) if better_acuity >= 3 else worse


def visual_fs_converted(visual_fs: int) -> int:
    return [0, 1, 2, 2, 3, 3, 4][min(visual_fs, 6)]


# ============================================================
# Brainstem FS
# ============================================================
def calc_brainstem_fs(eom=None, nystagmus=None, trigeminal=None, facial=None,
                      hearing=None, dysarthria=None, dysphagia=None, other_cn=None) -> int:
    return _safe(_max_or_none(eom, nystagmus, trigeminal, facial, hearing, dysarthria, dysphagia, other_cn), 0)


# ============================================================
# Pyramidal FS
# ============================================================
MUSCLE_KEYS = [
    "deltoid", "biceps", "triceps", "wflex", "wext",
    "hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant",
]
UE_MUSCLES = ["deltoid", "biceps", "triceps", "wflex", "wext"]
LE_MUSCLES = ["hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]


def calc_pyramidal_fs(strength: Optional[Dict[str, Dict[str, int]]] = None,
                      overall_motor=None, plantar=None, reflexes=None,
                      spasticity=None, gait_spast=None, cutaneous=None,
                      spast_arms_max=None, spast_legs_max=None) -> int:
    """strength = {"deltoid": {"R": 5, "L": 4}, ...}. spast_arms_max/spast_legs_max are
    kept for backward compatibility and fill both sides when spasticity is not given."""
    strength = strength or {}
    side_val = lambda m, side: _num(strength[m][side]) if (m in strength and strength[m].get(side) is not None) else 5

    muscle_min = {}
    for m in MUSCLE_KEYS:
        if m in strength:
            muscle_min[m] = min(_safe(strength[m].get("R"), 5), _safe(strength[m].get("L"), 5))

    limb_min = lambda ms, side: min(side_val(m, side) for m in ms)
    limb_max = lambda ms, side: max(side_val(m, side) for m in ms)
    UE_R, UE_L = limb_min(UE_MUSCLES, "R"), limb_min(UE_MUSCLES, "L")
    LE_R, LE_L = limb_min(LE_MUSCLES, "R"), limb_min(LE_MUSCLES, "L")
    limbs = [UE_R, UE_L, LE_R, LE_L]
    # A limb is plegic only when ALL its muscles are 0-1.
    UE_Rp, UE_Lp = limb_max(UE_MUSCLES, "R") <= 1, limb_max(UE_MUSCLES, "L") <= 1
    LE_Rp, LE_Lp = limb_max(LE_MUSCLES, "R") <= 1, limb_max(LE_MUSCLES, "L") <= 1
    plegic = [UE_Rp, UE_Lp, LE_Rp, LE_Lp]

    def strength_grade():
        if all(plegic):
            return 6
        if LE_Rp and LE_Lp:
            return 5
        if (UE_Rp and LE_Rp) or (UE_Lp and LE_Lp):
            return 5
        if len([x for x in limbs if x <= 2]) >= 3:
            return 5
        if any(plegic):
            return 4
        if len([x for x in limbs if x <= 2]) == 2:
            return 4
        if len([x for x in limbs if x <= 3]) >= 3:
            return 4
        leq2 = lambda ms, side: sum(1 for m in ms if side_val(m, side) <= 2)
        if leq2(UE_MUSCLES, "R") >= 2 or leq2(UE_MUSCLES, "L") >= 2 or \
           leq2(LE_MUSCLES, "R") >= 2 or leq2(LE_MUSCLES, "L") >= 2:
            return 4
        vals = list(muscle_min.values())
        if len([v for v in vals if v <= 3]) >= 1:
            return 3
        if len([v for v in vals if v == 4]) > 2:
            return 3
        if len([v for v in vals if v == 4]) >= 1:
            return 2
        if _safe(overall_motor, 0) >= 1:
            return 2
        return 0

    plantar = plantar or {}
    babinski = _safe(plantar.get("R")) >= 2 or _safe(plantar.get("L")) >= 2
    brisk_or_clonus = any(_safe(v) >= 3 for v in (reflexes or {}).values())
    cut_absent = _safe(cutaneous) >= 2
    sign_floor = 1 if (babinski or brisk_or_clonus or cut_absent) else 0

    sp = dict(spasticity or {})
    if not sp and (spast_arms_max is not None or spast_legs_max is not None):
        sp = {"arms_R": spast_arms_max, "arms_L": spast_arms_max, "legs_R": spast_legs_max, "legs_L": spast_legs_max}
    gs = gait_spast or {}
    limb_spast = max(_safe(sp.get("arms_R")), _safe(sp.get("arms_L")), _safe(sp.get("legs_R")), _safe(sp.get("legs_L")))
    gait_sp = max(_safe(gs.get("R")), _safe(gs.get("L")))
    spast_floor = 0
    if limb_spast >= 1 or gait_sp >= 1:
        spast_floor = 1
    if gait_sp >= 2 or limb_spast >= 3:
        spast_floor = 2
    if gait_sp >= 3:
        spast_floor = 3

    return max(strength_grade(), sign_floor, spast_floor)


# ============================================================
# Cerebellar FS
# ============================================================
def calc_cerebellar_fs(head_tremor=None, truncal_ataxia=None,
                       tremor_ue_R=None, tremor_ue_L=None, tremor_le_R=None, tremor_le_L=None,
                       rapid_ue_R=None, rapid_ue_L=None, rapid_le_R=None, rapid_le_L=None,
                       tandem=None, gait_ataxia=None, romberg=None,
                       pyr_weakness_interferes: bool = False) -> int:
    """pyr_weakness_interferes is kept for backward compatibility; the X marker is
    reported separately and does not change the FS grade (same as the JS engine)."""
    limb_tremor = _safe(_max_or_none(tremor_ue_R, tremor_ue_L, tremor_le_R, tremor_le_L), 0)
    limb_rapid = _safe(_max_or_none(rapid_ue_R, rapid_ue_L, rapid_le_R, rapid_le_L), 0)
    limb_overall = max(limb_tremor, limb_rapid)
    per_limb = [
        max(_safe(tremor_ue_R), _safe(rapid_ue_R)), max(_safe(tremor_ue_L), _safe(rapid_ue_L)),
        max(_safe(tremor_le_R), _safe(rapid_le_R)), max(_safe(tremor_le_L), _safe(rapid_le_L)),
    ]
    n_severe = len([v for v in per_limb if v >= 4])
    gait, trunc = _safe(gait_ataxia), _safe(truncal_ataxia)
    if n_severe >= 3 and gait >= 4 and trunc >= 4:
        return 5
    if n_severe >= 3 and (gait >= 4 or trunc >= 4):
        return 4
    if limb_overall >= 3 or gait >= 3 or trunc >= 3:
        return 3
    if limb_overall == 2 or _safe(romberg) >= 2 or _safe(tandem) >= 2 or trunc == 2 or gait == 2:
        return 2
    if limb_overall >= 1 or _safe(romberg) >= 1 or _safe(tandem) >= 1 or \
       _safe(head_tremor) >= 1 or trunc >= 1 or gait >= 1:
        return 1
    return 0


# ============================================================
# Sensory FS
# ============================================================
def _superficial_score(sup_ue_R=None, sup_ue_L=None, sup_trunk_R=None, sup_trunk_L=None,
                       sup_le_R=None, sup_le_L=None) -> int:
    limbs = [_safe(sup_ue_R), _safe(sup_ue_L), _safe(sup_le_R), _safe(sup_le_L)]
    trunk = max(_safe(sup_trunk_R), _safe(sup_trunk_L))
    top = max(*limbs, trunk)
    if top == 0:
        return 0
    n_at_max = len([x for x in limbs if x == top])
    n_above_2 = len([x for x in limbs if x >= 2])
    if top >= 5:
        return 5
    if top == 4:
        return 4 if n_at_max <= 2 else 5
    if top == 3:
        return 3 if n_at_max <= 2 else 4
    if top == 2:
        return 2 if n_above_2 <= 2 else 3
    if top == 1:
        return 2 if n_at_max >= 3 else 1
    return 0


def _deep_score(vib_ue_R=None, vib_ue_L=None, vib_le_R=None, vib_le_L=None,
                pos_ue_R=None, pos_ue_L=None, pos_le_R=None, pos_le_L=None) -> int:
    vib = [_safe(vib_ue_R), _safe(vib_ue_L), _safe(vib_le_R), _safe(vib_le_L)]
    pos = [_safe(pos_ue_R), _safe(pos_ue_L), _safe(pos_le_R), _safe(pos_le_L)]
    pos_max = max(pos)
    n_pos_severe = len([x for x in pos if x >= 3])
    vib_max = max(vib)
    n_vib_max = len([x for x in vib if x == vib_max])
    n_vib_severe = len([x for x in vib if x >= 3])
    if pos_max >= 3:
        return 5 if n_pos_severe > 2 else 4
    if pos_max == 2:
        return 3
    if pos_max == 1:
        return 2
    if vib_max >= 3:
        return 3 if n_vib_severe <= 2 else 4
    if vib_max == 2:
        return 2
    if vib_max == 1:
        return 2 if n_vib_max >= 3 else 1
    return 0


def calc_sensory_fs(sup_ue_R=None, sup_ue_L=None, sup_trunk_R=None, sup_trunk_L=None,
                    sup_le_R=None, sup_le_L=None,
                    vib_ue_R=None, vib_ue_L=None, vib_le_R=None, vib_le_L=None,
                    pos_ue_R=None, pos_ue_L=None, pos_le_R=None, pos_le_L=None) -> int:
    sup = _superficial_score(sup_ue_R, sup_ue_L, sup_trunk_R, sup_trunk_L, sup_le_R, sup_le_L)
    deep = _deep_score(vib_ue_R, vib_ue_L, vib_le_R, vib_le_L, pos_ue_R, pos_ue_L, pos_le_R, pos_le_L)
    if sup >= 5 and deep >= 5:
        return 6
    if sup == 4 and deep == 4:
        return 5
    return max(sup, deep)


# ============================================================
# Bowel/Bladder FS
# ============================================================
def calc_bb_fs(hesitancy=None, urgency=None, catheterisation=None, bowel=None) -> int:
    h, u, c, b = _safe(hesitancy), _safe(urgency), _safe(catheterisation), _safe(bowel)
    bladder_loss = h >= 4 or u >= 4
    bowel_loss = b >= 4
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
    return [0, 1, 2, 3, 3, 4, 5][min(bb_fs, 6)]


# ============================================================
# Cerebral FS
# ============================================================
def calc_cerebral_fs(mentation=None, fatigue=None, depression=None, euphoria=None,
                     exclude_fatigue: bool = False) -> int:
    """FS step = worse of mentation and fatigue (mild 1, moderate/severe 2).
    Depression/euphoria never change the step (see cerebral_mood_only)."""
    m = _safe(mentation)
    f = 0 if exclude_fatigue else _safe(fatigue)
    return max(m, 2 if f >= 2 else (1 if f >= 1 else 0))


def cerebral_mood_only(cerebral_fs: int, depression=None, euphoria=None) -> bool:
    return cerebral_fs == 0 and (_safe(depression) >= 1 or _safe(euphoria) >= 1)


# ============================================================
# Ambulation Score and cerebellar X marker
# ============================================================
def calc_ambulation_score(assistance=None, distance_m=None, is_normal=False) -> Optional[int]:
    fixed = {"bed_nocomm": 15, "bed_helpless": 14, "bed_much": 13, "bedbound": 12,
             "wheelchair_help": 11, "wheelchair_indep": 10}
    if assistance in fixed:
        return fixed[assistance]
    d = _num(distance_m)
    if d is None or d == "" or isinstance(d, str) or _is_nan(d):
        d = None
    if assistance == "unilateral":
        if d is None:
            return 6
        return 6 if d > 50 else 8
    if assistance == "bilateral":
        if d is None:
            return 7  # conservative default (EDSS 6.0), same as the unilateral default
        return 7 if d > 120 else 9
    if assistance in (None, "", "none"):
        if is_normal is True:
            return 0
        if d is None:
            return None
        if d >= 500:
            return 1
        if d >= 300:
            return 2
        if d >= 200:
            return 3
        if d >= 100:
            return 4
        return 5
    return None


def should_suggest_cerebellar_x(strength, sensory_args) -> bool:
    strength = strength or {}
    sensory_args = sensory_args or {}
    for m in MUSCLE_KEYS:
        if m in strength:
            if _safe(strength[m].get("R"), 5) <= 3 or _safe(strength[m].get("L"), 5) <= 3:
                return True
    for k in ("pos_ue_R", "pos_ue_L", "pos_le_R", "pos_le_L"):
        if _safe(sensory_args.get(k), 0) >= 2:
            return True
    return False


# ============================================================
# Final EDSS step
# ============================================================
@dataclass
class FSScores:
    """Bundle of all FS scores for EDSS calculation."""
    visual: int = 0       # CONVERTED (0-4)
    brainstem: int = 0    # 0-5
    pyramidal: int = 0    # 0-6
    cerebellar: int = 0   # 0-5
    sensory: int = 0      # 0-6
    bb: int = 0           # CONVERTED (0-5)
    cerebral: int = 0     # 0-5 (step value; mood alone does not count)

    def to_list(self):
        return [self.visual, self.brainstem, self.pyramidal,
                self.cerebellar, self.sensory, self.bb, self.cerebral]


def _fs_only_step(fs_list) -> float:
    N = max(fs_list)
    if N == 0:
        return 0.0
    nN = fs_list.count(N)
    rest = [v for v in fs_list if v != N]
    any_gt1 = any(v > 1 for v in rest)
    if N == 1:
        return 1.5 if nN >= 2 else 1.0
    if N == 2:
        if nN >= 5:
            return 3.5
        if nN == 1:
            return 2.0
        if nN == 2:
            return 3.0 if any_gt1 else 2.5
        return 3.5 if any_gt1 else 3.0
    if N == 3:
        n_twos = rest.count(2)
        if nN == 1:
            return 3.0 if n_twos == 0 else (3.5 if n_twos <= 2 else 4.0)
        if nN == 2:
            return 4.0 if any_gt1 else 3.5
        return 4.5 if any_gt1 else 4.0
    if N == 4:
        if nN == 1:
            n_gt1 = len([v for v in rest if v > 1])
            if n_gt1 == 0:
                return 4.0
            if n_gt1 == 1:
                return 4.5
            return 5.0
        return 5.0
    if N == 5:
        return 5.0
    return 6.0


AS_FIXED_EDSS = {5: 6.0, 6: 6.0, 7: 6.0, 8: 6.5, 9: 6.5, 10: 7.0, 11: 7.5, 12: 8.0, 13: 8.5, 14: 9.0, 15: 9.5}
AS_FLOOR_EDSS = {1: 2.0, 2: 4.5, 3: 5.0, 4: 5.5}


def calc_edss_step(fs, ambulation_score: Optional[int] = None) -> float:
    fs_list = [_safe(v) for v in (fs.to_list() if hasattr(fs, "to_list") else
               [fs.get(k) for k in ("visual", "brainstem", "pyramidal", "cerebellar", "sensory", "bb", "cerebral")])]
    AS = _safe(ambulation_score)
    fs_step = _fs_only_step(fs_list)
    if AS >= 5:
        return AS_FIXED_EDSS[min(AS, 15)]
    if AS >= 1:
        return max(AS_FLOOR_EDSS[AS], fs_step)
    return fs_step


# ============================================================
# Top level
# ============================================================
def _truthy(v) -> bool:
    return v is True or v == "true" or v == 1


def calculate_full_edss(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Same input keys and outputs as calculateFullEDSS in index.html."""
    g = lambda k: _num(inputs.get(k))

    visual_fs = calc_visual_fs(inputs.get("v_va_od"), inputs.get("v_va_os"), g("v_vf_od"), g("v_vf_os"),
                               g("v_scotoma_R"), g("v_scotoma_L"), g("v_pallor_od"), g("v_pallor_os"))
    visual_fs_conv = visual_fs_converted(visual_fs)

    brainstem_fs = calc_brainstem_fs(g("b_eom"), g("b_nys"), g("b_trig"), g("b_face"), g("b_hear"),
                                     g("b_dysarth"), g("b_dysphag"), g("b_othercn"))

    strength = {}
    for m in MUSCLE_KEYS:
        rk, lk = f"p_str_{m}_R", f"p_str_{m}_L"
        if rk in inputs or lk in inputs:
            strength[m] = {"R": _safe(g(rk), 5), "L": _safe(g(lk), 5)}
    pyramidal_fs = calc_pyramidal_fs(
        strength=strength,
        overall_motor=g("p_overall"),
        plantar={"R": g("p_plantar_R"), "L": g("p_plantar_L")},
        reflexes={k: g(f"p_refl_{k}") for k in
                  ("biceps_R", "biceps_L", "triceps_R", "triceps_L", "brach_R", "brach_L",
                   "knee_R", "knee_L", "ankle_R", "ankle_L")},
        spasticity={"arms_R": g("p_spast_arms_R"), "arms_L": g("p_spast_arms_L"),
                    "legs_R": g("p_spast_legs_R"), "legs_L": g("p_spast_legs_L")},
        gait_spast={"R": _first_val(g("p_gait_spast_R"), g("p_gait_spast")),
                    "L": _first_val(g("p_gait_spast_L"), g("p_gait_spast"))},
        cutaneous=g("p_cutaneous"),
    )

    cerebellar_fs = calc_cerebellar_fs(
        head_tremor=g("c_head"), truncal_ataxia=g("c_trunc"),
        tremor_ue_R=g("c_tremor_ue_R"), tremor_ue_L=g("c_tremor_ue_L"),
        tremor_le_R=g("c_tremor_le_R"), tremor_le_L=g("c_tremor_le_L"),
        rapid_ue_R=g("c_rapid_ue_R"), rapid_ue_L=g("c_rapid_ue_L"),
        rapid_le_R=g("c_rapid_le_R"), rapid_le_L=g("c_rapid_le_L"),
        tandem=g("c_tandem"), gait_ataxia=g("c_gait_ataxia"), romberg=g("c_romberg"),
    )

    sens_keys = ["sup_ue_R", "sup_ue_L", "sup_trunk_R", "sup_trunk_L", "sup_le_R", "sup_le_L",
                 "vib_ue_R", "vib_ue_L", "vib_le_R", "vib_le_L",
                 "pos_ue_R", "pos_ue_L", "pos_le_R", "pos_le_L"]
    sens = {k: g("s_" + k) for k in sens_keys}
    sensory_fs = calc_sensory_fs(**sens)

    bb_fs = calc_bb_fs(g("bb_hes"), g("bb_urg"), g("bb_cath"), g("bb_bowel"))
    bb_fs_conv = bb_fs_converted(bb_fs)

    cerebral_fs_step = calc_cerebral_fs(g("m_ment"), g("m_fat"), exclude_fatigue=_truthy(g("m_fat_excl")))
    mood_only = cerebral_mood_only(cerebral_fs_step, g("m_depress"), g("m_euph"))
    cerebral_fs = 1 if mood_only else cerebral_fs_step

    manual_as = inputs.get("a_score")
    if manual_as is not None and manual_as != "":
        ambulation_score, ambulation_source = _safe(_num(manual_as), 0), "manual"
    else:
        dm, dr = inputs.get("amb_distance_measured"), inputs.get("amb_distance_reported")
        dist = dm if (dm is not None and dm != "") else dr
        auto = calc_ambulation_score(inputs.get("amb_assistance"), dist, _truthy(inputs.get("amb_is_normal")))
        if auto is not None:
            ambulation_score, ambulation_source = auto, "auto"
        else:
            ambulation_score, ambulation_source = 0, "incomplete"

    sensory_args = {k: sens[k] for k in ("pos_ue_R", "pos_ue_L", "pos_le_R", "pos_le_L")}
    x_suggested = should_suggest_cerebellar_x(strength, sensory_args)
    x_manual = _truthy(g("c_x_marker"))

    fs_bundle = FSScores(visual=visual_fs_conv, brainstem=brainstem_fs, pyramidal=pyramidal_fs,
                         cerebellar=cerebellar_fs, sensory=sensory_fs, bb=bb_fs_conv,
                         cerebral=cerebral_fs_step)
    edss = calc_edss_step(fs_bundle, ambulation_score)

    return {
        "visual_fs": visual_fs, "visual_fs_conv": visual_fs_conv,
        "brainstem_fs": brainstem_fs, "pyramidal_fs": pyramidal_fs, "cerebellar_fs": cerebellar_fs,
        "cerebellar_x": x_manual or x_suggested, "cerebellar_x_suggested": x_suggested,
        "cerebellar_x_manual": x_manual,
        "sensory_fs": sensory_fs,
        "bb_fs": bb_fs, "bb_fs_conv": bb_fs_conv,
        "cerebral_fs": cerebral_fs, "cerebral_fs_step": cerebral_fs_step, "cerebral_mood_only": mood_only,
        "ambulation_score": ambulation_score, "ambulation_source": ambulation_source,
        "edss_step": edss,
    }


if __name__ == "__main__":
    demo = {"p_str_biceps_R": 5, "p_str_biceps_L": 4, "c_gait_ataxia": 1,
            "s_vib_le_R": 1, "s_vib_le_L": 1, "m_fat": 1, "a_score": 0}
    for k, v in calculate_full_edss(demo).items():
        print(f"  {k:24s}: {v}")
