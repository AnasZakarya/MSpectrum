# Changelog

## v36.3 (2026-11-10): EDSS record details and second wording pass

- **EDSS record:** the Cerebellar FS shows the X marker ("1 X") in the FS bars, the findings card, the transcription list and the summary line. Findings marked P / T (not due to MS) show "(not due to MS; not scored)" on page 1 and keep the P / T suffix on page 2. A "Severity and change" line (ARMSS, MSSS, change vs baseline, with sources) is printed when those values exist; it is left out of the Sheet Scanner export, which has no such inputs.
- **Wording, second pass:** about 25 short phrases close to a proprietary scoring booklet were rewritten in MSpectrum's own words with the same meaning (cerebellar FS grades 2 to 4 now use Kurtzke 1983 wording; mentation, bladder, swallowing, speech, facial palsy, nystagmus, facial sensation, sensory grades, position sense, Romberg and truncal ataxia labels).
- The legacy paper-form output code was removed from the public file (kept locally by the author, not deployed).
- **Sources:** Kurtzke 2015 ("On the origin of EDSS" and "Further to the origin of EDSS") added. The About and README note now says plainly that Kurtzke 1983 defines the scale and that the later standardized trial rules (Visual and Bowel/Bladder conversion, disc pallor as grade 1, walking-distance cut-offs) are not part of his scale, per Kurtzke 2015, and that the authors of those rules claim no rights on the EDSS or its FS, only on their training and documentation tools (Kappos et al. 2015). Scanner button renamed "EDSS record". The Sheet Scanner check screen now states that it follows the scanned sheet only for comparison, that only the numbers are used, and that downloads are the MSpectrum record and summary table ("4 steps" heading fixed).
- edss_calc.py docstring now says "scoring rules v3.4", matching the JS engine. Scores unchanged (2000/2000 parity).

## v36.2 (2026-11-10): EDSS record, own wording and sources, saving results

