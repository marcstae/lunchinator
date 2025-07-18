const CACHE_NAME = 'lunchinator-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting();
});

// Fetch event
self.addEventListener('fetch', event => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        
        return fetch(event.request).then(response => {
          // Don't cache non-successful responses
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });

          return response;
        }).catch(() => {
          // Return a fallback page when offline
          if (event.request.destination === 'document') {
            return caches.match('/index.html');
          }
        });
      })
  );
});

// Activate event
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Background sync for offline menu requests
self.addEventListener('sync', event => {
  if (event.tag === 'menu-sync') {
    event.waitUntil(syncMenuData());
  }
});

async function syncMenuData() {
  try {
    // Try to fetch latest menu data when back online
    const response = await fetch('/api/menu');
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      await cache.put('/api/menu', response);
      
      // Notify all clients about the update
      const clients = await self.clients.matchAll();
      clients.forEach(client => {
        client.postMessage({
          type: 'MENU_UPDATED',
          data: 'Menu data has been updated'
        });
      });
    }
  } catch (error) {
    console.log('Sync failed:', error);
  }
}

// Push notifications (for future use)
self.addEventListener('push', event => {
  if (event.data) {
    const data = event.data.json();
    
    const options = {
      body: data.body || 'Neues Menü verfügbar!',
      icon: '/icon-192x192.png',
      badge: '/badge-72x72.png',
      tag: 'menu-notification',
      renotify: true,
      actions: [
        {
          action: 'view',
          title: 'Menü anzeigen'
        },
        {
          action: 'dismiss',
          title: 'Schließen'
        }
      ]
    };

    event.waitUntil(
      self.registration.showNotification(data.title || 'Lunchinator', options)
    );
  }
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Periodic background sync (for browsers that support it)
self.addEventListener('periodicsync', event => {
  if (event.tag === 'menu-update') {
    event.waitUntil(syncMenuData());
  }
});
