#!/usr/bin/env python3
"""Batch 1 expansion: rebuild 10 CBTs to full-stack standard. Part 1: helpers + shared builders."""
import json, copy, sys

def L(title, domain_id, concepts, code, walkthrough, pitfalls, try_it, lang="text"):
    assert len(concepts) >= 4, f"lesson needs 4+ concepts: {title}"
    assert len(pitfalls) >= 3, f"lesson needs 3+ pitfalls: {title}"
    return {
        "title": title, "domain_id": domain_id, "concepts": concepts,
        "example": {"lang": lang, "code": code, "walkthrough": walkthrough},
        "pitfalls": pitfalls, "try_it": try_it,
    }

def S(sid, title, domain_id, situation, prompt, choices, answer, why, hint, objectives, mins, evidence):
    assert len(choices) == 4, f"scenario needs 4 choices: {title}"
    assert 0 <= answer <= 3
    return {
        "id": sid, "title": title, "domain_id": domain_id, "situation": situation,
        "prompt": prompt, "choices": choices, "answer": answer, "why": why,
        "hint": hint, "objectives": objectives, "mins": mins, "evidence": evidence,
    }

def LB(lid, title, domain_id, objective, steps, checks, success_message):
    return {
        "id": lid, "title": title, "domain_id": domain_id, "objective": objective,
        "steps": steps, "checks": checks, "success_message": success_message,
    }

def CHECK(cmd, expect, hint):
    return {"command_pattern": cmd, "expect_contains": expect, "hint": hint}

