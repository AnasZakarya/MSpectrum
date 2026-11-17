// EDSS Calculator (known FS grades + walking): fsCalcCompute uses the same engine rules.
const { loadEngine } = require('./load_engine');
const E = loadEngine();
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL: ' + m); } };
const C = E.fsCalcCompute;
const z = { pyramidal: 0, cerebellar: 0, brainstem: 0, sensory: 0, bb: 0, visual: 0, cerebral: 0 };
const has = (r, re) => r.flags.some(f => re.test(f.text));

ok(C({ ...z, as: 0 }).edss === 0, 'all normal, normal walking = 0');
ok(C({}).empty === true && C({}).flags.length === 0, 'empty state has no flags');
ok(C({ ...z, pyramidal: 2, cerebellar: 2, sensory: 2, bb: 2, as: 0 }).edss === 3.0, 'four FS grade 2 = 3.0');
const g = C({ ...z, pyramidal: 2, cerebellar: 2, sensory: 2, bb: 2, as: 2 });
ok(g.edss === 4.5 && has(g, /far apart/), 'walking floor 4.5 above FS 3.0, gap flagged');
ok(C({ ...z, pyramidal: 3, cerebellar: 2, brainstem: 2, as: 0 }).edss === 3.5, 'FS 3 + two FS 2 = 3.5');
const v = C({ ...z, visual: 4, as: 0 });
ok(v.fs.visual === 3 && v.edss === 3.0 && has(v, /Visual grade 4 counts as 3/), 'visual raw 4 converted to 3');
const b = C({ ...z, bb: 6, as: 0 });
ok(b.fs.bb === 5 && has(b, /counts as 5/), 'bowel/bladder raw 6 converted to 5');
const m = C({ ...z, cerebral: 1, cerebral_mood_only: true, as: 0 });
ok(m.edss === 0 && m.moodOnly && has(m, /mood change alone/), 'cerebral grade 1 mood only not counted');
ok(C({ ...z, cerebral: 1, as: 0 }).edss === 1.0, 'cerebral grade 1 (not mood only) counts');
const p = C({ ...z, pyramidal: 2, cerebellar: 2 });
ok(p.provisional && p.edss === 2.5 && /Walking not entered/.test(p.reason) && has(p, /Walking is not entered/), 'no walking = provisional FS pattern');
ok(C({ ...z, as: 10 }).edss === 7.0 && C({ ...z, as: 8 }).edss === 6.5 && C({ ...z, as: 6 }).edss === 6.0, 'walking-fixed steps');
ok(has(C({ ...z, as: 4 }), /Pyramidal, Cerebellar and Sensory are 0 or 1/), 'walking limited with normal motor FS flagged');
ok(C({ ...z, pyramidal: 1, as: 6 }).flags.filter(f => /Pyramidal, Cerebellar and Sensory/.test(f.text)).length === 1, 'one motor flag only (no duplicate)');
ok(has(C({ ...z, pyramidal: 2, as: 6 }), /2 or less/), 'walking-set step with motor FS 2 flagged');
ok(has(C({ ...z, pyramidal: 4, as: 0 }), /usually limits walking/), 'pyramidal 4 with normal walking flagged');
ok(has(C({ ...z, pyramidal: 4, cerebellar: 4, as: 0 }), /reaches 5\.0/), 'FS pattern 5.0 with full walking flagged');
const miss = C({ pyramidal: 2, as: 0 });
ok(has(miss, /Not entered, counted as 0: Cerebellar/), 'missing FS listed');
ok(C({ ...z, cerebellar: 2, cerebellar_x: true, as: 0 }).x === true, 'X recorded');
// walking choices map to the same Ambulation Score categories as calcAmbulationScore
const A = E.calcAmbulationScore;
const W = E.FSC_WALK;
ok(W.none[0][1] === A({ assistance: 'none', is_normal: true }), 'normal walking = AS 0');
ok(W.none[1][1] === A({ assistance: 'none', distance_m: 500 }) && W.none[2][1] === A({ assistance: 'none', distance_m: 300 })
   && W.none[3][1] === A({ assistance: 'none', distance_m: 200 }) && W.none[4][1] === A({ assistance: 'none', distance_m: 100 })
   && W.none[5][1] === A({ assistance: 'none', distance_m: 50 }), 'no-aid distances = AS 1-5');
ok(W.uni[0][1] === A({ assistance: 'unilateral', distance_m: 60 }) && W.uni[1][1] === A({ assistance: 'unilateral', distance_m: 50 }), 'one-sided aid = AS 6/8');
ok(W.bi[0][1] === A({ assistance: 'bilateral', distance_m: 130 }) && W.bi[1][1] === A({ assistance: 'bilateral', distance_m: 120 }), 'two-sided aid = AS 7/9');
ok(W.wc[0][1] === A({ assistance: 'wheelchair_indep' }) && W.wc[1][1] === A({ assistance: 'wheelchair_help' }), 'wheelchair = AS 10/11');
ok(W.bed.map(x => x[1]).join() === [A({ assistance: 'bedbound' }), A({ assistance: 'bed_much' }), A({ assistance: 'bed_helpless' }), A({ assistance: 'bed_nocomm' })].join(), 'bed = AS 12-15');
// same result as the full engine step function for random FS/AS
let same = 0;
for (let i = 0; i < 2000; i++) {
  const st = {}; E.FSC_KEYS.forEach(k => st[k] = Math.floor(Math.random() * (k === 'cerebellar' || k === 'brainstem' || k === 'cerebral' ? 6 : 7)));
  st.as = Math.floor(Math.random() * 16);
  const r = C(st);
  const ref = E.calcEDSSStep({ visual: E.visualFSConverted(st.visual), brainstem: st.brainstem, pyramidal: st.pyramidal, cerebellar: st.cerebellar, sensory: st.sensory, bb: E.bbFSConverted(st.bb), cerebral: st.cerebral }, st.as);
  if (r.edss === ref) same++;
}
ok(same === 2000, 'fsCalcCompute = calcEDSSStep on 2000 random cases (' + same + ')');
console.log(`EDSS Calculator: ${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
