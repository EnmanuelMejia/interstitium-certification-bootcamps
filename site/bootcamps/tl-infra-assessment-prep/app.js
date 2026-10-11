/* ============================================================================
 * app.js — ThreatLocker IT Infrastructure Assessment Prep CBT application
 * Single-file, zero-dependency engine. Data-driven from content.json.
 * Interstitium Labs · 2026-10-10
 * ============================================================================
 */
'use strict';

/* ============================ 0. CONFIG ================================= */
var SLUG = 'tl-infra-assessment-prep';
var LS_KEY = 'tl-infra-prep-v1';
var LS_CONTENT_CACHE = 'tl-infra-prep-content-cache';
var API_ME = '/api/me';
var API_PROGRESS = '/api/progress';
var SYNC_DEBOUNCE_MS = 10000;

/* ============================ 1. UTILITIES ================================ */
function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
function $(sel, root) { return (root || document).querySelector(sel); }
function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
function pad2(n) { return (n < 10 ? '0' : '') + n; }
function fmtClock(totalSec) {
  totalSec = Math.max(0, Math.floor(totalSec));
  var h = Math.floor(totalSec / 3600), m = Math.floor((totalSec % 3600) / 60), s = totalSec % 60;
  return (h ? h + ':' + pad2(m) : m) + ':' + pad2(s);
}
function fmtSec(ms) { return (ms / 1000).toFixed(1) + 's'; }
function todayKey(d) {
  d = d || new Date();
  return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate());
}
function dayDiff(aKey, bKey) {
  var a = new Date(aKey + 'T12:00:00'), b = new Date(bKey + 'T12:00:00');
  return Math.round((b - a) / 86400000);
}
function debounce(fn, ms) {
  var t = null;
  return function () {
    var args = arguments, self = this;
    clearTimeout(t);
    t = setTimeout(function () { fn.apply(self, args); }, ms);
  };
}
function slugify(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
}
function shuffle(arr, rand) {
  var a = arr.slice(), i, j;
  for (i = a.length - 1; i > 0; i--) {
    j = Math.floor(rand() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}
function mulberry32(seed) {
  var a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    var t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function toast(msg) {
  var t = $('#toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._h);
  t._h = setTimeout(function () { t.classList.remove('show'); }, 2600);
}

/* ==================== 2. CONTENT LOADER + MODEL =========================== */
var Content = {
  raw: null,
  domains: [],        // study modules (excludes mock-assessment)
  mockDomain: null,
  domainById: {},
  lessons: [],        // {id, domain_id, title, concepts[], example, pitfalls[], try_it}
  lessonById: {},
  labs: [],           // {id, domain_id, ...}
  labById: {},
  scenarios: [],      // flattened {id, domain_id, ...}
  scenarioById: {},
  simulations: [],    // mock items
  mockMinutes: 180,
  behavioral: [],
  resources: null,
  media: [],
  drillData: null,
  title: '', tagline: '', disclaimer: ''
};

function labDomainFor(labId) {
  // Derived mapping from lab id prefix -> domain id (structural, not content).
  var id = String(labId);
  var map = [
    ['lab-ad-', 'windows-server-ad'],
    ['lab-gpo-', 'windows-server-ad'],
    ['lab-replication-fsmo', 'windows-server-ad'],
    ['lab-subnet-', 'networking'],
    ['lab-vlan-', 'networking'],
    ['lab-ipsec-', 'vpn'],
    ['lab-client-vpn-', 'vpn'],
    ['lab-hyperv-', 'hyperv'],
    ['lab-sql-', 'sql-server'],
    ['lab-raid-', 'storage-backup-dr'],
    ['lab-backup-', 'storage-backup-dr'],
    ['lab-pipeline-', 'powershell'],
    ['lab-remoting-', 'powershell'],
    ['lab-harden-', 'security-hardening'],
    ['lab-ransomware-', 'security-hardening'],
    ['lab-branch-office-handover-pack', 'documentation'],
    ['lab-powershell-pipeline', 'powershell'],
    ['lab-write-psfunction', 'powershell'],
    ['lab-pester-infra-test', 'powershell'],
    ['lab-network-diagnosis-cmd', 'networking'],
    ['lab-osi-troubleshooting', 'networking'],
    ['lab-static-route-and-arp', 'networking'],
    ['lab-draw-kerberos-sequence', 'windows-server-ad'],
    ['lab-event-log-forensics', 'windows-server-ad'],
    ['lab-diskpart-provision', 'windows-server-ad'],
    ['lab-windows-update-audit', 'windows-server-ad'],
    ['lab-write-sop', 'documentation'],
    ['lab-capstone-', 'capstone-build'],
    ['lab-api-integration', 'enterprise-skills'],
    ['lab-fortigate-policy', 'firewalls'],
    ['lab-paloalto-app-rule', 'firewalls'],
    ['lab-firewall-rule-deploy', 'firewalls'],
    ['lab-proxmox-deploy', 'platform-skills'],
    ['lab-git-workflow', 'platform-skills'],
    ['lab-linux-permissions', 'linux-fundamentals'],
    ['lab-linux-log-triage', 'linux-fundamentals'],
    ['lab-bash-automation', 'linux-fundamentals']
  ];
  for (var i = 0; i < map.length; i++) {
    if (id.indexOf(map[i][0]) === 0) return map[i][1];
  }
  return 'windows-server-ad';
}

function loadContent() {
  return fetch('content.json', { cache: 'no-cache' }).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function (data) {
    try { localStorage.setItem(LS_CONTENT_CACHE, JSON.stringify(data)); } catch (e) {}
    normalizeContent(data);
    return Content;
  }).catch(function (err) {
    // Offline fallback: last cached copy.
    try {
      var cached = localStorage.getItem(LS_CONTENT_CACHE);
      if (cached) {
        normalizeContent(JSON.parse(cached));
        showOfflineBanner(true);
        return Content;
      }
    } catch (e) {}
    throw err;
  });
}

function loadDrillData() {
  return fetch('tools/drill-data.json', { cache: 'no-cache' }).then(function (r) {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  }).then(function (data) {
    Content.drillData = data;
    return data;
  }).catch(function () {
    Content.drillData = { commands: [], sequences: [], error_recovery: [], daily_sets: [], sprint: { tasks: [] }, meta: {} };
    return Content.drillData;
  });
}

function asArray(x) { return Array.isArray(x) ? x : []; }
function normalizeContent(d) {
  Content.raw = d;
  Content.title = d.title || 'IT Infrastructure Assessment Prep';
  Content.tagline = d.tagline || '';
  Content.disclaimer = d.disclaimer || '';
  Content.domains = [];
  Content.domainById = {};
  asArray(d.domains).forEach(function (dom) {
    if (dom.id === 'mock-assessment') { Content.mockDomain = dom; return; }
    Content.domains.push(dom);
    Content.domainById[dom.id] = dom;
    (dom.scenarios || []).forEach(function (sc) { sc.domain_id = dom.id; });
  });
  Content.lessons = [];
  Content.lessonById = {};
  asArray(d.lessons).forEach(function (l, idx) {
    var id = 'lesson-' + l.domain_id + '-' + idx;
    l._id = id;
    Content.lessons.push(l);
    Content.lessonById[id] = l;
  });
  Content.labs = [];
  Content.labById = {};
  asArray(d.labs).forEach(function (lab) {
    lab.domain_id = labDomainFor(lab.id);
    Content.labs.push(lab);
    Content.labById[lab.id] = lab;
  });
  Content.scenarios = [];
  Content.scenarioById = {};
  Content.domains.forEach(function (dom) {
    (dom.scenarios || []).forEach(function (sc) {
      Content.scenarios.push(sc);
      Content.scenarioById[sc.id] = sc;
    });
  });
  Content.simulations = asArray(d.simulations).slice();
  Content.mockMinutes = (d.simulation && d.simulation.minutes) || 180;
  Content.behavioral = asArray(d.behavioral);
  Content.resources = (d.resources && typeof d.resources === 'object') ? d.resources : { cheatsheet: [], glossary: [], checklist: [], links: [], references: [] };
  ['cheatsheet','glossary','checklist','links','references'].forEach(function(k){ Content.resources[k] = asArray(Content.resources[k]); });
  Content.media = asArray(d.media);
}

function mediaForDomain(domainId) {
  return Content.media.filter(function (m) { return m.lesson_ref === 'c-' + domainId; });
}
function lessonsForDomain(domainId) {
  return Content.lessons.filter(function (l) { return l.domain_id === domainId; });
}
function labsForDomain(domainId) {
  return Content.labs.filter(function (l) { return l.domain_id === domainId; });
}
function scenariosForDomain(domainId) {
  var dom = Content.domainById[domainId];
  return dom ? (dom.scenarios || []) : [];
}

/* ==================== 3. PROGRESS STORE + CLOUD SYNC ====================== */
/* localStorage is PRIMARY (works offline, no login needed).
 * When GET /api/me returns 200, the bootcamp's namespaced slice
 * progress["tl-infra-assessment-prep"] is PUT to cloud on changes
 * (debounced ~10s). On load, cloud->local merge: newer updatedAt wins
 * per item. 401/network failure -> stay local silently. */
var Store = {
  state: null,
  cloud: false,
  syncState: 'local',   // local | synced | offline | syncing
  _saveTimer: null,
  _syncTimer: null
};

function freshState() {
  return {
    v: 1,
    updatedAt: Date.now(),
    lessons: {},    // id -> {viewed:true, updatedAt}
    scenarios: {},  // id -> {answered:true, correct:bool, attempts:n, correctStreak:n, updatedAt}
    labs: {},       // id -> {completed:true, steps:{i:true}, checks:{i:true}, updatedAt}
    drills: {},     // cmdId -> {attempts, correct, totalMs, bestMs, mastered, lastPeeked, updatedAt}
    sr: {},         // itemId -> {ease, interval, reps, next_due, updatedAt}
    activity: {},   // YYYY-MM-DD -> count
    mockBest: { score: 0, at: 0 },       // best mock % 
    mockRuns: 0,
    checkItems: {}  // checklist id -> true (readiness checklist)
  };
}

function loadLocalState() {
  try {
    var raw = localStorage.getItem(LS_KEY);
    if (raw) {
      var s = JSON.parse(raw);
      var f = freshState();
      Object.keys(f).forEach(function (k) {
        // Shape guard: a hand-corrupted value (e.g. "activity": "x") would make
        // Store.save throw in strict mode and silently stop all future saves.
        var v = s[k];
        if (v === undefined || v === null) return;
        if (typeof f[k] === 'object') { if (typeof v === 'object') f[k] = v; }
        else if (typeof v === typeof f[k]) f[k] = v;
      });
      return f;
    }
  } catch (e) {}
  return freshState();
}

function persistLocal() {
  try {
    Store.state.updatedAt = Date.now();
    localStorage.setItem(LS_KEY, JSON.stringify(Store.state));
  } catch (e) {}
}

Store.save = debounce(function () {
  persistLocal();
  markActivity();
  if (Store.cloud) scheduleCloudSync();
}, 400);

function markActivity() {
  var k = todayKey();
  Store.state.activity[k] = (Store.state.activity[k] || 0) + 1;
}

/* ---- cloud sync ---- */
function setSyncDot(state, label) {
  Store.syncState = state;
  var dot = $('#syncDot');
  if (!dot) return;
  dot.className = 'sync-dot ' + state;
  dot.title = label || state;
  var lbl = $('#syncLabel');
  if (lbl) lbl.textContent = { local: 'local', synced: 'synced', offline: 'offline', syncing: 'syncing' }[state] || state;
}

function mergeCloudState(cloudSlice) {
  // Per-item: newer updatedAt wins. Activity: per-day max. mockBest: higher score wins.
  if (!cloudSlice || typeof cloudSlice !== 'object') return false;
  var local = Store.state, changed = false;
  ['lessons', 'scenarios', 'labs', 'drills', 'sr'].forEach(function (coll) {
    var c = cloudSlice[coll] || {};
    Object.keys(c).forEach(function (id) {
      var ci = c[id], li = local[coll][id];
      if (!li || (ci.updatedAt || 0) > (li.updatedAt || 0)) {
        local[coll][id] = ci;
        changed = true;
      }
    });
  });
  var ca = cloudSlice.activity || {};
  Object.keys(ca).forEach(function (day) {
    if ((ca[day] || 0) > (local.activity[day] || 0)) { local.activity[day] = ca[day]; changed = true; }
  });
  var cb = cloudSlice.mockBest;
  if (cb && (cb.score || 0) > (local.mockBest.score || 0)) { local.mockBest = cb; changed = true; }
  if ((cloudSlice.mockRuns || 0) > (local.mockRuns || 0)) { local.mockRuns = cloudSlice.mockRuns; changed = true; }
  var cc = cloudSlice.checkItems || {};
  Object.keys(cc).forEach(function (id) {
    if (cc[id] && !local.checkItems[id]) { local.checkItems[id] = true; changed = true; }
  });
  if (changed) persistLocal();
  return changed;
}

function bootSync() {
  var ctl = new AbortController();
  var to = setTimeout(function () { ctl.abort(); }, 6000);
  fetch(API_ME, { credentials: 'include', signal: ctl.signal }).then(function (r) {
    clearTimeout(to);
    if (!r.ok) { setSyncDot('local', 'local only — not signed in'); return; }
    Store.cloud = true;
    setSyncDot('syncing', 'syncing…');
    return fetch(API_PROGRESS, { credentials: 'include' }).then(function (pr) {
      if (!pr.ok) throw new Error('progress ' + pr.status);
      return pr.json();
    }).then(function (blob) {
      var slice = blob && blob.progress ? blob.progress[SLUG] : null;
      var changed = mergeCloudState(slice);
      setSyncDot('synced', 'synced to cloud');
      if (changed && location.hash) renderRoute(); // refresh current view with merged data
    }).catch(function () {
      setSyncDot('offline', 'cloud unreachable — local only');
    });
  }).catch(function () {
    clearTimeout(to);
    Store.cloud = false;
    setSyncDot('local', 'local only');
  });
}

function scheduleCloudSync() {
  if (!Store.cloud) return;
  clearTimeout(Store._syncTimer);
  Store._syncTimer = setTimeout(pushCloudSync, SYNC_DEBOUNCE_MS);
}

function pushCloudSync() {
  if (!Store.cloud) return;
  setSyncDot('syncing', 'syncing…');
  var body = { progress: {} };
  body.progress[SLUG] = Store.state;
  fetch(API_PROGRESS, {
    method: 'PUT',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  }).then(function (r) {
    if (!r.ok) throw new Error('PUT ' + r.status);
    setSyncDot('synced', 'synced to cloud');
  }).catch(function () {
    setSyncDot('offline', 'cloud unreachable — local only');
  });
}

/* ==================== 4. SPACED REPETITION (SM-2 lite) ==================== */
function srGet(itemId) {
  var s = Store.state.sr[itemId];
  if (!s) {
    s = { ease: 2.5, interval: 0, reps: 0, next_due: 0, updatedAt: Date.now() };
    Store.state.sr[itemId] = s;
  }
  return s;
}
/* quality 0..5: 5 perfect, 4 correct w/ hesitation or hint, 2 wrong */
function srUpdate(itemId, quality) {
  var s = srGet(itemId);
  if (quality < 3) {
    s.reps = 0;
    s.interval = 1;
    s.ease = Math.max(1.3, s.ease - 0.2);
  } else {
    s.ease = s.ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    if (s.ease < 1.3) s.ease = 1.3;
    s.reps += 1;
    if (s.reps === 1) s.interval = 1;
    else if (s.reps === 2) s.interval = 6;
    else s.interval = Math.max(1, Math.round(s.interval * s.ease));
  }
  s.next_due = Date.now() + s.interval * 86400000;
  s.updatedAt = Date.now();
  Store.save();
}
function srDueItems(limit) {
  var now = Date.now(), out = [];
  Object.keys(Store.state.sr).forEach(function (id) {
    var s = Store.state.sr[id];
    if (s.reps > 0 && s.next_due <= now) out.push({ id: id, sr: s });
  });
  out.sort(function (a, b) { return a.sr.next_due - b.sr.next_due; });
  return out.slice(0, limit || 20);
}
function srLabel(id) {
  if (Content.scenarioById[id]) return { kind: 'scenario', title: Content.scenarioById[id].title, href: '#/scenario/' + id };
  var sim = Content.simulations.filter(function (s) { return s.id === id; })[0];
  if (sim) return { kind: 'mock', title: sim.title, href: '#/mock' };
  var cmd = drillCommandById(id);
  if (cmd) return { kind: 'drill', title: cmd.command, href: '#/drills/speed?cmd=' + id, mono: true };
  return { kind: 'item', title: id, href: '#/dashboard' };
}

/* ==================== 5. STATS / READINESS ================================= */
function moduleCompletion(domainId) {
  var lessons = lessonsForDomain(domainId);
  var scenarios = scenariosForDomain(domainId);
  var total = lessons.length + scenarios.length;
  if (!total) return 1;
  var done = 0;
  lessons.forEach(function (l) { if (Store.state.lessons[l._id] && Store.state.lessons[l._id].viewed) done++; });
  scenarios.forEach(function (sc) { if (Store.state.scenarios[sc.id] && Store.state.scenarios[sc.id].answered) done++; });
  return done / total;
}
function domainMastery(domainId) {
  // 50% completion + 50% scenario correctness
  var scenarios = scenariosForDomain(domainId);
  var comp = moduleCompletion(domainId);
  var correct = 0, answered = 0;
  scenarios.forEach(function (sc) {
    var r = Store.state.scenarios[sc.id];
    if (r && r.answered) { answered++; if (r.correct) correct++; }
  });
  var acc = scenarios.length ? correct / scenarios.length : 0;
  return 0.5 * comp + 0.5 * acc;
}
function labsCompletion() {
  if (!Content.labs.length) return 0;
  var done = Content.labs.filter(function (l) {
    return Store.state.labs[l.id] && Store.state.labs[l.id].completed;
  }).length;
  return done / Content.labs.length;
}
function drillsMastery() {
  var cmds = (Content.drillData && Content.drillData.commands) || [];
  if (!cmds.length) return 0;
  var m = 0;
  cmds.forEach(function (c) {
    var r = Store.state.drills[c.id];
    if (r && r.mastered) m++;
  });
  return m / cmds.length;
}
function readinessScore() {
  var mods = Content.domains.length
    ? Content.domains.reduce(function (a, d) { return a + moduleCompletion(d.id); }, 0) / Content.domains.length
    : 0;
  var labs = labsCompletion();
  var drills = drillsMastery();
  var mock = (Store.state.mockBest.score || 0) / 100;
  var score = 0.25 * mods + 0.35 * labs + 0.20 * drills + 0.20 * mock;
  return { score: score, parts: { modules: mods, labs: labs, drills: drills, mock: mock } };
}
function weakestDomains(n) {
  return Content.domains.map(function (d) {
    return { id: d.id, name: d.name, mastery: domainMastery(d.id), completion: moduleCompletion(d.id) };
  }).sort(function (a, b) { return a.mastery - b.mastery; }).slice(0, n || 3);
}
function studyStreak() {
  var days = Object.keys(Store.state.activity).sort();
  if (!days.length) return 0;
  var streak = 0, cursor = todayKey();
  if (days.indexOf(cursor) < 0) cursor = todayKey(new Date(Date.now() - 86400000)); // allow today-missing
  while (days.indexOf(cursor) >= 0) { streak++; cursor = todayKey(new Date(new Date(cursor + 'T12:00:00').getTime() - 86400000)); }
  return streak;
}
function nextStep() {
  // One clear CTA: due reviews first, else first incomplete module, else mock.
  var due = srDueItems(1);
  if (due.length) {
    var l = srLabel(due[0].id);
    return { title: 'Review due: ' + l.title, href: l.href, why: due.length + ' item(s) due for spaced review' };
  }
  for (var i = 0; i < Content.domains.length; i++) {
    var d = Content.domains[i];
    if (moduleCompletion(d.id) < 1) {
      return { title: 'Continue: ' + d.name, href: '#/module/' + d.id, why: Math.round(moduleCompletion(d.id) * 100) + '% complete' };
    }
  }
  return { title: 'Take the 3-hour mock assessment', href: '#/mock', why: 'all modules complete — prove it under pressure' };
}
function drillCommandById(id) {
  var cmds = (Content.drillData && Content.drillData.commands) || [];
  for (var i = 0; i < cmds.length; i++) if (cmds[i].id === id) return cmds[i];
  return null;
}

/* ==================== 6. ROUTER + APP SHELL ================================ */
var NAV = [
  { id: 'dashboard', label: 'Dashboard', icon: '◈' },
  { id: 'learn', label: 'Learn', icon: '▤' },
  { id: 'drills', label: 'Drills', icon: '⚡' },
  { id: 'terminal', label: 'Terminal', icon: '⌁' },
  { id: 'mock', label: 'Mock', icon: '◉' },
  { id: 'reference', label: 'Reference', icon: '▦' }
];

function parseRoute() {
  var h = location.hash || '#/dashboard';
  var parts = h.replace(/^#\//, '').split('/');
  var arg = null;
  if (parts[1]) {
    try { arg = decodeURIComponent(parts[1].split('?')[0]); }
    catch (e) { arg = parts[1].split('?')[0]; } // malformed % escapes: fall back to raw so the router never throws
  }
  return { view: parts[0] || 'dashboard', arg: arg, query: h.split('?')[1] || '' };
}
function go(href) { location.hash = href; }

var Timers = {
  list: [],
  add: function (id) { this.list.push(id); },
  clear: function () { this.list.forEach(clearInterval); this.list = []; }
};

function paintView(v, html) {
  /* Progressive enhancement: crossfade route changes where the browser
   * supports the View Transitions API; skipped entirely under
   * prefers-reduced-motion or on unsupported browsers. */
  var apply = function () { v.innerHTML = html; };
  try {
    if (typeof document.startViewTransition === 'function' && window.matchMedia &&
        !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.startViewTransition(function () { apply(); });
      return;
    }
  } catch (e) { /* fall through to direct paint */ }
  apply();
}

function renderRoute() {
  Timers.clear();
  var r = parseRoute();
  $all('.nav-btn').forEach(function (b) {
    b.classList.toggle('active', b.dataset.view === r.view || (r.view === 'module' || r.view === 'lesson' || r.view === 'scenario' || r.view === 'lab') && b.dataset.view === 'learn');
  });
  var v = $('#view');
  window.scrollTo(0, 0);
  var html;
  try {
    if (r.view === 'dashboard') html = viewDashboard();
    else if (r.view === 'learn') html = viewLearn();
    else if (r.view === 'module') html = viewModule(r.arg);
    else if (r.view === 'lesson') html = viewLesson(r.arg);
    else if (r.view === 'scenario') html = viewScenario(r.arg);
    else if (r.view === 'lab') html = viewLab(r.arg);
    else if (r.view === 'drills') html = viewDrills(r.arg, r.query);
    else if (r.view === 'terminal') html = viewTerminal();
    else if (r.view === 'mock') html = viewMockLanding();
    else if (r.view === 'reference') html = viewReference();
    else html = viewDashboard();
  } catch (e) {
    html = '<div class="wrap"><div class="panel"><h2>Something failed to render</h2><p class="muted">' + esc(e.message) + '</p><a class="btn" href="#/dashboard">Back to dashboard</a></div></div>';
  }
  paintView(v, html);
  afterRender(r);
  if (window._swUpdateReady) showOfflineBanner(false);
}

function afterRender(r) {
  if (r.view === 'scenario') initScenarioView(r.arg);
  else if (r.view === 'drills') initDrillsView(r.arg, r.query);
  else if (r.view === 'terminal') initTerminalView();
  else if (r.view === 'lab') initLabView(r.arg);
  else if (r.view === 'mock') initMockLanding();
}

function progressBar(pct, label) {
  var p = Math.max(0, Math.min(100, Math.round(pct * 100)));
  return '<div class="bar" role="progressbar" aria-valuenow="' + p + '" aria-label="' + esc(label || 'progress') + '"><i style="width:' + p + '%"></i></div>';
}
function stateBadge(state) {
  var map = { locked: ['🔒', 'locked'], available: ['○', 'not-started'], progress: ['◐', 'in-progress'], complete: ['●', 'complete'], mastered: ['◆', 'mastered'] };
  var m = map[state] || map.available;
  return '<span class="badge st-' + m[1] + '">' + m[0] + ' ' + m[1] + '</span>';
}
function moduleState(domainId, idx) {
  if (idx > 0) {
    var prev = Content.domains[idx - 1];
    if (moduleCompletion(prev.id) < 0.8) return 'locked';
  }
  var c = moduleCompletion(domainId);
  if (c >= 1) {
    var m = domainMastery(domainId);
    return m >= 0.85 ? 'mastered' : 'complete';
  }
  return c > 0 ? 'progress' : 'available';
}

/* ==================== 7. DASHBOARD VIEW ==================================== */
function viewDashboard() {
  var rs = readinessScore();
  var pct = Math.round(rs.score * 100);
  var weak = weakestDomains(3);
  var streak = studyStreak();
  var due = srDueItems(6);
  var next = nextStep();
  var dueTotal = srDueItems(500).length;

  var h = '';
  h += '<div class="wrap">';
  h += '<div class="poster-banner"><img src="https://interstitiumlabs.dev/assets/cards/hq/hq-infra-assessment-prep_16x9_poster.png" alt="IT Infrastructure Assessment Prep — ThreatLocker Interview Ready" fetchpriority="high" onerror="this.closest(\'.poster-banner\').style.display=\'none\'" /></div>';
  h += '<section class="hero-mini"><div><p class="eyebrow">INTERSTITIUM LABS · CBT</p>';
  h += '<h1>' + esc(Content.title) + '</h1>';
  h += '<p class="lede">' + esc(Content.tagline) + '</p></div>';
  h += '<div class="score-ring" role="img" aria-label="Readiness ' + pct + ' percent">';
  h += '<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="52" class="ring-bg"/><circle cx="60" cy="60" r="52" class="ring-fg" stroke-dasharray="' + (pct * 3.267) + ' 326.7"/></svg>';
  h += '<div class="ring-num">' + pct + '<span>%</span></div><div class="ring-cap">readiness</div></div></section>';

  h += '<div class="stat-grid">';
  h += statCell('Readiness', pct + '%', 'modules 25 · labs 35 · drills 20 · mock 20');
  h += statCell('Study streak', streak + (streak === 1 ? ' day' : ' days'), 'days with activity');
  h += statCell('Due reviews', dueTotal, 'spaced-repetition queue');
  h += statCell('Best mock', (Store.state.mockBest.score || 0) + '%', Store.state.mockRuns + ' run(s)');
  h += '</div>';

  h += '<div class="panel cta-panel"><div><h3>Next step</h3><p class="muted">' + esc(next.why) + '</p></div>';
  h += '<a class="btn primary" href="' + esc(next.href) + '">' + esc(next.title) + ' →</a></div>';

  if (due.length) {
    h += '<div class="panel"><h3>Due review <span class="muted">(' + dueTotal + ' total)</span></h3><div class="due-list">';
    due.forEach(function (d) {
      var l = srLabel(d.id);
      h += '<a class="due-item" href="' + esc(l.href) + '"><span class="due-kind">' + esc(l.kind) + '</span>' +
        (l.mono ? '<code>' + esc(l.title.slice(0, 60)) + '</code>' : '<span>' + esc(l.title) + '</span>') + '<span class="due-go">review →</span></a>';
    });
    h += '</div></div>';
  }

  h += '<div class="panel"><h3>Weak areas <span class="muted">— bottom 3 domains</span></h3>';
  weak.forEach(function (w) {
    h += '<a class="weak-row" href="#/module/' + esc(w.id) + '"><span class="weak-name">' + esc(w.name) + '</span>' +
      progressBar(w.mastery) + '<span class="weak-pct">' + Math.round(w.mastery * 100) + '%</span></a>';
  });
  h += '</div>';

  h += '<div class="panel"><h3>Guided path</h3><div class="mod-grid">';
  Content.domains.forEach(function (d, i) {
    var st = moduleState(d.id, i);
    var locked = st === 'locked';
    h += locked
      ? '<div class="mod-card locked">' + stateBadge('locked') + '<strong>' + esc(d.name) + '</strong><p class="muted">Complete the previous module to 80% to unlock.</p>' + progressBar(moduleCompletion(d.id), d.name) + '</div>'
      : '<a class="mod-card" href="#/module/' + esc(d.id) + '">' + stateBadge(st) + '<strong>' + esc(d.name) + '</strong>' + progressBar(moduleCompletion(d.id), d.name) + '</a>';
  });
  h += '</div></div>';

  h += '<div class="reset-row"><button class="btn small ghost" id="resetProgress">Reset all progress</button></div>';
  h += '</div>';

  setTimeout(function () {
    var b = $('#resetProgress');
    if (b) b.onclick = function () {
      if (confirm('Reset ALL progress for this bootcamp? This cannot be undone.')) {
        Store.state = freshState();
        persistLocal();
        if (Store.cloud) pushCloudSync();
        renderRoute();
        toast('Progress reset');
      }
    };
  }, 0);
  return h;
}
function statCell(label, value, sub) {
  return '<div class="stat"><div class="v">' + esc(value) + '</div><div class="l">' + esc(label) + '</div><div class="s">' + esc(sub || '') + '</div></div>';
}

/* ==================== 8. LEARN / MODULE / LESSON VIEWS ===================== */
function viewLearn() {
  var h = '<div class="wrap"><div class="view-head"><p class="eyebrow">GUIDED PATH</p><h2>Learn</h2>';
  h += '<p class="muted">Sequential path: lessons → scenarios → labs. A module unlocks when the previous reaches 80%.</p></div><div class="mod-list">';
  Content.domains.forEach(function (d, i) {
    var st = moduleState(d.id, i);
    var locked = st === 'locked';
    var nL = lessonsForDomain(d.id).length, nS = scenariosForDomain(d.id).length, nB = labsForDomain(d.id).length;
    var inner = stateBadge(st) + '<div class="mod-meta"><strong>' + esc(d.name) + '</strong>' +
      '<p class="muted">' + nL + ' lessons · ' + nS + ' scenarios · ' + nB + ' labs</p>' +
      progressBar(moduleCompletion(d.id), d.name) + '</div><span class="chev">›</span>';
    h += locked ? '<div class="mod-row locked">' + inner + '</div>'
                : '<a class="mod-row" href="#/module/' + esc(d.id) + '">' + inner + '</a>';
  });
  h += '</div></div>';
  return h;
}

function viewModule(domainId) {
  var dom = Content.domainById[domainId];
  if (!dom) return '<div class="wrap"><div class="panel"><p>Unknown module.</p><a class="btn" href="#/learn">Back</a></div></div>';
  var idx = Content.domains.indexOf(dom);
  if (moduleState(domainId, idx) === 'locked')
    return '<div class="wrap"><div class="panel"><h2>🔒 Locked</h2><p class="muted">Complete the previous module to 80% to unlock ' + esc(dom.name) + '.</p><a class="btn" href="#/learn">Back to path</a></div></div>';

  var h = '<div class="wrap"><a class="back" href="#/learn">← Learn</a>';
  h += '<div class="view-head"><p class="eyebrow">MODULE ' + (idx + 1) + ' OF ' + Content.domains.length + '</p><h2>' + esc(dom.name) + '</h2>';
  h += progressBar(moduleCompletion(domainId), dom.name) + '</div>';

  var lessons = lessonsForDomain(domainId);
  if (lessons.length) {
    h += '<h3 class="sec-h">Lessons</h3><div class="item-list">';
    lessons.forEach(function (l) {
      var done = Store.state.lessons[l._id] && Store.state.lessons[l._id].viewed;
      h += '<a class="item-row" href="#/lesson/' + l._id + '"><span class="tick ' + (done ? 'on' : '') + '">' + (done ? '✓' : '○') + '</span><span>' + esc(l.title) + '</span><span class="chev">›</span></a>';
    });
    h += '</div>';
  }
  var scenarios = scenariosForDomain(domainId);
  if (scenarios.length) {
    h += '<h3 class="sec-h">Scenarios <span class="muted">(' + scenarios.length + ')</span></h3><div class="item-list">';
    scenarios.forEach(function (sc, i) {
      var r = Store.state.scenarios[sc.id];
      var cls = r && r.answered ? (r.correct ? 'ok' : 'bad') : '';
      var mark = r && r.answered ? (r.correct ? '✓' : '✗') : '○';
      h += '<a class="item-row" href="#/scenario/' + esc(sc.id) + '"><span class="tick ' + cls + '">' + mark + '</span><span>' + esc(sc.title) + '<em>' + (sc.mins || '') + ' min</em></span><span class="chev">›</span></a>';
    });
    h += '</div>';
  }
  var labs = labsForDomain(domainId);
  if (labs.length) {
    h += '<h3 class="sec-h">Labs</h3><div class="item-list">';
    labs.forEach(function (lab) {
      var done = Store.state.labs[lab.id] && Store.state.labs[lab.id].completed;
      h += '<a class="item-row" href="#/lab/' + esc(lab.id) + '"><span class="tick ' + (done ? 'on' : '') + '">' + (done ? '✓' : '○') + '</span><span>' + esc(lab.title) + '</span><span class="chev">›</span></a>';
    });
    h += '</div>';
  }
  var media = mediaForDomain(domainId);
  if (media.length) {
    h += '<h3 class="sec-h">Visuals</h3><div class="vis-grid">';
    media.forEach(function (m) {
      var src = m.svg || m.html;
      h += '<figure class="vis-card"><img src="' + esc(src) + '" alt="' + esc(m.title || 'diagram') + '" loading="lazy"><figcaption>' + esc(m.title || '') + '</figcaption></figure>';
    });
    h += '</div>';
  }
  h += '</div>';
  return h;
}

function viewLesson(lessonId) {
  var l = Content.lessonById[lessonId];
  if (!l) return '<div class="wrap"><div class="panel"><p>Unknown lesson.</p><a class="btn" href="#/learn">Back</a></div></div>';
  var done = !!(Store.state.lessons[lessonId] && Store.state.lessons[lessonId].viewed);
  var h = '<div class="wrap lesson"><a class="back" href="#/module/' + esc(l.domain_id) + '">← ' + esc(Content.domainById[l.domain_id].name) + '</a>';
  h += '<p class="eyebrow">LESSON</p><h2>' + esc(l.title) + '</h2>';
  if (l.concepts && l.concepts.length) {
    h += '<div class="panel"><h3>Key concepts</h3><ul class="bullets">';
    l.concepts.forEach(function (c) { h += '<li>' + esc(c) + '</li>'; });
    h += '</ul></div>';
  }
  if (l.example) {
    h += '<div class="panel"><h3>Worked example</h3>';
    if (l.example.code) h += '<pre class="code"><span class="code-lang">' + esc(l.example.lang || 'text') + '</span>' + esc(l.example.code) + '</pre>';
    if (l.example.walkthrough) h += '<p>' + esc(l.example.walkthrough) + '</p>';
    h += '</div>';
  }
  var media = mediaForDomain(l.domain_id);
  if (media.length) {
    h += '<div class="panel"><h3>Visuals</h3><div class="vis-grid">';
    media.forEach(function (m) {
      var src = m.svg || m.html;
      if (/\.html$/.test(src)) h += '<figure class="vis-card"><iframe src="' + esc(src) + '" title="' + esc(m.title || 'interactive') + '" loading="lazy"></iframe><figcaption>' + esc(m.title || '') + '</figcaption></figure>';
      else h += '<figure class="vis-card"><img src="' + esc(src) + '" alt="' + esc(m.title || 'diagram') + '" loading="lazy"><figcaption>' + esc(m.title || '') + (m.caption ? ' — ' + esc(m.caption) : '') + '</figcaption></figure>';
    });
    h += '</div></div>';
  }
  if (l.pitfalls && l.pitfalls.length) {
    h += '<div class="panel warn"><h3>⚠ Pitfalls</h3><ul class="bullets">';
    l.pitfalls.forEach(function (p) { h += '<li>' + esc(p) + '</li>'; });
    h += '</ul></div>';
  }
  if (l.try_it) h += '<div class="panel try"><h3>Try it</h3><p>' + esc(l.try_it) + '</p><a class="btn small" href="#/terminal">Open terminal →</a></div>';
  h += '<div class="action-row"><button class="btn primary" id="lessonDone">' + (done ? '✓ Lesson complete' : 'Mark lesson complete') + '</button></div>';
  h += '</div>';
  setTimeout(function () {
    var b = $('#lessonDone');
    if (b) b.onclick = function () {
      Store.state.lessons[lessonId] = { viewed: true, updatedAt: Date.now() };
      Store.save();
      b.textContent = '✓ Lesson complete';
      b.classList.add('done');
      toast('Lesson marked complete');
    };
  }, 0);
  return h;
}

/* ==================== 9. SCENARIO QUIZ VIEW ================================ */
function scenarioChoices(sc) {
  // Deterministic per-scenario shuffle so order is stable within a session.
  var seed = 0;
  for (var i = 0; i < sc.id.length; i++) seed = (seed * 31 + sc.id.charCodeAt(i)) >>> 0;
  var idx = sc.choices.map(function (_, i) { return i; });
  var rand = mulberry32(seed);
  idx = shuffle(idx, rand);
  return idx;
}

function viewScenario(scenarioId) {
  var sc = Content.scenarioById[scenarioId];
  if (!sc) return '<div class="wrap"><div class="panel"><p>Unknown scenario.</p><a class="btn" href="#/learn">Back</a></div></div>';
  var dom = Content.domainById[sc.domain_id];
  var order = scenarioChoices(sc);
  var h = '<div class="wrap"><a class="back" href="#/module/' + esc(sc.domain_id) + '">← ' + esc(dom.name) + '</a>';
  h += '<p class="eyebrow">SCENARIO · ' + esc(dom.name).toUpperCase() + (sc.mins ? ' · ~' + sc.mins + ' MIN' : '') + '</p>';
  h += '<h2>' + esc(sc.title) + '</h2>';
  if (sc.objectives && sc.objectives.length)
    h += '<div class="objectives"><p>OBJECTIVES</p><ul>' + sc.objectives.map(function (o) { return '<li>' + esc(o) + '</li>'; }).join('') + '</ul></div>';
  h += '<div class="situation"><p>' + esc(sc.situation).split('\n').join('</p><p>') + '</p></div>';
  if (sc.evidence && sc.evidence.length) {
    h += '<div class="ev-row" role="group" aria-label="Evidence">';
    sc.evidence.forEach(function (ev, i) {
      h += '<button class="btn small ghost ev-btn" data-ev="' + i + '">📄 ' + esc(ev[0]) + '</button>';
    });
    h += '</div><div class="ev-pane" id="evPane" hidden></div>';
  }
  h += '<p class="decision-prompt">' + esc(sc.prompt) + '</p>';
  h += '<div class="choices" role="radiogroup" aria-label="Answer choices">';
  order.forEach(function (ci) {
    h += '<label class="choice"><input type="radio" name="sc-choice" value="' + ci + '"><span class="choice-letter">' + 'ABCD'[order.indexOf(ci)] + '</span><span>' + esc(sc.choices[ci]) + '</span></label>';
  });
  h += '</div>';
  h += '<div class="hint-text" id="scHint" role="status"></div><div class="feedback" id="scFeedback"></div>';
  h += '<div class="action-row"><button class="btn small ghost" id="scHintBtn">💡 Hint</button>';
  h += '<button class="btn primary" id="scSubmit" disabled>Submit answer</button>';
  h += '<button class="btn small ghost" id="scNext" style="display:none">Next →</button>';
  h += '<span class="bench-timer" id="scTimer">00:00</span></div>';
  h += '</div>';
  return h;
}

function initScenarioView(scenarioId) {
  var sc = Content.scenarioById[scenarioId];
  if (!sc) return;
  var hintUsed = false, answered = false, startT = Date.now();
  var timerId = setInterval(function () {
    var el = $('#scTimer');
    if (el) el.textContent = fmtClock((Date.now() - startT) / 1000);
  }, 1000);
  Timers.add(timerId);

  $all('.ev-btn').forEach(function (b) {
    b.onclick = function () {
      var ev = sc.evidence[+b.dataset.ev];
      var pane = $('#evPane');
      pane.hidden = false;
      pane.innerHTML = '<p class="ev-title">' + esc(ev[0]) + '</p><pre class="code">' + esc(ev[1]) + '</pre>';
      $all('.ev-btn').forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
    };
  });
  $all('input[name="sc-choice"]').forEach(function (r) {
    r.onchange = function () { $('#scSubmit').disabled = false; };
  });
  $('#scHintBtn').onclick = function () {
    hintUsed = true;
    $('#scHint').textContent = '💡 ' + sc.hint;
    $('#scHintBtn').disabled = true;
  };
  $('#scSubmit').onclick = function () {
    if (answered) return;
    var sel = $('input[name="sc-choice"]:checked');
    if (!sel) return;
    answered = true;
    var picked = +sel.value, correct = picked === sc.answer;
    var fb = $('#scFeedback');
    fb.className = 'feedback ' + (correct ? 'ok' : 'no');
    fb.innerHTML = '<strong>' + (correct ? '✓ Correct' : '✗ Not quite') + '</strong><p>' + esc(sc.why) + '</p>';
    $all('.choice').forEach(function (lab) {
      var v = +$('input', lab).value;
      lab.classList.add('rated');
      if (v === sc.answer) lab.classList.add('is-answer');
      else if (v === picked) lab.classList.add('is-pick');
      $('input', lab).disabled = true;
    });
    $('#scSubmit').style.display = 'none';
    $('#scHintBtn').disabled = true;
    var prev = Store.state.scenarios[scenarioId] || { attempts: 0, correctStreak: 0 };
    prev.answered = true;
    prev.attempts = (prev.attempts || 0) + 1;
    prev.correctStreak = correct ? (prev.correctStreak || 0) + 1 : 0;
    prev.correct = correct;
    prev.updatedAt = Date.now();
    Store.state.scenarios[scenarioId] = prev;
    srUpdate(scenarioId, correct ? (hintUsed ? 4 : 5) : 2);
    Store.save();
    var nextBtn = $('#scNext');
    nextBtn.style.display = '';
    nextBtn.onclick = function () {
      var list = scenariosForDomain(sc.domain_id);
      var i = list.findIndex(function (s) { return s.id === scenarioId; });
      if (i >= 0 && i < list.length - 1) go('#/scenario/' + list[i + 1].id);
      else go('#/module/' + sc.domain_id);
    };
  };
}

/* ==================== 10. UNIFIED TERMINAL EMULATOR ======================== */
/* One component, five profiles: powershell, bash, ios, fortios, panos.
 * Each profile: prompt(), run(cmd) -> string, complete[] for tab-completion. */
var TermProfiles = {};

function normCmd(s) { return String(s).replace(/\s+/g, ' ').trim(); }
function normKey(s) { return normCmd(s).toLowerCase(); }

/* ---- shared drill-command output map (PowerShell-flavored) ---- */
var PS_EXACT = {};
(function buildPsExact() {
  function put(cmd, out) { PS_EXACT[normKey(cmd)] = out; }
  put('New-ADUser -Name "jdoe" -GivenName "John" -Surname "Doe" -SamAccountName "jdoe" -UserPrincipalName "jdoe@corp.local" -Path "OU=Users,DC=corp,DC=local" -Enabled $true -AccountPassword (Read-Host -AsSecureString "Enter password")', '');
  put('Get-ADUser -Filter \'Name -eq "jdoe"\' -Properties *',
    'DistinguishedName : CN=jdoe,OU=Users,DC=corp,DC=local\nEnabled           : True\nGivenName         : John\nName              : jdoe\nSamAccountName    : jdoe\nSurname           : Doe\nUserPrincipalName : jdoe@corp.local');
  put('Unlock-ADAccount -Identity "jdoe"', '');
  put('Set-ADAccountPassword -Identity "jdoe" -Reset -NewPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force)', '');
  put('New-ADOrganizationalUnit -Name "Servers" -Path "DC=corp,DC=local" -ProtectedFromAccidentalDeletion $true', '');
  put('New-GPLink -Name "Baseline Policy" -Target "OU=Workstations,DC=corp,DC=local" -LinkEnabled Yes',
    'GpoId       : {31B2F340-016D-11D2-945F-00C04FB984F9}\nTarget      : OU=Workstations,DC=corp,DC=local\nLinkEnabled : Yes');
  put('Add-ADGroupMember -Identity "HelpDesk" -Members "jdoe"', '');
  put('Get-ADComputer -Filter \'OperatingSystem -like "*Server*"\' | Select-Object Name, OperatingSystem',
    'Name      OperatingSystem\n----      ---------------\nSRV01     Windows Server 2025 Standard\nSRV02     Windows Server 2025 Standard\nDC01      Windows Server 2025 Datacenter');
  put('Set-ADUser -Identity "jdoe" -Department "IT" -Title "SysAdmin"', '');
  put('Disable-ADAccount -Identity "jdoe"', '');
  put('Add-DnsServerResourceRecordA -Name "web01" -ZoneName "corp.local" -IPv4Address "10.0.1.50"', '');
  put('Resolve-DnsName -Name "web01.corp.local" -Type A',
    'Name                         Type   TTL   Section    IPAddress\n----                         ----   ---   -------    ---------\nweb01.corp.local             A      3600  Answer     10.0.1.50');
  put('nslookup web01.corp.local',
    'Server:  dc01.corp.local\nAddress:  10.0.1.10\n\nName:    web01.corp.local\nAddress:  10.0.1.50');
  put('Add-DnsServerPrimaryZone -Name "corp.local" -ZoneFile "corp.local.dns"', '');
  put('dnscmd /recordadd corp.local web01 A 10.0.1.50', 'Add A Record for web01@corp.local [10.0.1.50]\nCommand completed successfully.');
  put('Get-DnsServerZone | Select-Object ZoneName, ZoneType, IsAutoCreated',
    'ZoneName        ZoneType  IsAutoCreated\n--------        --------  -------------\ncorp.local      Primary   False\n_msdcs.corp.local Primary   False');
  put('Add-DhcpServerv4Scope -Name "LAN" -StartRange 10.0.1.100 -EndRange 10.0.1.200 -SubnetMask 255.255.255.0', '');
  put('Set-DhcpServerv4OptionValue -ScopeId 10.0.1.0 -DnsServer 10.0.1.10 -Router 10.0.1.1', '');
  put('Get-DhcpServerv4Lease -ScopeId 10.0.1.0 | Where-Object {$_.HostName -like "*jdoe*"}',
    'IPAddress     HostName      ClientId           LeaseExpiryTime\n---------     --------      --------           ---------------\n10.0.1.105    jdoe-pc       00-1a-2b-3c-4d-5e   10/11/2026 8:00 AM');
  put('netsh dhcp server scope 10.0.1.0 show clients 1',
    'Changed the current scope context to 10.0.1.0 scope.\n\nType : N - NONE, D - DHCP B - BOTH, U - UNSPECIFIED\nIP Address      - Subnet Mask    - Unique ID        - Lease Expires        -Type -Name\n10.0.1.100      - 255.255.255.0  - 00-1a-2b-3c-4d-5e - 10/11/2026 8:00 AM  -D-   - jdoe-pc.corp.local\nNo. of Clients: 1 in the Scope : 10.0.1.0\nCommand completed successfully.');
  put('ipconfig /all',
    'Windows IP Configuration\n\n   Host Name . . . . . . . . . . . . : ADMIN-PC\n   Primary Dns Suffix  . . . . . . . : corp.local\n\nEthernet adapter Ethernet:\n   IPv4 Address. . . . . . . . . . . : 10.0.1.105(Preferred)\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n   Default Gateway . . . . . . . . . : 10.0.1.1\n   DNS Servers . . . . . . . . . . . : 10.0.1.10');
  put('ping -t 10.0.1.1',
    'Pinging 10.0.1.1 with 32 bytes of data:\nReply from 10.0.1.1: bytes=32 time<1ms TTL=128\nReply from 10.0.1.1: bytes=32 time<1ms TTL=128\nReply from 10.0.1.1: bytes=32 time<1ms TTL=128\nReply from 10.0.1.1: bytes=32 time<1ms TTL=128\n(simulated output truncated — real -t runs until Ctrl+C)');
  put('tracert 8.8.8.8',
    'Tracing route to dns.google [8.8.8.8]\nover a maximum of 30 hops:\n\n  1    <1 ms    <1 ms    <1 ms  10.0.1.1\n  2     4 ms     3 ms     4 ms  203.0.113.1\n  3     9 ms     8 ms     9 ms  8.8.8.8\n\nTrace complete.');
  put('netstat -ano',
    'Active Connections\n\n  Proto  Local Address          Foreign Address        State           PID\n  TCP    10.0.1.105:54231       10.0.1.10:389          ESTABLISHED     1234\n  TCP    10.0.1.105:54232       10.0.1.10:636          ESTABLISHED     1234\n  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       1024');
  put('Test-NetConnection -ComputerName 10.0.1.1 -Port 443',
    'ComputerName     : 10.0.1.1\nRemoteAddress    : 10.0.1.1\nRemotePort       : 443\nInterfaceAlias   : Ethernet\nTcpTestSucceeded : True');
  put('Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"}',
    'IPAddress         : 10.0.1.105\nInterfaceAlias    : Ethernet\nPrefixOrigin      : Dhcp');
  put('New-VMSwitch -Name "External" -NetAdapterName "Ethernet" -AllowManagementOS $true', '');
  put('New-VM -Name "SRV01" -MemoryStartupBytes 4GB -NewVHDPath "C:\\VMs\\SRV01.vhdx" -NewVHDSizeBytes 100GB -Generation 2 -SwitchName "External"',
    'Name State CPUUsage(%) MemoryAssigned(M) Uptime\n---- ----- ----------- ---------------- ------\nSRV01  Off   0           0                00:00:00');
  put('Get-VM | Where-Object {$_.State -eq "Running"} | Select-Object Name, State',
    'Name  State\n----  -----\nSRV01 Running');
  put('Checkpoint-VM -Name "SRV01" -SnapshotName "PrePatch"', '');
  put('Start-VM -Name "SRV01"', '');
  put('BACKUP DATABASE [SalesDB] TO DISK = \'E:\\Backups\\SalesDB_full.bak\' WITH INIT;',
    'Processed 1024 pages for database \'SalesDB\', file \'SalesDB\' on file 1.\nBACKUP DATABASE successfully processed 1024 pages in 1.204 seconds (6.667 MB/sec).');
  put('RESTORE DATABASE [SalesDB] FROM DISK = \'E:\\Backups\\SalesDB_full.bak\' WITH RECOVERY;',
    'Processed 1024 pages for database \'SalesDB\', file \'SalesDB\' on file 1.\nRESTORE DATABASE successfully processed 1024 pages in 0.982 seconds (8.192 MB/sec).');
  put('SELECT name, state_desc FROM sys.databases;',
    'name        state_desc\n----------- ----------\nmaster      ONLINE\ntempdb      ONLINE\nmodel       ONLINE\nmsdb        ONLINE\nSalesDB     ONLINE');
  put('DBCC CHECKDB (\'SalesDB\') WITH NO_INFOMSGS;', 'DBCC execution completed. If DBCC printed error messages, contact your system administrator.');
  put('Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name, CPU',
    'Name          CPU\n----          ---\nlsass       12.44\nsvchost     8.10\nsqlservr    5.02\nSystem        2.31\nsmss          0.98');
  put('Get-Service | Where-Object {$_.Status -eq "Running"} | Select-Object Name, DisplayName',
    'Name              DisplayName\n----              -----------\nDNS               DNS Server\nNTDS              Active Directory Domain Services\nNetlogon          Netlogon');
  put('Get-EventLog -LogName System -EntryType Error -Newest 20',
    'Index Time          EntryType Source       Message\n----- ----          --------- ------       -------\n48210 Oct 10 08:12  Error     DCOM         The server did not register with DCOM within the required timeout.');
  put('sfc /scannow',
    'Beginning system scan.  This process will take some time.\nBeginning verification phase of system scan.\nVerification 100% complete.\nWindows Resource Protection did not find any integrity violations.');
  put('dism /online /cleanup-image /restorehealth',
    'Deployment Image Servicing and Management tool\nVersion: 10.0.26100.1\n\n[==========================100.0%==========================]\nThe restore operation completed successfully.');
})();

function psNotRecognized(cmd) {
  var verb = normCmd(cmd).split(/\s+/)[0];
  return verb + ' : The term \'' + verb + '\' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.';
}

TermProfiles.powershell = {
  label: 'PowerShell',
  prompt: function () { return 'PS C:\\>'; },
  complete: ['Get-ADUser ', 'New-ADUser ', 'Set-ADUser ', 'Unlock-ADAccount ', 'Disable-ADAccount ', 'Set-ADAccountPassword ', 'New-ADOrganizationalUnit ', 'New-GPLink ', 'Add-ADGroupMember ', 'Get-ADComputer ', 'Add-DnsServerResourceRecordA ', 'Resolve-DnsName ', 'Add-DnsServerPrimaryZone ', 'Get-DnsServerZone ', 'Add-DhcpServerv4Scope ', 'Set-DhcpServerv4OptionValue ', 'Get-DhcpServerv4Lease ', 'ipconfig ', 'ping ', 'tracert ', 'nslookup ', 'netstat ', 'Test-NetConnection ', 'Get-NetIPAddress ', 'Get-Process ', 'Get-Service ', 'Get-EventLog ', 'Get-VM ', 'New-VM ', 'New-VMSwitch ', 'Checkpoint-VM ', 'Start-VM ', 'BACKUP DATABASE ', 'RESTORE DATABASE ', 'DBCC CHECKDB ', 'sfc ', 'dism ', 'netsh ', 'dnscmd ', 'Get-Help ', 'Clear-Host'],
  run: function (raw) {
    var cmd = normCmd(raw);
    if (!cmd) return '';
    if (/^(clear|cls)$/i.test(cmd)) return { clear: true };
    if (/^exit$/i.test(cmd)) return 'Use the profile switcher to change shells. (Simulated session — nothing to exit.)';
    if (/^Get-Help/i.test(cmd)) return 'PowerShell simulated help. Try: Get-ADUser, Test-NetConnection, Get-Process, Resolve-DnsName, Get-VM.';
    var key = normKey(cmd);
    if (PS_EXACT.hasOwnProperty(key)) return PS_EXACT[key];
    // verb heuristics
    var verb = cmd.split(/\s+/)[0];
    var v = verb.toLowerCase();
    if (/^(new|set|add|remove|enable|disable|unlock|checkpoint|start|stop|restart|move|rename|backup|restore)-/.test(v)) return '';
    if (/^get-/.test(v)) return '(no objects returned)';
    if (/^(ipconfig|ping|tracert|nslookup|netstat|netsh|dnscmd|sfc|dism)$/.test(v))
      return 'Usage: this simulated shell knows the drill commands exactly. Try "ipconfig /all", "ping -t 10.0.1.1", "tracert 8.8.8.8", "nslookup web01.corp.local", "netstat -ano".';
    return psNotRecognized(cmd);
  }
};

/* ---- bash ---- */
var BASH_EXACT = {};
(function () {
  function put(c, o) { BASH_EXACT[normKey(c)] = o; }
  put('ping -c 4 10.0.1.1',
    'PING 10.0.1.1 (10.0.1.1) 56(84) bytes of data.\n64 bytes from 10.0.1.1: icmp_seq=1 ttl=128 time=0.421 ms\n64 bytes from 10.0.1.1: icmp_seq=2 ttl=128 time=0.388 ms\n64 bytes from 10.0.1.1: icmp_seq=3 ttl=128 time=0.402 ms\n64 bytes from 10.0.1.1: icmp_seq=4 ttl=128 time=0.395 ms\n\n--- 10.0.1.1 ping statistics ---\n4 packets transmitted, 4 received, 0% packet loss, time 3004ms');
  put('traceroute 8.8.8.8',
    'traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets\n 1  10.0.1.1 (10.0.1.1)  0.512 ms  0.401 ms  0.388 ms\n 2  203.0.113.1 (203.0.113.1)  4.102 ms  3.988 ms  4.010 ms\n 3  dns.google (8.8.8.8)  8.771 ms  8.654 ms  8.702 ms');
  put('nslookup web01.corp.local',
    'Server:\t\t10.0.1.10\nAddress:\t10.0.1.10#53\n\nName:\tweb01.corp.local\nAddress: 10.0.1.50');
  put('dig web01.corp.local +short', '10.0.1.50');
  put('ip addr show',
    '2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500\n    inet 10.0.1.105/24 brd 10.0.1.255 scope global eth0');
  put('ip route show', 'default via 10.0.1.1 dev eth0\n10.0.1.0/24 dev eth0 proto kernel scope link src 10.0.1.105');
  put('whoami', 'admin');
  put('hostname', 'lab');
  put('pwd', '/home/admin');
  put('ls', 'notes.txt  scripts');
  put('ssh admin@10.0.1.10', 'admin@10.0.1.10\'s password: (simulated — no real connection made)');
})();
TermProfiles.bash = {
  label: 'Bash',
  prompt: function () { return 'admin@lab:~$'; },
  complete: ['ping ', 'traceroute ', 'nslookup ', 'dig ', 'ip ', 'ssh ', 'whoami', 'hostname', 'pwd', 'ls ', 'cat ', 'curl ', 'systemctl '],
  run: function (raw) {
    var cmd = normCmd(raw);
    if (!cmd) return '';
    if (/^clear$/.test(cmd)) return { clear: true };
    if (/^exit$/.test(cmd)) return 'Use the profile switcher to change shells. (Simulated session.)';
    var key = normKey(cmd);
    if (BASH_EXACT.hasOwnProperty(key)) return BASH_EXACT[key];
    if (/^ping\s/.test(key)) return 'PING ' + cmd.split(/\s+/)[1] + ': 4 packets transmitted, 4 received, 0% packet loss (simulated)';
    if (/^curl\s/.test(key)) return 'curl: (6) Could not resolve host — simulated shell has no network.';
    return 'bash: ' + cmd.split(/\s+/)[0] + ': command not found';
  }
};

/* ---- ios: reuse sims/ios-cli.js when present, else a small fallback ---- */
function iosFallbackRunFactory() {
  var mode = 'user', vlans = { 1: 'default' }, ctx = {};
  return {
    prompt: function () {
      if (mode === 'user') return 'SW1>';
      if (mode === 'enable') return 'SW1#';
      if (mode === 'config') return 'SW1(config)#';
      if (mode === 'config-if') return 'SW1(config-if)#';
      if (mode === 'config-vlan') return 'SW1(config-vlan)#';
      return 'SW1#';
    },
    run: function (raw) {
      var cmd = normCmd(raw), k = normKey(cmd);
      if (!cmd) return '';
      if (k === 'enable') { mode = 'enable'; return ''; }
      if (k === 'disable') { mode = 'user'; return ''; }
      if (k === 'exit') { mode = mode === 'user' ? 'user' : (mode === 'enable' ? 'user' : 'enable'); return ''; }
      if (k === 'end') { mode = 'enable'; return ''; }
      if (/^configure terminal$/.test(k) && (mode === 'enable' || mode === 'config')) { mode = 'config'; return 'Enter configuration commands, one per line.  End with CNTL/Z.'; }
      if (/^show vlan brief$/.test(k)) {
        var L = ['VLAN Name                             Status    Ports', '---- -------------------------------- --------- -------------------------------'];
        Object.keys(vlans).sort().forEach(function (id) { L.push((id + '   ').slice(0, 4) + ' ' + (vlans[id] + '                                ').slice(0, 32) + ' active'); });
        return L.join('\n');
      }
      if (/^show interfaces trunk$/.test(k)) return 'Port        Mode             Encapsulation  Status        Native vlan\nGi0/24      on               802.1q         trunking      1';
      if (/^vlan \d+$/.test(k) && mode === 'config') { var id = cmd.split(/\s+/)[1]; vlans[id] = 'VLAN' + id; mode = 'config-vlan'; ctx.vlan = id; return ''; }
      if (/^name \S+/.test(k) && mode === 'config-vlan') { vlans[ctx.vlan] = cmd.split(/\s+/)[1]; return ''; }
      if (/^interface /.test(k) && mode === 'config') { mode = 'config-if'; return ''; }
      if (/^switchport /.test(k) && mode === 'config-if') return '';
      if (/^copy running-config startup-config$/.test(k)) return 'Destination filename [startup-config]?\nBuilding configuration...\n[OK]';
      if (/^show running-config$/.test(k)) return 'Building configuration...\nCurrent configuration : 1842 bytes\n!\nhostname SW1\n!';
      if (mode === 'user' && /^(configure|vlan|interface|switchport)/.test(k)) return '% Invalid input detected at \'^\' marker.';
      return '% Invalid input detected at \'^\' marker.';
    }
  };
}
TermProfiles.ios = {
  label: 'Cisco IOS',
  _dev: null, _fb: null,
  prompt: function () {
    if (this._dev) return this._dev.prompt();
    if (!this._fb) this._fb = iosFallbackRunFactory();
    return this._fb.prompt();
  },
  complete: ['enable', 'configure terminal', 'vlan ', 'name ', 'interface ', 'switchport mode ', 'switchport access vlan ', 'switchport trunk allowed vlan ', 'show vlan brief', 'show interfaces trunk', 'show interfaces status', 'show running-config', 'copy running-config startup-config', 'end', 'exit', 'ping '],
  run: function (raw) {
    var cmd = normCmd(raw);
    if (!cmd) return '';
    if (typeof IOSDevice !== 'undefined') {
      if (!this._dev) {
        var ifs = [];
        for (var i = 1; i <= 24; i++) ifs.push('gi0/' + i);
        this._dev = new IOSDevice({ hostname: 'SW1', type: 'switch', interfaces: ifs });
      }
      if (/^exit$/i.test(cmd) && this._dev.mode() === 'user') return 'Use the profile switcher to change shells. (Simulated device.)';
      try { return this._dev.exec(cmd); } catch (e) { return '% Error: ' + e.message; }
    }
    if (!this._fb) this._fb = iosFallbackRunFactory();
    return this._fb.run(cmd);
  }
};

/* ---- fortios ---- */
function fortiosCfg() {
  return {
    mode: 'exec', ctx: null,
    prompt: function () {
      if (this.mode === 'phase1') return 'FGT-HQ (phase1-interface) #';
      if (this.mode === 'edit') return 'FGT-HQ (' + this.ctx + ') #';
      return 'FGT-HQ #';
    },
    run: function (raw) {
      var cmd = normCmd(raw), k = normKey(cmd);
      if (!cmd) return '';
      if (this.mode === 'exec') {
        if (k === 'get system status')
          return 'Version: FortiGate-60F v7.4.3,build2573\nSerial-Number: FGT60FTK12345678\nHostname: FGT-HQ\nOperation Mode: NAT\nSystem Time: ' + new Date().toUTCString();
        if (k === 'get system interface')
          return '== [ wan1 ]\nname: wan1   mode: dhcp   ip: 203.0.113.44/24   status: up\n== [ lan ]\nname: lan   mode: static   ip: 10.0.1.1/24   status: up';
        if (k === 'get router info routing-table all')
          return 'S*      0.0.0.0/0 [10/0] via 203.0.113.1, wan1\nC       10.0.1.0/24 is directly connected, lan\nC       203.0.113.0/24 is directly connected, wan1';
        if (k === 'diagnose vpn tunnel list')
          return 'list all ipsec tunnel in vd 0\n------------------------------------------------------\nname=HQ-Tampa ver=2 serial=1 203.0.113.44:0->198.51.100.10:0\nbound_if=3 lgwy=static/1 tun=intf/0 mode=auto/1 encap=none/512\nproxyid_num=1 child_num=0 refcnt=14 ilast=2 olast=2 ad=/0\nstat: rxp=12401 txp=11877 rxb=10485760 txb=9437184\nrun_tally=0';
        if (k === 'diagnose vpn ike gateway list')
          return 'vd: root/0\nname: HQ-Tampa\nversion: 2\ninterface: wan1\naddr: 203.0.113.44:500 -> 198.51.100.10:500\ncreated: 84211s ago\nIKE SA: created 1/1  established 1/1  time 60/60/60 ms\nIPsec SA: created 1/1  established 1/1  time 30/30/30 ms';
        if (/^diagnose sniffer packet /.test(k))
          return 'interfaces=[any]\nfilters=[host 10.0.1.50]\n2.512341 lan in 10.0.1.105 -> 10.0.1.50: icmp: echo request\n2.512402 lan out 10.0.1.50 -> 10.0.1.105: icmp: echo reply';
        if (/^execute ping /.test(k)) {
          var ip = cmd.split(/\s+/)[2] || '10.0.1.1';
          return 'PING ' + ip + ' (' + ip + '): 56 data bytes\n64 bytes from ' + ip + ': icmp_seq=0 ttl=128 time=0.8 ms\n64 bytes from ' + ip + ': icmp_seq=1 ttl=128 time=0.6 ms\n--- ' + ip + ' ping statistics ---\n2 packets transmitted, 2 packets received, 0% packet loss';
        }
        if (/^execute traceroute /.test(k)) return 'traceroute to 8.8.8.8, 30 hops max\n 1  10.0.1.1  0.512 ms\n 2  203.0.113.1  4.102 ms\n 3  8.8.8.8  8.771 ms';
        if (/^config vpn ipsec phase1-interface$/.test(k)) { this.mode = 'phase1'; return ''; }
        if (k === 'show') return 'config vpn ipsec phase1-interface\n    edit "HQ-Tampa"\n        set peertype any\n        set proposal aes256-sha256\n        set psksecret ENC <redacted>\n    next\nend';
        return 'Command fail. Return code -1';
      }
      if (this.mode === 'phase1') {
        var m = /^edit\s+"?([^"]+)"?$/.exec(cmd);
        if (m) { this.mode = 'edit'; this.ctx = m[1]; return ''; }
        if (k === 'end') { this.mode = 'exec'; return ''; }
        return 'Command fail. Return code -1';
      }
      if (this.mode === 'edit') {
        if (/^set\s+\S+/.test(k)) return '';
        if (k === 'next') { this.mode = 'phase1'; this.ctx = null; return ''; }
        if (k === 'end') { this.mode = 'exec'; this.ctx = null; return ''; }
        return 'Command fail. Return code -1';
      }
      return 'Command fail. Return code -1';
    }
  };
}
TermProfiles.fortios = {
  label: 'FortiOS',
  _s: null,
  prompt: function () { if (!this._s) this._s = fortiosCfg(); return this._s.prompt(); },
  complete: ['get system status', 'get system interface', 'get router info routing-table all', 'diagnose vpn tunnel list', 'diagnose vpn ike gateway list', 'diagnose sniffer packet any ', 'execute ping ', 'execute traceroute ', 'config vpn ipsec phase1-interface', 'show', 'end', 'edit ', 'set ', 'next'],
  run: function (raw) { if (!this._s) this._s = fortiosCfg(); return this._s.run(raw); }
};

/* ---- panos ---- */
function panosCfg() {
  return {
    mode: 'oper',
    prompt: function () { return this.mode === 'config' ? 'admin@PA-220#' : 'admin@PA-220>'; },
    run: function (raw) {
      var cmd = normCmd(raw), k = normKey(cmd);
      if (!cmd) return '';
      if (this.mode === 'oper') {
        if (k === 'show system info')
          return 'hostname: PA-220\nmodel: PA-220\nsw-version: 11.1.4-h2\nuptime: 42 days, 6:12:33';
        if (k === 'show interface all')
          return '--------------------------------------------------------------------------------\nName                Link  State   IP Address\n--------------------------------------------------------------------------------\nethernet1/1         up    up      203.0.113.44/24\nethernet1/2         up    up      10.0.1.1/24';
        if (k === 'show vpn ike-sa')
          return 'GwID/client IP           Peer-addr      State   Role  \nHQ-Tampa/203.0.113.44    198.51.100.10  ACTIVE  Initiator';
        if (k === 'show vpn ipsec-sa')
          return 'Tunnel                   State    ProxyID\nHQ-Tampa               active   10.0.1.0/24-192.168.20.0/24';
        var tm = /^test vpn ipsec-sa tunnel\s+(\S+)$/.exec(cmd);
        if (tm) return 'IPSec SA test for tunnel ' + tm[1] + ': SA is active, 2 SPIs installed. Test PASSED.';
        var pm = /^ping host\s+(\S+)$/.exec(cmd);
        if (pm) return 'PING ' + pm[1] + ' : 56 data bytes\n64 bytes from ' + pm[1] + ': icmp_seq=0 ttl=128 time=0.7 ms\n--- ' + pm[1] + ' ping statistics ---\n1 packets transmitted, 1 received, 0% packet loss';
        if (k === 'configure') { this.mode = 'config'; return 'Entering configuration mode'; }
        return 'Unknown command: ' + cmd.split(/\s+/)[0];
      }
      if (/^set\s+/.test(k)) return '';
      if (k === 'commit') return '\nCommit Successful\n';
      if (k === 'exit') { this.mode = 'oper'; return 'Exiting configuration mode'; }
      return 'Unknown command: ' + cmd.split(/\s+/)[0];
    }
  };
}
TermProfiles.panos = {
  label: 'PAN-OS',
  _s: null,
  prompt: function () { if (!this._s) this._s = panosCfg(); return this._s.prompt(); },
  complete: ['show system info', 'show interface all', 'show vpn ike-sa', 'show vpn ipsec-sa', 'test vpn ipsec-sa tunnel ', 'ping host ', 'configure', 'set ', 'commit', 'exit'],
  run: function (raw) { if (!this._s) this._s = panosCfg(); return this._s.run(raw); }
};

/* ---- the component ---- */
function createTerminal(mount, opts) {
  opts = opts || {};
  var profileId = opts.profile || 'powershell';
  var onCommand = opts.onCommand || null;
  var prof = TermProfiles[profileId];
  var hist = [], hIdx = -1;

  mount.innerHTML =
    '<div class="term-bar"><label>Shell <select class="term-profile">' +
    Object.keys(TermProfiles).map(function (id) {
      return '<option value="' + id + '"' + (id === profileId ? ' selected' : '') + '>' + esc(TermProfiles[id].label) + '</option>';
    }).join('') + '</select></label>' +
    '<button class="btn small ghost term-clear">clear</button></div>' +
    '<div class="term-out" aria-live="polite"></div>' +
    '<div class="term-line"><span class="term-prompt"></span><input class="term-in" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="Terminal input"></div>';

  var out = $('.term-out', mount), inp = $('.term-in', mount), promptEl = $('.term-prompt', mount);
  function refreshPrompt() { promptEl.textContent = prof.prompt(); }
  function print(text, cls) {
    if (text == null || text === '') return;
    var d = document.createElement('div');
    d.className = 'term-' + (cls || 'out');
    d.textContent = text;
    out.appendChild(d);
    out.scrollTop = out.scrollHeight;
  }
  function printCmd(cmd) {
    var d = document.createElement('div');
    d.className = 'term-echo';
    var s = document.createElement('span'); s.className = 'term-prompt-echo'; s.textContent = prof.prompt() + ' ';
    var c = document.createElement('span'); c.textContent = cmd;
    d.appendChild(s); d.appendChild(c);
    out.appendChild(d);
  }
  refreshPrompt();
  print(opts.welcome || (prof.label + ' simulator — practice safely. Type "clear" to clear.'));

  function execCmd(cmd) {
    printCmd(cmd);
    if (cmd.trim()) { hist.unshift(cmd); hIdx = -1; }
    var res;
    try { res = prof.run(cmd); } catch (e) { res = 'Error: ' + e.message; }
    if (res && typeof res === 'object' && res.clear) { out.innerHTML = ''; }
    else if (typeof res === 'string') print(res);
    refreshPrompt();
    out.scrollTop = out.scrollHeight;
    if (onCommand) { try { onCommand(cmd, res); } catch (e) {} }
  }

  inp.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') { execCmd(inp.value); inp.value = ''; }
    else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (hist.length) { hIdx = Math.min(hIdx + 1, hist.length - 1); inp.value = hist[hIdx]; }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (hIdx > 0) { hIdx--; inp.value = hist[hIdx]; } else { hIdx = -1; inp.value = ''; }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      var cur = inp.value;
      var cands = (prof.complete || []).filter(function (c) { return c.toLowerCase().indexOf(cur.toLowerCase()) === 0; });
      if (cands.length === 1) inp.value = cands[0];
      else if (cands.length > 1) {
        var pfx = cands[0];
        for (var i = 1; i < cands.length; i++) {
          var j = 0;
          while (j < pfx.length && j < cands[i].length && pfx[j].toLowerCase() === cands[i][j].toLowerCase()) j++;
          pfx = pfx.slice(0, j);
        }
        if (pfx.length > cur.length) inp.value = pfx;
        else print(cands.join('   '), 'hint');
      }
    }
  });
  $('.term-profile', mount).addEventListener('change', function (e) {
    profileId = e.target.value;
    prof = TermProfiles[profileId];
    hist = []; hIdx = -1;
    print('— switched to ' + prof.label + ' —', 'hint');
    refreshPrompt();
    inp.focus();
  });
  $('.term-clear', mount).addEventListener('click', function () { out.innerHTML = ''; inp.focus(); });
  mount.addEventListener('click', function (e) {
    if (e.target === mount || e.target === out) inp.focus();
  });
  return {
    focus: function () { inp.focus(); },
    print: print,
    exec: execCmd,
    get profile() { return profileId; }
  };
}

