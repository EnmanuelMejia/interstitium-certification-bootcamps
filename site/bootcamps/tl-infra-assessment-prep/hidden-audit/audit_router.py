#!/usr/bin/env python3
"""Router audit: list all routes handled in app.js, check each has a renderer,
and check every go()/href route target is handled."""
import re

js = open("/home/hatch/workspace/cbt-individual/tl-infra-assessment-prep/app.js", encoding="utf-8").read()

# Find router: look for route dispatch patterns like case '#/...' or if (hash.startsWith('#/...'))
cases = re.findall(r"""case\s+['"](#/[^'"]*)['"]""", js)
starts = re.findall(r"""(?:startsWith|indexOf)\(['"](#/[^'"]*)['"]""", js)
eqhash = re.findall(r"""(?:===|==)\s*['"](#/[^'"]*)['"]""", js)
print("case routes:", cases)
print("startsWith/indexOf routes:", starts)
print("== routes:", eqhash)

# renderer function names
renderers = set(re.findall(r"""function\s+(render[A-Za-z0-9_]*|show[A-Za-z0-9_]*|view[A-Za-z0-9_]*|draw[A-Za-z0-9_]*)""", js))
print(f"\nrenderer-ish functions ({len(renderers)}):", sorted(renderers)[:40])

# every route target used
targets = set(re.findall(r"""(?:go\(|href=)["'](#/[^"'#?]*?)(?:\?[^"']*)?["']""", js))
# also href="#/..." in template literals with dynamic parts
dyn = re.findall(r"""['"`](#/[A-Za-z0-9_\-./]*/)['"`]\s*\+\s*""", js)
print("\nstatic route targets used:", sorted(targets))
print("dynamic-prefix targets:", sorted(set(dyn)))

# module/scenario/lesson ids: verify render functions for pattern routes
print("\n--- router dispatch block ---")
# print lines containing route dispatch
for i, line in enumerate(js.splitlines(), 1):
    if re.search(r"#/(dashboard|learn|module|lesson|drills|mock|reference|terminal|lab|scenario)", line) and ("case" in line or "startsWith" in line or "===" in line or "function route" in line or "render(" in line):
        print(i, line.strip()[:160])
