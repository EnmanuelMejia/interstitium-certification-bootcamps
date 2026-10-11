#!/usr/bin/env python3
"""Shared builder for full-stack CBT reconstruction."""
import json, copy

def L(domain_id, title, concepts, code, walkthrough, pitfalls, try_it, lang="text"):
    assert len(concepts) >= 4, f"lesson needs 4+ concepts: {title}"
    assert len(pitfalls) >= 3, f"lesson needs 3+ pitfalls: {title}"
    return {"title": title, "domain_id": domain_id, "concepts": concepts,
            "example": {"code": code, "lang": lang, "walkthrough": walkthrough},
            "pitfalls": pitfalls, "try_it": try_it}

def S(domain_id, sid, title, situation, prompt, choices, answer, why, hint, objectives, mins, evidence):
    assert len(choices) == 4, f"scenario needs 4 choices: {title}"
    assert 0 <= answer <= 3
    assert len(objectives) >= 2
    return {"id": sid, "title": title, "domain_id": domain_id, "situation": situation,
            "prompt": prompt, "choices": choices, "answer": answer, "why": why,
            "hint": hint, "objectives": objectives, "mins": mins, "evidence": evidence}

def LB(lid, title, objective, steps, checks, success_message):
    ck = [{"command_pattern": p, "expect_contains": e, "hint": h} for (p, e, h) in checks]
    return {"id": lid, "title": title, "objective": objective, "steps": steps,
            "checks": ck, "success_message": success_message}

def D(dom_id, name, description, lessons=None, scenarios=None, icon=None):
    d = {"id": dom_id, "name": name, "scenarios": scenarios or []}
    if description: d["description"] = description
    if icon: d["icon"] = icon
    # Stash lessons for the applier to move to top-level data["lessons"]
    if lessons: d["_lessons"] = lessons
    return d

# ---------- shared start-here (parameterized) ----------
def start_here_domain(course_name, exam_or_interview, first_domain_name):
    did = "start-here"
    lessons = [
        L(did, "How to Use This Bootcamp",
          ["The study order is deliberate — follow it top to bottom: each domain builds on the previous one, and later scenarios assume earlier knowledge",
           "Every lesson ends with a knowledge check: answer correctly and the lesson auto-completes. Wrong answers send you back to review — this is verification, not clicking through",
           "Scenarios are timed decision exercises with evidence to examine. Treat each like the real thing: read everything, decide, then commit",
           "Your progress saves automatically. Domains unlock as you complete prerequisites — the path guides you, but you set the pace"],
          "LEARN path: lessons -> scenarios -> labs -> drills\nTERMINAL: hands-on command practice\nMOCK: full timed assessment when ready\n\nSuggested daily loop:\n  1. Complete 2-3 lessons (with knowledge checks)\n  2. Work 3-5 scenarios in those domains\n  3. Run 1 lab end-to-end\n  4. 10 minutes of drills",
          "The bootcamp mirrors how professionals actually work: learn the concept, apply it under realistic conditions, then prove it in the lab. Skipping straight to the mock without the lessons is the fastest way to fail it.",
          ["Skipping lessons and jumping to scenarios — the scenarios assume lesson knowledge",
           "Treating the knowledge check as a formality instead of a real self-test",
           "Ignoring the terminal and labs — hands-on reps are where durable skill comes from"],
          "Open the Learn path and complete the first lesson's knowledge check to see auto-completion in action."),
        L(did, f"{exam_or_interview} Strategy: How to Win",
          [f"The {exam_or_interview} rewards applied understanding over memorization — every domain here maps to something you will actually be asked to do",
           "Time management wins: in timed assessments, bank the easy wins first, flag the hard ones, and never leave a question blank",
           "Wrong answers are data: each missed scenario reveals a specific gap. Log it, revisit the lesson, and re-attempt until the pattern clicks",
           f"Sleep and spacing beat cramming: 90-minute focused sessions with breaks outperform marathon sessions, especially the week before {exam_or_interview.lower()} day"],
          "The 3-pass method for timed assessments:\n  Pass 1 (40% of time): answer everything you know cold\n  Pass 2 (40% of time): work the flagged mediums with evidence\n  Pass 3 (20% of time): educated guesses on the rest\n\nNever spend 10 minutes on one question while five easy ones wait.",
          "Elimination is a skill: practice ruling out two wrong choices fast, then deciding between the final two. Most scenario questions are designed so two options are clearly wrong to a prepared candidate.",
          ["Changing answers without new evidence — your first instinct after study is usually right",
           "Perfectionism on one hard question while easy points expire",
           "Studying new material the night before instead of reviewing what you know"],
          f"Do one full timed mock this week using the 3-pass method, even before you feel ready. Baseline yourself."),
        L(did, "Course Map: What You Will Master",
          [f"This bootcamp has 15+ domains covering the full {course_name} landscape — from foundations to the capstone project",
           f"Core domains teach the must-know systems; the Systems Anatomy domain teaches you to see them as living, connected flows",
           "The capstone project proves you can build and operate a real system end-to-end — this is your interview story",
           f"The mock assessment simulates the real {exam_or_interview.lower()} so there are no surprises on the day"],
          f"{course_name} mastery map:\n  Foundations -> Core systems (domains 2-10)\n  -> Systems Anatomy (see it all connected)\n  -> Capstone (build it yourself)\n  -> Mock (prove it under pressure)",
          f"Start with: {first_domain_name}. It unlocks everything downstream — the path is sequential for a reason.",
          ["Treating all domains as equal — weight your time toward the heaviest-tested areas",
           "Skipping Systems Anatomy — it is the differentiator between passing and excelling",
           "Saving the capstone for 'later' — start it early, iterate as you learn"],
          "Skim the domain list in the Learn path and note which three domains matter most for your goal. Start there after Start Here."),
    ]
    scenarios = [
        S(did, "sh-navigate", "Navigate the Bootcamp",
          "You have 30 days before your assessment. You open the bootcamp and see 15 domains, a terminal, drills, and a mock. You feel overwhelmed.",
          "What is the highest-leverage first week plan?",
          ["Complete Start Here, then work the first three core domains in order — lessons with knowledge checks, then their scenarios, then one lab. Establish the daily loop before widening.",
           "Take the full mock on day one to 'see where you stand,' then study randomly.",
           "Read every lesson in all 15 domains first, then attempt scenarios in week three.",
           "Skip lessons entirely and grind drills — speed matters more than understanding."],
          0,
          "The correct approach is the structured loop: Start Here orients you, then sequential domains build the foundation scenarios assume. The mock on day one wastes your only baseline and demoralizes; random study leaves gaps the assessment will find. Drills without understanding produce fast wrong answers.",
          "Think about what the scenarios assume you already know.",
          ["Apply the deliberate study order", "Build a sustainable daily loop", "Avoid common preparation traps"], 10,
          [["Study calendar", "30 days available, ~2 hours per day on weekdays"]]),
        S(did, "sh-stuck", "When You Get Stuck",
          "You have failed the same scenario three times. The explanation makes sense when you read it, but you keep choosing wrong under time pressure.",
          "What should you do?",
          ["Drop back to the lesson: re-read the concepts, write out the decision process in your own words, then re-attempt the scenario untimed before going timed again.",
           "Keep re-attempting the scenario until you memorize the right answer.",
           "Skip it and move on — one scenario will not decide the assessment.",
           "Look up the answer online and move faster through the rest."],
          0,
          "The correct approach treats repeated failure as a signal: the mental model is broken, not the memory. Rebuilding from the lesson concepts — in your own words — repairs the model. Memorizing the answer passes one scenario and fails the next variation. The assessment tests patterns, not instances.",
          "Is the problem memory or the underlying mental model?",
          ["Diagnose repeated failure correctly", "Repair mental models from lesson concepts", "Use untimed practice deliberately"], 10,
          [["Attempt log", "Scenario failed 3x: same wrong choice twice, different wrong choice once"]]),
    ]
    return D(did, "Start Here: Ground Floor", f"Orientation, study strategy, and course map for {course_name}.", lessons, scenarios)

