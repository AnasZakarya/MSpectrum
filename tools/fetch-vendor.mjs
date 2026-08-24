#!/usr/bin/env node
/*
 * fetch-vendor.mjs - download and self-host MSpectrum's third-party libraries.
 *
 * Purpose: pull the export + OCR libraries from npm at their pinned versions
 * into ./vendor and ./fonts, so the app can run fully offline with no CDN
 * requests (privacy + supply-chain hardening for clinical use).
 *
 * Usage:   node tools/fetch-vendor.mjs
 * Needs:   network access to the npm registry, `npm` on PATH, Node 18+.
 *
 * After running, the EXPORT libs are drop-in. To finish self-hosting the OCR
 * libs you must also re-point the loaders in index.html (documented at the
 * bottom of this file) and browser-test the Sheet Scanner.
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, copyFileSync, existsSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const ROOT = process.cwd();
const VENDOR = join(ROOT, 'vendor');
const FONTS = join(ROOT, 'fonts');
mkdirSync(VENDOR, { recursive: true });
mkdirSync(FONTS, { recursive: true });

// package spec -> [ [fileInsideTarball, destPath], ... ]
const JOBS = [
  ['html2canvas@1.4.1', [['package/dist/html2canvas.min.js', join(VENDOR, 'html2canvas.min.js')]]],
  ['jspdf@2.5.1', [['package/dist/jspdf.umd.min.js', join(VENDOR, 'jspdf.umd.min.js')]]],
  ['html2pdf.js@0.10.1', [['package/dist/html2pdf.bundle.min.js', join(VENDOR, 'html2pdf.bundle.min.js')]]],
  // --- OCR libs (uncomment to vendor; then re-point loaders, see notes below) ---
  // ['tesseract.js@5.1.0', [['package/dist/tesseract.min.js', join(VENDOR, 'tesseract.min.js')]]],
  // ['pdfjs-dist@3.11.174', [
  //   ['package/build/pdf.min.js', join(VENDOR, 'pdf.min.js')],
  //   ['package/build/pdf.worker.min.js', join(VENDOR, 'pdf.worker.min.js')],
  // ]],
  // onnxruntime-web and opencv.js ship many wasm/data files; vendor their whole
  // dist/ folders and set ort.env.wasm.wasmPaths / the opencv.js URL to local.
];

function fetchInto(spec) {
  const work = mkdtempSync(join(tmpdir(), 'mspv-'));
  const tgz = execFileSync('npm', ['pack', spec, '--silent'], { cwd: work, encoding: 'utf8' }).trim().split('\n').pop();
  execFileSync('tar', ['-xzf', tgz], { cwd: work });
  return work;
}

for (const [spec, files] of JOBS) {
  process.stdout.write(`* ${spec} ... `);
  try {
    const work = fetchInto(spec);
    for (const [src, dest] of files) {
      const p = join(work, src);
      if (!existsSync(p)) throw new Error(`missing ${src}`);
      copyFileSync(p, dest);
    }
    console.log('ok');
  } catch (e) {
    console.log('FAILED:', e.message);
  }
}

console.log(`\nDone. vendor/ now has:`);
for (const f of readdirSync(VENDOR)) console.log('  ' + f);

console.log(`
To fully self-host OCR (index.html), after vendoring the OCR libs above:
  1. scLoadTesseract(): replace the 3 CDN URLs with "vendor/tesseract.min.js".
  2. pdfjsLib.GlobalWorkerOptions.workerSrc = "vendor/pdf.worker.min.js"; and
     load "vendor/pdf.min.js".
  3. ort.env.wasm.wasmPaths = "vendor/ort/"; (vendor onnxruntime-web dist there)
  4. _ocr2EnsureLib("vendor/opencv.js", ...) (vendor opencv.js locally)
  5. Drop the now-unused CDN origins from the index.html <meta> CSP.
  6. Browser-test the Sheet Scanner end to end before deploying.
`);
