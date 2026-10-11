#!/usr/bin/env python3
"""
Add Systems Anatomy domain to all CBTs sitewide.
Based on the interactive 3D visualization pattern:
"A textbook diagram shows you one part. This shows you how all of it moves together."

For each CBT, generates a systems-anatomy domain tailored to its top domains.
"""

import json
import os
import sys
from pathlib import Path

BOOTCAMPS_DIR = Path("/home/hatch/workspace/cert-bootcamps/site/bootcamps")

# Generic lesson 1 - adaptable to any course
def lesson_living_systems(course_name):
    return {
        "title": "From Static Diagrams to Living Systems",
        "domain_id": "systems-anatomy",
        "concepts": [
            f"A textbook diagram shows you one part in isolation — a living systems view shows you how all parts of {course_name} move together in sequence",
            "The four-step systems anatomy method: (1) See the whole in context, (2) Cut it open to reveal layers, (3) Walk through the process step-by-step, (4) Pull apart into labeled pieces",
            "Apply this to any system in this course: start with the trigger action, trace through every component it touches, watch the data flow",
            "Interview/exam power: when asked 'how does X work?', narrate the journey — 'it starts here, then...'. This demonstrates senior-level systems thinking"
        ],
        "example": {
            "lang": "text",
            "code": "TRIGGER event occurs\n  → First system receives it (see the handoff)\n  → Processing happens in sequence (watch each step)\n  → State changes propagate (follow the ripple)\n  → Final outcome delivered\n\nEach arrow is a living handoff, not a static box.",
            "walkthrough": "This is the 'jet engine cutaway' for your field: instead of memorizing isolated facts, you see the entire flow as a moving sequence. Practice narrating this journey out loud."
        },
        "pitfalls": [
            "Memorizing terms without understanding the processes they participate in",
            "Drawing architecture diagrams as boxes without showing the data flow between them",
            "Answering 'how does X work?' with a definition instead of walking through the sequence"
        ],
        "try_it": "Pick any process in this course. Write out the full journey from trigger to outcome, naming every system touched."
    }

def lesson_system_anatomy(system_name, domain_name):
    """Generate an anatomy lesson for a specific system."""
    return {
        "title": f"Anatomy of {system_name}",
        "domain_id": "systems-anatomy",
        "concepts": [
            f"{system_name} is a multi-step process within {domain_name}: trace the full sequence from initiation to completion",
            f"See it as a journey: identify the trigger, follow each handoff, watch state change at every step",
            f"Every step depends on the previous — a failure at any point breaks the chain. Map these dependencies",
            f"Connect {system_name} to the broader {domain_name} ecosystem — nothing operates in isolation"
        ],
        "example": {
            "lang": "text",
            "code": f"Step 1: Initiation\n  {system_name} begins — what triggers it?\n\nStep 2: Processing\n  Data flows through — what transforms it?\n\nStep 3: Handoff\n  Result passes to next system — what is the interface?\n\nStep 4: Completion\n  Final state reached — how do you verify?",
            "walkthrough": f"Apply the four-step anatomy method to {system_name}. Draw it as a flowing sequence, not a static diagram."
        },
        "pitfalls": [
            f"Treating {system_name} as an isolated component instead of part of a living flow",
            "Skipping the dependency mapping — not asking 'what does this step need from the previous?'",
            "Memorizing the steps without understanding WHY each one exists"
        ],
        "try_it": f"Whiteboard the full {system_name} flow from memory. Label every handoff and dependency."
    }

def scenario_systems_thinking(course_name, system_name):
    """Generate a systems-thinking troubleshooting scenario."""
    return {
        "id": f"sysanat-{system_name.lower().replace(' ', '-').replace('&', 'and')[:30]}",
        "title": f"The {system_name} Mystery",
        "domain_id": "systems-anatomy",
        "situation": f"Users report that {system_name} is not working correctly. The obvious checks pass — the components are online, basic connectivity works. You need to think in systems, not symptoms.",
        "prompt": f"Using the systems anatomy method (whole → cut open → step through → pull apart), how would you systematically trace a failure in {system_name}?",
        "choices": [
            f"Walk the full journey: start from the trigger, verify each handoff in sequence, check dependencies at every step, and isolate where the flow breaks — then examine that specific layer",
            f"Restart all components — {system_name} issues are always fixed by restarting",
            f"Check the most common cause from memory and apply that fix immediately",
            f"Escalate to senior support — {system_name} is too complex to troubleshoot systematically"
        ],
        "answer": 0,
        "why": f"The correct answer is A. Systems thinking means tracing the living flow: (1) Whole: what is {system_name} supposed to do end-to-end? (2) Cut open: what are the layers/stages? (3) Step through: verify each handoff — where does the expected output diverge from actual? (4) Pull apart: isolate the broken layer and examine it in detail. This method works for any {system_name} failure in {course_name}.",
        "hint": "Don't jump to the fix. First map the journey, then find where it breaks.",
        "objectives": [f"Apply systems anatomy to {system_name}", "Trace failures through layered dependencies", "Distinguish symptoms from root causes"],
        "mins": 15,
        "evidence": [
            ["System Status", f"All {system_name} components report 'online'. Basic health checks pass."],
            ["User Report", "Functionality is broken despite green status indicators. The failure is in the flow, not the components."]
        ]
    }

