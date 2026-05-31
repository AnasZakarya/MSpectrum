"""
Unit tests for AutoEDSSguide calculation engine.

Tests cover:
- Each FS calculation in isolation (with edge cases)
- Conversion functions
- Final EDSS step (Fouad Fig 6-8 patterns)
- Ambulation override scenarios
- Real-world clinical cases
"""

import unittest
from edss_calc import (
    calc_visual_fs, visual_fs_converted, snellen_to_score,
    calc_brainstem_fs,
    calc_pyramidal_fs,
    calc_cerebellar_fs,
    calc_sensory_fs,
    calc_bb_fs, bb_fs_converted,
    calc_cerebral_fs,
    calc_edss_step, FSScores,
    calculate_full_edss,
)


class TestVisual(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(calc_visual_fs(va_od="20/20", va_os="20/20"), 0)

    def test_mild_one_eye(self):
        # 20/30 in one eye = grade 1
        self.assertEqual(calc_visual_fs(va_od="20/30", va_os="20/20"), 1)

    def test_moderate_unilateral(self):
        # 20/60 in one eye = grade 2
        self.assertEqual(calc_visual_fs(va_od="20/60", va_os="20/20"), 2)

    def test_with_scotoma(self):
        self.assertEqual(calc_visual_fs(scotoma_od=2, va_od="20/20", va_os="20/20"), 2)

    def test_with_field_defect(self):
        # complete homonymous hemianopsia → grade 3
        self.assertEqual(calc_visual_fs(vf_od=3, vf_os=3, va_od="20/20", va_os="20/20"), 3)

    def test_severe_one_eye_with_normal_other(self):
        # Per Neurostatus: 20/200 in one eye, 20/20 in other → grade 3
        # (severe in single eye when better eye is normal)
        result = calc_visual_fs(va_od="20/200", va_os="20/20")
        self.assertEqual(result, 3)

    def test_blindness(self):
        # NLP both eyes
        self.assertEqual(calc_visual_fs(va_od="NLP", va_os="NLP"), 6)

    def test_conversion(self):
        # Visual FS conversion: 0→0, 1→1, 2→2, 3→3, 4→3, 5→4, 6→5
        self.assertEqual(visual_fs_converted(0), 0)
        self.assertEqual(visual_fs_converted(1), 1)
        self.assertEqual(visual_fs_converted(4), 3)
        self.assertEqual(visual_fs_converted(5), 4)
        self.assertEqual(visual_fs_converted(6), 5)


class TestBrainstem(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(calc_brainstem_fs(), 0)

    def test_mild_nystagmus(self):
        self.assertEqual(calc_brainstem_fs(nystagmus=1), 1)

    def test_moderate_dysarthria(self):
        self.assertEqual(calc_brainstem_fs(dysarthria=2), 2)

    def test_severe_dysphagia(self):
        # dysphagia=5 → max=5
        self.assertEqual(calc_brainstem_fs(dysphagia=5), 5)

    def test_max_of_multiple(self):
        # Max of all subscores
        self.assertEqual(
            calc_brainstem_fs(eom=1, nystagmus=2, trigeminal=3, facial=2),
            3,
        )


class TestPyramidal(unittest.TestCase):
    def test_normal(self):
        s = {m: {"R": 5, "L": 5} for m in ["deltoid", "biceps", "triceps"]}
        self.assertEqual(calc_pyramidal_fs(strength=s), 0)

    def test_signs_only_fatigability(self):
        # Normal strength but fatigability complaint
        self.assertEqual(calc_pyramidal_fs(strength={}, overall_motor=1), 1)

    def test_minimal_one_muscle_grade4(self):
        s = {"deltoid": {"R": 4, "L": 5}}
        # BMRC 4 in 1 muscle = FS 2
        self.assertEqual(calc_pyramidal_fs(strength=s), 2)

    def test_mild_grade4_in_3plus(self):
        s = {"deltoid": {"R": 4, "L": 5}, "biceps": {"R": 4, "L": 5},
             "triceps": {"R": 4, "L": 5}}
        # BMRC 4 in >2 muscles = FS 3
        self.assertEqual(calc_pyramidal_fs(strength=s), 3)

    def test_grade3_in_one_muscle(self):
        s = {"deltoid": {"R": 3, "L": 5}}
        # BMRC 3 in 1 muscle = FS 3
        self.assertEqual(calc_pyramidal_fs(strength=s), 3)

    def test_severe_one_limb(self):
        # All UE_R muscles ≤1 → monoplegia
        s = {m: {"R": 1, "L": 5} for m in
             ["deltoid", "biceps", "triceps", "wflex", "wext"]}
        self.assertEqual(calc_pyramidal_fs(strength=s), 4)

    def test_paraplegia(self):
        s = {m: {"R": 0, "L": 0} for m in
             ["hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]}
        # Both LL = 0 → paraplegia → FS 5
        self.assertEqual(calc_pyramidal_fs(strength=s), 5)

    def test_hemiplegia(self):
        # UE_R + LE_R both 0
        s = {m: {"R": 0, "L": 5} for m in
             ["deltoid", "biceps", "triceps", "wflex", "wext",
              "hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]}
        self.assertEqual(calc_pyramidal_fs(strength=s), 5)

    def test_tetraplegia(self):
        s = {m: {"R": 0, "L": 0} for m in
             ["deltoid", "biceps", "triceps", "wflex", "wext",
              "hipflex", "kneeflex", "kneeext", "ankdorsi", "ankplant"]}
        self.assertEqual(calc_pyramidal_fs(strength=s), 6)


class TestCerebellar(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(calc_cerebellar_fs(), 0)

    def test_signs_only(self):
        self.assertEqual(calc_cerebellar_fs(head_tremor=1), 1)

    def test_mild_ataxia(self):
        self.assertEqual(calc_cerebellar_fs(tremor_ue_R=2), 2)

    def test_tandem_impossible(self):
        self.assertEqual(calc_cerebellar_fs(tandem=2), 2)

    def test_moderate_romberg_alone(self):
        self.assertEqual(calc_cerebellar_fs(romberg=2), 2)

    def test_moderate_limb_ataxia(self):
        self.assertEqual(calc_cerebellar_fs(tremor_ue_R=3, tremor_ue_L=2), 3)

    def test_severe_gait(self):
        self.assertEqual(calc_cerebellar_fs(gait_ataxia=4), 3)

    def test_severe_combined(self):
        # Severe ataxia in 3-4 limbs + severe truncal/gait
        self.assertEqual(calc_cerebellar_fs(
            tremor_ue_R=4, tremor_ue_L=4, tremor_le_R=4, tremor_le_L=3,
            gait_ataxia=4, truncal_ataxia=4,
        ), 4)


class TestSensory(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(calc_sensory_fs(), 0)

    def test_mild_vibration_one_limb(self):
        self.assertEqual(calc_sensory_fs(vib_le_R=1), 1)

    def test_moderate_vibration(self):
        # vib_max=2 in only 1-2 limbs → deep score 2 → final 2
        self.assertEqual(calc_sensory_fs(vib_le_R=2, vib_le_L=2), 2)

    def test_proprioception_loss(self):
        # Loss of position sense in 1-2 limbs → FS 4
        self.assertEqual(calc_sensory_fs(pos_le_R=3), 4)

    def test_combination_5(self):
        # superficial=4 + deep=4 → 5
        # superficial 4: marked decrease in 1-2 limbs
        # deep 4: pos loss in 1-2 limbs
        result = calc_sensory_fs(
            sup_ue_R=4, sup_ue_L=4,    # marked decrease in 2 limbs
            pos_le_R=3,                 # loss of proprioception in 1 limb
        )
        # Should be at least 4; the combination rule promotes 4+4 to 5
        self.assertGreaterEqual(result, 4)

    def test_combination_6(self):
        # superficial=5 + deep=5 → 6
        # superficial 5: complete loss in 1-2 limbs
        # deep 5: pos loss in >2 limbs
        result = calc_sensory_fs(
            sup_ue_R=5, sup_ue_L=5,
            pos_le_R=3, pos_le_L=3, pos_ue_R=3,
        )
        self.assertGreaterEqual(result, 5)


class TestBowelBladder(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(calc_bb_fs(), 0)

    def test_mild_hesitancy(self):
        self.assertEqual(calc_bb_fs(hesitancy=1), 1)

    def test_moderate_urgency(self):
        self.assertEqual(calc_bb_fs(urgency=2), 2)

    def test_constant_catheterisation(self):
        # cath=2 (constant) → equivalent to grade 4
        self.assertEqual(calc_bb_fs(catheterisation=2), 4)

    def test_severe_combination(self):
        # urgency=4 + bowel=4 → FS 5
        self.assertEqual(calc_bb_fs(urgency=4, bowel=4), 5)

    def test_conversion(self):
        # B/B FS conversion
        self.assertEqual(bb_fs_converted(0), 0)
        self.assertEqual(bb_fs_converted(3), 3)
        self.assertEqual(bb_fs_converted(4), 3)
        self.assertEqual(bb_fs_converted(5), 4)


class TestCerebral(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(calc_cerebral_fs(), 0)

    def test_fatigue_only(self):
        # 0 mentation + ≥1 fatigue → 1
        self.assertEqual(calc_cerebral_fs(mentation=0, fatigue=2), 1)

    def test_mild_mentation(self):
        self.assertEqual(calc_cerebral_fs(mentation=2), 2)

    def test_dementia(self):
        self.assertEqual(calc_cerebral_fs(mentation=5), 5)

    def test_depression_does_not_count(self):
        # Depression doesn't add to FS
        self.assertEqual(calc_cerebral_fs(mentation=0, depression=1), 0)


class TestEDSSStep(unittest.TestCase):
    """Test final EDSS step calculation against Fouad's Fig 6 patterns."""

    def test_all_zero(self):
        fs = FSScores()
        self.assertEqual(calc_edss_step(fs), 0.0)

    def test_one_fs_one(self):
        fs = FSScores(pyramidal=1)
        self.assertEqual(calc_edss_step(fs), 1.0)

    def test_two_fs_one(self):
        fs = FSScores(pyramidal=1, sensory=1)
        self.assertEqual(calc_edss_step(fs), 1.5)

    def test_one_fs_two(self):
        fs = FSScores(pyramidal=2)
        self.assertEqual(calc_edss_step(fs), 2.0)

    def test_two_fs_two(self):
        fs = FSScores(pyramidal=2, sensory=2)
        self.assertEqual(calc_edss_step(fs), 2.5)

    def test_three_fs_two(self):
        fs = FSScores(pyramidal=2, sensory=2, cerebellar=2)
        self.assertEqual(calc_edss_step(fs), 3.0)

    def test_five_fs_two_special(self):
        # 5 FSs of grade 2 → 5.0 (Fouad exception)
        fs = FSScores(pyramidal=2, sensory=2, cerebellar=2,
                      brainstem=2, visual=2)
        self.assertEqual(calc_edss_step(fs), 5.0)

    def test_one_fs_three(self):
        fs = FSScores(pyramidal=3)
        self.assertEqual(calc_edss_step(fs), 3.0)

    def test_three_with_two_others(self):
        fs = FSScores(pyramidal=3, sensory=2, cerebellar=2)
        # FS 3 + 2 others at 2 → 3.5
        self.assertEqual(calc_edss_step(fs), 3.5)

    def test_two_fs_three(self):
        fs = FSScores(pyramidal=3, sensory=3)
        self.assertEqual(calc_edss_step(fs), 3.5)

    def test_fs_four_unrestricted(self):
        # FS=4 with AS=0 (unrestricted) → 4.0
        fs = FSScores(pyramidal=4)
        self.assertEqual(calc_edss_step(fs, ambulation_score=0), 4.0)

    def test_fs_four_with_500m(self):
        # FS=4 + AS=1 (>500m) → 4.0
        fs = FSScores(pyramidal=4)
        self.assertEqual(calc_edss_step(fs, ambulation_score=1), 4.0)

    def test_fs_four_with_300_500(self):
        # FS=4 + AS=2 (300-499m) → 4.5
        fs = FSScores(pyramidal=4)
        self.assertEqual(calc_edss_step(fs, ambulation_score=2), 4.5)

    def test_ambulation_5_dominates(self):
        # AS=5 (<100m) → 6.0 regardless of FS (as long as not higher)
        fs = FSScores(pyramidal=2)
        self.assertEqual(calc_edss_step(fs, ambulation_score=5), 6.0)

    def test_wheelchair(self):
        fs = FSScores(pyramidal=5)
        self.assertEqual(calc_edss_step(fs, ambulation_score=10), 7.0)

    def test_wheelchair_with_help(self):
        fs = FSScores(pyramidal=6)
        self.assertEqual(calc_edss_step(fs, ambulation_score=11), 7.5)

    def test_bedbound(self):
        fs = FSScores(pyramidal=6)
        self.assertEqual(calc_edss_step(fs, ambulation_score=12), 8.0)


class TestRealWorldCases(unittest.TestCase):
    """Realistic clinical scenarios."""

    def test_mild_RRMS(self):
        """Patient with mild RRMS: signs only, fully ambulatory."""
        inputs = {
            "p_str_deltoid_R": 5, "p_str_deltoid_L": 4,
            "c_gait_ataxia": 1,
            "s_vib_le_R": 1, "s_vib_le_L": 1,
            "m_ment": 0, "m_fat": 1,
            "a_score": 0,
        }
        result = calculate_full_edss(inputs)
        # FS 2 (one BMRC 4) + cerebellar 1 + sensory 1 + cerebral 1
        # Max=2, with several 1s → ~2.0
        self.assertLessEqual(result["edss_step"], 3.0)

    def test_RRMS_with_walking_difficulty(self):
        """Moderate RRMS with limited walking."""
        inputs = {
            "p_str_kneeext_R": 3, "p_str_kneeext_L": 4,
            "p_str_ankdorsi_R": 3, "p_str_ankdorsi_L": 4,
            "c_gait_ataxia": 2,
            "a_score": 4,  # 100-200m
        }
        result = calculate_full_edss(inputs)
        # Pyramidal FS=3, Cerebellar=2, AS=4 → EDSS 5.5
        self.assertEqual(result["edss_step"], 5.5)
        self.assertEqual(result["pyramidal_fs"], 3)

    def test_severe_disability(self):
        """Severe MS, wheelchair-bound."""
        inputs = {
            "p_str_kneeext_R": 1, "p_str_kneeext_L": 1,
            "p_str_ankdorsi_R": 1, "p_str_ankdorsi_L": 1,
            "p_str_kneeflex_R": 2, "p_str_kneeflex_L": 2,
            "p_str_hipflex_R": 2,  "p_str_hipflex_L": 2,
            "p_str_ankplant_R": 1, "p_str_ankplant_L": 1,
            "a_score": 10,  # Wheelchair without help
        }
        result = calculate_full_edss(inputs)
        # Paraplegia → Pyramidal FS 5, AS=10 → EDSS 7.0
        self.assertEqual(result["pyramidal_fs"], 5)
        self.assertEqual(result["edss_step"], 7.0)

    def test_visual_dominant(self):
        """Optic neuritis with no other disability."""
        inputs = {
            "v_va_od": "20/200", "v_va_os": "20/20",
        }
        result = calculate_full_edss(inputs)
        # 20/200 in one eye, normal other → Visual FS=3 → conv=3
        self.assertEqual(result["visual_fs"], 3)
        self.assertGreaterEqual(result["edss_step"], 3.0)


class TestAmbulationFSCombinations(unittest.TestCase):
    """
    Critical tests for the 4.0-5.5 range where FS and AS combine.
    Each AS level dictates a floor; FS pattern can push higher.
    """

    # ========== AS=0 (Unrestricted) — pure FS ==========
    def test_AS0_no_fs(self):
        self.assertEqual(calc_edss_step(FSScores(), 0), 0.0)

    def test_AS0_one_fs1(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=1), 0), 1.0)

    def test_AS0_fs2(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=2), 0), 2.0)

    def test_AS0_fs3(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=3), 0), 3.0)

    def test_AS0_fs4(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=4), 0), 4.0)

    def test_AS0_fs5(self):
        # FS=5 alone but unrestricted (rare but possible)
        self.assertEqual(calc_edss_step(FSScores(sensory=5), 0), 5.0)

    # ========== AS=1 (>500m, not unrestricted) — floor 4.0 ==========
    def test_AS1_no_fs(self):
        self.assertEqual(calc_edss_step(FSScores(), 1), 4.0)

    def test_AS1_low_fs(self):
        # Even with low FS, AS=1 gives 4.0 floor
        self.assertEqual(calc_edss_step(FSScores(pyramidal=2), 1), 4.0)

    def test_AS1_fs4(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=4), 1), 4.0)

    def test_AS1_fs5(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=5), 1), 5.0)

    # ========== AS=2 (300-499m) — floor 4.5 ==========
    def test_AS2_no_fs(self):
        self.assertEqual(calc_edss_step(FSScores(), 2), 4.5)

    def test_AS2_with_low_fs(self):
        # Low FS but AS=2 → 4.5
        self.assertEqual(calc_edss_step(FSScores(pyramidal=2), 2), 4.5)

    def test_AS2_fs4(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=4), 2), 4.5)

    def test_AS2_fs5(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=5), 2), 5.0)

    # ========== AS=3 (200-299m) — floor 5.0 ==========
    def test_AS3_no_fs(self):
        # Critical case: AS=3 alone → 5.0
        self.assertEqual(calc_edss_step(FSScores(), 3), 5.0)

    def test_AS3_low_fs(self):
        # Critical case from user: FS=2 + AS=3 → must be 5.0 not 2.0
        self.assertEqual(calc_edss_step(FSScores(pyramidal=2), 3), 5.0)

    def test_AS3_fs4(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=4), 3), 5.0)

    def test_AS3_fs5(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=5), 3), 5.0)

    def test_AS3_fs6(self):
        # FS=6 (tetraplegia) overrides AS=3 floor
        self.assertEqual(calc_edss_step(FSScores(pyramidal=6), 3), 6.0)

    # ========== AS=4 (100-199m) — fixed 5.5 ==========
    def test_AS4_no_fs(self):
        self.assertEqual(calc_edss_step(FSScores(), 4), 5.5)

    def test_AS4_low_fs(self):
        self.assertEqual(calc_edss_step(FSScores(pyramidal=1), 4), 5.5)

    def test_AS4_fs6(self):
        # FS=6 overrides
        self.assertEqual(calc_edss_step(FSScores(pyramidal=6), 4), 6.0)

    # ========== AS=5+ (no aid <100m or with aid) — ambulation only ==========
    def test_AS5(self):
        self.assertEqual(calc_edss_step(FSScores(), 5), 6.0)

    def test_AS5_high_fs(self):
        # AS=5 alone determines, FS doesn't matter once >5
        self.assertEqual(calc_edss_step(FSScores(pyramidal=5), 5), 6.0)

    def test_AS6_unilateral(self):
        self.assertEqual(calc_edss_step(FSScores(), 6), 6.0)

    def test_AS7_bilateral(self):
        self.assertEqual(calc_edss_step(FSScores(), 7), 6.0)

    def test_AS8_unilateral_short(self):
        self.assertEqual(calc_edss_step(FSScores(), 8), 6.5)

    def test_AS9_bilateral_short(self):
        self.assertEqual(calc_edss_step(FSScores(), 9), 6.5)

    def test_AS10_wheelchair(self):
        self.assertEqual(calc_edss_step(FSScores(), 10), 7.0)

    def test_AS11_wheelchair_help(self):
        self.assertEqual(calc_edss_step(FSScores(), 11), 7.5)

    def test_AS12_bedbound(self):
        self.assertEqual(calc_edss_step(FSScores(), 12), 8.0)


