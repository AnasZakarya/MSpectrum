// EDSS engine battery — asserts the audited Neurostatus behaviour of index.html.
// Expected values are taken directly from the letter-by-letter audited rules.
const { loadEngine } = require('./load_engine');
const E = loadEngine();

const cases = [];
function eq(name, got, want) { cases.push({ name, got, want, ok: got === want }); }
function full(inputs) { return E.calculateFullEDSS(inputs); }

// ---------- Snellen -> score ----------
eq('snellen 20/20', E.snellenToScore('20/20'), 0);
eq('snellen 20/25', E.snellenToScore('20/25'), 1);
eq('snellen 20/30', E.snellenToScore('20/30'), 2);
eq('snellen 20/50', E.snellenToScore('20/50'), 2);
eq('snellen 20/60', E.snellenToScore('20/60'), 3);
eq('snellen 20/100', E.snellenToScore('20/100'), 4);
eq('snellen 20/200', E.snellenToScore('20/200'), 4);
eq('snellen NLP', E.snellenToScore('NLP'), 5);
eq('snellen blank', E.snellenToScore(''), 0);

// ---------- Visual FS + conversion ----------
eq('visual normal', E.calcVisualFS({ va_od: '20/20', va_os: '20/20' }), 0);
eq('visual mild one eye 20/25', E.calcVisualFS({ va_od: '20/25', va_os: '20/20' }), 1);
eq('visual 20/60 one eye', E.calcVisualFS({ va_od: '20/60', va_os: '20/20' }), 3);
eq('visual 20/100 one eye (no bump, better eye good)', E.calcVisualFS({ va_od: '20/100', va_os: '20/20' }), 4);
eq('visual 20/100 both eyes (bump)', E.calcVisualFS({ va_od: '20/100', va_os: '20/100' }), 5);
eq('visual scotoma small=1', E.calcVisualFS({ scotoma_od: 1, va_od: '20/20', va_os: '20/20' }), 1);
eq('visual scotoma large=2 -> 3', E.calcVisualFS({ scotoma_od: 2, va_od: '20/20', va_os: '20/20' }), 3);
eq('visual pallor only -> 1', E.calcVisualFS({ pallor_od: 1, va_od: '20/20', va_os: '20/20' }), 1);
eq('visualConv table [0,1,2,2,3,3,4] @4', E.visualFSConverted(4), 3);
eq('visualConv table @6', E.visualFSConverted(6), 4);
eq('visualConv table @3', E.visualFSConverted(3), 2);

// ---------- Brainstem ----------
eq('brainstem max rule', E.calcBrainstemFS({ eom: 1, dysarthria: 3, hearing: 2 }), 3);

// ---------- Pyramidal ----------
eq('pyramidal fatigability -> FS2', full({ p_overall: 1 }).pyramidal_fs, 2);
eq('pyramidal babinski -> FS1', full({ p_plantar_R: 2 }).pyramidal_fs, 1);
eq('pyramidal brisk reflex(3) -> FS1', full({ p_refl_knee_R: 3 }).pyramidal_fs, 1);
eq('pyramidal equivocal plantar(1) not counted', full({ p_plantar_R: 1 }).pyramidal_fs, 0);
eq('pyramidal monoplegia (all UE_R <=1) -> FS4', full({
  p_str_deltoid_R: 1, p_str_biceps_R: 1, p_str_triceps_R: 1, p_str_wflex_R: 0, p_str_wext_R: 1,
}).pyramidal_fs, 4);
// Severe monoparesis: one limb with BMRC <=2 in >=2 groups exceeds the FS3 "one group" limit -> FS4.
eq('pyramidal severe monoparesis (>=2 groups <=2 in one limb) -> FS4', full({
  p_str_hipflex_R: 3, p_str_kneeflex_R: 2, p_str_kneeext_R: 2, p_str_ankdorsi_R: 1, p_str_ankplant_R: 1,
}).pyramidal_fs, 4);
eq('pyramidal single group <=2 (one muscle) stays FS3', full({ p_str_ankdorsi_R: 2 }).pyramidal_fs, 3);
eq('pyramidal single weak muscle BMRC3 -> FS3', full({ p_str_deltoid_R: 3 }).pyramidal_fs, 3);
eq('pyramidal BMRC4 one group -> FS2', full({ p_str_deltoid_R: 4 }).pyramidal_fs, 2);

// ---------- Cerebellar ----------
eq('cerebellar moderate limb(3) -> FS3', full({ c_tremor_ue_R: 3 }).cerebellar_fs, 3);
eq('cerebellar mild(1) -> FS1', full({ c_gait_ataxia: 1 }).cerebellar_fs, 1);

// ---------- Sensory ----------
eq('sensory vibration moderate(2) alone -> FS2', full({ s_vib_le_R: 2 }).sensory_fs, 2);
eq('sensory position(1) one limb -> FS2', full({ s_pos_le_R: 1 }).sensory_fs, 2);
eq('sensory superficial moderate 1 limb -> FS2', full({ s_sup_ue_R: 2 }).sensory_fs, 2);

