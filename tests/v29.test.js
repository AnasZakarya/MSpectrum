// v29 regressions: gait spasticity from the guided form (single p_gait_spast value) reaches the Pyramidal FS.
const { loadEngine } = require('./load_engine');
const E = loadEngine();
const results = [];
const fs = (inp) => E.calculateFullEDSS(inp).pyramidal_fs;
results.push({ name: 'p_gait_spast=3 (guided form) -> Pyramidal FS 3', ok: fs({ p_gait_spast: 3 }) === 3 });
results.push({ name: 'p_gait_spast=2 -> Pyramidal FS 2', ok: fs({ p_gait_spast: 2 }) === 2 });
results.push({ name: 'p_gait_spast_R/L (scanner) still used', ok: fs({ p_gait_spast_R: 3, p_gait_spast_L: 0 }) === 3 });
results.push({ name: 'empty p_gait_spast -> Pyramidal FS 0', ok: fs({ p_gait_spast: '' }) === 0 });
for (const r of results) console.log((r.ok ? 'ok  ' : 'FAIL') + ' ' + r.name);
const pass = results.filter(r => r.ok).length;
console.log(`\nv29 fixes: ${pass}/${results.length} passed`);
process.exit(pass === results.length ? 0 : 1);
