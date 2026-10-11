#!/usr/bin/env python3
"""Move the 12 dsc lessons wrongly inserted into SCENARIOS to LESSONS."""
import ast

PATH = "/home/hatch/workspace/cert-bootcamps/scen_batchE.py"
lines = open(PATH).readlines()

# Block currently at 1-indexed lines 1356..1636 (right after SCENARIOS dsc open)
start = 1356 - 1
end = 1637 - 1  # exclusive: line 1637 is the original '# ---- ds-certs (2)'
assert lines[start].strip() == "# ds-certs (+2)", lines[start]
assert "ds-certs (2)" in lines[end], lines[end]
block = lines[start:end]
assert block[1].strip() == '"dsc-extra-dscerts-exam-anatomy": {', block[1]

rest = lines[:start] + lines[end:]

# Find LESSONS dict, then its "data-science-certs" opening
li = next(i for i, l in enumerate(rest) if l.startswith("LESSONS = {"))
t = next(i for i in range(li + 1, len(rest))
         if rest[i] == '    "data-science-certs": {\n')
new_lines = rest[: t + 1] + block + rest[t + 1:]

src = "".join(new_lines)
# NOTE: full ast.parse would fail: LESSONS dict is intentionally still open
# (more lessons to append). Validate structurally instead.

with open(PATH, "w") as f:
    f.write(src)
print("moved", len(block), "lines; total lines:", len(new_lines))

# Structural sanity via brace-aware scan (file intentionally unclosed at tail)
import re
# SCENARIOS dsc: find its dict open, check first key
m = re.search(r'^SCENARIOS = \{$', src, re.M)
assert m
dsc_m = re.search(r'^    "data-science-certs": \{$', src[m.end():], re.M)
seg = src[m.end() + dsc_m.end(): m.end() + dsc_m.end() + 400]
first_key = re.search(r'"([a-z0-9-]+)": \{', seg).group(1)
print("SCENARIOS dsc first key:", first_key)
assert first_key == "dsc-dscerts-sc1", "SCENARIOS dsc still polluted!"
# LESSONS dsc: count lesson entries moved
lm = re.search(r'^LESSONS = \{$', src, re.M)
assert lm
ldsc_m = re.search(r'^    "data-science-certs": \{$', src[lm.end():], re.M)
lseg_start = lm.end() + ldsc_m.end()
lesson_keys = re.findall(r'^        "(dsc-extra-[a-z0-9-]+)": \{$', src[lseg_start:], re.M)
print("LESSONS dsc lesson count:", len(lesson_keys))
assert len(lesson_keys) == 12, lesson_keys
print("OK: block moved cleanly")