function viewTerminal() {
  var h = '<div class="wrap"><div class="view-head"><p class="eyebrow">HANDS-ON</p><h2>Terminal</h2>';
  h += '<p class="muted">A simulated shell — practice commands safely. Five profiles: PowerShell, Bash, Cisco IOS, FortiOS, PAN-OS. Everything runs locally.</p></div>';
  h += '<div class="panel"><div id="mainTerm"></div></div>';
  h += '<div class="panel"><h3>Try these</h3><div class="try-grid">';
  var tries = [
    ['powershell', 'Test-NetConnection -ComputerName 10.0.1.1 -Port 443', 'Prove a TCP port is reachable'],
    ['powershell', 'Get-ADUser -Filter \'Name -eq "jdoe"\' -Properties *', 'Look up an AD user'],
    ['ios', 'show vlan brief', 'VLAN summary on the switch'],
    ['fortios', 'diagnose vpn tunnel list', 'IPsec tunnel status'],
    ['panos', 'show vpn ipsec-sa', 'IPsec SAs on PAN-OS'],
    ['bash', 'traceroute 8.8.8.8', 'Trace the path (Linux name)']
  ];
  tries.forEach(function (t, i) {
    h += '<button class="try-cmd" data-try="' + i + '"><code>' + esc(t[1]) + '</code><span>' + esc(t[2]) + ' · ' + esc(TermProfiles[t[0]].label) + '</span></button>';
  });
  h += '</div></div></div>';
  setTimeout(function () {
    var mount = $('#mainTerm');
    if (!mount) return;
    var term = createTerminal(mount, { profile: 'powershell' });
    $all('.try-cmd').forEach(function (b) {
      b.onclick = function () {
        var t = tries[+b.dataset.try];
        var sel = $('.term-profile', mount);
        if (sel && sel.value !== t[0]) { sel.value = t[0]; sel.dispatchEvent(new Event('change')); }
        term.exec(t[1]);
        mount.scrollIntoView({ behavior: 'smooth', block: 'center' });
      };
    });
  }, 0);
  return h;
}
function initTerminalView() { /* wired in viewTerminal via setTimeout */ }

