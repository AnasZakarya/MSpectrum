// Check my MS: every guided step has checklist text and a tool panel, and the report covers each step.
const fs = require('fs'), path = require('path');
const s = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL: ' + m); } };
const flow = JSON.parse(s.match(/const GFLOW=(\[\[.*?\]\]);/)[1]);
const ids = flow.map(f => f[0]);
ok(ids.join() === 'edss,pdds,fesi,mfis,pdq,smscreen,blcs,bwcs,sci,phq9,gad7,promispain,rand36', '13 steps in order');
const meta = s.match(/const GFLOW_META=\{([\s\S]*?)\n\};/)[1];
const metaIds = [...meta.matchAll(/^\s{2}(\w+):\{sub:/gm)].map(m => m[1]);
ok(JSON.stringify(metaIds) === JSON.stringify(ids), 'checklist entries match the flow exactly (no leftovers)');
for (const id of ids) ok(s.includes('id="p_' + id + '"') || new RegExp('\\n\\s*' + id + ':\\{short:').test(s), id + ': has a panel');
for (const k of ['Thinking & memory in daily life (PDQ)', 'Bladder control (BLCS)', 'Bowel control (BWCS)', 'Sleep (SCI)', 'General health & quality of life (RAND-36)']) ok(s.includes(k), 'report row: ' + k);
ok(/Thirteen short questionnaires/.test(s), '"What this covers" lists 13');
ok(/16 or less suggests probable insomnia disorder \(Espie 2014\)/.test(s), 'SCI flag uses the published cut-off');
console.log(`Check my MS: ${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
