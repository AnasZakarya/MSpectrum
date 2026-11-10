# MSpectrum

**MSpectrum** is a free, browser-based, privacy-first hub for the outcome measures used in multiple sclerosis. Everything is computed in your browser; nothing is uploaded, and nothing is saved unless you press "Save to browser" in AutoEDSSguide. It has four parts:

- **AutoEDSSguide** (`index.html`): the full EDSS exam, scored with Kurtzke's EDSS and the standardized scoring rules published in the literature (see Algorithm & scoring sources), plus the streamlined EDSS (sEDSS, Baldassari 2018) and a patient self-report EDSS range (SRDSS, Kaufmann 2020, with PDDS) fast modes, a print-ready EDSS record, and an OCR sheet scanner.
- **MS Score Hub** (`scores.html`): stateless calculators and full questionnaires for the cognition, fatigue, mood, walking, quality-of-life and disease-severity measures used alongside the EDSS, each with automatic published norms (z / T / percentile) and a plain-language interpretation.
- **Check my MS** (`scores.html#report`): a guided, patient-facing pathway that walks through 13 self-report questionnaires (EDSS and age, PDDS, FES-I, MFIS, PDQ, SymptoMScreen, BLCS, BWCS, SCI, PHQ-9, GAD-7, pain, RAND-36) and produces one plain-language summary of how MS is affecting the person, for understanding and discussion rather than diagnosis.
- **MS Criteria Checker** (`mcdonald.html`): an adaptive wizard that applies the 2024 revisions of the McDonald criteria (Montalban et al., Lancet Neurol 2025) to reach an MS diagnosis across relapsing, progressive and RIS onset, covering the five DIS regions (incl. optic nerve), DIT, CSF (OCB / k-FLC) and susceptibility markers (CVS, PRL), with older-onset and mimic safeguards and a printable summary.

MSpectrum is not an official product of, and is not endorsed by, any university, hospital or government agency.

If you use a result from MSpectrum in research or publication, please cite the original source shown for each tool and cite MSpectrum as listed in CITATION.cff.

---

## Try it now