/* ==================== 11. LAB VIEW ========================================= */
function viewLab(labId) {
  var lab = Content.labById[labId];
  if (!lab) return '<div class="wrap"><div class="panel"><p>Unknown lab.</p><a class="btn" href="#/learn">Back</a></div></div>';
  var st = Store.state.labs[labId] || {};
  var dom = Content.domainById[lab.domain_id];
  var h = '<div class="wrap"><a class="back" href="#/module/' + esc(lab.domain_id) + '">← ' + esc(dom.name) + '</a>';
  h += '<p class="eyebrow">HANDS-ON LAB</p><h2>' + esc(lab.title) + '</h2>';
  h += '<div class="panel"><h3>Objective</h3><p>' + esc(lab.objective) + '</p></div>';
  h += '<div class="panel"><h3>Steps</h3><div class="steps">';
  lab.steps.forEach(function (s, i) {
    var done = st.steps && st.steps[i];
    h += '<label class="step"><input type="checkbox" data-step="' + i + '"' + (done ? ' checked' : '') + '><span>' + esc(s) + '</span></label>';
  });
  h += '</div></div>';
  h += '<div class="panel"><h3>Validate in the terminal</h3><p class="muted">Run the commands below — checks validate automatically as you type.</p><div id="labTerm"></div><div class="checks" id="labChecks">';
  lab.checks.forEach(function (c, i) {
    var ok = st.checks && st.checks[i];
    h += '<div class="check' + (ok ? ' ok' : '') + '" data-check="' + i + '"><span>' + (ok ? '✓' : '○') + '</span><span>Check ' + (i + 1) + ': <code>' + esc(c.command_pattern) + '</code></span></div>';
  });
  h += '</div></div>';
  h += '<div class="action-row"><button class="btn primary" id="labDone">' + (st.completed ? '✓ Lab complete' : 'Mark lab complete') + '</button></div>';
  h += '<div class="feedback" id="labWin" style="display:' + (st.completed ? 'block' : 'none') + '"><strong>✓ ' + esc(lab.success_message || 'Lab complete.') + '</strong></div>';
  h += '</div>';
  return h;
}
function initLabView(labId) {
  var lab = Content.labById[labId];
  if (!lab) return;
  var mount = $('#labTerm');
  function getSt() {
    if (!Store.state.labs[labId]) Store.state.labs[labId] = { steps: {}, checks: {} };
    return Store.state.labs[labId];
  }
  $all('#view .step input').forEach(function (cb) {
    cb.onchange = function () {
      var st = getSt();
      st.steps = st.steps || {};
      if (cb.checked) st.steps[+cb.dataset.step] = true; else delete st.steps[+cb.dataset.step];
      st.updatedAt = Date.now();
      Store.save();
    };
  });
  var regexes = lab.checks.map(function (c) {
    try { return new RegExp(c.command_pattern, 'i'); } catch (e) { return null; }
  });
  var term = createTerminal(mount, {
    profile: 'powershell',
    welcome: 'Lab terminal (PowerShell) — run the lab steps here. Checks validate automatically.',
    onCommand: function (cmd) {
      var st = getSt();
      st.checks = st.checks || {};
      var hit = false;
      regexes.forEach(function (re, i) {
        if (re && !st.checks[i] && re.test(cmd)) {
          st.checks[i] = true; hit = true;
          var el = $('.check[data-check="' + i + '"]');
          if (el) { el.classList.add('ok'); el.querySelector('span').textContent = '✓'; }
          term.print('✓ Check ' + (i + 1) + ' passed', 'ok');
        }
      });
      if (hit) {
        st.updatedAt = Date.now();
        Store.save();
        var all = lab.checks.every(function (_, i) { return st.checks[i]; });
        if (all) {
          term.print('All checks passed — ' + (lab.success_message || 'lab complete.'), 'ok');
          $('#labWin').style.display = 'block';
          $('#labWin').innerHTML = '<strong>✓ ' + esc(lab.success_message || 'Lab complete.') + '</strong>';
          $('#labDone').textContent = '✓ Lab complete';
        }
      }
    }
  });
  $('#labDone').onclick = function () {
    var st = getSt();
    st.completed = true;
    st.updatedAt = Date.now();
    Store.save();
    $('#labDone').textContent = '✓ Lab complete';
    $('#labWin').style.display = 'block';
    $('#labWin').innerHTML = '<strong>✓ ' + esc(lab.success_message || 'Lab complete.') + '</strong>';
    toast('Lab marked complete');
  };
}

