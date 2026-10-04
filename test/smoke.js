#!/usr/bin/env node
/* Headless smoke test for engine/bootcamp.js and engine/chat.js.
 * Runs the real engine sources in Node with stub DOM/storage/fetch and
 * exercises the pure logic via the window.ENGINE_TEST seam.
 * Usage: node test/smoke.js   (exit 0 = all pass)
 */
'use strict';
const fs = require('fs');
const path = require('path');
const ENG = path.join(__dirname, '..', 'engine');

let failures = 0;
function check(name, cond, extra) {
  if (cond) { console.log('  ok  ' + name); }
  else { failures++; console.log('  FAIL ' + name + (extra ? ' :: ' + extra : '')); }
}

/* ---------------- stub browser ---------------- */
function makeEl() {
  return {
    style: {}, dataset: {}, disabled: false, value: '',
    textContent: '', innerHTML: '',
    classList: { add() {}, remove() {}, toggle() {} },
    addEventListener() {}, removeEventListener() {},
    setAttribute() {}, getAttribute() { return null; },
    querySelector() { return null; }, querySelectorAll() { return []; },
    appendChild(c) { return c; }, focus() {}, click() {},
    scrollIntoView() {},
  };
}
function makeWindow() {
  const store = {};
  const win = {
    ENGINE_TEST: true,
    scrollTo() {},
    localStorage: {
      getItem: k => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: k => { delete store[k]; },
    },
  };
  return win;
}
function installGlobals(win, fetchJson) {
  global.window = win;
  global.localStorage = win.localStorage;
  global.document = {
    readyState: 'complete',
    title: '',
    getElementById: () => makeEl(),
    querySelectorAll: () => [],
    querySelector: () => null,
    createElement: () => makeEl(),
    addEventListener() {},
  };
  global.fetch = async () => ({ ok: true, json: async () => fetchJson });
}
function loadEngine(file) {
  const src = fs.readFileSync(path.join(ENG, file), 'utf8');
  // eslint-disable-next-line no-eval
  eval.call(global, src);
}
const tick = () => new Promise(r => setTimeout(r, 10));

/* ---------------- sample content ---------------- */
function scen(id, domain) {
  return {
    id, title: 'Scenario ' + id, situation: 'Situation for ' + id + ' with enough detail.',
    prompt: 'What is the best next action?',
    evidence: [['term.txt', 'output line 1\noutput line 2']],
    choices: ['Option A', 'Option B', 'Option C', 'Option D'],
    answer: 1, why: 'Because B is correct.',
    hint: 'Think about B.', objectives: ['Objective one'], mins: 5,
  };
}
const SAMPLE = {
  slug: 'smoke', title: 'Smoke Test', tagline: 'tag', disclaimer: 'disc',
  vendor: { name: 'Smoke Vendor', certs: 'SMK-001' },
  simulation: { items: 6, minutes: 60, evidence_cost_mins: 0 },
  domains: [
    { id: 'd1', name: 'Domain One', scenarios: [scen('a', 1), scen('b', 1), scen('c', 1)] },
    { id: 'd2', name: 'Domain Two', scenarios: [scen('d', 2), scen('e', 2), scen('f', 2)] },
    { id: 'd3', name: 'Domain Three', scenarios: [scen('g', 3), scen('h', 3), scen('i', 3)] },
  ],
  behavioral: [{ prompt: 'p', framework: 'STAR', points: ['x'], pitfalls: ['y'] }],
  chat: {
    persona: 'A rigorous coach.',
    topics: [
      { id: 'd1', name: 'Domain One',
        key_points: ['mutable default arguments are evaluated once at def time',
                     'use None as the default and create the list inside'],
        followups: ['What breaks with a dict default?'] },
    ],
  },
};

