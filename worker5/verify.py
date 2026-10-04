#!/usr/bin/env python3
"""Verify all 17 extended.json fragments for Worker 5 group B."""
import json, re, glob, os, sys

BASE = os.path.expanduser("~/workspace/cert-bootcamps/content")
SLUGS = ["cissp","cism","aws-clf","aws-saa","aws-soa","aws-dop","aws-scs","aws-data",
         "aws-ml","ms-fundamentals","az-104","az-305","az-700","azure-developer",
         "dp-203","sc-200","sc-300"]
errors, total = [], 0

for slug in SLUGS:
    with open(f"{BASE}/{slug}.json") as f:
        base = json.load(f)
    with open(f"{BASE}/{slug}/fragments/extended.json") as f:
        frag = json.load(f)
    domains = {d["id"] for d in base.get("domains", [])}
    existing_labs = {l["id"] for l in base.get("labs", [])}
    ids = set()
    def reg(iid, where):
        if iid in ids: errors.append(f"{slug}: duplicate id {iid} in {where}")
        if iid in existing_labs: errors.append(f"{slug}: id collides with existing lab: {iid}")
        ids.add(iid)
    counts = {}
    for key in ["labs_add","simulations","consoleSims","terminalMissions"]:
        items = frag.get(key, [])
        counts[key] = len(items)
        for it in items:
            reg(it["id"], key)
            if key in ("simulations","consoleSims") and it.get("domain_id") not in domains:
                errors.append(f"{slug}: {it['id']} bad domain_id {it.get('domain_id')}")
            for c in it.get("checks", []):
                try: re.compile(c["command_pattern"])
                except re.error as e:
                    errors.append(f"{slug}: {it['id']} bad regex {c['command_pattern']}: {e}")
                if "expect_contains" not in c or "command_pattern" not in c or "hint" not in c:
                    errors.append(f"{slug}: {it['id']} check missing keys")
    # difficulty sanity
    diffs = [l.get("difficulty") for l in frag["labs_add"]]
    if sorted(diffs) != [1,1,2,3]:
        errors.append(f"{slug}: lab difficulties {diffs} not 2x1/1x2/1x3")
    kinds = {s["kind"] for s in frag["simulations"]}
    if len(kinds) < 2:
        errors.append(f"{slug}: simulations need >=2 kinds, have {kinds}")
    if len(frag["simulations"]) < 4: errors.append(f"{slug}: <4 simulations")
    if len(frag["consoleSims"]) < 2: errors.append(f"{slug}: <2 consoleSims")
    if len(frag["terminalMissions"]) < 6: errors.append(f"{slug}: <6 missions")
    total += sum(counts.values())
    print(f"{slug}: labs_add={counts['labs_add']} sims={counts['simulations']} "
          f"consoles={counts['consoleSims']} missions={counts['terminalMissions']} "
          f"sim-kinds={sorted(kinds)}")

print(f"\nTOTAL items: {total}")
if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors: print("  -", e)
    sys.exit(1)
print("\nALL CHECKS PASSED")
