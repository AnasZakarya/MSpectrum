# MSpectrum test tool

Zero-dependency regression tests. Run from `Codes/`:

```
npm test          # or: node tests/run.js
```

## What it checks
- **engine.test.js** — loads the EDSS engine straight out of `index.html`
  (via the `module.exports` hook) and runs a 64-case battery covering every
  Functional System, the visual/BB conversions, the FS-combination table, and
  the ambulation-score → EDSS mapping. Expected values follow the audited
  Neurostatus (Kappos 2011 / Fouad 2023) rules.
- **scorehub.test.js** — loads every inline script of `scores.html` under a DOM
  stub. Catches the "stray `,,`" class of crash that passes `node --check` but
  breaks the hub at runtime. Also verifies all 29 tools have a panel and that
  every `calc*()` runs on empty input without throwing.
- **mcdonald.test.js** — same load-without-throw check for `mcdonald.html`.

## After editing app code
Run `npm test` before deploying. Green = safe to upload. If you add a Score Hub
tool, the structural check will confirm it has a panel; add an engine assertion
when you change any FS rule.

## JS-Python parity

`python3 tests/parity_check.py [n]` scores random EDSS inputs (fixed seed) with the JS engine in `index.html` and with `edss_calc.py` and fails on any difference. `node tests/run.js` runs it too (2,000 cases) when python3 is installed.