/* ==================== 12. DRILLS VIEW ====================================== */
function drillCategories() {
  var cmds = (Content.drillData && Content.drillData.commands) || [];
  var cats = [];
  cmds.forEach(function (c) { if (cats.indexOf(c.category) < 0) cats.push(c.category); });
  return cats;
}
function drillScore(c) {
  // mastery score: higher = stronger. Used for adaptive weighting.
  var r = Store.state.drills[c.id];
  if (!r || !r.attempts) return 0;
  var acc = r.correct / r.attempts;
  var speed = r.bestMs ? Math.max(0, Math.min(1, 1 - (r.bestMs - 4000) / 12000)) : 0;
  return acc * 0.6 + speed * 0.4;
}
function pickDrillCommand(cat) {
  var cmds = ((Content.drillData && Content.drillData.commands) || []).filter(function (c) {
    return !cat || cat === 'all' || c.category === cat;
  });
  if (!cmds.length) return null;
  // adaptive: weight inversely to mastery so weak items appear more often
  var weights = cmds.map(function (c) { return 1.6 - drillScore(c); });
  var total = weights.reduce(function (a, b) { return a + b; }, 0);
  var roll = Math.random() * total;
  for (var i = 0; i < cmds.length; i++) { roll -= weights[i]; if (roll <= 0) return cmds[i]; }
  return cmds[cmds.length - 1];
}
function recordDrillAttempt(cmd, ms, correct, peeked) {
  var r = Store.state.drills[cmd.id] || { attempts: 0, correct: 0, totalMs: 0, bestMs: 0, mastered: false };
  r.attempts++;
  r.totalMs += ms;
  if (correct && !peeked) {
    r.correct++;
    if (!r.bestMs || ms < r.bestMs) r.bestMs = Math.round(ms);
    if (r.bestMs < 10000) r.mastered = true;
  } else if (!correct) {
    r.mastered = false;
  }
  r.lastPeeked = !!peeked;
  r.updatedAt = Date.now();
  Store.state.drills[cmd.id] = r;
  srUpdate(cmd.id, !correct ? 2 : (ms < 10000 && !peeked ? 5 : 4));
  Store.save();
  return r;
}

