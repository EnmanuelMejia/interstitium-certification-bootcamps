#!/usr/bin/env python3
"""Final global verification for Batch 6 (11 bootcamps).
1. All content.json parse; counts 5/4/7.
2. IDs unique globally across the site for the new items.
3. Console actions exist in _engine/consoles.js vocabulary.
4. Engine-level: every new mission check -- the hint's 'Type exactly: X'
   command matches command_pattern AND produces output containing
   expect_contains (runs the real terminal.js in node).
"""
import json, os, re, subprocess, sys

BASE = '/home/hatch/workspace/cert-bootcamps/site/bootcamps'
SLUGS = ['android-interview','embedded-interview','ios-interview','python-systems',
         'alan-turing','aleks-ops-math','enochian-programming','electrician-apprentice',
         'fde-training','humanmetrics','fullstack-desk']

# 1+2: parse, counts, global id uniqueness
all_ids = {}
errs = []
for slug in SLUGS:
    d = json.load(open(os.path.join(BASE, slug, 'content.json'), encoding='utf-8'))
    assert len(d['simulations']) == 5, slug
    assert len(d['consoleSims']) == 4, slug
    assert len(d['terminalMissions']) == 7, slug
    for key in ('simulations','consoleSims','terminalMissions'):
        for item in d[key]:
            iid = item['id']
            if iid in all_ids:
                errs.append('DUP ID %s in %s and %s' % (iid, slug, all_ids[iid]))
            all_ids[iid] = slug
print('parse+counts OK; new items:', len(all_ids))

# 3: console actions vs vocabulary
src = open(os.path.join(BASE, '_engine','consoles.js'), encoding='utf-8').read()
actions = set(re.findall(r"if \(action === '([\w-]+)'\)", src))
print('engine actions found:', len(actions))
for slug in SLUGS:
    d = json.load(open(os.path.join(BASE, slug, 'content.json'), encoding='utf-8'))
    for c in d['consoleSims']:
        for t in c['tasks']:
            a = t['validate']['action']
            if a not in actions:
                errs.append('%s %s: unknown action %s' % (slug, c['id'], a))
print('console actions OK')

# 4: engine-level mission check verification via node
node_script = r'''
global.window = { ENGINE_TEST: true };
require('/home/hatch/workspace/cert-bootcamps/site/bootcamps/_engine/terminal.js');
const E = global.window.__terminalEngine;
const fs = require('fs');
const slugs = JSON.parse(fs.readFileSync('/tmp/batch6-slugs.json','utf8'));
let fails = 0, total = 0;
for (const slug of slugs){
  const prof = E.profileFor(slug);
  const ctx = { state: (prof.initState ? prof.initState() : {}), profile: prof };
  const data = JSON.parse(fs.readFileSync('/home/hatch/workspace/cert-bootcamps/site/bootcamps/'+slug+'/content.json','utf8'));
  for (const m of data.terminalMissions){
    for (const ch of m.checks){
      total++;
      const hint = ch.hint || '';
      const mm = hint.match(/^Type exactly:\s*(.*)$/);
      if (!mm){ console.log('NOHINT', m.id); fails++; continue; }
      const typed = mm[1];
      let out;
      try { out = String(prof.runLine(typed, ctx)); }
      catch(e){ console.log('THROW', m.id, typed, e.message); fails++; continue; }
      let rx; try { rx = new RegExp(ch.command_pattern); } catch(e){ console.log('BADRX', m.id); fails++; continue; }
      const okCmd = rx.test(typed);
      const okOut = out.indexOf(ch.expect_contains) >= 0;
      if (!okCmd || !okOut){ console.log('FAIL', m.id, JSON.stringify(typed), 'cmd:'+okCmd, 'out:'+okOut, 'got:'+JSON.stringify(out).slice(0,80)); fails++; }
    }
  }
}
console.log('checks tested:', total, 'failures:', fails);
'''
json.dump(SLUGS, open('/tmp/batch6-slugs.json','w'))
r = subprocess.run(['node','-e',node_script], capture_output=True, text=True, cwd='/tmp')
print(r.stdout)
if r.stderr.strip():
    print('STDERR:', r.stderr[:500])
sys.exit(1 if errs or 'failures: 0' not in r.stdout else 0)
for e in errs: print('ERR:', e)
