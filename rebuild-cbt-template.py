#!/usr/bin/env python3
"""
Full-Stack CBT Rebuild Template
Rebuilds any CBT to the tl-infra-assessment-prep standard:
- 15+ domains (core + standard)
- 60+ lessons with concepts, examples, pitfalls, try_it
- 80+ scenarios with evidence, hints, objectives
- 20+ labs (hands-on)
- Standard domains: start-here, systems-anatomy, mock-assessment, capstone-build

Usage: python3 rebuild-cbt-template.py <cbt-id> [--dry-run]
"""

import json
import sys
from pathlib import Path

BOOTCAMPS_DIR = Path("/home/hatch/workspace/cert-bootcamps/site/bootcamps")
TEMPLATE_PATH = BOOTCAMPS_DIR / "tl-infra-assessment-prep" / "content.json"

# Load template for standard domain structures
with open(TEMPLATE_PATH) as f:
    TEMPLATE = json.load(f)

def get_template_domain(domain_id):
    """Get a standard domain structure from the template."""
    for d in TEMPLATE["domains"]:
        if d["id"] == domain_id:
            return d
    return None

def get_template_lessons(domain_id):
    """Get lessons for a domain from template."""
    return [l for l in TEMPLATE["lessons"] if l.get("domain_id") == domain_id]

# Standard domains every full-stack CBT should have
STANDARD_DOMAINS = ["start-here", "systems-anatomy", "mock-assessment", "capstone-build"]

def analyze_cbt(cbt_id):
    """Analyze a CBT's current state vs the full-stack standard."""
    cbt_path = BOOTCAMPS_DIR / cbt_id
    content_path = cbt_path / "content.json"
    
    if not content_path.exists():
        return None
    
    with open(content_path) as f:
        data = json.load(f)
    
    domains = data.get("domains", [])
    lessons = data.get("lessons", [])
    scenarios = sum(len(d.get("scenarios", [])) for d in domains)
    labs = len(data.get("labs", []))
    
    domain_ids = [d.get("id") for d in domains]
    missing_standard = [d for d in STANDARD_DOMAINS if d not in domain_ids]
    
    return {
        "id": cbt_id,
        "domains": len(domains),
        "lessons": len(lessons),
        "scenarios": scenarios,
        "labs": labs,
        "missing_standard": missing_standard,
        "domain_ids": domain_ids,
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 rebuild-cbt-template.py <cbt-id> [--dry-run]")
        print("   or: python3 rebuild-cbt-template.py --all --dry-run")
        sys.exit(1)
    
    dry_run = "--dry-run" in sys.argv
    
    if sys.argv[1] == "--all":
        # Analyze all CBTs
        results = []
        for cbt_dir in sorted(BOOTCAMPS_DIR.iterdir()):
            if not cbt_dir.is_dir() or cbt_dir.name.startswith("_"):
                continue
            analysis = analyze_cbt(cbt_dir.name)
            if analysis:
                results.append(analysis)
        
        # Sort by most incomplete first
        results.sort(key=lambda x: x["lessons"])
        
        print(f"\n{'CBT':<35} {'D':>3} {'L':>3} {'S':>3} {'Labs':>4}  Missing")
        print("-" * 80)
        for r in results:
            missing = ",".join(r["missing_standard"]) if r["missing_standard"] else "-"
            print(f"{r['id']:<35} {r['domains']:>3} {r['lessons']:>3} {r['scenarios']:>3} {r['labs']:>4}  {missing}")
        
        # Summary stats
        total_lessons = sum(r["lessons"] for r in results)
        total_scenarios = sum(r["scenarios"] for r in results)
        avg_lessons = total_lessons / len(results) if results else 0
        print(f"\nTotal CBTs: {len(results)}")
        print(f"Average lessons: {avg_lessons:.1f} (target: 60+)")
        print(f"CBTs below 30 lessons: {sum(1 for r in results if r['lessons'] < 30)}")
    else:
        cbt_id = sys.argv[1]
        analysis = analyze_cbt(cbt_id)
        if not analysis:
            print(f"CBT not found: {cbt_id}")
            sys.exit(1)
        print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
