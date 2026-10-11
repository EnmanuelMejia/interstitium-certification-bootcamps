"""Shared helpers for rebuilding CBTs to full-stack standard."""
import json, copy

def L(title, domain_id, concepts, code, walkthrough, pitfalls, try_it, lang="text"):
    assert len(concepts) >= 4, f"lesson needs 4+ concepts: {title}"
    pitfalls = list(pitfalls)
    while len(pitfalls) < 3:
        pitfalls.append("Skimming without self-testing — cover the concepts above and recall each aloud before moving on.")
    return {
        "title": title,
        "domain_id": domain_id,
        "concepts": concepts,
        "example": {"code": code, "lang": lang, "walkthrough": walkthrough},
        "pitfalls": pitfalls,
        "try_it": try_it,
    }

def S(sid, title, domain_id, situation, prompt, choices, answer, why, hint, objectives, mins, evidence):
    assert len(choices) == 4, f"scenario needs 4 choices: {title}"
    assert 0 <= answer <= 3
    assert len(objectives) >= 1
    ev = []
    for e in evidence:
        if isinstance(e, (list, tuple)):
            ev.append([e[0], e[1]])
        else:
            ev.append(e)
    return {
        "id": sid, "title": title, "domain_id": domain_id,
        "situation": situation, "prompt": prompt, "choices": choices,
        "answer": answer, "why": why, "hint": hint,
        "objectives": objectives, "mins": mins, "evidence": ev,
    }

def LAB(lid, title, objective, steps, domain_id=None):
    lab = {"id": lid, "title": title, "objective": objective, "steps": steps}
    if domain_id:
        lab["domain_id"] = domain_id
    return lab

def start_here_domain(course_title, course_blurb, study_order, first_action):
    """Returns (domain_dict, lessons_list)."""
    did = "start-here"
    lessons = [
        L(f"How to Use This Bootcamp: {course_title}",
          did,
          [f"This bootcamp is organized as a guided path: Start Here → domains in order → scenarios → labs → mock assessment. Follow the sequence; each domain unlocks the next at 80% completion.",
           f"Lessons teach concepts with worked examples. Scenarios test application under realistic conditions. Labs give hands-on reps. The mock assessment simulates the real thing under time pressure.",
           "The study order is deliberate: " + study_order,
           "Track your progress on the dashboard. Revisit weak domains — spaced repetition beats cramming. Aim for mastery (correct streaks), not just completion."],
          "STUDY LOOP (repeat per domain):\n  1. Read the lessons — take notes in your own words\n  2. Run the scenarios — explain your reasoning before submitting\n  3. Do the labs — hands-on reps lock in muscle memory\n  4. Check the dashboard — below 80%? Loop again before moving on",
          f"Work one domain at a time. {course_blurb} Finish every domain, then take the mock assessment under timed conditions.",
          ["Skipping ahead to the mock before finishing domains — the mock measures readiness, it does not build it.",
           "Reading passively without doing scenarios and labs — recognition is not recall.",
           "Ignoring the dashboard — weak domains compound; fix them early."],
          first_action),
        L("Study Strategy: How to Master This Material",
          did,
          ["Active recall beats re-reading: after each lesson, close the page and explain the key ideas aloud in your own words.",
           "Interleaving beats blocking: mix scenarios from different domains in one session to build discrimination skill.",
           "Spaced repetition beats cramming: revisit completed domains after 1 day, 3 days, and 7 days.",
           "Teach-back is the mastery test: if you can whiteboard a concept for a colleague, you own it."],
          "WEEKLY CADENCE:\n  Mon–Fri: 1 domain per day (lessons + scenarios + labs)\n  Saturday: mixed scenario review across all completed domains\n  Sunday: rest or light flashcard review\n  Repeat until dashboard shows 80%+ everywhere, then mock.",
          "Consistency compounds. Ninety focused minutes daily beats a ten-hour weekend binge — your brain consolidates during sleep, so daily touchpoints win.",
          ["Cramming the night before — short-term memory evaporates under pressure.",
           "Only doing what is comfortable — growth lives in the scenarios you get wrong.",
           "No notes — writing forces encoding; highlight-only reading does not."],
          "Right now: create a study log (paper or digital). After each session write 3 things learned and 1 thing still fuzzy."),
        L("Course Map: What You Will Learn",
          did,
          [f"This bootcamp covers the full scope of {course_title}, from foundations to advanced application.",
           "Each domain is a vertical slice: concepts, worked examples, pitfalls, hands-on practice, and scenario assessments.",
           "The capstone domain guides you to build a real project that proves your skills to employers or examiners.",
           "The mock assessment pulls scenarios from every domain under timed conditions — your final readiness gate."],
          "DOMAIN MAP:\n" + study_order + "\n  → systems-anatomy: see every system as a living flow\n  → capstone-build: prove it with a real project\n  → mock-assessment: timed final validation",
          "Skim the Learn page now to see the full domain list. Notice the progression from foundations to advanced topics — that is your path.",
          ["Treating all domains as equal — foundations deserve more reps; advanced topics build on them.",
           "Skipping systems-anatomy — it teaches the thinking skill that makes every other domain easier.",
           "Skipping the capstone — projects turn knowledge into proof employers trust."],
          "Open the Learn page and read every domain name and description. Write down the three you are weakest in — those get extra sessions."),
        L("How You Will Be Assessed",
          did,
          ["Scenarios are the core assessment: realistic situations with four options, hints, evidence panels, and detailed explanations.",
           "Knowledge checks verify lesson comprehension — answer correctly and the lesson auto-completes. No empty clicking.",
           "Labs are hands-on: follow the steps, run the commands, verify the outcome. Muscle memory matters.",
           "The mock assessment is timed and draws from all domains. Hints are disabled. Treat it like the real exam or interview."],
          "SCORING MENTAL MODEL:\n  Scenario correct, no hint  → mastery signal\n  Scenario correct, hint used → understood with support; revisit\n  Scenario wrong              → read the 'why', redo the lesson, retry tomorrow",
          "Use every wrong answer as a diagnostic. The explanation tells you exactly which concept to revisit — follow that thread immediately.",
          ["Rushing scenarios to inflate completion — the dashboard measures streaks, not clicks.",
           "Ignoring hints when stuck — a hint used and understood beats a guess.",
           "Skipping the mock — timed practice is the only honest readiness signal."],
          "Do one scenario right now in any domain. Read the full explanation after submitting, right or wrong."),
    ]
    domain = {"id": did, "name": "Start Here: Ground Floor", "scenarios": []}
    return domain, lessons

