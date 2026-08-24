# Security

MSpectrum is a **fully static, client-side web app**. There is no backend, no
database, no account system, and no server-side code. Everything (EDSS scoring,
questionnaires, OCR, PDF export) runs in the visitor's browser. This shapes the
whole security model: the main asset to protect is the patient data a user types
in, and that data stays on the user's device.

## Data flow

- Scores, exam findings and any text a user enters live only in page memory and,
  if the user presses **Save to browser**, in that browser's `localStorage`.
- Nothing is uploaded. The app makes no API calls with user data.
- Network requests are limited to fetching **static libraries** (see Third-party
  code below). None of them receive patient data.
- **Export** (PDF / JSON / CSV) writes files to the user's own device only.

## In-page protections (active on every deploy, including GitHub Pages)

- **Content-Security-Policy** meta tag on all three pages: `default-src 'self'`,
  `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, and an explicit
  allow-list for the few library origins the OCR needs. `scores.html` and
  `mcdonald.html` load **no external origins at all**.

> `'unsafe-eval'` is kept in `index.html` and `scores.html` because it is genuinely required: `html2pdf.bundle` uses `Function("...")` (global detection, jsPDF cell rendering) and the OCR WASM libraries need it. Dropping it breaks PDF export and the scanner, so it stays.
- **`<meta name="referrer" content="no-referrer">`** so URLs are never leaked.
- Fonts are **self-hosted** (`fonts/`); the app makes **no request to Google
  Fonts** or any font CDN.
- The PDF/screenshot libraries used by the EDSS and Score Hub pages are
  **self-hosted** (`vendor/`), so third-party code never touches the rendered
  patient sheet on those paths.

## Server deployment (when not on GitHub Pages)

GitHub Pages cannot set HTTP response headers, so the meta CSP is the ceiling
there. When hosting MSpectrum on your own server or a headers-capable host, add
the stronger transport headers:

- `_headers` - Netlify / Cloudflare Pages.
- `deploy/nginx-security.conf` - Nginx snippet.
- `deploy/apache.htaccess` - Apache (rename to `.htaccess`).

These add HSTS, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`
(plus CSP `frame-ancestors 'none'`), `Referrer-Policy`, a locked-down
`Permissions-Policy`, and cross-origin isolation headers. Always serve over
**HTTPS**.

## Third-party code (OCR only, `index.html`)

The Sheet Scanner loads these version-pinned libraries from public CDNs on first
use; they process the uploaded sheet image **in the browser** and send nothing
back:

| Library | Purpose | Origin |
|---|---|---|
| OpenCV.js | image geometry / deskew | docs.opencv.org |
| Tesseract.js | text recognition | jsDelivr / unpkg / cdnjs (fallback chain) |
| onnxruntime-web | digit CNN | jsDelivr |
| pdf.js | render uploaded PDF sheets | cdnjs |

**Hardening path (recommended, not yet applied):** vendor these into `vendor/`
so the OCR is fully self-contained and offline, removing the last third-party
requests. A helper is provided at `tools/fetch-vendor.mjs`. This was left as a
follow-up because it needs browser testing of the OCR flow after re-pointing the
loaders.

## Reporting a vulnerability

Please report security issues privately to the maintainers (see `CITATION.cff` /
the GitHub repository contact) rather than opening a public issue. Include steps
to reproduce and the affected page.
