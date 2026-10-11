#!/usr/bin/env python3
"""Rebalance scenario answer indices to ~25% each via choice rotation."""
import ast
import json
import re

PATH = "/home/hatch/workspace/cert-bootcamps/scen_batchE.py"
src = open(PATH).read()

pat = re.compile(r'"choices": \[(.*?)\],\n(\s*)"answer": (\d)', re.S)
matches = list(pat.finditer(src))
print("scenario choice-blocks found:", len(matches))
assert len(matches) == 140, f"expected 140, got {len(matches)}"

out = []
last = 0
for idx, m in enumerate(matches):
    raw_choices = "[" + m.group(1) + "]"
    choices = ast.literal_eval(raw_choices)
    assert len(choices) == 4, f"block {idx}: {len(choices)} choices"
    a = int(m.group(3))
    t = idx % 4  # round-robin target: 0,1,2,3,...
    k = (a - t) % 4
    rot = choices[k:] + choices[:k]
    # rebuild with original formatting style
    indent = "                "
    body = (",\n").join(indent + json.dumps(c, ensure_ascii=True) for c in rot)
    new_block = f'"choices": [\n{body}\n            ],\n{m.group(2)}"answer": {t}'
    out.append(src[last:m.start()])
    out.append(new_block)
    last = m.end()
out.append(src[last:])
new_src = "".join(out)

ast.parse(new_src)  # syntax check
with open(PATH, "w") as f:
    f.write(new_src)

# verify distribution
mod = {}
exec(compile(ast.parse(new_src), PATH, "exec"), {}, mod)
from collections import Counter
dist = Counter(s["answer"] for d in mod["SCENARIOS"].values() for s in d.values())
print("new answer distribution:", dict(dist))
assert set(dist) == {0, 1, 2, 3}, dist
# verify each scenario still has 4 choices and key/id integrity
for cbt, d in mod["SCENARIOS"].items():
    for sid, s in d.items():
        assert sid == s["id"] and len(s["choices"]) == 4
print("OK: rebalanced, structure intact")
