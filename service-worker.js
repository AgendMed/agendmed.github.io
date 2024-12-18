const CACHE_NAME = "agend-med-cache-v2.1";
const URLS_TO_CACHE = [
    "./",
    "./img/Logo-Azul-AgendMed.png",
    "./img/Logo-branca-AgendMed.png",
    "./img/calendario.png",
    "./img/news.png",
    "./img/ticket.png",
    "./app.js",
    "./cadastro.css",
    "./cadastro.html",
    "./index.html",
    "./login.css",
    "./login.html",
    "./login.js",
    "./manifest.json",
    "./onboarding.css",
    "./onboarding.html",
    "./onboarding.js",
    "./Pre_Login.css",
    "./scripts.js",
    "./service-worker.js",
    "./style.css",
    "./user.html",
    "./user.css",
    "./perfil.js"
];

// Evento de instalação do Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log("Arquivos em cache");
                return cache.addAll(URLS_TO_CACHE);
            })
            .then(() => self.skipWaiting())
    );
});

// Evento de ativação do Service Worker
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        console.log("Cache antigo removido");
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Evento de busca (fetch) para capturar as requisições
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Retorna o recurso do cache se encontrado, caso contrário, faz uma requisição de rede
                return response || fetch(event.request)
                    .then(networkResponse => {
                        // Cacheia o recurso novo
                        return caches.open(CACHE_NAME).then(cache => {
                            cache.put(event.request, networkResponse.clone());
                            return networkResponse;
                        });
                    });
            })
            .catch(() => {
                // Exibe uma mensagem ou uma página alternativa se o recurso não estiver no cache e não houver conexão
                if (event.request.mode === 'navigate') {
                    return caches.match('/index.html');
                }
            })
    );
}); 