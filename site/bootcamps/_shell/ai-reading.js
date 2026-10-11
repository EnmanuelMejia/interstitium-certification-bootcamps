/* Interstitium Labs — AI Reading Companion (ai-reading.js).
   Turns static Learn slides into living reading:
   - AI extras per slide: Explain Differently / More Examples /
     Key Ideas (highlighting) / Animate (systems anatomy via NoahViz)
   - weak-concept highlighting: key terms in the slide get refresher
     tooltips; highlighting is ON by default when the student's skill
     profile for this bootcamp is struggling/developing
   - supplemental resources generated on demand and cached per slide
   - a "Keep going" panel on the final slide: an AI practice question
     for the lesson + follow-up suggestions
   - Sources & deep dives (2026-10-11): per-slide panel fed by the
     Knowledge Source Layer (/api/sources/panel) — attributed Wikipedia
     card, Stack Overflow Q&As, GitHub repos, papers and reading links.
     Sourced material is always labeled with its source; never passed
     off as original lesson text.
   - RTFM panel (2026-10-11): once per lesson, a collapsible list of
     OFFICIAL sources (cert-body exam objectives, vendor manuals, API
     references, RFCs, roadmaps) from _shell/rtfm-registry.json, keyed
     by the lesson's domain/cert. Direct links only; community sources
     (roadmap.sh) are labeled as community.
   Enhancement layer over learn.js (observes #learnBody). Vanilla JS,
   zero dependencies, ES5-compatible. Everything degrades: AI extras
   fall back to local extraction/restatement; Animate hides itself
   when NoahViz cannot be loaded. */
