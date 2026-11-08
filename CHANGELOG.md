# Changelog

## v34 (2026-11-08): more MSQLI scales, SDMT reliable change, clean-up

### MS Score Hub
- **New MSQLI scales** (NMSS MSQLI User's Manual, 1997; items and scoring as in the manual): Mental Health Inventory (MHI-18: total and Anxiety, Depression, Behavioral Control and Positive Affect subscales, 0-100, with the manual's missing-item rules), Perceived Deficits Questionnaire (PDQ-20 with 4 subscales and PDQ-5), MOS Modified Social Support Survey (4 subscales, total and MSSS-5, 0-100) and Sexual Satisfaction Scale (4-24, skipped when there is no primary partner).
- **SDMT change between visits**: optional previous oral SDMT and interval (about 6 months or 1 year); the change is compared with the reliable-change indices of Strober 2022 (7/8/10 points at 6 months, 8/10/12 points at 1 year for 70/80/90% confidence). Written SDMT age field now allows 91.
- Percentile labels now use correct ordinals (1st, 2nd, 3rd instead of 1th, 2th, 3th).
- References list: MSQLI, TUG and 2MWT added; the PROMIS-29 and PROMIS Cognitive 4a entries no longer mention T-score tables (missed in v33).

### AutoEDSSguide
- Removed the last two mentions of the members-only Neurostatus Forum (an ambulation note shown to users and a code comment). The 50 m rule note now cites the published rule (Kappos 2011); the restricted-ambulation check is described as a plausibility check.

### Repository
- New `tests/v34_scorehub.test.js` (hand-computed MHI-18, PDQ, MSSS and SSS cases; SDMT reliable change).
- `LICENSES-INSTRUMENTS.md` and README updated for the new scales.

## v33 (2026-11-08): copyright clean-up and new tools

### AutoEDSSguide
- **Clinical mode rebuilt as the sEDSS** (streamlined EDSS; Baldassari LE et al. Mult Scler 2018;24(10):1347-55, Supplementary Appendix 1): each FS is the highest subscore, no Visual or Bowel/Bladder conversion, no separate ambulation score, Kurtzke step rules, and ambulation from the patient-reported walking time and pace. Same scoring as the paper; the question wording and order are MSpectrum's own.
- **Quick Check rebuilt from published instruments only**: the 3-question SRDSS decision tree (Kaufmann M et al. Mult Scler Relat Disord 2020;42:102148, CC BY-NC-ND 4.0) gives an EDSS range (3.5 or lower, 4.0-6.5, 7.0 or higher), shown with the PDDS step (NARCOMS). MSpectrum's own early-exit rules and invented questions were removed.
- **Visual FS fix**: the one-grade bump now follows Kurtzke 1983 exactly: it needs the ACUITY of the better (less affected) eye to be 20/60 or worse. Field or scotoma findings in the better eye no longer trigger it. Grade 6 label corrected. Engine version is now v3.3 (JS and Python identical on 2000 random cases).
- Checker messages cite "the published scoring conventions (Kappos 2011)"; the Pyramidal examples were rewritten as typical patient reports; the Fouad 2023 citation was corrected; Şen 2018 and Piri Çınar 2018 were added to the references.
- Non-affiliation notice now names Neurostatus-UHB AG, NMSS, WPS, PAR and Pearson, and states that users are responsible for licences and rater certification; the sheet adds that clinical trials need their own Neurostatus licence.

### MS Score Hub
- **PROMIS**: T-score and SE tables removed (HealthMeasures claims copyright in them). PROMIS-29, PROMIS Cognitive Function 4a and the converter now give raw sums only. The PROMIS lookup CSV download was removed.
- **Written SDMT norms** now use the regression equations of Fellows RP, Schmitter-Edgecombe M (Arch Clin Neuropsychol 2020;35(1):105-15; 536 healthy US adults, ages 18-91), checked against the authors' calculator. The Centofanti 1975 table was removed.
- Marrie 2021 CVLT-II / BVMT-R norms are given only for ages 18-65, the range of that sample.
- **FES-I**: official 16 items, order and instructions. **SymptoMScreen**: official domain names, instruction and anchor labels.
- PDDS shows the NARCOMS credit line. Non-affiliation lines added for WPS (SDMT), PAR (BVMT-R), Pearson (CVLT-II) and NMSS (MFIS, MSFC, MSQLI).
- **New tools**: MSQLI Pain Effects Scale, Bladder Control Scale, Bowel Control Scale and Impact of Visual Impairment Scale (NMSS MSQLI manual, 1997), Timed Up and Go (with MS reference values from Kalron 2017 and Nilsagård 2007) and 2-Minute Walk Test (Scalzitti 2018).
- ARMSS citation corrected to Mult Scler 2017;23(14) and its source files and licence named.

