// v29 regressions: gait spasticity from the guided form (single p_gait_spast value) reaches the Pyramidal FS.
const { loadEngine } = require('./load_engine');
const E = loadEngine();
const results = [];
const fs = (inp) => E.calculateFullEDSS(inp).pyramidal_fs;
results.push({ name: 'p_gait_spast=3 (guided form) -> Pyramidal FS 3', ok: fs({ p_gait_spast: 3 }) === 3 });
results.push({ name: 'p_gait_spast=2 -> Pyramidal FS 2', ok: fs({ p_gait_spast: 2 }) === 2 });
results.push({ name: 'p_gait_spast_R/L (scanner) still used', ok: fs({ p_gait_spast_R: 3, p_gait_spast_L: 0 }) === 3 });
results.push({ name: 'empty p_gait_spast -> Pyramidal FS 0', ok: fs({ p_gait_spast: '' }) === 0 });
// v31: scoring profile for the 50 m rule (unilateral aid, exactly 50 m)
const asOf = (inp) => E.calculateFullEDSS(inp).ambulation_score;
results.push({ name: 'unilateral 50 m, standard profile -> AS 8 (6.5)', ok: asOf({ amb_assistance: 'unilateral', amb_distance_reported: 50 }) === 8 });
results.push({ name: 'unilateral 50 m, forum50 profile -> AS 6 (6.0)', ok: asOf({ amb_assistance: 'unilateral', amb_distance_reported: 50, score_profile: 'forum50' }) === 6 });
results.push({ name: 'unilateral 51 m, standard -> AS 6', ok: asOf({ amb_assistance: 'unilateral', amb_distance_reported: 51 }) === 6 });
for (const r of results) console.log((r.ok ? 'ok  ' : 'FAIL') + ' ' + r.name);
const pass = results.filter(r => r.ok).length;
console.log(`\nv29/v31 fixes: ${pass}/${results.length} passed`);
process.exit(pass === results.length ? 0 : 1);
