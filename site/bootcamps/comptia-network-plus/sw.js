/* _shell/sw.js — unified service worker for all CBTs.
 * Cache-first for shell assets; network-first for content.json (must always be fresh).
 * Each CBT registers this as ./sw.js (copied per-CBT at build time with its own cache name).
 * CACHE_NAME is replaced at copy time with 'cbt-<slug>-v1'.
 */
'use strict';
var CACHE = 'cbt-comptia-network-plus-v1'; // replaced per-CBT
var SHELL_ASSETS = [
  './',
  './index.html',
  './sw.js',
  './content.json',
  '../_shell/shell-core.js',
  '../_shell/ai-client.js',
  '../_shell/ai-dynamic.js',
  '../_shell/learn.js',
  '../_shell/ai-math.js',
  '../_shell/ai-reading.js',
  '../_shell/labs.js',
  '../_shell/simulations.js',
  '../_shell/terminal.js',
  '../_shell/ai-terminal.js',
  '../_shell/consoles.js',
  '../_shell/ai-coding.js',
  '../_shell/missions.js',
  '../_shell/chat.js',
  '../_shell/notes-bridge.js',
  '../_shell/shell.css',
  '../_shell/il-topic-themes.css',
  '../_shell/foundations.json',
  '../_shell/math.json'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(SHELL_ASSETS.map(function (u) { return new Request(u, { cache: 'reload' }); }))
        .catch(function () { /* best effort */ });
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

function isApi(url) { return url.indexOf('/api/') !== -1; }

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin && !isApi(req.url)) return;

  if (isApi(req.url)) {
    e.respondWith(
      fetch(req).catch(function () {
        return new Response(JSON.stringify({ ok: false, offline: true }), {
          status: 503, headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }
  // Network-first for content.json — must always be fresh
  if (/content\.json$/.test(url.pathname)) {
    e.respondWith(
      fetch(req).then(function (res) {
        if (res && res.ok) {
          var copy = res.clone();
          caches.open(CACHE).then(function (cache) { cache.put(req, copy); });
        }
        return res;
      }).catch(function () {
        return caches.match(req, { ignoreSearch: true });
      })
    );
    return;
  }
  // Cache-first for static assets
  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then(function (hit) {
      if (hit) return hit;
      return fetch(req).then(function (res) {
        if (res && res.ok) {
          var copy = res.clone();
          caches.open(CACHE).then(function (cache) { cache.put(req, copy); });
        }
        return res;
      }).catch(function () {
        if (req.mode === 'navigate') return caches.match('./index.html');
        throw new Error('offline');
      });
    })
  );
});
