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

async function testSims() {
  console.log('simulations.js');
  const win = makeWindow();
  win.BOOTCAMP_PAGE = { slug: 'smoke', hubUrl: '../../index.html', title: 'Smoke Test' };
  installGlobals(win, { slug: 'smoke', simulations: [] });
  loadEngine('simulations.js');
  await tick();
  const E = win.__simsEngine;
  check('ENGINE_TEST seam exposed', !!E);
  if (!E) return;

  let r = E.checkOrdering(['a', 'b', 'c'], [2, 0, 1], [2, 0, 1]);
  check('ordering exact match is correct', r.correct === true && r.score === 1, JSON.stringify(r));
  r = E.checkOrdering(['a', 'b', 'c'], [0, 1, 2], [2, 0, 1]);
  check('ordering wrong order is incorrect', r.correct === false && r.score === 0, JSON.stringify(r));
  r = E.checkOrdering(['a', 'b', 'c'], [2, 1, 0], [2, 0, 1]);
  check('ordering partial scores 1/3', r.correct === false && Math.abs(r.score - 1 / 3) < 1e-9, r.score);
  r = E.checkOrdering(['a', 'b'], [1], [1, 0]);
  check('ordering short answer is incorrect', r.correct === false && r.score === 0.5, JSON.stringify(r));

  const sb = E.scoreBranching([{ points: 2 }, { points: 0 }, { points: 3 }]);
  check('branching scorer sums points', sb.total === 5 && sb.steps === 3, JSON.stringify(sb));
  check('branching scorer tolerates numbers', E.scoreBranching([2, 3]).total === 5);
  const tree = [
    { id: 's1', choices: [{ label: 'a', next: 's2', points: 2 }, { label: 'b', next: 'END', points: 5 }] },
    { id: 's2', choices: [{ label: 'c', next: 'END', points: 4 }] },
  ];
  check('branching max-points DFS', E.maxBranchingPoints(tree) === 6, E.maxBranchingPoints(tree));

  const issues = [{ line: 3, description: 'x', fix: 'y' }, { line: 7, description: 'z', fix: 'w' }];
  let c = E.checkConfigCheck([3, 7], issues, 2);
  check('config-check exact is correct', c.correct === true && c.score === 1, JSON.stringify(c));
  c = E.checkConfigCheck([3], issues, 2);
  check('config-check partial: 1 hit, 1 missed', c.correct === false && c.hits === 1 && c.missed.length === 1, JSON.stringify(c));
  c = E.checkConfigCheck([3, 7, 9], issues, 2);
  check('config-check false positive penalized', c.correct === false && c.falsePositives === 1 && c.score < 1, JSON.stringify(c));
  c = E.checkConfigCheck([], issues, 2);
  check('config-check empty selection scores 0', c.correct === false && c.score === 0, JSON.stringify(c));
}

async function testConsoles() {
  console.log('consoles.js');
  const win = makeWindow();
  win.BOOTCAMP_PAGE = { slug: 'smoke', hubUrl: '../../index.html', title: 'Smoke Test' };
  installGlobals(win, { slug: 'smoke', consoleSims: [] });
  loadEngine('consoles.js');
  await tick();
  check('ConsoleView exposed', !!win.ConsoleView && typeof win.ConsoleView.render === 'function');
  const E = win.__consoleEngine;
  check('ENGINE_TEST seam exposed', !!E);
  if (!E) return;

  const expected = ['aws-vpc', 'aws-iam', 'azure-portal', 'k8s-dashboard', 'firewall',
    'switch-cli', 'linux-desktop', 'sql-studio', 'git-host', 'cicd-pipeline',
    'siem-dashboard', 'ticketing', 'code-editor', 'db-admin', 'generic-web'];
  const missing = expected.filter(t => E.consoles.indexOf(t) < 0);
  check('all 15 console types registered', missing.length === 0, missing.join(','));

  check('default match: action + subset params',
    E.match({ action: 'create-vpc', params: { cidr: '10.0.0.0/16' } },
      'create-vpc', { name: 'prod', cidr: '10.0.0.0/16', extra: 1 }) === true);
  check('default match rejects wrong action',
    E.match({ action: 'create-vpc', params: {} }, 'delete-vpc', {}) === false);
  check('default match rejects param mismatch',
    E.match({ action: 'create-vpc', params: { cidr: '10.0.0.0/16' } },
      'create-vpc', { cidr: '10.1.0.0/16' }) === false);
  check('default match: numeric subset',
    E.match({ action: 'scale', params: { replicas: 3 } }, 'scale', { deployment: 'web', replicas: 3 }) === true);

  check('coerce turns numeric strings into numbers',
    E.coerce('80') === 80 && E.coerce('3.5') === 3.5 && E.coerce('us-east-1a') === 'us-east-1a');
  check('subsetMatch handles nested objects',
    E.subsetMatch({ a: 1, b: { c: 2 } }, { a: 1, b: { c: 2, d: 3 }, e: 4 }) === true);
}

