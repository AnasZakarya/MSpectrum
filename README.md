# MSpectrum

**MSpectrum** is a free, browser-based, privacy-first hub for the outcome measures used in multiple sclerosis. Everything is computed in your browser; nothing is uploaded or stored. It has four parts:

* **AutoEDSSguide** (`index.html`): the full Neurostatus EDSS with algorithmic combination rules, plus streamlined and patient-reported fast modes, a print-ready Neurostatus sheet, and an OCR sheet scanner.
* **MS Score Hub** (`scores.html`): stateless calculators and full questionnaires for the cognition, fatigue, mood, walking, quality-of-life and disease-severity measures used alongside the EDSS, each with automatic published norms (z / T / percentile) and a plain-language interpretation.
* **Check my MS** (`scores.html#report`): a guided, patient-facing pathway that walks through the self-report questionnaires and produces one plain-language summary of how MS is affecting the person, for understanding and discussion rather than diagnosis.
* **MS Criteria Checker** (`mcdonald.html`): an adaptive wizard that applies the 2024 revisions of the McDonald criteria to reach an MS diagnosis across relapsing, progressive and RIS onset, covering the five DIS regions (incl. optic nerve), DIT, CSF (OCB / k-FLC) and susceptibility markers (CVS, PRL), with older-onset and mimic safeguards and a printable summary.

Developed at Wayne State University, Department of Neurology, by Anas Nourelden, under the supervision of Dr. Anza Memon.

---

## Try it now

