#!/usr/bin/env python3
"""Apply built content to CBT content.json files. Only ADDS. Validates JSON."""
import json, sys, importlib

BOOT = "/home/hatch/workspace/cert-bootcamps/site/bootcamps"

def apply_cbt(cbt_id, builders):
    """builders: list of (module_name, fn_name). Returns stats."""
    path = f"{BOOT}/{cbt_id}/content.json"
    with open(path) as f:
        data = json.load(f)

    existing_ids = {d["id"] for d in data["domains"]}
    existing_lab_ids = {l["id"] for l in data.get("labs", [])}
    data.setdefault("lessons", [])
    data.setdefault("labs", [])

    n_domains = n_lessons = n_scenarios = n_labs = 0

    for mod_name, fn_name in builders:
        mod = importlib.import_module(mod_name)
        result = getattr(mod, fn_name)()
        if len(result) == 4:
            new_domains, lessons_extra, scenarios_extra, labs = result
        elif "_expansion" in fn_name:
            lessons_extra, scenarios_extra = result
            new_domains, labs = [], []
        else:
            new_domains, labs = result
            lessons_extra, scenarios_extra = [], {}
        # Apply extra lessons (expansions of existing domains)
        for les in lessons_extra:
            data["lessons"].append(les)
            n_lessons += 1
        # Apply extra scenarios to existing domains
        for did, slist in scenarios_extra.items():
            dom = next((d for d in data["domains"] if d["id"] == did), None)
            assert dom is not None, f"expansion domain not found: {did}"
            for s in slist:
                assert s["domain_id"] == did
                assert len(s["choices"]) == 4
                dom.setdefault("scenarios", []).append(s)
                n_scenarios += 1
        for d in new_domains:
            if d["id"] in existing_ids:
                print(f"  [{cbt_id}] SKIP duplicate domain {d['id']}")
                continue
            existing_ids.add(d["id"])
            # Extract stashed lessons to top-level
            stashed = d.pop("_lessons", [])
            for les in stashed:
                assert les["domain_id"] == d["id"], f"lesson domain mismatch in {d['id']}"
                data["lessons"].append(les)
                n_lessons += 1
            # Validate scenarios
            for s in d.get("scenarios", []):
                assert s["domain_id"] == d["id"], f"scenario domain mismatch in {d['id']}"
                assert len(s["choices"]) == 4
            n_scenarios += len(d.get("scenarios", []))
            data["domains"].append(d)
            n_domains += 1
        for lab in labs:
            if lab["id"] in existing_lab_ids:
                print(f"  [{cbt_id}] SKIP duplicate lab {lab['id']}")
                continue
            existing_lab_ids.add(lab["id"])
            data["labs"].append(lab)
            n_labs += 1

    # Validate whole file
    json.dumps(data)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    # Re-read to confirm valid
    with open(path) as f:
        json.load(f)

    return n_domains, n_lessons, n_scenarios, n_labs

def report(cbt_id):
    path = f"{BOOT}/{cbt_id}/content.json"
    with open(path) as f:
        data = json.load(f)
    n_dom = len(data["domains"])
    n_les = len(data.get("lessons", []))
    n_scen = sum(len(d.get("scenarios", [])) for d in data["domains"])
    n_labs = len(data.get("labs", []))
    doms = sorted(d["id"] for d in data["domains"])
    return n_dom, n_les, n_scen, n_labs, doms

if __name__ == "__main__":
    plan = {
        "active-directory-defense": [("cbt_data_add1", "build_part1"), ("cbt_data_add2", "build_part2"), ("cbt_data_add3", "build_part3")],
        "ai-agent-sec": [("cbt_data_aas", "build"), ("cbt_data_aas2", "build_aas2"), ("cbt_data_aas3", "build_aas3")],
        "ai-product": [("cbt_data_aiprod", "build_aiprod"), ("cbt_data_aiprod_exp", "build_expansion_aiprod")],
        "aws-clf": [("cbt_data_awsclf", "build_awsclf"), ("cbt_data_awsclf_exp", "build_expansion_awsclf")],
        "adaptive-foundations": [("cbt_data_adf2", "build_adf2"), ("cbt_data_adf3", "build_adf3"), ("cbt_data_adf4", "build_adf4"), ("cbt_data_adf2", "build_adf2_expansion")],
        "alan-turing": [("cbt_data_turing", "build_turing"), ("cbt_data_turing2", "build_turing2"), ("cbt_data_turing3", "build_turing3"), ("cbt_data_turing", "build_turing_expansion")],
        "ai-lab": [("cbt_data_ailab1", "build_ailab1"), ("cbt_data_ailab2", "build_ailab2"), ("cbt_data_ailab3", "build_ailab3"), ("cbt_data_ailab4", "build_ailab4"), ("cbt_data_ailab4", "build_ailab_expansion")],
        "aleks-ops-math": [("cbt_data_aleks1", "build_aleks1"), ("cbt_data_aleks2", "build_aleks2"), ("cbt_data_aleks3", "build_aleks3"), ("cbt_data_aleks4", "build_aleks4"), ("cbt_data_aleks4", "build_aleks_expansion")],
        "android-interview": [("cbt_data_android", "build_android"), ("cbt_data_android_exp1", "build_expansion_android")],
        "aws-cloud-practitioner-plus": [("cbt_data_awsp", "build_awsp"), ("cbt_data_awsp_exp", "build_expansion_awsp")],
    }
    only = sys.argv[1:] or list(plan.keys())
    for cbt_id in only:
        if cbt_id not in plan:
            print(f"No plan for {cbt_id}")
            continue
        print(f"Applying {cbt_id}...")
        try:
            st = apply_cbt(cbt_id, plan[cbt_id])
            print(f"  added: domains={st[0]} lessons={st[1]} scenarios={st[2]} labs={st[3]}")
            r = report(cbt_id)
            print(f"  TOTAL: domains={r[0]} lessons={r[1]} scenarios={r[2]} labs={r[3]}")
        except Exception as e:
            print(f"  ERROR: {e}")
            raise
