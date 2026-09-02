var CACHE_NAME = 'meow-ocr-v1';
var CORE_ASSETS = [
  '/',
  '/static/style.css',
  '/static/manifest.json',
  '/static/favicon.png'
];

self.addEventListener('install', function (event) {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(CORE_ASSETS).catch(function () {});
    })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (key) {
        if (key !== CACHE_NAME) {
          return caches.delete(key);
        }
      }));
    }).then(function () {
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET') {
    return;
  }
  var url = req.url;
  if (url.indexOf('/api/') > -1 || url.indexOf('/progress/') > -1 || url.indexOf('/handwrite') > -1) {
    return;
  }
  event.respondWith(
    fetch(req).then(function (res) {
      var copy = res.clone();
      caches.open(CACHE_NAME).then(function (cache) {
        cache.put(req, copy).catch(function () {});
      });
      return res;
    }).catch(function () {
      return caches.match(req).then(function (hit) {
        return hit || caches.match('/');
      });
    })
  );
});