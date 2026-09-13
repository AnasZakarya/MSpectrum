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
index.html            EDSS app (HTML + CSS + JS + inlined OCR engine, ~1.7 MB)
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
- `calcEDSSStepTrace(fs, AS)` returns the EDSS step **and** the branch it took
  (`fs_pattern`, `as_floor`, `as_fixed`) with a plain-language reason. The
  "How was this scored?" panel, `edssWhatWouldChange` (one grade up or down) and
  `edssProvisional` (missing fields, range) all read that trace, so the number
  and its explanation cannot drift apart. Clinical mode calls the same engine
  through `clinCalcEDSS`. `ENGINE_VERSION` is stamped on the Final Sheet, the
  exports and the "Scoring conventions" panel in About; bump it when a rule
  changes. `edss_calc.py` mirrors the engine (116 unittest cases).
- FS combination table (`_fsOnlyStep`, mirrored in `edss_calc._fs_only_step`):
  the FS pattern alone never exceeds 5.0 ("EDSS steps 5.5 to 8.0 are
  exclusively defined by the ability to ambulate", Neurostatus general rules)
  and a FS 6 forces at least 6.0. Engine 3.2 fixed this (3.1 returned 5.5/6.0
  from FS alone). Verified against the Sen 2018 worked examples.
- Ambulation Score 0 to 15 (`AS_FIXED_EDSS`, `AS_FLOOR_EDSS`, `AS_LABEL`);
  AS 13 to 15 map to 8.5, 9.0 and 9.5. Cerebral FS = max(mentation, fatigue);
  depression or euphoria alone give Cerebral FS 1 on the sheet but not in the step.
- The engine's pure region ends at an `if (false) { module.exports = {...} }`
  hook (the harness flips it to `true`); the test harness (`tests/load_engine.js`) slices from the first bare
  `<script>` to that hook and requires it. **Do not add a bare `<script>` block
  before the engine block, and keep the export hook intact**, or the harness
  breaks. New inline scripts should carry an attribute or sit after the engine.

## Tests (must stay green)

```
node tests/run.js     # or: npm test
```
Runs the engine battery + Score Hub / PROMIS / norms / McDonald checks in
isolated child processes. Also sanity-check that every inline `<script>` block
parses after any edit to the HTML (a naive regex splitter reports two false
positives for template strings containing `<\/script>`; a headless-browser
load with no page errors is the real check).

## UI conventions (2026-09)

- Every hub page opens with one `info-rail` (Who / How / Disclaimer) instead of
  stacked notice boxes; the full disclaimer lives in the footer or About.
- Score Hub tool cards are split at load into `.panel-main` (form) and
  `aside.panel-side` (result, patient-bar note, Save/CSV buttons); on screens
  1000 px and wider the side panel is sticky on the right, on phones it sticks
  to the bottom (static inside the patient flow). "How it works" and "Scoring
  and sources" start closed; the page-bottom references card opens from the
  footer "Sources" link. Calc functions still write to the same `*_out` ids.
  The "This patient" bar on the hub (`pb_*` inputs, `pbApply()`) feeds the
  demographic fields of SDMT, BVMT-R, CVLT-II, BICAMS, 6MWT and ARMSS/MSSS.
  Test-fill rows (`.actions.fill-row`) are hidden while `body.patient-flow` is
  set (Check my MS). The Check my MS checklist is generated from `GFLOW` +
  `GFLOW_META` (time estimates, done checks); edit those, never the HTML.
- AutoEDSSguide: list questions render as radio rows (the user preferred them).
  The chip layout is still in the code behind `CHIPS_ENABLED = false`
  (`_chipShorts`, `.score-chip` CSS); flip the flag to try it. Cards whose
  title starts with "Optional" render as a closed `<details>` (opened
  automatically before print). Roadmap tabs are numbered 1 to 4 + Σ. The
  per-tab disclaimer bar is gone; the disclaimer sits once in the app footer
  and on the Final Sheet.
- Train mode (`#train`, `TRAIN_CASES`, `showTrain`): 20 reference cases, four
  of them the published worked examples in Sen S, Arch Neuropsychiatry
  2018;55(Suppl 1):S80-3; the answer key is `calcEDSSStepTrace` on the case's
  FS grades and AS, so it can never disagree with the engine. Add cases to
  `TRAIN_CASES` only (fields: title, fs, as, note, optional src).
- Landing keeps the original nine feature cards and the original About
  toggles; "Cite us" has a Copy button (`#cite-text`). The three notices on
  each hub page are `.info-cards` (icon, title, full text).
- McDonald: `calculateDiagnosis()` still sets the internal scenario strings
  ("Possible Multiple Sclerosis (Single Location)", "... (RIS-onset)", etc.);
  `RESULT_LABELS` in `updateUI()` maps them to the seven displayed categories
  ("2024 McDonald criteria met", "... (pending exclusion of alternatives)",
  "Possible MS: criteria not yet met", "Radiologically Isolated Syndrome (RIS)",
  "Criteria not met: clinically isolated syndrome", "Criteria not met:
  non-specific incidental lesions", "Incomplete: brain MRI required"). Badge and
  print logic key on the substrings "pending exclusion", "criteria met",
  "Possible", "not met", "Incomplete". Every branch that is not "criteria met"
  sets `complete` (the "What would complete the criteria" line, `#result-complete`
  and `#print-complete`). The specific-marker caution uses `needsSpecific`
  (age >= 50 or any vascular risk factor). Print sheet says "Not assessed" for
  modalities not ticked.

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