def mock_domain(mock_name="Mock Assessment"):
    return {"id": "mock-assessment", "name": mock_name, "scenarios": []}

def capstone_domain(cap_name, cap_blurb, project_ideas):
    """project_ideas: list of (title, description) tuples."""
    did = "capstone-build"
    ideas_text = "\n".join(f"  {i+1}. {t} — {d}" for i, (t, d) in enumerate(project_ideas))
    lessons = [
        L(f"Capstone Overview: {cap_name}", did,
          [f"Your capstone is a real, demonstrable project: {cap_blurb}",
           "Pick one project and scope it to 2–4 weeks of part-time work. Smaller and finished beats ambitious and abandoned.",
           "Document as you build: architecture decisions, problems hit, how you solved them. This becomes your interview story.",
           "Publish the result: code repository, write-up, demo video. Employers and examiners trust artifacts over claims."],
          "PROJECT OPTIONS:\n" + ideas_text,
          "Choose your project by the end of this week. Write a one-page plan: goal, milestones, tech, done-criteria. " + cap_blurb,
          ["Choosing three projects — finish one brilliantly before starting a second.",
           "Building without documenting — the write-up is half the value.",
           "Tutorial-copying — extend it, break it, make it yours."],
          "Right now: rank the project options above. Write two sentences on why your top pick fits your goals."),
        L("Build in Public: Documentation That Proves Skill", did,
          ["A README that explains the problem, your approach, and the result is worth more than the code alone.",
           "Architecture diagrams show systems thinking. Decision logs show judgment. Test results show rigor.",
           "Demo videos (2–5 min) let reviewers see it working without installing anything.",
           "Link everything: resume → portfolio → repository → live demo. One click from claim to proof."],
          "README SKELETON:\n  # Project name — one-line outcome\n  ## Problem — who hurts and how\n  ## Approach — architecture + key decisions\n  ## Results — metrics, screenshots, demo link\n  ## What I'd do next — shows growth mindset",
          "Start your README on day one, not at the end. Fill it in as you build — it becomes your lab notebook.",
          ["README as afterthought — stale docs signal sloppy engineering.",
           "No demo — 'trust me, it works' convinces nobody.",
           "Hiding failures — 'what broke and how I fixed it' is the most credible section."],
          "Create the repository and README skeleton today, even before writing code."),
        L("Presenting Your Capstone: The Interview Story", did,
          ["Structure your story: situation → complication → your action → result. Sixty seconds, crisp.",
           "Lead with the outcome ('cut report time from 2 days to 20 minutes'), then explain how.",
           "Prepare for deep follow-ups: 'why this approach over X?' — your decision log has the answers.",
           "Connect the project to the role: map each project skill to a line in the job description."],
          "STORY TEMPLATE:\n  'We had [problem] costing [impact]. I built [solution] using [tech].\n   The hard part was [complication]; I solved it by [approach].\n   Result: [metric]. Next I'd [improvement].'",
          "Rehearse the story aloud three times. Record yourself once — painful but effective.",
          ["Rambling — practice the 60-second version until it is tight.",
           "Only happy path — interviewers probe failures; own yours with the fix.",
           "No metrics — 'it works' is weak; 'cut time 90%' is proof."],
          "Write your 60-second capstone story now. Time yourself reading it aloud."),
    ]
    domain = {"id": did, "name": cap_name, "scenarios": []}
    return domain, lessons

def ensure_simulation(d, items=None, minutes=None):
    sim = d.get("simulation") or {}
    if items is not None:
        sim["items"] = items
    if minutes is not None:
        sim["minutes"] = minutes
    sim.setdefault("evidence_cost_mins", 0)
    d["simulation"] = sim

def add_domain(d, domain):
    ids = [x.get("id") for x in d.get("domains", [])]
    if domain["id"] not in ids:
        d.setdefault("domains", []).append(domain)
        return True
    return False

def add_lessons(d, lessons):
    d.setdefault("lessons", []).extend(lessons)

def domain_by_id(d, did):
    for x in d.get("domains", []):
        if x.get("id") == did:
            return x
    return None

def lesson_count(d, did):
    return len([l for l in d.get("lessons", []) if l.get("domain_id") == did])

def validate(path):
    with open(path) as f:
        json.load(f)
    print("  JSON valid:", path)
