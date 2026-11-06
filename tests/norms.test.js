// Normative-table regression for the Score Hub cognitive/motor norms.
// Drives the live norm functions with stubbed inputs and locks the published values.
// SDMT oral: Strober 2020, Table 5 (age x sex x education). Verified vs Norms/SDMT.pdf.
const fs = require('fs'); const path = require('path');
const { install } = require('./dom_stub');
install();
const html = fs.readFileSync(path.join(__dirname, '..', 'scores.html'), 'utf8');
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n;\n');

// controllable input map for el(id).value
const inputs = {};
global.document.getElementById = (id) => ({
  value: (id in inputs) ? inputs[id] : '',
  classList:{add(){},remove(){},toggle(){},contains(){return false;}},
  parentNode:{classList:{add(){},remove(){},toggle(){}}},
  querySelectorAll:()=>[], addEventListener(){}, style:{}, innerHTML:'',
});
try { (0, eval)(code); } catch (e) {}

// Strober 2020 Table 5 — [mean, sd] by [edu][sex][ageband], ageband midpoints below
const T5 = {
  lo:{ M:[[65.32,10.17],[61.33,8.93],[56.77,8.42],[55.42,6.63],[50.50,8.46],[47.85,5.76]],
       F:[[64.78,8.85],[65.30,10.30],[63.33,10.51],[60.00,8.45],[55.85,8.64],[52.85,7.53]] },
  hi:{ M:[[67.55,10.92],[62.65,6.11],[66.55,8.79],[58.62,9.92],[50.80,6.75],[49.18,4.67]],
       F:[[65.30,9.54],[70.41,7.23],[65.38,9.99],[64.95,7.31],[56.17,4.90],[52.35,8.06]] },
};
const ageForBand = [20,30,40,50,60,70]; // <25,25-34,35-44,45-54,55-64,65-74
const near = (a,b) => Math.abs(a-b) < 0.005;
const results = [];
for (const edu of ['lo','hi']) for (const sex of ['M','F']) for (let b=0;b<6;b++){
  inputs.sdmt_raw='50'; inputs.sdmt_age=String(ageForBand[b]); inputs.sdmt_sex=sex; inputs.sdmt_edu=(edu==='lo'?'12':'16'); inputs.sdmt_ver='oral';
  const nm = global.sdmtNorm();
  const ok = nm && near(nm.mean, T5[edu][sex][b][0]) && near(nm.sd, T5[edu][sex][b][1]);
  results.push({name:`SDMT ${edu}/${sex}/band${b} = ${T5[edu][sex][b][0]}(${T5[edu][sex][b][1]})`, ok});
}

// --- BVMT-R / CVLT-II: Marrie 2021 Table 3 regression coefficients (verified vs Norms/CVLT-II.pdf & BVMT-R.pdf) ---
// age=36.12 -> centered age 0, so these exercise Constant+Sex+Educ(+Race) and SD.
function zclose(name, got, want){ results.push({name, ok: got!=null && Math.abs(got-want)<0.01}); }
zclose('CVLT-II z (no race)',  global.cvltNorm(50,36.12,1,12,'') && global.cvltNorm(50,36.12,1,12,'').z, 0.528);
zclose('CVLT-II z (with race)',global.cvltNorm(50,36.12,1,12,'1') && global.cvltNorm(50,36.12,1,12,'1').z, 0.422);
zclose('BVMT-R z (no race)',   global.bvmtNorm(24,36.12,1,12,'') && global.bvmtNorm(24,36.12,1,12,'').z, -0.448);
zclose('BVMT-R z (with race)', global.bvmtNorm(24,36.12,1,12,'1') && global.bvmtNorm(24,36.12,1,12,'1').z, -0.544);

// --- MSFC / PASAT-3 / T25FW / 9-HPT: Fischer 2001 reference (verified vs Norms/MSFC_Manual.pdf) ---
const srcHasRef = html.includes('pegM:0.0439') && html.includes('pegSD:0.0101') && html.includes('walkM:9.5353')
  && html.includes('walkSD:11.4058') && html.includes('pasatM:45.0311') && html.includes('pasatSD:12.0771');
results.push({name:'MSFC_REF Fischer 2001 constants present', ok: srcHasRef});
zclose('zPasat at reference mean = 0', global.zPasat(45.0311), 0);
zclose('zPasat mean+SD = 1', global.zPasat(45.0311+12.0771), 1);
zclose('zWalk at reference mean = 0', global.zWalk(9.5353), 0);
zclose('zWalk mean+SD = -1 (slower=worse)', global.zWalk(9.5353+11.4058), -1);

