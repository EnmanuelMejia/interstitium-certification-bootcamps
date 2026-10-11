/* Interstitium Labs — Notes bridge for CBT lessons (notes-bridge.js).
 * Adds the personal-vault actions to every lesson in the unified shell:
 *   📝 Add note    — captures this lesson into My Notes (Obsidian-style)
 *   🧠 Mind map    — this bootcamp's auto-generated mind map (NoahViz)
 *   🔖 Bookmark    — saves this page to the workspace dashboard
 * Loads the flagship vault modules (il-notes.js, il-mindmap.js, noah-viz.js)
 * from interstitiumlabs.dev on first use; degrades silently if offline.
 * Enhancement layer over learn.js (observes #learnBody, same pattern as
 * ai-reading.js). Vanilla JS, zero dependencies, ES5-compatible. */
(function () {
  'use strict';

  var SLUG = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.slug) || 'bootcamp';
  var CBT_TITLE = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.title) || 'Bootcamp';
  var ASSETS = 'https://interstitiumlabs.dev/assets/';

  var CSS = [
    '.ilnb-bar{margin-top:14px;border:1px dashed rgba(201,162,39,.45);border-radius:var(--radius,12px);background:var(--surface,#0a0f1c);padding:12px 14px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}',
    '.ilnb-bar .ilnb-tag{font:600 11px var(--mono,monospace);letter-spacing:.06em;color:var(--accent,#c9a227);margin-right:4px}',
    '.ilnb-overlay{position:fixed;inset:0;background:rgba(3,5,9,.8);backdrop-filter:blur(4px);z-index:9980;display:flex;align-items:center;justify-content:center;padding:14px}',
    '.ilnb-modal{background:#0a0f1c;border:1px solid rgba(94,234,212,.25);border-radius:16px;width:min(1080px,100%);padding:14px;color:#dbe4ee}',
    '.ilnb-modal h3{margin:0 0 10px;font-size:16px;color:#fff}',
    '.ilnb-modal canvas{width:100%;display:block;background:#06080c;border-radius:10px}',
    '.ilnb-modal .ilnb-row{display:flex;justify-content:space-between;align-items:center;gap:10px}'
  ].join('\n');

  function injectCSS() {
    if (document.getElementById('ilnb-css')) return;
    var st = document.createElement('style'); st.id = 'ilnb-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }

  function loadScript(src) {
    return new Promise(function (resolve) {
      if (document.querySelector('script[src="' + src + '"]')) { resolve(true); return; }
      var s = document.createElement('script');
      s.src = src; s.defer = true;
      s.onload = function () { resolve(true); };
      s.onerror = function () { resolve(false); };
      document.head.appendChild(s);
    });
  }

  function ensureNotes() {
    if (window.ILNotes) return Promise.resolve(true);
    return loadScript(ASSETS + 'il-notes.js').then(function () { return !!window.ILNotes; });
  }
  function ensureMindmap() {
    if (window.ILMindmap) return Promise.resolve(true);
    return loadScript(ASSETS + 'il-mindmap.js').then(function () { return !!window.ILMindmap; });
  }

  function lessonTitle() {
    var h = document.querySelector('.learn-slide h2, .learn-slide h3, .learn-deck h2, .learn-deck h3');
    var t = h ? h.textContent.replace(/\s+/g, ' ').trim() : '';
    return t || CBT_TITLE;
  }

  function lessonConcepts() {
    var out = [], seen = {};
    document.querySelectorAll('.learn-slide strong, .learn-slide b, .learn-slide code').forEach(function (el) {
      var t = el.textContent.replace(/\s+/g, ' ').trim();
      if (t && t.length <= 90 && !seen[t]) { seen[t] = 1; out.push(t); }
    });
    return out.slice(0, 8);
  }

  function addNote() {
    ensureNotes().then(function (ok) {
      if (!ok) return;
      var note = window.ILNotes.noteFromLesson({
        title: lessonTitle(), slug: SLUG,
        concepts: lessonConcepts(), ref: location.href
      });
      window.ILNotes.openEditor(note.id);
    });
  }

  function bookmark() {
    ensureNotes().then(function (ok) {
      if (!ok) return;
      window.ILNotes.addBookmark(CBT_TITLE + ' — ' + lessonTitle(), location.href);
      flash('Bookmarked to My Notes ✓');
    });
  }

  function flash(msg) {
    var d = document.createElement('div');
    d.textContent = msg;
    d.style.cssText = 'position:fixed;bottom:18px;left:50%;transform:translateX(-50%);background:#0a0f1c;border:1px solid #5EEAD4;color:#dbe4ee;border-radius:999px;padding:9px 18px;z-index:9995;font:13px system-ui;box-shadow:0 10px 30px rgba(0,0,0,.5)';
    document.body.appendChild(d);
    setTimeout(function () { d.remove(); }, 2200);
  }

  function openMap() {
    ensureMindmap().then(function (ok) {
      if (!ok) return;
      injectCSS();
      var ov = document.createElement('div');
      ov.className = 'ilnb-overlay';
      ov.innerHTML = '<div class="ilnb-modal"><div class="ilnb-row"><h3>🧠 ' +
        CBT_TITLE.replace(/</g, '&lt;') + ' — Mind Map</h3>' +
        '<button type="button" class="btn small ghost" data-ilnb-close>✕ Close</button></div>' +
        '<canvas height="540"></canvas>' +
        '<p style="color:#8b93a5;font-size:12.5px;margin:10px 0 0">Auto-generated from this bootcamp’s structure. Click branches to expand/collapse. Full editor: <a href="https://interstitiumlabs.dev/my-notes/" style="color:#5EEAD4">My Notes → Mind Maps</a></p></div>';
      document.body.appendChild(ov);
      ov.addEventListener('click', function (e) { if (e.target === ov || e.target.closest('[data-ilnb-close]')) ov.remove(); });
      var canvas = ov.querySelector('canvas');
      window.ILMindmap.fetchCbtTree(SLUG, function (tree, content) {
        if (!tree) { ov.querySelector('h3').textContent = 'Mind map unavailable offline'; return; }
        window.ILMindmap.renderInto(canvas, tree, { title: (content && content.title) || CBT_TITLE });
      });
    });
  }

  function mountBar() {
    var deck = document.querySelector('.learn-deck');
    if (!deck || deck.querySelector('.ilnb-bar')) return;
    injectCSS();
    var bar = document.createElement('div');
    bar.className = 'ilnb-bar';
    bar.innerHTML = '<span class="ilnb-tag">MY NOTES</span>' +
      '<button type="button" class="btn small ghost" data-ilnb="note">📝 Add note</button>' +
      '<button type="button" class="btn small ghost" data-ilnb="map">🧠 Mind map</button>' +
      '<button type="button" class="btn small ghost" data-ilnb="bookmark">🔖 Bookmark</button>' +
      '<a class="btn small ghost" href="https://interstitiumlabs.dev/my-notes/" style="text-decoration:none">Open workspace →</a>';
    bar.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('[data-ilnb]') : null;
      if (!b) return;
      var k = b.getAttribute('data-ilnb');
      if (k === 'note') addNote();
      else if (k === 'map') openMap();
      else if (k === 'bookmark') bookmark();
    });
    deck.appendChild(bar);
  }

  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    setTimeout(function () { scheduled = false; mountBar(); }, 250);
  }

  var bootTries = 0;
  function boot() {
    var body = document.getElementById('learnBody');
    if (!body) { if (++bootTries <= 12) setTimeout(boot, 600); return; }
    mountBar();
    if (window.MutationObserver) {
      new MutationObserver(schedule).observe(body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