def mock_domain(course_name):
    return D("mock-assessment", "Full Mock Assessment",
             f"A complete timed simulation of the {course_name} assessment. Scenarios are drawn from every domain — hints disabled, every decision final.", [], [])

def capstone_domain(course_name, project_name, project_desc, build_steps):
    did = "capstone-build"
    lessons = [
        L(did, f"Capstone: {project_name} — Overview",
          [f"Your capstone: {project_desc}",
           "Break the build into phases: plan, build, secure, validate, document. Each phase maps to domains in this bootcamp",
           "Document as you go — your write-up is the interview artifact that proves senior-level ownership",
           "Done beats perfect: a working system with honest limitations beats an unfinished ambitious one"],
          "\n".join(f"Phase {i+1}: {s}" for i, s in enumerate(build_steps)),
          "Treat each phase as a mini-project with a definition of done. Demo each phase working before moving on — integration surprises compound.",
          ["Starting to build before writing the plan — an hour of planning saves ten of rework",
           "Skipping documentation until the end — you will forget why decisions were made",
           "Gold-plating phase one while phase four remains untouched"],
          "Write the one-paragraph project plan: what you will build, in what phases, and what 'done' looks like."),
        L(did, "Capstone: Validation and Demo",
          ["Validate every requirement with a test you can show: screenshots, command output, or a live demo",
           "Prepare the 5-minute demo narrative: problem, approach, build, validation, lessons learned",
           "Anticipate questions: know the trade-offs you made and what you would do with more time",
           "Publish the write-up: architecture diagram, build log, validation evidence, reflection"],
          "Demo script template:\n  1. The problem (30s)\n  2. Architecture overview (60s)\n  3. Live walkthrough (2 min)\n  4. Validation evidence (60s)\n  5. What I would do next (30s)",
          "A demo that only shows the happy path invites the hardest questions. Show one failure mode and how the system handles it — that is what interviewers remember.",
          ["Demoing without rehearsing — run it three times end-to-end first",
           "Hiding limitations — name them before you are asked",
           "No architecture diagram — draw the system before you demo it"],
          "Draft your 5-minute demo script for the capstone project."),
    ]
    scenarios = [
        S(did, "cap-plan", "Capstone Planning",
          f"You are about to start the {project_name} capstone. You have limited lab time and want maximum interview value.",
          "How do you scope the build?",
          ["Write the plan first: phases with definitions of done, mapped to bootcamp domains. Start with the smallest working core, then layer on complexity. Document decisions as you go.",
           "Start building immediately — planning wastes lab time.",
           "Attempt the most impressive architecture possible to stand out.",
           "Build whatever is easiest to finish quickly."],
          0,
          "The correct approach balances ambition with completion: a planned, phased build that finishes is worth more than an impressive unfinished one. Mapping phases to domains turns the capstone into applied review of the whole course.",
          "What does the interviewer actually evaluate in a project?",
          ["Scope a project realistically", "Phase work with definitions of done", "Connect build to course domains"], 15,
          [["Time budget", "20 hours of lab time available over two weeks"]]),
    ]
    return D(did, f"Capstone: {project_name}", f"Build a complete {project_desc} to prove mastery.", lessons, scenarios)