**[▶ Open MSpectrum](https://anaszakarya.github.io/MSpectrum/)**

No installation. No login. Works in any modern browser.

---

## AutoEDSSguide: six ways to use it

| Mode | For whom | What it is |
|------|----------|------------|
| **Roadmap** | Raters / research | Full standardized EDSS exam, guided step-by-step in exam order (history, then cranial nerves, then body). |
| **System view** | Raters | All 7 Functional Systems on one page, in the usual paper-form order. |
| **Clinical EDSS** | Neurologists | Fast adaptive follow-up scoring (streamlined sEDSS, Baldassari 2018). |
| **Quick Check** | People with MS | Four published self-report questions: SRDSS (Kaufmann 2020) gives an EDSS range; PDDS adds the disease step. |
| **Sheet Scanner** | Raters | Upload or photograph a completed EDSS scoring sheet (standard research layout); fields are OCR-extracted and scored. |
| **Train mode** | Raters in training | 20 reference cases (four are the published worked examples in Sen 2018): read the FS grades and Ambulation Score, pick the EDSS, and compare with the engine step and the rule behind it. A practice aid, not a certification. |

All modes compute through a **single shared engine**, so the header, roadmap, printed sheet, and scanner always produce identical EDSS values.

The Final Sheet (and the Sheet Scanner export) prints an **MSpectrum EDSS record**: page 1 is a summary (EDSS step and how it was reached, walking, the 7 Functional Systems in Kurtzke order, abnormal findings only, signature); page 2 is a transcription list with every recorded value in the sequence of common paper EDSS forms, so a rater can copy the numbers onto a paper record. MSpectrum does not reproduce any paper form layout.

---

## MS Score Hub: measures beyond EDSS

Stateless calculators and full questionnaires. Results show the raw score and, where an open published norm exists, an automatic standardized score (z / T / percentile) with a plain-language interpretation and the norm source cited; nothing is stored.

| Domain | Instruments | Standardized output (source) |
|--------|-------------|------------------------------|
| Disability & severity | EDSS, PDDS, **ARMSS / MSSS**, **P-MSSS** | severity vs peers by age / disease duration (Manouchehrinia 2017; Roxburgh 2005; Kister 2013 for PDDS) |
| Disease activity & worsening | ARR, CDP, **PIRA / RAW across visits**, NEDA-3/4 | harmonized PIRA definition: roving reference, confirmation ≥ 3 months, relapse windows (Müller 2023) |
| Cognition (BICAMS) | SDMT, CVLT-II, BVMT-R, **BICAMS** panel | auto z + impairment (z ≤ −1.5): oral SDMT US norms (Strober 2020) and reliable change between visits (Strober 2022); written SDMT regression norms (Fellows & Schmitter-Edgecombe 2020, ages 18-91); CVLT-II/BVMT-R US regression norms (Parmenter 2010; controls aged 20-60, flagged outside that range); BVMT-R Delayed-Recall T and CVLT-II LDFR T (Parmenter 2010) |
| Cognition (other) | PASAT-3, PROMIS Cognitive Function 4a, PDQ (MSQLI) | PASAT-3 z vs NMSS Task Force (Fischer 2001); PROMIS raw sum; PDQ scored as in the MSQLI manual |
| Walking, balance & motor | MSWS-12, T25FW, 9-HPT, 6MWT, **2MWT**, **TUG**, ABC, FES-I, **MSFC** | MSWS-12 0–100 transform; T25FW benchmarks (Goldman 2013); z & composite vs NMSS Task Force (Fischer 2001); 6MWT % predicted (Enright 1998); 6MWT/2MWT meaningful change (Baert 2014); TUG MS reference values (Kalron 2017; Nilsagård 2007); ABC bands (Myers 1998) and 67% (Lajoie 2004); FES-I cut-points (Delbaere 2010) |
| Spasticity | Modified Ashworth | grade per muscle group (Bohannon 1987) |
| Vision | LCVA (Sloan 2.5% and 1.25%), IVIS (MSQLI) | letters per eye; 7-letter meaningful change (Balcer 2017) |
| Fatigue | MFIS (≥38), FSS (≥4), FSMC | MFIS cut-off (Flachenecker 2002) and MID (Rooney 2019); FSMC grades (Penner 2009) |
| Mood | PHQ-9, GAD-7, MHI-18 (MSQLI) | validated severity bands (+ PHQ-9 item-9 safety prompt); MHI-18 per MSQLI manual |
| Symptom burden | SymptoMScreen, PROMIS pain intensity, Pain Effects, Bladder and Bowel Control, Sexual Satisfaction (MSQLI) | totals by domain; pain intensity bands (Serlin 1995) |
| Quality of life / impact | MSQOL-54, RAND-36, PROMIS-29 v2.1, PROMIS Cognitive Function 4a, MSIS-29 | MSQOL composites; PROMIS raw sums per domain (T-score tables not included); 0–100 transforms |
| MSQLI scales (NMSS 1997) | **Pain Effects Scale, Bladder Control Scale, Bowel Control Scale, Impact of Visual Impairment Scale, Sexual Satisfaction Scale, Perceived Deficits Questionnaire (PDQ-20 and PDQ-5), Mental Health Inventory (MHI-18), MOS Modified Social Support Survey (MOS-SSS)** | totals and subscales scored exactly as in the MSQLI manual (Ritvo et al. 1997) |
| Sleep | **Sleep Condition Indicator (SCI)** | total 0-32 and 0-10; 16 or less = probable insomnia disorder (Espie 2014; CC BY-NC 4.0) |

Extras: result charts (BICAMS and MSFC z-scores, SDMT reliable change, ARMSS/MSSS position, RAND-36 and MSQOL-54 profiles); paste-answers box on number-entry questionnaires; demographics entered once drive the cognitive z-scores; CVLT-II recognition sub-scores (SDFR, LDFR, d′, discriminability, Forced-Choice validity); a guided **Check my MS** patient pathway with a plain-language report; a **Clinician summary** that compiles all entered tools; out-of-range input flagging; unanswered-item highlighting; an **"ℹ How it works"** helper on every tool; **Export CSV** per tool. Self-report questionnaires can be filled by the patient; performance tests and composites are clinician-administered.

### Score & norm converter (bulk)

**AutoEDSSguide extras (v31):** copy a paste-ready EMR note; ARMSS/MSSS next to the EDSS; change vs a baseline EDSS (possible RAW / PIRA, needs a confirming visit); a batch CSV scorer for research cohorts; a REDCap data dictionary with coded choices; Snellen labels with 6 m and decimal equivalents; OCR libraries self-hosted for offline use.

A **Score & norm converter** turns a whole list of patients into finished scores at once: pick a questionnaire or test, paste one patient per line (values separated by comma, space or tab, with an optional leading ID), and get a downloadable results table. It covers **34 instruments** in eight groups: patient-reported questionnaires (PHQ-9, GAD-7, MFIS, FSS, MSWS-12, MSIS-29, MSQOL-54, SymptoMScreen, FSMC, PDDS, ABC, FES-I), the eight MSQLI scales (PES, BLCS, BWCS, IVIS, SSS, PDQ, MHI-18, MOS-SSS), RAND-36 and the Sleep Condition Indicator, P-MSSS from PDDS, norm-based cognitive tests that use age/sex/education (SDMT, BVMT-R, CVLT-II), cognitive/motor tests scored against a fixed reference (PASAT-3, T25FW, 9-HPT), PROMIS (raw sums per domain for PROMIS-29 and PROMIS Cognitive 4a), and disease severity (ARMSS, MSSS). This complements data platforms such as **REDCap**, giving the norm-based z/T scores those platforms store the answers for but do not compute. For a single patient with the full breakdown and interpretation, each tool's own page is used instead. Everything runs in the browser; nothing is uploaded.

> **Decision support, not a diagnosis.** MSpectrum computes outcome-measure scores and applies published diagnostic criteria, and explains what the results mean. It supports clinical judgment but does not itself diagnose; interpretation, diagnosis and treatment remain the decision of a qualified clinician. See the in-app **Disclaimer & terms of use** for the full medico-legal notice.

---

## Offline & privacy

Works fully offline once loaded (open `index.html` directly). No account, no tracking, nothing uploaded; nothing is saved unless you press "Save to browser" in AutoEDSSguide. Do not enter patient names or identifiers (PHI); use a non-identifying code.

Fonts, the PDF/export libraries and the OCR libraries are **self-hosted**, so a normal session makes no third-party requests. Public CDN copies are used only as a fallback if a self-hosted file fails to load; images are always processed in the browser. Saved data lives only in your browser; a **Clear saved data** button wipes it, which is useful on shared computers. For the deployment security model and a HIPAA-conscious usage guide, see [SECURITY.md](SECURITY.md) and [PRIVACY-and-HIPAA.md](PRIVACY-and-HIPAA.md).

---

## MS Criteria Checker: diagnosis by the 2024 McDonald criteria

An adaptive, single-page wizard (`mcdonald.html`) that implements the **2024 revisions of the McDonald criteria** (Montalban et al., Lancet Neurol 2025) and their companion consensus papers. It adapts to patient age and onset course (relapsing, primary-progressive, RIS), asks only about the investigations you have, and reports which diagnostic category the findings fulfil (criteria met, possible MS, RIS, criteria not met or incomplete), the criteria it rests on, safety cautions and recommended next steps, with a print / PDF summary. It applies the criteria; the diagnosis stays with the treating neurologist.

- **All 2024 pathways:** DIS across five regions (incl. optic nerve), the 4-region shortcut, DIT, CSF (OCB / k-FLC), and susceptibility markers (select-6 CVS, ≥ 1 PRL).
- **κ-FLC index helper:** enter CSF and serum κ-FLC and albumin to get the κ-FLC index ((CSF/serum κ-FLC) / (CSF/serum albumin)); it is compared with an editable cut-off (default 6.1; Hegen 2023), with the Reiber 2019 hyperbolic limit and intrathecal fraction for context. It informs only; the clinician ticks the box.
- **Safeguards:** older-onset (≥ 50) vascular caution, pediatric ADEM / MOG-IgG guidance, atypical red-flag prompts for NMOSD / MOGAD, and a "no better explanation" acknowledgment that is part of the criteria: until it is confirmed the category stays provisional.
- Independent educational aid; not affiliated with any commercial application.

---

## Cite us

If you used MSpectrum in research, please cite it:

> Nourelden A. *MSpectrum: a free, browser-based toolkit for multiple sclerosis outcome measures and diagnosis (AutoEDSSguide, MS Score Hub and MS Criteria Checker).* 2026. Available from: https://github.com/AnasZakarya/MSpectrum

(GitHub also offers ready APA/BibTeX via the "Cite this repository" button, generated from `CITATION.cff`.)

---

## Algorithm & scoring sources

- Kurtzke JF. *Rating neurologic impairment in multiple sclerosis: an expanded disability status scale (EDSS).* Neurology 1983;33:1444-52. Kurtzke JF. *The Disability Status Scale for multiple sclerosis: apologia pro DSS sua.* Neurology 1989;39:291-302.
- Kurtzke JF. *On the origin of EDSS.* Mult Scler Relat Disord 2015;4(2):95-103. DOI: [10.1016/j.msard.2015.02.003](https://doi.org/10.1016/j.msard.2015.02.003). Kurtzke JF. *Further to the origin of EDSS.* Mult Scler Relat Disord 2015;4(3):186. DOI: [10.1016/j.msard.2015.04.007](https://doi.org/10.1016/j.msard.2015.04.007).
- Kappos L, D'Souza M, Lechner-Scott J, Lienert C. *On the origin of Neurostatus.* Mult Scler Relat Disord 2015;4(3):182-5. DOI: [10.1016/j.msard.2015.04.001](https://doi.org/10.1016/j.msard.2015.04.001).
- Fouad AM, Abdel Naseer M, Farghaly M, Hegazy MI. *New algorithmic approach for easier and faster extended disability status scale calculation.* Mult Scler J Exp Transl Clin 2023;9(1):20552173231155055. DOI: [10.1177/20552173231155055](https://doi.org/10.1177/20552173231155055).
- Sen S. *Neurostatus and EDSS calculation with cases.* Arch Neuropsychiatry 2018;55(Suppl 1):S80-S83. DOI: [10.29399/npa.23412](https://doi.org/10.29399/npa.23412).
- Piri Çınar B, Güven Yorgun Y. *What we learned from the history of multiple sclerosis measurement: Expanded Disability Status Scale.* Arch Neuropsychiatry 2018;55(Suppl 1):S69-S75. DOI: [10.29399/npa.23343](https://doi.org/10.29399/npa.23343).
- Open-source implementation: [edss](https://github.com/adobrasinovic/edss) (Dobrašinović A, 2020; MIT licence).
- Kurtzke 1983 defines the Functional Systems and the EDSS steps (a US Government work in the public domain; Kurtzke 2015). The later papers describe standardized scoring rules added for clinical trials (Visual and Bowel/Bladder conversion, optic disc pallor as Visual grade 1, fatigue in the Cerebral FS, walking-distance cut-offs); Kurtzke (2015) stated that these are not part of his scale, and their authors state that they claim no rights on the EDSS or its Functional Systems, only on their training and documentation tools (Kappos et al. 2015). MSpectrum applies them because current trials and raters use them, and follows Kurtzke 1983 where the two give different steps (for example five FS grade 2 = EDSS 3.5).
- Kaufmann M et al. *Development and validation of the self-reported disability status scale (SRDSS) to estimate EDSS-categories.* Mult Scler Relat Disord 2020;42:102148 (Quick Check; CC BY-NC-ND 4.0, used unchanged).
- Baldassari LE et al. *Streamlined EDSS for use in multiple sclerosis clinical practice.* Mult Scler 2018;24(10):1347-55 (Clinical mode, sEDSS).
- MS Score Hub instruments are cited in full inside the app (References & scoring sources).
- Montalban X, Lebrun-Frénay C, Oh J et al. *Diagnosis of multiple sclerosis: 2024 revisions of the McDonald criteria.* Lancet Neurol (2025);24(10):850–865 (MS Criteria Checker), with companion consensus papers (2024 MAGNIMS–CMSC–NAIMS MRI recommendations; visual system; kFLC / OCB) and Solomon AJ et al. Lancet Neurol 2023;22:750–68 (differential diagnosis).
- Functional-System scoring follows the standardized rules in the sources above (implemented from the rules, with MSpectrum's own wording), including the Cerebellar (severe-ataxia) and Bowel/Bladder (loss-of-function to FS 5/6) rules, and an optional toggle to exclude fatigue from the Cerebral FS per study protocol.

---

## License

© 2026 Anas Z. Nourelden. Licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0) - see the [LICENSE](LICENSE) file for the full text.

In short: you are free to use, study, share and modify MSpectrum, but any distributed or network-served modified version must also be released as open source under the same licence (AGPL Section 13, network-use clause). This keeps the tool free and open for the MS community while protecting the authors' work. For a different (e.g. commercial or closed) arrangement, contact the authors for separate licensing.

### Instrument use & attribution

The AGPL-3.0 licence covers MSpectrum's own code, algorithms and interface - **not** the third-party clinical instruments it scores. Each instrument remains the property of its authors/publishers and is used here for research and educational purposes:

- **Item wording shown in full, with citation** (public domain or free to use): PHQ-9, GAD-7 (Pfizer, no permission required), MFIS (public domain), PDDS (not copyrighted; provided by the NARCOMS Registry), SymptoMScreen (CC BY 4.0), FES-I (free when referenced), the MSQLI scales (NMSS 1997 manual, provided for photocopying and use), the RAND-36 (RAND: no written permission needed; credit line given), the Sleep Condition Indicator (Sleepio, CC BY-NC 4.0) and the 0-10 pain rating. See [LICENSES-INSTRUMENTS.md](LICENSES-INSTRUMENTS.md) for one row per instrument.
- **Number-entry only, item wording not reproduced** (copyrighted; short topic labels only): FSS, MSQOL-54, ABC, MSWS-12, MSIS-29, PROMIS-29 and PROMIS Cognitive Function 4a, plus the licensed performance tests SDMT, BVMT-R, CVLT-II, LCVA/Sloan and FSMC. Enter answers from your own copy of the official form.

PROMIS T-scores are not computed: HealthMeasures holds copyright in the scoring tables, so MSpectrum shows raw sums only until written permission is given. PROMIS® is a registered trademark of the U.S. Department of Health and Human Services. BVMT-R and CVLT-II norms come from peer-reviewed papers (Parmenter 2010), not from the test manuals. If you reuse MSpectrum, you are responsible for complying with each instrument's own terms.

---

## Disclaimer

For clinical, research and educational use. Not a diagnosis and not a substitute for a clinician. The final EDSS step remains the responsibility of the examining clinician; validate locally before any trial or registry use. EDSS scoring follows the Kurtzke EDSS (Kurtzke 1983) and the standardized scoring rules described in the published sources listed above. MSpectrum is independent: it is not affiliated with, endorsed by, or licensed by Neurostatus-UHB AG or the University Hospital Basel, and Neurostatus-UHB AG was not involved in its development or validation. Neurostatus and Neurostatus-EDSS are trademarks of Neurostatus-UHB AG, named here only to identify the rating system that some of the cited papers describe. The definitions shown in the tool are summaries written by the MSpectrum authors, not the official Neurostatus definitions; obtain official materials and rater certification from Neurostatus-UHB AG when a study requires them. Train mode is a practice aid, not Neurostatus training or certification.

MSpectrum has not been reviewed, cleared, or approved by the U.S. Food and Drug Administration. It is provided "as is", without warranty of any kind; the authors accept no liability for any use of the tool or its results. All processing happens on the user's device; MSpectrum does not upload, store, or transmit data. Content and views are the authors' own and do not represent the official position of any institution.

Parts of this code were written with AI-assisted tools and reviewed by the author. This repository contains no patient data or patient images. Proprietary/licensed instruments (e.g. SDMT, BVMT-R, CVLT-II, FSS, MSQOL-54, ABC, MSWS-12, MSIS-29, PROMIS) are scored from entered values only; their full content and norm tables are not reproduced, and users must hold any required licence and use the official forms.
