# MSpectrum

**MSpectrum** is a free, browser-based, privacy-first hub for the outcome measures used in multiple sclerosis. Everything is computed in your browser; nothing is uploaded or stored. It has four parts:

- **AutoEDSSguide** (`index.html`): the full EDSS exam, scored with the published Neurostatus conventions (Kappos 2011) and the algorithmic combination rules of Fouad et al. 2023, plus streamlined (Baldassari 2017) and patient-reported (Romeo 2021) fast modes, a print-ready EDSS sheet in the standard FS layout used on research and clinical-trial forms, and an OCR sheet scanner.
- **MS Score Hub** (`scores.html`): stateless calculators and full questionnaires for the cognition, fatigue, mood, walking, quality-of-life and disease-severity measures used alongside the EDSS, each with automatic published norms (z / T / percentile) and a plain-language interpretation.
- **Check my MS** (`scores.html#report`): a guided, patient-facing pathway that walks through the self-report questionnaires and produces one plain-language summary of how MS is affecting the person, for understanding and discussion rather than diagnosis.
- **MS Criteria Checker** (`mcdonald.html`): an adaptive wizard that applies the 2024 revisions of the McDonald criteria (Montalban et al., Lancet Neurol 2025) to reach an MS diagnosis across relapsing, progressive and RIS onset, covering the five DIS regions (incl. optic nerve), DIT, CSF (OCB / k-FLC) and susceptibility markers (CVS, PRL), with older-onset and mimic safeguards and a printable summary.

Developed at Wayne State University, Department of Neurology.

---

## Try it now

