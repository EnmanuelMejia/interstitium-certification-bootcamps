#!/usr/bin/env python3
"""Batch 1 builder: acad-career — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-career'
D = 'acad-career'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The lowball offer",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The offer letter is here — 20% below your target, 'take it or leave it, we need an answer by Friday.' You want this job. Decide like a negotiator, not a supplicant.",
        "steps": [
            {
                "symptom": "Offer: $72k. Your target: $90k. Market data for the role: $85-95k. Deadline: Friday. You want the job.",
                "evidence": [
                    ["Offer", "Offer: $72k | your target: $90k\nMarket range: $85-95k | deadline: Friday\nYou: want this job"]
                ],
                "options": [
                    "Accept immediately — a bird in the hand",
                    "Counter with evidence: thank them, anchor at $92k citing the market range and your specific value, and ask what flexibility exists on base, bonus, and start date",
                    "Reject outright — the lowball is insulting",
                    "Accept but plan to keep job hunting"
                ],
                "correct": 1,
                "explain": "Negotiation is collaborative problem-solving with numbers: gratitude, a counter anchored in market data (not feelings), and multiple levers (base, bonus, start date, review timeline). 'Take it or leave it' is usually an opening position, and exploding offers are often extendable when asked."
            },
            {
                "symptom": "They moved to $80k: 'This is our max for the band.' The hiring manager privately says the band can flex for exceptional candidates.",
                "evidence": [
                    ["Round 2", "Offer: $80k, 'max of band'\nHiring manager (off-record): 'bands flex for exceptional hires'\nYour leverage: two other processes in final rounds"]
                ],
                "options": [
                    "Accept $80k — the band is the band",
                    "Use the full picture: restate your value, mention competing processes without bluffing, and propose $88k with a 6-month performance review tied to compensation",
                    "Threaten to walk unless they hit $90k",
                    "Go around the recruiter to the CEO"
                ],
                "correct": 1,
                "explain": "Real leverage is real alternatives — mention them honestly, never as a bluff. And the 6-month review clause converts 'we can't' into 'prove it and we will': it gives them a face-saving yes and gives you a contractual second negotiation."
            },
            {
                "symptom": "Final: $86k base, $5k signing bonus, 6-month comp review. Above your walk-away, below your target. Friday is here.",
                "evidence": [
                    ["Final", "$86k + $5k signing + 6-month review\nYour walk-away: $80k | target: $90k"]
                ],
                "options": [
                    "Hold out for the full $90k",
                    "Accept: it clears your walk-away, the review clause protects the upside, and the role itself is what you wanted — then negotiate hard at month six with evidence",
                    "Accept but feel resentful",
                    "Ask for the weekend to think, hoping they panic"
                ],
                "correct": 1,
                "explain": "Negotiation ends with judgment, not victory: $86k clears your walk-away, the signing bonus bridges year one, and the review clause is a scheduled second negotiation. Take the win, document your impact from day one, and come back at month six with receipts."
            }
        ],
        "debrief": "You countered with data, used honest leverage, and closed with a review clause instead of a grudge. Salary negotiation is not combat — it is joint problem-solving where you know your numbers.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Resume vs reality",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You sailed the resume screen — but in the technical interview, your answers do not match your resume's claims. The interviewer notices. Fix the positioning before it becomes a credibility problem.",
        "steps": [
            {
                "symptom": "Your resume says 'led Kubernetes migration.' The interviewer asks about it; your answers reveal you assisted on one cluster.",
                "evidence": [
                    ["Interview", "Resume: 'Led Kubernetes migration'\nReality (your answers): assisted on one cluster\nInterviewer: noticeable pause, follow-up questions sharpen"]
                ],
                "options": [
                    "Double down — confidence is everything",
                    "Correct it in the moment: 'To be precise, I assisted on the migration — I owned the monitoring piece. Let me tell you what I actually did there.'",
                    "Deflect to a different topic",
                    "Blame the resume writer"
                ],
                "correct": 1,
                "explain": "The moment you feel the gap, you close it yourself — honestly and specifically. Interviewers forgive junior experience; they do not forgive discovered inflation. 'Let me be precise' followed by real detail rebuilds more credibility than the claim ever built."
            },
            {
                "symptom": "The interview recovered. But the resume still says 'led.' What changes tonight?",
                "evidence": [
                    ["Resume line", "'Led Kubernetes migration' — still on the resume"]
                ],
                "options": [
                    "Leave it — you talked your way through it once",
                    "Rewrite every inflated line into precise, verifiable claims: what you owned, what you assisted, what you learned — precision is the whole strategy",
                    "Delete the Kubernetes line entirely",
                    "Add more impressive verbs to compensate"
                ],
                "correct": 1,
                "explain": "The resume gets the precision treatment: 'assisted' where you assisted, 'owned' where you owned, numbers where you have them. A resume is a set of claims you must defend live — every line should survive its own interview."
            },
            {
                "symptom": "Resume fixed. A friend asks you to review THEIR resume — it has the same inflation.",
                "evidence": [
                    ["Ask", "Friend's resume: 'Architected microservices platform' (they configured one service)"]
                ],
                "options": [
                    "'Looks great!' — not your problem",
                    "Give them the same medicine, kindly: show them how precision ('configured and monitored X, serving Y requests') actually sounds stronger than the inflated version",
                    "Rewrite it for them with bigger claims",
                    "Tell them to remove the line"
                ],
                "correct": 1,
                "explain": "Precision sounds stronger than inflation: specific verbs and real scope are what hiring managers remember. Teaching it to someone else locks in your own lesson — and it is good karma in a small industry."
            }
        ],
        "debrief": "You corrected the record live, rewrote the resume into defensible claims, and taught the principle forward. Careers are built on credibility compounding — one honest correction at a time.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "The networking cold email",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You found the hiring manager of your dream role on LinkedIn. No mutual connections. One cold email stands between you and invisibility. Write it right.",
        "steps": [
            {
                "symptom": "Target: hiring manager, dream role, no warm intro. You have one shot at a cold email that gets opened, read, and answered.",
                "evidence": [
                    ["Target", "Hiring manager, infra team | no mutuals\nTheir recent post: about the team's migration to event-driven architecture\nYou: built a small event-driven side project"]
                ],
                "options": [
                    "'Hi, I'm looking for a job. Here's my resume. Can we chat?'",
                    "Short, specific, generous: reference their post genuinely, mention your relevant project in one line, ask for 15 minutes of advice — not a job",
                    "A long email detailing your life story",
                    "Connect with no message and hope"
                ],
                "correct": 1,
                "explain": "Cold outreach works on specificity and low ask: prove you did homework (their post), offer relevance (your project) in one line, and ask for advice — not employment. 'Can I pick your brain for 15 minutes?' gets answered; 'give me a job' gets archived."
            },
            {
                "symptom": "They replied: 'Happy to chat Thursday.' The call is in two days. How do you prepare?",
                "evidence": [
                    ["Call", "Thursday, 15 min | topic: their architecture migration"]
                ],
                "options": [
                    "Wing it — it is just a chat",
                    "Prepare three thoughtful questions about their migration, one crisp summary of your relevant work, and zero expectation of a referral — then follow up with thanks",
                    "Prepare a 10-minute pitch about yourself",
                    "Ask for a referral in the first 5 minutes"
                ],
                "correct": 1,
                "explain": "Networking calls are interviews where curiosity is the product: thoughtful questions about THEIR work, a crisp summary of yours if asked, and no referral ask on call one. The referral comes later — after you have been useful or memorable, not before."
            },
            {
                "symptom": "Great call. They said 'keep in touch.' What does that actually mean, operationally?",
                "evidence": [
                    ["Follow-up", "'Keep in touch!' — Thursday call went well"]
                ],
                "options": [
                    "Email them every week with updates",
                    "Send a thank-you within 24 hours with one specific takeaway, then follow up quarterly with something genuinely useful (an article, a project update) — 'keep in touch' is a system, not a sentiment",
                    "Wait for them to contact you",
                    "Immediately ask for the referral"
                ],
                "correct": 1,
                "explain": "'Keep in touch' fails without a system: thank-you in 24 hours (with a specific takeaway proving you listened), then light, useful touchpoints quarterly. Networking is farming, not hunting — and farmers keep a calendar."
            }
        ],
        "debrief": "You led with homework instead of hunger, prepared curiosity instead of a pitch, and turned 'keep in touch' into a system. Networking is just being usefully memorable, on a schedule.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "Burnout on the job hunt",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "200 applications. 3 callbacks. 0 offers. It is month four, the savings are thinning, and every rejection email feels personal. Respond — to the situation, not just the feelings.",
        "steps": [
            {
                "symptom": "200 applications, 3 callbacks (1.5%), 0 offers. Month four. You are starting to dread opening email.",
                "evidence": [
                    ["Funnel", "200 applied -> 3 callbacks (1.5%) -> 0 offers\nMonth 4 | savings: thinning\nEmotional state: dreading email"]
                ],
                "options": [
                    "Double the volume — 400 applications",
                    "Diagnose the funnel like an engineer: 1.5% callback means the top of funnel is broken — resume, targeting, or channel — not your worth. Fix the input before scaling the output",
                    "Take a month off entirely",
                    "Conclude you are unemployable"
                ],
                "correct": 1,
                "explain": "A 1.5% callback rate is a top-of-funnel problem with a top-of-funnel fix: resume, targeting, or channel — not a verdict on you. Doubling volume on a broken funnel just doubles rejection. Diagnose first, then scale what works."
            },
            {
                "symptom": "Diagnosis: you have been spraying generic applications at senior roles two levels up. The fix is targeting — but targeting feels slower.",
                "evidence": [
                    ["Diagnosis", "Pattern: generic resume x 200, mostly senior roles\nActual level: junior/associate\nChannel: 100% job boards, 0% referrals"]
                ],
                "options": [
                    "Keep spraying — volume will win eventually",
                    "Retarget: junior/associate roles, tailored resume per application, 5 quality applications a day, plus 2 networking conversations a week — slower per day, faster per offer",
                    "Only apply to dream companies from now on",
                    "Pay a resume service $500 and hope"
                ],
                "correct": 1,
                "explain": "The job hunt is a conversion funnel, and yours was miscalibrated at every stage: wrong level, generic resume, zero referrals. Five tailored applications plus real conversations beat fifty sprays — because referrals convert at 10x job boards and targeting converts at 10x spraying."
            },
            {
                "symptom": "The system is fixed and working — but month five is still hard. How do you sustain yourself?",
                "evidence": [
                    ["Sustain", "System working, results lagging (hiring takes weeks)\nEnergy: fragile"]
                ],
                "options": [
                    "Grind harder — rest is for the employed",
                    "Build the hunt like a job: fixed hours, measurable inputs (not just outcomes), one full day off weekly, exercise, and a weekly review — burnout makes you worse at the thing you need to be good at",
                    "Tie your self-worth to the offer count",
                    "Isolate until you have an offer"
                ],
                "correct": 1,
                "explain": "The job hunt is an endurance event run on your own psychology: fixed hours prevent the 14-hour despair spirals, input metrics (applications, conversations) give you wins before offers arrive, and rest is performance equipment. You cannot interview well from burnout."
            }
        ],
        "debrief": "You diagnosed the funnel instead of internalizing it, retargeted with precision, and built a sustainable system. The job hunt is a systems problem — and you are the system worth optimizing.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "The take-home test",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Final round: a take-home project, 'about 3-4 hours,' unpaid. It is now hour 9 and you see the edge of the scope. The hiring manager 'can't wait to see what you do with it.' Decide your boundaries.",
        "steps": [
            {
                "symptom": "Hour 9 of a '3-4 hour' take-home. The scope keeps expanding as you see edge cases. You really want this job.",
                "evidence": [
                    ["Take-home", "Quoted: 3-4 hours | actual: 9+ hours\nScope: expanding | desire for job: high"]
                ],
                "options": [
                    "Keep going until it is perfect — the job is worth it",
                    "Timebox it: finish a clean, working, documented core in 2 more hours, note the deliberately deferred edge cases in the README, and submit — boundaries are data about you too",
                    "Submit the half-done work now with apologies",
                    "Withdraw from the process in protest"
                ],
                "correct": 1,
                "explain": "A take-home that eats 12+ hours is testing your boundaries as much as your code. Timebox, ship a clean core, document the trade-offs explicitly — that README section ('deferred: X, Y because...') demonstrates senior judgment better than a perfect solution does."
            },
            {
                "symptom": "Submitted at hour 11 with documented trade-offs. The hiring manager asks: 'Why didn't you handle the edge cases?'",
                "evidence": [
                    ["Review", "'Why no edge-case handling?'"]
                ],
                "options": [
                    "Apologize and offer to do them now, free",
                    "'I timeboxed to the quoted scope plus a buffer, and documented what I deferred and why — in production I'd scope the same way. Happy to walk through how I'd handle them.'",
                    "'I ran out of time.'",
                    "Criticize their take-home design"
                ],
                "correct": 1,
                "explain": "Defend the boundary as engineering judgment: scoping under constraints IS the skill being tested (or should be). 'How I'd handle them' turns a gap into a demonstration. Never apologize for having a life — frame it as professional scoping."
            },
            {
                "symptom": "You got the job. A friend now faces a 15-hour take-home from another company. What do you tell them?",
                "evidence": [
                    ["Ask", "Friend: 'This take-home wants 15 hours. Should I do it?'"]
                ],
                "options": [
                    "'Do whatever it takes.'",
                    "'Evaluate the company by its hiring process: a 15-hour unpaid take-home signals how they value your time as an employee. Timebox it, or walk — your boundaries are set before you're hired, not after.'",
                    "'Just do it, everyone does.'",
                    "'Report them.'"
                ],
                "correct": 1,
                "explain": "The hiring process is the company's culture in preview: how they treat your unpaid time predicts how they treat your paid time. Boundaries set during hiring are the only ones that survive hiring. Teach it forward."
            }
        ],
        "debrief": "You timeboxed with documented trade-offs, defended scoping as a skill, and read the company's culture in its process. Boundaries are not the opposite of ambition — they are how ambition stays sustainable.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-tick-1",
        "title": "Track the application pipeline",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Run your job hunt like a pipeline: every application is a ticket. Open a P2 ticket for your target application, then assign the seeded INC-9001 to yourself (candidate) as the owner.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a ticket titled 'Application: Data Analyst role' with priority P2.",
                "validate": {"action": "create-ticket", "params": {"title": "Application: Data Analyst role", "priority": "P2"}},
                "hint": "Open New ticket: TITLE='Application: Data Analyst role', PRIORITY=P2."
            },
            {
                "id": "t2",
                "instruction": "Assign ticket INC-9001 to candidate.",
                "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "candidate"}},
                "hint": "Assign INC-9001: ID=INC-9001, ASSIGNEE=candidate."
            }
        ],
        "debrief": "Applications are a pipeline: tracked, owned, and staged. What gets ticketed gets followed up."
    },
    {
        "id": f"{SLUG}-csim-tick-2",
        "title": "Run the pipeline to offer",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The application is moving. Advance INC-9001 to in-progress, log the recruiter screen as a note, then resolve it when the offer lands — with the outcome recorded.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set ticket INC-9001 status to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "INC-9001", "status": "in-progress"}},
                "hint": "Update INC-9001: STATUS=in-progress."
            },
            {
                "id": "t2",
                "instruction": "Add a note to INC-9001: 'Recruiter screen scheduled.'",
                "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "Recruiter screen scheduled."}},
                "hint": "Add a note on INC-9001 with the exact text."
            },
            {
                "id": "t3",
                "instruction": "Resolve INC-9001 with resolution 'Offer accepted.'",
                "validate": {"action": "resolve-ticket", "params": {"id": "INC-9001", "resolution": "Offer accepted."}},
                "hint": "Resolve INC-9001 with the exact resolution text."
            }
        ],
        "debrief": "Every stage logged, every outcome recorded. A pipeline you can review is a pipeline you can improve."
    },
    {
        "id": f"{SLUG}-csim-web-1",
        "title": "Complete your public profile",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Recruiters google you. Complete the public profile: set the profile name, the contact email, and submit — an incomplete profile is an incomplete first impression.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the site_name field to 'My portfolio'.",
                "validate": {"action": "set-field", "params": {"id": "site_name", "value": "My portfolio"}},
                "hint": "Set field: FIELD=site_name, VALUE='My portfolio'."
            },
            {
                "id": "t2",
                "instruction": "Set the admin_email field to 'keeper@example.com'.",
                "validate": {"action": "set-field", "params": {"id": "admin_email", "value": "keeper@example.com"}},
                "hint": "Set field: FIELD=admin_email, VALUE=keeper@example.com."
            },
            {
                "id": "t3",
                "instruction": "Submit the form.",
                "validate": {"action": "submit-form", "params": {}},
                "hint": "Click Submit settings."
            }
        ],
        "debrief": "Complete profiles get found; complete profiles get contacted. Fill every field — the algorithm and the recruiter both notice."
    },
    {
        "id": f"{SLUG}-csim-git-1",
        "title": "Publish the resume site",
        "console": "git-host",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Your resume site update is ready. Create a branch feat/resume-site, then open a pull request into main — even personal projects ship through review.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a branch named feat/resume-site.",
                "validate": {"action": "create-branch", "params": {"name": "feat/resume-site"}},
                "hint": "Open Branches and create: NAME=feat/resume-site."
            },
            {
                "id": "t2",
                "instruction": "Open a pull request titled 'Publish resume site' from feat/resume-site into main.",
                "validate": {"action": "open-pr", "params": {"title": "Publish resume site", "base": "main", "head": "feat/resume-site"}},
                "hint": "Open a PR: TITLE='Publish resume site', BASE=main, HEAD=feat/resume-site."
            }
        ],
        "debrief": "Your career artifacts deserve the same rigor as production code: branched, reviewed, merged."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Inventory your assets",
        "domain_id": D,
        "difficulty": 1,
        "brief": "A career is a portfolio of assets. Start by inventorying this workspace: list the home directory and see what you have to work with.",
        "objectives": ["List your assets"],
        "checks": [
            {
                "command_pattern": "^ls$",
                "expect_contains": "README.md",
                "hint": "Run: ls — inventory what you have."
            }
        ],
        "success_message": "Assets inventoried. You cannot position what you have not catalogued."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Read your own story",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Before you tell your story to employers, read it yourself. Display README.md — does it say what you want it to say?",
        "objectives": ["Read your story"],
        "checks": [
            {
                "command_pattern": "^cat\\s+README\\.md$",
                "expect_contains": "Practice workspace",
                "hint": "Run: cat README.md — read your own narrative."
            }
        ],
        "success_message": "Story read. Your narrative is a product — review it like one."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Write your headline",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Every profile needs a one-line headline. Write yours with echo — it must contain 'DevSecOps'. Say what you are, plainly.",
        "objectives": ["Write your professional headline"],
        "checks": [
            {
                "command_pattern": "^echo\\s+.*DevSecOps.*$",
                "expect_contains": "DevSecOps",
                "hint": "Run: echo with your one-line headline containing DevSecOps (e.g. echo \"DevSecOps engineer\")."
            }
        ],
        "success_message": "Headline written. If you cannot say it in one line, you do not own it yet."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Commit to the practice",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Careers compound on deliberate practice. Hash the token 'practice' and confirm digest ada750e3f8464e9e1fd6a882b1a3b46cad39a1876c3fb7b85abe47a887c977fb — commit to the work.",
        "objectives": ["Hash the commitment token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+practice$",
                "expect_contains": "ada750e3f8464e9e1fd6a882b1a3b46cad39a1876c3fb7b85abe47a887c977fb",
                "hint": "Run: sha256sum practice — the digest must match character for character."
            }
        ],
        "success_message": "Practice committed. Careers are built in the hours nobody sees."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Learn from history",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Your past commands are a mentor. Search notes.txt for 'history' — the study notes explain how to learn from what you have already done.",
        "objectives": ["Find the history lesson"],
        "checks": [
            {
                "command_pattern": "^grep\\s+history\\s+notes\\.txt$",
                "expect_contains": "history",
                "hint": "Run: grep history notes.txt — learn from the past."
            }
        ],
        "success_message": "Lesson found. Review your history the way you would review a mentor's advice."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "How deep is your prep",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Interview prep has depth. Count the lines in notes.txt — measure the material you are bringing to the interview.",
        "objectives": ["Measure your prep"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+notes\\.txt$",
                "expect_contains": "8 notes.txt",
                "hint": "Run: wc -l notes.txt (pass the file; stdin is not simulated)."
            }
        ],
        "success_message": "8 lines of prep, measured. What gets measured gets deepened."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Research the employer",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Never interview blind. Verify the employer's infrastructure the way you would verify any claim: check connectivity with ping, then confirm name resolution with dig. Research is due diligence.",
        "objectives": ["Verify connectivity", "Verify name resolution"],
        "checks": [
            {
                "command_pattern": "^ping\\s+\\S+$",
                "expect_contains": "0% packet loss",
                "hint": "Run: ping <host> — confirm 0% packet loss."
            },
            {
                "command_pattern": "^dig\\s+\\S+$",
                "expect_contains": "93.184.216.34",
                "hint": "Run: dig <host> — confirm the A record in the ANSWER SECTION."
            }
        ],
        "success_message": "Employer researched. The candidate who did homework is the candidate who gets remembered."
    }
]


def main():
    path = os.path.join(BASE, SLUG, 'content.json')
    d = json.load(open(path))
    assert d['simulations'] == [], f"{SLUG}: simulations not empty"
    assert d['consoleSims'] == [], f"{SLUG}: consoleSims not empty"
    assert d['terminalMissions'] == [], f"{SLUG}: terminalMissions not empty"
    d['simulations'].extend(simulations)
    d['consoleSims'].extend(consoleSims)
    d['terminalMissions'].extend(terminalMissions)
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(tmp, path)
    d2 = json.load(open(path))
    ids = []
    for arr in ('simulations', 'consoleSims', 'terminalMissions'):
        for item in d2[arr]:
            ids.append(item['id'])
    assert len(ids) == len(set(ids)), 'duplicate ids'
    assert len(d2['simulations']) == 5 and len(d2['consoleSims']) == 4 and len(d2['terminalMissions']) == 7
    for m in d2['terminalMissions']:
        for c in m['checks']:
            assert c.get('hint'), f"missing hint in {m['id']}"
    for c in d2['consoleSims']:
        for t in c['tasks']:
            assert t.get('hint'), f"missing hint in {c['id']}"
    print(f"{SLUG}: OK — 5 sims, 4 csims, 7 missions; {len(ids)} unique ids")


if __name__ == '__main__':
    main()
