#!/usr/bin/env node
/* Headless smoke test of app.js view functions with DOM stubs. */
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const ROOT = path.join(process.env.HOME, 'workspace/cbt-individual/tl-infra-assessment-prep');

function makeEl(tag) {
  const el = {
    tagName: (tag || 'div').toUpperCase(),
    _innerHTML: '',
    set innerHTML(v) { this._innerHTML = String(v); },
    get innerHTML() { return this._innerHTML; },
    textContent: '', value: '', disabled: false, checked: false,
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    dataset: {}, style: {}, children: [],
    addEventListener() {}, removeEventListener() {},
    appendChild(c) { this.children.push(c); return c; },
    setAttribute() {}, getAttribute() { return null; },
    focus() {}, click() {}, scrollIntoView() {},
    getContext() { return null; },
    onclick: null, onchange: null,
  };
  el.querySelector = (sel) => {
    const html = el._innerHTML || '';
    const m = sel.match(/^#([\w-]+)$/);
    if (m && html.includes('id="' + m[1] + '"')) return makeEl('div');
    const c = sel.match(/^\.([\w-]+)$/);
    if (c && new RegExp('class="[^"]*\\b' + c[1] + '\\b').test(html)) return makeEl('div');
    return null;
  };
  el.querySelectorAll = () => [];
  return el;
}

const content = JSON.parse(fs.readFileSync(path.join(ROOT, 'content.json'), 'utf8'));
const drills = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/drill-data.json'), 'utf8'));

const store = {};
const sandbox = {
  console, setTimeout: (fn) => 0, clearTimeout() {}, setInterval: () => 0, clearInterval() {},
  Math, JSON, Date, RegExp, Error, Object, Array, String, Number, Boolean, Promise,
  encodeURIComponent, decodeURIComponent, parseInt, parseFloat, isNaN,
  localStorage: {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
  },
  location: { hash: '#/dashboard', href: 'http://localhost/', reload() {} },
  navigator: { onLine: true, serviceWorker: { register: () => Promise.resolve({}) }, userAgent: 'node-smoke' },
  fetch: (url) => {
    const body = String(url).includes('drill-data') ? drills : content;
    return Promise.resolve({ ok: true, json: () => Promise.resolve(body), text: () => Promise.resolve('') });
  },
  AbortController: function () { this.signal = {}; this.abort = () => {}; },
  confirm: () => true, alert() {},
  requestAnimationFrame: () => 0,
  addEventListener() {}, removeEventListener() {},
  scrollTo() {},
};
const els = {};
function getEl(id) { if (!els[id]) els[id] = makeEl('div'); return els[id]; }
sandbox.document = {
  getElementById: (id) => getEl(id),
  querySelector: (sel) => { const m = /#([A-Za-z0-9_-]+)/.exec(sel); return m ? getEl(m[1]) : makeEl('div'); },
  querySelectorAll: () => [],
  createElement: (t) => makeEl(t),
  addEventListener: (ev, fn) => { if (ev === 'DOMContentLoaded') sandbox.__domReady = fn; },
  removeEventListener() {},
  body: makeEl('body'), documentElement: makeEl('html'),
  visibilityState: 'visible', title: '',
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
sandbox.self = sandbox;

const code = fs.readFileSync(path.join(ROOT, process.env.APPJS || 'app.js'), 'utf8');
vm.createContext(sandbox);
try {
  vm.runInContext(code, sandbox, { filename: process.env.APPJS || 'app.js' });
} catch (e) {
  console.log('LOAD THROW:', e.message);
  process.exit(1);
}
// fire DOMContentLoaded
sandbox.__domReady();

function check(name, fn) {
  try {
    const r = fn();
    if (typeof r !== 'string') { console.log('FAIL', name, '- not a string'); return false; }
    console.log('OK  ', name, '(' + r.length + ' chars)');
    return true;
  } catch (e) {
    console.log('THROW', name, '-', e.message);
    return false;
  }
}

setTimeout(() => {
  const V = sandbox; // view fns are global in vm context
  let pass = 0, fail = 0;
  const t = (n, f) => (check(n, f) ? pass++ : fail++);
  const C = V.Content;
  const dom0 = C.domains[0].id;
  const lesson0 = C.lessons[0]._id;
  const scn0 = C.domains.flatMap(d => d.scenarios || [])[0].id;
  const lab0 = C.labs[0].id;

  t('viewDashboard', () => V.viewDashboard());
  t('viewLearn', () => V.viewLearn());
  t('viewModule(valid)', () => V.viewModule(dom0));
  t('viewModule(bad-id)', () => V.viewModule('nope'));
  t('viewLesson(valid)', () => V.viewLesson(lesson0));
  t('viewLesson(bad-id)', () => V.viewLesson('nope'));
  t('viewScenario(valid)', () => V.viewScenario(scn0));
  t('viewScenario(bad-id)', () => V.viewScenario('nope'));
  t('viewLab(valid)', () => V.viewLab(lab0));
  t('viewLab(bad-id)', () => V.viewLab('nope'));
  t('viewDrills(speed)', () => V.viewDrills('speed', ''));
  t('viewDrills(blind)', () => V.viewDrills('blind', ''));
  t('viewDrills(sequences)', () => V.viewDrills('sequences', ''));
  t('viewDrills(errors)', () => V.viewDrills('errors', ''));
  t('viewDrills(sprint)', () => V.viewDrills('sprint', ''));
  t('viewDrills(daily)', () => V.viewDrills('daily', ''));
  t('viewDrills(speed?cmd=)', () => V.viewDrills('speed', 'cmd=' + encodeURIComponent(C.drillData.commands[0].id)));
  t('viewTerminal', () => V.viewTerminal());
  t('viewMockLanding', () => V.viewMockLanding());
  t('viewReference', () => V.viewReference());

  // route-level: parseRoute + renderRoute for every hash
  const routes = ['#/dashboard', '#/learn', '#/module/' + dom0, '#/lesson/' + lesson0,
    '#/scenario/' + scn0, '#/lab/' + lab0, '#/drills/speed', '#/drills/daily',
    '#/drills/speed?cmd=' + C.drillData.commands[0].id, '#/terminal', '#/mock', '#/reference', '#/bogus'];
  for (const h of routes) {
    sandbox.location.hash = h;
    try { V.renderRoute(); console.log('OK   renderRoute', h); pass++; }
    catch (e) { console.log('THROW renderRoute', h, '-', e.message); fail++; }
  }

  // mock run
  try { V.initMockLanding(); console.log('OK   initMockLanding'); pass++; }
  catch (e) { console.log('THROW initMockLanding -', e.message); fail++; }
  try { V.startMock(); V.renderMockItem(); console.log('OK   startMock+renderMockItem'); pass++; }
  catch (e) { console.log('THROW mock run -', e.message); fail++; }
  // drill inits with real body html
  try {
    const body = V.document.createElement('div');
    V.initDrillsView('speed', 'cmd=bogus-id');
    V.initDrillsView('daily', '');
    V.initDrillsView('sequences', '');
    V.initDrillsView('errors', '');
    V.initDrillsView('sprint', '');
    console.log('OK   initDrillsView all modes'); pass++;
  } catch (e) { console.log('THROW initDrillsView -', e.message); fail++; }
  try { V.initLabView(lab0); console.log('OK   initLabView'); pass++; }
  catch (e) { console.log('THROW initLabView -', e.message); fail++; }
  try { V.initScenarioView(scn0); console.log('OK   initScenarioView'); pass++; }
  catch (e) { console.log('THROW initScenarioView -', e.message); fail++; }
  console.log(`\nPASS ${pass} FAIL ${fail}`);
  process.exit(fail ? 1 : 0);
}, 500);
