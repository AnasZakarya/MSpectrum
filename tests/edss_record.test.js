// EDSS record (Final Sheet / scanner export): every value box of the sheet is carried into the
// transcription list, page 1 uses Kurtzke order, and no paper-form wording or header is reproduced.
const fs = require('fs'), path = require('path');
const s = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
let pass = 0, fail = 0; const ok = (c, m) => { if (c) pass++; else { fail++; console.log('FAIL: ' + m); } };
const rowsSrc = s.slice(s.indexOf('const ER_ROWS = ['), s.indexOf('const ER_SEC ='));
const covered = new Set([...rowsSrc.matchAll(/"([a-z]+(?:-[a-z0-9]+)+)"/g)].map(m => m[1]));
const sheet = s.slice(s.indexOf('id="sc-review"'), s.indexOf('<!-- Results -->', s.indexOf('id="sc-review"')));
const ids = [...sheet.matchAll(/<input[^>]*\bid="([^"]+)"/g)].map(m => m[1]);
const skip = /^(syn-|fs-|edss-step-val|dob-|doe-|study-name|patient-id|centre-nr|rater-name|sc-amb-score-display)/;
const missing = ids.filter(id => !skip.test(id) && !covered.has(id));
ok(ids.length > 100, 'sheet inputs found (' + ids.length + ')');
ok(missing.length === 0, 'every sheet value box is in the transcription list; missing: ' + missing.join(','));
ok(/const ER_KURTZKE_ORDER = \["P","C","BS","S","BB","V","CB"\]/.test(s), 'page 1 in Kurtzke 1983 order');
ok(/const ER_PAPER_ORDER = \["V","BS","P","C","S","BB","CB","A"\]/.test(s), 'page 2 in paper-form sequence');
ok(/container\.innerHTML = buildEdssRecordHTML\(r\)/.test(s), 'Final Sheet uses the MSpectrum record');
ok(/function scExportSheet\(\)\{[\s\S]{0,1500}buildEdssRecordHTML\(r\)/.test(s), 'scanner export uses the same record');
ok((s.match(/legacyCloneFinalSheet\(/g)||[]).length===1 && (s.match(/scExportSheetLegacy\(/g)||[]).length===1 && (s.match(/_syncExplainSheetPage\(/g)||[]).length===1, 'legacy paper-form outputs kept in code but never called');
ok(!/Centre Nr\/Country|Name of EDSS rater|v04\/10\.2|Kappos 2011/.test(s), 'no form header labels or booklet citation');
const ns = (s.match(/neurostatus/gi) || []).length;
ok(ns <= 8, 'Neurostatus only in the trademark notice and paper titles (' + ns + ')');
// Form -> sheet mapping used by the record: right goes to right, left to left, and every record box has a source.
const seg = s.slice(s.indexOf('function syncFinalSheet'), s.indexOf('function scAmbSync'));
const fwd = {}; for (const m of seg.matchAll(/setVal\("([a-z0-9-]+)",\s*inp\.([A-Za-z0-9_]+)/g)) fwd[m[1]] = m[2];
const side = (x, re1, re2) => re1.test(x) ? 'R' : re2.test(x) ? 'L' : null;
const swapped = Object.entries(fwd).filter(([sid, key]) => { const a = side(sid, /-(r|od)$/, /-(l|os)$/), b = side(key, /_(R|od)$/, /_(L|os)$/); return a && b && a !== b; });
ok(swapped.length === 0, 'no right/left swap between form and record: ' + JSON.stringify(swapped));
const noSrc = [...rowsSrc.matchAll(/\[([^\[\]]*)\],"[a-z]+"/g)].flatMap(m => [...m[1].matchAll(/"([a-z0-9-]+)"/g)].map(x => x[1])).filter(id => !fwd[id]);
ok(JSON.stringify(noSrc.sort()) === JSON.stringify(['amb-assistance-text','c-other-rebound','p-opt-lift-l','p-opt-lift-r']), 'only rebound (worst value), help text and single-leg raise have no direct form key: ' + noSrc.join(','));
console.log(`EDSS record: ${pass}/${pass + fail} checks passed`);
process.exit(fail ? 1 : 0);