async function testMissions() {
  console.log('missions.js');
  const win = makeWindow();
  win.BOOTCAMP_PAGE = { slug: 'smoke', hubUrl: '../../index.html', title: 'Smoke Test' };
  installGlobals(win, { slug: 'smoke', terminalMissions: [] });
  loadEngine('missions.js');
  await tick();
  check('MissionsView exposed', !!win.MissionsView && typeof win.MissionsView.render === 'function');
  const E = win.__missionsEngine;
  check('ENGINE_TEST seam exposed', !!E);
  if (!E) return;
  check('check contract: regex + substring',
    E.checkCommand('^kubectl\\s+get\\s+pods', 'Running', 'kubectl get pods -n prod', 'web-1  Running') === true);
  check('check contract rejects wrong command',
    E.checkCommand('^kubectl\\s+get\\s+pods', 'Running', 'kubectl describe pod web-1', 'Running') === false);
  check('check contract rejects missing output',
    E.checkCommand('^kubectl\\s+get\\s+pods', 'Running', 'kubectl get pods', 'No resources found') === false);
  check('check contract tolerates bad regex',
    E.checkCommand('([invalid', 'x', 'cmd', 'x') === false);
}

async function testProgressIntel() {
  console.log('bootcamp.js progress intelligence');
  const win = makeWindow();
  win.BOOTCAMP_PAGE = { slug: 'smoke', hubUrl: '../../index.html', title: 'Smoke Test' };
  const ext = Object.assign({}, SAMPLE, {
    labs: [
      { id: 'lab-1', title: 'Lab One', domain_id: 'd1', objective: 'o', steps: [], checks: [], success_message: 'ok' },
      { id: 'lab-2', title: 'Lab Two', domain_id: 'd2', objective: 'o', steps: [], checks: [], success_message: 'ok' },
    ],
    simulations: [
      { id: 'sim-1', title: 'Sim One', kind: 'ordering', domain_id: 'd1', points: 10 },
    ],
    terminalMissions: [
      { id: 'mis-1', title: 'Mission One', domain_id: 'd2', checks: [] },
    ],
  });
  installGlobals(win, ext);
  loadEngine('bootcamp.js');
  await tick(); await tick();
  const E = win.__bootcampEngine;
  check('progress seam exposed', !!E && !!E.domainMastery && !!E.nextRecommendations);
  if (!E || !E.domainMastery) return;

  const dm = E.domainMastery();
  check('domainMastery covers 3 domains', Object.keys(dm).length === 3, Object.keys(dm).join(','));
  check('domainMastery starts at 0%', dm.d1.pct === 0 && dm.d1.total === 3);
  E.recordResult(E.SCEN[0].id, true);
  const dm2 = E.domainMastery();
  check('domainMastery reflects drill clears', dm2.d1.pct === 33 && dm2.d2.pct === 0, JSON.stringify(dm2.d1));

  check('window.ILBProgress exposed', !!win.ILBProgress);
  const recs = E.nextRecommendations(2);
  check('recommendations target weakest domain first', recs.length === 2 && recs[0].domain_id === 'd2',
    JSON.stringify(recs.map(r => r.kind + ':' + r.id)));
  check('recommendation shape', recs.every(r => r.kind && r.id && r.title && r.domain_id && r.reason),
    JSON.stringify(recs[0]));
  check('kind variety in recommendations',
    new Set(recs.map(r => r.kind)).size === 2, recs.map(r => r.kind).join(','));

  // mark everything in d2 done -> recommendations should move to d3 (no items) then d1
  win.localStorage.setItem('ilb-bootcamp-smoke-labs-v1', JSON.stringify({ 'lab-2': true }));
  win.localStorage.setItem('ilb-bootcamp-smoke-missions-v1', JSON.stringify({ 'mis-1': true }));
  const recs2 = E.nextRecommendations(5);
  check('done items are skipped', recs2.every(r => r.id !== 'lab-2' && r.id !== 'mis-1'),
    JSON.stringify(recs2.map(r => r.id)));
  check('recommendations fall through to next-weakest domain',
    recs2.length > 0 && recs2[0].domain_id === 'd1', JSON.stringify(recs2.map(r => r.id)));

  const recs3 = E.nextRecommendations(0); // limit 0 -> default 3
  check('limit 0 falls back to default', recs3.length <= 3, recs3.length);
}

(async () => {
  try {
    await testBootcamp();
    await testChat();
    await testSims();
    await testConsoles();
    await testMissions();
    await testProgressIntel();
  } catch (e) {
    failures++;
    console.log('  FAIL uncaught exception: ' + (e && e.stack || e));
  }
  console.log(failures ? `\n${failures} FAILURE(S)` : '\nALL PASS');
  process.exit(failures ? 1 : 0);
})();
