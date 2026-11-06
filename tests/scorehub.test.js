// Score Hub sanity for scores.html: load-without-throw + structural + calc smoke.
const fs = require('fs'); const path = require('path');
const { install, loadInline } = require('./dom_stub');
install();

const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const results = [];
const rec = (name, ok, info='') => results.push({ name, ok, info });

const load = loadInline(html);
rec('found inline script blocks', load.blocks >= 1, `${load.blocks} blocks`);
rec('scores.html inline JS loads without throwing', load.ok, load.err);

const ids = [...html.matchAll(/\{id:"([a-z0-9]+)"/g)].map(m => m[1]);
rec('TOOLS array present', ids.length > 0, `${ids.length} tools`);
const missingPanel = ids.filter(id => !html.includes(`id="p_${id}"`));
rec('every tool id has a panel (p_<id>)', missingPanel.length === 0, missingPanel.join(', '));

const calcNames = [...html.matchAll(/function (calc[A-Za-z0-9_]+)/g)].map(m => m[1]);
rec('calc functions discovered', calcNames.length > 0, `${calcNames.length} functions`);
let threw = [];
if (load.ok) for (const fn of calcNames) {
  if (typeof global[fn] === 'function') { try { global[fn](); } catch (e) { threw.push(`${fn}: ${(e&&e.message)||e}`); } }
  else threw.push(`${fn}: not defined after load`);
}
rec('all calc*() run on empty input without throwing', threw.length === 0, threw.join(' | '));

module.exports = { results, toolCount: ids.length, calcCount: calcNames.length };
if (require.main === module) {
  for (const r of results) console.log(`  ${r.ok?'ok  ':'FAIL'} ${r.name}${r.info?'  ['+r.info+']':''}`);
  const f = results.filter(r => !r.ok).length;
  console.log(`\nScore Hub sanity: ${results.length-f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
