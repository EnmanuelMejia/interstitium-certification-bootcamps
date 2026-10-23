#!/usr/bin/env python3
"""Strict button audit: require direct wiring evidence per button."""
import os, re

def _script_spans(html):
    """(start, end, body) for each <script>...</script> block, found by
    scanning (regexes cannot match end-tag variants like </script >
    reliably). Case-insensitive; tolerates attributes on both tags."""
    low = html.lower()
    spans, i = [], 0
    while True:
        start = low.find("<script", i)
        if start < 0:
            break
        open_end = low.find(">", start)
        if open_end < 0:
            break
        close = low.find("</script", open_end)
        if close < 0:
            break
        close_end = low.find(">", close)
        end = close_end + 1 if close_end >= 0 else len(html)
        spans.append((start, end, html[open_end + 1:close]))
        i = end
    return spans

ROOT = os.path.expanduser("~/workspace/cbt-individual/tl-infra-assessment-prep")
dead, ok = [], 0

for dirpath, _, filenames in sorted(os.walk(ROOT)):
    if "hidden-audit" in dirpath:
        continue
    for f in sorted(filenames):
        if not f.endswith(".html"):
            continue
        path = os.path.join(dirpath, f)
        rel = os.path.relpath(path, ROOT)
        html = open(path, encoding="utf-8", errors="replace").read()
        scripts = " ".join(body for _, _, body in _script_spans(html))
        # remove dynamically-generated HTML strings from scripts for static-button matching
        for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", html, re.S | re.I):
            attrs, inner = m.group(1), m.group(2).strip()[:60].replace("\n", " ")
            line = html[:m.start()].count("\n") + 1
            # skip buttons that are inside <script> template strings (dynamically created)
            scr_ranges = [(start, end) for start, end, _ in _script_spans(html)]
            if any(s <= m.start() < e for s, e in scr_ranges):
                continue
            wired = False
            if re.search(r"\bonclick\s*=", attrs, re.I):
                wired = True
            else:
                bid = re.search(r'''\bid\s*=\s*["']([^"']+)["']''', attrs)
                if bid:
                    b = re.escape(bid.group(1))
                    # el("id").addEventListener / .onclick = / $("#id").on( / addEventListener after el("id") within same statement
                    if re.search(r"""(?:el|getElementById|\$|jQuery|querySelector)\s*\(\s*['"]#?""" + b + r"""['"]\s*\)\s*(?:\)?)\s*\.\s*(?:addEventListener|onclick)""", scripts) or \
                       re.search(r"""\.\s*(?:addEventListener|onclick)\s*[=(].{0,200}(?:el|getElementById|\$)\s*\(\s*['"]#?""" + b + r"""['"]\s*\)""", scripts, re.S):
                        wired = True
                if not wired:
                    data_attrs = re.findall(r"\bdata-([a-zA-Z0-9_-]+)", attrs)
                    for da in data_attrs:
                        if re.search(r"dataset\." + re.escape(da) + r"|getAttribute\(['\"]data-" + re.escape(da), scripts):
                            wired = True
                            break
                if not wired and re.search(r"""\btype\s*=\s*['"]submit['"]""", attrs, re.I):
                    before = html[:m.start()]
                    open_forms = len(re.findall(r"<form\b", before, re.I)) - len(re.findall(r"</form>", before, re.I))
                    if open_forms > 0 and re.search(r"addEventListener\s*\(\s*['\"]submit['\"]", scripts):
                        wired = True
            if wired:
                ok += 1
            else:
                dead.append(f"BUTTON: {rel}:{line} id={[re.search(chr(105)+chr(100)+r'=\\"[^\"]*\\"', attrs).group(0) if re.search(chr(105)+chr(100)+r'=\\"[^\"]*\\"', attrs) else None]} inner='{inner}'")
        for m in re.finditer(r"<input\b([^>]*\btype\s*=\s*['\"](button|submit|reset)['\"][^>]*)>", html, re.I):
            attrs = m.group(1)
            line = html[:m.start()].count("\n") + 1
            if re.search(r"\bonclick\s*=", attrs, re.I):
                ok += 1; continue
            bid = re.search(r'''\bid\s*=\s*["']([^"']+)["']''', attrs)
            b = re.escape(bid.group(1)) if bid else None
            if b and re.search(r"""(?:el|getElementById|\$)\s*\(\s*['"]#?""" + b + r"""['"]\s*\)\s*\.\s*(?:addEventListener|onclick)""", scripts):
                ok += 1
            else:
                dead.append(f"INPUT: {rel}:{line} <input{attrs[:70]}>")

print("wired:", ok, "| unwired:", len(dead))
for d in dead:
    print("  " + d)
