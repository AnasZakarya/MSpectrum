// v36 Score Hub regressions: RAND-36 (RAND scoring Tables 1-2), Sleep Condition Indicator (Espie 2014),
// P-MSSS lookup (Kister 2013 Figure 2), harmonized CDP thresholds (Muller 2023), Parmenter 2010 age/education
// range note, and SymptoMScreen wording (Green 2016 Figure 1). Expected values are hand-computed.
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');
try { (0, eval)(code + '\n;globalThis.__V36 = { MSQLI_SCALES, PMSSS, CONV, CONV_EG };'); } catch (e) {}
const G = (name) => { try { return (0, eval)(name); } catch (e) { return undefined; } };
const V = global.__V36 || {};
const S = V.MSQLI_SCALES || {};
const results = [];
const rec = (name, ok) => results.push({ name, ok: !!ok });
const near = (a, b) => a != null && Math.abs(a - b) < 0.001;

// RAND-36, every answer = 1. Recoded: item 1 -> 100; PF 0; RP 0; RE 0; EF (23,27 -> 100; 29,31 -> 0) 50;
// EWB (24,25,28 -> 0; 26,30 -> 100) 40; SF (20 -> 100, 32 -> 0) 50; Pain (21,22 -> 100) 100;
// GH (1 -> 100, 33 -> 0, 34 -> 100, 35 -> 0, 36 -> 100) 60.
const r36 = G('rand36Scores');
const sc = r36 && r36(Array(36).fill(1));
const want = { 'Physical functioning': 0, 'Role limitations due to physical health': 0, 'Role limitations due to emotional problems': 0, 'Energy/fatigue': 50, 'Emotional well-being': 40, 'Social functioning': 50, 'Pain': 100, 'General health': 60 };
rec('RAND-36 all 1 -> PF 0, EF 50, EWB 40, SF 50, Pain 100, GH 60', sc && sc.every(x => near(x.score, want[x.name])));
// Missing data: Social functioning with item 32 blank equals item 20 alone (RAND example).
const v2 = Array(36).fill(null); v2[19] = 2; // item 20 = 2 -> 75
const sc2 = r36 && r36(v2);
rec('RAND-36 SF with item 32 blank = item 20 (75)', sc2 && near(sc2.find(x => x.name === 'Social functioning').score, 75));
const conv = V.CONV || {};
const c36 = conv.rand36 && conv.rand36.score(Array(36).fill('1'));
rec('Converter RAND-36 matches (GH 60, Pain 100)', c36 && c36['General health'] === 60 && c36['Pain'] === 100);
rec('Converter RAND-36 flags item outside options', conv.rand36 && !!conv.rand36.score(['1', '1', '4'].concat(Array(33).fill('1')))._err);

// SCI: item scores 3,2,2,3,3,2,2,1 -> 18; 0-10 = 5.6; not <= 16. All 2 -> 16 -> probable insomnia.
const sci = S.sci && S.sci.custom([3, 2, 2, 3, 3, 2, 2, 1]);
rec('SCI 18/32, 0-10 = 5.6, not probable insomnia', sci && sci.html.includes('18<small> / 32') && sci.html.includes('<b>5.6</b>') && sci.html.includes('above 16'));
const sci2 = S.sci && S.sci.custom(Array(8).fill(2));
rec('SCI 16 -> probable insomnia disorder', sci2 && sci2.html.includes('16 or less'));
rec('Converter SCI 16 -> yes', conv.sci && conv.sci.score(Array(8).fill('2'))['Probable insomnia (16 or less)'] === 'yes');

// P-MSSS cells checked against Kister 2013 Figure 2.
const pm = G('pmsss');
const cells = [[0, 0, 2.19], [8, 0, 9.97], [3, 5, 6.27], [1, 10, 2.51], [4, 25, 4.65], [6, 34, 7.03], [2, 45, 1.13], [7, 23, 8.99]];
rec('P-MSSS table cells match Kister 2013 Figure 2', pm && cells.every(([p, y, v]) => pm(p, y).v === v));
rec('P-MSSS table is 46 x 9 and rises with PDDS in every row', V.PMSSS && V.PMSSS.length === 46 && V.PMSSS.every(r => r.length === 9 && r.every((x, i) => i === 0 || x > r[i - 1])));
rec('P-MSSS 12.7 years uses year 12', pm && pm(3, 12.7).v === 4.77);
rec('P-MSSS beyond 45 years -> out of range', pm && pm(3, 46).oor === true);

