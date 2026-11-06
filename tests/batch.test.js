// Batch scorer (scores.html): verifies batchScore() output matches single-tool results.
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');
try { (0, eval)(code); } catch (e) {}

const results = [];
const eq = (name, got, want) => results.push({ name, ok: String(got) === String(want), got, want });

const hdr = ['id'];
for (let i=1;i<=28;i++) hdr.push('pr_'+i); hdr.push('pr_pi');
for (let i=1;i<=9;i++) hdr.push('phq_'+i);
for (let i=1;i<=9;i++) hdr.push('fss_'+i);
const mkrow = (id,pr,pi,phq,fss) => { const a=[id]; for(let i=0;i<28;i++)a.push(pr); a.push(pi); for(let i=0;i<9;i++)a.push(phq); for(let i=0;i<9;i++)a.push(fss); return a.join(','); };
const csv = [hdr.join(','), mkrow('001',3,5,1,4), mkrow('002',1,'',0,7)].join('\n');

let res;
try { res = global.batchScore(csv); } catch (e) { res = { error: e.message }; }
results.push({ name: 'batchScore runs without error', ok: !!res && !res.error, got: res && res.error, want: 'no error' });

if (res && !res.error) {
  const r1 = res.rows[0], r2 = res.rows[1];
  eq('detects promis+phq+fss', res.detected.sort().join(','), 'fss,phq,promis');
  eq('S001 PROMIS phys T', r1.PROMIS_phys_T, '36.7');
  eq('S001 PROMIS phys SE', r1.PROMIS_phys_SE, '2.3');
  eq('S001 PROMIS dep T', r1.PROMIS_dep_T, '62.2');
  eq('S001 PHQ total', r1.PHQ9_total, 9);
  eq('S001 PHQ band', r1.PHQ9_band, 'Mild');
  eq('S001 FSS mean', r1.FSS_mean, '4.00');
  eq('S002 PROMIS phys T', r2.PROMIS_phys_T, '22.5');
  eq('S002 PHQ band', r2.PHQ9_band, 'Minimal');
  eq('S002 blank pain intensity', r2.PROMIS_painIntensity, '');
}

module.exports = { results };
if (require.main === module) {
  for (const r of results) console.log(`  ${r.ok?'ok  ':'FAIL'} ${r.name}${r.ok?'':'  (got '+r.got+', want '+r.want+')'}`);
  const f = results.filter(r=>!r.ok).length;
  console.log(`\nBatch scorer: ${results.length-f}/${results.length} checks passed`);
  process.exit(f ? 1 : 0);
}
