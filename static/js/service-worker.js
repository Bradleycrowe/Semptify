const CACHE_NAME = 'semptify-cache-v1';
const CORE_ASSETS = [
  '/',
  '/static/css/app.css',
  '/static/manifest.webmanifest'
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
