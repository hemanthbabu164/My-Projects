# Offline-First Version Enhancement

## Overview
This document outlines how to enhance the todo app for offline-first functionality using IndexedDB and Service Workers.

## Implementation Strategy

### 1. IndexedDB Implementation

Create `static/db.js`:

```javascript
class TodoDB {
    constructor() {
        this.dbName = 'TodoAppDB';
        this.version = 1;
        this.db = null;
    }

    async init() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // Tasks store
                if (!db.objectStoreNames.contains('tasks')) {
                    const taskStore = db.createObjectStore('tasks', { keyPath: 'id', autoIncrement: true });
                    taskStore.createIndex('category_id', 'category_id', { unique: false });
                    taskStore.createIndex('completed', 'completed', { unique: false });
                    taskStore.createIndex('priority', 'priority', { unique: false });
                    taskStore.createIndex('due_date', 'due_date', { unique: false });
                }
                
                // Categories store
                if (!db.objectStoreNames.contains('categories')) {
                    const categoryStore = db.createObjectStore('categories', { keyPath: 'id', autoIncrement: true });
                    categoryStore.createIndex('name', 'name', { unique: true });
                }
                
                // Sync queue store (for when back online)
                if (!db.objectStoreNames.contains('syncQueue')) {
                    db.createObjectStore('syncQueue', { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    }
    
    async addTask(task) {
        const transaction = this.db.transaction(['tasks'], 'readwrite');
        const store = transaction.objectStore('tasks');
        return store.add(task);
    }
    
    async getAllTasks() {
        const transaction = this.db.transaction(['tasks'], 'readonly');
        const store = transaction.objectStore('tasks');
        return new Promise((resolve, reject) => {
            const request = store.getAll();
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    async updateTask(task) {
        const transaction = this.db.transaction(['tasks'], 'readwrite');
        const store = transaction.objectStore('tasks');
        return store.put(task);
    }
    
    async deleteTask(id) {
        const transaction = this.db.transaction(['tasks'], 'readwrite');
        const store = transaction.objectStore('tasks');
        return store.delete(id);
    }
    
    // Similar methods for categories...
    
    async addToSyncQueue(operation) {
        const transaction = this.db.transaction(['syncQueue'], 'readwrite');
        const store = transaction.objectStore('syncQueue');
        return store.add({
            operation: operation.type, // 'create', 'update', 'delete'
            data: operation.data,
            timestamp: new Date(),
            synced: false
        });
    }
}
```

### 2. Service Worker for Caching

Create `static/sw.js`:

```javascript
const CACHE_NAME = 'todo-app-v1';
const urlsToCache = [
    '/',
    '/static/style.css',
    '/static/script.js',
    '/static/db.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            }
        )
    );
});

// Background sync for offline changes
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(syncOfflineChanges());
    }
});

async function syncOfflineChanges() {
    // Sync pending changes when back online
    // Implementation would read from IndexedDB sync queue
}
```

### 3. Enhanced Script Integration

Add to `static/script.js`:

```javascript
// Offline support initialization
let isOnline = navigator.onLine;
let dbInstance = null;

async function initOfflineSupport() {
    // Initialize IndexedDB
    dbInstance = new TodoDB();
    await dbInstance.init();
    
    // Register service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js');
    }
    
    // Listen for online/offline events
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
}

function handleOffline() {
    isOnline = false;
    showNotification('You are offline. Changes will sync when connection is restored.', 'warning');
}

async function handleOnline() {
    isOnline = true;
    showNotification('Connection restored. Syncing changes...', 'info');
    await syncOfflineChanges();
}

// Modified API calls to use IndexedDB when offline
async function apiCallWithOfflineSupport(endpoint, method = 'GET', data = null) {
    if (isOnline) {
        try {
            return await apiCall(endpoint, method, data);
        } catch (error) {
            // If network fails, fall back to offline mode
            isOnline = false;
            return await handleOfflineRequest(endpoint, method, data);
        }
    } else {
        return await handleOfflineRequest(endpoint, method, data);
    }
}

async function handleOfflineRequest(endpoint, method, data) {
    // Handle requests using IndexedDB
    if (endpoint.includes('/tasks')) {
        if (method === 'GET') {
            return await dbInstance.getAllTasks();
        } else if (method === 'POST') {
            const task = { ...data, id: Date.now(), created_at: new Date() };
            await dbInstance.addTask(task);
            await dbInstance.addToSyncQueue({ type: 'create', data: task });
            return task;
        }
        // Handle other methods...
    }
}
```

## Benefits

1. **True Offline Functionality**: App works completely offline
2. **Data Persistence**: No data loss when offline
3. **Automatic Sync**: Changes sync automatically when back online
4. **Performance**: Faster loading with cached resources
5. **Progressive Enhancement**: Graceful degradation for older browsers

## Implementation Steps

1. Add IndexedDB wrapper (`db.js`)
2. Implement Service Worker (`sw.js`) 
3. Modify existing JavaScript to use offline capabilities
4. Add online/offline status indicators to UI
5. Implement conflict resolution for sync scenarios
6. Add comprehensive error handling

This approach ensures your todo app works seamlessly regardless of network connectivity.
