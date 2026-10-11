#!/usr/bin/env python3
"""Schema validator for cert-bootcamp content.json files (unified shell project).

Checks (per docs/content-schema.md + task spec):
  1. Valid JSON (no parse errors)
  2. Required top-level keys: slug, title, domains, lessons
  3. domains: each has id, name; each scenario has id
  4. lessons: each lesson's domain_id matches an existing domain id (no dangling refs)
  5. No duplicate IDs within domains / scenarios / lessons / labs / simulations
  6. labs: each has id, title

Usage:
  python3 validate-content.py [--root DIR] [--report PATH]
Default root: ~/workspace/cert-bootcamps/site/bootcamps
Exits 0 if all files valid, 1 otherwise.
"""
import argparse
import json
import os
import sys
from collections import Counter

REQUIRED_TOP_KEYS = ["slug", "title", "domains", "lessons"]


def check_bootcamp(path):
    """Return list of error strings for one content.json. Empty = valid."""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"]
    except OSError as e:
        return [f"cannot read file: {e}"]
    except UnicodeDecodeError as e:
        return [f"encoding error (not valid UTF-8): {e}"]

    if not isinstance(data, dict):
        return ["top level is not a JSON object"]

    # --- 2. required top-level keys -------------------------------------
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            errors.append(f"missing required top-level key: '{key}'")

    # --- 3. domains ------------------------------------------------------
    domains = data.get("domains")
    domain_ids = set()
    domain_dupes = Counter()
    scenario_ids = Counter()
    if isinstance(domains, list):
        for i, dom in enumerate(domains):
            where = f"domains[{i}]"
            if not isinstance(dom, dict):
                errors.append(f"{where}: not an object")
                continue
            did = dom.get("id")
            if not did:
                errors.append(f"{where}: missing 'id'")
            else:
                domain_dupes[did] += 1
                domain_ids.add(did)
            if not dom.get("name"):
                errors.append(f"{where}: missing 'name' (id={did!r})")
            scenarios = dom.get("scenarios", [])
            if not isinstance(scenarios, list):
                errors.append(f"{where}: 'scenarios' is not a list")
                continue
            for j, sc in enumerate(scenarios):
                sw = f"{where}.scenarios[{j}]"
                if not isinstance(sc, dict):
                    errors.append(f"{sw}: not an object")
                    continue
                sid = sc.get("id")
                if not sid:
                    errors.append(f"{sw}: missing 'id'")
                else:
                    scenario_ids[sid] += 1
        for dup, n in sorted(domain_dupes.items()):
            if n > 1:
                errors.append(f"duplicate domain id: {dup!r} ({n} occurrences)")
        for dup, n in sorted(scenario_ids.items()):
            if n > 1:
                errors.append(f"duplicate scenario id: {dup!r} ({n} occurrences)")
    elif "domains" in data:
        errors.append("'domains' is not a list")

    # --- 4. lessons (dangling domain_id refs) + lesson id dupes -----------
    lessons = data.get("lessons")
    if isinstance(lessons, list):
        lesson_ids = Counter()
        for i, lesson in enumerate(lessons):
            where = f"lessons[{i}]"
            if not isinstance(lesson, dict):
                errors.append(f"{where}: not an object")
                continue
            dom_id = lesson.get("domain_id")
            if not dom_id:
                errors.append(f"{where}: missing 'domain_id' (title={lesson.get('title')!r})")
            elif dom_id not in domain_ids:
                errors.append(
                    f"{where}: dangling domain_id {dom_id!r} "
                    f"(no matching domain; title={lesson.get('title')!r})"
                )
            if lesson.get("id") is not None:
                lesson_ids[lesson["id"]] += 1
        for dup, n in sorted(lesson_ids.items()):
            if n > 1:
                errors.append(f"duplicate lesson id: {dup!r} ({n} occurrences)")
    elif "lessons" in data:
        errors.append("'lessons' is not a list")

    # --- 6. labs: each has id, title; no duplicate ids -------------------
    labs = data.get("labs")
    if isinstance(labs, list):
        lab_ids = Counter()
        for i, lab in enumerate(labs):
            where = f"labs[{i}]"
            if not isinstance(lab, dict):
                errors.append(f"{where}: not an object")
                continue
            lid = lab.get("id")
            if not lid:
                errors.append(f"{where}: missing 'id'")
            else:
                lab_ids[lid] += 1
            if not lab.get("title"):
                errors.append(f"{where}: missing 'title' (id={lid!r})")
        for dup, n in sorted(lab_ids.items()):
            if n > 1:
                errors.append(f"duplicate lab id: {dup!r} ({n} occurrences)")
    elif labs is not None:
        errors.append("'labs' is not a list")

    # --- 5b. simulations: no duplicate ids (when present as a list) ------
    sims = data.get("simulations")
    if isinstance(sims, list):
        sim_ids = Counter()
        for i, sim in enumerate(sims):
            where = f"simulations[{i}]"
            if not isinstance(sim, dict):
                errors.append(f"{where}: not an object")
                continue
            sid = sim.get("id")
            if sid is not None:
                sim_ids[sid] += 1
        for dup, n in sorted(sim_ids.items()):
            if n > 1:
                errors.append(f"duplicate simulation id: {dup!r} ({n} occurrences)")
    elif sims is not None:
        errors.append("'simulations' is not a list")

    return errors


def main():
    ap = argparse.ArgumentParser(description="Validate cert-bootcamp content.json files")
    ap.add_argument("--root", default=os.path.expanduser(
        "~/workspace/cert-bootcamps/site/bootcamps"),
        help="bootcamps directory (default: ~/workspace/cert-bootcamps/site/bootcamps)")
    ap.add_argument("--report", default=None,
                    help="optional path to write JSON report")
    args = ap.parse_args()

    results = {}
    slugs = sorted(
        d for d in os.listdir(args.root)
        if os.path.isdir(os.path.join(args.root, d))
        and os.path.isfile(os.path.join(args.root, d, "content.json"))
    )
    for slug in slugs:
        path = os.path.join(args.root, slug, "content.json")
        results[slug] = check_bootcamp(path)

    total = len(results)
    failed = {s: e for s, e in results.items() if e}

    print(f"Validated {total} content.json files: {total - len(failed)} PASS, {len(failed)} FAIL")
    print()
    for slug in sorted(failed):
        print(f"FAIL  {slug}")
        for err in failed[slug]:
            print(f"      - {err}")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(
                {"total": total, "passed": total - len(failed),
                 "results": results},
                f, indent=2, ensure_ascii=False,
            )
        print(f"\nJSON report written to {args.report}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