### MS Criteria Checker
- **κ-FLC index helper** under the CSF item: (CSF/serum κ-FLC) / (CSF/serum albumin), compared with an editable cut-off (default 6.1; Hegen H et al. Mult Scler 2023;29:169-81), with the Reiber hyperbolic limit and intrathecal fraction (Clin Chim Acta 2019;497:153-62). It informs only and does not tick the criterion.

### Repository
- New `LICENSES-INSTRUMENTS.md`: one row per instrument with owner, status, how MSpectrum uses it and the notice shown.
- No links to external tools inside MSpectrum.
- Tests: new `v33_scorehub.test.js`; Visual FS, PROMIS raw-only, Fellows norms and dynamic panel checks updated. Python test for bilateral field defects corrected to the Kurtzke rule.

## v32 (2026-11-06)

- Removed the "Scoring profile" option added in v31. The 50 m rule with one aid follows the Neurostatus manual ("more than 50 m"), as before v31.

## v31 (2026-11-06): new features

- **Copy EMR note** (Final sheet toolbar): one click copies a paste-ready EDSS summary (EDSS, 7 FS, ambulation, P/T exclusions, severity, change vs baseline, engine version).
- **ARMSS and MSSS in the EDSS result**: new optional "Year of first MS symptoms" field; ARMSS needs year of birth. Shown under the Final sheet toolbar and added to exports.
- **Visual acuity labels** show the 6 m and decimal equivalents (for example 20/40 (6/12 · 0.5)). Stored values are unchanged.
- **Self-hosted OCR libraries** (`vendor/ocr/`): pdf.js, tesseract.js (core + English data), onnxruntime-web and OpenCV.js load from MSpectrum itself first, so the scanner works offline and behind hospital firewalls; CDNs are only a fallback. Also fixes the v28 OpenCV pin (docs.opencv.org has no 4.10.0 build): the self-hosted file is the validated 4.x build (4.13.0).
- **Batch CSV scorer** (Final sheet toolbar): score many patients from a CSV on this device, with consistency flags, ARMSS/MSSS and change vs baseline; template download included.
- **REDCap dictionary with choices**: item fields are dropdowns with the form's own coding (BMRC 0-5 for strength); every cell is CSV-quoted (labels with commas no longer break the file).
- **Change vs baseline (CDP/PIRA screen)**: optional "Baseline / previous EDSS" and "Relapse in the last 90 days". Flags when the worsening threshold is met (+1.5 from 0.0, +1.0 from 1.0-5.5, +0.5 from 6.0) as possible RAW or possible PIRA; one visit cannot confirm progression.

## v30 (2026-11-06): Neurostatus naming

- "Neurostatus" is no longer used as a name for MSpectrum's own output, layout or exam: wording now says "standardized EDSS exam", "EDSS sheet" and "classic FS layout used on research and clinical-trial EDSS forms". Removed from page keywords and internal comments that described the sheet as a copy.
- Kept on purpose: citations of Kappos 2011, the phrase "published Neurostatus conventions" (what the scoring follows), rule citations in messages and code, and the trademark and non-affiliation notices.

## v29 (2026-11-06): bug fixes, privacy and engine parity

