const assets = [
    "app.webmanifest",
    "service-worker.js",
    "templates/min/index.min.html",
    "static/css/min/index.min.css",
    "static/assets/backs/*.jpg",
    "static/assets/decks/fr1/*.jpg",
    "static/assets/decks/fr2/*.jpg",
    "static/assets/decks/ita/*.jpg",
    "static/assets/fiches/*.jpg",
    "static/assets/favicon.png",
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