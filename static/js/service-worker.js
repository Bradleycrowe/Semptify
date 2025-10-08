const CACHE_NAME = 'semptify-cache-v2';
const CORE_ASSETS = [
  '/',
  '/offline',
  '/static/css/app.css',
  '/static/manifest.webmanifest',
  '/version',
  '/health'
];
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(CORE_ASSETS))
  );
});
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))))
  );
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // HTML navigation fallback offline
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req).catch(() => caches.match('/offline'))
    );
    return;
  }
  e.respondWith(
    caches.match(req).then(cached => {
      const fetchPromise = fetch(req).then(networkResp => {
        if(networkResp && networkResp.status === 200){
          const cloned = networkResp.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, cloned));
        }
        return networkResp;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