def process_cbt(cbt_path):
    """Add systems-anatomy domain to a single CBT."""
    content_path = cbt_path / "content.json"
    if not content_path.exists():
        return None, "no content.json"
    
    try:
        with open(content_path) as f:
            data = json.load(f)
    except Exception as e:
        return None, f"JSON error: {e}"
    
    # Skip if already has systems-anatomy
    domain_ids = [d.get("id") for d in data.get("domains", [])]
    if "systems-anatomy" in domain_ids:
        return None, "already has systems-anatomy"
    
    # Get course name
    course_name = cbt_path.name.replace("-", " ").title()
    
    # Get top domains by content volume (lessons + scenarios)
    domains = data.get("domains", [])
    if not domains:
        return None, "no domains"
    
    # Score domains by content
    scored = []
    for d in domains:
        score = len(d.get("lessons", [])) + len(d.get("scenarios", [])) * 2
        # Also check top-level lessons/scenarios arrays filtered by domain
        scored.append((score, d))
    scored.sort(reverse=True, key=lambda x: x[0])
    
    # Take top 2-3 domains for anatomy lessons
    top_domains = scored[:3]
    
    lessons = [lesson_living_systems(course_name)]
    for score, d in top_domains:
        sys_name = d.get("name", d.get("id", "System"))
        lessons.append(lesson_system_anatomy(sys_name, sys_name))
    
    scenarios = []
    for score, d in top_domains[:2]:
        sys_name = d.get("name", d.get("id", "System"))
        scenarios.append(scenario_systems_thinking(course_name, sys_name))
    
    systems_domain = {
        "id": "systems-anatomy",
        "name": "Systems Anatomy: Seeing Systems as Living Flows",
        "description": f"Learn to see {course_name} as living systems — not static diagrams, but moving sequences where every part connects. Master systems thinking for exams and interviews.",
        "icon": "🔬",
        "lessons": [],
        "scenarios": scenarios
    }
    
    # Add domain
    data["domains"].append(systems_domain)
    
    # Add lessons to top-level lessons array
    if "lessons" not in data:
        data["lessons"] = []
    for lesson in lessons:
        data["lessons"].append(lesson)
    
    # Write back
    with open(content_path, "w") as f:
        json.dump(data, f, indent=2)
    
    return True, f"added {len(lessons)} lessons, {len(scenarios)} scenarios"

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        dry_run = True
    else:
        dry_run = False
    
    results = {"added": 0, "skipped": 0, "errors": 0}
    details = []
    
    for cbt_dir in sorted(BOOTCAMPS_DIR.iterdir()):
        if not cbt_dir.is_dir() or cbt_dir.name.startswith("_"):
            continue
        
        if dry_run:
            content_path = cbt_dir / "content.json"
            if content_path.exists():
                try:
                    with open(content_path) as f:
                        data = json.load(f)
                    has_it = "systems-anatomy" in [d.get("id") for d in data.get("domains", [])]
                    details.append(f"{cbt_dir.name}: {'SKIP (has it)' if has_it else 'WOULD ADD'}")
                    if has_it:
                        results["skipped"] += 1
                except:
                    details.append(f"{cbt_dir.name}: ERROR reading")
                    results["errors"] += 1
        else:
            success, msg = process_cbt(cbt_dir)
            if success:
                results["added"] += 1
                details.append(f"{cbt_dir.name}: {msg}")
            elif "already has" in msg:
                results["skipped"] += 1
            else:
                results["errors"] += 1
                details.append(f"{cbt_dir.name}: {msg}")
    
    print(f"\n{'DRY RUN' if dry_run else 'RESULTS'}:")
    print(f"  Added: {results['added']}")
    print(f"  Skipped: {results['skipped']}")
    print(f"  Errors: {results['errors']}")
    
    if results["errors"] > 0 or dry_run:
        print("\nDetails:")
        for d in details[:50]:
            print(f"  {d}")

if __name__ == "__main__":
    main()
