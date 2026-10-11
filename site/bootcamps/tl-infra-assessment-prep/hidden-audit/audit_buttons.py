#!/usr/bin/env python3
"""Button audit: every <button> must have onclick / addEventListener / delegated data-* handler."""
import os, re

ROOT = os.path.expanduser("~/workspace/cbt-individual/tl-infra-assessment-prep")
dead = []
ok_count = 0

for dirpath, _, filenames in sorted(os.walk(ROOT)):
    if "hidden-audit" in dirpath:
        continue
    for f in sorted(filenames):
        if not f.endswith(".html"):
            continue
        path = os.path.join(dirpath, f)
        rel = os.path.relpath(path, ROOT)
        html = open(path, encoding="utf-8", errors="replace").read()
        scripts = " ".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S | re.I))
        has_delegation = re.search(r"addEventListener\s*\(\s*['\"]click['\"]", scripts)
        # find buttons
        for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", html, re.S | re.I):
            global_ok = ok_count
            attrs, inner = m.group(1), m.group(2).strip()[:50]
            line = html[:m.start()].count("\n") + 1
            if re.search(r"\bonclick\s*=", attrs, re.I):
                ok_count += 1
                continue
            bid = re.search(r'''\bid\s*=\s*["']([^"']+)["']''', attrs)
            if bid and re.search(
                r"(getElementById|el|querySelector|querySelectorAll|\$|jQuery)\s*\(\s*['\"]#?" + re.escape(bid.group(1)) + r"['\"]",
                scripts):
                # listener attached? check addEventListener or .onclick near
                if re.search(r"addEventListener|onclick", scripts):
                    ok_count += 1
                    continue
            # data-* attribute with delegation
            data_attrs = re.findall(r"\bdata-([a-zA-Z0-9_-]+)\s*=\s*[\"']([^\"']*)[\"']", attrs)
            if data_attrs and has_delegation:
                ok_count += 1
                continue
            # type=submit inside a form
            if re.search(r"""\btype\s*=\s*['"]submit['"]""", attrs, re.I):
                # check enclosing form with handler
                before = html[:m.start()]
                open_forms = len(re.findall(r"<form\b", before, re.I)) - len(re.findall(r"</form>", before, re.I))
                if open_forms > 0 and re.search(r"addEventListener\s*\(\s*['\"]submit['\"]|<form\b[^>]*\bon(action|submit)", scripts, re.I):
                    ok_count += 1
                    continue
            dead.append(f"BUTTON: {rel}:{line} <button{attrs[:90]}> inner='{inner}' — no handler found")
        # also check <input type=button|submit|reset> and role=button divs? focus on button tags per task
        for m in re.finditer(r"<input\b([^>]*\btype\s*=\s*['\"](button|submit|reset)['\"][^>]*)>", html, re.I):
            attrs = m.group(1)
            line = html[:m.start()].count("\n") + 1
            if re.search(r"\bonclick\s*=", attrs, re.I):
                ok_count += 1; continue
            bid = re.search(r'''\bid\s*=\s*["']([^"']+)["']''', attrs)
            if bid and re.search(r"addEventListener|onclick", scripts):
                ok_count += 1; continue
            dead.append(f"INPUT-BUTTON: {rel}:{line} <input{attrs[:90]}> — no handler found")

print("buttons/inputs with handlers:", ok_count)
print("dead buttons/inputs:", len(dead))
for d in dead:
    print("  " + d)
