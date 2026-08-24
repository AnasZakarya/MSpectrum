# MSpectrum: Developer Notes

Internal reference for architecture, deployment, and updates.

---

## Repository

- Source: https://github.com/AnasZakarya/MSpectrum
- Live: https://anaszakarya.github.io/MSpectrum/
- GitHub Pages serves from the **repo root**; the local `Codes/` folder is a
  mirror of that root. Deploy by uploading changed files to the repo root.

---

## File structure

```
index.html            EDSS app (HTML + CSS + JS + inlined OCR engine, ~2.0 MB)
scores.html           MS Score Hub (instruments, norms, "Check my MS")
mcdonald.html         2024 McDonald criteria checker
ocr2.js               source of the OCR2 engine (inlined into index.html)
edss_calc.py          Python reference port of the scoring engine
test_edss_calc.py     Python parity/UI tests
tests/                Node test harness (zero-dep): `node tests/run.js`
fonts/                self-hosted woff2 + OFL licenses (replaces Google Fonts)
vendor/               self-hosted html2canvas / jsPDF / html2pdf.js (MIT)
deploy/               nginx + apache security-header samples
_headers              Netlify / Cloudflare Pages header rules
sw.js                 service worker (network-first PWA cache)
manifest.webmanifest  PWA manifest + icons, og-image.png
SECURITY.md           security model + vuln reporting
PRIVACY-and-HIPAA.md  privacy / HIPAA-conscious usage guide
```

> The app is one file per page; `index.html` is large because the OCR2 engine
> and its assets are inlined. This is intentional (single-file, offline-capable).

---

## Scoring engine (do not break)

- `calculateFullEDSS(inputs)` in `index.html` is the **single scoring engine**.
  All paths (System view, Roadmap, OCR scanner) build their own input dict and
  funnel through it. Per-FS functions (`calcVisualFS`, `calcPyramidalFS`, ...)
  are pure and node-testable.
- Reference: `Literature search & scheme/Original EDSS neurostatus.pdf`
  (Kappos/Kurtzke). Audited letter-by-letter.
- The engine's pure region ends at an `if (true) { module.exports = {...} }`
  hook; the test harness (`tests/load_engine.js`) slices from the first bare
  `<script>` to that hook and requires it. **Do not add a bare `<script>` block
  before the engine block, and keep the export hook intact**, or the harness
  breaks. New inline scripts should carry an attribute or sit after the engine.

## Tests (must stay green)

```
node tests/run.js     # or: npm test
```
Runs the engine battery + Score Hub / PROMIS / norms / McDonald checks in
isolated child processes. Also sanity-check that every inline `<script>` block
parses after any edit to the HTML.

---

## Fonts and libraries (self-hosted)

- Fonts: `fonts/` (Fraunces + IBM Plex, latin subset, OFL). No Google Fonts.
  `@font-face` is inlined per page in `<style id="mspectrum-fonts">`.
- Export libs: `vendor/` (html2canvas, jsPDF, html2pdf.js). `scores.html` loads
  only these local copies; `index.html` loads local-first with a cdnjs fallback.
- OCR libs (OpenCV.js, Tesseract.js, onnxruntime-web, pdf.js) still load from
  CDN in `index.html`. To self-host them, run `node tools/fetch-vendor.mjs`
  (uncomment the OCR jobs) and re-point the loaders (notes in that script), then
  browser-test the Sheet Scanner.
- Refresh vendored assets with the `npm pack` commands in `fonts/README.md` and
  `vendor/README.md`.

---

## Updating the app

1. Edit files locally in `Codes/`.
2. Run `node tests/run.js` (green) and confirm inline JS parses.
3. Upload changed files to the GitHub repo root (Add file -> Upload files, or
   edit in place), commit to `main`. Pages redeploys in ~30 s.
4. **When adding the new `fonts/` and `vendor/` folders, upload them to the root
   too**, or self-hosted fonts and `scores.html` PDF export will 404.

---

## Deployment security

GitHub Pages cannot set HTTP headers, so the in-page `<meta>` CSP is the ceiling
there. On a headers-capable host, add the transport headers:
`_headers` (Netlify/Cloudflare Pages), `deploy/nginx-security.conf`,
`deploy/apache.htaccess`. Always serve over HTTPS. See `SECURITY.md`.

Other static hosts: Netlify (drag the folder), Cloudflare Pages (upload assets).
Local (no internet): open `index.html` directly; the OCR needs internet on first
use until its CDN libs are cached (or vendored).
