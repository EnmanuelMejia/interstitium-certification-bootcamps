/* Interstitium Labs — AI Pair Programmer (ai-coding.js).
   Codecademy-style AI pairing for the simulated consoles (code-editor,
   sql-studio) and any code surface in the shell:
   - Review my code: structured review from the code agent; offline,
     a local heuristic linter (balance, secrets, TODOs, debug prints)
   - Explain this error: harvests the console's latest error + the code,
     explains WHY it happened and the fix pattern, not just the message
   - New exercise: fresh per-topic exercises via the dynamic endpoint,
     with starter code and checkable success criteria
   - Ask: free-text question about the current code, answered in context
   Enhancement layer over consoles.js (observes #consoleBody). Never
   replaces it. Vanilla JS, zero dependencies, ES5-compatible. */
(function () {
  'use strict';

  var SLUG = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.slug) || 'bootcamp';
  var LS_CACHE = 'ilb-pair-cache-' + SLUG;

  var CSS = [
    '.aix-pair{margin:16px 0;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);padding:16px 18px}',
    '.aix-pair h4{margin:0 0 4px;font-size:15px}',
    '.aix-pair .aix-sub{color:var(--muted);font-size:13px;margin:0 0 12px}',
    '.aix-pair .aix-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}',
    '.aix-pair input[type=text]{flex:1;min-width:180px;background:var(--surface-2);border:1px solid var(--line);border-radius:8px;color:var(--ink);padding:9px 11px;font:14px var(--mono)}',
    '.aix-pair .aix-out{margin-top:12px;font-size:14px;line-height:1.6;white-space:pre-wrap;word-break:break-word}',
    '.aix-pair .aix-out:empty{display:none}',
    '.aix-pair pre{background:#0d1117;border:1px solid var(--line);border-radius:8px;padding:12px;overflow-x:auto;font:13px/1.7 var(--mono);margin:10px 0}',
    '.aix-pair .aix-tag{display:inline-block;font:600 11px var(--mono);letter-spacing:.06em;color:var(--accent);border:1px solid var(--line);border-radius:99px;padding:2px 9px;margin-bottom:8px}'
  ].join('\n');

  function injectCSS() {
    if (document.getElementById('aix-pair-css')) return;
    var st = document.createElement('style');
    st.id = 'aix-pair-css'; st.textContent = CSS;
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
      if (keys.length > 40) delete c[keys[0]];
      localStorage.setItem(LS_CACHE, JSON.stringify(c));
    } catch (e) {}
  }

  /* ---------------- code + error extraction ---------------- */

  function extractCode(scope) {
    var tas = scope.querySelectorAll('textarea');
    for (var i = 0; i < tas.length; i++) {
      if (tas[i].value && tas[i].value.trim().length > 3) return tas[i].value;
    }
    var ed = scope.querySelector('.csim-editor');
    if (ed) return ed.textContent.replace(/\n{2,}/g, '\n').trim();
    var pre = scope.querySelector('pre');
    return pre ? pre.textContent.trim() : '';
  }

  var ERROR_RE = /(error|exception|failed|denied|syntax|traceback|not recognized|commandnotfound)/i;
  function extractError(scope) {
    var nodes = scope.querySelectorAll('div, p, li, pre, code, span');
    var found = '';
    for (var i = 0; i < nodes.length; i++) {
      var t = (nodes[i].textContent || '').trim();
      if (t && t.length < 400 && ERROR_RE.test(t)) found = t;
    }
    return found;
  }

  /* ---------------- local heuristic linter (offline review) ---------------- */

  function localLint(code) {
    var notes = [];
    var opens = (code.match(/[{[(]/g) || []).length;
    var closes = (code.match(/[}\])]/g) || []).length;
    if (opens !== closes) notes.push('Delimiters look unbalanced: ' + opens + ' opening vs ' + closes +
      ' closing brackets/braces/parens. Count them pair by pair — a missing closer is the #1 cause of "unexpected end of input".');
    if (/TODO|FIXME|XXX/.test(code)) notes.push('Leftover TODO/FIXME markers — resolve or delete them before calling this done.');
    if (/(password|passwd|pwd|secret|api[_-]?key)\s*[:=]\s*['"][^'"]+['"]/i.test(code)) {
      notes.push('⚠ Hardcoded credential in the code. In real work this goes in an environment variable or vault — never in source.');
    }
    if (/\beval\s*\(/.test(code)) notes.push('eval() executes arbitrary text as code — a classic injection hole. Parse data instead.');
    if (/console\.log|print\s*\(/.test(code) && code.length > 400) notes.push('Debug output statements are still in here — fine while building, noise in production.');
    if (/select\s+\*/i.test(code)) notes.push('SELECT * pulls every column. Naming the columns you need is faster and survives schema changes.');
    var lines = code.split('\n');
    for (var i = 0; i < lines.length; i++) {
      if (lines[i].length > 120) { notes.push('Line ' + (i + 1) + ' is ' + lines[i].length + ' chars — break it up for readability.'); break; }
    }
    if (!notes.length) notes.push('No structural issues found by the offline linter. Structure looks clean — for a deeper review, reconnect and ask again.');
    return notes;
  }

  var ERROR_TABLE = [
    { re: /syntaxerror|unexpected token|unexpected end/i, why: 'The parser hit something it could not read — usually a missing/extra bracket, quote, or comma ABOVE the reported line. The reported line is where it gave up, not where the mistake is.' },
    { re: /nameerror|not defined|is not defined|cannot find the name/i, why: 'A name was used before it existed: typo, missing import, or the variable is scoped inside another block/function.' },
    { re: /typeerror|cannot read propert|cannot convert/i, why: 'An operation was applied to the wrong kind of value (e.g., calling a method on null/None). Trace the value back to where it was supposed to be set.' },
    { re: /401|unauthori[sz]ed/i, why: 'The server does not accept WHO you are: missing/expired token or wrong credentials. Authentication (who) comes before authorization (what).' },
    { re: /403|forbidden|access is denied/i, why: 'You ARE authenticated but not ALLOWED: a permissions/policy problem, not a password problem. Check the policy attached to the identity.' },
    { re: /connection refused|econnrefused|could not connect/i, why: 'Nothing is listening on that host:port — service down, wrong port, or a firewall silently dropping. Verify the service first, then the path.' },
    { re: /no such table|relation .* does not exist|unknown column/i, why: 'The schema does not match the query: wrong database, missing migration, or a misspelled table/column name. Compare against the actual schema.' },
    { re: /duplicate|unique constraint|primary key/i, why: 'The write collided with existing data — a uniqueness rule did its job. Decide: is this an update that was written as an insert?' }
  ];
  function localExplain(errText) {
    for (var i = 0; i < ERROR_TABLE.length; i++) {
      if (ERROR_TABLE[i].re.test(errText)) return ERROR_TABLE[i].why;
    }
    return 'Read the LAST line of the error first — it names the actual failure; the lines above are the path that got there. Then check: right names? right values? right order?';
  }

  /* ---------------- AI calls ---------------- */

  function agentCall(kind, code, extra) {
    if (!window.AIClient) return Promise.reject(new Error('no-client'));
    var prompt = '';
    if (kind === 'review') {
      prompt = 'Review this student code from a ' + SLUG + ' bootcamp exercise. Structure your reply: ' +
        '1) What is RIGHT about it (1-2 lines). 2) What to FIX, each with the reason WHY (max 4 items). ' +
        '3) One next-level improvement. Plain text, under 220 words.\n\nCODE:\n' + code;
    } else if (kind === 'error') {
      prompt = 'A student hit this error:\n' + extra + '\n\nTheir code:\n' + code +
        '\n\nExplain WHY this happened (the mechanism, not just the message) and the fix pattern. ' +
        'Plain text, under 150 words.';
    } else {
      prompt = 'The student asks about their code: "' + extra + '"\n\nCODE:\n' + code +
        '\n\nAnswer directly, with a tiny example if useful. Plain text, under 180 words.';
    }
    return window.AIClient.agent('code', prompt, { slug: SLUG }).then(function (r) { return r.answer; });
  }

  /* ---------------- pair panel ---------------- */

  function panelHTML() {
    return '<div class="aix-pair">' +
      '<span class="aix-tag">AI PAIR PROGRAMMER</span>' +
      '<h4>🤖 Code with Noah</h4>' +
      '<p class="aix-sub">Reviews, error explanations, and fresh exercises — tuned to your level.</p>' +
      '<div class="aix-row">' +
      '<button class="btn small primary" data-pair="review">Review my code</button>' +
      '<button class="btn small" data-pair="error">Explain the error</button>' +
      '<button class="btn small" data-pair="exercise">New exercise</button></div>' +
      '<div class="aix-row" style="margin-top:10px">' +
      '<input type="text" placeholder="Ask about this code…" aria-label="Ask about this code">' +
      '<button class="btn small ghost" data-pair="ask">Ask</button></div>' +
      '<div class="aix-out" role="status"></div></div>';
  }

  function attachPanel(scope) {
    var editor = scope.querySelector('.csim-editor') ||
                 scope.querySelector('textarea') ||
                 scope.querySelector('pre');
    if (!editor || scope.querySelector('.aix-pair')) return;
    var host = editor.parentNode;
    if (!host) return;
    var wrap = document.createElement('div');
    wrap.innerHTML = panelHTML();
    var panel = wrap.firstChild;
    if (editor.nextSibling) host.insertBefore(panel, editor.nextSibling);
    else host.appendChild(panel);

    var out = panel.querySelector('.aix-out');
    function busy(msg) { out.textContent = msg; }
    function show(text) { out.textContent = text; }

    panel.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-pair]') : null;
      if (!btn) return;
      var kind = btn.getAttribute('data-pair');
      var code = extractCode(scope);

      if (kind === 'review') {
        if (!code) { show('No code found yet — write something in the editor first, then ask for a review.'); return; }
        var ck = 'review:' + hashStr(code);
        var hit = cacheGet(ck);
        if (hit) { show(hit); return; }
        busy('🤖 Noah is reviewing…');
        agentCall('review', code).then(function (txt) { cacheSet(ck, txt); show(txt); })
          .catch(function () {
            show('🛠 Offline review (local linter):\n\n• ' + localLint(code).join('\n• '));
          });
        return;
      }
      if (kind === 'error') {
        var err = extractError(scope);
        if (!err) { show('No visible error in this console right now. Run your code — when it fails, ask again and I will explain the failure, not just quote it.'); return; }
        busy('🤖 Noah is diagnosing…');
        agentCall('error', code, err).then(function (txt) { show(txt); })
          .catch(function () { show('🛠 Offline diagnosis:\n\nError: ' + err + '\n\nWhy: ' + localExplain(err)); });
        return;
      }
      if (kind === 'exercise') {
        busy('🤖 Noah is writing you an exercise…');
        var level = (window.AIDynamic && window.AIDynamic.getLevel('coding')) || 'developing';
        if (window.AIClient) {
          window.AIClient.dynamic('generate_question', {
            domain: 'coding', difficulty: (window.AIDynamic ? window.AIDynamic.difficultyFor('coding') : 'medium'),
            skillLevel: level, seed: String(Date.now())
          }).then(function (res) {
            if (res && res.question) {
              var q = res.question;
              show('🎯 Exercise: ' + (q.title || 'Practice') + '\n' + (q.situation || q.prompt || '') +
                '\n\nSolve it in the editor above, then hit "Review my code" and I will grade your approach.');
            } else { throw new Error('empty'); }
          }).catch(function () { localExercise(show); });
        } else { localExercise(show); }
        return;
      }
      if (kind === 'ask') {
        var q2 = panel.querySelector('input').value.trim();
        if (!q2) { show('Type a question about this code first.'); return; }
        if (!code) { show('No code in the editor yet — the answer is better with code to look at.'); return; }
        busy('🤖 Noah is thinking…');
        agentCall('ask', code, q2).then(function (txt) { show(txt); })
          .catch(function () { show('🛠 Offline: I cannot reach the AI right now. Try "Review my code" — the local linter still works.'); });
      }
    });
    panel.querySelector('input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') panel.querySelector('[data-pair="ask"]').click();
    });
  }

  function localExercise(show) {
    var bank = [
      '🎯 Exercise: Write a function that takes a list of server names and returns only those ending in "-prod", sorted alphabetically. Then hit "Review my code".',
      '🎯 Exercise: Read a log line and extract the IP address and the HTTP status code into two variables. Test it on: 10.0.4.21 "GET /login" 403. Then hit "Review my code".',
      '🎯 Exercise: Write a loop that pings each host in a list and prints UP or DOWN per host (simulate the ping with a random boolean). Then hit "Review my code".',
      '🎯 Exercise: Given a dictionary of users and last-login days, print everyone inactive for 90+ days — the classic audit query. Then hit "Review my code".'
    ];
    show(bank[Math.floor(Math.random() * bank.length)]);
  }

  /* ---------------- wiring ---------------- */

  var scanQueued = false;
  function scan() {
    if (scanQueued) return;
    scanQueued = true;
    setTimeout(function () {
      scanQueued = false;
      var body = $('consoleBody');
      if (body) attachPanel(body);
    }, 60);
  }

  function init() {
    injectCSS();
    var body = $('consoleBody');
    if (!body) { setTimeout(init, 400); return; }
    if (window.MutationObserver) {
      new MutationObserver(scan).observe(body, { childList: true, subtree: true });
    }
    document.addEventListener('ilb:view', function (e) {
      if (e && e.detail === 'console') setTimeout(scan, 120);
    });
    scan();
  }

  window.AICoding = { lint: localLint, explainError: localExplain, attach: attachPanel };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
