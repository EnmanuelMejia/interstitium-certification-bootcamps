#!/usr/bin/env python3
"""Assemble the top-level "sections" array for every content/<slug>.json.

Learning path per bootcamp (KodeKloud-style, zero-knowledge assumption):

    Foundations -> Core -> Advanced -> Exam Prep

Section shape:
    {"id","title","kind","lectures","lab_ids","drill_domain_ids"}
    kind is one of: foundation | core | advanced | exam-prep
    lectures entries are lecture ids:
        m-<math_id>      -> expands to ALL lectures of math module <math_id>
        f-<track>-<i>    -> foundations track <track>, lecture index <i>
        c-<domain_id>    -> core/advanced lecture built from the domain's lesson

Foundation track lecture counts come from generator/foundation-tracks.json
(workstream E's source of truth). If that file is absent, the foundation
section is emitted with lectures: [] and a warning (the coordinator re-runs
this script after E lands) — never a crash.

Usage:
    python3 generator/gen_sections.py [--content-dir DIR] [--limit N]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
TRACKS_PATH = ROOT / "generator" / "foundation-tracks.json"

ADV_RE = re.compile(
    r"advanced|security|hardening|tuning|optim|threat|governance|"
    r"compliance|architecture|design",
    re.IGNORECASE,
)


def foundation_lectures(data):
    """m-<id> refs from content.json + f-<track>-<i> from foundation-tracks.json."""
    lectures = []
    math_refs = data.get("math") or []
    if isinstance(math_refs, dict):
        math_refs = math_refs.get("modules", []) or math_refs.get("ids", [])
    for m in math_refs:
        mid = m.get("id") if isinstance(m, dict) else m
        if mid:
            lectures.append("m-%s" % mid)
    try:
        with open(TRACKS_PATH, encoding="utf-8") as f:
            tracks_data = json.load(f)
    except FileNotFoundError:
        print("  WARN: %s absent — foundation track lectures left empty" % TRACKS_PATH.name)
        return lectures
    except json.JSONDecodeError as e:
        print("  WARN: %s invalid JSON (%s) — foundation track lectures left empty"
              % (TRACKS_PATH.name, e))
        return lectures
    tracks = tracks_data.get("tracks", tracks_data)
    if isinstance(tracks, dict):
        track_map = dict(tracks.items())
    elif isinstance(tracks, list):
        track_map = {}
        for i, t in enumerate(tracks):
            tid = (t.get("id") if isinstance(t, dict) else None) or str(i)
            track_map[tid] = t
    else:
        track_map = {}
    # Only the tracks assigned to THIS bootcamp (data["foundations"]).
    assigned = []
    for f in data.get("foundations") or []:
        tid = f.get("track") if isinstance(f, dict) else f
        if tid and tid not in assigned:
            assigned.append(tid)
    for tid in assigned:
        t = track_map.get(tid)
        if not isinstance(t, dict):
            print("  WARN: foundation track '%s' not in %s" % (tid, TRACKS_PATH.name))
            continue
        for i in range(len(t.get("lectures", []))):
            lectures.append("f-%s-%d" % (tid, i))
    return lectures


def split_core_advanced(domains):
    """Heuristic split; falls back to 60/40 when the heuristic finds nothing."""
    core, adv = [], []
    for d in domains:
        blob = "%s %s" % (d.get("id", ""), d.get("name", ""))
        (adv if ADV_RE.search(blob) else core).append(d)
    if not adv and len(domains) > 1:
        cut = max(1, int(len(domains) * 0.6))
        core, adv = domains[:cut], domains[cut:]
    return core, adv


def section(sec_id, title, kind, lectures, lab_ids, drill_domain_ids):
    return {
        "id": sec_id,
        "title": title,
        "kind": kind,
        "lectures": lectures,
        "lab_ids": lab_ids,
        "drill_domain_ids": drill_domain_ids,
    }


def process_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    domains = data.get("domains") or []
    domain_ids = [d.get("id") for d in domains if d.get("id")]
    labs = data.get("labs") or []
    lab_ids = [lb.get("id") for lb in labs if isinstance(lb, dict) and lb.get("id")]

    core_domains, adv_domains = split_core_advanced(domains)
    core_ids = [d.get("id") for d in core_domains if d.get("id")]
    adv_ids = [d.get("id") for d in adv_domains if d.get("id")]

    split = (len(lab_ids) + 1) // 2  # first half (rounded up) -> core
    sections = [
        section("foundations", "Foundations", "foundation",
                foundation_lectures(data), [], []),
        section("core", "Core", "core",
                ["c-%s" % i for i in core_ids], lab_ids[:split], core_ids),
        section("advanced", "Advanced", "advanced",
                ["c-%s" % i for i in adv_ids], lab_ids[split:], adv_ids),
        section("exam-prep", "Exam Prep", "exam-prep",
                [], [], list(domain_ids)),
    ]

    out = {}
    inserted = False
    anchor = "lessons" if "lessons" in data else "domains"
    for k, v in data.items():
        if k == "sections":
            continue  # replaced below; never carry the stale value forward
        out[k] = v
        if k == anchor and not inserted:
            out["sections"] = sections
            inserted = True
    if not inserted:
        out["sections"] = sections
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    summ = " | ".join(
        "%s: %d lec / %d labs / %d drill" % (s["id"], len(s["lectures"]),
                                            len(s["lab_ids"]), len(s["drill_domain_ids"]))
        for s in sections
    )
    return summ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content-dir", default=None)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    content_dir = Path(args.content_dir) if args.content_dir else CONTENT_DIR
    files = sorted(content_dir.glob("*.json"))
    if args.limit:
        files = files[:args.limit]
    for path in files:
        try:
            print("%s: %s" % (path.stem, process_file(path)))
        except Exception as e:
            print("%s: ERROR %s" % (path.stem, e), file=sys.stderr)


if __name__ == "__main__":
    main()
