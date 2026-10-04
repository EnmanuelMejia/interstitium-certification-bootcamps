#!/usr/bin/env python3
"""Cross-check: every DOM id referenced by the engines exists in its template,
and every BOOTCAMP_PAGE/CHAT_PAGE field used by an engine is set by the shell."""
import re, sys

def ids_in_engine(path):
    src = open(path, encoding="utf-8").read()
    pat1 = re.compile(r"\bel\(['\"]([\w-]+)['\"]\)")
    pat2 = re.compile(r"\$\(['\"]([\w-]+)['\"]\)")
    pat3 = re.compile(r"getElementById\(['\"]([\w-]+)['\"]\)")
    return set(pat1.findall(src)) | set(pat2.findall(src)) | set(pat3.findall(src))

def ids_in_tpl(path):
    return set(re.compile(r'id="([\w-]+)"').findall(open(path, encoding="utf-8").read()))

def page_fields_set(tpl, var):
    src = open(tpl, encoding="utf-8").read()
    m = re.search(r"window\." + re.escape(var) + r"\s*=\s*\{([\s\S]*?)\n\};", src)
    return set(re.findall(r"(\w+)\s*:", m.group(1))) if m else set()

def page_fields_used(eng, var):
    src = open(eng, encoding="utf-8").read()
    # engines alias: var PAGE = window.BOOTCAMP_PAGE || {};
    m = re.search(r"var\s+(\w+)\s*=\s*window\." + re.escape(var), src)
    alias = m.group(1) if m else var
    return set(re.findall(re.escape(alias) + r"\.(\w+)", src))

# ids created dynamically via innerHTML inside the engine, then bound
# immediately (verified by inspection) — not present in static templates
DYNAMIC_IDS = {"backToDash", "nextRepBtn", "rerunSim"}

pairs = [
    ("engine/bootcamp.js", "templates/bootcamp.html", "BOOTCAMP_PAGE"),
    ("engine/chat.js", "templates/chat.html", "CHAT_PAGE"),
    ("engine/hub.js", "templates/hub.html", None),
]
ok = True
for eng, tpl, var in pairs:
    need = ids_in_engine(eng) - DYNAMIC_IDS
    have = ids_in_tpl(tpl)
    missing = sorted(need - have)
    print("%s -> %s: %d ids, missing=%s" % (eng, tpl, len(need), missing or "NONE"))
    ok = ok and not missing
    if var:
        used, sett = page_fields_used(eng, var), page_fields_set(tpl, var)
        gap = sorted(used - sett)
        print("  %s fields used=%s set=%s gap=%s" % (var, sorted(used), sorted(sett), gap or "NONE"))
        ok = ok and not gap
print("ALL OK" if ok else "MISMATCH FOUND")
sys.exit(0 if ok else 1)
