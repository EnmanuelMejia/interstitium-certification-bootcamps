/* Interstitium Labs — Adaptive Math Engine (ai-math.js).
   ALEKS-style knowledge-space tutoring over _shell/math.json:
   - per-module knowledge state: mastery (EMA), misconception ledger
   - prerequisite chain -> the student's "learning frontier"
   - problems generated at the edge of ability: AI first (/api/ai/route,
     task type "math"), local parameterized generators offline
   - wrong answers are DIAGNOSED: each generator enumerates the classic
     distractor computations, so feedback names the misconception
   - worked solutions are ANIMATED SVG (place-value chart, number line,
     bar chart, coordinate grid), synchronized step-by-step
   Mounts into Learn "Your turn" (tryit) slides and adds an Adaptive
   Math Practice launcher when the bootcamp carries math sections.
   Vanilla JS, zero dependencies, ES5-compatible. */
(function () {
  'use strict';

  var SLUG = (window.BOOTCAMP_PAGE && window.BOOTCAMP_PAGE.slug) || 'bootcamp';
  var LS_STATE = 'ilb-math-state-v1';
  var MODULE_ORDER = ['binary', 'logic', 'subnetting', 'stats', 'probability', 'linalg'];
  var PREREQ = { subnetting: ['binary'], probability: ['stats'] };

  var CSS = [
    '.aix-math{margin-top:18px;border:1px solid var(--line);border-radius:var(--radius);background:var(--surface);padding:18px}',
    '.aix-math h4{margin:0 0 4px;font-size:16px}',
    '.aix-math .aix-sub{color:var(--muted);font-size:13px;margin:0 0 14px}',
    '.aix-math .aix-q{font:600 17px/1.5 var(--mono);margin:0 0 12px}',
    '.aix-math .aix-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}',
    '.aix-math input[type=text]{flex:1;min-width:160px;background:var(--surface-2);border:1px solid var(--line);border-radius:8px;color:var(--ink);padding:10px 12px;font:15px var(--mono)}',
    '.aix-math .aix-fb{margin-top:12px;font-size:14px;line-height:1.55}',
    '.aix-math .aix-fb.good{color:#3fb950}.aix-math .aix-fb.bad{color:#f85149}',
    '.aix-math .aix-steps{margin:14px 0 0;padding:0;list-style:none}',
    '.aix-math .aix-steps li{opacity:.25;transform:translateX(-4px);transition:opacity .5s,transform .5s;padding:7px 10px;border-left:3px solid var(--line);font:14px/1.55 var(--mono);margin-bottom:6px}',
    '.aix-math .aix-steps li.on{opacity:1;transform:none;border-left-color:var(--accent)}',
    '.aix-math svg{display:block;max-width:100%;margin:12px auto 4px}',
    '.aix-math .aix-viz-el{opacity:0;transition:opacity .6s}',
    '.aix-math .aix-viz-el.on{opacity:1}',
    '.aix-math .aix-meter{height:8px;background:var(--surface-2);border-radius:99px;overflow:hidden;margin:6px 0 12px}',
    '.aix-math .aix-meter i{display:block;height:100%;background:var(--accent);transition:width .8s}',
    '.aix-launch{cursor:pointer}',
    '@media (prefers-reduced-motion: reduce){.aix-math .aix-steps li,.aix-math .aix-viz-el,.aix-math .aix-meter i{transition:none}}'
  ].join('\n');

  function injectCSS() {
    if (document.getElementById('aix-math-css')) return;
    var st = document.createElement('style');
    st.id = 'aix-math-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function $(id) { return document.getElementById(id); }
  function rnd(lo, hi) { return lo + Math.floor(Math.random() * (hi - lo + 1)); }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
  function round2(n) { return Math.round(n * 100) / 100; }

  /* ---------------- knowledge state ---------------- */

  function blankState() {
    var s = { modules: {}, updatedAt: null };
    for (var i = 0; i < MODULE_ORDER.length; i++) {
      s.modules[MODULE_ORDER[i]] = { mastery: 0, attempts: 0, correct: 0, misconceptions: {}, streakWrong: 0 };
    }
    return s;
  }
  function loadState() {
    var s;
    try { s = JSON.parse(localStorage.getItem(LS_STATE)); } catch (e) { s = null; }
    if (!s || !s.modules) s = blankState();
    for (var i = 0; i < MODULE_ORDER.length; i++) {
      if (!s.modules[MODULE_ORDER[i]]) s.modules[MODULE_ORDER[i]] = blankState().modules[MODULE_ORDER[i]];
    }
    return s;
  }
  function saveState(s) {
    s.updatedAt = new Date().toISOString();
    try { localStorage.setItem(LS_STATE, JSON.stringify(s)); } catch (e) {}
  }
  function frontier(state) {
    /* First module (in chain order) whose prereqs are mastered but which is not. */
    for (var i = 0; i < MODULE_ORDER.length; i++) {
      var id = MODULE_ORDER[i];
      var pre = PREREQ[id] || [];
      var ready = true;
      for (var j = 0; j < pre.length; j++) {
        if ((state.modules[pre[j]] || {}).mastery < 0.8) ready = false;
      }
      if (ready && state.modules[id].mastery < 0.9) return id;
    }
    return 'binary';
  }
  function recordResult(moduleId, ok, misconceptionTag) {
    var s = loadState();
    var m = s.modules[moduleId];
    m.attempts++;
    if (ok) { m.correct++; m.streakWrong = 0; } else { m.streakWrong++; }
    /* EMA mastery: correct pulls up fast early, wrong pulls down gently. */
    var target = ok ? 1 : 0;
    var rate = m.attempts < 5 ? 0.3 : 0.18;
    m.mastery = Math.round((m.mastery + (target - m.mastery) * rate) * 100) / 100;
    if (!ok && misconceptionTag) {
      m.misconceptions[misconceptionTag] = (m.misconceptions[misconceptionTag] || 0) + 1;
    }
    saveState(s);
    if (window.AIDynamic) window.AIDynamic.recordAttempt('math', ok, {});
    return s;
  }

  /* ---------------- local generators ----------------
     Each returns {module, question, answer, tolerance, unit, steps[],
     viz:{type,...}, distractors:[{value, tag, feedback}]}            */

  function genBinary() {
    var kind = pick(['d2b', 'b2d', 'pow', 'count']);
    if (kind === 'd2b') {
      var n = rnd(9, 250);
      /* Avoid palindromes: reversed bits would equal the answer and the
         read-backwards trap could not be diagnosed. */
      while (n.toString(2) === n.toString(2).split('').reverse().join('')) n++;
      return { module: 'binary', question: 'Convert ' + n + ' (decimal) to binary.',
        answer: n.toString(2), tolerance: 0, unit: '',
        steps: ['Divide by 2 repeatedly, recording remainders.', 'Remainders for ' + n + ': ' +
          remainders(n).join(', ') + '.', 'Read the remainders bottom-up: ' + n.toString(2) + '.'],
        viz: { type: 'placevalue', bits: n.toString(2) },
        distractors: [ { value: String(reversedBits(n)), tag: 'read-backwards',
          feedback: 'You read the remainders in the wrong direction — binary is written most-significant bit first (left to right).' } ] };
    }
    if (kind === 'b2d') {
      var b = ''; var bits = rnd(5, 8);
      for (var i = 0; i < bits; i++) b += Math.random() < 0.5 ? '0' : '1';
      if (b.charAt(0) === '0') b = '1' + b.slice(1);
      var v = parseInt(b, 2);
      return { module: 'binary', question: 'Convert binary ' + b + ' to decimal.',
        answer: String(v), tolerance: 0, unit: '',
        steps: placeSteps(b), viz: { type: 'placevalue', bits: b },
        distractors: [ { value: String(v + 1), tag: 'off-by-one',
          feedback: 'Off by one — the rightmost bit is worth 2^0 = 1, not 2. Start counting powers from 0.' } ] };
    }
    if (kind === 'pow') {
      var p = rnd(4, 12);
      return { module: 'binary', question: 'What is 2^' + p + '?', answer: String(Math.pow(2, p)),
        tolerance: 0, unit: '', steps: ['Double 1 exactly ' + p + ' times.', '2^' + p + ' = ' + Math.pow(2, p) + '.'],
        viz: { type: 'numberline', value: Math.pow(2, p), max: Math.pow(2, p) },
        distractors: [ { value: String(2 * p), tag: 'times-not-power',
          feedback: '2^' + p + ' means 2 multiplied by itself ' + p + ' times — not 2 × ' + p + '.' } ] };
    }
    var c = rnd(3, 10);
    return { module: 'binary', question: 'How many different values can ' + c + ' bits represent?',
      answer: String(Math.pow(2, c)), tolerance: 0, unit: '',
      steps: ['Each bit doubles the combinations.', c + ' bits → 2^' + c + ' = ' + Math.pow(2, c) + ' values.'],
      viz: { type: 'placevalue', bits: '1' + new Array(c).join('0') },
      distractors: [ { value: String(Math.pow(2, c) - 1), tag: 'max-vs-count',
        feedback: 'That is the LARGEST value, not the COUNT. ' + c + ' bits count from 0 to ' + (Math.pow(2, c) - 1) + ' — which is ' + Math.pow(2, c) + ' values.' } ] };
  }
  function remainders(n) {
    var out = [];
    while (n > 0) { out.push(n % 2); n = Math.floor(n / 2); }
    return out;
  }
  function reversedBits(n) {
    return n.toString(2).split('').reverse().join('').replace(/^0+/, '') || '0';
  }
  function placeSteps(b) {
    var steps = [], sum = 0, parts = [];
    for (var i = 0; i < b.length; i++) {
      var power = b.length - 1 - i;
      if (b.charAt(i) === '1') { parts.push('2^' + power); sum += Math.pow(2, power); }
    }
    steps.push('Label each bit with its place value: powers of two, right to left from 2^0.');
    steps.push('Add only the places holding a 1: ' + parts.join(' + ') + ' = ' + sum + '.');
    return steps;
  }

  function genSubnetting() {
    var prefix = pick([22, 23, 24, 25, 26, 27, 28, 29, 30]);
    var hostBits = 32 - prefix;
    var total = Math.pow(2, hostBits);
    var kind = pick(['hosts', 'usable', 'network']);
    if (kind === 'network') {
      var oct = rnd(1, 200), last = rnd(1, 254);
      var block = total;
      var net = Math.floor(last / block) * block;
      return { module: 'subnetting',
        question: 'Host 192.168.' + oct + '.' + last + ' is in a /' + prefix + ' subnet. What is the network address? (last octet only)',
        answer: String(net), tolerance: 0, unit: '',
        steps: ['/' + prefix + ' leaves ' + hostBits + ' host bits → block size ' + block + ' in the last octet.',
          'Multiples of ' + block + ': ' + net + ' is the largest multiple ≤ ' + last + '.',
          'Network address: 192.168.' + oct + '.' + net + '.'],
        viz: { type: 'numberline', value: net, max: 255, mark: last },
        distractors: [ { value: String(net + block - 1), tag: 'broadcast-confusion',
          feedback: 'That is the BROADCAST address (last in the block). The network address is the FIRST address of the block.' } ] };
    }
    var usable = kind === 'usable';
    return { module: 'subnetting',
      question: 'How many ' + (usable ? 'usable host addresses' : 'total addresses') + ' are in a /' + prefix + ' subnet?',
      answer: String(usable ? total - 2 : total), tolerance: 0, unit: '',
      steps: ['/' + prefix + ' leaves ' + hostBits + ' host bits.', 'Total addresses: 2^' + hostBits + ' = ' + total + '.' +
        (usable ? ' Subtract 2 (network + broadcast) → ' + (total - 2) + ' usable.' : '')],
      viz: { type: 'bars', bars: [{ label: 'total', value: total }, { label: 'usable', value: total - 2 }] },
      distractors: [ { value: String(usable ? total : total - 2), tag: usable ? 'forgot-minus-2' : 'minus-2-unneeded',
        feedback: usable ? 'You forgot to subtract the network and broadcast addresses — usable hosts = total − 2.'
                         : 'Total addresses includes network and broadcast — do not subtract for the TOTAL count.' },
        { value: String(total / 2), tag: 'halved', feedback: 'Each extra host bit DOUBLES the count; do not halve — use 2^(host bits).' } ] };
  }

  function genLogic() {
    var A = Math.random() < 0.5 ? 0 : 1, B = Math.random() < 0.5 ? 0 : 1;
    var op = pick(['AND', 'OR', 'XOR', 'NAND', 'NOR']);
    var val = { AND: A & B, OR: A | B, XOR: A ^ B, NAND: 1 - (A & B), NOR: 1 - (A | B) }[op];
    var other = { AND: A | B, OR: A & B }[op];
    return { module: 'logic', question: 'What is ' + A + ' ' + op + ' ' + B + '? (answer 0 or 1)',
      answer: String(val), tolerance: 0, unit: '',
      steps: [op + ' rule: ' + opRule(op) + '.', 'So ' + A + ' ' + op + ' ' + B + ' = ' + val + '.'],
      viz: { type: 'truth', op: op, a: A, b: B },
      distractors: typeof other === 'number' && other !== val ? [ { value: String(other), tag: 'wrong-gate',
        feedback: 'That is the answer for a different gate. ' + op + ': ' + opRule(op) + '.' } ] : [] };
  }
  function opRule(op) {
    return { AND: 'output is 1 only when BOTH inputs are 1',
      OR: 'output is 1 when AT LEAST ONE input is 1',
      XOR: 'output is 1 when the inputs DIFFER',
      NAND: 'AND, then flipped — 0 only when both inputs are 1',
      NOR: 'OR, then flipped — 1 only when both inputs are 0' }[op];
  }

  function genStats() {
    var data = []; var n = rnd(5, 7);
    for (var i = 0; i < n; i++) data.push(rnd(2, 40));
    var kind = pick(['mean', 'median', 'range']);
    var sorted = data.slice().sort(function (a, b) { return a - b; });
    var sum = data.reduce(function (a, b) { return a + b; }, 0);
    if (kind === 'mean') {
      return { module: 'stats', question: 'Find the mean of: ' + data.join(', ') + ' (round to 2 decimals)',
        answer: String(round2(sum / n)), tolerance: 0.02, unit: '',
        steps: ['Sum: ' + data.join(' + ') + ' = ' + sum + '.', 'Count: ' + n + ' values.',
          'Mean = ' + sum + ' / ' + n + ' = ' + round2(sum / n) + '.'],
        viz: { type: 'bars', bars: data.map(function (v, i) { return { label: 'x' + (i + 1), value: v }; }) },
        distractors: [ { value: String(round2(sum / (n - 1))), tag: 'wrong-count',
          feedback: 'You divided by ' + (n - 1) + ' — the mean divides by the number of values, ' + n + '.' } ] };
    }
    if (kind === 'median') {
      /* Regenerate until the unsorted middle differs from the true median,
         so the classic unsorted-median trap is actually diagnosable. */
      var med = n % 2 ? sorted[(n - 1) / 2] : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
      var tries = 0;
      while (data[Math.floor(n / 2)] === med && tries < 25) {
        tries++;
        data = []; for (var q = 0; q < n; q++) data.push(rnd(2, 40));
        sorted = data.slice().sort(function (a, b) { return a - b; });
        med = n % 2 ? sorted[(n - 1) / 2] : (sorted[n / 2 - 1] + sorted[n / 2]) / 2;
      }
      return { module: 'stats', question: 'Find the median of: ' + data.join(', '),
        answer: String(med), tolerance: 0.001, unit: '',
        steps: ['Sort first: ' + sorted.join(', ') + '.', 'The median is the middle value: ' + med + '.'],
        viz: { type: 'numberline', value: med, max: sorted[n - 1] },
        distractors: [ { value: String(data[Math.floor(n / 2)]), tag: 'unsorted-median',
          feedback: 'You took the middle of the UNSORTED list. Always sort before picking the median.' } ] };
    }
    return { module: 'stats', question: 'Find the range of: ' + data.join(', '),
      answer: String(sorted[n - 1] - sorted[0]), tolerance: 0, unit: '',
      steps: ['Max = ' + sorted[n - 1] + ', min = ' + sorted[0] + '.',
        'Range = ' + sorted[n - 1] + ' − ' + sorted[0] + ' = ' + (sorted[n - 1] - sorted[0]) + '.'],
      viz: { type: 'bars', bars: data.map(function (v, i) { return { label: 'x' + (i + 1), value: v }; }) },
      distractors: [ { value: String(sorted[n - 1] + sorted[0]), tag: 'added-not-range',
        feedback: 'Range is a DIFFERENCE (max − min), not a sum.' } ] };
  }

  function genProbability() {
    var kind = pick(['simple', 'both', 'complement']);
    if (kind === 'simple') {
      var fav = rnd(1, 9), tot = fav + rnd(1, 12);
      return { module: 'probability',
        question: 'A bag holds ' + tot + ' marbles, ' + fav + ' of them red. What is P(red) as a decimal? (2 decimals)',
        answer: String(round2(fav / tot)), tolerance: 0.006, unit: '',
        steps: ['P = favorable / total = ' + fav + ' / ' + tot + '.', '= ' + round2(fav / tot) + ' as a decimal.'],
        viz: { type: 'numberline', value: round2(fav / tot), max: 1 },
        distractors: [ { value: String(round2(tot / fav)), tag: 'inverted-fraction',
          feedback: 'The fraction is upside down — probability is favorable ÷ total, and never exceeds 1.' },
          { value: String(round2(fav / (tot - fav))), tag: 'odds-not-prob',
          feedback: 'That is the ODDS (favorable vs unfavorable). Probability divides by the TOTAL.' } ] };
    }
    if (kind === 'both') {
      var p1 = pick([0.5, 0.2, 0.25, 0.1, 0.4]), p2 = pick([0.5, 0.3, 0.2, 0.6]);
      return { module: 'probability',
        question: 'Two INDEPENDENT events have probabilities ' + p1 + ' and ' + p2 + '. What is P(both occur)? (2 decimals)',
        answer: String(round2(p1 * p2)), tolerance: 0.006, unit: '',
        steps: ['Independent → MULTIPLY.', p1 + ' × ' + p2 + ' = ' + round2(p1 * p2) + '.'],
        viz: { type: 'numberline', value: round2(p1 * p2), max: 1 },
        distractors: [ { value: String(round2(p1 + p2)), tag: 'added-independent',
          feedback: 'You ADDED — addition is for "or" questions. "Both/and" with independence means multiply.' } ] };
    }
    var p = pick([0.15, 0.3, 0.65, 0.8, 0.42]);
    return { module: 'probability',
      question: 'P(rain tomorrow) = ' + p + '. What is P(NO rain)? (2 decimals)',
      answer: String(round2(1 - p)), tolerance: 0.006, unit: '',
      steps: ['Complements sum to 1.', 'P(no rain) = 1 − ' + p + ' = ' + round2(1 - p) + '.'],
      viz: { type: 'numberline', value: round2(1 - p), max: 1 },
      distractors: [ { value: String(p), tag: 'same-not-complement',
        feedback: 'That is P(rain) again. The complement is everything else: 1 − P.' } ] };
  }

  function genLinalg() {
    var kind = pick(['add', 'dot', 'scale', 'magnitude']);
    function nz() { var v = 0; while (v === 0) v = rnd(-6, 9); return v; }
    var a = [nz(), nz()], b = [nz(), nz()];
    /* Cross-added must differ from the true sum, else the trap is invisible. */
    if (kind === 'add') {
      var guard = 0;
      while (a[0] + b[1] === a[0] + b[0] && a[1] + b[0] === a[1] + b[1] && guard++ < 20) { b = [nz(), nz()]; }
    }
    if (kind === 'add') {
      return { module: 'linalg', question: 'Add the vectors (' + a + ') + (' + b + '). Answer as "x,y".',
        answer: (a[0] + b[0]) + ',' + (a[1] + b[1]), tolerance: 0, unit: '',
        steps: ['Add component-wise: x with x, y with y.',
          '(' + a[0] + '+' + b[0] + ', ' + a[1] + '+' + b[1] + ') = (' + (a[0] + b[0]) + ', ' + (a[1] + b[1]) + ').'],
        viz: { type: 'grid', a: a, b: b, result: [a[0] + b[0], a[1] + b[1]] },
        distractors: [ { value: (a[0] + b[1]) + ',' + (a[1] + b[0]), tag: 'cross-added',
          feedback: 'Components must stay in their lanes: x adds to x, y adds to y — never cross them.' } ] };
    }
    if (kind === 'dot') {
      return { module: 'linalg', question: 'Find the dot product of (' + a + ') · (' + b + ').',
        answer: String(a[0] * b[0] + a[1] * b[1]), tolerance: 0, unit: '',
        steps: ['Multiply matching components, then ADD the products.',
          a[0] + '×' + b[0] + ' + ' + a[1] + '×' + b[1] + ' = ' + (a[0] * b[0]) + ' + ' + (a[1] * b[1]) + ' = ' + (a[0] * b[0] + a[1] * b[1]) + '.'],
        viz: { type: 'grid', a: a, b: b },
        distractors: [ { value: (a[0] + b[0]) + ',' + (a[1] + b[1]), tag: 'vector-not-scalar',
          feedback: 'A dot product is a single NUMBER (scalar), not a vector. Multiply pairs, then add.' } ] };
    }
    if (kind === 'scale') {
      var k = rnd(2, 5);
      return { module: 'linalg', question: 'Multiply the vector (' + a + ') by the scalar ' + k + '. Answer as "x,y".',
        answer: (a[0] * k) + ',' + (a[1] * k), tolerance: 0, unit: '',
        steps: ['The scalar multiplies EVERY component.', '(' + a[0] + '×' + k + ', ' + a[1] + '×' + k + ') = (' + (a[0] * k) + ', ' + (a[1] * k) + ').'],
        viz: { type: 'grid', a: a, result: [a[0] * k, a[1] * k] },
        distractors: [ { value: (a[0] * k) + ',' + a[1], tag: 'partial-scale',
          feedback: 'Only the x component was scaled — a scalar multiplies EVERY component.' } ] };
    }
    var v = pick([[3, 4], [6, 8], [5, 12], [8, 15], [9, 12]]);
    var mag = Math.sqrt(v[0] * v[0] + v[1] * v[1]);
    return { module: 'linalg', question: 'Find the magnitude (length) of the vector (' + v + ').',
      answer: String(mag), tolerance: 0.01, unit: '',
      steps: ['Magnitude = √(x² + y²) — Pythagoras.', '√(' + v[0] + '² + ' + v[1] + '²) = √(' + (v[0] * v[0]) + ' + ' + (v[1] * v[1]) + ') = √' + (v[0] * v[0] + v[1] * v[1]) + ' = ' + mag + '.'],
      viz: { type: 'grid', a: v, result: v },
      distractors: [ { value: String(v[0] + v[1]), tag: 'added-components',
        feedback: 'Magnitude is not x + y. Square each component, add, then take the square root.' } ] };
  }

  var GENERATORS = { binary: genBinary, subnetting: genSubnetting, logic: genLogic,
                     stats: genStats, probability: genProbability, linalg: genLinalg };

  /* Safety net: a distractor whose value equals the correct answer can
     never be diagnosed (the student typed the right value). Strip those
     from every generated problem, whatever generator produced it. */
  function normVal(v) { return String(v).replace(/\s+/g, '').toLowerCase(); }
  (function wrapGenerators() {
    for (var key in GENERATORS) {
      (function (fn) {
        GENERATORS[key] = function () {
          var p = fn();
          if (p && p.distractors) {
            p.distractors = p.distractors.filter(function (d) {
              return normVal(d.value) !== normVal(p.answer);
            });
          }
          return p;
        };
      })(GENERATORS[key]);
    }
  })();

  /* ---------------- answer checking + misconception diagnosis ---------------- */

  function checkAnswer(problem, raw) {
    var given = String(raw || '').trim().replace(/\s+/g, '');
    var want = String(problem.answer).replace(/\s+/g, '');
    var tol = problem.tolerance || 0;
    var gNum = parseFloat(given), wNum = parseFloat(want);
    if (!isNaN(gNum) && !isNaN(wNum) && /,/.test(want) === false) {
      if (Math.abs(gNum - wNum) <= Math.max(tol, 0.0001)) return { ok: true };
    } else if (given.toLowerCase() === want.toLowerCase()) {
      return { ok: true };
    }
    var ds = problem.distractors || [];
    var dTol = Math.max(tol, 0.004);
    for (var i = 0; i < ds.length; i++) {
      var dv = String(ds[i].value).replace(/\s+/g, '');
      if (dv.toLowerCase() === want.toLowerCase()) continue; /* collides with answer */
      var dNum = parseFloat(dv);
      if ((!isNaN(gNum) && !isNaN(dNum) && Math.abs(gNum - dNum) <= dTol && /,/.test(dv) === false) ||
          given.toLowerCase() === dv.toLowerCase()) {
        return { ok: false, tag: ds[i].tag, feedback: ds[i].feedback };
      }
    }
    return { ok: false, tag: 'general', feedback: 'Not quite. Work the steps below, then try a fresh problem of the same kind.' };
  }

  /* ---------------- animated SVG solutions ---------------- */

  function svgWrap(inner, w, h) {
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" width="' + Math.min(w, 520) +
      '" role="img" aria-label="Animated solution diagram">' + inner + '</svg>';
  }
  function renderViz(viz) {
    if (!viz) return '';
    var accent = '#5eead4', gold = '#c9a227', ink = '#e6edf3', muted = '#8b949e';
    if (viz.type === 'placevalue') {
      var bits = viz.bits.split(''), n = bits.length, bw = 44, x0 = 20, s = '';
      for (var i = 0; i < n; i++) {
        var power = n - 1 - i, on = bits[i] === '1';
        s += '<g class="aix-viz-el" data-step="' + Math.min(i + 1, 2) + '">' +
          '<rect x="' + (x0 + i * (bw + 8)) + '" y="18" width="' + bw + '" height="46" rx="8" fill="' +
          (on ? 'rgba(94,234,212,.18)' : 'rgba(139,148,158,.10)') + '" stroke="' + (on ? accent : muted) + '"/>' +
          '<text x="' + (x0 + i * (bw + 8) + bw / 2) + '" y="48" fill="' + ink + '" font-size="20" font-family="monospace" text-anchor="middle">' + bits[i] + '</text>' +
          '<text x="' + (x0 + i * (bw + 8) + bw / 2) + '" y="84" fill="' + gold + '" font-size="12" font-family="monospace" text-anchor="middle">2^' + power + (on ? '=' + Math.pow(2, power) : '') + '</text></g>';
      }
      return svgWrap(s, x0 * 2 + n * (bw + 8), 100);
    }
    if (viz.type === 'numberline') {
      var max = viz.max || 10, w = 520, x = 30 + (viz.value / max) * (w - 60);
      var s2 = '<line x1="30" y1="45" x2="' + (w - 30) + '" y2="45" stroke="' + muted + '" stroke-width="2"/>' +
        '<g class="aix-viz-el" data-step="1"><circle cx="' + x + '" cy="45" r="8" fill="' + accent + '"/>' +
        '<text x="' + x + '" y="28" fill="' + ink + '" font-size="14" font-family="monospace" text-anchor="middle">' + viz.value + '</text></g>';
      if (typeof viz.mark === 'number') {
        var mx = 30 + (viz.mark / max) * (w - 60);
        s2 += '<g class="aix-viz-el" data-step="1"><circle cx="' + mx + '" cy="45" r="5" fill="' + gold + '"/>' +
          '<text x="' + mx + '" y="70" fill="' + gold + '" font-size="11" font-family="monospace" text-anchor="middle">host ' + viz.mark + '</text></g>';
      }
      s2 += '<text x="30" y="70" fill="' + muted + '" font-size="11" font-family="monospace">0</text>' +
            '<text x="' + (w - 30) + '" y="70" fill="' + muted + '" font-size="11" font-family="monospace" text-anchor="end">' + max + '</text>';
      return svgWrap(s2, w, 84);
    }
    if (viz.type === 'bars') {
      var bars = viz.bars, mx2 = 1, w3 = 520, bh = 22, s3 = '';
      for (var j = 0; j < bars.length; j++) mx2 = Math.max(mx2, bars[j].value);
      for (var k = 0; k < bars.length; k++) {
        var bw2 = (bars[k].value / mx2) * (w3 - 170);
        s3 += '<g class="aix-viz-el" data-step="' + (k % 2 + 1) + '">' +
          '<text x="86" y="' + (26 + k * (bh + 10)) + '" fill="' + muted + '" font-size="12" font-family="monospace" text-anchor="end">' + esc(bars[k].label) + '</text>' +
          '<rect x="94" y="' + (12 + k * (bh + 10)) + '" width="' + Math.max(bw2, 2) + '" height="' + bh + '" rx="4" fill="' + (k ? gold : accent) + '" opacity=".75"/>' +
          '<text x="' + (100 + bw2) + '" y="' + (28 + k * (bh + 10)) + '" fill="' + ink + '" font-size="12" font-family="monospace">' + bars[k].value + '</text></g>';
      }
      return svgWrap(s3, w3, 20 + bars.length * (bh + 10));
    }
    if (viz.type === 'grid') {
      var c = 130, sc = 11, s4 = '';
      for (var g = -10; g <= 10; g += 5) {
        s4 += '<line x1="' + (c + g * sc) + '" y1="10" x2="' + (c + g * sc) + '" y2="250" stroke="rgba(139,148,158,.18)"/>' +
              '<line x1="10" y1="' + (c - g * sc) + '" x2="250" y2="' + (c - g * sc) + '" stroke="rgba(139,148,158,.18)"/>';
      }
      s4 += '<line x1="10" y1="' + c + '" x2="250" y2="' + c + '" stroke="' + muted + '"/>' +
            '<line x1="' + c + '" y1="10" x2="' + c + '" y2="250" stroke="' + muted + '"/>';
      function vec(v, color, step) {
        return '<g class="aix-viz-el" data-step="' + step + '"><line x1="' + c + '" y1="' + c +
          '" x2="' + (c + v[0] * sc) + '" y2="' + (c - v[1] * sc) + '" stroke="' + color + '" stroke-width="3"/>' +
          '<circle cx="' + (c + v[0] * sc) + '" cy="' + (c - v[1] * sc) + '" r="4" fill="' + color + '"/>' +
          '<text x="' + (c + v[0] * sc + 6) + '" y="' + (c - v[1] * sc - 4) + '" fill="' + color +
          '" font-size="12" font-family="monospace">(' + v[0] + ',' + v[1] + ')</text></g>';
      }
      if (viz.a) s4 += vec(viz.a, accent, 1);
      if (viz.b) s4 += vec(viz.b, gold, 1);
      if (viz.result && viz.result !== viz.a) s4 += vec(viz.result, '#3fb950', 2);
      return svgWrap(s4, 260, 260);
    }
    if (viz.type === 'truth') {
      var rows = [[0, 0], [0, 1], [1, 0], [1, 1]], s5 = '';
      function evalOp(op, x, y) { return { AND: x & y, OR: x | y, XOR: x ^ y, NAND: 1 - (x & y), NOR: 1 - (x | y) }[op]; }
      s5 += '<text x="20" y="24" fill="' + muted + '" font-size="13" font-family="monospace">A   B   ' + viz.op + '</text>';
      for (var r = 0; r < 4; r++) {
        var hl = rows[r][0] === viz.a && rows[r][1] === viz.b;
        s5 += '<g class="aix-viz-el" data-step="' + (hl ? 2 : 1) + '">' +
          '<text x="20" y="' + (52 + r * 26) + '" fill="' + (hl ? accent : ink) + '" font-size="14" font-family="monospace">' +
          rows[r][0] + '   ' + rows[r][1] + '    ' + evalOp(viz.op, rows[r][0], rows[r][1]) + (hl ? '  ← your row' : '') + '</text></g>';
      }
      return svgWrap(s5, 300, 160);
    }
    return '';
  }

  /* ---------------- problem sourcing: AI first, local always ---------------- */

  function aiProblem(moduleId) {
    if (!window.AIClient) return Promise.reject(new Error('no-client'));
    return window.AIClient.route('math', [{ role: 'user', content:
      'Create ONE practice problem for the math topic "' + moduleId + '" for an IT certification student. ' +
      'Reply with ONLY a JSON object (no markdown fences) with keys: question (string), answer (string), ' +
      'steps (array of 2-4 short strings), hint (string). The answer must be a plain number or short string.' }],
      { maxTokens: 500 }).then(function (res) {
        var m = /\{[\s\S]*\}/.exec(res.reply || '');
        if (!m) throw new Error('no-json');
        var p = JSON.parse(m[0]);
        if (!p.question || typeof p.answer === 'undefined' || !p.steps) throw new Error('bad-shape');
        return { module: moduleId, question: String(p.question), answer: String(p.answer),
                 tolerance: 0.02, steps: p.steps.map(String), viz: null, distractors: [], remote: true };
      });
  }

  function getProblem(moduleId) {
    return aiProblem(moduleId).catch(function () {
      return GENERATORS[moduleId]();
    });
  }

  /* ---------------- practice widget ---------------- */

  function widgetHTML(moduleId) {
    return '<div class="aix-math" data-aix-math="' + esc(moduleId) + '">' +
      '<h4>🧮 Adaptive practice — ' + esc(moduleId) + '</h4>' +
      '<p class="aix-sub">Problems tuned to your level. Wrong answers get diagnosed, not just marked.</p>' +
      '<div class="aix-meter"><i style="width:0%"></i></div>' +
      '<p class="aix-q">Loading a problem…</p>' +
      '<div class="aix-viz"></div>' +
      '<div class="aix-row"><input type="text" placeholder="Your answer" aria-label="Your answer">' +
      '<button class="btn primary aix-check">Check</button>' +
      '<button class="btn small ghost aix-new">New problem</button>' +
      '<button class="btn small ghost aix-show" style="display:none">Show animated solution</button></div>' +
      '<div class="aix-fb" role="status"></div><ol class="aix-steps"></ol></div>';
  }

  function mountWidget(host, moduleId) {
    if (!host || host.querySelector('[data-aix-math]')) return;
    var wrap = document.createElement('div');
    wrap.innerHTML = widgetHTML(moduleId);
    host.appendChild(wrap.firstChild);
    var root = host.querySelector('[data-aix-math]');
    var current = null, solved = false;

    function paintMeter() {
      var s = loadState();
      root.querySelector('.aix-meter i').style.width =
        Math.round((s.modules[moduleId].mastery || 0) * 100) + '%';
    }
    function load() {
      solved = false;
      root.querySelector('.aix-fb').textContent = '';
      root.querySelector('.aix-fb').className = 'aix-fb';
      root.querySelector('.aix-steps').innerHTML = '';
      root.querySelector('.aix-viz').innerHTML = '';
      root.querySelector('.aix-show').style.display = 'none';
      root.querySelector('.aix-q').textContent = 'Loading a problem…';
      paintMeter();
      getProblem(moduleId).then(function (p) {
        current = p;
        root.querySelector('.aix-q').textContent = p.question;
        root.querySelector('input').value = '';
      });
    }
    function showSolution(animate) {
      if (!current) return;
      var vizHost = root.querySelector('.aix-viz');
      vizHost.innerHTML = renderViz(current.viz);
      var stepsOl = root.querySelector('.aix-steps');
      stepsOl.innerHTML = current.steps.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') +
        '<li><strong>Answer: ' + esc(current.answer) + '</strong></li>';
      var lis = stepsOl.querySelectorAll('li');
      var els = vizHost.querySelectorAll('.aix-viz-el');
      var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      function reveal(i) {
        if (i < lis.length) lis[i].classList.add('on');
        for (var j = 0; j < els.length; j++) {
          if (parseInt(els[j].getAttribute('data-step'), 10) <= i + 1) els[j].classList.add('on');
        }
      }
      if (!animate || reduce) {
        for (var i = 0; i < lis.length; i++) reveal(i);
      } else {
        var k = 0;
        reveal(0);
        var timer = setInterval(function () {
          k++; reveal(k);
          if (k >= lis.length) clearInterval(timer);
        }, 900);
      }
    }
    root.querySelector('.aix-check').addEventListener('click', function () {
      if (!current || solved) return;
      var val = root.querySelector('input').value;
      var res = checkAnswer(current, val);
      var fb = root.querySelector('.aix-fb');
      var st = recordResult(moduleId, res.ok, res.ok ? null : res.tag);
      paintMeter();
      if (res.ok) {
        solved = true;
        fb.className = 'aix-fb good';
        fb.textContent = '✅ Correct! Mastery in ' + moduleId + ' is now ' +
          Math.round(st.modules[moduleId].mastery * 100) + '%.';
        showSolution(true);
      } else {
        fb.className = 'aix-fb bad';
        fb.textContent = '❌ ' + res.feedback;
        root.querySelector('.aix-show').style.display = '';
        if (st.modules[moduleId].streakWrong >= 3) {
          fb.textContent += ' Three misses in a row — watch the animated solution, then try a fresh one.';
          showSolution(true);
        }
      }
    });
    root.querySelector('.aix-new').addEventListener('click', load);
    root.querySelector('.aix-show').addEventListener('click', function () { showSolution(true); });
    root.querySelector('input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') root.querySelector('.aix-check').click();
    });
    load();
  }

  /* ---------------- mounting into Learn ---------------- */

  var mathCache = null;
  function loadMath() {
    if (mathCache) return Promise.resolve(mathCache);
    return fetch('../_shell/math.json').then(function (r) { return r.json(); })
      .then(function (d) { mathCache = d; return d; })
      .catch(function () { return null; });
  }

  function tryitModule(slideText) {
    if (!mathCache) return null;
    var modules = mathCache.modules || [];
    for (var i = 0; i < modules.length; i++) {
      var lectures = modules[i].lectures || [];
      for (var j = 0; j < lectures.length; j++) {
        var slides = lectures[j].slides || [];
        for (var k = 0; k < slides.length; k++) {
          if (slides[k].kind === 'tryit' && slides[k].text === slideText) return modules[i].id;
        }
      }
    }
    return null;
  }

  var lastSlideKey = '';
  function scan() {
    var stage = $('learnStage');
    if (!stage) return;
    var tryit = stage.querySelector('.learn-tryit');
    if (tryit) {
      var key = 'tryit:' + tryit.textContent.slice(0, 60);
      if (key !== lastSlideKey) {
        lastSlideKey = key;
        loadMath().then(function () {
          var mod = tryitModule(tryit.textContent) || frontier(loadState());
          var slide = tryit.closest ? tryit.closest('.learn-slide') : stage;
          mountWidget(slide, mod);
        });
      }
      return;
    }
    /* Learn overview: offer the practice launcher once. */
    var body = $('learnBody');
    if (body && !body.querySelector('.learn-deck') && !body.querySelector('[data-aix-launch]') &&
        !body.querySelector('[data-aix-math]')) {
      var key2 = 'overview';
      if (lastSlideKey !== key2) {
        lastSlideKey = key2;
        fetch('content.json').then(function (r) { return r.json(); }).then(function (c) {
          if (!c || !(c.math && c.math.length)) return;
          if (body.querySelector('[data-aix-launch]')) return;
          var s = loadState();
          var f = frontier(s);
          var card = document.createElement('div');
          card.className = 'aix-math aix-launch';
          card.setAttribute('data-aix-launch', '1');
          card.innerHTML = '<h4>🧮 Adaptive Math Practice</h4>' +
            '<p class="aix-sub">ALEKS-style: problems at the edge of your ability, diagnosed feedback, ' +
            'animated solutions. Your current frontier: <strong>' + esc(f) + '</strong> (' +
            Math.round((s.modules[f].mastery || 0) * 100) + '% mastered). Tap to train.</p>';
          card.addEventListener('click', function () {
            card.removeAttribute('data-aix-launch');
            card.classList.remove('aix-launch');
            mountWidget(card.parentNode, f);
            card.remove();
          });
          body.insertBefore(card, body.firstChild);
        }).catch(function () {});
      }
    }
  }

  function init() {
    injectCSS();
    var body = $('learnBody');
    if (!body) { setTimeout(init, 400); return; }
    if (window.MutationObserver) {
      new MutationObserver(function () { scan(); }).observe(body, { childList: true, subtree: true });
    }
    document.addEventListener('ilb:view', function (e) {
      if (e && e.detail === 'learn') setTimeout(scan, 120);
    });
    scan();
  }

  window.AIMath = {
    state: loadState,
    frontier: function () { return frontier(loadState()); },
    generators: GENERATORS,
    checkAnswer: checkAnswer,
    mount: mountWidget,
    recordResult: recordResult
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