// CDP thresholds (Muller 2023): baseline 5.0 -> +1.0 needed; baseline 5.5 -> +0.5 enough.
const set = (id, v) => { global.document.getElementById(id).value = v; };
const cdp = G('calcCDP');
set('cdp_conf', '');
set('cdp_base', '5.5'); set('cdp_fu', '6'); cdp && cdp();
rec('CDP baseline 5.5 -> 6.0 meets threshold (0.5)', /Meets the progression threshold/.test(global.document.getElementById('cdp_out').innerHTML));
set('cdp_base', '5'); set('cdp_fu', '5.5'); cdp && cdp();
rec('CDP baseline 5.0 -> 5.5 does not (needs 1.0)', /does not reach the threshold/.test(global.document.getElementById('cdp_out').innerHTML));
set('cdp_base', '0'); set('cdp_fu', '1'); cdp && cdp();
rec('CDP baseline 0 -> 1.0 does not (needs 1.5)', /does not reach the threshold/.test(global.document.getElementById('cdp_out').innerHTML));

// Parmenter 2010 range (controls 20-60 y, 12-18 y education).
const pr = G('_parRange');
rec('Parmenter range: age 65 flagged, age 40/edu 16 not', pr && /outside 20-60/.test(pr(65, 16)) && pr(40, 16) === '' && /outside 12-18/.test(pr(40, 10)));

// SymptoMScreen wording (Green 2016 Figure 1).
rec('SymptoMScreen domain names and descriptors', html.includes('1:"Walking/Mobility"') && html.includes('5:"Sensory symptoms"') && html.includes('Numbness, tingling, or burning'));
rec('SymptoMScreen anchors', html.includes('moderate limitation/ I reduced my daily activities') && html.includes('total limitation/ I&rsquo;m unable to do most daily activities'));

// Gemini round-4 fixes: converter range checks, full MSQOL-54 output, written SDMT example, no promisBand.
const cre = G('_convRangeErr');
rec('Converter PHQ-9 value 99 rejected', cre && /outside 0-3/.test(cre('phq9', ['1','2','3','99','0','0','0','0','0'])));
rec('Converter FES-I blank item rejected (every item needed)', cre && /every item/.test(cre('fesi', Array(15).fill('2').concat(['NA']))));
rec('Converter ABC with 12 answers accepted, 11 rejected', cre && cre('abc', Array(12).fill('50').concat(Array(4).fill('NA'))) === null && /at least 12/.test(cre('abc', Array(11).fill('50').concat(Array(5).fill('NA')))));
const mq = conv.msqol && conv.msqol.score(V.CONV_EG.msqol.split(/[\s,]+/));
rec('Converter MSQOL-54 returns 12 subscales + 2 composites', mq && Object.keys(mq).length === 14 && 'Sexual function' in mq);
rec('Written SDMT converter example has 4 values', V.CONV_EG && V.CONV_EG.sdmt_w.split(',').length === 4);
rec('promisBand removed', !/function promisBand/.test(html));

// PIRA / RAW across visits (Muller 2023): mockup sample. Expected: RAW at visit 3 (relapse 19 days before,
// confirmed visit 4), new EDSS reference 2.5 at visits 5-6, PIRA at visit 7 confirmed at visit 8 (EDSS +1.0 from 2.5
// and T25FW +24%), 9-HPT and SDMT below threshold.
const pc = G('piraClassify'), D = s => Date.parse(s + 'T00:00:00Z');
const vis = [['2024-01-10',2.0,5.1,21.0,52],['2024-07-08',2.0,5.0,20.6,53],['2024-09-20',3.5,null,null,null],['2025-01-15',3.0,5.6,21.4,51],['2025-07-10',2.5,5.4,21.1,52],['2026-01-12',2.5,5.5,21.3,51],['2026-07-14',3.5,6.8,22.0,50],['2027-01-11',3.5,7.0,22.4,49]].map(r => ({ t: D(r[0]), edss: r[1], t25: r[2], hpt: r[3], sdmt: r[4] }));
const pa = pc && pc(vis, [D('2024-09-01')], true);
const ev = pa ? pa.events : [];
const find = (i, m, type) => ev.some(e => e.i === i && e.m === m && e.type === type);
rec('PIRA module: RAW at visit 3 (EDSS)', find(2, 'EDSS', 'RAW'));
rec('PIRA module: new EDSS reference at visit 5 (2.5)', ev.some(e => e.type === 'ref' && e.m === 'EDSS' && e.x === 2.5));
rec('PIRA module: PIRA at visit 7 (EDSS and T25FW)', find(6, 'EDSS', 'PIRA') && find(6, 'T25FW', 'PIRA'));
rec('PIRA module: no 9-HPT or SDMT events', !ev.some(e => (e.m === '9-HPT' || e.m === 'SDMT') && e.type !== 'ref'));
const pr2 = pc && pc(vis, [D('2024-09-01'), D('2026-07-01')], true);
rec('PIRA module: relapse 13 days before visit 7 turns it into RAW', pr2 && pr2.events.some(e => e.i === 6 && e.m === 'EDSS' && e.type === 'RAW'));
const pr3 = pc && pc([{ t: D('2024-01-01'), edss: 5.5 }, { t: D('2024-07-01'), edss: 6.0 }, { t: D('2025-01-01'), edss: 6.0 }], [], false);
rec('PIRA module: 5.5 -> 6.0 confirmed is PIRA (+0.5 needed from 5.5)', pr3 && pr3.events.some(e => e.type === 'PIRA'));

