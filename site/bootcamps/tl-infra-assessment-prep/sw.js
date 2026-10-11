/* sw.js — offline-first service worker for tl-infra-assessment-prep CBT.
 * Cache-first for the bootcamp's own assets; network-first for /api/*. */
'use strict';
var CACHE = 'tl-infra-prep-v5';
var ASSETS = [
  './',
  './index.html',
  './app.min.js',
  './infra-ai-bridge.js',
  './sw.js',
  './content.json',
  './tools/drill-data.json',
  './tools/subnet-calculator.html',
  './tools/muscle-memory-drills.html',
  './sims/ios-cli.js',
  './sims/terminal-mastery.html',
  './sims/proxmox-sim.html',
  './sims/fortigate-sim.html',
  './sims/paloalto-sim.html',
  './sims/git-simulator.html',
  './sims/vlan-basics.html',
  './sims/static-routing.html',
  './sims/inter-vlan-routing.html',
  './sims/dhcp-server.html',
  './sims/nat-pat.html',
  './sims/site-to-site-vpn.html',
  './diagrams/index.html',
  './diagrams/network-topology.svg',
  './diagrams/vlan-trunking.svg',
  './diagrams/ad-ou-hierarchy.svg',
  './diagrams/vpn-tunnel.svg',
  './diagrams/raid-levels.svg',
  './diagrams/hyperv-switches.svg',
  './diagrams/dns-resolution.svg',
  './diagrams/dhcp-dora.svg',
  './diagrams/sql-backup-chain.svg',
  './visuals/index.html',
  './visuals/tcp-handshake.svg',
  './visuals/kerberos-flow.svg',
  './visuals/osi-model.svg',
  './visuals/stp-convergence.svg',
  './visuals/gpo-precedence.svg',
  './visuals/backup-restore-flow.svg',
  './visuals/dhcp-vs-static.svg',
  './visuals/firewall-rule-flow.svg',
  './visuals/subnet-splitter.html',
  './visuals/raid-simulator.html',
  './visuals/vlan-explorer.html',
  './visuals/kerberos-explorer.html'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(ASSETS.map(function (u) { return new Request(u, { cache: 'reload' }); }))
        .catch(function () { /* best effort: cache what we can */ });
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
  if (url.origin !== self.location.origin && !isApi(req.url)) return; // leave CDN/absolute alone

  if (isApi(req.url)) {
    // network-first for API (progress sync), no caching
    e.respondWith(
      fetch(req).catch(function () {
        return new Response(JSON.stringify({ ok: false, offline: true }), {
          status: 503, headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }
  // Network-first for data files (content.json must always be fresh)
  // Cache-first for static assets (JS, CSS, images)
  var isDataFile = /content\.json$/.test(url.pathname);
  if (isDataFile) {
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
  // cache-first for static assets
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
