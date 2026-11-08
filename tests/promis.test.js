// v33: PROMIS raw-to-T and SE tables were removed (HealthMeasures permission pending).
// This test makes sure no PROMIS conversion table ships, and that raw domain sums still work.
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');
try { (0, eval)(code); } catch (e) {}
const results = [];
results.push({ name: 'no PROMIS_T table in scores.html', ok: !/const\s+PROMIS_T\s*=/.test(html) });
results.push({ name: 'no PROMIS_SE table in scores.html', ok: !/const\s+PROMIS_SE\s*=/.test(html) });
results.push({ name: 'no PROMIS_COG_T table in scores.html', ok: !/PROMIS_COG_T/.test(html) });
results.push({ name: 'no verbatim PROMIS pain stem', ok: !/how would you rate your pain on average/i.test(html) });
const resp = {}; for (let i = 1; i <= 28; i++) resp[i] = (i % 5) + 1;
const o = global.scorePROMIS(resp, 3);
results.push({ name: 'raw domain sums computed', ok: o.phys === 2+3+4+5 && o.painIntensity === 3 });
const partial = { 1: 1, 2: 2, 3: 3 };
results.push({ name: 'incomplete domain -> null', ok: global.scorePROMIS(partial, null).phys === null });
module.exports = { results };
if (require.main === module) {
  for (const r of results) console.log(`  ${r.ok ? 'ok  ' : 'FAIL'} ${r.name}`);
  const f = results.filter(r => !r.ok).length;
  console.log(`\nPROMIS (raw sums only): ${results.length - f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
