#!/usr/bin/env python3
"""Full validation of scen_batchE.py content."""
import ast
import re
import sys

PATH = "/home/hatch/workspace/cert-bootcamps/scen_batchE.py"
src = open(PATH).read()
tree = ast.parse(src)

# Extract the three top-level dicts safely
mod = {}
exec(compile(tree, PATH, "exec"), {}, mod)
SCENARIOS, LESSONS, LABS = mod["SCENARIOS"], mod["LESSONS"], mod["LABS"]

errors = []

# ---- structural shape ----
assert set(SCENARIOS) == {"data-analyst-to-ml", "data-science-certs"}, set(SCENARIOS)
assert set(LESSONS) == {"data-analyst-to-ml", "data-science-certs"}, set(LESSONS)
assert set(LABS) == {"data-analyst-to-ml", "data-science-certs"}, set(LABS)
assert isinstance(LABS["data-analyst-to-ml"], list)

# ---- counts ----
exp_scen = {"data-analyst-to-ml": 70, "data-science-certs": 70}
exp_less = {"data-analyst-to-ml": 24, "data-science-certs": 24}
exp_labs = {"data-analyst-to-ml": 12, "data-science-certs": 13}
for cbt, n in exp_scen.items():
    got = len(SCENARIOS[cbt])
    print(f"scenarios {cbt}: {got} (expect {n})")
    if got != n:
        errors.append(f"scenario count {cbt}: {got} != {n}")
for cbt, n in exp_less.items():
    got = len(LESSONS[cbt])
    print(f"lessons   {cbt}: {got} (expect {n})")
    if got != n:
        errors.append(f"lesson count {cbt}: {got} != {n}")
for cbt, n in exp_labs.items():
    got = len(LABS[cbt])
    print(f"labs      {cbt}: {got} (expect {n})")
    if got != n:
        errors.append(f"lab count {cbt}: {got} != {n}")

# ---- scenario field checks ----
SCEN_FIELDS = {"id", "title", "domain_id", "situation", "prompt", "choices",
               "answer", "why", "hint", "objectives", "mins", "evidence"}
for cbt, d in SCENARIOS.items():
    for sid, s in d.items():
        if sid != s.get("id"):
            errors.append(f"key/id mismatch: {sid} vs {s.get('id')}")
        missing = SCEN_FIELDS - set(s)
        if missing:
            errors.append(f"{sid} missing fields {missing}")
        ch = s.get("choices", [])
        if len(ch) != 4:
            errors.append(f"{sid} choices != 4 ({len(ch)})")
        a = s.get("answer")
        if not isinstance(a, int) or not (0 <= a <= 3):
            errors.append(f"{sid} bad answer index {a}")
        if not isinstance(s.get("mins"), int):
            errors.append(f"{sid} mins not int")
        if not s.get("objectives") or not s.get("evidence"):
            errors.append(f"{sid} empty objectives/evidence")

# answer index distribution (should vary)
from collections import Counter
dist = Counter(s["answer"] for d in SCENARIOS.values() for s in d.values())
print("answer index distribution:", dict(dist))

# ---- lesson field checks ----
LES_FIELDS = {"_id", "id", "title", "domain_id", "concepts", "example",
              "pitfalls", "try_it"}
for cbt, d in LESSONS.items():
    for lid, ls in d.items():
        if lid != ls.get("id") or lid != ls.get("_id"):
            errors.append(f"lesson key/id mismatch: {lid}")
        missing = LES_FIELDS - set(ls)
        if missing:
            errors.append(f"{lid} missing {missing}")
        ex = ls.get("example", {})
        if not isinstance(ex, dict) or "code" not in ex or "walkthrough" not in ex:
            errors.append(f"{lid} bad example shape")
        if len(ls.get("concepts", [])) < 3:
            errors.append(f"{lid} <3 concepts")
        if len(ls.get("pitfalls", [])) < 3:
            errors.append(f"{lid} <3 pitfalls")

# ---- lab field checks ----
LAB_FIELDS = {"_id", "id", "title", "domain_id", "objective", "steps",
              "checks", "debrief"}
for cbt, labs in LABS.items():
    for lab in labs:
        missing = LAB_FIELDS - set(lab)
        if missing:
            errors.append(f"{lab.get('id')} missing {missing}")
        if lab.get("_id") != lab.get("id"):
            errors.append(f"lab _id/id mismatch {lab.get('id')}")
        if len(lab.get("steps", [])) < 3:
            errors.append(f"{lab.get('id')} <3 steps")
        for c in lab.get("checks", []):
            if set(c) != {"command", "output", "hint"}:
                errors.append(f"{lab.get('id')} bad check shape {set(c)}")

# ---- global id uniqueness ----
all_ids = []
for d in SCENARIOS.values():
    all_ids += list(d.keys())
for d in LESSONS.values():
    all_ids += list(d.keys())
for labs in LABS.values():
    all_ids += [l["id"] for l in labs]
dupes = [i for i, c in Counter(all_ids).items() if c > 1]
if dupes:
    errors.append(f"duplicate ids: {dupes}")
print("total items:", len(all_ids), "| unique:", len(set(all_ids)))

# ---- per-domain scenario distribution ----
for cbt, d in SCENARIOS.items():
    print(cbt, dict(Counter(s["domain_id"] for s in d.values())))
for cbt, d in LESSONS.items():
    print(cbt, "lessons:", dict(Counter(s["domain_id"] for s in d.values())))
for cbt, labs in LABS.items():
    print(cbt, "labs:", dict(Counter(s["domain_id"] for s in labs)))

# ---- competitor-name scan ----
COMPETITORS = ["udemy", "coursera", "pluralsight", "udacity", "datacamp",
               "codecademy", "linkedin learning", "skillshare", "masterclass",
               "khan academy"]
low = src.lower()
hits = [c for c in COMPETITORS if c in low]
if hits:
    errors.append(f"competitor names found: {hits}")
else:
    print("competitor scan: clean")

# ---- no empty-string fields ----
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str) and not o.strip():
        errors.append(f"empty string at {path}")

walk(mod)
print("errors:", len(errors))
for e in errors[:30]:
    print("  -", e)
sys.exit(1 if errors else 0)
