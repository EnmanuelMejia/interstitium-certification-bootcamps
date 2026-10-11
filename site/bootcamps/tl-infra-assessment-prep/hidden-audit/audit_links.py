#!/usr/bin/env python3
"""Link integrity audit: crawl all internal references and verify targets exist."""
import os, re, json, sys

ROOT = os.path.expanduser("~/workspace/cbt-individual/tl-infra-assessment-prep")
all_files = []
for dirpath, _, filenames in os.walk(ROOT):
    if "hidden-audit" in dirpath:
        continue
    for f in filenames:
        all_files.append(os.path.join(dirpath, f))

html_files = sorted(f for f in all_files if f.endswith(".html"))
print("HTML files:", len(html_files))
for f in html_files:
    print("  ", os.path.relpath(f, ROOT))

issues = []
checked = 0

def check(source, lineno, ref, base_dir):
    """Resolve ref relative to base_dir (bootcamp root-relative), verify existence."""
    global checked
    ref = ref.strip()
    if not ref:
        return
    # skip external, anchors-only, data:, mailto, tel, javascript, telnet
    if re.match(r"^(https?:|data:|mailto:|tel:|javascript:|telnet:|#)", ref):
        return
    # strip query and fragment
    clean = ref.split("#")[0].split("?")[0]
    if not clean:
        return
    checked += 1
    resolved = os.path.normpath(os.path.join(base_dir, clean))
    if not os.path.exists(resolved):
        issues.append(f"LINK: {os.path.relpath(source, ROOT)}:{lineno} -> '{ref}' resolves to {os.path.relpath(resolved, ROOT)} (MISSING)")
    # trailing slash -> should map to index
    if ref.endswith("/") and os.path.isdir(resolved):
        idx = os.path.join(resolved, "index.html")
        if not os.path.exists(idx):
            issues.append(f"LINK: {os.path.relpath(source, ROOT)}:{lineno} -> '{ref}' is a directory without index.html")

# 1) HTML attributes
for path in html_files:
    base = os.path.dirname(path)
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        # href / src / action attributes
        for m in re.finditer(r'''(?:href|src|action)\s*=\s*["']([^"']+)["']''', line):
            check(path, i, m.group(1), base)
        # url(...) in styles
        for m in re.finditer(r"""url\(\s*['"]?([^'")\s]+)['"]?\s*\)""", line):
            check(path, i, m.group(1), base)

# 2) content.json resources.links + media svg
cj = json.load(open(os.path.join(ROOT, "content.json")))
links_checked = 0
def walk(obj):
    global links_checked
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("url", "href", "src", "svg") and isinstance(v, str):
                links_checked += 1
                check(os.path.join(ROOT, "content.json"), 0, v, ROOT)
            walk(v)
    elif isinstance(obj, list):
        for x in obj:
            walk(x)
walk(cj)
print("content.json url-like fields checked:", links_checked)

# 3) app.js route targets
js = open(os.path.join(ROOT, "app.js"), encoding="utf-8").read()
routes_in_go = set(re.findall(r"""go\(['"](#/[^'"]*)['"]""", js))
routes_in_href = set(re.findall(r'''href=["'](#/[^"']*)["']''', js))
routes_in_template = set(re.findall(r'''["'](#/[A-Za-z0-9_\-./?]*)["']''', js))
print("\ngo() routes:", sorted(routes_in_go))
print("href routes:", sorted(routes_in_href))

# 4) ios-cli.js reference from each network sim page
# NOTE: terminal-mastery.html is a LINUX terminal sim with its own inline engine;
# ios-cli.js is the Cisco IOS engine used only by the 6 IOS network sims. Exempt by design.
net_sims = ["vlan-basics.html", "inter-vlan-routing.html", "static-routing.html",
            "dhcp-server.html", "nat-pat.html", "site-to-site-vpn.html"]
for s in net_sims:
    p = os.path.join(ROOT, "sims", s)
    content = open(p, encoding="utf-8").read()
    if "ios-cli.js" in content:
        print(f"  {s}: references ios-cli.js OK")
    else:
        issues.append(f"IOS-CLI: sims/{s} does NOT reference sims/ios-cli.js")

# Also check all sims reference it where they use shared CLI
for path in html_files:
    if "/sims/" in path:
        content = open(path, encoding="utf-8").read()
        uses_cli = re.search(r"CLI|cli|command", content[:2000], re.I)

print("\n==== SUMMARY ====")
print("internal refs checked:", checked)
print("issues:", len(issues))
for i in issues:
    print("  " + i)
