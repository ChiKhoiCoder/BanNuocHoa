/**
 * PWA Service Worker
 */

const CACHE_NAME = 'perfume-shop-v2';
const urlsToCache = [
    '/',
    '/static/css/base.css',
    '/static/css/cart.css',
    '/static/css/checkout.css',
    '/static/js/cart.js',
    '/static/js/checkout.js',
    '/static/js/ui-enhancements.js',
    '/static/images/logo.png',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
    self.skipWaiting();
});

// Fetch event
self.addEventListener('fetch', event => {
    const req = event.request;
    if (req.method !== 'GET') return;

    const url = new URL(req.url);
    const isHTML = req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html');
    const isStatic = url.pathname.startsWith('/static/') || url.origin !== self.location.origin;

    // Always prefer network for HTML navigations to avoid stale pages.
    if (isHTML) {
        event.respondWith(
            fetch(req).catch(() => caches.match(req))
        );
        return;
    }

    // Cache-first for static assets, network fallback.
    if (isStatic) {
        event.respondWith(
            caches.match(req).then((cached) => {
                if (cached) return cached;
                return fetch(req).then((res) => {
                    if (!res || res.status !== 200) return res;
                    const copy = res.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
                    return res;
                });
            })
        );
        return;
    }

    // Network-first for other same-origin GET requests.
    event.respondWith(
        fetch(req)
            .then((res) => {
                if (!res || res.status !== 200 || res.type !== 'basic') return res;
                const copy = res.clone();
                caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
                return res;
            })
            .catch(() => caches.match(req))
    );
});

// Activate event
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});