// --- MSSS (Roxburgh 2005 / updated global) & ARMSS (Manouchehrinia 2017) spot values ---
zclose('MSSS-orig EDSS4.0 x 10y = 5.267', global.computeMSSSorig(4.0,10), 5.267);
zclose('MSSS-orig EDSS6.0 x 5y = 8.827',  global.computeMSSSorig(6.0,5), 8.827);
zclose('MSSS-orig EDSS3.0 x 15y = 2.824', global.computeMSSSorig(3.0,15), 2.824);
zclose('MSSS-upd EDSS4.0 x 10y = 6.26',   global.computeMSSSupd(4.0,10), 6.26);
zclose('ARMSS EDSS4.0 x age40 = 7.03',    global.computeARMSS(4.0,40), 7.03);
zclose('ARMSS EDSS0.0 x age20 = 1.44',    global.computeARMSS(0.0,20), 1.44);

// --- 6MWT % predicted: Enright & Sherrill 1998 reference equations ---
(function(){ const m=global.score6MWT(500,{sex:'M',age:50,ht:175,wt:80});
  results.push({name:'6MWT predicted (male ref eq)', ok: m && Math.abs(m.pred-623.95)<0.05});
  const w=global.score6MWT(500,{sex:'F',age:50,ht:165,wt:65});
  results.push({name:'6MWT predicted (female ref eq)', ok: w && Math.abs(w.pred-577.3)<0.05});
})();


// --- CVLT-II LDFR (Parmenter 2010) — VERIFIED vs the actual paper (Norms/CVLT-II-Subscores-US.pdf):
//     Table 1 raw->scaled, Table 4 regression (const 1.648, age 0.245, age^2 -0.003, sex 1.661, educ 0.073), Table 2 residual SD 2.93344 ---
(function(){ const got=[5,6,8,9,14,16].map(r=>global._ldfrScaled(r)).join(',');
  results.push({name:'CVLT LDFR raw->scaled matches Parmenter Table 1', ok: got==='3,4,5,6,12,16'}); })();
zclose('CVLT LDFR T (Parmenter regression) raw12/age40/M/edu12 = 49.37', global.ldfrT(12,40,1,12), 49.37);

// --- BVMT-R Delayed Recall (Parmenter 2010 MACFIMS) — Table 1 raw->scaled + Table 4 regression (SD 2.37938).
//     v28: replaces the BVMT-R manual (Benedict 1997, PAR) sub-score tables. ---
(function(){
  const map=[[5,3],[6,5],[7,5],[8,6],[9,8],[10,9],[11,10],[12,13]];
  results.push({name:'BVMT-R DR raw->scaled matches MACFIMS Table 1', ok: map.every(([r,sc])=>global._bvmtDrScaled(r)===sc)});
  zclose('BVMT-R DR T raw9/age40/M/edu12 = 38.77', global.bvmtDrT(9,40,1,12), 38.77);
  zclose('BVMT-R DR T raw12/age30/F/edu16 = 57.65', global.bvmtDrT(12,30,2,16), 57.65);
  results.push({name:'Benedict manual tables removed', ok: typeof global.benedictBVMT==='undefined' && !html.includes('BENEDICT_BVMT')});
})();

// --- SDMT written norms (Centofani 1975, adopted by the Smith 1982 WPS manual) —
//     VERIFIED vs Sheridan 2006 Table 1 (Norms/SDMT-Written-Younger.pdf). ---
(function(){ const exp=[[20,55.2,7.5],[30,53.6,6.6],[40,51.1,8.1],[50,46.8,8.4],[60,41.5,8.6]];
  for(const [age,m,sd] of exp){ inputs.sdmt_ver='written'; inputs.sdmt_raw='50'; inputs.sdmt_age=String(age); inputs.sdmt_sex=''; inputs.sdmt_edu='';
    const n=global.sdmtNorm();
    results.push({name:`SDMT-written age${age} = ${m}(${sd}) [Centofani/Sheridan Table 1]`, ok:n&&Math.abs(n.mean-m)<0.005&&Math.abs(n.sd-sd)<0.005}); }
  inputs.sdmt_ver='oral';
})();

module.exports = { results };
if (require.main === module) {
  for (const r of results) if(!r.ok) console.log(`  FAIL ${r.name}`);
  const f = results.filter(r=>!r.ok).length;
  console.log(`Normative tables (SDMT Strober 2020): ${results.length-f}/${results.length} passed`);
  process.exit(f ? 1 : 0);
}
