// Service Worker for Códigos de Contenedores aerococina
// Strategy: cache-first with network fallback + auto-update when online

const CACHE_VERSION = 'codigos-v1.1-2026-05-17';
const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

// INSTALL: pre-cache core app shell
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then(cache => {
        // Don't fail install if some optional assets are missing
        return Promise.all(
          CORE_ASSETS.map(url =>
            cache.add(url).catch(err => console.log('Skip cache:', url, err.message))
          )
        );
      })
      .then(() => self.skipWaiting())
  );
});

// ACTIVATE: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(names => Promise.all(
        names.filter(name => name !== CACHE_VERSION)
             .map(name => caches.delete(name))
      ))
      .then(() => self.clients.claim())
  );
});

// FETCH: cache-first for static assets, network-first for HTML
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET requests
  if (req.method !== 'GET') return;

  // Skip cross-origin requests (fonts CDN handled by browser cache)
  if (url.origin !== self.location.origin) return;

  // QR images & PNG assets: cache-first (rarely change)
  if (url.pathname.match(/\.(png|jpg|jpeg|svg|webp|ico)$/i) ||
      url.pathname.includes('qr_bodegas/')) {
    event.respondWith(
      caches.match(req).then(cached => {
        if (cached) return cached;
        return fetch(req).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_VERSION).then(cache => cache.put(req, clone));
          }
          return response;
        }).catch(() => cached || new Response('', { status: 404 }));
      })
    );
    return;
  }

  // HTML & other: network-first with cache fallback (fresh content when online)
  event.respondWith(
    fetch(req)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_VERSION).then(cache => cache.put(req, clone));
        }
        return response;
      })
      .catch(() => caches.match(req).then(cached => cached || caches.match('./index.html')))
  );
});

// MESSAGE: allow page to trigger immediate update
self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
