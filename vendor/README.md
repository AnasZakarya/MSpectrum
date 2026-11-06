# Self-hosted libraries

PDF and screenshot libraries used by the export paths, bundled locally so
third-party CDN code never runs against the rendered patient sheet (a
supply-chain / PHI-exposure hardening) and so export works offline.

| File | Library | Version | License | Used by |
|---|---|---|---|---|
| `html2canvas.min.js` | html2canvas | 1.4.1 | MIT | `index.html` (email PDF), `scores.html` |
| `jspdf.umd.min.js` | jsPDF | 4.2.1 | MIT | `index.html` (email PDF) |
| `html2pdf.bundle.min.js` | html2pdf.js (bundles html2canvas + jsPDF 4 + DOMPurify) | 0.14.0 | MIT | `scores.html` |

Fetched from npm at the pinned versions above. v28 (2026-11): jsPDF 2.5.1 -> 4.2.1 and html2pdf.js 0.10.1 -> 0.14.0 to clear CVE-2025-29907 and later jsPDF advisories.

- `scores.html` now loads **only these local files** - no external origin.
- `index.html` loads the local copy first and falls back to the cdnjs URL if the
  local file is missing (e.g. not uploaded to the deploy root).

## OCR libraries (v31, `vendor/ocr/`)

The Sheet Scanner now loads these self-hosted copies first and falls back to the CDN only if a file is missing, so OCR works offline and behind hospital firewalls that block CDNs.

| Folder | Library | Version | License |
|---|---|---|---|
| `ocr/pdfjs/` | pdf.js (pdfjs-dist) | 3.11.174 | Apache-2.0 |
| `ocr/tesseract/` | tesseract.js | 5.1.0 | Apache-2.0 |
| `ocr/tesseract-core/` | tesseract.js-core (LSTM builds) | 5.1.0 | Apache-2.0 |
| `ocr/tessdata/` | English data, 4.0.0_best_int (@tesseract.js-data/eng) | 1.0.0 | Apache-2.0 |
| `ocr/ort/` | onnxruntime-web (single-thread WASM) | 1.19.2 | MIT |
| `ocr/opencv/` | OpenCV.js (docs.opencv.org/4.x build) | 4.13.0 | Apache-2.0 |

Note: docs.opencv.org serves no 4.10.0 build (404), so the 4.x build the scanner was validated with is self-hosted. SHA-256 hashes for every file are in `sbom.cdx.json`.

## Updating / verifying

```
npm pack html2canvas@1.4.1 jspdf@4.2.1 html2pdf.js@0.14.0
# then copy dist/html2canvas.min.js, dist/jspdf.umd.min.js, dist/html2pdf.bundle.min.js here
```
