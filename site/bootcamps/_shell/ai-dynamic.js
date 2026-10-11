/* Interstitium Labs — AI Dynamic Engine (ai-dynamic.js).
   AI as the ENGINE under labs and CBTs, making them dynamic. NOT course content.
   Vanilla JS, zero dependencies, ES5-compatible.
   Enhances labs.js, missions.js, shell-core.js drill workbench, terminal.js —
   does NOT replace them. All AI features degrade gracefully:
   remote (/api/noah) -> local heuristics -> pre-generated/static fallback.
   Exposes window.AIDynamic. */
(function () {
  'use strict';

  var SLUG = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.slug) || '';
  var LS_SKILL = 'ilb-bootcamp-' + SLUG + '-skill-v1';
  var LS_VARIANTS = 'ilb-bootcamp-' + SLUG + '-dynvar-v1';

  var LEVELS = ['struggling', 'developing', 'proficient', 'mastered'];
  var DYNAMIC_ENDPOINT = '/api/noah/dynamic';

  /* ---------------- skill profile ---------------- */

  function blankDomain() {
    return { attempts: 0, correct: 0, hintsUsed: 0, totalTimeSec: 0,
             level: 'developing', lastActive: null, streak: 0 };
  }

  function loadProfile() {
    var p;
    try { p = JSON.parse(localStorage.getItem(LS_SKILL)); } catch (e) { p = null; }
    if (!p || typeof p !== 'object') {
      p = { slug: SLUG, domains: {}, overall: 'developing',
            independenceScore: 1.0, updatedAt: null };
    }
    return p;
  }

  function saveProfile(p) {
    p.updatedAt = new Date().toISOString();
    try { localStorage.setItem(LS_SKILL, JSON.stringify(p)); } catch (e) {}
  }

  function domainProfile(p, domain) {
    var key = String(domain || 'general').toLowerCase();
    if (!p.domains[key]) p.domains[key] = blankDomain();
    return p.domains[key];
  }

  function recomputeLevel(dp) {
    if (dp.attempts < 3) return dp.level; /* not enough signal */
    var acc = dp.correct / dp.attempts;
    var hintRate = dp.hintsUsed / dp.attempts;
    var next;
    if (acc >= 0.85 && hintRate < 0.25) next = 'mastered';
    else if (acc >= 0.65 && hintRate < 0.5) next = 'proficient';
    else if (acc >= 0.4) next = 'developing';
    else next = 'struggling';
    /* Hysteresis: only move one step at a time to avoid oscillation. */
    var cur = LEVELS.indexOf(dp.level), want = LEVELS.indexOf(next);
    if (want > cur) dp.level = LEVELS[Math.min(cur + 1, 3)];
    else if (want < cur) dp.level = LEVELS[Math.max(cur - 1, 0)];
    return dp.level;
  }

  /* Record a scored attempt. ok=true/false. opts: {hintsUsed, timeSec}. */
  function recordAttempt(domain, ok, opts) {
    var p = loadProfile();
    var dp = domainProfile(p, domain);
    opts = opts || {};
    dp.attempts++;
    if (ok) { dp.correct++; dp.streak++; } else { dp.streak = 0; }
    dp.hintsUsed += (opts.hintsUsed || 0);
    dp.totalTimeSec += (opts.timeSec || 0);
    dp.lastActive = new Date().toISOString();
    recomputeLevel(dp);
    /* Independence score: fraction of attempts with zero hints, decayed. */
    var indep = opts.hintsUsed ? 0 : 1;
    p.independenceScore = Math.round((p.independenceScore * 0.9 + indep * 0.1) * 100) / 100;
    saveProfile(p);
    return dp.level;
  }

  function recordHint(domain) {
    var p = loadProfile();
    var dp = domainProfile(p, domain);
    dp.hintsUsed++;
    saveProfile(p);
  }

  function getLevel(domain) {
    var p = loadProfile();
    return domainProfile(p, domain).level;
  }

  function getProfile() { return loadProfile(); }

  /* Difficulty mapping: skill level -> question/scenario difficulty. */
  function difficultyFor(domain) {
    var lvl = getLevel(domain);
    return { struggling: 'easy', developing: 'medium',
             proficient: 'hard', mastered: 'expert' }[lvl] || 'medium';
  }

  /* ---------------- remote call ---------------- */

  function callDynamic(payload) {
    /* Prefer the unified AI client when loaded (same backend, cleaner path). */
    if (window.AIClient && window.AIClient.dynamic) {
      var action = payload.action;
      var rest = {};
      for (var k in payload) { if (payload.hasOwnProperty(k) && k !== 'action') rest[k] = payload[k]; }
      return window.AIClient.dynamic(action, rest);
    }
    var body = JSON.stringify(payload);
    return fetch(DYNAMIC_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body
    }).then(function (r) {
      if (!r.ok) throw new Error('dynamic ' + r.status);
      return r.json();
    });
  }

  function remoteAvailable() {
    /* The endpoint may not exist yet; probe once and cache. */
    if (typeof remoteAvailable._cache !== 'undefined') {
      return Promise.resolve(remoteAvailable._cache);
    }
    return fetch(DYNAMIC_ENDPOINT, { method: 'HEAD' }).then(function (r) {
      remoteAvailable._cache = (r.status !== 404);
      return remoteAvailable._cache;
    }).catch(function () {
      remoteAvailable._cache = false;
      return false;
    });
  }

  /* ---------------- pre-generated variant bank ---------------- */

  function loadVariantBank() {
    var b;
    try { b = JSON.parse(localStorage.getItem(LS_VARIANTS)); } catch (e) { b = null; }
    return b || {};
  }

  function bankVariants(kind, key) {
    var b = loadVariantBank();
    return (b[kind] && b[kind][key]) || [];
  }

  function pickVariant(variants, seedKey) {
    if (!variants.length) return null;
    /* Deterministic rotation: hash the seed key, rotate by day. */
    var h = 0, s = String(seedKey || '');
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    var day = Math.floor(Date.now() / 86400000);
    return variants[Math.abs(h + day) % variants.length];
  }

  /* ---------------- dynamic question generation ---------------- */

  /* Offline question mutator: takes a static scenario and produces a variant
     by swapping key parameters. Deterministic per student per day. */
  function mutateQuestion(item, seedKey) {
    if (!item) return null;
    var h = 0, s = String(seedKey || item.id || '');
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    var day = Math.floor(Date.now() / 86400000);
    var rng = mulberry(Math.abs(h) + day * 7919);

    /* Find swappable tokens: IPs, hostnames, usernames, ports, numbers. */
    var text = item.situation || item.desc || '';
    var swaps = extractSwappables(text);
    if (!swaps.length) return null;

    var mutated = {
      id: item.id + '-dyn',
      title: item.title,
      domain: item.domain,
      mins: item.mins,
      prompt: item.prompt,
      objectives: item.objectives,
      hint: item.hint,
      why: item.why,
      answer: item.answer,
      dynamic: true
    };
    /* Swap parameters in situation, evidence outputs, and choices. */
    mutated.situation = swapAll(item.situation, swaps, rng);
    mutated.desc = swapAll(item.desc, swaps, rng);
    if (item.evidence) {
      mutated.evidence = item.evidence.map(function (p) {
        return [p[0], swapAll(p[1], swaps, rng)];
      });
    }
    if (item.choices) {
      mutated.choices = item.choices.map(function (c) { return swapAll(c, swaps, rng); });
    }
    return mutated;
  }

  function extractSwappables(text) {
    var out = [], seen = {};
    text = String(text || '');
    var patterns = [
      { re: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g, gen: genIP },
      { re: /\b[A-Z]{2,}-[A-Z0-9]{2,8}-\d{1,4}\b/g, gen: genHostname },
      { re: /\b[a-z][a-z0-9]{2,7}\d{1,3}\b/g, gen: genUsername },
      { re: /\b(?:port\s+)(\d{2,5})\b/gi, gen: genPort }
    ];
    for (var i = 0; i < patterns.length; i++) {
      var m;
      patterns[i].re.lastIndex = 0;
      while ((m = patterns[i].re.exec(text))) {
        var v = m[0];
        if (!seen[v]) { seen[v] = true; out.push({ orig: v, gen: patterns[i].gen }); }
      }
    }
    return out;
  }

  function swapAll(text, swaps, rng) {
    var t = String(text || '');
    for (var i = 0; i < swaps.length; i++) {
      var repl = swaps[i].gen(rng);
      t = t.split(swaps[i].orig).join(repl);
    }
    return t;
  }

  function genIP(rng) {
    return '10.' + (1 + Math.floor(rng() * 254)) + '.' +
           Math.floor(rng() * 256) + '.' + (2 + Math.floor(rng() * 250));
  }
  function genHostname(rng) {
    var pre = ['SRV', 'WS', 'DC', 'FW', 'VPN', 'DB'][Math.floor(rng() * 6)];
    var mid = ['ORL', 'TPA', 'MIA', 'ATL', 'DFW'][Math.floor(rng() * 5)];
    return pre + '-' + mid + '-' + (100 + Math.floor(rng() * 900));
  }
  function genUsername(rng) {
    var names = ['tuser', 'jdoe', 'asmith', 'bwright', 'klee', 'mchen'];
    return names[Math.floor(rng() * names.length)] + (1 + Math.floor(rng() * 9));
  }
  function genPort(rng) {
    var ports = ['443', '3389', '22', '445', '1433', '5432', '1194', '51820'];
    return ports[Math.floor(rng() * ports.length)];
  }

  function mulberry(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* Main entry: get a dynamic question. Tries remote -> mutation -> static. */
  function dynamicQuestion(item, domain, opts) {
    opts = opts || {};
    var difficulty = opts.difficulty || difficultyFor(domain);
    /* 1. Remote generation. */
    return remoteAvailable().then(function (ok) {
      if (!ok) throw new Error('no-remote');
      return callDynamic({
        action: 'generate_question',
        domain: domain,
        difficulty: difficulty,
        skillLevel: getLevel(domain),
        sourceItem: { id: item.id, title: item.title, objectives: item.objectives },
        seed: String(Date.now())
      });
    }).then(function (res) {
      if (res && res.question) {
        res.question.dynamic = true;
        res.question.remote = true;
        return res.question;
      }
      throw new Error('bad-remote');
    }).catch(function () {
      /* 2. Offline variant bank. */
      var bank = bankVariants('questions', domain);
      var v = pickVariant(bank, domain + '-q');
      if (v) { v.dynamic = true; v.bank = true; return v; }
      /* 3. Local mutation of the static item. */
      var m = mutateQuestion(item, domain + '-' + (item.id || ''));
      if (m) return m;
      /* 4. Static fallback — the original item, unchanged. */
      return item;
    });
  }

  /* ---------------- adaptive hints ---------------- */

  var HINT_LEVELS = [
    'nudge',       /* look again */
    'directional', /* where to look */
    'specific',    /* what exactly */
    'walkthrough'  /* full steps */
  ];

  /* Local hint escalation: builds a progressive hint from the static hint
     and the student's failure context, without needing the network. */
  function localHint(staticHint, failCtx) {
    failCtx = failCtx || {};
    var level = failCtx.hintLevel || 0;
    var cmd = failCtx.lastCommand || '';
    var attempts = failCtx.attempts || 1;

    if (level === 0) {
      return 'Take another look at the output. What is it actually telling you? ' +
        (cmd ? 'Your last command was: ' + cmd : 'Try running the step again and read the result carefully.');
    }
    if (level === 1) {
      /* Point at the area, not the answer. */
      var area = guessProblemArea(staticHint);
      return 'The issue is in ' + area + '. ' +
        'You have made ' + attempts + ' attempt' + (attempts > 1 ? 's' : '') +
        ' — slow down and check each parameter against the step.';
    }
    if (level === 2) {
      /* Reveal the static hint — it is specific by design. */
      return staticHint || 'Review the step instructions line by line and compare with what you typed.';
    }
    /* Walkthrough: restate the objective as guided steps. */
    return (staticHint || 'Follow the lab steps in order.') +
      ' Walk through it slowly: read the step, type exactly what it says, ' +
      'then verify the output before moving on.';
  }

  function guessProblemArea(hint) {
    var h = String(hint || '').toLowerCase();
    if (/path|ou=|distinguished/i.test(h)) return 'the distinguished name / -Path parameter';
    if (/filter/i.test(h)) return 'the -Filter expression';
    if (/password|credential/i.test(h)) return 'the credential / password handling';
    if (/port|firewall|network/i.test(h)) return 'the network / port configuration';
    if (/permission|access|denied/i.test(h)) return 'permissions on the target object';
    return 'the command parameters';
  }

  /* Main entry: get an adaptive hint. level 0-3. */
  function adaptiveHint(opts) {
    opts = opts || {};
    var domain = opts.domain || 'general';
    var level = Math.min(Math.max(opts.level || 0, 0), 3);
    recordHint(domain);
    var failCtx = { hintLevel: level, lastCommand: opts.lastCommand,
                    attempts: opts.attempts || 1 };

    return remoteAvailable().then(function (ok) {
      if (!ok) throw new Error('no-remote');
      return callDynamic({
        action: 'hint',
        level: level,
        levelName: HINT_LEVELS[level],
        stuckOn: { objective: opts.objective, lastCommand: opts.lastCommand,
                   attempts: opts.attempts, staticHint: opts.staticHint },
        domain: domain,
        skillLevel: getLevel(domain)
      });
    }).then(function (res) {
      if (res && res.hint) return { text: res.hint, level: level, remote: true };
      throw new Error('bad-remote');
    }).catch(function () {
      return { text: localHint(opts.staticHint, failCtx), level: level, remote: false };
    });
  }

  /* ---------------- intelligent evaluation ---------------- */

  /* Local semantic-ish evaluation: beyond regex, understand common
     alternative approaches for terminal commands. */
  var COMMAND_EQUIVALENTS = [
    { patterns: [/get-aduser\s+-filter/i, /get-aduser\s+-identity/i],
      note: 'Both -Filter and -Identity can retrieve the user; -Identity is more direct for a known account.' },
    { patterns: [/select-object/i, /select\s/i],
      note: 'Select-Object and its alias select do the same thing.' },
    { patterns: [/\|\s*where/i, /-filter/i],
      note: 'Piping to Where-Object works, but -Filter runs server-side and is faster on large directories.' }
  ];

  function localEvaluate(studentWork, expected) {
    /* studentWork: array of command strings. expected: {command_pattern, expect_contains}. */
    var joined = (studentWork || []).join('\n');
    var notes = [];
    var matched = false;
    try {
      var rx = new RegExp(expected.command_pattern, 'i');
      matched = rx.test(joined);
    } catch (e) { matched = false; }
    var containsOk = !expected.expect_contains ||
      joined.toLowerCase().indexOf(String(expected.expect_contains).toLowerCase()) >= 0;

    for (var i = 0; i < COMMAND_EQUIVALENTS.length; i++) {
      var eq = COMMAND_EQUIVALENTS[i];
      var hitA = eq.patterns[0].test(joined);
      var hitB = eq.patterns.length > 1 && eq.patterns[1].test(joined);
      if (hitA || hitB) notes.push(eq.note);
    }
    /* Detect common failure modes. */
    if (/commandnotfound|not recognized/i.test(joined)) {
      notes.push('The command was not recognized — check spelling and that the required module is imported.');
    }
    return { matched: matched && containsOk, notes: notes,
             partial: matched !== containsOk };
  }

  /* Main entry: evaluate student work. Returns {correct, feedback, notes}. */
  function evaluateWork(opts) {
    opts = opts || {};
    var domain = opts.domain || 'general';
    var work = opts.work || [];
    var expected = opts.expected || {};

    return remoteAvailable().then(function (ok) {
      if (!ok) throw new Error('no-remote');
      return callDynamic({
        action: 'evaluate',
        objective: opts.objective,
        studentWork: work,
        expectedOutcome: expected.expect_contains,
        domain: domain,
        skillLevel: getLevel(domain)
      });
    }).then(function (res) {
      if (res && typeof res.correct !== 'undefined') {
        recordAttempt(domain, !!res.correct, { hintsUsed: opts.hintsUsed || 0,
                                               timeSec: opts.timeSec || 0 });
        return { correct: !!res.correct, feedback: res.feedback || '',
                 notes: res.notes || [], remote: true };
      }
      throw new Error('bad-remote');
    }).catch(function () {
      var local = localEvaluate(work, expected);
      recordAttempt(domain, local.matched, { hintsUsed: opts.hintsUsed || 0,
                                             timeSec: opts.timeSec || 0 });
      return { correct: local.matched, feedback: local.matched ?
        'Check passed.' : 'Not quite — compare your command against the step.',
        notes: local.notes, partial: local.partial, remote: false };
    });
  }

  /* ---------------- dynamic scenario generation ---------------- */

  /* Offline scenario mutation for labs: swaps parameters in steps/checks
     so each student gets a unique variant. */
  function mutateLab(lab, seedKey) {
    if (!lab) return lab;
    var h = 0, s = String(seedKey || lab.id || '');
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    var day = Math.floor(Date.now() / 86400000);
    var rng = mulberry(Math.abs(h) + day * 7919);

    var allText = (lab.steps || []).join('\n') + '\n' +
                  (lab.checks || []).map(function (c) { return c.hint || ''; }).join('\n');
    var swaps = extractSwappables(allText);
    if (!swaps.length) return lab;

    var mutated = {
      id: lab.id, title: lab.title, objective: lab.objective,
      success_message: lab.success_message, dynamic: true
    };
    mutated.steps = (lab.steps || []).map(function (st) { return swapAll(st, swaps, rng); });
    mutated.checks = (lab.checks || []).map(function (c) {
      return { command_pattern: swapAll(c.command_pattern, swaps, rng),
               expect_contains: swapAll(c.expect_contains, swaps, rng),
               hint: swapAll(c.hint, swaps, rng) };
    });
    return mutated;
  }

  function dynamicLab(lab, domain) {
    domain = domain || 'general';
    var difficulty = difficultyFor(domain);
    return remoteAvailable().then(function (ok) {
      if (!ok) throw new Error('no-remote');
      return callDynamic({
        action: 'generate_scenario',
        objective: lab.objective,
        domain: domain,
        difficulty: difficulty,
        skillLevel: getLevel(domain),
        sourceLab: { id: lab.id, title: lab.title, stepCount: (lab.steps || []).length },
        seed: String(Date.now())
      });
    }).then(function (res) {
      if (res && res.scenario) {
        var gen = {
          id: lab.id, title: lab.title, objective: lab.objective,
          success_message: lab.success_message,
          steps: res.scenario.steps || lab.steps,
          checks: res.scenario.checks || lab.checks,
          narrative: res.scenario.narrative || '',
          dynamic: true, remote: true
        };
        return gen;
      }
      throw new Error('bad-remote');
    }).catch(function () {
      var bank = bankVariants('labs', lab.id);
      var v = pickVariant(bank, lab.id + '-lab');
      if (v) {
        v.id = lab.id; v.title = lab.title; v.dynamic = true; v.bank = true;
        return v;
      }
      return mutateLab(lab, domain + '-' + lab.id);
    });
  }

  /* ---------------- public API ---------------- */

  window.AIDynamic = {
    /* skill profile */
    getProfile: getProfile,
    getLevel: getLevel,
    difficultyFor: difficultyFor,
    recordAttempt: recordAttempt,
    recordHint: recordHint,
    /* dynamic content */
    dynamicQuestion: dynamicQuestion,
    dynamicLab: dynamicLab,
    mutateQuestion: mutateQuestion,
    mutateLab: mutateLab,
    /* evaluation + hints */
    evaluateWork: evaluateWork,
    adaptiveHint: adaptiveHint,
    localEvaluate: localEvaluate,
    /* plumbing */
    remoteAvailable: remoteAvailable,
    HINT_LEVELS: HINT_LEVELS
  };
})();
