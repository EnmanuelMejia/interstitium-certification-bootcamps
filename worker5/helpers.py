#!/usr/bin/env python3
"""Worker 5 (group B) fragment builder — shared helpers."""
import json, os, re

BASE = os.path.expanduser('~/workspace/cert-bootcamps/content')

def check(pattern, expect, hint_cmd):
    return {"command_pattern": pattern,
            "expect_contains": expect,
            "hint": "In the Terminal tab, run `%s`. If the check fails, confirm you typed it exactly and that the output contains \"%s\"." % (hint_cmd, expect)}

def lab(lid, title, objective, difficulty, steps, checks, success):
    return {"id": lid, "title": title, "objective": objective,
            "difficulty": difficulty, "steps": steps, "checks": checks,
            "success_message": success}

def mission(mid, title, domain_id, difficulty, brief, objectives, checks, success):
    return {"id": mid, "title": title, "domain_id": domain_id,
            "difficulty": difficulty, "brief": brief, "objectives": objectives,
            "checks": checks, "success_message": success}

def sim(sid, title, kind, domain_id, difficulty, brief, steps, debrief, points=10):
    return {"id": sid, "title": title, "kind": kind, "domain_id": domain_id,
            "difficulty": difficulty, "brief": brief, "steps": steps,
            "debrief": debrief, "points": points}

def console(cid, title, console_type, domain_id, difficulty, brief, tasks, debrief):
    return {"id": cid, "title": title, "console": console_type,
            "domain_id": domain_id, "difficulty": difficulty, "brief": brief,
            "tasks": tasks, "debrief": debrief}

def task(tid, instruction, action, params, hint):
    return {"id": tid, "instruction": instruction,
            "validate": {"action": action, "params": params}, "hint": hint}

def write_fragment(slug, fragment):
    d = os.path.join(BASE, slug, 'fragments')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'extended.json')
    with open(p, 'w') as f:
        json.dump(fragment, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print('wrote', p)

def build(fragments):
    for slug, frag in fragments.items():
        write_fragment(slug, frag)