**[▶ Open MSpectrum](https://anaszakarya.github.io/MSpectrum/)**

No installation. No login. Works in any modern browser and is suitable for all devices and operating systems.

---

## AutoEDSSguide: five ways to use it

| Mode | For whom | What it is |
|------|----------|------------|
| **Roadmap** | Raters / research | Full Neurostatus exam, guided step-by-step in exam order (history, then cranial nerves, then body). |
| **System view** | Raters | All 7 Functional Systems on one page, classic Neurostatus layout. |
| **Clinical EDSS** | Neurologists | Fast adaptive follow-up scoring (streamlined sEDSS). |
| **Quick Check** | People with MS | Plain-language adaptive questionnaire (~14 questions) to self-estimate EDSS. |
| **Sheet Scanner** | Raters | Upload or photograph a completed Neurostatus form; fields are OCR-extracted and scored. |

All modes compute through a **single shared engine**, so the header, roadmap, printed sheet, and scanner always produce identical EDSS values.

---

## MS Score Hub: measures beyond EDSS

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
| Quality of life / impact | MSQOL-54, PROMIS-29 v2.1, MSIS-29 | MSQOL composites; PROMIS official raw-to-T **plus Standard Error (SE)** tables (HealthMeasures); 0–100 transforms |

Extras: demographics entered once drive the cognitive z-scores; CVLT-II recognition sub-scores (SDFR, LDFR, d′, discriminability, Forced-Choice validity); a guided **Check my MS** patient pathway with a plain-language report; a **Clinician summary** that compiles all entered tools; out-of-range input flagging; unanswered-item highlighting; an **"ℹ How it works"** helper on every tool; **Export JSON / CSV** per tool. Self-report questionnaires can be filled by the patient; performance tests and composites are clinician-administered.

### Score & norm converter (bulk)

A **Score & norm converter** turns a whole list of patients into finished scores at once: pick a questionnaire or test, paste one patient per line (values separated by comma, space or tab, with an optional leading ID), and get a downloadable results table. It covers **22 instruments** across four groups: patient-reported questionnaires (PHQ-9, GAD-7, MFIS, FSS, MSWS-12, MSIS-29, MSQOL-54, SymptoMScreen, FSMC, PDDS, ABC, FES-I), norm-based cognitive tests that use age/sex/education (SDMT, BVMT-R, CVLT-II), cognitive/motor tests scored against a fixed reference (PASAT-3, T25FW, 9-HPT), PROMIS (PROMIS-29 with raw + T + SE + band per domain, PROMIS Cognitive 4a), and disease severity (ARMSS, MSSS). This complements data platforms such as **REDCap**, giving the norm-based z/T scores those platforms store the answers for but do not compute. A downloadable **PROMIS raw-to-T-to-SE lookup table (CSV)** is also provided. For a single patient with the full breakdown and interpretation, each tool's own page is used instead. Everything runs in the browser; nothing is uploaded.

> **Decision support, not a diagnosis.** MSpectrum computes outcome-measure scores and applies published diagnostic criteria, and explains what the results mean. It supports clinical judgement but does not itself diagnose; interpretation, diagnosis and treatment remain the decision of a qualified clinician. See the in-app **Disclaimer & terms of use** for the full medico-legal notice.

---

## MS Criteria Checker: diagnosis by the 2024 McDonald criteria

An adaptive, single-page wizard (`mcdonald.html`) that implements the **2024 revisions of the McDonald criteria** (Montalban et al., Lancet Neurol 2025) and their companion consensus papers. It adapts to patient age and onset course (relapsing, primary-progressive, RIS), asks only about the investigations you have, and reports the diagnosis, the criteria it rests on, safety cautions and recommended next steps, with a print / PDF summary.

- **All 2024 pathways:** DIS across five regions (incl. optic nerve), the 4-region shortcut, DIT, CSF (OCB / k-FLC), and susceptibility markers (select-6 CVS, ≥ 1 PRL).
- **Safeguards:** older-onset (≥ 50) vascular caution, pediatric ADEM / MOG-IgG guidance, atypical red-flag prompts for NMOSD / MOGAD, and a "no better explanation" acknowledgment.
- Independent educational aid; not affiliated with any commercial application.

---

## Privacy

Works fully in your browser once loaded. No account, no tracking, nothing uploaded or stored. Do not enter patient names or identifiers (PHI); use a non-identifying code.

---

## Cite us

If you used MSpectrum in research, please cite it:

> Nourelden A, Memon A. *MSpectrum: a free, browser-based toolkit for multiple sclerosis outcome measures and diagnosis (AutoEDSSguide, MS Score Hub, patient report, and MS Criteria Checker).* Wayne State University, Department of Neurology; 2026. Available from: https://github.com/AnasZakarya/MSpectrum

(GitHub also offers ready APA/BibTeX via the "Cite this repository" button, generated from `CITATION.cff`.)

---

## References & scoring sources

**EDSS & diagnosis (algorithm)**
- Neurostatus/EDSS FS: Kappos L. Neurostatus definitions v04/10.2, 2011.
- EDSS algorithm: Fouad AM et al. Mult Scler J Exp Transl Clin 2023;9(1). doi:10.1177/20552173231155055.
- Streamlined EDSS (Clinical mode): Baldassari LE et al. Mult Scler J 2018;24(11):1526-35.
- Patient-reported EDSS (Quick Check): Romeo AR et al. Mult Scler J 2021;27(9):1432-41.
- McDonald 2024: Montalban X et al. Lancet Neurol 2025;24(10):850-65.
- Differential diagnosis: Solomon AJ et al. Lancet Neurol 2023;22(8):750-68.

**Cognition**
- SDMT: Smith A. SDMT manual, 1982; norms Strober L et al. 2020.
- BVMT-R: Benedict RHB. BVMT-R manual. PAR, 1997.
- CVLT-II: Delis DC et al. CVLT-II manual. Pearson, 2000; Parmenter BA et al. J Int Neuropsychol Soc 2010;16:6-16; Marrie RA et al. Front Neurol 2021;11:621010.
- BICAMS: Langdon DW et al. Mult Scler J 2012;18(6):891-8; Marrie RA et al. Front Neurol 2021;11:621010.
- PASAT-3: Gronwall DMA. Percept Mot Skills 1977;44:367-73; Fischer JS et al. Mult Scler 1999;5(4):244-50.
- PROMIS Cognitive Abilities 4a: Cella D et al. J Clin Epidemiol 2010; HealthMeasures (Northwestern).

**Fatigue**
- MFIS: Fisk JD et al. Clin Infect Dis 1994;18(Suppl 1):S79-83.
- FSS: Krupp LB et al. Arch Neurol 1989;46(10):1121-3.
- FSMC: Penner IK et al. Mult Scler 2009;15(12):1509-17.

**Mood**
- PHQ-9: Kroenke K et al. J Gen Intern Med 2001;16(9):606-13.
- GAD-7: Spitzer RL et al. Arch Intern Med 2006;166(10):1092-7.

**Walking & motor**
- MSWS-12: Hobart JC et al. Neurology 2003;60(1):31-6.
- T25FW: Fischer JS et al. Mult Scler 1999;5(4):244-50 (MSFC).
- 9-HPT: Mathiowetz V et al. Occup Ther J Res 1985;5(1):24-38; Fischer JS et al. Mult Scler 1999;5(4):244-50.
- 6MWT: Enright PL, Sherrill DL. Am J Respir Crit Care Med 1998;158:1384-7; Goldman MD et al. Mult Scler 2008.
- MSFC: Fischer JS et al. Mult Scler 1999;5(4):244-50.

**Quality of life & disability**
- PDDS: Hohol MJ et al. Neurology 1995;45(2):251-5; Learmonth YC et al. BMC Neurol 2013;13:37.
- MSQOL-54: Vickrey BG et al. Qual Life Res 1995;4(3):187-206.
- PROMIS-29: Cella D et al. J Clin Epidemiol 2010;63(11):1179-94.
- MSIS-29: Hobart J et al. Brain 2001;124(Pt 5):962-73.

**Pain, balance & symptoms**
- PROMIS Pain Intensity (Global07): Cella D et al. 2010; HealthMeasures.
- ABC scale: Powell LE, Myers AM. J Gerontol A Biol Sci Med Sci 1995;50A(1):M28-34.
- FES-I: Yardley L et al. Age Ageing 2005;34(6):614-9.
- SymptoMScreen: Green R et al. Int J MS Care 2017;19(1):1-8.

**Vision**
- LCVA: Sloan LL et al. J Opt Soc Am 1952; Balcer LJ et al. Neurology 2003;61(10):1433-5.

**Disease severity**
- ARMSS: Manouchehrinia A et al. Mult Scler 2017;23:1938-46.
- MSSS: Roxburgh RH et al. Neurology 2005;64:1144-51.

Note: ARR, CDP and NEDA-3/4 are computed disease-activity metrics based on standard published definitions (no single instrument citation).

---

## License

© 2026 Anas Z. Nourelden and Anza B. Memon. Licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0) — see the [LICENSE](LICENSE) file for the full text.

