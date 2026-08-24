# Privacy and HIPAA-conscious use

> **Plain statement:** HIPAA compliance is a property of an *organization and its
> workflows*, not of a piece of software. No web app can be "HIPAA compliant" by
> itself. What MSpectrum can do - and does - is stay out of the way of
> compliance: it is built so that **protected health information (PHI) never
> leaves the clinician's device**, which removes most of the ways a tool like
> this would otherwise create HIPAA risk.

## Why the design is HIPAA-friendly

- **No transmission.** MSpectrum is a static, client-side app. Patient data
  entered into it is not uploaded, logged, or sent to any server (the authors',
  the host's, or a third party's). There is no analytics or tracking.
- **No third party receives PHI.** Fonts and the PDF/export libraries are
  self-hosted. The optional OCR libraries run in the browser and receive no data.
- **No server, no server-side PHI store, no server logs of PHI.** When you self
  host, the server only ships static files; it never sees what a user types.
- **You stay in control of exports.** PDF/JSON/CSV are written to the user's own
  device only.

Because no PHI reaches the hosting server, hosting MSpectrum (on GitHub Pages,
Netlify, Cloudflare Pages, or your own server) does **not** require a Business
Associate Agreement with the host *for the app's function* - the host never
processes PHI on your behalf through this app.

## Where PHI can persist, and how to control it

1. **Browser memory** - cleared when the tab closes.
2. **`localStorage`** - only if the user presses **Save to browser**. This
   survives closing the tab and is readable by anyone with access to that OS
   user profile.
   - Use the new **Clear saved data** button to erase it, especially on shared
     or clinic computers.
   - Prefer **Export JSON** to a secured location over Save to browser when you
     need to keep a record.
3. **Exported files** - your responsibility once saved; store them per your
   organization's rules.

## Recommended practice for clinical use

- **Do not enter direct identifiers.** Use a non-identifying study/visit code
  instead of names or MRNs. The in-app notice says this; please follow it.
  (Note: the app currently offers a *Date of birth* field, which is itself an
  identifier - see `PROJECT-REVIEW-2026-08-23.md`, item on PHI fields.)
- On shared computers, press **Clear saved data** before leaving, or use a
  private/incognito window (which discards `localStorage` on close).
- Serve over **HTTPS** with the headers in `SECURITY.md` / `deploy/`.
- Keep devices patched and access-controlled - device security is the main
  remaining control, since that is where the data lives.

## What this document is not

This is not legal advice and not a certification. Each organization remains
responsible for its own HIPAA (or GDPR / local) obligations, including risk
analysis, workforce training, device and access management, and how exported
files are handled. MSpectrum is decision support; the clinician remains
responsible for the assessment and for lawful handling of any PHI.