function viewDrills(mode, query) {
  mode = mode || 'speed';
  var h = '<div class="wrap"><div class="view-head"><p class="eyebrow">MUSCLE MEMORY</p><h2>Drills</h2>';
  h += '<p class="muted">Sub-10-second recall, blind. Adaptive: slow or missed commands come back more often.</p></div>';
  h += '<div class="tabs" role="tablist">';
  [['speed', '⚡ Speed'], ['blind', '🙈 Blind'], ['sequences', '🔗 Sequences'], ['errors', '🛠 Error recovery'], ['sprint', '🏁 Sprint'], ['daily', '📅 Daily sets']].forEach(function (t) {
    h += '<button class="tab' + (mode === t[0] ? ' active' : '') + '" data-dmode="' + t[0] + '" role="tab">' + t[1] + '</button>';
  });
  h += '</div><div id="drillBody"></div></div>';
  setTimeout(function () {
    $all('.tab').forEach(function (b) {
      b.onclick = function () { go('#/drills/' + b.dataset.dmode); };
    });
  }, 0);
  return h;
}

function initDrillsView(mode, query) {
  mode = mode || 'speed';
  var body = $('#drillBody');
  if (!body) return;
  if (mode === 'speed') drillSpeedUI(body, false, query);
  else if (mode === 'blind') drillSpeedUI(body, true, query);
  else if (mode === 'sequences') drillSequencesUI(body);
  else if (mode === 'errors') drillErrorsUI(body);
  else if (mode === 'sprint') drillSprintUI(body);
  else if (mode === 'daily') drillDailyUI(body);
}