# ---------------------------------------------------------------- shared builders
def start_here_lessons(course_name, exam_name, weekly_plan):
    return [
        L(f"How to Use This Bootcamp",
          "start-here",
          [
              f"The study order is deliberate \u2014 follow it: Start Here first, then work each domain in listed order. Domains unlock as you demonstrate mastery, because {exam_name} topics build on each other.",
              "What 'terminal' means: the Terminal tab is a real shell where labs run. Every lab command executes there \u2014 you learn by doing, not by reading about doing.",
              "Lessons teach concepts with a worked example, pitfalls, and a try-it prompt. Scenarios test judgment under realistic pressure. Labs prove you can execute. The mock assessment ties it all together.",
              "Knowledge checks verify understanding before a lesson counts complete \u2014 you cannot click through. Spaced repetition resurfaces weak areas automatically.",
              "Your progress syncs as you work. A domain is mastered when lessons are verified, scenarios answered, and labs completed.",
          ],
          f"Day 1: complete all 4 Start Here lessons\nDay 2-3: first two content domains (lessons + scenarios)\nDay 4+: one domain per day, labs each evening\nFinal 3 days: mock assessment runs + capstone build",
          "This order exists because later domains assume earlier vocabulary. Skipping ahead creates gaps that the mock assessment will expose \u2014 painfully. Trust the sequence.",
          [
              "Skimming lessons without attempting the knowledge check \u2014 verification is the learning, not a gate to dodge.",
              "Doing scenarios before reading the domain lessons \u2014 scenarios assume the concepts; you will guess instead of reason.",
              "Ignoring the Terminal labs \u2014 hands-on execution is what separates passing from failing on performance-based questions.",
          ],
          "Open the Terminal tab now and type `whoami`. That is the smallest possible lab \u2014 you just proved the environment works."),
        L(f"{exam_name} Exam Strategy",
          "start-here",
          [
              f"{exam_name} tests applied judgment more than memorization. Roughly a third of questions are scenario-based: read the situation, eliminate distractors, pick the BEST answer \u2014 not merely a correct one.",
              "Performance-based questions (PBQs) simulate real tasks: drag-and-drop, CLI output analysis, log reading. The labs in this bootcamp are PBQ rehearsal \u2014 treat every lab as exam practice.",
              "Time budget: divide total minutes by question count before you start, then check the clock every 20 questions. Flag hard questions and move on \u2014 a stuck minute is a lost minute.",
              "Elimination first: cross out the two obviously wrong choices, then compare the remaining two against the question's constraints (cheapest? most secure? first step?).",
              "Never leave a question blank. There is no penalty for wrong answers \u2014 an educated guess beats an empty one every time.",
          ],
          "Q: 'A user reports... Which should you do FIRST?'\n  \u2192 The word FIRST is the whole question.\n  \u2192 Eliminate any choice that is a later step.\n  \u2192 Among the rest, pick the diagnostic before the fix.",
          "Exam writers love FIRST, BEST, MOST, and LEAST. Those words change the answer even when the scenario looks identical. Read the actual question stem twice \u2014 once for the story, once for the ask.",
          [
              "Answering the scenario instead of the question \u2014 the story is context; the final sentence is the task.",
              "Changing answers on review without new evidence \u2014 first instincts outperform second-guessing statistically.",
              "Memorizing acronyms without understanding the process behind them \u2014 PBQs punish surface knowledge.",
          ],
          "Take any scenario in this bootcamp, cover the choices, and write what the question is really asking in one sentence before looking at options."),
        L("Study System: Spaced Repetition That Sticks",
          "start-here",
          [
              "Forgetting is the default \u2014 plan for it. Review a domain's key concepts at expanding intervals: 1 day, 3 days, 7 days, 14 days. Each successful recall strengthens the memory trace.",
              "Active recall beats re-reading: close the lesson and explain the concept aloud in your own words. If you cannot explain it, you do not know it yet.",
              "Interleave domains instead of block-studying one: mix scenarios from two domains in a session. Exams mix topics \u2014 your practice should too.",
              "The Feynman check: after each lesson, write a 3-sentence explanation a junior could follow. Vague sentences reveal vague understanding.",
              weekly_plan,
          ],
          "Session template (90 min):\n  0-10   warm-up: 5 flashcards / quick recalls\n  10-50  new domain: lessons + knowledge checks\n  50-75  scenarios from today + one older domain (interleaving)\n  75-90  one terminal lab, then 3-sentence Feynman writes",
          "Ninety focused minutes beat four distracted hours. The template above is engineered for retention, not seat time \u2014 protect the lab block, it is where skills become reflexes.",
          [
              "Re-reading notes and calling it studying \u2014 recognition is not recall; the exam tests recall.",
              "Cramming new domains the night before \u2014 sleep consolidates memory; an all-nighter trades retention for exhaustion.",
              "Skipping the Feynman write \u2014 it feels slow, but it is the fastest diagnostic of real understanding.",
          ],
          "Do one Feynman write right now: explain in 3 sentences what a bootcamp 'domain' is and why the order matters."),
        L("Systems Thinking: Your Unfair Advantage",
          "start-here",
          [
              "Exams and interviews reward systems thinkers: people who trace a request end-to-end instead of reciting isolated facts. This bootcamp trains that explicitly in the Systems Anatomy domain.",
              "The four-step method: (1) see the whole in context, (2) cut it open to reveal layers, (3) walk the process step-by-step, (4) pull apart into labeled pieces.",
              "Every troubleshooting scenario here is a systems trace in disguise: start from the symptom, walk backward through dependencies, find where the expected flow diverges from reality.",
              "In interviews, narrate the journey: 'the request starts here, then\u2026' \u2014 hiring managers hear senior-level thinking when you trace instead of define.",
              "The Systems Anatomy explorer in Visuals lets you step through living systems click by click. Use it before each domain's scenarios.",
          ],
          "Weak answer: 'DNS resolves names to IPs.'\nStrong answer: 'The stub resolver asks the recursive resolver, which walks root \u2192 TLD \u2192 authoritative, caching at each level \u2014 that is why the first lookup is slow and the second is instant.'",
          "One narrated journey demonstrates more competence than ten memorized definitions. Practice this voice in every scenario's 'why' explanation \u2014 read them aloud.",
          [
              "Defining terms instead of tracing flows when asked 'how does X work?'",
              "Jumping to fixes before mapping the system \u2014 fixes applied to the wrong layer waste time and credibility.",
              "Treating each domain as separate \u2014 the mock assessment deliberately chains them; practice connecting domains now.",
          ],
          "Open the Systems Anatomy domain and step through one full system in the explorer before your first study session."),
    ]

def mock_domain(course_name, exam_name, n_scenarios=0, minutes=180):
    return {
        "id": "mock-assessment",
        "name": f"Mock Assessment: {exam_name} Simulation",
        "description": f"A timed, exam-realistic simulation for {course_name}. Questions are drawn from every domain \u2014 hints disabled, each decision final, just like the real thing.",
        "icon": "\U0001F3AF",
        "lessons": [],
        "scenarios": [],
    }

