const CACHE_NAME = 'youtube-transcript-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-192.png',
  '/icon-512.png'
];

// Install Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache.filter(url => url !== '/'));
      })
      .catch((error) => {
        console.log('Cache addAll failed:', error);
      })
  );
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch Event - Network First Strategy
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip external requests (YouTube API, etc.)
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Check if valid response
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }

        // Clone the response
        const responseToCache = response.clone();

        caches.open(CACHE_NAME)
          .then((cache) => {
            cache.put(event.request, responseToCache);
          });

        return response;
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(event.request)
          .then((response) => {
            if (response) {
              return response;
            }
            
            // Return offline page for navigation requests
            if (event.request.mode === 'navigate') {
              return caches.match('/index.html');
            }
          });
      })
  );
});

// Background Sync for offline transcript saving
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-transcript-save') {
    event.waitUntil(doBackgroundSync());
  }
});

async function doBackgroundSync() {
  try {
    // Get pending transcripts from IndexedDB
    const pendingTranscripts = await getPendingTranscripts();
    
    for (const transcript of pendingTranscripts) {
      try {
        // Attempt to process transcript
        await processTranscript(transcript);
        // Remove from pending list on success
        await removePendingTranscript(transcript.id);
      } catch (error) {
        console.log('Failed to process transcript:', error);
      }
    }
  } catch (error) {
    console.log('Background sync failed:', error);
  }
}

// IndexedDB helpers for offline functionality
async function getPendingTranscripts() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('TranscriptDB', 1);
    
    request.onerror = () => reject(request.error);
    
    request.onsuccess = () => {
      const db = request.result;
      const transaction = db.transaction(['pending'], 'readonly');
      const store = transaction.objectStore('pending');
      const getAllRequest = store.getAll();
      
      getAllRequest.onsuccess = () => resolve(getAllRequest.result);
      getAllRequest.onerror = () => reject(getAllRequest.error);
    };
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('pending')) {
        db.createObjectStore('pending', { keyPath: 'id' });
      }
    };
  });
}

async function removePendingTranscript(id) {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('TranscriptDB', 1);
    
    request.onsuccess = () => {
      const db = request.result;
      const transaction = db.transaction(['pending'], 'readwrite');
      const store = transaction.objectStore('pending');
      const deleteRequest = store.delete(id);
      
      deleteRequest.onsuccess = () => resolve();
      deleteRequest.onerror = () => reject(deleteRequest.error);
    };
  });
}

async function processTranscript(transcript) {
  // This would handle the actual transcript processing
  // For now, just simulate processing
  console.log('Processing transcript:', transcript);
  return Promise.resolve();
}

// Push notification handling
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'تم تحديث التطبيق',
    icon: '/icon-192.png',
    badge: '/icon-72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: 'فتح التطبيق',
        icon: '/icon-192.png'
      },
      {
        action: 'close',
        title: 'إغلاق',
        icon: '/icon-192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('مستخرج نصوص اليوتيوب', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('Notification click received.');

  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handling from main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_TRANSCRIPT') {
    // Cache transcript data for offline access
    const transcriptData = event.data.payload;
    event.waitUntil(
      caches.open(CACHE_NAME).then((cache) => {
        // Store transcript as a synthetic response
        const response = new Response(JSON.stringify(transcriptData), {
          headers: { 'Content-Type': 'application/json' }
        });
        return cache.put(`/transcript/${transcriptData.videoId}`, response);
      })
    );
  }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'transcript-cleanup') {
    event.waitUntil(cleanupOldTranscripts());
  }
});

async function cleanupOldTranscripts() {
  try {
    const cache = await caches.open(CACHE_NAME);
    const keys = await cache.keys();
    const now = Date.now();
    const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days

    for (const key of keys) {
      if (key.url.includes('/transcript/')) {
        const response = await cache.match(key);
        const data = await response.json();
        
        if (now - data.timestamp > maxAge) {
          await cache.delete(key);
          console.log('Deleted old transcript:', key.url);
        }
      }
    }
  } catch (error) {
    console.log('Cleanup failed:', error);
  }
}

// Handle app update
self.addEventListener('install', (event) => {
  // Skip waiting to activate new version immediately
  self.skipWaiting();
});

// Send update available message to clients
self.addEventListener('controllerchange', () => {
  self.clients.matchAll().then(clients => {
    clients.forEach(client => {
      client.postMessage({ type: 'APP_UPDATED' });
    });
  });
});