// Gemini round-6 checks against Muller 2023 (text: roving reference "confirmed at the following visit";
// 9-HPT/T25FW threshold ">20%"; confirmation not within 30 days before to 90 days after a relapse onset).
const sv = (rows) => rows.map(r => ({ t: D(r[0]), edss: r[1], t25: r[2] == null ? null : r[2] }));
const step = pc && pc(sv([['2024-01-01',3.0],['2024-05-01',2.5],['2024-09-01',1.5],['2025-01-01',1.5],['2025-05-01',2.5],['2025-09-01',2.5]]), [], false);
rec('PIRA: stepwise improvement 3.0 -> 2.5 -> 1.5 confirmed sets reference 1.5, then +1.0 is PIRA', step && step.events.some(e => e.type === 'ref' && e.x === 1.5) && step.events.some(e => e.type === 'PIRA' && e.i === 4));
const t20 = pc && pc(sv([['2024-01-01',2.0,5.0],['2024-05-01',2.0,6.0],['2024-09-01',2.0,6.0]]), [], true);
rec('PIRA: T25FW exactly +20% is not worsening (Muller: >20%)', t20 && !t20.events.some(e => e.m === 'T25FW' && e.type !== 'ref'));
const cw = pc && pc(sv([['2024-01-01',2.0],['2024-03-01',3.0],['2024-06-10',3.0],['2024-12-01',3.0]]), [D('2024-06-01')], false);
rec('PIRA: confirmation inside a relapse window is skipped; later clean visit confirms PIRA', cw && cw.events.some(e => e.type === 'PIRA' && e.i === 1 && e.j === 3));
const cw2 = pc && pc(sv([['2024-01-01',2.0],['2024-03-01',3.0],['2024-06-10',3.0]]), [D('2024-06-01')], false);
rec('PIRA: only confirmation inside a relapse window -> unclassified, reference not raised', cw2 && cw2.events.some(e => e.type === 'unclassified') && !cw2.events.some(e => e.type === 'PIRA'));

const cfe = G('_convFieldErr');
const mqv = V.CONV_EG && V.CONV_EG.msqol.split(/[\s,]+/); const mqBad = mqv && mqv.slice(); if (mqBad) mqBad[52] = '99';
rec('Converter MSQOL-54: example accepted, item 53 = 99 rejected', cfe && cfe('msqol', mqv) === null && /item 53/.test(cfe('msqol', mqBad)));
rec('Converter BVMT-R trial 99 rejected; ARMSS EDSS 4.2 rejected', cfe && /value 1/.test(cfe('bvmt', ['99','10','10','10','40','F','16'])) && /0.5 steps/.test(cfe('armss', ['4.2','45'])) && cfe('armss', ['4.5','45']) === null);

// Gemini round-5 fixes: quick-fill buttons hidden in the patient flow, readable scale labels.
rec('PROMIS Cog, ABC and FES-I quick-fill rows hidden in patient flow', ['fillPromisCog(5)','fillABC(100)','fillFesi(1)'].every(f => new RegExp('<div class="actions fill-row">\\s*<button class="btn" onclick="' + f.replace(/[()]/g, '\\$&')).test(html)));
rec('Scale labels at least 9.5px', /\.scale \.sc-t\{font-size:9\.5px/.test(html));

module.exports = { results };
if (require.main === module) {
  for (const x of results) console.log(`  ${x.ok ? 'ok  ' : 'FAIL'} ${x.name}`);
  const f = results.filter(x => !x.ok).length;
  console.log(`\nv36 Score Hub: ${results.length - f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
