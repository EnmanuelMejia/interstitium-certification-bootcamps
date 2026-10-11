#!/usr/bin/env python3
"""Apply built content to CBT content.json files. Only ADDS, never modifies existing."""
import json, sys, importlib

BOOT = "/home/hatch/workspace/cert-bootcamps/site/bootcamps"

# cbt_id -> list of (module_name, builder_fn_name, extra_labs)
PLAN = {
    "active-directory-defense": [
        ("cbt_data_add1", "build_part1", None),
        ("cbt_data_add2", "build_part2", None),
    ],
}

def expand_existing(data, target_lessons=4):
    """Add lessons to existing domains to reach target_lessons each."""
    # This is handled per-CBT in data modules via EXTRA_LESSONS if needed
    return 0

def apply_cbt(cbt_id, parts):
    path = f"{BOOT}/{cbt_id}/content.json"
    with open(path) as f:
        data = json.load(f)

    existing_ids = {d["id"] for d in data["domains"]}
    total_lessons = 0
    total_scenarios = 0
    total_labs = 0

    for mod_name, fn_name, _ in parts:
        mod = importlib.import_module(mod_name)
        fn = getattr(mod, fn_name)
        new_domains, labs = fn()
        for d in new_domains:
            if d["id"] in existing_ids:
                print(f"  SKIP duplicate domain {d['id']}")
                continue
            # lessons were built alongside; find them
            existing_ids.add(d["id"])
            data["domains"].append(d)
            total_scenarios += len(d.get("scenarios", []))
        # lessons are top-level
        # We need the lessons list too — rebuild: collect from module
        total_labs += len(labs)
        data.setdefault("labs", []).extend(labs)

    # Collect lessons: re-run builders to get lessons (they're returned separately)
    # Actually lessons are inside new_domains build; let's restructure:
    return data, total_scenarios, total_labs

if __name__ == "__main__":
    # This is a library; real apply is in cbt_run.py
    print("import cbt_apply and use apply logic in cbt_run.py")
