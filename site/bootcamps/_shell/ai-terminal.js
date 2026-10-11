/* Interstitium Labs — AI Terminal Coach (ai-terminal.js).
   Makes the simulated terminal dynamic, adaptive, and personalized:
   - unique seeded session environment (hostname/user/site) per student
   - typo rescue ("did you mean ...?") against a command vocabulary
   - error coaching: local rule table instantly, tutor AI on repeat errors
   - `ai` meta-commands: help / explain / challenge / hint / quiz / answer
   Enhancement layer over terminal.js via its published contract
   (ILBTerminal.onCommand / ILBTerminal.print). Never replaces it.
   Vanilla JS, zero dependencies, ES5-compatible. Degrades silently
   offline: local coaching and the local challenge bank always work. */
(function () {
  'use strict';

  var SLUG = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.slug) || 'bootcamp';
  var SS_ENV = 'ilb-term-env-' + SLUG;
  var DOMAIN = SLUG.replace(/-/g, ' ');

  /* ---------------- seeded session environment ---------------- */

  function hashStr(s) {
    var h = 0; s = String(s || '');
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    return Math.abs(h);
  }
  function mulberry(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function sessionEnv() {
    var raw = null;
    try { raw = sessionStorage.getItem(SS_ENV); } catch (e) {}
    if (raw) { try { return JSON.parse(raw); } catch (e) {} }
    var seed = String(Date.now()) + '-' + Math.floor(Math.random() * 1e9);
    try { sessionStorage.setItem(SS_ENV + '-seed', seed); } catch (e) {}
    var rng = mulberry(hashStr(seed + SLUG));
    var sites = ['ORL', 'TPA', 'MIA', 'ATL', 'DFW', 'CLT'];
    var roles = ['SRV', 'WS', 'DC', 'APP', 'DB'];
    var users = ['student', 'trainee', 'labuser', 'candidate'];
    var env = {
      hostname: roles[Math.floor(rng() * roles.length)] + '-' +
                sites[Math.floor(rng() * sites.length)] + '-' +
                (100 + Math.floor(rng() * 900)),
      user: users[Math.floor(rng() * users.length)] + (1 + Math.floor(rng() * 9)),
      subnet: '10.' + (1 + Math.floor(rng() * 40)) + '.' + Math.floor(rng() * 200),
      seed: seed
    };
    try { sessionStorage.setItem(SS_ENV, JSON.stringify(env)); } catch (e) {}
    return env;
  }

  /* ---------------- command vocabulary (typo rescue) ---------------- */

  var KNOWN = ('ls dir cd pwd mkdir rmdir rm cp mv cat type echo clear cls help exit hostname whoami ' +
    'ipconfig ifconfig ping tracert traceroute nslookup netstat route arp telnet ssh curl wget ' +
    'get-aduser get-adcomputer get-adgroup get-service get-process get-eventlog get-childitem ' +
    'get-netipaddress get-netadapter test-connection test-netconnection restart-service stop-process ' +
    'set-adaccountpassword unlock-adaccount enable-adaccount disable-adaccount new-aduser ' +
    'kubectl docker systemctl service journalctl ps top kill grep find awk sed chmod chown sudo apt yum dnf ' +
    'show configure terminal interface vlan switchport trunk access shutdown no end write copy running-config ' +
    'select insert update delete from where join group order limit create table drop ' +
    'git python python3 node npm pip az aws gcloud terraform ansible ' +
    'gpupdate gpresult dsquery dsmod net user group localgroup share use view time ' +
    'sc query config tasklist taskkill reg query add systeminfo ver ipconfig').split(' ');

  function levenshtein(a, b) {
    var m = a.length, n = b.length, i, j;
    if (Math.abs(m - n) > 2) return 99;
    var prev = [], cur = [];
    for (j = 0; j <= n; j++) prev[j] = j;
    for (i = 1; i <= m; i++) {
      cur[0] = i;
      for (j = 1; j <= n; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1,
          prev[j - 1] + (a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1));
      }
      var t = prev; prev = cur; cur = t;
    }
    return prev[n];
  }

  function typoSuggestion(token) {
    var t = token.toLowerCase();
    if (t.length < 3 || KNOWN.indexOf(t) >= 0) return null;
    /* Not a bare command (hyphens are fine — cmdlets have them): paths,
       drive letters, flags, assignments, and filenames are excluded. */
    if (/[\/=.\\:]/.test(t) || t.charAt(0) === '-') return null;
    var best = null, bestD = 3;
    for (var i = 0; i < KNOWN.length; i++) {
      var d = levenshtein(t, KNOWN[i]);
      if (d < bestD) { bestD = d; best = KNOWN[i]; }
    }
    return (best && bestD <= 2) ? best : null;
  }

  /* ---------------- error coaching ---------------- */

  var ERROR_RULES = [
    { re: /commandnotfound|not recognized as (the name of )?a cmdlet|command not found|: command not found/i,
      family: 'not-found',
      tip: 'That command was not recognized. Check the spelling first — and that the right shell/module is loaded (PowerShell cmdlets differ from Linux commands).' },
    { re: /cannot find the path|no such file or directory|path not found|cannot find path/i,
      family: 'no-such-file',
      tip: 'That path does not exist here. List the current directory (ls / dir) and verify each segment of the path — one wrong folder name breaks the whole chain.' },
    { re: /access is denied|permission denied|unauthorized/i,
      family: 'permission',
      tip: 'Access denied. This usually means the shell is not elevated or your account lacks rights on the target. Note WHICH object denied you — that is the clue.' },
    { re: /syntax|parameter cannot be found|missing argument|invalid switch/i,
      family: 'syntax',
      tip: 'The command shape is off — a parameter name or value is wrong. Compare against the step word for word; parameter spelling is exact.' },
    { re: /timed out|unreachable|could not resolve|name resolution|network path was not found/i,
      family: 'network',
      tip: 'Network layer problem: name resolution or reachability. Work bottom-up — ping the IP first, then the name, to separate DNS from routing.' },
    { re: /logon failure|authentication failed|bad password|account.*locked/i,
      family: 'auth',
      tip: 'Authentication failed. Verify the username format (DOMAIN\\user vs user@domain) and check whether the account is locked before retrying.' }
  ];

  function classifyError(output) {
    var out = String(output || '');
    for (var i = 0; i < ERROR_RULES.length; i++) {
      if (ERROR_RULES[i].re.test(out)) return ERROR_RULES[i];
    }
    return null;
  }

  /* ---------------- coach state ---------------- */

  var state = {
    history: [],          /* [{cmd, output}] last 25 */
    errorStreak: 0,
    lastTipAt: 0,
    cleanStreak: 0,
    challenge: null,      /* {title, objective, checks:[{pattern, expect}], narrative} */
    challengeHints: 0,
    quiz: null            /* {question, keywords:[...]} */
  };

  function print(lines) {
    if (!window.ILBTerminal) return;
    if (typeof lines === 'string') lines = [lines];
    for (var i = 0; i < lines.length; i++) window.ILBTerminal.print(lines[i]);
  }

  function tipAllowed() {
    var now = Date.now();
    if (now - state.lastTipAt < 15000) return false;
    state.lastTipAt = now;
    return true;
  }

  function level() {
    return (window.AIDynamic && window.AIDynamic.getLevel(DOMAIN)) || 'developing';
  }

  function wrap(text, width) {
    var words = String(text || '').split(/\s+/), lines = [], cur = '';
    for (var i = 0; i < words.length; i++) {
      if ((cur + ' ' + words[i]).length > width && cur) { lines.push(cur); cur = words[i]; }
      else cur = cur ? cur + ' ' + words[i] : words[i];
    }
    if (cur) lines.push(cur);
    return lines;
  }

  function aiAsk(taskType, promptText) {
    if (!window.AIClient) return Promise.reject(new Error('no-client'));
    return window.AIClient.route(taskType, [{ role: 'user', content: promptText }], { maxTokens: 500 });
  }

  /* ---------------- ai meta-commands ---------------- */

  var LOCAL_CHALLENGES = [
    { title: 'Find the failing service',
      objective: 'A critical service is stopped. Find which one and report its exact name.',
      narrative: 'The monitoring board is red. Somewhere on this host a service that should be running is stopped.',
      checks: [ { pattern: 'get-service|sc\\s+query|systemctl\\s+status|service\\s+\\S+\\s+status', expect: '' } ] },
    { title: 'Trace the unreachable host',
      objective: 'Prove whether the problem is DNS or routing: test by IP first, then by name.',
      narrative: 'Users cannot reach the file server by name. Determine which layer is broken.',
      checks: [ { pattern: 'ping|test-connection|test-netconnection', expect: '' },
                { pattern: 'nslookup|resolve-dnsname|dig\\s', expect: '' } ] },
    { title: 'Audit the directory',
      objective: 'List the accounts in the directory and find the locked-out user.',
      narrative: 'A user reports being locked out after the weekend. Audit the accounts.',
      checks: [ { pattern: 'get-aduser|search-adaccount|net\\s+user', expect: '' } ] },
    { title: 'Map the network',
      objective: 'Document this host: its IP configuration, gateway, and listening ports.',
      narrative: 'You inherited this host with zero documentation. Build the picture.',
      checks: [ { pattern: 'ipconfig|get-netipaddress|ifconfig|ip\\s+a', expect: '' },
                { pattern: 'netstat|get-nettcpconnection|ss\\s+-', expect: '' } ] }
  ];

  function startChallenge() {
    print(['', '🤖 Noah is preparing a challenge at your level (' + level() + ')…']);
    var done = function (ch) {
      state.challenge = { title: ch.title, objective: ch.objective,
        narrative: ch.narrative || '', checks: ch.checks || [], doneFlags: [] };
      state.challengeHints = 0;
      print(['', '🎯 CHALLENGE: ' + ch.title, ch.narrative, 'Objective: ' + ch.objective,
        'Work in this terminal. I am watching your commands — finish the objective and I will confirm it.']);
    };
    if (window.AIDynamic && window.AIClient) {
      window.AIClient.dynamic('generate_scenario', {
        objective: 'Terminal troubleshooting practice for ' + DOMAIN,
        domain: DOMAIN, difficulty: window.AIDynamic.difficultyFor(DOMAIN), skillLevel: level()
      }).then(function (res) {
        if (res && res.scenario && res.scenario.steps) {
          done({ title: res.scenario.title || 'AI challenge',
                 objective: res.scenario.objective || 'Complete the scenario steps.',
                 narrative: res.scenario.narrative || '',
                 checks: (res.scenario.checks || []).map(function (c) {
                   return { pattern: c.command_pattern || '', expect: c.expect_contains || '' };
                 }) });
        } else {
          done(LOCAL_CHALLENGES[Math.floor(Math.random() * LOCAL_CHALLENGES.length)]);
        }
      }).catch(function () {
        done(LOCAL_CHALLENGES[Math.floor(Math.random() * LOCAL_CHALLENGES.length)]);
      });
    } else {
      done(LOCAL_CHALLENGES[Math.floor(Math.random() * LOCAL_CHALLENGES.length)]);
    }
  }

  function checkChallenge(cmd) {
    var ch = state.challenge;
    if (!ch) return;
    var remaining = 0;
    for (var i = 0; i < ch.checks.length; i++) {
      if (ch.doneFlags[i]) continue;
      var ok = true;
      try { ok = !ch.checks[i].pattern || new RegExp(ch.checks[i].pattern, 'i').test(cmd); }
      catch (e) { ok = true; }
      if (ok && ch.checks[i].expect) {
        ok = cmd.toLowerCase().indexOf(String(ch.checks[i].expect).toLowerCase()) >= 0;
      }
      if (ok) ch.doneFlags[i] = true; else remaining++;
    }
    if (ch.checks.length && remaining === 0) {
      state.challenge = null;
      if (window.AIDynamic) window.AIDynamic.recordAttempt(DOMAIN, true, { hintsUsed: state.challengeHints });
      print(['', '🏆 Challenge complete: ' + ch.title,
        'Noah: clean work. Type "ai challenge" for another — they get harder as you improve.']);
    }
  }

  function handleAiCommand(cmd) {
    var rest = cmd.replace(/^ai\s*/i, '');
    var parts = rest.split(/\s+/);
    var sub = (parts[0] || '').toLowerCase();

    if (!sub || sub === 'help') {
      print(['', '🤖 Noah — your AI terminal coach. Commands:',
        '  ai explain <topic>   — a plain-language explanation, right here',
        '  ai challenge         — a hands-on challenge at your level',
        '  ai hint              — a hint for the active challenge',
        '  ai quiz              — one quick question; answer with: ai answer <text>',
        '  ai env               — show this session\'s unique environment',
        'I also coach automatically: typos, errors, and wrong turns.']);
      return;
    }
    if (sub === 'env') {
      var e = sessionEnv();
      print(['', '🖥  Session environment (unique to you, this session):',
        '  Hostname : ' + e.hostname, '  User     : ' + e.user,
        '  Subnet   : ' + e.subnet + '.0/24']);
      return;
    }
    if (sub === 'challenge') { startChallenge(); return; }
    if (sub === 'hint') {
      if (!state.challenge) { print(['', '🤖 No active challenge. Type "ai challenge" to start one.']); return; }
      state.challengeHints++;
      if (window.AIDynamic) {
        window.AIDynamic.adaptiveHint({ domain: DOMAIN, level: Math.min(state.challengeHints - 1, 3),
          objective: state.challenge.objective, staticHint: state.challenge.objective,
          lastCommand: state.history.length ? state.history[state.history.length - 1].cmd : '' })
          .then(function (h) { print(['', '💡 ' + h.text]); });
      } else {
        print(['', '💡 Re-read the objective and work it one verb at a time: ' + state.challenge.objective]);
      }
      return;
    }
    if (sub === 'explain') {
      var topic = rest.replace(/^explain\s*/i, '');
      if (!topic) { print(['', '🤖 Usage: ai explain <topic>']); return; }
      print(['', '🤖 Noah is thinking about "' + topic + '"…']);
      aiAsk('tutor', 'Explain "' + topic + '" to a ' + level() + '-level IT student preparing for ' +
        DOMAIN + '. Plain text only, no markdown, under 130 words, one concrete example.')
        .then(function (res) { print([''].concat(wrap('🤖 ' + res.reply, 100))); })
        .catch(function () {
          print(['🤖 (offline) Break "' + topic + '" into parts: what it is, what it does, ' +
            'and the one command or screen where you see it. The Learn tab covers it in depth.']);
        });
      return;
    }
    if (sub === 'quiz') {
      print(['', '🤖 Noah is writing you a question…']);
      aiAsk('tutor', 'Ask ONE short troubleshooting question about ' + DOMAIN +
        ' for a ' + level() + ' student. Plain text. End with a line "KEYWORDS: a, b, c" ' +
        'listing 3-5 words a correct answer must contain.')
        .then(function (res) {
          var m = /KEYWORDS:\s*(.+)$/im.exec(res.reply || '');
          var kws = m ? m[1].split(/[,;]/).map(function (s) { return s.trim().toLowerCase(); }) : [];
          state.quiz = { question: (res.reply || '').replace(/KEYWORDS:.*$/im, '').trim(), keywords: kws };
          print([''].concat(wrap('❓ ' + state.quiz.question, 100),
            ['Answer with: ai answer <your answer>']));
        })
        .catch(function () {
          state.quiz = { question: 'A user cannot reach a server by name but CAN by IP. What is the likely failing layer, and what do you test first?',
            keywords: ['dns', 'name', 'resolution'] };
          print(['', '❓ ' + state.quiz.question, 'Answer with: ai answer <your answer>']);
        });
      return;
    }
    if (sub === 'answer') {
      var ans = rest.replace(/^answer\s*/i, '');
      if (!state.quiz) { print(['', '🤖 No open question. Type "ai quiz" first.']); return; }
      var q = state.quiz; state.quiz = null;
      var hits = 0;
      for (var i = 0; i < q.keywords.length; i++) {
        if (ans.toLowerCase().indexOf(q.keywords[i]) >= 0) hits++;
      }
      var ok = q.keywords.length === 0 ? ans.length > 10 : hits >= Math.ceil(q.keywords.length / 2);
      if (window.AIDynamic) window.AIDynamic.recordAttempt(DOMAIN, ok, {});
      print(['', ok ? '✅ Correct — you hit the key ideas. That is the interview answer.'
                    : '❌ Not quite — a strong answer mentions: ' + q.keywords.join(', ') + '.']);
      return;
    }
    print(['', '🤖 Unknown ai command. Type "ai help".']);
  }

  /* ---------------- main command hook ---------------- */

  function onCommand(cmd, output) {
    cmd = String(cmd || '');
    output = String(output || '');
    state.history.push({ cmd: cmd, output: output });
    if (state.history.length > 25) state.history.shift();

    /* ai meta-commands */
    if (/^ai(\s|$)/i.test(cmd)) { handleAiCommand(cmd); return; }

    /* challenge tracking */
    checkChallenge(cmd);

    /* typo rescue */
    var first = cmd.trim().split(/\s+/)[0] || '';
    var suggestion = typoSuggestion(first);
    if (suggestion && tipAllowed()) {
      print(['', '💡 Noah: did you mean "' + suggestion + '"? Command names are exact — one wrong letter and the shell cannot find it.']);
      state.errorStreak = 0;
      return;
    }

    /* error coaching */
    var rule = classifyError(output);
    if (rule) {
      state.errorStreak++;
      state.cleanStreak = 0;
      if (state.errorStreak === 1 && tipAllowed()) {
        print(['', '💡 Noah: ' + rule.tip]);
      } else if (state.errorStreak >= 2 && tipAllowed()) {
        state.errorStreak = 0; /* reset after escalation */
        var tail = output.split('\n').slice(-6).join('\n');
        aiAsk('tutor', 'A ' + level() + '-level student ran: ' + cmd + '\nOutput:\n' + tail +
          '\nGive ONE specific next step and the reason, plain text, under 60 words. No markdown.')
          .then(function (res) { print([''].concat(wrap('🤖 Noah: ' + res.reply, 100))); })
          .catch(function () { print(['', '💡 Noah: ' + rule.tip]); });
        /* 2026-10-11: Stack Overflow lookup for the failing command/error
           (Knowledge Source Layer; attributed, fire-and-forget). */
        try {
          var errLine = tail.split('\n').filter(function (l) { return l.trim(); }).pop() || rule.family;
          var soQ = ((cmd.trim().split(/\s+/)[0] || '') + ' ' + errLine).slice(0, 120);
          fetch('/api/sources/stackoverflow?limit=2&q=' + encodeURIComponent(soQ))
            .then(function (r) { return r.json(); })
            .then(function (j) {
              var top = j && j.results && j.results[0];
              if (top) {
                print(['', '📚 Stack Overflow: "' + top.title + '"' +
                  ' (' + (top.meta.answers || 0) + ' answers, score ' + (top.meta.score || 0) + ')',
                  '   ' + top.url]);
              }
            })
            .catch(function () {});
        } catch (e) {}
      }
      return;
    }

    /* clean command streaks feed the shared skill profile */
    state.errorStreak = 0;
    if (cmd.trim()) {
      state.cleanStreak++;
      if (state.cleanStreak >= 10) {
        state.cleanStreak = 0;
        if (window.AIDynamic) window.AIDynamic.recordAttempt(DOMAIN, true, {});
      }
    }
  }

  /* ---------------- wiring ---------------- */

  function wire() {
    if (!window.ILBTerminal) { setTimeout(wire, 300); return; }
    window.ILBTerminal.onCommand(onCommand);
    document.addEventListener('ilb:view', function (e) {
      if (e && e.detail === 'terminal' && !wire._banner) {
        wire._banner = true;
        var env = sessionEnv();
        setTimeout(function () {
          print(['', '🤖 Noah AI is coaching this terminal. Your session environment: host ' +
            env.hostname + ', user ' + env.user + ', subnet ' + env.subnet + '.0/24.',
            'Type "ai help" for coaching commands, or "ai challenge" to train.']);
        }, 600);
      }
    });
  }

  window.AITerminal = {
    env: sessionEnv,
    state: function () { return state; },
    _levenshtein: levenshtein,
    _classifyError: classifyError,
    _typoSuggestion: typoSuggestion
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else { wire(); }
})();
