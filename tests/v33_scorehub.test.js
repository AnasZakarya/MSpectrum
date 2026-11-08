// v33 Score Hub regressions: Fellows 2020 written SDMT norms (oracle = the authors' Excel
// calculator formulas), official FES-I and SymptoMScreen wording, no WPS-manual table.
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');
try { (0, eval)(code); } catch (e) {}
const results = [];
const near = (a, b) => Math.abs(a - b) < 0.01;
// sex in the paper: 1 = female, 2 = male
const cases = [[45,52,'F',16,37.5296],[60,30,'M',12,52.2625],[30,80,'F',10,36.0619],[84,20,'M',20,73.0812],[20,70,'M',8,23.0069]];
for (const [raw, age, sex, edu, T] of cases) {
  const r = global.sdmtWrittenFellows(raw, age, sex, edu);
  results.push({ name: `Fellows written SDMT raw ${raw}, age ${age}, ${sex}, edu ${edu} -> T ${T}`, ok: r && near(50 + 10 * r.z, T) });
}
results.push({ name: 'Fellows: age 95 out of range', ok: global.sdmtWrittenFellows(40, 95, 'F', 12).oor === true });
results.push({ name: 'no Centofanti / WPS-manual written table', ok: !/CENTOFANI_WRITTEN/.test(html) });
results.push({ name: 'FES-I item 1 official wording', ok: html.includes('Cleaning the house (e.g. sweep, vacuum or dust)') });
results.push({ name: 'FES-I item 16 official wording', ok: html.includes('Going out to a social event (e.g. religious service, family gathering or club meeting)') });
results.push({ name: 'SymptoMScreen official domain names', ok: html.includes('2:"Hand function/Dexterity"') && html.includes('10:"Cognitive function"') });
module.exports = { results };
if (require.main === module) {
  for (const r of results) console.log(`  ${r.ok ? 'ok  ' : 'FAIL'} ${r.name}`);
  const f = results.filter(r => !r.ok).length;
  console.log(`\nv33 Score Hub: ${results.length - f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