def mock_briefing_lessons(course_name, exam_name):
    return [
        L(f"Mock Assessment Briefing: Rules of Engagement",
          "mock-assessment",
          [
              f"The mock simulates {exam_name} conditions: timed, mixed-domain, no hints, one shot per question. Treat it as the real exam \u2014 same chair, same focus, no phone.",
              "Scoring mirrors the real exam's weighting: scenario judgment counts more than recall. A wrong answer on a multi-step scenario costs more than a missed definition.",
              "Run the mock only after all domains show 80%+ mastery. Running it early wastes its diagnostic value \u2014 it is a measuring instrument, not a study tool.",
              "After each run, the review breaks down misses by domain. Your next study block targets exactly those domains \u2014 the mock tells you where to aim.",
              "Two full runs minimum: the first finds gaps, the second confirms they are closed. A passing second run is your green light.",
          ],
          "Mock protocol:\n  1. Silence notifications, full-screen the bootcamp\n  2. Note start time; budget per-question time on paper\n  3. Answer every question \u2014 no blanks\n  4. Flag-and-move on stuck questions; return with fresh eyes\n  5. Review the domain breakdown before any celebration",
          "The mock's value is the breakdown, not the score. A 68% with a clear miss-map beats a lucky 82% \u2014 the map tells you exactly what to study next.",
          [
              "Peeking at notes mid-mock \u2014 it inflates the score and destroys the diagnostic.",
              "Running the mock as a first activity \u2014 without domain mastery it only measures unpreparedness.",
              "Ignoring the domain breakdown \u2014 the score is trivia; the miss-map is the study plan.",
          ],
          f"Check your domain mastery percentages now. List any domain under 80% \u2014 those are your pre-mock targets."),
        L("Reviewing a Mock Run: Turning Misses into Mastery",
          "mock-assessment",
          [
              "For every missed question, classify the error: knowledge gap (never learned it), application gap (knew it, misapplied it), or reading error (misread the ask). Each type needs a different fix.",
              "Knowledge gaps go back to the domain lesson \u2014 re-read, re-verify, Feynman-write. Application gaps need more scenarios, not more reading. Reading errors need the exam-strategy lesson again.",
              "Keep an error log: question topic, error type, correct reasoning in one sentence. Patterns emerge fast \u2014 three 'reading errors' in a row is a process problem, not a knowledge problem.",
              "Re-test missed topics within 48 hours with fresh scenarios. A corrected mistake that is not re-tested is a mistake waiting to recur.",
              "Your second mock run should show misses migrating: fewer knowledge gaps, zero repeated reading errors. That migration is the signal you are ready.",
          ],
          "Error log entry:\n  Q: firewall rule order scenario \u2192 chose 'deny' before 'allow'\n  Type: application gap (knew rule order, misapplied under time pressure)\n  Fix: 5 more firewall scenarios, timed\n  Correct reasoning: 'First match wins \u2014 the allow had to precede the deny.'",
          "Do not just re-read the explanation and move on. The error log forces you to name the failure mode \u2014 and named failures are fixable failures.",
          [
              "Re-reading explanations passively \u2014 recognition feels like learning but evaporates under pressure.",
              "Studying only the missed topics and neglecting maintenance review of strong ones \u2014 strengths decay too.",
              "Taking the second mock too soon \u2014 give fixes 48 hours and a re-test cycle first.",
          ],
          "Create your error log file now (paper or notes app). You will need it after your first mock run."),
    ]

def capstone_domain(course_name, project_ideas):
    return {
        "id": "capstone-build",
        "name": f"Capstone: Build {course_name}",
        "description": f"Prove it by building it. A guided portfolio project that turns {course_name} knowledge into something you can demo in an interview.",
        "icon": "\U0001F6E0\uFE0F",
        "lessons": [],
        "scenarios": [],
    }