In short: you are free to use, study, share and modify MSpectrum, but any distributed or network-served modified version must also be released as open source under the same licence (AGPL Section 13, network-use clause). This keeps the tool free and open for the MS community while protecting the authors' work. For a different (e.g. commercial or closed) arrangement, contact the authors for separate licensing.

### Instrument use & attribution

The AGPL-3.0 licence covers MSpectrum's own code, algorithms and interface — **not** the third-party clinical instruments it scores. Each instrument remains the property of its authors/publishers and is used here for research and educational purposes:

- **Free / open instruments** are reproduced verbatim with citation: PROMIS (29, Cognitive, Pain), PHQ-9, GAD-7, PDDS, MFIS, MSQOL-54, FSS, ABC, FES-I, SymptoMScreen.
- **Reproduced under non-commercial academic use** (would require a paid licence if MSpectrum is ever commercialised): MSWS-12 and MSIS-29 (Transform MS CIC / Mapi-ePROVIDE), and FSS (Krupp — free for non-profit use).
- **Licensed instruments are number-entry only** — item text is never reproduced: SDMT, BVMT-R, CVLT-II, LCVA/Sloan (performance tests) and FSMC (shown as "Item N").

Normative conversion tables (e.g. the PROMIS raw→T→SE lookups) are taken verbatim from the official HealthMeasures scoring manuals and cited in-app. If you reuse MSpectrum, you are responsible for complying with each instrument's own terms.

---

## Disclaimer

For clinical, research and educational use. Not a diagnosis and not a substitute for a clinician. The final EDSS step remains the responsibility of the examining clinician; validate locally before any trial or registry use. Implements the Neurostatus scoring system © Ludwig Kappos; not affiliated with or endorsed by the Neurostatus group. Proprietary/licensed instruments (e.g. SDMT, BVMT-R, CVLT-II, MSWS-12, MSIS-29) are scored from entered values only; their full content and norm tables are not reproduced, and users must hold any required licence and use the official forms.
