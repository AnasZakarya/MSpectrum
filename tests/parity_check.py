"""JS-Python engine parity check.

Generates random EDSS inputs (fixed seed), scores them with the JavaScript engine in
index.html (via node + tests/load_engine.js) and with edss_calc.py, and fails on any
difference. Run from the repo root:  python3 tests/parity_check.py [n_cases]
"""
import json, os, random, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from edss_calc import calculate_full_edss, MUSCLE_KEYS  # noqa: E402

SNELLEN = ["", "20/20", "20/25", "20/30", "20/40", "20/50", "20/60", "20/70", "20/80", "20/100", "20/200", "20/400", "CF", "HM", "LP", "NLP"]
ASSIST = ["", "none", "unilateral", "bilateral", "wheelchair_indep", "wheelchair_help", "bedbound", "bed_much", "bed_helpless", "bed_nocomm"]
SIDES = ("R", "L")


def rnd_case(rng):
    c = {}
    def maybe(k, hi, p=0.5, lo=0):
        if rng.random() < p:
            c[k] = rng.randint(lo, hi) if rng.random() > 0.05 else ""
    # Visual
    for k in ("v_va_od", "v_va_os"):
        if rng.random() < 0.6: c[k] = rng.choice(SNELLEN)
    for k in ("v_vf_od", "v_vf_os"): maybe(k, 3, 0.3)
    for k in ("v_scotoma_R", "v_scotoma_L"): maybe(k, 2, 0.3)
    for k in ("v_pallor_od", "v_pallor_os"): maybe(k, 1, 0.2)
    # Brainstem
    for k, hi in (("b_eom", 4), ("b_nys", 3), ("b_trig", 4), ("b_face", 4), ("b_hear", 4), ("b_dysarth", 5), ("b_dysphag", 5), ("b_othercn", 4)):
        maybe(k, hi, 0.3)
    # Pyramidal
    weak = rng.random()
    for m in MUSCLE_KEYS:
        for s in SIDES:
            if rng.random() < 0.6:
                c[f"p_str_{m}_{s}"] = rng.choice([5, 5, 5, 4, 3, 2, 1, 0]) if weak < 0.7 else rng.randint(0, 2)
    maybe("p_overall", 2, 0.3)
    for s in SIDES: maybe(f"p_plantar_{s}", 2, 0.3)
    for r in ("biceps", "triceps", "brach", "knee", "ankle"):
        for s in SIDES: maybe(f"p_refl_{r}_{s}", 5, 0.2)
    for k in ("p_spast_arms_R", "p_spast_arms_L", "p_spast_legs_R", "p_spast_legs_L"): maybe(k, 4, 0.2)
    if rng.random() < 0.5: maybe("p_gait_spast", 3, 1.0)
    else:
        for s in SIDES: maybe(f"p_gait_spast_{s}", 3, 0.3)
    maybe("p_cutaneous", 2, 0.2)
    # Cerebellar
    maybe("c_head", 3, 0.2); maybe("c_trunc", 4, 0.3)
    for x in ("tremor", "rapid"):
        for l in ("ue", "le"):
            for s in SIDES: maybe(f"c_{x}_{l}_{s}", 4, 0.3)
    maybe("c_tandem", 2, 0.3); maybe("c_gait_ataxia", 4, 0.3); maybe("c_romberg", 3, 0.3)
    if rng.random() < 0.1: c["c_x_marker"] = True
    # Sensory
    for x, hi in (("sup", 5), ("vib", 3), ("pos", 3)):
        for l in (("ue", "trunk", "le") if x == "sup" else ("ue", "le")):
            for s in SIDES: maybe(f"s_{x}_{l}_{s}", hi, 0.3)
    # Bowel/bladder, cerebral
    maybe("bb_hes", 4, 0.3); maybe("bb_urg", 4, 0.3); maybe("bb_cath", 2, 0.2); maybe("bb_bowel", 4, 0.3)
    maybe("m_ment", 5, 0.3); maybe("m_fat", 3, 0.4); maybe("m_depress", 1, 0.2); maybe("m_euph", 1, 0.1)
    if rng.random() < 0.15: c["m_fat_excl"] = True
    # Ambulation
    if rng.random() < 0.3:
        c["a_score"] = rng.randint(0, 15)
    else:
        if rng.random() < 0.8: c["amb_assistance"] = rng.choice(ASSIST)
        if rng.random() < 0.7: c["amb_distance_reported"] = rng.choice([5, 10, 20, 49, 50, 51, 100, 119, 120, 121, 150, 199, 200, 250, 299, 300, 450, 499, 500, 800])
        if rng.random() < 0.3: c["amb_distance_measured"] = rng.choice([50, 120, 200, 300, 500])
        if rng.random() < 0.3: c["amb_is_normal"] = True
        if rng.random() < 0.3: c["score_profile"] = rng.choice(["standard", "forum50", ""])
    return c


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    rng = random.Random(20261106)
    cases = [rnd_case(rng) for _ in range(n)]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(cases, f); path = f.name
    js = json.loads(subprocess.check_output(["node", os.path.join(HERE, "parity_js.js"), path]))
    os.unlink(path)
    bad = 0
    for i, (c, j) in enumerate(zip(cases, js)):
        p = calculate_full_edss(c)
        diffs = {k: (j[k], p[k]) for k in j if j[k] != p[k]}
        if diffs:
            bad += 1
            if bad <= 5:
                print("MISMATCH case", i, diffs, "\n  input:", json.dumps(c))
    print(f"JS-Python parity: {n - bad}/{n} cases identical")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