/* ---- speed / blind drill ---- */
function drillSpeedUI(body, blind, query) {
  var cats = drillCategories();
  var presetCmd = null;
  var qm = /cmd=([^&]+)/.exec(query || '');
  if (qm) {
    try { presetCmd = drillCommandById(decodeURIComponent(qm[1])); }
    catch (e) { presetCmd = null; } // malformed % escapes: ignore the preset
  }
  body.innerHTML =
    '<div class="panel"><div class="row"><select id="dCat" class="select">' +
    '<option value="all">All categories</option>' +
    cats.map(function (c) { return '<option>' + esc(c) + '</option>'; }).join('') +
    '</select><button class="btn" id="dNew">New drill</button></div>' +
    '<p class="muted" style="margin-top:8px">Read the prompt, type the command exactly. Timer starts on your first keystroke. Whitespace is forgiven — syntax is not.</p>' +
    '<div class="terminal"><div class="prompt-line" id="dPrompt">Press “New drill” to begin.</div>' +
    '<div class="hidden-box" id="dBlindBox" style="display:none">Prompt hidden — type from memory. <button class="btn ghost" id="dReveal" style="min-height:32px;padding:4px 12px;font-size:.75rem">Reveal (marks peeked)</button></div>' +
    '<div class="row" style="justify-content:space-between"><span class="timer" id="dTimer">0.0s</span><span id="dMeta" class="muted"></span></div>' +
    '<input class="cmd-input" id="dInput" placeholder="type the command here, press Enter" autocomplete="off" autocapitalize="off" spellcheck="false">' +
    '<div class="feedback" id="dFb"></div></div>' +
    '<div class="row"><button class="btn ghost" id="dNext" disabled>Next command →</button><button class="btn ghost" id="dShow" disabled>Show answer</button></div>' +
    '<div class="stat-grid">' + statCell('reps', '0', 'this session') + statCell('accuracy', '—', '') + statCell('best', '—', 'this session') + '</div></div>';

  var cur = null, t0 = 0, ticking = false, peeked = false, blindTimer = null;
  var reps = 0, okCount = 0, best = 0;
  var $p = $('#dPrompt'), $t = $('#dTimer'), $m = $('#dMeta'), $in = $('#dInput'), $fb = $('#dFb');

  function stats() {
    var cells = $all('.stat .v', body);
    if (cells[0]) cells[0].textContent = reps;
    if (cells[1]) cells[1].textContent = reps ? Math.round(okCount / reps * 100) + '%' : '—';
    if (cells[2]) cells[2].textContent = best ? fmtSec(best) : '—';
  }
  function newDrill(forced) {
    clearTimeout(blindTimer);
    peeked = false;
    cur = forced || pickDrillCommand($('#dCat').value);
    if (!cur) { $p.textContent = 'No drill data available.'; return; }
    $p.innerHTML = '<span class="d-cat">' + esc(cur.category) + '</span> ' + esc(cur.context);
    $('#dBlindBox').style.display = 'none';
    if (blind) {
      var n = 3;
      $m.textContent = 'hiding in ' + n + '…';
      blindTimer = setInterval(function () {
        n--;
        if (n <= 0) {
          clearInterval(blindTimer);
          $p.innerHTML = '<span class="d-cat">' + esc(cur.category) + '</span> <em>hidden — type from memory</em>';
          $('#dBlindBox').style.display = '';
          $m.textContent = 'blind';
        } else $m.textContent = 'hiding in ' + n + '…';
      }, 1000);
      Timers.add(blindTimer); // killed on hash change like every other drill timer
    } else $m.textContent = esc(cur.category);
    $fb.className = 'feedback'; $fb.innerHTML = '';
    $in.value = ''; $in.disabled = false; $in.focus();
    ticking = false; t0 = 0; $t.textContent = '0.0s';
    $('#dNext').disabled = true; $('#dShow').disabled = false;
  }
  $in.addEventListener('input', function () {
    if (!ticking && $in.value.length) { ticking = true; t0 = Date.now(); }
    if (ticking) $t.textContent = ((Date.now() - t0) / 1000).toFixed(1) + 's';
  });
  function submit() {
    if (!cur || !ticking && !$in.value) return;
    var ms = ticking ? Date.now() - t0 : 0;
    var typed = normCmd($in.value), want = normCmd(cur.command);
    var correct = typed === want;
    clearTimeout(blindTimer);
    reps++;
    if (correct && !peeked) { okCount++; if (!best || ms < best) best = ms; }
    recordDrillAttempt(cur, ms, correct, peeked);
    $fb.className = 'feedback ' + (correct ? 'ok' : 'no');
    $fb.innerHTML = correct
      ? '✓ <strong>' + fmtSec(ms) + '</strong>' + (ms < 10000 && !peeked ? ' <span class="badge sub10">sub-10s</span>' : peeked ? ' <span class="badge peeked">peeked</span>' : ' <span class="badge slow">slow</span>')
      : '✗ Expected:<pre class="code">' + esc(cur.command) + '</pre>';
    $in.disabled = true;
    $('#dNext').disabled = false; $('#dShow').disabled = true;
    stats();
  }
  $in.addEventListener('keydown', function (e) { if (e.key === 'Enter') submit(); });
  $('#dNew').onclick = function () { newDrill(); };
  $('#dNext').onclick = function () { newDrill(); };
  $('#dShow').onclick = function () {
    if (!cur) return;
    peeked = true;
    $fb.className = 'feedback';
    $fb.innerHTML = '<pre class="code">' + esc(cur.command) + '</pre><p class="muted">Answer shown — this rep is marked peeked.</p>';
  };
  var rv = $('#dReveal');
  if (rv) rv.onclick = function () {
    peeked = true;
    $p.innerHTML = '<span class="d-cat">' + esc(cur.category) + '</span> ' + esc(cur.context);
    $('#dBlindBox').style.display = 'none';
  };
  stats();
  if (presetCmd) { newDrill(presetCmd); } else { $p.textContent = 'Press “New drill” to begin.'; }
}

