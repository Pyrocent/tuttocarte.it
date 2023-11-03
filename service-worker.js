const assets = [
    "/",
    "static/assets/",
    "/templates/min/index.min.html",
    "/static/css/min/index.min.css",
    "https://fonts.googleapis.com/css2?family=Outfit&display=swap"
];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open("cache")
            .then(cache => {
                return cache.addAll(assets);
            })
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
    );
});