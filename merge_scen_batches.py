#!/usr/bin/env python3
"""Merge scen_batchA/B/C/D/E.py into the 10 CBT content.json files."""
import json, sys, importlib.util

BASE = '/home/hatch/workspace/cert-bootcamps/site/bootcamps'
BATCH_FILES = ['scen_batchA.py', 'scen_batchB.py', 'scen_batchC.py',
               'scen_batchD.py', 'scen_batchE.py']

# Batch E subagent used wrong domain IDs for daml/dsc (brief had an error).
# Remap to the actual domain IDs in content.json.
DOMAIN_REMAP = {
    "data-analyst-to-ml": {
        "ml-python": "data-analyst-to-ml",
        "ml-algorithms": "ml-foundations",
        "hands-on-labs": "ml-systems",
    },
    "data-science-certs": {
        "ds-certs": "data-science-certs",
    },
}

def remap(cbt, did):
    return DOMAIN_REMAP.get(cbt, {}).get(did, did)

SCEN_REQ = {"id", "title", "domain_id", "situation", "prompt", "choices",
            "answer", "why", "hint", "objectives", "mins", "evidence"}
LESSON_REQ = {"_id", "id", "title", "domain_id", "concepts", "example",
              "pitfalls", "try_it"}
LAB_REQ = {"_id", "id", "title", "domain_id", "objective", "steps",
           "checks", "debrief"}

def load_batch(fname):
    spec = importlib.util.spec_from_file_location(fname[:-3],
        f'/home/hatch/workspace/cert-bootcamps/{fname}')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def main():
    merged_scen, merged_lessons, merged_labs = {}, {}, {}
    for fname in BATCH_FILES:
        try:
            m = load_batch(fname)
        except FileNotFoundError:
            print(f"SKIP {fname} (not yet delivered)")
            continue
        # SCENARIOS may be {cbt: {domain: [sc,...]}} or {cbt: {scen_id: scen}} (id-keyed)
        for cbt, domains in getattr(m, 'SCENARIOS', {}).items():
            merged_scen.setdefault(cbt, {})
            for key, val in domains.items():
                if isinstance(val, dict) and 'domain_id' in val:
                    # id-keyed: group by (remapped) domain_id
                    did = remap(cbt, val['domain_id'])
                    val['domain_id'] = did
                    merged_scen[cbt].setdefault(did, []).append(val)
                else:
                    did = remap(cbt, key)
                    for sc in val:
                        sc['domain_id'] = did
                    merged_scen[cbt].setdefault(did, []).extend(val)
        # LESSONS likewise
        for cbt, domains in getattr(m, 'LESSONS', {}).items():
            merged_lessons.setdefault(cbt, {})
            for key, val in domains.items():
                if isinstance(val, dict) and 'domain_id' in val:
                    did = remap(cbt, val['domain_id'])
                    val['domain_id'] = did
                    merged_lessons[cbt].setdefault(did, []).append(val)
                else:
                    did = remap(cbt, key)
                    for l in val:
                        l['domain_id'] = did
                    merged_lessons[cbt].setdefault(did, []).extend(val)
        for cbt, labs in getattr(m, 'LABS', {}).items():
            for lab in labs:
                lab['domain_id'] = remap(cbt, lab['domain_id'])
            merged_labs.setdefault(cbt, []).extend(labs)
        print(f"loaded {fname}")

    # validate merged content
    for cbt, domains in merged_scen.items():
        for did, scs in domains.items():
            for sc in scs:
                missing = SCEN_REQ - set(sc.keys())
                assert not missing, f"{fname}: scenario {sc.get('id')} missing {missing}"
                assert len(sc['choices']) == 4
                assert 0 <= sc['answer'] < 4
    for cbt, domains in merged_lessons.items():
        for did, ls in domains.items():
            for l in ls:
                missing = LESSON_REQ - set(l.keys())
                assert not missing, f"lesson {l.get('id')} missing {missing}"
                assert len(l['concepts']) >= 4 and len(l['pitfalls']) >= 3
    for cbt, labs in merged_labs.items():
        for lab in labs:
            missing = LAB_REQ - set(lab.keys())
            assert not missing, f"lab {lab.get('id')} missing {missing}"
    print("all merged content validates")

    results = []
    for cbt in sorted(set(list(merged_scen.keys()) + list(merged_lessons.keys()) + list(merged_labs.keys()))):
        path = f"{BASE}/{cbt}/content.json"
        with open(path) as f:
            data = json.load(f)
        before = (len(data['domains']), len(data['lessons']),
                  sum(len(d.get('scenarios', [])) for d in data['domains']),
                  len(data['labs']))
        domain_ids = {d['id'] for d in data['domains']}
        lesson_ids = {l.get('_id') for l in data['lessons']}
        lab_ids = {l.get('_id') for l in data['labs']}

        # scenarios
        for did, scs in merged_scen.get(cbt, {}).items():
            assert did in domain_ids, f"{cbt}: unknown domain {did}"
            dom = next(d for d in data['domains'] if d['id'] == did)
            existing = {s.get('id') or s.get('_id') for s in dom.get('scenarios', [])}
            for sc in scs:
                sid = sc.get('id') or sc.get('_id')
                if sid not in existing:
                    dom.setdefault('scenarios', []).append(sc)
                    existing.add(sid)

        # lessons
        for did, ls in merged_lessons.get(cbt, {}).items():
            assert did in domain_ids, f"{cbt}: unknown domain {did}"
            for l in ls:
                if l['_id'] not in lesson_ids:
                    l['domain_id'] = did
                    data['lessons'].append(l)
                    lesson_ids.add(l['_id'])

        # labs
        for lab in merged_labs.get(cbt, []):
            assert lab['domain_id'] in domain_ids, f"{cbt}: unknown lab domain {lab['domain_id']}"
            if lab['_id'] not in lab_ids:
                data['labs'].append(lab)
                lab_ids.add(lab['_id'])

        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        with open(path) as f:
            json.load(f)  # re-validate from disk
        after = (len(data['domains']), len(data['lessons']),
                 sum(len(d.get('scenarios', [])) for d in data['domains']),
                 len(data['labs']))
        results.append((cbt, before, after))

    print(f"\n{'CBT':22s} {'domains':>8s} {'lessons':>8s} {'scenarios':>10s} {'labs':>6s}")
    all_ok = True
    for cbt, b, a in results:
        ok = a[0] >= 15 and a[1] >= 60 and a[2] >= 80 and a[3] >= 20
        all_ok = all_ok and ok
        flag = "" if ok else "  <-- BELOW TARGET"
        print(f"{cbt:22s} {b[0]:>3d}->{a[0]:<4d} {b[1]:>3d}->{a[1]:<4d} {b[2]:>3d}->{a[2]:<5d} {b[3]:>3d}->{a[3]:<4d}{flag}")
    print("\nALL TARGETS MET" if all_ok else "\nSOME BELOW TARGET — review flags above")

if __name__ == '__main__':
    main()
