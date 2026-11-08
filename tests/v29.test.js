// v29 regressions: gait spasticity from the guided form (single p_gait_spast value) reaches the Pyramidal FS.
const { loadEngine } = require('./load_engine');
const E = loadEngine();
const results = [];
const fs = (inp) => E.calculateFullEDSS(inp).pyramidal_fs;
results.push({ name: 'p_gait_spast=3 (guided form) -> Pyramidal FS 3', ok: fs({ p_gait_spast: 3 }) === 3 });
results.push({ name: 'p_gait_spast=2 -> Pyramidal FS 2', ok: fs({ p_gait_spast: 2 }) === 2 });
results.push({ name: 'p_gait_spast_R/L (scanner) still used', ok: fs({ p_gait_spast_R: 3, p_gait_spast_L: 0 }) === 3 });
results.push({ name: 'empty p_gait_spast -> Pyramidal FS 0', ok: fs({ p_gait_spast: '' }) === 0 });
// 50 m rule with one aid follows the Neurostatus manual ("more than 50 m")
const asOf = (inp) => E.calculateFullEDSS(inp).ambulation_score;
results.push({ name: 'unilateral 50 m -> AS 8 (6.5)', ok: asOf({ amb_assistance: 'unilateral', amb_distance_reported: 50 }) === 8 });
results.push({ name: 'unilateral 51 m -> AS 6 (6.0)', ok: asOf({ amb_assistance: 'unilateral', amb_distance_reported: 51 }) === 6 });
// v33: Visual FS better-eye bump depends on the better eye's ACUITY only (Kurtzke 1983)
const vis = (inp) => E.calculateFullEDSS(inp).visual_fs;
results.push({ name: 'OD 20/80, OS 20/20 + large scotoma -> Visual FS 3 (no bump)', ok: vis({ v_va_od: '20/80', v_va_os: '20/20', v_scotoma_L: 2 }) === 3 });
results.push({ name: 'OD 20/80, OS 20/70 -> Visual FS 4 (bump)', ok: vis({ v_va_od: '20/80', v_va_os: '20/70' }) === 4 });
results.push({ name: 'OD 20/200, OS 20/40 -> Visual FS 4 (no bump)', ok: vis({ v_va_od: '20/200', v_va_os: '20/40' }) === 4 });
results.push({ name: 'OD marked field loss, OS 20/60 -> Visual FS 5', ok: vis({ v_vf_od: 3, v_va_os: '20/60' }) === 5 });
for (const r of results) console.log((r.ok ? 'ok  ' : 'FAIL') + ' ' + r.name);
const pass = results.filter(r => r.ok).length;
console.log(`\nv29/v31 fixes: ${pass}/${results.length} passed`);
process.exit(pass === results.length ? 0 : 1);
