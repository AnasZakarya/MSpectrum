# Self-hosted libraries

PDF and screenshot libraries used by the export paths, bundled locally so
third-party CDN code never runs against the rendered patient sheet (a
supply-chain / PHI-exposure hardening) and so export works offline.

| File | Library | Version | License | Used by |
|---|---|---|---|---|
| `html2canvas.min.js` | html2canvas | 1.4.1 | MIT | `index.html` (email PDF), `scores.html` |
| `jspdf.umd.min.js` | jsPDF | 2.5.1 | MIT | `index.html` (email PDF) |
| `html2pdf.bundle.min.js` | html2pdf.js (bundles html2canvas + jsPDF) | 0.10.1 | MIT | `scores.html` |

Byte-for-byte the same builds as the previously used cdnjs URLs (fetched from
npm at the identical pinned versions).

- `scores.html` now loads **only these local files** - no external origin.
- `index.html` loads the local copy first and falls back to the cdnjs URL if the
  local file is missing (e.g. not uploaded to the deploy root).

> **Not yet vendored:** the OCR libraries (OpenCV.js, Tesseract.js,
> onnxruntime-web, pdf.js) still load from CDN in `index.html`. See
> `tools/fetch-vendor.mjs` and `SECURITY.md` for the path to fully self-host them.

## Updating / verifying

```
npm pack html2canvas@1.4.1 jspdf@2.5.1 html2pdf.js@0.10.1
# then copy dist/html2canvas.min.js, dist/jspdf.umd.min.js, dist/html2pdf.bundle.min.js here
```
