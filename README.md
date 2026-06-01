# AutoEDSSguide

**AutoEDSSguide** is a free, offline-capable EDSS scoring tool for multiple sclerosis research and clinical assessment. Built on the Neurostatus algorithm (Kappos 2011) and validated against Fouad et al. 2023.

Developed at Wayne State University, Department of Neurology.

---

## Try it now

**[▶ Open AutoEDSSguide](https://anaszakarya.github.io/AutoEDSSguide/index.html)**

No installation. No login. Works in any modern browser.

---

## What it does

- Guides you through all 7 Functional Systems (FS) with structured input
- Calculates EDSS in real time as you enter exam findings
- Generates a print-ready Neurostatus-style scoring sheet (2-page PDF)
- Flags clinical inconsistencies (e.g. Pyramidal–Sensory dissociation)
- Scans photographed or uploaded Neurostatus forms via OCR
- Exports data as JSON or REDCap-compatible CSV

---

## How to use

1. Open the tool via the link above (or double-click `index.html` locally)
2. Choose your entry mode:
   - **Roadmap** — step-by-step guided exam entry
   - **System view** — all systems on one page
   - **Quick Check** — 5-question EDSS estimate
   - **Sheet Scanner** — upload or photograph a completed Neurostatus form
3. Fill in exam findings — EDSS updates live in the header
4. Go to the **Σ tab** to review and print the final scoring sheet

### Saving and transferring data
- **Save / Load** — stores data in your browser (same device only)
- **Export JSON** — saves a file you can email and re-import on another device
- **REDCap CSV** — exports a flat CSV ready for REDCap import

---

## Offline use

The tool works fully offline once loaded. Only Google Fonts is fetched on first visit (cached automatically). To use with no internet at all, double-click `index.html` — it falls back to system fonts gracefully.

---

## Cite this tool

> Zakarya A, et al. *AutoEDSSguide: an offline EDSS scoring tool for MS research.* Wayne State University, 2025. Available at: https://github.com/AnasZakarya/AutoEDSSguide

---

## Algorithm sources

- Kappos L. Neurostatus scoring definitions (v04/10.2), 2011
- Fouad S, et al. J Mult Scler (2023). DOI: [10.1177/20552173231155055](https://doi.org/10.1177/20552173231155055)

---

## Disclaimer

This tool is for clinical and research use only. The final EDSS step remains the responsibility of the examining clinician. Validate locally before any trial or registry use.

This tool implements the Neurostatus scoring system © Ludwig Kappos. It is not affiliated with or endorsed by the Neurostatus group.
