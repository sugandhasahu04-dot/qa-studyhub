// QA StudyHub service worker: makes the site installable and usable with a weak connection.
// Pages: network first (always fresh data), fall back to the last saved copy, then an offline page.
// Static files (CSS, JS, icons): served from cache instantly, refreshed in the background (stale-while-revalidate).
const VERSION = 'studyhub-v4';
const STATIC = ['/static/style.css', '/static/runner.js', '/static/viz.js', '/static/sample_db.sql',
  '/static/icons/icon-192.png', '/offline'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(STATIC)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin || url.pathname.startsWith('/api/')) return;

  if (url.pathname.startsWith('/static/')) {
    e.respondWith(caches.match(req).then(hit => {
      const fresh = fetch(req).then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); }
        return res;
      }).catch(() => hit);
      return hit || fresh;
    }));
    return;
  }

  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(res => {
      if (res.ok && !res.redirected) { const copy = res.clone(); caches.open(VERSION).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req).then(hit => hit || caches.match('/offline'))));
  }
});
