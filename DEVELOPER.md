# AutoEDSSguide — Developer Notes

Internal reference for deployment, updates, and architecture.

---

## Repository

https://github.com/AnasZakarya/AutoEDSSguide

Live site: https://anaszakarya.github.io/AutoEDSSguide/

---

## File structure

```
index.html                        ← entire app (HTML + CSS + JS, ~360 KB)
edss_calc.py                      ← Python version of the scoring engine (reference + tests)
test_edss_calc.py                 ← 94 parity tests + 18 end-to-end UI tests
README.md                         ← public-facing description
DEVELOPER.md                      ← this file
Wayne_State_Warriors_primary_logo.svg
```

---

## Updating the app

1. Edit `index.html` locally
2. Go to https://github.com/AnasZakarya/AutoEDSSguide
3. Click `index.html` → Edit (pencil icon) → or use Upload to replace the file
4. Commit directly to `main`
5. GitHub Pages redeploys automatically in ~30 seconds

---

## Deployment (GitHub Pages)

Already configured:
- Branch: `main`
- Folder: `/ (root)`
- URL: `https://anaszakarya.github.io/AutoEDSSguide/`

To change: Settings → Pages

---

## Alternative deployment options

**Netlify:** Sign in at netlify.com → drag the folder containing `index.html` → instant URL.

**Cloudflare Pages:** dash.cloudflare.com → Workers & Pages → Upload assets → drop folder.

**Local (no internet):** Double-click `index.html` in any browser. Camera capture requires HTTPS so won't work locally.

**Custom domain:** Add a `CNAME` file with your domain, then set a CNAME DNS record pointing to `anaszakarya.github.io`.

---

## Architecture

- Pure frontend — no server, no build step, no dependencies
- All logic in vanilla JavaScript inside `index.html`
- Data stored in `localStorage` (browser only, never sent anywhere)
- Scoring engine: `calculateFullEDSS()` → reads `FORM_STATE` → returns EDSS step
- OCR: pixel-level zone analysis on uploaded/captured images
- Print: CSS `@page A4` rules produce 2-page Neurostatus layout

---

## Key FORM_STATE keys

Visual, Brainstem, Pyramidal, Cerebellar, Sensory, BB, Cerebral fields + ambulation.
See inline comments in `index.html` for full list.

---

## Known bugs fixed (last session)

1. BB catheterisation FS: was =2, now =3 minimum
2. Ambulation null distance: unilateral/bilateral without distance returned null → EDSS 0 (fixed to conservative default)
3. OCR empty page noise: threshold raised 2%→5%, luminance 80→60
4. Clone selector: was `.sc-img-preview-wrap`, now `[id^='sc-img-preview']`
5. `amb_distance_measured` duplicate ID in two sections
6. Print was 4 pages → now correctly 2 pages
7. "undefined" in print: section-header hidden in print mode
