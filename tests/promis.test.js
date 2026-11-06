// PROMIS conversion-table regression: locks every raw->T and raw->SE value to the
// official HealthMeasures manuals (PROMIS-29 v2.1; Pain Interference 4a v1.0;
// Cognitive Function Abilities 4a v2.0). If anyone edits a table, this fails.
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');
try { (0, eval)(code); } catch (e) {}

const T = {
  phys:[22.5,26.6,28.9,30.5,31.9,33.2,34.4,35.6,36.7,37.9,39.2,40.5,41.9,43.5,45.5,48.3,57.0],
  anx:[40.3,48.0,51.2,53.7,55.8,57.7,59.5,61.4,63.4,65.3,67.3,69.3,71.2,73.3,75.4,77.9,81.6],
  dep:[41.0,49.0,51.8,53.9,55.7,57.3,58.9,60.5,62.2,63.9,65.7,67.5,69.4,71.2,73.3,75.7,79.4],
  fat:[33.7,39.7,43.1,46.0,48.6,51.0,53.1,55.1,57.0,58.8,60.7,62.7,64.6,66.7,69.0,71.6,75.8],
  sleep:[32.0,37.5,41.1,43.8,46.2,48.4,50.5,52.4,54.3,56.1,57.9,59.8,61.7,63.8,66.0,68.8,73.3],
  social:[27.5,31.8,34.0,35.7,37.3,38.8,40.5,42.3,44.2,46.2,48.1,50.0,51.9,53.7,55.8,58.3,64.2],
  painint:[41.6,49.6,52.0,53.9,55.6,57.1,58.5,59.9,61.2,62.5,63.8,65.2,66.6,68.0,69.7,71.6,75.6],
};
const SE = {
  phys:[4.0,2.8,2.5,2.4,2.3,2.3,2.3,2.3,2.3,2.3,2.4,2.4,2.5,2.6,2.8,3.3,6.6],
  anx:[6.1,3.6,3.1,2.8,2.7,2.6,2.6,2.6,2.6,2.7,2.7,2.7,2.7,2.7,2.7,2.9,3.7],
  dep:[6.2,3.2,2.7,2.4,2.3,2.3,2.3,2.3,2.3,2.3,2.3,2.3,2.3,2.4,2.4,2.6,3.6],
  fat:[4.9,3.1,2.7,2.6,2.5,2.5,2.4,2.4,2.3,2.3,2.3,2.4,2.4,2.4,2.5,2.7,3.9],
  sleep:[5.2,4.0,3.7,3.5,3.5,3.4,3.4,3.4,3.4,3.4,3.3,3.3,3.3,3.4,3.4,3.7,4.6],
  social:[4.1,2.5,2.3,2.2,2.1,2.2,2.3,2.3,2.3,2.3,2.2,2.2,2.2,2.3,2.3,2.7,5.1],
  painint:[6.1,2.5,2.0,1.9,1.9,1.9,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.8,1.9,2.1,3.7],
};
const COG_T=[26.6,30.7,33.2,35.4,37.3,39.0,40.7,42.4,44.1,45.8,47.6,49.5,51.4,53.6,56.1,59.3,64.9];
const COG_SE=[4.8,3.8,3.6,3.5,3.4,3.3,3.3,3.3,3.3,3.4,3.4,3.4,3.5,3.5,3.7,4.1,5.5];

const results = [];
const near = (a,b) => Math.abs(a-b) < 0.05;
for (const k of Object.keys(T)) {
  let okT=true, okSE=true;
  for (let raw=4; raw<=20; raw++){
    if(!near(global.promisT(k,raw), T[k][raw-4])) okT=false;
    if(!near(global.promisSE(k,raw), SE[k][raw-4])) okSE=false;
  }
  results.push({name:`${k} T-table matches official`, ok:okT});
  results.push({name:`${k} SE-table matches official`, ok:okSE});
}
// Cognitive: read the source arrays directly (they are consts, not exported)
function arr(name){ const m=html.match(new RegExp('const '+name+'\\s*=\\s*\\[([^\\]]*)\\]')); return m? m[1].split(',').map(x=>parseFloat(x)) : null; }
const cogT=arr('PROMIS_COG_T'), cogSE=arr('PROMIS_COG_SE');
results.push({name:'Cognitive 4a T-table matches official', ok: cogT && cogT.length===17 && cogT.every((v,i)=>near(v,COG_T[i]))});
results.push({name:'Cognitive 4a SE-table matches official', ok: cogSE && cogSE.length===17 && cogSE.every((v,i)=>near(v,COG_SE[i]))});

module.exports = { results };
if (require.main === module) {
  for (const r of results) console.log(`  ${r.ok?'ok  ':'FAIL'} ${r.name}`);
  const f = results.filter(r=>!r.ok).length;
  console.log(`\nPROMIS tables: ${results.length-f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