/* ---- sequences ---- */
function drillSequencesUI(body) {
  var seqs = (Content.drillData && Content.drillData.sequences) || [];
  body.innerHTML = '<div class="panel"><div class="row"><select id="sSel" class="select" style="flex:1">' +
    seqs.map(function (s, i) { return '<option value="' + i + '">' + esc(s.title) + ' (' + s.steps.length + ' steps)</option>'; }).join('') +
    '</select><button class="btn" id="sStart">Start sequence</button></div>' +
    '<div class="terminal" id="sTerm" style="display:none"><div class="seq-step" id="sStep"></div>' +
    '<div class="prompt-line" id="sScenario"></div>' +
    '<div class="row" style="justify-content:space-between"><span class="timer" id="sTimer">0.0s</span><span id="sMeta" class="muted"></span></div>' +
    '<input class="cmd-input" id="sInput" placeholder="type step command, press Enter" autocomplete="off" autocapitalize="off" spellcheck="false">' +
    '<div class="feedback" id="sFb"></div></div><div id="sDone"></div></div>';
  var seq = null, si = 0, t0 = 0, wrong = 0, timerId = null;
  $('#sStart').onclick = function () {
    seq = seqs[+$('#sSel').value]; si = 0; wrong = 0; t0 = Date.now();
    $('#sTerm').style.display = ''; $('#sDone').innerHTML = '';
    $('#sScenario').textContent = seq.scenario;
    showStep();
    $('#sInput').value = ''; $('#sInput').focus();
    clearInterval(timerId);
    timerId = setInterval(function () { $('#sTimer').textContent = ((Date.now() - t0) / 1000).toFixed(1) + 's'; }, 100);
    Timers.add(timerId);
  };
  function showStep() {
    $('#sStep').textContent = 'Step ' + (si + 1) + ' of ' + seq.steps.length;
    $('#sMeta').textContent = si + '/' + seq.steps.length + ' · ' + wrong + ' miss(es)';
    $('#sFb').className = 'feedback'; $('#sFb').innerHTML = '';
  }
  $('#sInput').addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' || !seq) return;
    var want = normCmd(seq.steps[si]);
    if (normCmd($('#sInput').value) === want) {
      si++;
      if (si >= seq.steps.length) {
        clearInterval(timerId);
        var ms = Date.now() - t0;
        $('#sTerm').style.display = 'none';
        $('#sDone').innerHTML = '<div class="feedback ok" style="display:block">✓ Sequence complete in ' + fmtSec(ms) + ' with ' + wrong + ' miss(es).</div><div class="row"><button class="btn ghost" id="sAgain">Run again</button></div>';
        $('#sAgain').onclick = function () { $('#sStart').click(); };
        seq.steps.forEach(function (st) {
          var fake = { id: 'seq:' + seq.id + ':' + slugify(st).slice(0, 40), command: st };
          recordDrillAttempt(fake, ms / seq.steps.length, true, false);
        });
      } else { $('#sInput').value = ''; showStep(); }
    } else {
      wrong++;
      $('#sFb').className = 'feedback no';
      $('#sFb').textContent = '✗ Wrong step — check the syntax and try again. (' + wrong + ' miss)';
      showStep();
    }
  });
}

/* ---- error recovery ---- */
function drillErrorsUI(body) {
  var errs = (Content.drillData && Content.drillData.error_recovery) || [];
  body.innerHTML = '<div class="panel"><div class="row"><button class="btn" id="eNew">New error trap</button><span id="eMeta" class="muted"></span></div>' +
    '<div class="terminal" id="eTerm" style="display:none"><div class="prompt-line">Broken command:</div><pre class="bad" id="eBroken"></pre>' +
    '<div class="prompt-line" style="margin-top:10px">Error output:</div><pre class="err" id="eOutput"></pre>' +
    '<input class="cmd-input" id="eInput" placeholder="type the fix, press Enter" autocomplete="off" autocapitalize="off" spellcheck="false">' +
    '<div class="feedback" id="eFb"></div><div class="explain" id="eExplain" style="display:none"></div></div>' +
    '<div class="row"><button class="btn ghost" id="eNext" style="display:none">Next trap →</button></div></div>';
  var cur = null, order = shuffle(errs.map(function (_, i) { return i; }), mulberry32(Date.now() % 100000)), ei = 0;
  function show() {
    cur = errs[order[ei % order.length]]; ei++;
    $('#eTerm').style.display = '';
    $('#eBroken').textContent = cur.broken_command;
    $('#eOutput').textContent = cur.error_output;
    $('#eInput').value = ''; $('#eInput').disabled = false; $('#eInput').focus();
    $('#eFb').className = 'feedback'; $('#eFb').innerHTML = '';
    $('#eExplain').style.display = 'none';
    $('#eMeta').textContent = 'trap ' + cur.id;
    $('#eNext').style.display = 'none';
  }
  $('#eNew').onclick = show;
  $('#eNext').onclick = show;
  $('#eInput').addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' || !cur) return;
    var ok = normCmd($('#eInput').value) === normCmd(cur.fix);
    $('#eFb').className = 'feedback ' + (ok ? 'ok' : 'no');
    $('#eFb').innerHTML = ok ? '✓ Fixed.' : '✗ Not the fix — compare carefully and try again.';
    if (ok) {
      $('#eExplain').style.display = '';
      $('#eExplain').innerHTML = '<strong>Why it failed:</strong> ' + esc(cur.explanation);
      $('#eInput').disabled = true;
      $('#eNext').style.display = '';
      recordDrillAttempt({ id: 'err:' + cur.id, command: cur.fix }, 8000, true, false);
    }
  });
}

/* ---- sprint ---- */
function drillSprintUI(body) {
  var tasks = ((Content.drillData && Content.drillData.sprint) || {}).tasks || [];
  var mins = ((Content.drillData && Content.drillData.sprint) || {}).duration_minutes || 30;
  body.innerHTML = '<div class="panel"><p class="muted">' + tasks.length + ' rapid-fire tasks, ' + mins + '-minute countdown. Back-to-back, no pausing. Enter submits — or skip (counts as miss).</p>' +
    '<div class="row"><button class="btn" id="spStart">Start ' + mins + '-minute sprint</button></div>' +
    '<div class="terminal" id="spTerm" style="display:none"><div class="big-clock" id="spClock">' + mins + ':00</div>' +
    '<div class="seq-step" id="spStep"></div><div class="prompt-line" id="spPrompt"></div>' +
    '<input class="cmd-input" id="spInput" placeholder="type the command, press Enter" autocomplete="off" autocapitalize="off" spellcheck="false">' +
    '<div class="feedback" id="spFb"></div>' +
    '<div class="row" style="margin-top:8px"><button class="btn warn" id="spSkip">Skip (counts as miss)</button></div></div>' +
    '<div id="spDone"></div></div>';
  var i = 0, ok = 0, miss = 0, endAt = 0, timerId = null, order = [];
  function finish() {
    clearInterval(timerId);
    $('#spTerm').style.display = 'none';
    var total = ok + miss;
    $('#spDone').innerHTML = '<div class="feedback ' + (ok / Math.max(1, total) >= 0.8 ? 'ok' : 'no') + '" style="display:block">Sprint done: <strong>' + ok + '/' + total + '</strong> correct (' + Math.round(ok / Math.max(1, total) * 100) + '%).</div>' +
      '<div class="row"><button class="btn ghost" id="spAgain">Run again</button></div>';
    $('#spAgain').onclick = function () { $('#spStart').click(); };
  }
  function show() {
    if (!$('#spStep')) return; // view torn down (hash change) while a one-shot was pending
    if (i >= order.length) { finish(); return; }
    var t = tasks[order[i]];
    $('#spStep').textContent = 'Task ' + (i + 1) + ' of ' + order.length;
    $('#spPrompt').textContent = t.prompt;
    $('#spInput').value = ''; $('#spInput').focus();
    $('#spFb').className = 'feedback'; $('#spFb').innerHTML = '';
  }
  function grade(gotIt) {
    var t = tasks[order[i]];
    var good = gotIt && t.expected_commands.some(function (ec) { return normCmd($('#spInput').value) === normCmd(ec); });
    if (good) { ok++; $('#spFb').className = 'feedback ok'; $('#spFb').textContent = '✓'; }
    else { miss++; $('#spFb').className = 'feedback no'; $('#spFb').innerHTML = '✗ Expected:<pre class="code">' + esc(t.expected_commands[0]) + '</pre>'; }
    i++;
    setTimeout(show, good ? 500 : 1600);
  }
  $('#spStart').onclick = function () {
    order = shuffle(tasks.map(function (_, x) { return x; }), mulberry32(Date.now() % 100000));
    i = 0; ok = 0; miss = 0;
    endAt = Date.now() + mins * 60000;
    $('#spTerm').style.display = ''; $('#spDone').innerHTML = '';
    clearInterval(timerId);
    timerId = setInterval(function () {
      var left = Math.max(0, endAt - Date.now());
      var el = $('#spClock');
      if (el) el.textContent = fmtClock(left / 1000);
      if (left <= 0) finish();
    }, 500);
    Timers.add(timerId);
    show();
  };
  $('#spInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') grade(true); });
  $('#spSkip').onclick = function () { grade(false); };
}

/* ---- daily sets ---- */
function drillDailyUI(body) {
  var sets = (Content.drillData && Content.drillData.daily_sets) || [];
  var cmds = (Content.drillData && Content.drillData.commands) || [];
  var byId = {};
  cmds.forEach(function (c) { byId[c.id] = c; });
  var dayNames = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
  var today = dayNames[new Date().getDay()];
  var active = sets.some(function (s) { return s.day === today; }) ? today : (sets[0] && sets[0].day);
  // weakest-15 generated set
  var weakest = cmds.slice().sort(function (a, b) { return drillScore(a) - drillScore(b); }).slice(0, 15);

  function render() {
    var h = '<div class="panel"><div class="daytabs">';
    sets.forEach(function (s) {
      h += '<button class="' + (s.day === active ? 'active' : '') + '" data-day="' + s.day + '">' + s.day[0].toUpperCase() + s.day.slice(1) + '</button>';
    });
    h += '<button class="' + (active === 'weakest' ? 'active' : '') + '" data-day="weakest">⚠ Weakest</button></div>';
    if (active === 'weakest') {
      h += '<p class="muted">Auto-generated from your 15 weakest commands (slowest / most-missed).</p><div id="dailyList">';
      weakest.forEach(function (c) {
        var r = Store.state.drills[c.id];
        h += dailyRow(c, r);
      });
    } else {
      var s = sets.filter(function (x) { return x.day === active; })[0];
      h += '<p class="muted">' + esc(s.focus) + '</p><div id="dailyList">';
      s.drills.forEach(function (id) {
        var c = byId[id];
        if (c) h += dailyRow(c, Store.state.drills[id]);
      });
    }
    h += '</div></div>';
    body.innerHTML = h;
    $all('[data-day]', body).forEach(function (b) { b.onclick = function () { active = b.dataset.day; render(); }; });
    $all('[data-drillcmd]', body).forEach(function (b) {
      b.onclick = function () { go('#/drills/speed?cmd=' + encodeURIComponent(b.dataset.drillcmd)); };
    });
  }
  function dailyRow(c, r) {
    var meta = r && r.attempts ? Math.round(r.correct / r.attempts * 100) + '% · ' + (r.bestMs ? fmtSec(r.bestMs) : '—') + (r.mastered ? ' · <span class="badge sub10">sub-10s</span>' : '') : '<span class="muted">not attempted</span>';
    return '<div class="drill-item"><div class="ctx"><div class="cat">' + esc(c.category) + '</div><div>' + esc(c.context) + '</div><div class="muted" style="font-size:.75rem;margin-top:4px">' + meta + '</div></div>' +
      '<button class="btn small mini" data-drillcmd="' + esc(c.id) + '">drill →</button></div>';
  }
  render();
}

/* ==================== 13. MOCK ASSESSMENT ================================== */
var Mock = { items: [], i: 0, answers: [], endAt: 0, timerId: null, started: false };