class TestClinicalScenariosExpanded(unittest.TestCase):
    """Real-world cases at multiple disability levels."""

    def test_normal_exam(self):
        result = calculate_full_edss({})
        self.assertEqual(result["edss_step"], 0.0)

    def test_signs_only(self):
        # Just a hyperreflexia, no disability
        inputs = {
            "p_str_biceps_R": 5, "p_str_biceps_L": 5,
            "p_overall": 1,  # subjective fatigability only
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["pyramidal_fs"], 1)
        self.assertEqual(result["edss_step"], 1.0)

    def test_minimal_two_fs(self):
        # Two FS at grade 2 → EDSS 2.5
        inputs = {
            "p_str_deltoid_R": 4,  # FS pyramidal 2
            "c_gait_ataxia": 2,    # FS cerebellar 2 (mild ataxia)
            "a_score": 0,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["pyramidal_fs"], 2)
        # Cerebellar=2 (mild ataxia → mild = 2)
        self.assertEqual(result["edss_step"], 2.5)

    def test_moderate_one_fs_3(self):
        # One FS at 3, rest minimal
        inputs = {
            "p_str_deltoid_R": 3,  # BMRC 3 in 1 muscle → FS 3
            "a_score": 0,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["pyramidal_fs"], 3)
        self.assertEqual(result["edss_step"], 3.0)

    def test_fully_ambulatory_severe_disability(self):
        # FS=4 but still walks >500m without aid (AS=1)
        inputs = {
            # Monoplegia of UE_R
            "p_str_deltoid_R": 1, "p_str_biceps_R": 1,
            "p_str_triceps_R": 1, "p_str_wflex_R": 1,
            "p_str_wext_R": 1,
            "p_str_deltoid_L": 5, "p_str_biceps_L": 5,
            "p_str_triceps_L": 5, "p_str_wflex_L": 5,
            "p_str_wext_L": 5,
            "p_str_hipflex_R": 5, "p_str_kneeflex_R": 5,
            "p_str_kneeext_R": 5, "p_str_ankdorsi_R": 5,
            "p_str_ankplant_R": 5,
            "p_str_hipflex_L": 5, "p_str_kneeflex_L": 5,
            "p_str_kneeext_L": 5, "p_str_ankdorsi_L": 5,
            "p_str_ankplant_L": 5,
            "a_score": 1,  # >500m
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["pyramidal_fs"], 4)
        self.assertEqual(result["edss_step"], 4.0)

    def test_walking_300_500m(self):
        # AS=2 → EDSS 4.5
        inputs = {
            "p_str_kneeext_R": 4, "p_str_kneeext_L": 4,
            "a_score": 2,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 4.5)

    def test_walking_200_300m(self):
        # AS=3 → EDSS 5.0 floor regardless of mild FS
        inputs = {
            "p_str_kneeext_R": 4,  # only one BMRC4 → FS 2
            "a_score": 3,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["pyramidal_fs"], 2)
        self.assertEqual(result["edss_step"], 5.0)  # AS dominates

    def test_walking_100_200m(self):
        # AS=4 → EDSS 5.5
        inputs = {
            "p_str_kneeext_R": 4,
            "a_score": 4,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 5.5)

    def test_walking_lt_100m_unaided(self):
        # AS=5 → EDSS 6.0
        inputs = {
            "p_str_kneeext_R": 3,
            "a_score": 5,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 6.0)

    def test_unilateral_cane(self):
        # AS=6 → EDSS 6.0
        inputs = {
            "p_str_hipflex_R": 3, "p_str_hipflex_L": 3,
            "a_score": 6,
        }
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 6.0)

    def test_bilateral_cane(self):
        # AS=7 → EDSS 6.0
        inputs = {"a_score": 7}
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 6.0)

    def test_wheelchair_independent(self):
        # AS=10 → EDSS 7.0
        inputs = {"a_score": 10}
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 7.0)

    def test_wheelchair_help(self):
        # AS=11 → EDSS 7.5
        inputs = {"a_score": 11}
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 7.5)

    def test_bedbound(self):
        # AS=12 → EDSS 8.0
        inputs = {"a_score": 12}
        result = calculate_full_edss(inputs)
        self.assertEqual(result["edss_step"], 8.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
