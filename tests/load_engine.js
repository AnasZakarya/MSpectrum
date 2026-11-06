// MSpectrum test harness — loads the EDSS engine straight out of index.html.
// The engine's pure-function region ends with an `if(false){ module.exports = {...} }`
// hook. We slice that region (no DOM calls in it), flip the guard to true, write a
// temp module, and require it. Zero external dependencies.
const fs = require('fs');
const path = require('path');

function loadEngine() {
  const idx = path.join(__dirname, '..', 'index.html');
  const html = fs.readFileSync(idx, 'utf8');
  // First BARE <script> (line ~3815) — attribute scripts like ld+json don't match /<script>\n/.
  const m = html.match(/<script>\n([\s\S]*?)\n<\/script>/);
  if (!m) throw new Error('engine <script> block not found');
  const block = m[1];
  const cut = block.indexOf('module.exports');
  if (cut < 0) throw new Error('module.exports hook not found — did the export block move?');
  const objEnd = block.indexOf('};', cut);          // end of the exports object literal
  const ifEnd = block.indexOf('}', objEnd + 2) + 1; // closing brace of the if(...) block
  let engine = block.slice(0, ifEnd).replace('if (false) {', 'if (true) {');
  const tmp = path.join(__dirname, '_engine.gen.js');
  fs.writeFileSync(tmp, engine);
  delete require.cache[require.resolve(tmp)];
  return require(tmp);
}

module.exports = { loadEngine };

if (require.main === module) {
  const E = loadEngine();
  console.log('Exported keys:', Object.keys(E).join(', '));
  // smoke: all-normal patient => EDSS 0
  const r = E.calculateFullEDSS({});
  console.log('Smoke all-normal:', JSON.stringify(r).slice(0, 300));
}
