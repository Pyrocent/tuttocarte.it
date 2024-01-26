// const CACHE_NAME = "v1";
// const assets = [
//     "/manifest.json",
//     "/service-worker.js",
//     "/templates/index.html",
//     "/static/css/index.css",
//     "/static/assets/favicon.ico",
//     "/static/assets/backs/*.jpg",
//     "/static/assets/fiches/*.png",
//     "/static/assets/decks/fr1/*.jpg",
//     "/static/assets/decks/fr2/*.jpg",
//     "/static/assets/decks/ita/*.jpg",
//     "https://fonts.googleapis.com/css2?family=Outfit&display=swap"
// ];

// self.addEventListener("install", event => {
//     event.waitUntil(
//         caches.open(CACHE_NAME)
//             .then(cache => cache.addAll(assets))
//             .catch(err => console.error("Failed to cache", err))
//     );
// });

// self.addEventListener("activate", event => {
//     event.waitUntil(
//         caches.keys().then(keyList => {
//             return Promise.all(keyList.map(key => {
//                 if (key !== CACHE_NAME) {
//                     return caches.delete(key);
//                 }
//             }));
//         })
//     );
// });

// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request).then(async fetchRes => {
//                     const cache = await caches.open(CACHE_NAME);
//                     cache.put(event.request.url, fetchRes.clone());
//                     return fetchRes;
//                 });
//             })
//             .catch(() => caches.match("/templates/offline.html"))
//     );
// });