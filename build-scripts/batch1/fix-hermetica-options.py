#!/usr/bin/env python3
"""Add 4th distractor options to acad-hermetica-sim-5 steps (consistency: 4 options each)."""
import json, os

path = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps/acad-hermetica/content.json')
d = json.load(open(path))

for s in d['simulations']:
    if s['id'] == 'acad-hermetica-sim-5':
        assert len(s['steps']) == 3
        s['steps'][0]['options'].append(
            "No model fits — treat the rumor as a unique crisis with no precedent")
        s['steps'][1]['options'].append(
            "Bank-run model: reassure deployers the queue is fine and ask them to wait calmly")
        s['steps'][2]['options'].append(
            "Traffic-jam model: process withdrawals faster to clear the queue")
        for st in s['steps']:
            assert len(st['options']) == 4

tmp = path + '.tmp'
with open(tmp, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')
os.replace(tmp, path)

d2 = json.load(open(path))
for s in d2['simulations']:
    if s['id'] == 'acad-hermetica-sim-5':
        for st in s['steps']:
            assert len(st['options']) == 4 and isinstance(st['correct'], int)
print('acad-hermetica-sim-5: 4 options per step OK')
