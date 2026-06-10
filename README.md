# AutoEDSSguide

**AutoEDSSguide** is a free, offline-capable EDSS scoring tool for multiple sclerosis research and clinical assessment. It implements the Neurostatus algorithm (Kappos 2011) with the algorithmic combination rules of Fouad et al. 2023, plus streamlined (Baldassari 2017) and patient-reported (Romeo 2021) variants for its fast modes.

Developed at Wayne State University, Department of Neurology.

---

## Try it now

**[▶ Open AutoEDSSguide](https://anaszakarya.github.io/AutoEDSSguide/)**

No installation. No login. Works in any modern browser.

---

## Five ways to use it

| Mode | For whom | What it is |
|------|----------|------------|
| **Roadmap** | Raters / research | Full Neurostatus exam, guided step-by-step in exam order (history → cranial nerves → body). |
| **System view** | Raters | All 7 Functional Systems on one page, classic Neurostatus layout. |
| **Clinical EDSS** | Neurologists | Fast adaptive follow-up scoring (streamlined sEDSS, Baldassari 2017) — wheelchair/bedbound cases finish in under a minute. |
| **Quick Check** | People with MS | Plain-language adaptive questionnaire (~14 questions, ePR-EDSS / Romeo 2021) to self-estimate EDSS. |
| **Sheet Scanner** | Raters | Upload or photograph a completed Neurostatus form; fields are OCR-extracted and scored. |

All five modes compute through a **single shared engine**, so the header, roadmap, printed sheet, and scanner always produce identical EDSS values.

---

## What it does

- Calculates EDSS and all 7 FS scores in real time as you enter findings
- One shared, Neurostatus/Fouad-exact scoring engine across every mode
- "Set normal / Clear" buttons (global, per-system, and for large sections) to speed up exams
- Generates a print-ready, auto-populated Neurostatus scoring sheet (PDF)
- Emails the sheet as a PDF attachment (via the device share sheet, or download + mail)
- Flags clinical inconsistencies (bilateral mismatches, cross-system conflicts, unusual FS combinations)
- OCR scanning of photographed or uploaded Neurostatus forms
- Exports data as JSON or REDCap-compatible CSV (+ REDCap data dictionary)
- Auto-fills the examination date; patient info flows to the printed sheet header

---

## How to use

1. Open the tool via the link above (or double-click `index.html` locally).
2. Choose a mode from the landing page.
3. Fill in findings — EDSS updates live in the header. Use **Set all normal** to pre-fill a normal exam, then change only the abnormal items.
4. Open the **Final Sheet** tab to review, print/export to PDF, or email the sheet.

### Saving and transferring data
- **Save / Load** — stores data in your browser (same device only)
- **Export JSON** — a file you can re-import on another device
- **REDCap CSV / Dictionary** — flat CSV + data dictionary ready for REDCap import

---

## Offline use

The tool works fully offline once loaded. Open `index.html` directly with no internet and it falls back to system fonts gracefully. (PDF generation for email uses libraries fetched on first use.)

---

## Cite this tool

> Zakarya A, et al. *AutoEDSSguide: an offline EDSS scoring tool for MS research.* Wayne State University, 2025. Available at: https://github.com/AnasZakarya/AutoEDSSguide

---

## Algorithm sources

- Kappos L. *Neurostatus scoring definitions* (v04/10.2), 2011
- Fouad S, et al. *An algorithmic approach to the EDSS.* J Mult Scler (2023). DOI: [10.1177/20552173231155055](https://doi.org/10.1177/20552173231155055)
- Baldassari LE, et al. *Streamlined EDSS (sEDSS) for clinical practice.* Mult Scler J (2017) — used in Clinical EDSS mode
- Romeo AR, et al. *Electronic patient-reported EDSS (ePR-EDSS).* Mult Scler (2021) — used in Quick Check mode

---

## Disclaimer

This tool is for clinical and research use only. The final EDSS step remains the responsibility of the examining clinician. Validate locally before any trial or registry use.

This tool implements the Neurostatus scoring system © Ludwig Kappos. It is not affiliated with or endorsed by the Neurostatus group.
