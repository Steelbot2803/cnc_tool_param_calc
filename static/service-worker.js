self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open('cnc-toolcalc-v1').then(function (cache) {
            return cache.addAll([
                '/',
                '/static/icon-192.png',
                '/static/icon-512.png',
                '/static/manifest.json'
            ]);
        })
    );
});

self.addEventListener('fetch', function (e) {
    e.respondWith(
        caches.match(e.request).then(function (response) {
            return response || fetch(e.request);
        })
    );
});
