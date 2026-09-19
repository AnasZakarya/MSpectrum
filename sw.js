/* MSpectrum service worker - NETWORK-FIRST.
   Always serves the freshest version when online (so deployed changes show immediately);
   falls back to the cached copy only when there is no connection. Bump CACHE to force-clear. */
const CACHE = "mspectrum-v9";
const CORE = [
  "./", "./index.html", "./scores.html", "./mcdonald.html", "./manifest.webmanifest",
  "./mspectrum-logo.svg", "./favicon.svg",
  "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png",
  // self-hosted fonts (correct typography offline)
  "./fonts/fraunces-standard-normal.woff2", "./fonts/ibm-plex-sans-wght-normal.woff2",
  "./fonts/ibm-plex-mono-400-normal.woff2",
  // self-hosted export libraries (PDF/image export offline)
  "./vendor/html2canvas.min.js", "./vendor/jspdf.umd.min.js", "./vendor/html2pdf.bundle.min.js"
];

self.addEventListener("install", function (e) {
  self.skipWaiting();
  // Pre-cache every tool + asset individually, so one missing file never blocks the rest.
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return Promise.all(CORE.map(function (u) { return c.add(u).catch(function () {}); }));
  }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) { if (k !== CACHE) return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  e.respondWith(
    fetch(req).then(function (res) {
      try {
        if (res && res.status === 200 && new URL(req.url).origin === self.location.origin) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(req, copy); }).catch(function () {});
        }
      } catch (_) {}
      return res;
    }).catch(function () {
      // Offline: serve the cached copy. Only page navigations fall back to the app shell;
      // a failed script/asset request must not receive HTML.
      return caches.match(req).then(function (m) {
        if (m) return m;
        if (req.mode === "navigate") return caches.match("./index.html");
        return Response.error();
      });
    })
  );
});