async function testBootcamp() {
  console.log('bootcamp.js');
  const win = makeWindow();
  win.BOOTCAMP_PAGE = { slug: 'smoke', hubUrl: '../../index.html', title: 'Smoke Test' };
  installGlobals(win, SAMPLE);
  loadEngine('bootcamp.js');
  await tick(); await tick(); // let boot()'s fetch chain settle
  const E = win.__bootcampEngine;
  check('ENGINE_TEST seam exposed', !!E);
  if (!E) return;

  check('ingest flattens 9 scenarios', E.SCEN.length === 9, E.SCEN.length);
  check('3 domains in order', JSON.stringify(E.DOMAINS) === JSON.stringify(['Domain One', 'Domain Two', 'Domain Three']));
  check('SIM config honored', E.SIM.items === 6 && E.SIM.minutes === 60, JSON.stringify(E.SIM));

  const q = E.buildQueue();
  check('queue covers all scenarios', q.length === 9, q.length);

  const first = E.SCEN[0].id;
  check('not cleared initially', !E.cleared(first));
  E.recordResult(first, false);
  check('wrong answer: attempted, not cleared', !E.cleared(first));
  E.recordResult(first, true);
  check('right answer clears', E.cleared(first));
  check('mastery 1/3 after one clear', Math.abs(E.mastery('Domain One') - 1 / 3) < 1e-9, E.mastery('Domain One'));
  check('overallPct rounds', E.overallPct() === Math.round(100 / 9), E.overallPct());

  const weak = E.weakestFirst();
  check('weakest domain is not the cleared one', weak[0] !== 'Domain One', weak[0]);
  // clearing all of Domain One should push it last
  E.recordResult(E.SCEN[1].id, true); E.recordResult(E.SCEN[2].id, true);
  check('fully cleared domain sorts last', E.weakestFirst()[2] === 'Domain One');

  const sim = E.pickSimItems();
  check('sim lineup within budget', sim.length > 0 && sim.length <= E.SIM.items, sim.length);
  check('sim lineup unique', new Set(sim).size === sim.length);

  check('verdict 90 ASSESSMENT-READY', E.verdict(90)[0] === 'ASSESSMENT-READY');
  check('verdict 75 NEARLY READY', E.verdict(75)[0] === 'NEARLY READY');
  check('verdict 55 DEVELOPING', E.verdict(55)[0] === 'DEVELOPING');
  check('verdict 10 FOUNDATIONS FIRST', E.verdict(10)[0] === 'FOUNDATIONS FIRST');

  // localStorage namespaced per slug
  check('progress namespaced', !!win.localStorage.getItem('ilb-bootcamp-smoke-v1'));
}

async function testChat() {
  console.log('chat.js');
  const win = makeWindow();
  win.CHAT_PAGE = { slug: 'smoke', bootcampUrl: '../index.html', hubUrl: '../../../index.html', title: 'Smoke Test' };
  installGlobals(win, SAMPLE);
  loadEngine('chat.js');
  await tick(); await tick();
  const E = win.__chatEngine;
  check('ENGINE_TEST seam exposed', !!E);
  if (!E) return;

  const cues = E.keywordsFor('mutable default arguments are evaluated once at def time');
  check('keyword derivation keeps significant words',
    cues.includes('mutable') && cues.includes('default') && cues.includes('evaluated'), cues.join(','));
  check('keyword derivation drops stopwords/short words',
    !cues.includes('are') && !cues.includes('at') && !cues.includes('of'), cues.join(','));

  const kp = [{ label: 'use None as the default and create the list inside' }];
  const strong = E.analyze('I would use None as the default and create the list inside the function body', kp);
  check('full-coverage answer is strong', strong[0].verdict === 'strong', JSON.stringify(strong[0]));
  const partial = E.analyze('I would create the list somewhere', kp);
  check('one-cue answer is partial', partial[0].verdict === 'partial', JSON.stringify(partial[0]));
  const missed = E.analyze('I have absolutely no idea what to do here', kp);
  check('no-cue answer is missed', missed[0].verdict === 'missed', JSON.stringify(missed[0]));

  const fallback = E.topicPrompt({ name: 'Domain One' });
  check('topicPrompt fallback generated', /Domain One/.test(fallback) && /Walk me through/.test(fallback));
}

(async () => {
  try {
    await testBootcamp();
    await testChat();
  } catch (e) {
    failures++;
    console.log('  FAIL uncaught exception: ' + (e && e.stack || e));
  }
  console.log(failures ? `\n${failures} FAILURE(S)` : '\nALL PASS');
  process.exit(failures ? 1 : 0);
})();
