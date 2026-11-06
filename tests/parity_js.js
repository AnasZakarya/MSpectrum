// Reads cases JSON from argv[2], prints JS engine results as JSON (used by tests/parity_check.py).
const fs = require('fs');
const { loadEngine } = require('./load_engine');
const E = loadEngine();
const cases = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const keys = ["visual_fs","visual_fs_conv","brainstem_fs","pyramidal_fs","cerebellar_fs","cerebellar_x","sensory_fs",
  "bb_fs","bb_fs_conv","cerebral_fs","cerebral_fs_step","cerebral_mood_only","ambulation_score","ambulation_source","score_profile","edss_step"];
const out = cases.map(c => { const r = E.calculateFullEDSS(c); const o = {}; keys.forEach(k => o[k] = r[k]); return o; });
process.stdout.write(JSON.stringify(out));
