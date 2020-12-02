const cacheName = 'reach-pwa';
const cacheAssets = [
  // '../main.py',
  // './templates/base.html',
  // '../templates/index.html',
  '/style/stylesheet.css'
];

// call install event
self.addEventListener('install', e => {
  console.log('service worker: installed');

  e.waitUntil(
    caches
      .open(cacheName)
      .then(cache => {
        console.log('sw: caching')
        cache.addAll(cacheAssets);
      })
      .then(() => self.skipWaiting())
  )
})

// call activate event
self.addEventListener('activate', e => {
  console.log('service worker: activated');
  // remove umwanted caches
  e.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== cacheName) {
            console.log('sw: clearing old cache');
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

// call fetch event
self.addEventListener('fetch', e => {
  console.log('sw:Fetching')
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
});