// ---------- Bowel/Bladder ----------
eq('bb cath constant c=2 -> FS4', E.calcBBFS({ catheterisation: 2 }), 4);
eq('bb cath c=1 -> FS3', E.calcBBFS({ catheterisation: 1 }), 3);
eq('bb bladder loss urgency4 -> FS5', E.calcBBFS({ urgency: 4 }), 5);
eq('bb both loss -> FS6', E.calcBBFS({ urgency: 4, bowel: 4 }), 6);
eq('bb moderate urgency2 -> FS2', E.calcBBFS({ urgency: 2 }), 2);
eq('bbConv raw6 -> 5', E.bbFSConverted(6), 5);
eq('bbConv raw4 -> 3', E.bbFSConverted(4), 3);

// ---------- Cerebral ----------
eq('cerebral mild fatigue f=1 -> FS1', E.calcCerebralFS({ fatigue: 1 }), 1);
eq('cerebral moderate fatigue f=2 -> FS2', E.calcCerebralFS({ fatigue: 2 }), 2);
eq('cerebral exclude fatigue drops it', E.calcCerebralFS({ fatigue: 2, exclude_fatigue: true }), 0);
eq('cerebral mentation dominates', E.calcCerebralFS({ mentation: 3, fatigue: 1 }), 3);

// ---------- Ambulation ----------
eq('amb normal/unrestricted -> AS0', E.calcAmbulationScore({ assistance: 'none', is_normal: true }), 0);
eq('amb none 500m -> AS1', E.calcAmbulationScore({ assistance: 'none', distance_m: 500 }), 1);
eq('amb none 300m -> AS2', E.calcAmbulationScore({ assistance: 'none', distance_m: 300 }), 2);
eq('amb none 200m -> AS3', E.calcAmbulationScore({ assistance: 'none', distance_m: 200 }), 3);
eq('amb none 100m -> AS4', E.calcAmbulationScore({ assistance: 'none', distance_m: 100 }), 4);
eq('amb none 50m -> AS5', E.calcAmbulationScore({ assistance: 'none', distance_m: 50 }), 5);
eq('amb unilateral >50 -> AS6', E.calcAmbulationScore({ assistance: 'unilateral', distance_m: 100 }), 6);
eq('amb unilateral <=50 -> AS8', E.calcAmbulationScore({ assistance: 'unilateral', distance_m: 40 }), 8);
eq('amb bilateral >120 -> AS7', E.calcAmbulationScore({ assistance: 'bilateral', distance_m: 150 }), 7);
eq('amb bilateral <=120 -> AS9', E.calcAmbulationScore({ assistance: 'bilateral', distance_m: 80 }), 9);
eq('amb wheelchair indep -> AS10', E.calcAmbulationScore({ assistance: 'wheelchair_indep' }), 10);
eq('amb bedbound -> AS12', E.calcAmbulationScore({ assistance: 'bedbound' }), 12);

// ---------- EDSS step (FS combination) ----------
eq('edss all-normal -> 0', full({}).edss_step, 0);
eq('edss one FS2 -> 2.0', full({ p_str_deltoid_R: 4 }).edss_step, 2.0); // FS2 pyramidal, AS0
eq('edss five FS2 -> 3.5', full({
  p_str_deltoid_R: 4, s_vib_le_R: 2, c_gait_ataxia: 2, bb_urg: 2, m_fat: 2,
}).edss_step, 3.5);
eq('edss AS floor: unilateral aid dominates -> 6.0', full({ amb_assistance: 'unilateral', amb_distance_reported: 100 }).edss_step, 6.0);
eq('edss AS=4 (100m) floor -> 5.5', full({ amb_assistance: 'none', amb_distance_reported: 100 }).edss_step, 5.5);
eq('edss AS=1 (>=500m) floor 2.0', full({ amb_assistance: 'none', amb_distance_reported: 500 }).edss_step, 2.0);
eq('edss wheelchair indep -> 7.0', full({ amb_assistance: 'wheelchair_indep' }).edss_step, 7.0);

// ---------- integration: high FS + severe ambulation ----------
const r1 = full({ p_str_hipflex_R: 1, p_str_kneeflex_R: 1, p_str_kneeext_R: 1, p_str_ankdorsi_R: 1, p_str_ankplant_R: 1, amb_assistance: 'bilateral', amb_distance_reported: 80 });
eq('integration paretic leg + bilateral aid -> 6.5', r1.edss_step, 6.5);

module.exports = { cases };

if (require.main === module) {
  const fails = cases.filter(c => !c.ok);
  for (const f of fails) console.log(`  FAIL  ${f.name}: got ${f.got}, want ${f.want}`);
  console.log(`\nEngine battery: ${cases.length - fails.length}/${cases.length} passed`);
  process.exit(fails.length ? 1 : 0);
}