**[▶ Open MSpectrum](https://anaszakarya.github.io/MSpectrum/)**

No installation. No login. Works in any modern browser.

---

## AutoEDSSguide: five ways to use it

| Mode | For whom | What it is |
|------|----------|------------|
| **Roadmap** | Raters / research | Full standardized EDSS exam, guided step-by-step in exam order (history, then cranial nerves, then body). |
| **System view** | Raters | All 7 Functional Systems on one page, in the classic FS layout used on research EDSS forms. |
| **Clinical EDSS** | Neurologists | Fast adaptive follow-up scoring (streamlined sEDSS, Baldassari 2017). |
| **Quick Check** | People with MS | Plain-language adaptive questionnaire (~14 questions, ePR-EDSS / Romeo 2021) to self-estimate EDSS. |
| **Sheet Scanner** | Raters | Upload or photograph a completed EDSS scoring sheet (standard research layout); fields are OCR-extracted and scored. |

All modes compute through a **single shared engine**, so the header, roadmap, printed sheet, and scanner always produce identical EDSS values.

---

## MS Score Hub: measures beyond EDSS

Stateless calculators and full questionnaires. Every result shows the raw score **and** an automatic standardized score (z / T / percentile) with a plain-language interpretation and the norm source cited; nothing is stored.

| Domain | Instruments | Standardized output (source) |
|--------|-------------|------------------------------|
| Disability & severity | EDSS, PDDS, **ARMSS / MSSS** | severity vs peers by age / disease duration (Manouchehrinia 2017; Roxburgh 2005) |
| Cognition (BICAMS) | SDMT, CVLT-II, BVMT-R, **BICAMS** panel | auto z + impairment (z ≤ −1.5): SDMT US norms (Strober 2020); CVLT-II/BVMT-R regression norms (Marrie 2021); BVMT-R Delayed-Recall T and CVLT-II LDFR T (Parmenter 2010) |
| Cognition (other) | PASAT-3 | z vs NMSS Task Force (Fischer 2001) |
| Motor / function | T25FW, 9-HPT, **MSFC** | z & composite vs NMSS Task Force (Fischer 2001) |
| Fatigue | MFIS (≈38), FSS (≥4) | clinical cut-offs |
| Mood | PHQ-9, GAD-7 | validated severity bands (+ PHQ-9 item-9 safety prompt) |
| Walking | MSWS-12 | 0–100 transform |
| Quality of life / impact | MSQOL-54, PROMIS-29 v2.1, MSIS-29 | MSQOL composites; PROMIS official raw-to-T **plus Standard Error (SE)** tables (HealthMeasures); 0–100 transforms |

Extras: demographics entered once drive the cognitive z-scores; CVLT-II recognition sub-scores (SDFR, LDFR, d′, discriminability, Forced-Choice validity); a guided **Check my MS** patient pathway with a plain-language report; a **Clinician summary** that compiles all entered tools; out-of-range input flagging; unanswered-item highlighting; an **"ℹ How it works"** helper on every tool; **Export JSON / CSV** per tool. Self-report questionnaires can be filled by the patient; performance tests and composites are clinician-administered.

### Score & norm converter (bulk)

A **Score & norm converter** turns a whole list of patients into finished scores at once: pick a questionnaire or test, paste one patient per line (values separated by comma, space or tab, with an optional leading ID), and get a downloadable results table. It covers **22 instruments** across four groups: patient-reported questionnaires (PHQ-9, GAD-7, MFIS, FSS, MSWS-12, MSIS-29, MSQOL-54, SymptoMScreen, FSMC, PDDS, ABC, FES-I), norm-based cognitive tests that use age/sex/education (SDMT, BVMT-R, CVLT-II), cognitive/motor tests scored against a fixed reference (PASAT-3, T25FW, 9-HPT), PROMIS (PROMIS-29 with raw + T + SE + band per domain, PROMIS Cognitive 4a), and disease severity (ARMSS, MSSS). This complements data platforms such as **REDCap**, giving the norm-based z/T scores those platforms store the answers for but do not compute. A downloadable **PROMIS raw-to-T-to-SE lookup table (CSV)** is also provided. For a single patient with the full breakdown and interpretation, each tool's own page is used instead. Everything runs in the browser; nothing is uploaded.

> **Decision support, not a diagnosis.** MSpectrum computes outcome-measure scores and applies published diagnostic criteria, and explains what the results mean. It supports clinical judgement but does not itself diagnose; interpretation, diagnosis and treatment remain the decision of a qualified clinician. See the in-app **Disclaimer & terms of use** for the full medico-legal notice.

---

## Offline & privacy

Works fully offline once loaded (open `index.html` directly). No account, no tracking, nothing uploaded or stored. Do not enter patient names or identifiers (PHI); use a non-identifying code.

Fonts and the PDF/export libraries are **self-hosted**, so a normal session makes no third-party requests at all (the optional OCR scanner is the only feature that fetches libraries, and it processes images in the browser). Saved data lives only in your browser; a **Clear saved data** button wipes it, which is useful on shared computers. For the deployment security model and a HIPAA-conscious usage guide, see [SECURITY.md](SECURITY.md) and [PRIVACY-and-HIPAA.md](PRIVACY-and-HIPAA.md).

---

## MS Criteria Checker: diagnosis by the 2024 McDonald criteria

An adaptive, single-page wizard (`mcdonald.html`) that implements the **2024 revisions of the McDonald criteria** (Montalban et al., Lancet Neurol 2025) and their companion consensus papers. It adapts to patient age and onset course (relapsing, primary-progressive, RIS), asks only about the investigations you have, and reports which diagnostic category the findings fulfil (criteria met, possible MS, RIS, criteria not met or incomplete), the criteria it rests on, safety cautions and recommended next steps, with a print / PDF summary. It applies the criteria; the diagnosis stays with the treating neurologist.

- **All 2024 pathways:** DIS across five regions (incl. optic nerve), the 4-region shortcut, DIT, CSF (OCB / k-FLC), and susceptibility markers (select-6 CVS, ≥ 1 PRL).
- **Safeguards:** older-onset (≥ 50) vascular caution, pediatric ADEM / MOG-IgG guidance, atypical red-flag prompts for NMOSD / MOGAD, and a "no better explanation" acknowledgment that is part of the criteria: until it is confirmed the category stays provisional.
- Independent educational aid; not affiliated with any commercial application.

---

## Cite us

If you used MSpectrum in research, please cite it:

> Nourelden A. *MSpectrum: a free, browser-based toolkit for multiple sclerosis outcome measures and diagnosis (AutoEDSSguide, MS Score Hub and MS Criteria Checker).* Wayne State University, Department of Neurology; 2026. Available from: https://github.com/AnasZakarya/MSpectrum

(GitHub also offers ready APA/BibTeX via the "Cite this repository" button, generated from `CITATION.cff`.)

---

## Algorithm & scoring sources

- Kappos L. *Neurostatus scoring definitions* (v04/10.2), 2011.
- Fouad S et al. *An algorithmic approach to the EDSS.* Mult Scler J–ETC (2023). DOI: [10.1177/20552173231155055](https://doi.org/10.1177/20552173231155055).
- Baldassari LE et al. *Streamlined EDSS (sEDSS).* Mult Scler J (2017) (Clinical EDSS mode).
- Romeo AR et al. *Electronic patient-reported EDSS (ePR-EDSS).* Mult Scler (2021) (Quick Check mode).
- MS Score Hub instruments are cited in full inside the app (References & scoring sources).
- Montalban X, Lebrun-Frénay C, Oh J et al. *Diagnosis of multiple sclerosis: 2024 revisions of the McDonald criteria.* Lancet Neurol (2025);24(10):850–865 (MS Criteria Checker), with companion consensus papers (2024 MAGNIMS–CMSC–NAIMS MRI recommendations; visual system; kFLC / OCB) and Solomon AJ et al. Lancet Neurol 2023;22:750–68 (differential diagnosis).
- Functional-System scoring follows the published **Neurostatus v04/10.2 scoring conventions** (implemented from the rules, with MSpectrum's own wording), including the Cerebellar (severe-ataxia) and Bowel/Bladder (loss-of-function to FS 5/6) rules, and an optional toggle to exclude fatigue from the Cerebral FS per study protocol.

---

## License

© 2026 Anas Z. Nourelden. Licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0) - see the [LICENSE](LICENSE) file for the full text.

In short: you are free to use, study, share and modify MSpectrum, but any distributed or network-served modified version must also be released as open source under the same licence (AGPL Section 13, network-use clause). This keeps the tool free and open for the MS community while protecting the authors' work. For a different (e.g. commercial or closed) arrangement, contact the authors for separate licensing.

### Instrument use & attribution

The AGPL-3.0 licence covers MSpectrum's own code, algorithms and interface - **not** the third-party clinical instruments it scores. Each instrument remains the property of its authors/publishers and is used here for research and educational purposes:

- **Item wording shown in full, with citation** (public domain or free to use): PHQ-9, GAD-7 (Pfizer, no permission required), MFIS (public domain), PDDS (not copyrighted), SymptoMScreen (free to use), FES-I (free when referenced), and the 0-10 pain rating.
- **Number-entry only, item wording not reproduced** (copyrighted; short topic labels only): FSS, MSQOL-54, ABC, MSWS-12, MSIS-29, PROMIS-29 and PROMIS Cognitive Function 4a, plus the licensed performance tests SDMT, BVMT-R, CVLT-II, LCVA/Sloan and FSMC. Enter answers from your own copy of the official form.

PROMIS T-scores are computed from the publicly available HealthMeasures scoring manuals and cited in-app; the lookup tables are not offered as a separate download. PROMIS® is a registered trademark of the U.S. Department of Health and Human Services. BVMT-R and CVLT-II norms come from peer-reviewed papers (Parmenter 2010; Marrie 2021), not from the test manuals. If you reuse MSpectrum, you are responsible for complying with each instrument's own terms.

---

## Disclaimer

For clinical, research and educational use. Not a diagnosis and not a substitute for a clinician. The final EDSS step remains the responsibility of the examining clinician; validate locally before any trial or registry use. EDSS scoring follows the Kurtzke EDSS (Kurtzke 1983), the published Neurostatus scoring conventions (Kappos 2011) and the algorithmic rules of Fouad et al. 2023 (CC BY-NC 4.0). MSpectrum is independent: it is not affiliated with, endorsed by, or licensed by Neurostatus-UHB AG or the University Hospital Basel, and Neurostatus-UHB AG was not involved in its development or validation. Neurostatus and Neurostatus-EDSS are trademarks of Neurostatus-UHB AG, named here only to identify the published conventions. The definitions shown in the tool are summaries written by the MSpectrum authors, not the official Neurostatus definitions; obtain official materials and rater certification from Neurostatus-UHB AG when a study requires them. Train mode is a practice aid, not Neurostatus training or certification.

MSpectrum has not been reviewed, cleared, or approved by the U.S. Food and Drug Administration. It is provided "as is", without warranty of any kind; the authors accept no liability for any use of the tool or its results. All processing happens on the user's device; MSpectrum does not upload, store, or transmit data. Content and views are the authors' own and do not represent the official position of any institution.

Parts of this code were written with AI-assisted tools and reviewed by the author. This repository contains no patient data or patient images. Proprietary/licensed instruments (e.g. SDMT, BVMT-R, CVLT-II, FSS, MSQOL-54, ABC, MSWS-12, MSIS-29, PROMIS) are scored from entered values only; their full content and norm tables are not reproduced, and users must hold any required licence and use the official forms.
