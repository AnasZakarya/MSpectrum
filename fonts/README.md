# Self-hosted fonts

These fonts are bundled with MSpectrum so the app renders its intended
typography **without contacting Google Fonts** (a privacy improvement for a
clinical tool, and it lets the app work fully offline). They replace the former
`<link>` to `fonts.googleapis.com`.

| File | Family | Axis / weight | Source package |
|---|---|---|---|
| `fraunces-standard-normal.woff2` | Fraunces | variable, opsz + wght 100-900 | `@fontsource-variable/fraunces` 5.3.0 |
| `fraunces-standard-italic.woff2` | Fraunces | variable italic (mcdonald) | same |
| `ibm-plex-sans-wght-normal.woff2` | IBM Plex Sans | variable wght 100-700 | `@fontsource-variable/ibm-plex-sans` 5.3.0 |
| `ibm-plex-sans-wght-italic.woff2` | IBM Plex Sans | variable italic (mcdonald) | same |
| `ibm-plex-mono-400/500/600-normal.woff2` | IBM Plex Mono | static 400/500/600 | `@fontsource/ibm-plex-mono` 5.3.0 |
| `ibm-plex-mono-400-italic.woff2` | IBM Plex Mono | static 400 italic (mcdonald) | same |

Only the **latin** subset is included to keep size small (~316 KB total).
`@font-face` rules are inlined in each HTML page (`<style id="mspectrum-fonts">`).

## Licensing

Both families are licensed under the **SIL Open Font License 1.1** (OFL), which
permits bundling and redistribution. Full texts:

- Fraunces: `Fraunces-OFL.txt` (c) The Fraunces Project Authors.
- IBM Plex Sans / Mono: `IBMPlex-OFL.txt` (c) IBM Corp.

## Updating

Re-run: `npm pack @fontsource-variable/fraunces @fontsource-variable/ibm-plex-sans @fontsource/ibm-plex-mono`,
then copy the `files/*-latin-*.woff2` you need here under the names above.
