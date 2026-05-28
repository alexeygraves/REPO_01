const CACHE = 'app-cache-v1';
const PRECACHE = ['/', '/index.html'];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE).then(c => c.addAll(PRECACHE))
    );
    self.skipWaiting();
});

// on activate — drop old cache versions so users don't get stale assets
self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', e => {
    const { request } = e;

    if (request.method !== 'GET' || request.url.includes('/api/')) return;

    e.respondWith(
        caches.match(request).then(cached => {
            const netFetch = fetch(request).then(res => {
                if (res.ok) {
                    const copy = res.clone();
                    caches.open(CACHE).then(c => c.put(request, copy));
                }
                return res;
            });

            // for page navigations prefer network, fall back to cache
            if (request.mode === 'navigate') {
                return netFetch.catch(() => cached || caches.match('/index.html'));
            }

            return cached || netFetch;
        })
    );
});