### EDSS record (Final Sheet)
- The Final Sheet no longer copies the paper-form layout. It is now an **MSpectrum EDSS record**: page 1 summary (EDSS step and how it was reached, walking first, the 7 Functional Systems in Kurtzke 1983 order with bars, abnormal findings only, signature); page 2 transcription list (every value box of the sheet, numbered, in the sequence of common paper forms, with MSpectrum's own labels and no form boxes or header). Print, PDF and email use it; the Sheet Scanner export uses the same record. The separate export-only interpretation page is folded into page 1.
- Sheet header fields "Centre Nr/Country" and "Name of EDSS rater" renamed "Site" and "Rater".

### Wording and sources
- About 20 definition labels that matched a proprietary scoring booklet were rewritten in MSpectrum's own words with the same meaning (mentation, hearing, facial weakness, position sense, spasticity, gait spasticity, limb ataxia, nystagmus, ataxic gait, drift / heel-toe walking options, single-leg raise, other cerebellar signs).
- EDSS sources are now one combined list that complement each other: Kurtzke 1983 and 1989; Kappos et al. 2015; Sen 2018; Piri Çınar 2018; Fouad et al. 2023; the open-source edss library (MIT). Where they differ, MSpectrum follows Kurtzke 1983. The citation of an unpublished definitions booklet (v04/10.2) was removed.
- The rating-system name now appears only in the trademark / non-affiliation sentence in About, in README / LICENSES, and in the titles of cited papers. Code comments cite the published sources instead. Engine label: "MSpectrum scoring rules v3.4 (Kurtzke EDSS; published standardized rules)"; scores are unchanged (2000/2000 parity).
- New tests: tests/edss_record.test.js.

### Saving results
- "Save patient summary" (image or PDF) added to the four Score Hub tools that lacked it: MS severity (ARMSS/MSSS), ARR, CDP and NEDA, with a CSV button like the other tools. The PIRA button now has the same label.
- The "summary saved" / "report saved" message no longer appears when the summary preview opens (nothing is saved at that point). A message now appears only after a file is actually produced: "Image saved: <file>.png" or "Downloaded <file>.csv". "Save PDF / print" opens the browser's print dialog, so no message is shown there.

## v36.1 (2026-11-09): one disclaimer box and a short footer

- **"Use and limitations" box** (was "Not a diagnosis") only on the main pages: the AutoEDSSguide mode picker, the Score Hub home, the Check my MS start page and the Criteria Checker. Same layout everywhere: one sentence written for that page, one point for that page (Training; Questionnaires and norms; If you feel unsafe, with the 988 line), then the same 3 shared points in the same order (Not a medical device, Privacy, Independence), and a last line with copyright, About, Full disclaimer, Cite and Contact.
- Removed: the box on the home page, the box inside each AutoEDSSguide mode and Score Hub tool, the Sheet Scanner yellow bar, the Neurostatus line in the footer, and the repeated "the diagnosis stays with the treating neurologist" in the Criteria Checker header. Neurostatus is named once in the AutoEDSSguide box; the full trademark notice stays in About, which now also names the instrument owners.
- **Sub-pages** (each mode and tool) end with a 2-line footer: "Supports, but does not replace, clinical judgment. Not an official product of, or endorsed by, any university, hospital or government agency." and copyright with the links. The Disclaimer link opens "Disclaimer & terms of use" in About from any page.
- Less empty space below the box (Score Hub bottom padding 80 to 24 px on desktop; mobile keeps room for the floating buttons).
- One spelling: "judgment". Mobile: the Clinical EDSS header no longer scrolls sideways at 390 px.
- Dead CSS removed (disclaimer bar, warning card, old box footer). New test: tests/disclaimer.test.js.
- Print and PDF disclaimers and tool-specific notes (Quick Check, sEDSS, PHQ-9/GAD-7, PIRA) are unchanged.

### Check my MS: 13 questionnaires
- Added to the guided flow, all with item wording that may be shown: PDQ (everyday thinking and memory), BLCS (bladder), BWCS (bowel), SCI (sleep) and RAND-36 (general health and quality of life). The report shows each with its range; only SCI has a published cut-off (16 or less, probable insomnia disorder, Espie 2014), so only SCI can raise a flag.
- Removed leftover checklist entries for steps no longer in the flow (MSWS-12, PROMIS Cognitive 4a, MSIS-29, MSQOL-54).
- New test: tests/checkmyms.test.js.

### Gemini round 7 (checked against the code; 8 of 10 points fixed)
- PIRA chart and PIRA / RAW badges now follow dark mode (theme colours instead of fixed dark colours).
- The norms caveat "(Marrie 2021)" now gives the full citation: Marrie RA et al. Front Neurol 2021;11:621010 (checked in PubMed). The Marrie norms themselves stay removed.
- Kappos 2020 added to the AutoEDSSguide reference list (it is cited on the final sheet).
- Score Hub: PROMIS-29 card no longer says "with severity bands"; MSFC group subtitle says "NMSS Task Force reference".
- README: Marrie removed from the norms line; Train mode added (six modes); privacy line mentions "Save to browser"; Check my MS lists its 13 questionnaires.
- Not adopted: the ".viz-t endpoint labels" point (no such class or function exists in the code); the "Assessment 2021" journal for Marrie (that text is not in the files; the old citation was already Front Neurol).

## v36 (2026-11-09): RAND-36, SCI, P-MSSS, PIRA/RAW module, harmonized worsening thresholds, Gemini review fixes

### MS Score Hub
- **RAND-36** (RAND 36-Item Health Survey 1.0): items from Hays 1993 (Appendix), scored with the RAND instructions (Table 1 recoding, Table 2 scales; blank items left out of the mean). 8 scales, 0-100, with the MOS reference means (Table 3) for context; item 2 (health change) shown on its own. RAND credit line and "electronic format, wording unchanged" note. Added to the converter.
- **Sleep Condition Indicator (SCI)**: 8 items and answer options from Espie 2014 (Appendix), total 0-32, 0-10 format, items at threshold (scores 0-2) and the 16-or-less probable insomnia screen. © Sleepio Limited, CC BY-NC 4.0 notice. Added to the converter.
- **P-MSSS** in the PDDS tool: optional "years since first MS symptoms" gives the disease-duration-adjusted PDDS rank from Kister 2013 (Figure 2, 0-45 years). Values transcribed and checked twice against the figure; the table itself is not displayed. Converter entry added.
- **SymptoMScreen** now matches Figure 1 of Green 2016 exactly: domain names (Walking/Mobility, Bodily Pain, Sensory symptoms), the short descriptor under each domain, the full answer options (for example "moderate limitation/ I reduced my daily activities") and the instruction. Licence stated as CC BY 4.0.
- **Parmenter 2010 range note**: its controls were aged 20-60 with 12-18 years of education; outside that range the BVMT-R/CVLT-II Parmenter z/T is flagged as an extrapolation (tool pages and converter).
- **CDP tool**: thresholds follow the harmonized definition (Müller 2023): +1.5 from 0, +1.0 from 1.0-5.0, +0.5 from 5.5 or more; 48-week confirmation option; relapse window 30 days before to 90 days after a relapse onset.

### AutoEDSSguide
- Change vs baseline uses the same Müller 2023 thresholds (baseline 5.5 now needs +0.5) and says the confirming visit should be at least 3 months later (preferably 6 or 12).

### New tool
- **PIRA / RAW across visits** (Disease activity & progression): enter dated visits (EDSS, optional T25FW, 9-HPT, SDMT) and relapse onsets; each confirmed worsening is classed as PIRA or RAW with the harmonized definition (Müller 2023): roving reference, EDSS thresholds by reference score, T25FW/9-HPT > 20%, SDMT ≥ 4 points or > 10%, confirmation ≥ 3 months, relapse window 30 days before to 90 days after. Chart with the roving reference, event table, paste from a spreadsheet, CSV. Built from the approved mockup.

### Fixes from the Gemini round-4 review (each checked against the code and the sources)
- **McDonald**: an optic nerve lesion on orbital MRI was wiped when "Visual tests" was not ticked; now MRI, OCT and VEP are cleared only when their own test is unavailable. Progressive course without MRI now says "brain MRI required". The single-region progressive branch now shows the age ≥ 50 / vascular-risk caution (as the multi-region branch did). The unused "CNS sites on examination" field was removed from the progressive inputs. Companion references corrected to the exact PubMed titles and authors (Saidha 2025, Barkhof 2025); the unverifiable "Fluid biomarkers 2025" item was replaced by Hegen 2023 and Reiber 2019. Toast now fires on "Save as PDF".
- **sEDSS**: fine finger movements become required when strength is normal ("required if UE strength 5/5", Appendix 1). Correlation text corrected to Spearman rho 0.99 (pilot, n=102) and 0.93 (CombiRx, n=968).
- **Converter**: answers outside each tool's range are rejected (for example 99 on the PHQ-9), blank items are no longer counted as 0, ABC needs 12 answers; MSQOL-54 now returns all 12 subscales and both composites to one decimal; the written SDMT example has 4 values.
- **Text**: the "Who can use each tool" card no longer says full item text is shown for copyrighted questionnaires; the BICAMS sources name Strober 2020, Fellows 2020 and Parmenter 2010 (not Marrie 2021); index references name Parmenter 2010 as the primary BVMT-R/CVLT-II norm; Visual grade 3 label says "or worse-eye VA".
- **Code**: dead `promisBand` (old PROMIS raw cut-offs) and an unused sensory variable removed; exports stamp `MSpectrum-v36`; `edss_calc.py` header and Fouad citation updated; README now says CDN copies are only a fallback.

### Citation and claim audit (every citation checked in PubMed; every number checked against its source)
- **Removed** statements with no source: LCVA "typical ranges" (35-50 / 20-40 letters) and the ≥ 5-letter asymmetry flag (the inter-eye difference is now shown without a judgement); MSWS-12 "typical cohort range"; MSIS-29 "> 50 = substantial impact"; MSQOL-54 "< 50 = below average"; MFIS "cut-offs vary 34-43"; ARR activity bands and untreated-rate range; 6MWT % predicted grades; 9-HPT healthy range; PDDS "≥ 1 step is meaningful" (not in Learmonth 2013).
- **Corrected sources**: LCVA 7-letter change now cites Balcer 2017 (Mult Scler 23(5):734-47; the 2007 trials used 10 letters); PHQ-9 cut-point 11 in MS now cites Patten 2015 (was a review that does not state it); GAD-7 4-point change now cites Toussaint 2020 (the earlier "Rubin 2016" could not be found in PubMed); ABC bands now cite Myers 1998; RIS 5-year risk cites Okuda 2014 (34%) and 10-year risk Lebrun-Frénay 2020 (51%); Flachenecker 2002 now has volume and pages.
- **Repository**: the unused Wayne State logo file is removed (no institutional logo on the site).
- **Added published values**: 6MWT and 2MWT meaningful change in MS (Baert 2014: about 22 m and 10 m from the patient's view).

### Organization
- Score Hub groups: new **Vision** group (LCVA, IVIS; LCVA was under walking); "Walking, balance & motor function" (MSWS-12, ABC and FES-I named as self-report); PROMIS pain intensity moved to Symptom burden; Disease activity subtitle now names PIRA / RAW. MSFC subtitle on patient summaries now says "Walking, hand and cognitive function".
- README instrument table now lists every Score Hub tool with its source.

### Gemini round-5 fixes (each checked against the code)
- **Ambulation**: bilateral aid with no distance now defaults to AS 7 (EDSS 6.0), the same conservative choice as the unilateral default (was AS 8, EDSS 6.5), in JS and Python; a new check asks for the distance walked with the aid.
- **Quick Check**: the SRDSS question wording is unchanged (CC BY-NC-ND); the "Yes" answer now says "For example a cane or a rollator".
- **Check my MS**: the EDSS step now says to skip it when only a Quick Check range is known (severity scores need an exact EDSS); it no longer suggests picking a value inside the range.
- **Score Hub**: quick-fill buttons hidden in the patient flow for PROMIS Cognitive 4a, ABC and FES-I; scale answer labels enlarged from 7.5 px to 9.5 px; the 0-10 MSQLI items no longer repeat the number under each button; 6MWT explains in the result box why no % predicted is shown outside ages 40-80; image-export message no longer says internet is needed (the renderer is bundled).
- **Mobile result box**: on screens under 1000 px the sticky result box has a "Minimize result" button that folds it to the main score line, so the questions and sources can be read; "Show full result" opens it again. Hidden on desktop and in the patient flow.
- MFIS result text now names Flachenecker 2002 for the 38 cut-off.

### Institutional neutrality and home page
- The Wayne State University shield and name block were removed from the home footer; the university is named only as the author's affiliation. The page metadata (JSON-LD) now names the author, not the university, as publisher; "Developed at Wayne State University" and the university as citation publisher were removed (README, Cite us); the no-warranty clause no longer speaks for the university.
- New sentence on every page and in the README: "MSpectrum is not an official product of, and is not endorsed by, any university, hospital or government agency."
- Home footer: disclaimer in two balanced lines, then the copyright; the Neurostatus trademark line moved to the AutoEDSSguide footer and to About > Disclaimer ("Independence and trademarks").
- Home content: AutoEDSSguide "6 modes" (Train mode counted); unsourced "7-10 min" for sEDSS removed; feature cards list the current tools (PDDS no longer under quality of life); "full question text" now says copyrighted questionnaires take answers from the official form; "Validated" card renamed "Published rules, norms & checks"; plain-language card says peer comparison applies where norms exist; About lists the new Vision group; MRI consensus reference has authors and pages; RIS reference adds Okuda 2014.
- "Not a diagnosis" boxes (AutoEDSSguide, Score Hub, Criteria Checker): the long legal paragraph is now four short points (Not a medical device; Training and licences; Privacy; Independence); duplicated sentences removed; the AutoEDSSguide footer now shows only the copyright. Home page: less empty space under About and the footer.

### Gemini round-6 review (each point checked against the code and, for PIRA, against the Müller 2023 PDF)
- **PIRA / RAW**: (1) the roving reference skipped the visit that confirmed an improvement, so a second step down (for example 3.0 -> 2.5 -> 1.5) was missed and a later PIRA could be missed; the reference now resets at every confirmed lower score ("confirmed at the following visit", Müller 2023). (2) A confirmation visit inside a relapse window no longer confirms the event or raises the reference; the next visit at least 3 months later and outside every relapse window is used ("should not happen 30 days before and 90 days after the onset of a relapse"). The >20% threshold for T25FW and 9-HPT was kept: Müller 2023 says ">20%" (Gemini's ">=20%" was not adopted). (3) "Researcher: CSV" now exports one row per visit with each event, reference, change, confirming visit and the relapse dates (it exported almost nothing). (4) Paste accepts MM/DD/YYYY and reports skipped lines.
- **Sheet Scanner**: the seven FS score boxes called a missing function (`updateConvertedScores`) or were overwritten on the next keystroke. They are now read-only and computed from the sheet items, the single source used for the synopsis, table and EDSS. The cerebral "FS = 0" hint no longer states a wrong rule ("2 items needed").
- **Converter**: MSQOL-54 answers are checked item by item (item 53 = 99 was scored as 990); SDMT, BVMT-R, CVLT-II, T25FW, 9-HPT, ARMSS and MSSS fields are range-checked (EDSS in 0.5 steps).
- **Text**: PASAT "practice effect" line removed (it cited Rao 1991, which does not report it); README says CSV export (Score Hub has no JSON export); OCR debug text names the current button; AutoEDSSguide privacy text now mentions the optional "Save to browser".
- **Code clean-up**: unused functions removed (refreshChipDetails, qcCheckEarlyExit, scUpdateEdssLive, snapZones and its 4 helpers, normBlock, _Tsc, exportJSON, _sdmtBulkZ, pcDownloadPDF, lpToggle), plus unused variables, a dead JSON-import handler and a dead synopsis builder. 6MWT has its Clear button. ARMSS colour readable in dark mode.
- **Not adopted (Gemini wrong after checking)**: WSU shield "still on the landing page" (no such element); "no Content-Security-Policy" (all three pages have one); "AS 16 = death" (EDSS 10 is not an ambulation grade); Fellows written-SDMT equation and sign (Gemini quoted an equation that is not in the code); McDonald copy summary "missing what would complete the criteria" (already included); adding an id to the scanner synopsis grid (would have replaced the working grid); several table rows describing fields that do not exist (binocular LCLA, 6MWT minute splits, TUG and ABC cut-offs from Sebastião or Cattaneo); Müller PMID 37782491 (correct PMID 37782515).
- Tests: v36 suite now 37 checks (PIRA stepwise reference, exact 20%, relapse-window confirmation, converter ranges).

### Final source pass and Nour's decisions (2026-11-09)
- **Marrie 2021 (Canadian) norms removed** from BVMT-R, CVLT-II, BICAMS and the converter, with the race fields; Parmenter 2010 (US) is the only BVMT-R/CVLT-II norm. Marrie 2021 stays cited only for its finding that published norms can misclassify impairment when applied to a different population.
- **Self-made bands removed**: MSWS-12, MSIS-29, MSQOL-54, SymptoMScreen total and MFIS cognitive items had site-made severity bands in the tool pages and the Check my MS report; they are now shown without a severity colour, with a sourced meaningful-change value where one exists (MSWS-12 Baert 2014, MSIS-29 physical Costelloe 2007). FSS "5 or more = severe" removed (only the cut-off of 4 is sourced). MFIS 38 is described as "clinically significant fatigue impact" (Flachenecker 2002), not "severe". FES-I and pain bands name their sources; a pain score of 0 now reads "No pain".
- **Unsourced numbers removed** in AutoEDSSguide: "1 city block = 200 m" and "observe 130 m with assistance" (replaced by the Neurostatus distance thresholds).
- **References list completed** (Score Hub): Modified Ashworth (Bohannon 1987), PIRA / RAW (Müller 2023; Kappos 2020), MFIS cut-off (Flachenecker 2002), PHQ-9 cut-point in MS (Patten 2015), GAD-7 change (Toussaint 2020), 2MWT change (Baert 2014).
- **Paste answers**: FSS, MSWS-12, MSIS-29, FSMC, ABC, MSQOL-54, PROMIS-29 and PROMIS Cognitive 4a can be filled from one pasted line, with the converter's range checks (hidden in the patient pathway).

### Checked against the original papers (Nour's PDFs)
- FES-I cut-points 16-19 / 20-27 / 28-64 match Delbaere 2010 exactly; the text now says they come from adults aged 70-90 and that the authors call them preliminary.
- FSMC cut-offs match Penner 2009 Table 7 (total 43/53/63, cognitive 22/28/34, motor 22/27/32); the motor and cognitive subscales are now graded too (only the total was).
- ABC 67% matches Lajoie 2004 (sensitivity 84.4%, specificity 87.5%, older adults); the unsourced "MS-specific cut-offs vary" sentence was replaced.

### Result charts (neutral colours; a line only where a published cut-off exists)
- **BICAMS**: the three z-scores on one axis with a dashed line at z = -1.5 (impaired range shaded). **MSFC**: the three component z-scores on one axis (no cut-off; 0 = Task Force MS reference mean).
- **SDMT**: the change since the last visit, drawn against the Strober 2022 reliable-change bands (70%, 80%, 90%).
- **ARMSS / MSSS**: position on the 0-10 scale (5 = middle of people with MS of the same age or disease duration). The ARMSS number is no longer coloured green/amber/red (those bands had no source).
- **RAND-36**: the 8 scales as bars with the MOS reference mean (RAND Table 3) as a tick. **MSQOL-54**: the subscale profile as bars (no cut-offs).

### Site
- Home page: 43 tools; About and References list RAND-36, SCI, P-MSSS and Müller 2023. Converter: 34 instruments in eight groups.
- New `tests/v36_scorehub.test.js` (29 hand-computed checks).

## v35 (2026-11-08): new tools wired into every part of the site

- **Score & norm converter**: the eight MSQLI scales were added (new group "MSQLI scales"; 31 instruments in six groups). Same rules as the tool pages; out-of-range answers are flagged; MHI-18 accepts NA for skipped items.
- **New tools in the shared features**: MSQLI, TUG and 2MWT pages now have "Save patient summary" and "Researcher: CSV"; every tool has a subtitle on the patient summary; the Clinician summary now compiles every Score Hub tool (it listed only 21).
- The MSQLI social support survey is shown as **MOS-SSS** so it is not confused with the MS Severity Score (MSSS); its page explains the manual's name.
- **Home page**: Score Hub badge 30 → 40 tools, updated tool list and description; AutoEDSSguide card names the sEDSS and the SRDSS + PDDS Quick Check; About lists all 40 Score Hub tools by domain; References add MSQLI, TUG/2MWT, a pointer to the Score Hub list and the κ-FLC sources (Hegen 2023; Reiber 2019).
- No em dashes left in user-visible text (patient summary title, EDSS e-mail subject and body, two PDF messages).
- Page keywords updated (MSQLI, MHI-18, TUG, 2MWT, sEDSS, SRDSS, κ-FLC).

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