(function () {
  'use strict';

  var SLUG = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.slug) || 'bootcamp';
  var LS_CACHE = 'ilb-reading-cache-' + SLUG;
  var VIZ_URL = 'https://interstitiumlabs.dev/assets/noah-viz.js';

  var CSS = [
    '.aix-read{margin-top:14px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);padding:14px 16px}',
    '.aix-read .aix-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}',
    '.aix-read .aix-tag{display:inline-block;font:600 11px var(--mono);letter-spacing:.06em;color:var(--accent);margin-right:6px}',
    '.aix-read .aix-panel{margin-top:12px;font-size:14.5px;line-height:1.65;display:none}',
    '.aix-read .aix-panel.open{display:block}',
    '.aix-read .aix-panel p{margin:0 0 10px}',
    '.aix-read canvas{max-width:100%;display:block;margin:8px auto}',
    '.aix-read mark.aix-key{background:rgba(201,162,39,.28);color:inherit;border-radius:3px;padding:0 3px;cursor:help;border-bottom:1px dotted var(--accent)}',
    '.aix-read .aix-answer{display:none;margin-top:10px;border-left:3px solid var(--accent);padding:8px 12px;background:var(--surface-2)}',
    '.aix-read .aix-answer.open{display:block}',
    '.aix-read .aix-src{margin:10px 0;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--surface-2);overflow:hidden}',
    '.aix-read .aix-src h5{margin:0 0 4px;font-size:13.5px;line-height:1.4}',
    '.aix-read .aix-src p{font-size:13.5px;margin:0 0 6px}',
    '.aix-read .aix-src img{float:right;width:54px;height:54px;object-fit:contain;border-radius:6px;margin:0 0 6px 10px;background:#fff}',
    '.aix-read .aix-src blockquote{margin:6px 0;padding:6px 10px;border-left:3px solid var(--accent);font-size:13px;color:var(--muted)}',
    '.aix-read .aix-attr{font-size:11.5px;color:var(--muted);margin-top:8px}',
    '.aix-read ul.aix-links{margin:6px 0;padding-left:18px}',
    '.aix-read ul.aix-links li{margin:4px 0;font-size:13.5px}',
    '.aix-rtfm{margin-top:14px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);padding:12px 16px}',
    '.aix-rtfm summary{cursor:pointer;font:600 12px var(--mono);letter-spacing:.06em;color:var(--accent)}',
    '.aix-rtfm ul{margin:10px 0 4px;padding-left:18px}',
    '.aix-rtfm li{margin:5px 0;font-size:14px;line-height:1.5}',
    '.aix-rtfm .aix-rtfm-type{font:600 10.5px var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-right:6px}',
    '.aix-rtfm .aix-attr{font-size:11.5px;color:var(--muted);margin-top:8px}'
  ].join('\n');

  function injectCSS() {
    if (document.getElementById('aix-read-css')) return;
    var st = document.createElement('style');
    st.id = 'aix-read-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function $(id) { return document.getElementById(id); }
  function hashStr(s) {
    var h = 0; s = String(s || '');
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    return 'h' + Math.abs(h);
  }
  function cacheGet(k) {
    try { var c = JSON.parse(localStorage.getItem(LS_CACHE)) || {}; return c[k]; }
    catch (e) { return null; }
  }
  function cacheSet(k, v) {
    try {
      var c = JSON.parse(localStorage.getItem(LS_CACHE)) || {};
      c[k] = v;
      var keys = Object.keys(c);
      if (keys.length > 60) delete c[keys[0]];
      localStorage.setItem(LS_CACHE, JSON.stringify(c));
    } catch (e) {}
  }
  function level() {
    return (window.AIDynamic && window.AIDynamic.getLevel(SLUG.replace(/-/g, ' '))) || 'developing';
  }
  function slideText(stage) {
    var slide = stage.querySelector('.learn-slide');
    return slide ? slide.textContent.replace(/\s+/g, ' ').trim().slice(0, 2400) : '';
  }
  function slideHeading(stage) {
    var h = stage.querySelector('.learn-slide h3, .learn-slide h2');
    return h ? h.textContent.trim() : 'this lesson';
  }

  /* ---------------- NoahViz lazy load ---------------- */

  var vizPromise = null;
  function loadViz() {
    if (window.NoahViz) return Promise.resolve(window.NoahViz);
    if (vizPromise) return vizPromise;
    vizPromise = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = VIZ_URL;
      s.onload = function () { window.NoahViz ? resolve(window.NoahViz) : reject(new Error('viz-empty')); };
      s.onerror = function () { reject(new Error('viz-load')); };
      document.head.appendChild(s);
    });
    return vizPromise;
  }

  /* ---------------- key-idea extraction + highlighting ---------------- */

  function keyTerms(stage) {
    var terms = {};
    var nodes = stage.querySelectorAll('.learn-slide strong, .learn-slide b, .learn-slide code');
    for (var i = 0; i < nodes.length; i++) {
      var t = nodes[i].textContent.trim();
      if (t.length >= 3 && t.length <= 48) terms[t] = true;
    }
    /* Capitalized multi-word phrases and acronyms from bullets. */
    var text = slideText(stage);
    var m, re = /\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2}|[A-Z]{2,}[-\w]*)\b/g;
    while ((m = re.exec(text))) { if (Object.keys(terms).length < 14) terms[m[1]] = true; }
    return Object.keys(terms);
  }

  function highlight(stage) {
    var terms = keyTerms(stage);
    if (!terms.length) return 0;
    var count = 0;
    var walker = document.createTreeWalker(stage, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = n.parentNode;
        if (!p || /^(SCRIPT|STYLE|MARK|BUTTON)$/.test(p.nodeName)) return NodeFilter.FILTER_REJECT;
        if (p.closest && p.closest('.aix-read')) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    terms.sort(function (a, b) { return b.length - a.length; });
    for (var ti = 0; ti < terms.length; ti++) {
      var term = terms[ti];
      for (var ni = 0; ni < textNodes.length; ni++) {
        var node = textNodes[ni];
        if (!node.parentNode) continue;
        var idx = node.nodeValue.indexOf(term);
        if (idx < 0) continue;
        var mark = document.createElement('mark');
        mark.className = 'aix-key';
        mark.title = 'Key idea: ' + term + ' — central to this lesson. If this feels shaky, use "Explain differently".';
        mark.textContent = term;
        var after = node.splitText(idx);
        after.nodeValue = after.nodeValue.slice(term.length);
        node.parentNode.insertBefore(mark, after);
        count++;
        break; /* one highlight per term */
      }
    }
    return count;
  }

  /* ---------------- AI supplemental content ---------------- */

  function tutorAsk(promptText) {
    if (!window.AIClient) return Promise.reject(new Error('no-client'));
    return window.AIClient.route('tutor', [{ role: 'user', content: promptText }], { maxTokens: 600 })
      .then(function (r) { return r.reply; });
  }

  function paragraphs(text) {
    return String(text || '').split(/\n{2,}|\n/).filter(function (p) { return p.trim(); })
      .map(function (p) { return '<p>' + esc(p.trim()) + '</p>'; }).join('');
  }

  function localExplain(text, heading) {
    return 'Another way to see "' + heading + '": strip it to the moving parts. ' +
      'Ask three questions of the material: (1) What goes IN? (2) What changes? (3) What comes OUT? ' +
      'Nearly every system in this field is input → transformation → output. Re-read the slide and label ' +
      'each sentence with one of the three — the structure appears, and the details hang on it. ' +
      '(Connect to get Noah\'s full re-teaching of this slide in a second voice.)';
  }
  function localExamples(heading) {
    return 'Try these in the Terminal tab:\n' +
      '1) Find one real place "' + heading + '" shows up in a system you have used today — name the input and the output.\n' +
      '2) Break it on purpose: what is the FIRST symptom when this fails? That symptom is the interview answer.\n' +
      '(Connect to get two fully worked examples from Noah.)';
  }

  /* ---------------- sources & deep dives (Knowledge Source Layer) ---------------- */

  function lessonDomainName() {
    var body = $('learnBody');
    return body ? (body.getAttribute('data-noah-lesson-domain') || '') : '';
  }

  function renderSourcesPanel(j) {
    if (!j || !j.ok || !j.sections) return '<p>No sources came back for this one. The lesson above stands on its own.</p>';
    var byName = {};
    j.sections.forEach(function (s) { byName[s.name] = s; });
    var html = '';
    var wiki = byName.wikipedia && byName.wikipedia.results[0];
    if (wiki) {
      html += '<div class="aix-src">' +
        (wiki.meta && wiki.meta.thumbnail ? '<img src="' + esc(wiki.meta.thumbnail) + '" alt="">' : '') +
        '<h5><a href="' + esc(wiki.url) + '" target="_blank" rel="noopener">' + esc(wiki.title) + '</a> — Wikipedia</h5>' +
        '<p>' + esc(wiki.summary) + '</p>' +
        '<p class="aix-attr">Summary from Wikipedia (CC BY-SA) — the concept in the wider world, beyond this course.</p></div>';
    }
    var so = (byName.stackoverflow && byName.stackoverflow.results) || [];
    if (so.length) {
      html += '<p><strong>Stack Overflow — how practitioners solve it:</strong></p>';
      so.forEach(function (r) {
        html += '<div class="aix-src"><h5><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a></h5>' +
          '<p class="aix-attr">Score ' + esc(r.meta.score != null ? r.meta.score : 0) + ' · ' + esc(r.meta.answers || 0) + ' answers' +
          (r.meta.tags && r.meta.tags.length ? ' · ' + esc(r.meta.tags.join(', ')) : '') + '</p>';
        if (r.meta.topAnswer) {
          html += '<blockquote><strong>Top answer' + (r.meta.topAnswerAccepted ? ' (accepted)' : '') + ':</strong> ' +
            esc(r.meta.topAnswer) + '</blockquote>';
        }
        html += '</div>';
      });
    }
    var gh = (byName.github && byName.github.results) || [];
    if (gh.length) {
      html += '<p><strong>GitHub — real-world code:</strong></p><ul class="aix-links">';
      gh.forEach(function (r) {
        html += '<li><a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.title) + '</a>' +
          ' <span style="color:var(--muted)">★ ' + esc(r.meta.stars != null ? r.meta.stars : '') +
          (r.meta.language ? ' · ' + esc(r.meta.language) : '') +
          (r.meta.license ? ' · ' + esc(r.meta.license) : '') + '</span>' +
          (r.summary ? '<br><span style="color:var(--muted)">' + esc(r.summary) + '</span>' : '') + '</li>';
      });
      html += '</ul>';
    }
    var more = [];
    ['arxiv', 'mdn', 'substack', 'hackernews', 'reddit', 'youtube'].forEach(function (n) {
      var sec = byName[n];
      if (!sec) return;
      sec.results.forEach(function (r) { more.push({ label: sec.label, r: r }); });
    });
    if (more.length) {
      html += '<p><strong>Go deeper:</strong></p><ul class="aix-links">';
      more.slice(0, 8).forEach(function (m) {
        html += '<li><a href="' + esc(m.r.url) + '" target="_blank" rel="noopener">' + esc(m.r.title) + '</a>' +
          ' <span style="color:var(--muted)">— ' + esc(m.label) +
          (m.r.meta && m.r.meta.publication ? ' · ' + esc(m.r.meta.publication) : '') +
          (m.r.meta && m.r.meta.channel ? ' · ' + esc(m.r.meta.channel) : '') + '</span></li>';
      });
      html += '</ul>';
    }
    if (!html) return '<p>No live sources for this slide right now — the lesson above is complete on its own.</p>';
    html += '<p class="aix-attr">' + esc(j.attribution || 'Supplemental material shown with attribution; follow the links to verify at the source.') + '</p>';
    return html;
  }

  /* ---------------- RTFM: official sources per lesson ---------------- */

  var rtfmRegistryPromise = null;
  function loadRtfmRegistry() {
    if (rtfmRegistryPromise) return rtfmRegistryPromise;
    rtfmRegistryPromise = fetch('/bootcamps/_shell/rtfm-registry.json')
      .then(function (r) { if (!r.ok) throw new Error('rtfm-http'); return r.json(); })
      .catch(function () { return null; });
    return rtfmRegistryPromise;
  }

  function rtfmEntriesFor(reg, heading) {
    var out = [], seen = {};
    function add(list) {
      (list || []).forEach(function (e) {
        if (e && e.url && !seen[e.url]) { seen[e.url] = 1; out.push(e); }
      });
    }
    var body = $('learnBody');
    var topicId = body ? (body.getAttribute('data-noah-lesson-topic') || '') : '';
    var bc = (reg.bootcamps || {})[SLUG] || {};
    (bc.certs || []).forEach(function (c) { add((reg.certs || {})[c]); });
    if (reg.certs && reg.certs[SLUG]) add(reg.certs[SLUG]);
    (bc.domains || []).forEach(function (d) { add((reg.domains || {})[d]); });
    if (topicId && reg.domains && reg.domains[topicId]) add(reg.domains[topicId]);
    var hay = ((heading || '') + ' ' + lessonDomainName() + ' ' + SLUG + ' ' + topicId).toLowerCase();
    (reg.topics || []).forEach(function (t) {
      if (!t.match) return;
      for (var i = 0; i < t.match.length; i++) {
        if (hay.indexOf(t.match[i]) !== -1) { add(t.sources); break; }
      }
    });
    add(reg.defaults);
    return out.slice(0, 12);
  }

  function maybeRtfm(deck, heading) {
    if (deck.querySelector('.aix-rtfm')) return;
    loadRtfmRegistry().then(function (reg) {
      if (!reg || deck.querySelector('.aix-rtfm')) return;
      var entries = rtfmEntriesFor(reg, heading);
      if (!entries.length) return;
      var box = document.createElement('details');
      box.className = 'aix-rtfm';
      var items = entries.map(function (e) {
        return '<li><span class="aix-rtfm-type">' + esc(e.type || 'doc') + '</span>' +
          '<a href="' + esc(e.url) + '" target="_blank" rel="noopener">' + esc(e.title) + '</a>' +
          ' <span style="color:var(--muted)">— ' + esc(e.source || '') + '</span></li>';
      }).join('');
      box.innerHTML = '<summary>📖 RTFM — OFFICIAL SOURCES (' + entries.length + ')</summary>' +
        '<ul>' + items + '</ul>' +
        '<p class="aix-attr">The manual, from the source: official cert-body objectives, vendor docs, standards and API references — the ground truth this lesson teaches from. Community roadmaps are labeled as such.</p>';
      deck.appendChild(box);
    });
  }

  /* ---------------- extras bar ---------------- */

  function extrasHTML() {
    return '<div class="aix-read"><div class="aix-row">' +
      '<span class="aix-tag">✦ NOAH EXTRAS</span>' +
      '<button class="btn small ghost" data-read="explain">Explain differently</button>' +
      '<button class="btn small ghost" data-read="examples">More examples</button>' +
      '<button class="btn small ghost" data-read="keys">Key ideas</button>' +
      '<button class="btn small ghost" data-read="animate">▶ Animate this</button>' +
      '<button class="btn small ghost" data-read="sources">Sources &amp; deep dives</button></div>' +
      '<div class="aix-panel" role="status"></div></div>';
  }

  function enhance() {
    var stage = $('learnStage');
    var deck = document.querySelector('.learn-deck');
    if (!stage || !deck) return;
    var text = slideText(stage);
    if (!text) return;
    var key = hashStr(text.slice(0, 400));
    if (deck.getAttribute('data-aix-key') === key) return;
    deck.setAttribute('data-aix-key', key);
    var old = deck.querySelector('.aix-read');
    if (old) old.parentNode.removeChild(old);

    var wrap = document.createElement('div');
    wrap.innerHTML = extrasHTML();
    var bar = wrap.firstChild;
    deck.appendChild(bar);
    var panel = bar.querySelector('.aix-panel');
    var heading = slideHeading(stage);

    function openPanel(html) { panel.innerHTML = html; panel.classList.add('open'); }

    bar.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-read]') : null;
      if (!btn) return;
      var kind = btn.getAttribute('data-read');

      if (kind === 'sources') {
        var ckSrc = 'sources:' + key;
        var hitSrc = cacheGet(ckSrc);
        if (hitSrc) { openPanel(hitSrc); return; }
        openPanel('<p>Gathering sources for &quot;' + esc(heading) + '&quot;…</p>');
        var topic = (heading + ' ' + lessonDomainName()).replace(/\s+/g, ' ').trim().slice(0, 160);
        fetch('/api/sources/panel?topic=' + encodeURIComponent(topic))
          .then(function (r) { return r.json(); })
          .then(function (j) {
            var html = renderSourcesPanel(j);
            cacheSet(ckSrc, html);
            openPanel(html);
          })
          .catch(function () {
            openPanel('<p>Live sources are unreachable right now. This lesson is complete on its own — try again in a bit, or use the RTFM panel below for the official manuals.</p>');
          });
        return;
      }
      if (kind === 'keys') {
        var n = highlight(stage);
        openPanel('<p>' + (n ? 'Highlighted ' + n + ' key idea' + (n > 1 ? 's' : '') +
          ' in this slide. Hover or tap one for a refresher. These are the terms an interviewer listens for.' :
          'No extractable key terms on this slide — it is mostly narrative. Try "Explain differently" instead.') + '</p>');
        return;
      }
      if (kind === 'explain' || kind === 'examples') {
        var ck = kind + ':' + key;
        var hit = cacheGet(ck);
        if (hit) { openPanel(paragraphs(hit)); return; }
        openPanel('<p>Noah is preparing that for you…</p>');
        var prompt = kind === 'explain'
          ? 'Re-teach this lesson slide to a ' + level() + '-level student using a DIFFERENT analogy and ' +
            'structure than the original. Plain text, 2 short paragraphs.\n\nSLIDE:\n' + text
          : 'Give TWO new worked examples for the topic "' + heading + '" (different from the slide), ' +
            'each 3-5 lines, showing the steps. Plain text.\n\nSLIDE CONTEXT:\n' + text.slice(0, 900);
        tutorAsk(prompt).then(function (txt) { cacheSet(ck, txt); openPanel(paragraphs(txt)); })
          .catch(function () {
            openPanel(paragraphs(kind === 'explain' ? localExplain(text, heading) : localExamples(heading)));
          });
        return;
      }
      if (kind === 'animate') {
        openPanel('<p>Building the systems anatomy…</p>');
        loadViz().then(function (Viz) {
          var ckA = 'anatomy:' + key;
          var cached = cacheGet(ckA);
          function render(spec) {
            panel.innerHTML = '';
            panel.classList.add('open');
            var cv = document.createElement('canvas');
            cv.width = 640; cv.height = 360;
            panel.appendChild(cv);
            var note = document.createElement('p');
            note.textContent = 'Systems anatomy of "' + heading + '" — whole, cut open, flow, parts. Step through it.';
            panel.appendChild(note);
            try { Viz.anatomy(cv, spec); } catch (err) { panel.innerHTML = '<p>The visual engine could not render this one.</p>'; }
          }
          if (cached) { render(JSON.parse(cached)); return; }
          tutorAsk('Turn this lesson into a systems-anatomy diagram spec. Reply with ONLY a JSON object ' +
            '(no markdown fences): {"parts":[{"id":"a","label":"..."}], "flows":[{"from":"a","to":"b","label":"..."}]} ' +
            'with 3-5 parts max.\n\nLESSON:\n' + text.slice(0, 1200))
            .then(function (txt) {
              var m = /\{[\s\S]*\}/.exec(txt || '');
              if (!m) throw new Error('no-json');
              var spec = JSON.parse(m[0]);
              cacheSet(ckA, JSON.stringify(spec));
              render(spec);
            })
            .catch(function () {
              /* Local fallback: linear anatomy from the slide's own key terms. */
              var terms = keyTerms(stage).slice(0, 4);
              if (terms.length < 2) terms = [heading, 'Core process', 'Result'];
              var parts = terms.map(function (t, i) { return { id: 'p' + i, label: t }; });
              var flows = [];
              for (var i = 0; i < parts.length - 1; i++) flows.push({ from: parts[i].id, to: parts[i + 1].id, label: 'feeds' });
              render({ parts: parts, flows: flows });
            });
        }).catch(function () {
          openPanel('<p>The animation engine (NoahViz) is not reachable from this page right now. The slide\'s own diagram still works — use the ↻ Replay diagram button.</p>');
        });
      }
    });

    /* Weak readers get highlighting automatically. */
    var lvl = level();
    if (lvl === 'struggling' || lvl === 'developing') {
      setTimeout(function () { highlight(stage); }, 350);
    }

    maybeKeepGoing(deck, heading, key);
    maybeRtfm(deck, heading);
  }

  /* ---------------- keep-going panel (final slide) ---------------- */

  function maybeKeepGoing(deck, heading, key) {
    var dots = deck.querySelectorAll('.learn-dot');
    var onIdx = -1;
    for (var i = 0; i < dots.length; i++) if (dots[i].classList.contains('on')) onIdx = i;
    if (!dots.length || onIdx !== dots.length - 1) return;
    if (deck.querySelector('.aix-keep')) return;
    var box = document.createElement('div');
    box.className = 'aix-read aix-keep';
    box.innerHTML = '<div class="aix-row"><span class="aix-tag">KEEP GOING</span>' +
      '<strong>Lock it in:</strong><span style="color:var(--muted)">one practice question for "' + esc(heading) + '"</span>' +
      '<button class="btn small primary" data-keep="go">Give me the question</button></div>' +
      '<div class="aix-panel" role="status"></div>';
    deck.appendChild(box);
    var panel = box.querySelector('.aix-panel');
    box.querySelector('[data-keep="go"]').addEventListener('click', function () {
      panel.classList.add('open');
      panel.innerHTML = '<p>Writing your question…</p>';
      var ck = 'keepq:' + key;
      var hit = cacheGet(ck);
      if (hit) { renderQ(JSON.parse(hit)); return; }
      if (window.AIClient) {
        window.AIClient.dynamic('generate_question', {
          domain: heading, difficulty: (window.AIDynamic ? window.AIDynamic.difficultyFor(heading) : 'medium'),
          skillLevel: level(), seed: key
        }).then(function (res) {
          if (res && res.question) { cacheSet(ck, JSON.stringify(res.question)); renderQ(res.question); }
          else { throw new Error('empty'); }
        }).catch(localQ);
      } else { localQ(); }
      function localQ() {
        renderQ({ situation: 'From "' + heading + '": explain the core idea in your own words, name one way it fails in production, and the first command or check you would run.',
                  answer: 'Compare against the lesson: core idea stated plainly, a REAL failure mode (not "it breaks"), and a specific first diagnostic step.' });
      }
      function renderQ(q) {
        panel.innerHTML = '<p>' + esc(q.situation || q.prompt || '') + '</p>' +
          '<button class="btn small ghost" data-keep="reveal">Reveal a strong answer</button>' +
          '<div class="aix-answer">' + esc(q.answer || q.why || 'Re-read the lesson and try again — the answer is in the worked example.') + '</div>';
        var rb = panel.querySelector('[data-keep="reveal"]');
        if (rb) rb.addEventListener('click', function () {
          panel.querySelector('.aix-answer').classList.add('open');
          if (window.AIDynamic) window.AIDynamic.recordAttempt(heading, true, {});
        });
      }
    });
  }

  /* ---------------- wiring ---------------- */

  var timer = null;
  function schedule() {
    if (timer) clearTimeout(timer);
    timer = setTimeout(enhance, 180);
  }
  function init() {
    injectCSS();
    var body = $('learnBody');
    if (!body) { setTimeout(init, 400); return; }
    if (window.MutationObserver) {
      new MutationObserver(schedule).observe(body, { childList: true, subtree: true });
    }
    document.addEventListener('ilb:view', function (e) {
      if (e && e.detail === 'learn') schedule();
    });
    schedule();
  }

  window.AIReading = { enhance: enhance, keyTerms: keyTerms, highlight: highlight };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