def capstone_lessons(course_name, projects):
    # projects: list of (title, what, demo_script)
    lessons = [
        L(f"Capstone Plan: What You Will Build and Why",
          "capstone-build",
          [
              f"Employers and examiners trust demonstrated skill over claimed knowledge. Your capstone is a working artifact \u2014 something you can screenshare and narrate in under 10 minutes.",
              "Pick ONE project from the list below. Depth beats breadth: a single polished build outperforms three half-finished ones.",
              "Scope it to finish in 2\u20133 focused sessions. If it needs more, cut features \u2014 a complete small project beats an ambitious pile of parts.",
              "Document as you go: every decision gets a one-line reason. That log becomes your interview narration script.",
              "Done means: it works end-to-end, you can demo it live, and you can explain every part without notes.",
          ],
          "Pick your project:\n" + "\n".join(f"  {i+1}. {p[0]} \u2014 {p[1]}" for i, p in enumerate(projects)),
          "Choose the project that scares you slightly \u2014 that is where the growth is. But cap the scope ruthlessly: you must finish.",
          [
              "Starting two projects and finishing neither \u2014 pick one, finish it, then consider a second.",
              "Building without documenting \u2014 the demo narration is half the value; no log means no story.",
              "Gold-plating instead of finishing \u2014 ship the working core first, polish only if time remains.",
          ],
          "Write your one-paragraph project selection rationale now: which project, why it fits your goals, and what 'done' looks like."),
        L("Build Log: Decisions, Dead Ends, and Proof",
          "capstone-build",
          [
              "Keep a build log with timestamps: what you tried, what happened, what you changed. Dead ends are valuable \u2014 they prove you debugged, not just followed a tutorial.",
              "For each component, record: purpose (one line), how it works (three lines), how you tested it (one command or check).",
              "Screenshot or record key milestones. A 60-second screen recording of the working project is worth more than a page of description.",
              "Version your work: even a simple dated folder structure beats a single 'final' file. Show the progression.",
              "The log is not overhead \u2014 it IS the deliverable's companion. Interviewers ask 'tell me about a challenge'; your log hands you the answer.",
          ],
          "Build log entry:\n  14:32 \u2014 Tried X config; service failed with error Y\n  14:47 \u2014 Found cause: Z was misconfigured (docs said A, reality was B)\n  15:05 \u2014 Fixed; verified with [test command]; works end-to-end",
          "Write the log as you go, not after. Memory lies; timestamps do not. Future-you (in the interview) will thank present-you.",
          [
              "Writing the log from memory at the end \u2014 you will forget the dead ends, which are the best stories.",
              "Skipping the 'how I tested it' line \u2014 untested claims collapse under the first interview question.",
              "No recordings \u2014 a live demo can fail; a recording is bulletproof backup.",
          ],
          "Create your build log file now with today's date and your project title as the header."),
        L("Demo Day: Narrating Your Build in 10 Minutes",
          "capstone-build",
          [
              "Structure the demo: problem (1 min) \u2192 architecture (2 min) \u2192 live walkthrough (5 min) \u2192 lessons learned (2 min). Rehearse it twice, timed.",
              "Narrate the systems journey: 'a request starts here, flows through\u2026' \u2014 the Systems Anatomy voice. Show you understand the whole, not just the parts you typed.",
              "Prepare for three hard questions: 'why this approach over X?', 'what breaks at scale?', 'what would you do differently?'. Write your answers in advance.",
              "Lead with the working demo, not slides. Working software presented live beats any deck.",
              "End with the repo/README link and offer to walk through the code. Make it effortless for them to verify your work.",
          ],
          "Demo script skeleton:\n  'I built [X] because [problem]. It works by [3-step journey].\n   Watch: [live action]. The tricky part was [challenge] \u2014\n   I solved it by [approach]. Code and docs are at [link].'",
          "Rehearsal is non-negotiable. A polished 10-minute demo signals preparation, communication skill, and genuine ownership \u2014 exactly what hiring managers screen for.",
          [
              "Wing the demo \u2014 'let me just show you' without a plan wastes the moment.",
              "Hiding the challenges \u2014 the dead ends and fixes are what prove real engineering happened.",
              "No backup plan \u2014 have the recording ready in case live demo gods are unkind.",
          ],
          "Draft your three hard-question answers now, before you build. They will sharpen your design decisions."),
    ]
    return lessons

def ensure_domains(data, domain_defs):
    """Add domains that don't exist. domain_defs: list of (id, name, description, icon)."""
    existing = {d.get('id') for d in data.get('domains', [])}
    for did, name, desc, icon in domain_defs:
        if did not in existing:
            data['domains'].append({"id": did, "name": name, "description": desc, "icon": icon,
                                    "lessons": [], "scenarios": []})
            existing.add(did)

def add_lessons(data, lessons):
    data.setdefault('lessons', []).extend(lessons)

def add_scenarios(data, domain_id, scenarios):
    for d in data['domains']:
        if d['id'] == domain_id:
            d.setdefault('scenarios', []).extend(scenarios)
            return
    raise ValueError(f"domain {domain_id} not found")

def add_labs(data, labs):
    data.setdefault('labs', []).extend(labs)

def counts(data):
    n_dom = len(data.get('domains', []))
    n_les = len(data.get('lessons', []))
    n_scen = sum(len(d.get('scenarios', [])) for d in data.get('domains', []))
    n_labs = len(data.get('labs', []))
    return n_dom, n_les, n_scen, n_labs
