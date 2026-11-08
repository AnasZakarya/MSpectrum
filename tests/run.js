// MSpectrum test runner — one command to verify the whole app.
//   node tests/run.js   (or: npm test)
// Each suite is run in an isolated child process so DOM stubs never collide.
const { execFileSync } = require('child_process');
const path = require('path');
const suites = ['engine.test.js', 'v29.test.js', 'scorehub.test.js', 'convert.test.js', 'promis.test.js', 'norms.test.js', 'v33_scorehub.test.js', 'v34_scorehub.test.js', 'mcdonald.test.js'];
let failed = 0;
for (const s of suites) {
  console.log('\n=== ' + s + ' ===');
  try { console.log(execFileSync('node', [path.join(__dirname, s)], { encoding: 'utf8' }).trim()); }
  catch (e) { failed++; console.log((e.stdout||'').trim()); console.log((e.stderr||'').trim()); }
}
// v29: JS-Python engine parity (needs python3; skipped if it is not installed)
console.log('\n=== parity_check.py (JS vs edss_calc.py) ===');
for (const py of ['python3', 'python']) {
  try { console.log(execFileSync(py, [path.join(__dirname, 'parity_check.py'), '2000'], { encoding: 'utf8' }).trim()); break; }
  catch (e) { if (e.code === 'ENOENT') { if (py === 'python') console.log('skipped (python not found)'); continue; } failed++; console.log((e.stdout||'').trim()); break; }
}
console.log('\n' + '='.repeat(40));
console.log(failed ? `❌ ${failed} suite(s) FAILED` : '✅ ALL SUITES PASSED');
process.exit(failed ? 1 : 0);
