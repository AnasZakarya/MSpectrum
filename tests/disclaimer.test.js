// Disclaimer box and footer. Main pages (AutoEDSSguide mode picker, Score Hub home, Check my MS start,
// Criteria Checker) carry one "Use and limitations" box: a page sentence, an optional page point, then
// the same 3 shared points in the same order, and a copyright/links line. Sub-pages carry a short footer.
const fs = require('fs'), path = require('path');
const R = f => fs.readFileSync(path.join(__dirname, '..', f), 'utf8');
const files = { 'index.html': R('index.html'), 'scores.html': R('scores.html'), 'mcdonald.html': R('mcdonald.html') };
let pass = 0, fail = 0;
const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL: ' + m); } };
const boxes = {};
for (const [f, s] of Object.entries(files)) {
  const re = /<div class="tool-disclaimer no-print" data-disc="(\w+)">([\s\S]*?)<div class="disc-foot">([\s\S]*?)<\/div>/g; let m;
  while ((m = re.exec(s))) { ok(!boxes[m[1]], 'duplicate box ' + m[1]); boxes[m[1]] = { f, body: m[2], foot: m[3] }; }
  ok(s.split('class="tool-disclaimer no-print"').length - 1 === Object.values(boxes).filter(b => b.f === f).length, f + ': every box has data-disc and a disc-foot');
}
const want = { edss: 'index.html', hub: 'scores.html', report: 'scores.html', mcd: 'mcdonald.html' };
for (const [k, f] of Object.entries(want)) ok(boxes[k] && boxes[k].f === f, 'box ' + k + ' in ' + f);
ok(Object.keys(boxes).length === 4, 'exactly 4 boxes (no box on the home page)');
const li = b => b.match(/<li>[\s\S]*?<\/li>/g) || [];
const shared = li(boxes.mcd.body);
ok(shared.length === 3 && /Not a medical device/.test(shared[0]) && /Privacy/.test(shared[1]) && /Independence/.test(shared[2]), 'shared points: device, privacy, independence');
for (const k of Object.keys(boxes)) {
  const b = boxes[k];
  ok(/<span>Use and limitations<\/span>/.test(b.body), k + ': title');
  ok(JSON.stringify(li(b.body).slice(-3)) === JSON.stringify(shared), k + ': same 3 shared points, same order, at the end');
  ok(li(b.body).length === (k === 'mcd' ? 3 : 4), k + ': at most one page point');
  ok(/&copy; 2026 Anas Z\. Nourelden/.test(b.foot) && /#about-disclaimer">Full disclaimer</.test(b.foot) && /#cite"/.test(b.foot) && /mailto:/.test(b.foot), k + ': copyright and links inside the box');
}
ok(!/Neurostatus/.test(boxes.edss.body) && /Kurtzke/.test(boxes.edss.body), 'AutoEDSSguide box cites Kurtzke and published rules, no Neurostatus name');
ok(!/Centre Nr\/Country|Name of EDSS rater|v04\/10\.2|Not an official Neurostatus form/.test(files['index.html']), 'no Neurostatus form labels or booklet citation');
ok(/On the origin of Neurostatus/.test(files['index.html']) && /Fouad AM/.test(files['index.html']) && /Sen S\./.test(files['index.html']) && /edss \(Dobra/.test(files['index.html']), 'combined EDSS sources in About');
const FOOT1 = 'MSpectrum supports, but does not replace, clinical judgment. It is not an official product of, or endorsed by, any university, hospital or government agency.';
for (const [f, s] of Object.entries(files)) {
  for (const gone of ['disclaimer-bar', 'info-card-warn', 'tool-disclaimer-footer', 'Not a diagnosis</span>']) ok(!s.includes(gone), f + ': no ' + gone);
  ok(!/judgement/i.test(s), f + ': spelling "judgment"');
  ok(!/MSpectrum is not affiliated with it\./.test(s), f + ': no Neurostatus line in footers');
}
ok(files['index.html'].includes('<p>' + FOOT1 + '</p>') && files['scores.html'].includes('<p>' + FOOT1 + '</p>'), 'sub-page footer line');
ok(!files['mcdonald.html'].includes('class="site-foot'), 'Criteria Checker: box only, no second footer');
ok(/#landing\.active ~ \.site-foot\{display:none\}/.test(files['index.html']), 'index: sub-page footer hidden on home and mode picker');
ok(/body:has\(#home:not\(\[style\*="none"\]\)\) \.site-foot,body:has\(#p_report\.active\) \.site-foot\{display:none\}/.test(files['scores.html']), 'Score Hub: footer hidden where the box is');
ok(/<details class="about-toggle" id="about-disclaimer">/.test(files['index.html']), 'About disclaimer anchor');
ok(/Neurostatus-UHB AG, the National MS Society, Western Psychological Services, PAR, Pearson/.test(files['index.html']), 'About names the instrument owners');
console.log(`Disclaimer/footer: ${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
