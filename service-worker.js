const assets = [
    "./static/assets/backs/*.jpg",
    "./templates/min/index.min.html",
    "./static/css/min/index.min.css",
    "./static/assets/decks/fr1/*.jpg",
    "./static/assets/decks/fr2/*.jpg",
    "./static/assets/decks/ita/*.jpg",
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