# AutoEDSSguide — Deployment Guide

A single self-contained HTML file (~89 KB) implementing the full EDSS Structured Roadmap with real-time scoring, print-friendly Neurostatus output, and offline-capable browser storage.

## What's inside

- **Pure-frontend app** — no server, no build step, no dependencies to install. The whole thing is one `index.html`.
- **JavaScript scoring engine** ported 1:1 from `edss_calc.py` (94 parity tests + 18 end-to-end UI tests, all passing).
- **Algorithm sources** — Kappos Neurostatus 2011 + Fouad et al. 2023 (DOI: 10.1177/20552173231155055).
- **Live recalculation** — every input change updates each FS score, the section pills, and the final EDSS step in the header.
- **Print / PDF** — the *Print* button opens the browser print dialog showing a clean Neurostatus-style scoring sheet (use *Save as PDF* in the destination dropdown).
- **Local persistence** — *Save / Load* uses `localStorage` (data stays in this browser only). *Export / Import JSON* lets you move data between devices.
- **Mobile-responsive** — the layout collapses on narrow screens; tabs scroll horizontally.

## Files

```
index.html        ← the entire app (deploy this)
```

That's it. Open it locally by double-clicking, or deploy it as a static page.

---

## Option A — GitHub Pages (free, recommended)

1. Create a new public repo on GitHub (e.g. `autoedssguide`).
2. Upload `index.html` to the repo root.
3. In the repo, go to **Settings → Pages**.
4. Under *Source*, select branch `main` and folder `/ (root)`. Click **Save**.
5. Wait ~30 s. The page goes live at:
   ```
   https://YOUR-USERNAME.github.io/autoedssguide/
   ```

Updating the app later: just commit a new `index.html` to the same repo — Pages redeploys automatically.

### Custom domain (optional)
Add a `CNAME` file with your domain (e.g. `edss.example.org`), then set a CNAME DNS record pointing at `YOUR-USERNAME.github.io`.

---

## Option B — Netlify (free, drag-and-drop)

1. Sign in at https://app.netlify.com/ (GitHub or email).
2. On the Sites page, drag the folder containing `index.html` onto the page.
3. Netlify gives you a URL like `https://lucky-lebkuchen-12345.netlify.app/` immediately.
4. **Site settings → Change site name** to pick a friendlier subdomain.

To update later: drag a new folder onto **Deploys → Drag & drop**.

---

## Option C — Cloudflare Pages (free, fast CDN)

1. Sign in at https://dash.cloudflare.com/.
2. **Workers & Pages → Create → Pages → Upload assets**.
3. Drop the folder containing `index.html`. Click **Deploy site**.
4. URL: `https://YOUR-PROJECT.pages.dev/`.

---

## Option D — Run it locally (no internet)

Just open `index.html` directly in any modern browser:

```bash
# macOS / Linux
open index.html       # macOS
xdg-open index.html   # most Linux

# Windows
start index.html
```

Or run a tiny local server (useful for testing print on iOS Safari, since `file://` blocks some features):

```bash
# Python (any 3.x)
python3 -m http.server 8000
# then visit http://localhost:8000/

# Node.js
npx serve .
```

The app works offline once loaded — only Google Fonts is fetched on first visit and the browser caches it. If you need full offline (no font fetch), the app falls back gracefully to system fonts.

---

## Using the app

1. **Patient tab** — enter ID, dates, rater.
2. **Ambulation tab** — pick the AS (0–12). For EDSS ≥ 4.0 this is the dominant input.
3. **Visual / Brainstem / Pyramidal / Cerebellar / Sensory / B&B / Cerebral** — fill the items as you examine. The FS pill in each tab updates live; the EDSS readout in the header updates after every change.
4. **Summary & Print tab** — review all FS scores and the final EDSS, then click **Print / Export to PDF**.

### Tips
- The header always shows the live EDSS step. You can fill the form in any order.
- *Save to browser* → *Load from browser* survives page refresh on the same device/browser.
- *Export JSON* → email/transfer the file → *Import JSON* on another device to move a half-completed assessment.
- Print uses `@page A4`; in Chrome/Edge use **More settings → Paper size: A4** if it defaults to Letter.

### Browser compatibility
- Chrome, Edge, Safari, Firefox — all current versions.
- iOS Safari ≥ 16 / Android Chrome — fully responsive; printing to PDF works via the share sheet.

---

## Verifying the build

If you want to re-run the test suite:

```bash
# Engine parity (94 tests, requires Node 18+)
node test_engine.js
# → "94 passed, 0 failed"

# End-to-end DOM (18 tests, requires jsdom)
npm i jsdom
node e2e_test.js
# → "18 passed, 0 failed"
```

---

## Disclaimer

This tool is for **clinical educational use**. The implementation follows published Neurostatus / Fouad et al. algorithms, but the final EDSS step is the responsibility of the rater's clinical judgement. Validate locally before any research or trial use.
