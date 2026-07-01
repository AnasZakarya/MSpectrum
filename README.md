# MSpectrum

**MSpectrum** is a free, offline, privacy-first hub for the outcome measures used in multiple sclerosis. Everything is computed in your browser — nothing is uploaded or stored. It has two parts:

- **AutoEDSSguide** (`index.html`) — the full Neurostatus EDSS (Kappos 2011) with the algorithmic combination rules of Fouad et al. 2023, plus streamlined (Baldassari 2017) and patient-reported (Romeo 2021) fast modes, a print-ready Neurostatus sheet, and an OCR sheet scanner.
- **MS Score Hub** (`scores.html`) — stateless calculators and full questionnaires for the cognition, fatigue, mood, walking, quality-of-life and disease-severity measures used alongside the EDSS, each with automatic published norms (z / T / percentile) and a plain-language interpretation.

Developed at Wayne State University, Department of Neurology.

---

## Try it now

**[▶ Open MSpectrum](https://anaszakarya.github.io/MSpectrum/)**

No installation. No login. Works in any modern browser.

---

## AutoEDSSguide — five ways to use it

| Mode | For whom | What it is |
|------|----------|------------|
| **Roadmap** | Raters / research | Full Neurostatus exam, guided step-by-step in exam order (history → cranial nerves → body). |
| **System view** | Raters | All 7 Functional Systems on one page, classic Neurostatus layout. |
| **Clinical EDSS** | Neurologists | Fast adaptive follow-up scoring (streamlined sEDSS, Baldassari 2017). |
| **Quick Check** | People with MS | Plain-language adaptive questionnaire (~14 questions, ePR-EDSS / Romeo 2021) to self-estimate EDSS. |
| **Sheet Scanner** | Raters | Upload or photograph a completed Neurostatus form; fields are OCR-extracted and scored. |

All modes compute through a **single shared engine**, so the header, roadmap, printed sheet, and scanner always produce identical EDSS values.

---

## MS Score Hub — measures beyond EDSS

Stateless calculators and full questionnaires. Every result shows the raw score **and** an automatic standardized score (z / T / percentile) with a plain-language interpretation and the norm source cited; nothing is stored.

| Domain | Instruments | Standardized output (source) |
|--------|-------------|------------------------------|
| Disability & severity | EDSS, PDDS, **ARMSS / MSSS** | severity vs peers by age / disease duration (Manouchehrinia 2017; Roxburgh 2005) |
| Cognition (BICAMS) | SDMT, CVLT-II, BVMT-R, **BICAMS** panel | auto z + impairment (z ≤ −1.5): SDMT US norms (Strober 2020); CVLT-II/BVMT-R regression norms (Marrie 2021); BVMT-R Learning/Delayed-Recall T (Benedict 1997); CVLT-II LDFR T (Parmenter 2010) |
| Cognition (other) | PASAT-3 | z vs NMSS Task Force (Fischer 2001) |
| Motor / function | T25FW, 9-HPT, **MSFC** | z & composite vs NMSS Task Force (Fischer 2001) |
| Fatigue | MFIS (≈38), FSS (≥4) | clinical cut-offs |
| Mood | PHQ-9, GAD-7 | validated severity bands (+ PHQ-9 item-9 safety prompt) |
| Walking | MSWS-12 | 0–100 transform |
| Quality of life / impact | MSQOL-54, PROMIS-29 v2.1, MSIS-29 | MSQOL composites; PROMIS official raw→T tables (HealthMeasures); 0–100 transforms |

Extras: demographics entered once drive the cognitive z-scores; CVLT-II recognition sub-scores (SDFR, LDFR, d′, discriminability, Forced-Choice validity); a guided **Check my MS** patient pathway with a plain-language report; a **Clinician summary** that compiles all entered tools; out-of-range input flagging; unanswered-item highlighting; an **"ℹ How it works"** helper on every tool; **Export JSON / CSV** per tool. Self-report questionnaires can be filled by the patient; performance tests and composites are clinician-administered.

> **Not a diagnosis.** MSpectrum reports scores from validated, published instruments and explains what they mean. Interpretation, diagnosis and treatment remain the decision of a qualified clinician. See the in-app **Disclaimer & terms of use** for the full medico-legal notice.

---

## Offline & privacy

Works fully offline once loaded (open `index.html` directly). No account, no tracking, nothing uploaded or stored. Do not enter patient names or identifiers (PHI) — use a non-identifying code.

---

## Cite us

If you used MSpectrum in research, please cite it:

> Nourelden A, Memon A. *MSpectrum: a free, offline toolkit for multiple sclerosis outcome measures (AutoEDSSguide and MS Score Hub).* Wayne State University, Department of Neurology; 2026. Available from: https://github.com/AnasZakarya/MSpectrum

(GitHub also offers ready APA/BibTeX via the "Cite this repository" button, generated from `CITATION.cff`.)

---

## Algorithm & scoring sources

- Kappos L. *Neurostatus scoring definitions* (v04/10.2), 2011
- Fouad S, et al. *An algorithmic approach to the EDSS.* Mult Scler J–ETC (2023). DOI: [10.1177/20552173231155055](https://doi.org/10.1177/20552173231155055)
- Baldassari LE, et al. *Streamlined EDSS (sEDSS).* Mult Scler J (2017) — Clinical EDSS mode
- Romeo AR, et al. *Electronic patient-reported EDSS (ePR-EDSS).* Mult Scler (2021) — Quick Check mode
- MS Score Hub instruments are cited in full inside the app (References & scoring sources).
- Functional-System scoring follows the **Neurostatus v04/10.2 definitions** exactly, including the Cerebellar (severe-ataxia) and Bowel/Bladder (loss-of-function → FS 5/6) rules, and an optional toggle to exclude fatigue from the Cerebral FS per study protocol.

---

## Disclaimer

For clinical, research and educational use. Not a diagnosis and not a substitute for a clinician. The final EDSS step remains the responsibility of the examining clinician; validate locally before any trial or registry use. Implements the Neurostatus scoring system © Ludwig Kappos; not affiliated with or endorsed by the Neurostatus group. Proprietary/licensed instruments (e.g. SDMT, BVMT-R, CVLT-II, MSWS-12, MSIS-29) are scored from entered values only — their full content and norm tables are not reproduced; users must hold any required licence and use the official forms.