function viewMockLanding() {
  var mins = Content.mockMinutes, n = Content.simulations.length;
  var doms = {};
  Content.simulations.forEach(function (s) { doms[s.domain_id || 'general'] = true; });
  var h = '<div class="wrap sim-shell"><div id="mockLanding">';
  h += '<p class="eyebrow">FINAL EVOLUTION</p><h2>Prove it under pressure</h2>';
  h += '<p class="muted" style="max-width:640px">A timed run across ' + n + ' hands-on mock scenarios. Hints are disabled and each decision is final — like the real 3-hour assessment.</p>';
  h += '<div class="mission-grid" style="max-width:560px;margin:22px 0">';
  h += '<div class="metric"><strong>' + n + '</strong><span>scenarios</span></div>';
  h += '<div class="metric"><strong>' + mins + '</strong><span>minutes</span></div>';
  h += '<div class="metric"><strong>' + Object.keys(doms).length + '</strong><span>domains</span></div></div>';
  if (Store.state.mockBest.score) h += '<p class="muted">Best score so far: <strong>' + Store.state.mockBest.score + '%</strong> (' + Store.state.mockRuns + ' runs)</p>';
  h += '<div class="cta-row"><button class="btn primary" id="mockStart">Stage the mock →</button></div></div>';
  h += '<div id="mockActive" style="display:none"></div><div id="mockResults" style="display:none"></div></div>';
  return h;
}
function initMockLanding() {
  var b = $('#mockStart');
  if (b) b.onclick = function () {
    if (!confirm('Start the ' + Content.mockMinutes + '-minute timed mock? Hints are disabled.')) return;
    startMock();
  };
}
function startMock() {
  Mock.items = shuffle(Content.simulations.slice(), mulberry32(Date.now() % 100000));
  Mock.i = 0; Mock.answers = []; Mock.started = true;
  Mock.endAt = Date.now() + Content.mockMinutes * 60000;
  $('#mockLanding').style.display = 'none';
  $('#mockResults').style.display = 'none';
  $('#mockActive').style.display = '';
  clearInterval(Mock.timerId);
  Mock.timerId = setInterval(function () {
    var left = Math.max(0, Mock.endAt - Date.now());
    var el = $('#mockTimer');
    if (el) {
      el.textContent = fmtClock(left / 1000);
      el.classList.toggle('danger', left < 10 * 60000);
    }
    if (left <= 0) finishMock(true);
  }, 1000);
  Timers.add(Mock.timerId);
  renderMockItem();
}
function renderMockItem() {
  var box = $('#mockActive');
  var s = Mock.items[Mock.i];
  if (!s) { finishMock(false); return; }
  var h = '<div class="action-row" style="justify-content:space-between"><div><p class="wb-eyebrow">MOCK ' + (Mock.i + 1) + ' / ' + Mock.items.length + (s.domain_id ? ' · ' + esc((Content.domainById[s.domain_id] || { name: s.domain_id }).name) : '') + '</p><h2 style="margin:0">' + esc(s.title) + '</h2></div>';
  h += '<div style="text-align:right"><div class="sim-timer" id="mockTimer">' + fmtClock((Mock.endAt - Date.now()) / 1000) + '</div><div class="status-label">' + (s.mins ? '~' + s.mins + ' min budget' : '') + '</div></div></div>';
  h += '<div class="situation"><p>' + esc(s.situation).split('\n').join('</p><p>') + '</p></div>';
  if (s.evidence && s.evidence.length) {
    h += '<div class="ev-row">';
    s.evidence.forEach(function (ev, i) { h += '<button class="btn small ghost ev-btn" data-ev="' + i + '">📄 ' + esc(ev[0]) + '</button>'; });
    h += '</div><div class="ev-pane" id="evPane" hidden></div>';
  }
  h += '<p class="decision-prompt">' + esc(s.prompt) + '</p><div class="choices" role="radiogroup">';
  s.choices.forEach(function (c, i) {
    h += '<label class="choice"><input type="radio" name="mk-choice" value="' + i + '"><span class="choice-letter">' + 'ABCD'[i] + '</span><span>' + esc(c) + '</span></label>';
  });
  h += '</div><div class="feedback" id="mkFb"></div>';
  h += '<div class="action-row"><button class="btn primary" id="mkLock" disabled>Lock in answer</button><button class="btn small ghost" id="mkEnd">End run early</button></div>';
  box.innerHTML = h;
  $all('.ev-btn', box).forEach(function (b) {
    b.onclick = function () {
      var ev = s.evidence[+b.dataset.ev];
      var pane = $('#evPane', box);
      pane.hidden = false;
      pane.innerHTML = '<p class="ev-title">' + esc(ev[0]) + '</p><pre class="code">' + esc(ev[1]) + '</pre>';
    };
  });
  $all('input[name="mk-choice"]', box).forEach(function (r) { r.onchange = function () { $('#mkLock', box).disabled = false; }; });
  $('#mkLock', box).onclick = function () {
    var sel = $('input[name="mk-choice"]:checked', box);
    if (!sel) return;
    Mock.answers.push({ id: s.id, correct: +sel.value === s.answer, domain: s.domain_id });
    srUpdate(s.id, +sel.value === s.answer ? 5 : 2);
    Mock.i++;
    renderMockItem();
  };
  $('#mkEnd', box).onclick = function () {
    if (confirm('End the mock run early? Unanswered items count as misses.')) finishMock(false);
  };
}
function finishMock(timedOut) {
  clearInterval(Mock.timerId);
  Mock.started = false;
  var total = Mock.items.length;
  var correct = Mock.answers.filter(function (a) { return a.correct; }).length;
  var score = total ? Math.round(correct / total * 100) : 0;
  var byDom = {};
  Mock.answers.forEach(function (a) {
    var d = a.domain || 'general';
    byDom[d] = byDom[d] || { ok: 0, n: 0 };
    byDom[d].n++; if (a.correct) byDom[d].ok++;
  });
  Store.state.mockRuns++;
  if (score > (Store.state.mockBest.score || 0)) Store.state.mockBest = { score: score, at: Date.now() };
  Store.save();

  var h = '<p class="eyebrow">MOCK RESULTS' + (timedOut ? ' · TIME EXPIRED' : '') + '</p>';
  h += '<h2>' + score + '% <span class="muted">(' + correct + '/' + total + ')</span></h2>';
  h += progressBar(score / 100, 'mock score');
  h += '<h3 class="sec-h">Per-domain breakdown</h3><div class="item-list">';
  Object.keys(byDom).sort().forEach(function (d) {
    var b = byDom[d];
    var name = (Content.domainById[d] || { name: d }).name;
    h += '<div class="item-row static"><span>' + esc(name) + '</span>' + progressBar(b.ok / b.n, name) + '<span class="weak-pct">' + b.ok + '/' + b.n + '</span></div>';
  });
  h += '</div><h3 class="sec-h">Review the misses</h3><div class="item-list">';
  Mock.answers.forEach(function (a, i) {
    if (a.correct) return;
    var s = Mock.items.filter(function (x) { return x.id === a.id; })[0];
    if (!s) return;
    h += '<div class="panel" style="margin-bottom:10px"><strong>' + esc(s.title) + '</strong><p class="muted">' + esc(s.prompt) + '</p><p>✓ Correct: ' + esc(s.choices[s.answer]) + '</p><p class="muted">' + esc(s.why || '') + '</p></div>';
  });
  h += '</div><div class="action-row"><a class="btn primary" href="#/dashboard">Back to dashboard</a><button class="btn ghost" id="mockRetry">Retry mock</button></div>';
  $('#mockActive').style.display = 'none';
  var res = $('#mockResults');
  res.style.display = '';
  res.innerHTML = h;
  $('#mockRetry').onclick = function () { go('#/mock'); setTimeout(function () { var b = $('#mockStart'); if (b) b.click(); }, 50); };
  toast('Mock complete: ' + score + '%');
}

/* ==================== 14. REFERENCE VIEW =================================== */
function viewReference() {
  var R = Content.resources;
  var h = '<div class="wrap"><div class="view-head"><p class="eyebrow">REFERENCE SHELF</p><h2>Reference</h2>';
  h += '<p class="muted">Cheat sheets, tools, simulators, official docs, and behavioral prep.</p></div>';

  if (R.cheatsheet && R.cheatsheet.length) {
    h += '<h3 class="sec-h">Cheat sheets</h3><div class="card-grid">';
    R.cheatsheet.forEach(function (c) {
      h += '<div class="panel"><h4>' + esc(c.title) + '</h4><p>' + esc(c.body) + '</p></div>';
    });
    h += '</div>';
  }
  h += '<h3 class="sec-h">Interactive tools</h3><div class="card-grid">';
  h += refCard('Subnet calculator', 'Binary view, practice mode with scoring, and a subnet planner.', 'tools/subnet-calculator.html');
  h += refCard('Muscle-memory drills', '50 commands · 10 workflows · 12 error traps — standalone drill page.', 'tools/muscle-memory-drills.html');
  h += refCard('Subnet splitter', 'Visual subnet carving practice.', 'visuals/subnet-splitter.html');
  h += refCard('VLAN explorer', 'VLAN/trunk concepts, interactive.', 'visuals/vlan-explorer.html');
  h += refCard('Kerberos explorer', 'Kerberos flow walkthrough.', 'visuals/kerberos-explorer.html');
  h += refCard('RAID simulator', 'RAID levels with capacity math.', 'visuals/raid-simulator.html');
  h += '</div>';
  h += '<h3 class="sec-h">Simulators</h3><div class="card-grid">';
  h += refCard('Terminal mastery', 'Guided terminal exercises.', 'sims/terminal-mastery.html');
  h += refCard('Proxmox sim', 'Proxmox VE console simulator.', 'sims/proxmox-sim.html');
  h += refCard('FortiGate sim', 'FortiGate console simulator.', 'sims/fortigate-sim.html');
  h += refCard('Palo Alto sim', 'PAN-OS simulator: App-ID proof, zones, NAT-before-policy.', 'sims/paloalto-sim.html');
  h += refCard('Git simulator', 'Animated commit graph, merge-conflict walkthrough, PR flow.', 'sims/git-simulator.html');
  h += refCard('VLAN basics', 'VLAN trunking CLI lab (IOS engine).', 'sims/vlan-basics.html');
  h += refCard('Diagram gallery', 'All animated diagrams in one place.', 'diagrams/index.html');
  h += '</div>';

  if (R.checklist && R.checklist.length) {
    h += '<h3 class="sec-h">Readiness checklist</h3><div class="panel"><div class="steps">';
    R.checklist.forEach(function (item, i) {
      var id = 'chk-' + i;
      var done = !!Store.state.checkItems[id];
      h += '<label class="step"><input type="checkbox" data-chk="' + id + '"' + (done ? ' checked' : '') + '><span>' + esc(item) + '</span></label>';
    });
    h += '</div></div>';
  }
  if (R.links && R.links.length) {
    h += '<h3 class="sec-h">Links</h3><div class="item-list">';
    R.links.forEach(function (l) {
      h += '<a class="item-row" href="' + esc(l.url) + '" target="_blank" rel="noopener"><span>' + esc(l.label) + '<em>' + esc(l.note || '') + '</em></span><span class="chev">↗</span></a>';
    });
    h += '</div>';
  }
  if (R.references && R.references.length) {
    h += '<h3 class="sec-h">Official references</h3><div class="item-list">';
    R.references.forEach(function (r) {
      h += '<a class="item-row" href="' + esc(r.url) + '" target="_blank" rel="noopener"><span>' + esc(r.title) + '</span><span class="chev">↗</span></a>';
    });
    h += '</div>';
  }
  if (Content.behavioral && Content.behavioral.length) {
    h += '<h3 class="sec-h">Behavioral prep <span class="muted">(STAR)</span></h3>';
    Content.behavioral.forEach(function (b, i) {
      h += '<div class="panel beh"><button class="beh-q" data-beh="' + i + '"><span>' + esc(b.prompt) + '</span><span class="chev">+</span></button><div class="beh-a" hidden>';
      if (b.points) h += '<p><strong>Hit these points:</strong></p><ul class="bullets">' + b.points.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>';
      if (b.pitfalls) h += '<p><strong>Avoid:</strong></p><ul class="bullets">' + b.pitfalls.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>';
      h += '</div></div>';
    });
  }
  h += '</div>';
  setTimeout(function () {
    $all('[data-chk]').forEach(function (cb) {
      cb.onchange = function () {
        if (cb.checked) Store.state.checkItems[cb.dataset.chk] = true;
        else delete Store.state.checkItems[cb.dataset.chk];
        Store.save();
      };
    });
    $all('.beh-q').forEach(function (b) {
      b.onclick = function () {
        var a = b.nextElementSibling;
        a.hidden = !a.hidden;
        b.querySelector('.chev').textContent = a.hidden ? '+' : '−';
      };
    });
  }, 0);
  return h;
}
function refCard(title, desc, href) {
  return '<a class="panel ref-card" href="' + esc(href) + '" target="_blank" rel="noopener"><h4>' + esc(title) + '</h4><p class="muted">' + esc(desc) + '</p><span class="chev">Open ↗</span></a>';
}

/* ==================== 15. OFFLINE / SW / INIT ============================== */
function showOfflineBanner(show) {
  var b = $('#offlineBanner');
  if (!b) return;
  b.style.display = show ? '' : 'none';
}
function updateOnlineStatus() {
  showOfflineBanner(!navigator.onLine);
}
function registerSW() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('sw.js').then(function (reg) {
      reg.addEventListener('updatefound', function () {
        var w = reg.installing;
        w.addEventListener('statechange', function () {
          if (w.state === 'installed' && navigator.serviceWorker.controller) {
            window._swUpdateReady = true;
            toast('Update available — reload for the latest version');
          }
        });
      });
    }).catch(function () { /* offline-first still works without SW */ });
  }
}

function buildNav() {
  var html = NAV.map(function (n) {
    return '<button class="nav-btn" data-view="' + n.id + '" data-route="#/' + n.id + '"><span class="nav-ic">' + n.icon + '</span><span class="nav-lb">' + n.label + '</span></button>';
  }).join('');
  $('#topnav').innerHTML = html;
  $('#bottomnav').innerHTML = html;
  $all('.nav-btn').forEach(function (b) {
    b.addEventListener('click', function () { go(b.dataset.route); });
  });
}

function init() {
  Store.state = loadLocalState();
  buildNav();
  window.addEventListener('hashchange', renderRoute);
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') { persistLocal(); if (Store.cloud) scheduleCloudSync(); }
  });
  registerSW();
  updateOnlineStatus();
  loadContent().then(function () {
    return loadDrillData();
  }).then(function () {
    $('#heroTitle') && ($('#heroTitle').textContent = Content.title);
    renderRoute();
    bootSync();
  }).catch(function (err) {
    $('#view').innerHTML = '<div class="wrap"><div class="panel"><h2>Couldn\'t load content</h2><p class="muted">' + esc(err.message) + ' — check your connection and reload. The app works offline after the first successful load.</p><button class="btn primary" onclick="location.reload()">Retry</button></div></div>';
  });
}
document.addEventListener('DOMContentLoaded', init);