### Fixes
- CSV and REDCap export now score with the same P/T exclusions as the screen, so the exported EDSS matches. New columns at the end: `study_centre`, `p_gait_spasticity`, `m_fatigue_excluded`, `excluded_pt_flags`. Bowel/Bladder raw range in the dictionary corrected to 0-6.
- Gait spasticity entered in the guided form (`p_gait_spast`) now reaches the Pyramidal FS (the engine only read the scanner's R/L fields).
- Consistency rule 7 (position sense with ataxia) counted normal limbs; it now counts position sense grade 2 or worse.
- Clinical EDSS mode: systems skipped with "Get EDSS now" show N/C instead of 0 (screen and saved image).
- Quick Check: "Continue anyway" now works and keeps the early-exit banner closed until the check restarts.
- Final sheet: the bilateral rebound test now appears (worst of the four values).
- Sheet scanner: walking 500 m or more with the Assistance box empty now raises a review flag (AS 0 or AS 1).
- Train mode: 20 cases, as the interface says (added "Walks 200 to 299 m").
- Year-of-birth limit follows the current year; duplicate CSS rule merged; unused legacy OCR zone table removed.

### Privacy
- The embedded OCR model no longer contains local file paths (PyTorch stack traces with the author's user name and folder names were stripped from the ONNX metadata). Model output is identical (max difference 0.0).

### Python engine
- `edss_calc.py` re-synchronised with the JS engine (plegia rule, reflexes/Babinski/spasticity/gait spasticity, sensory rules, fatigue exclusion, ambulation score, cerebellar X). New `tests/parity_check.py`: 5,000 random cases identical between JS and Python. One old Python test expectation corrected (hip/knee flexors 2/5 = marked paraparesis, FS 4, not paraplegia).

## v28 (2026-11-06): IP, security and wording hardening

No change to any EDSS, FS or outcome-measure scoring result, except the BVMT-R Delayed Recall norm (now Parmenter 2010) and the BVMT-R Learning Index (now shown raw). The full regression suite passes (96 EDSS cases, Score Hub, converter, PROMIS tables, norms, McDonald).

### Security
- pdf.js: `getDocument` now runs with `isEvalSupported: false` (CVE-2024-4367 mitigation).
- jsPDF 2.5.1 -> 4.2.1 and html2pdf.js 0.10.1 -> 0.14.0 (vendored; CVE-2025-29907 and later jsPDF advisories).
- OpenCV.js pinned to 4.10.0, with the 4.x build as a fallback.
- Added `sbom.cdx.json` (CycloneDX 1.5 software bill of materials).

### EDSS sheet and Neurostatus
- Printed sheet renamed "EDSS Examination Record"; same fields and order; MSpectrum navy design (light section bars with a navy edge) instead of the green Neurostatus-style bars.
- Removed the reproduced Neurostatus copyright line and title text from the sheet footer; notes rewritten in MSpectrum's own words.
- Definition texts that matched the Neurostatus booklet word for word were rewritten in MSpectrum's own words. Wording that comes from Kurtzke 1983 (public domain) is kept.
- Non-affiliation and trademark notice for Neurostatus-UHB AG added to the sheet, every page footer and the README.

### MS Score Hub
- FSS, MSQOL-54, ABC, MSWS-12, MSIS-29, PROMIS-29 and PROMIS Cognitive Function 4a are now number-entry with short topic labels; their item wording is no longer in the code.
- Removed the downloadable PROMIS raw-to-T lookup table. PROMIS T-scores are still computed, with source and trademark notes.
- BVMT-R manual (PAR) sub-score tables removed. Delayed Recall T now uses Parmenter 2010 (MACFIMS Table 1 and Table 4).
- SDMT: Strober 2020 described correctly (675 healthy US adults, stratified norms); reliable change of 7 to 10 points at 6 months and 8 to 12 at 1 year added (Strober 2022).
- Norms caveat (Marrie 2021) added to SDMT, CVLT-II, BVMT-R and BICAMS.
- Attribution lines for PHQ-9, GAD-7, MFIS, PDDS, SymptoMScreen and FES-I.
- Check my MS guided flow now uses only instruments whose wording may be shown: EDSS and age, PDDS, FES-I, MFIS, SymptoMScreen, PHQ-9, GAD-7 and a 0-10 pain rating.

### Ownership, affiliation and notices
- Single author (Anas Z. Nourelden) in LICENSE, README, CITATION.cff, page metadata, footer and citation text.
- Removed VA affiliation lines from the footer and CITATION.cff (MSpectrum was not developed with VA resources).
- Global notice on every page: research and education tool, not FDA reviewed, provided as is, on-device privacy, views are the authors' own, instrument copyrights belong to their owners.

### Tests
- Full test suite added to `tests/` (`node tests/run.js`). SDMT test updated for education in years; Benedict tests replaced with Parmenter Delayed Recall tests.

The previous version is tagged `v27-pre-ip`.
