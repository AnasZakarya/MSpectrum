// Score & norm converter (scores.html): drives runConvert() and checks output HTML.
const fs=require('fs'); const path=require('path');
const { install } = require('./dom_stub');
install();
const doc=global.document;
const html=fs.readFileSync(path.join(__dirname,'..','scores.html'),'utf8');
const code=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).join('\n;\n');
try{(0,eval)(code);}catch(e){}

const results=[];
function run(tool,input){ doc.getElementById('conv_tool').value=tool; doc.getElementById('conv_in').value=input; doc.getElementById('conv_out').innerHTML=''; try{global.runConvert();}catch(e){return 'THREW:'+e.message;} return doc.getElementById('conv_out').innerHTML; }
const has=(name,out,...needles)=>results.push({name, ok: needles.every(n=>out.includes(n))});

has('PHQ-9 total+band+ID', run('phq9','A001, 2,1,3,2,0,1,2,1,0'), '12 / 27','Moderate','A001');
has('PHQ-9 severe (no ID)', run('phq9','3 3 2 3 2 3 3 2 1'), '22 / 27','Severe');
has('SDMT z+percentile', run('sdmt','P1 45 52 F 16'), 'Percentile');
has('PROMIS-29 T+SE (all 3)', run('promis29','X '+Array(28).fill('3').join(' ')), '36.7','2.3');
has('CVLT LDFR T', run('cvlt','c1,8,10,11,12,13,12,40,F,16'), 'LDFR T');
has('ARMSS 4.0x40=7.03', run('armss','p 4.0 40'), '7.03');
has('MSSS 4.0x10 (upd 6.26, orig 5.267)', run('msss','p 4.0 10'), '6.26','5.267');
has('tab-separated', run('gad7','g1\t1\t2\t1\t0\t2\t1\t1'), '8 / 21');
has('wrong length flagged', run('phq9','bad 1 2 3'), 'expected 9 values');

module.exports={results};
if(require.main===module){ for(const r of results) console.log(`  ${r.ok?'ok  ':'FAIL'} ${r.name}`); const f=results.filter(r=>!r.ok).length; console.log(`\nConverter: ${results.length-f}/${results.length} passed`); process.exit(f?1:0); }
