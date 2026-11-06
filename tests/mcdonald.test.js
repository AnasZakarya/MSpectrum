// McDonald checker (mcdonald.html): load-without-throw sanity.
const fs = require('fs'); const path = require('path');
const { install, loadInline } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'mcdonald.html'), 'utf8');
const load = loadInline(html);
const results = [
  { name: 'found inline script blocks', ok: load.blocks >= 1, info: `${load.blocks} blocks` },
  { name: 'mcdonald.html inline JS loads without throwing', ok: load.ok, info: load.err },
];
module.exports = { results };
if (require.main === module) {
  for (const r of results) console.log(`  ${r.ok?'ok  ':'FAIL'} ${r.name}${r.info?'  ['+r.info+']':''}`);
  const f = results.filter(r => !r.ok).length;
  console.log(`\nMcDonald checker: ${results.length-f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
