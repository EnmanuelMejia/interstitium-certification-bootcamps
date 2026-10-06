"""Microsoft Fundamentals restructure (CBT-8 section 8): restructure ms-fundamentals.json
into four explicit exam tracks.

- domains -> az-900 / ai-900 / dp-900 / sc-900 (8 scenarios each, 32 total)
- 24 scenarios reused verbatim from the original file; 8 new original scenarios added
- lessons, behavioral, chat, labs, terminalMissions, simulations rewritten per-track
- accent "#00a4ef", simulation {"items":30,"minutes":45}
- sections + media lesson_refs updated to the new track ids
- slug/title/vendor/disclaimer/foundations/math/consoleSims/resources kept as-is

Run: python3 docs/restructure-ms-fundamentals.py
"""
import copy
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE, "content")
DOCS_DIR = os.path.join(BASE, "docs")
PATH = os.path.join(CONTENT_DIR, "ms-fundamentals.json")
NEW = os.path.join(DOCS_DIR, "ms-fundamentals-new-content.json")
BACKUP = os.path.join(DOCS_DIR, "backups", "ms-fundamentals.json.2026-10-06.bak")

TRACKS = [
    ("az-900", "AZ-900: Azure Fundamentals"),
    ("ai-900", "AI-900: Azure AI Fundamentals"),
    ("dp-900", "DP-900: Azure Data Fundamentals"),
    ("sc-900", "SC-900: Security, Compliance & Identity"),
]

SCENARIO_KEYS = {"id", "title", "situation", "prompt", "evidence", "choices",
                 "answer", "why", "objectives", "mins", "hint"}


def check_scenario(s):
    assert SCENARIO_KEYS <= set(s), f"scenario {s.get('id')} missing keys: {SCENARIO_KEYS - set(s)}"
    assert len(s["choices"]) == 4, f"scenario {s['id']} choices != 4"
    assert isinstance(s["answer"], int) and 0 <= s["answer"] < 4, f"scenario {s['id']} bad answer"
    assert isinstance(s["id"], str) and s["id"]


def main():
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    with open(PATH, encoding="utf-8") as f:
        original = f.read()
    d = json.loads(original)
    new = json.load(open(NEW, encoding="utf-8"))

    lookup = {}
    for dom in d["domains"]:
        for s in dom["scenarios"]:
            check_scenario(s)
            assert s["id"] not in lookup, f"duplicate scenario id {s['id']}"
            lookup[s["id"]] = s

    new_scenarios = new["new_scenarios"]
    for sid, s in new_scenarios.items():
        assert sid == s["id"], f"new scenario key/id mismatch: {sid}"
        check_scenario(s)

    # assemble the four tracks: 24 reused verbatim + 8 new = 32
    domains = []
    used = set()
    for track_id, track_name in TRACKS:
        ids = new["track_scenarios"][track_id]
        assert len(ids) == 8, f"{track_id}: {len(ids)} scenarios, need 8"
        scenarios = []
        for sid in ids:
            assert sid not in used, f"scenario {sid} used twice"
            used.add(sid)
            if sid in new_scenarios:
                scenarios.append(copy.deepcopy(new_scenarios[sid]))
            else:
                assert sid in lookup, f"unknown scenario id {sid}"
                scenarios.append(copy.deepcopy(lookup[sid]))
        domains.append({"id": track_id, "name": track_name, "scenarios": scenarios})
    d["domains"] = domains
    assert len(used) == 32

    # top-level fields
    d["accent"] = "#00a4ef"
    d["simulation"] = {"items": 30, "minutes": 45}
    d["tagline"] = "AZ-900 · AI-900 · DP-900 · SC-900 — four fundamentals tracks, one sweep"

    # rewritten blocks
    lessons = new["lessons"]
    assert [l["domain_id"] for l in lessons] == [t[0] for t in TRACKS], "one lesson per track required"
    for l in lessons:
        assert {"domain_id", "title", "concepts", "example", "pitfalls", "try_it"} <= set(l)
    d["lessons"] = lessons

    behavioral = new["behavioral"]
    assert len(behavioral) == 8, f"behavioral must be exactly 8, got {len(behavioral)}"
    for b in behavioral:
        assert {"prompt", "framework", "points", "pitfalls"} <= set(b)
    d["behavioral"] = behavioral

    chat = new["chat"]
    assert [t["id"] for t in chat["topics"]] == [t[0] for t in TRACKS], "chat topic ids must match domain ids"
    d["chat"] = chat

    labs = new["labs"]
    assert 4 <= len(labs) <= 6, f"labs must be 4-6, got {len(labs)}"
    d["labs"] = labs

    missions = new["terminalMissions"]
    assert 3 <= len(missions) <= 4, f"missions must be 3-4, got {len(missions)}"
    d["terminalMissions"] = missions

    sims = new["simulations"]
    assert 2 <= len(sims) <= 3, f"sims must be 2-3, got {len(sims)}"
    d["simulations"] = sims

    d["sections"] = new["sections"]

    # media lesson_refs -> new track ids
    ref_map = new["media_lesson_refs"]
    for m in d.get("media", []):
        old = m.get("lesson_ref")
        if old in ref_map:
            m["lesson_ref"] = ref_map[old]

    # safety: slug/title/vendor/disclaimer untouched
    before = json.loads(original)
    for k in ("slug", "title", "vendor", "disclaimer", "foundations", "math", "consoleSims", "resources"):
        assert d[k] == before[k], f"top-level key {k} was altered"
    assert d["slug"] == "ms-fundamentals" and d["title"] == "Microsoft Fundamentals"

    with open(BACKUP, "w", encoding="utf-8") as f:
        f.write(original)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=True)
        f.write("\n")

    # verify
    with open(PATH, encoding="utf-8") as f:
        v = json.load(f)
    print("OK - parses")
    print("accent:", v["accent"], "| simulation:", v["simulation"])
    print("domains:", [(dom["id"], len(dom["scenarios"])) for dom in v["domains"]])
    print("lessons:", len(v["lessons"]), "| behavioral:", len(v["behavioral"]),
          "| labs:", len(v["labs"]), "| missions:", len(v["terminalMissions"]),
          "| sims:", len(v["simulations"]), "| foundations:", len(v["foundations"]))
    print("chat topics:", [t["id"] for t in v["chat"]["topics"]])
    print("disclaimer:", v["disclaimer"])
    print("file size:", os.path.getsize(PATH), "bytes")
    print("backup:", BACKUP)


if __name__ == "__main__":
    main()
