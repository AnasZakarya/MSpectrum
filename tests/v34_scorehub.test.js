// v34 Score Hub regressions: MSQLI MHI-18, PDQ, MSSS and SSS scored as in the 1997 MSQLI
// User's Manual (hand-computed expected values), and the oral SDMT reliable-change helper
// (Strober 2022: 6 months 7/8/10, 1 year 8/10/12 points at 70/80/90% confidence).
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');
try { (0, eval)(code + '\n;globalThis.__V34 = { MSQLI_SCALES, SDMT_RCI };'); } catch (e) {}
const G = (name) => { try { return (0, eval)(name); } catch (e) { return undefined; } };
const V = global.__V34 || {};
const S = V.MSQLI_SCALES || {};
const results = [];
const rec = (name, ok) => results.push({ name, ok: !!ok });
const fill = (n, f) => Array.from({ length: n }, (_, k) => f(k + 1));
const has = (r, txt) => r && r.html && r.html.includes(txt);

// MHI-18: all answers 1 ("All of the time"). Reversed items 1,3,5,7,8,10,13,15 become 6.
// Total mean = (8*6 + 10*1)/18 = 3.222 -> 44.4; Anxiety (4,6,10r,11,18) mean 2 -> 20.0;
// Depression 0.0; Behavioral Control (5r,8r,16,17) mean 3.5 -> 50.0; Positive Affect 100.0.
let r = S.mhi && S.mhi.custom(fill(18, () => 1));
rec('MHI-18 total 44.4 with all answers 1', has(r, '44.4'));
rec('MHI-18 Anxiety 20.0 / Depression 0.0 / Behavioral Control 50.0 / Positive Affect 100.0',
  has(r, 'Anxiety <b>20.0') && has(r, 'Depression <b>0.0') && has(r, 'Behavioral Control <b>50.0') && has(r, 'Positive Affect <b>100.0'));
r = S.mhi && S.mhi.custom(fill(18, i => (i <= 8 ? 1 : null)));
rec('MHI-18 total not computed with 10 items skipped', r && !r.done && !has(r, '/ 100'));
r = S.mhi && S.mhi.custom(fill(18, i => (i === 2 || i === 9 || i === 12 ? null : 6)));
rec('MHI-18 Depression n/c when 3 of its 4 items are skipped', has(r, 'Depression <b>n/c'));

// PDQ: all 2 -> total 40, each subscale and PDQ-5 = 10.
r = S.pdq && S.pdq.custom(fill(20, () => 2));
rec('PDQ total 40, subscales 10/20', has(r, '40<small> / 80') && has(r, 'Attention/Concentration <b>10</b>/20') && has(r, 'PDQ-5 <b>10</b>/20'));
rec('PDQ needs every item', S.pdq && S.pdq.custom(fill(20, i => (i === 1 ? null : 2))) === null);

// MSSS: all 3 -> every subscale (3-1)/4*100 = 50.0, total 50.0, MSSS-5 50.0; all 5 -> 100.
r = S.msss && S.msss.custom(fill(18, () => 3));
rec('MSSS all 3 -> 50.0 everywhere', has(r, '50.0<small> / 100') && has(r, 'Tangible <b>50.0') && has(r, 'MSSS-5 <b>50.0'));
r = S.msss && S.msss.custom(fill(18, () => 5));
rec('MSSS all 5 -> 100.0', has(r, '100.0<small> / 100'));

// SSS: partner yes, items 2-5 = 3 -> 12 / 24; no partner -> skipped.
r = S.sss && S.sss.custom([1, 3, 3, 3, 3]);
rec('SSS items 2-5 = 3 -> 12', has(r, '12<small> / 24'));
r = S.sss && S.sss.custom([0, null, null, null, null]);
rec('SSS skipped with no primary partner', r && r.done && has(r, 'No primary partner'));

// SDMT reliable change (oral).
const RCI = V.SDMT_RCI;
rec('SDMT RCI values (Strober 2022)', RCI && JSON.stringify(RCI[6]) === '[7,8,10]' && JSON.stringify(RCI[12]) === '[8,10,12]');
const set = (id, v) => { global.document.getElementById(id).value = v; };
set('sdmt_prev', '50'); set('sdmt_int', '6');
const chg = G('sdmtChange');
rec('SDMT -10 over 6 months -> reliable at 90%', chg && chg(40, 'oral').includes('90% confidence'));
rec('SDMT -5 over 6 months -> not reliable', chg && chg(45, 'oral').includes('smaller than the reliable-change threshold'));
set('sdmt_int', '12');
rec('SDMT -8 over 1 year -> reliable at 70%', chg && chg(42, 'oral').includes('70% confidence'));
rec('SDMT written -> oral-only note', chg && chg(42, 'written').includes('oral SDMT only'));

module.exports = { results };
if (require.main === module) {
  for (const x of results) console.log(`  ${x.ok ? 'ok  ' : 'FAIL'} ${x.name}`);
  const f = results.filter(x => !x.ok).length;
  console.log(`\nv34 Score Hub: ${results.length - f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
