#!/usr/bin/env python3
"""Batch 1 builder: acad-theory — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-theory'
D = 'acad-theory'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "P vs NP in the standup",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The routing team needs optimal delivery routes for 200 stops by Friday. Someone suggests 'just try all permutations.' You know why that fails. Decide what ships.",
        "steps": [
            {
                "symptom": "200 stops, optimal routes, Friday deadline. Proposal: brute-force all permutations and pick the best.",
                "evidence": [
                    ["Proposal", "Stops: 200 | approach: enumerate all permutations\nDeadline: Friday | claim: 'computers are fast now'"]
                ],
                "options": [
                    "Approve — modern hardware can handle it",
                    "Reject with the math: 200! is ~10^374 permutations — more than atoms in the universe times itself. Brute force is not slow, it is impossible",
                    "Rent a bigger cluster for the enumeration",
                    "Reduce to 10 stops so brute force works"
                ],
                "correct": 1,
                "explain": "Factorial growth is not a performance problem — it is a physics problem. 200! dwarfs the age of the universe in nanoseconds. Complexity theory is not academic here; it is the difference between a plan and a fantasy."
            },
            {
                "symptom": "Brute force is dead. The team asks what actually ships Friday.",
                "evidence": [
                    ["Constraint", "Need: good routes by Friday | optimal: provably impossible at this scale"]
                ],
                "options": [
                    "Ship nothing — the problem is unsolvable",
                    "Ship a heuristic: nearest-neighbor plus local improvement gets within a few percent of optimal in seconds — and say so honestly",
                    "Wait for a quantum computer",
                    "Hire more drivers instead of optimizing"
                ],
                "correct": 1,
                "explain": "NP-hard means 'no known efficient exact algorithm' — not 'give up.' Heuristics and approximation algorithms exist precisely for this: near-optimal answers at industrial speed, with the approximation gap stated honestly. Theory tells you what not to attempt; engineering tells you what ships."
            },
            {
                "symptom": "Heuristic shipped: routes 4% longer than the theoretical optimum, computed in 11 seconds. How do you present it?",
                "evidence": [
                    ["Result", "Routes: within 4% of optimal | compute: 11s\nStakeholder question: 'Why not optimal?'"]
                ],
                "options": [
                    "'The algorithm is optimal.'",
                    "'Optimal would take longer than the universe; we get within 4% in 11 seconds. That 4% costs us roughly $X/week — here is the trade, in dollars.'",
                    "'Nobody needs optimal.'",
                    "Hide the 4% gap"
                ],
                "correct": 1,
                "explain": "Approximation is a business decision once you price the gap: 4% longer routes = $X/week, versus the impossibility of optimal. Theory gave you the impossibility proof; arithmetic gives you the price tag. Present both."
            }
        ],
        "debrief": "You killed the fantasy with factorial math, shipped the heuristic honestly, and priced the approximation gap. Complexity theory is project management for the impossible.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "The halting helpdesk ticket",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Ticket: 'Write a linter rule that detects ALL infinite loops before deployment.' The requester is serious, senior, and wrong in an interesting way. Handle it.",
        "steps": [
            {
                "symptom": "The ticket asks for a perfect infinite-loop detector. The requester cites 'AI advances' as evidence it is now possible.",
                "evidence": [
                    ["Ticket", "'Detect all infinite loops pre-deploy'\nRequester: senior eng | justification: 'AI can do anything now'"]
                ],
                "options": [
                    "Assign it to the team as a stretch goal",
                    "Explain the halting problem: no program can correctly decide halting for ALL programs — it is proven impossible, not merely hard. Then offer what IS possible",
                    "Buy an AI tool that claims to do it",
                    "Close the ticket as 'won't fix' with no explanation"
                ],
                "correct": 1,
                "explain": "The halting problem is undecidable — proven, not conjectured. No amount of AI changes a mathematical impossibility; a tool that 'detects all infinite loops' is either unsound or incomplete by necessity. 'Won't fix' without the explanation wastes the teaching moment."
            },
            {
                "symptom": "The requester accepts the proof but asks: 'So we just deploy infinite loops and hope?'",
                "evidence": [
                    ["Follow-up", "'What DO we do about runaway processes?'"]
                ],
                "options": [
                    "'Yes, hope is the strategy.'",
                    "Offer the decidable substitutes: timeouts, resource limits, loop-complexity heuristics, and termination proofs for the specific patterns you actually use — impossibility of the general case does not block the practical cases",
                    "Write the perfect detector anyway",
                    "Ban loops in the codebase"
                ],
                "correct": 1,
                "explain": "Undecidable in general, manageable in practice: timeouts bound the damage, resource limits contain it, and heuristics catch the common patterns. Theory draws the boundary of the possible; engineering works the territory inside it."
            },
            {
                "symptom": "Timeouts and limits are in. A junior asks why the linter still misses some infinite loops.",
                "evidence": [
                    ["Ask", "Junior: 'I thought we fixed this?'"]
                ],
                "options": [
                    "'We did — the linter is just buggy.'",
                    "'We bounded the damage, we did not solve the problem — and we cannot, provably. Knowing which problems are impossible is what keeps us from wasting sprints on them.'",
                    "'Don't worry about it.'",
                    "Assign the junior to fix the linter"
                ],
                "correct": 1,
                "explain": "The deepest lesson: knowing a problem is impossible is productive knowledge — it redirects effort from the unwinnable to the winnable. That is what computability theory is for: a map of where not to dig."
            }
        ],
        "debrief": "You delivered the impossibility proof with kindness, offered the practical substitutes, and taught the team to read the map. Undecidability is not despair — it is direction.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "Exponential blowup",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The recursive Fibonacci service handles n=30 fine and dies at n=50. The code 'works' — it just never finishes. Find the complexity bug.",
        "steps": [
            {
                "symptom": "fib(30) returns in a second. fib(50) has been running for an hour. Same code, same machine.",
                "evidence": [
                    ["Code", "def fib(n):\n    if n < 2: return n\n    return fib(n-1) + fib(n-2)\nTiming: n=30 ~1s | n=50 >1h (killed)"]
                ],
                "options": [
                    "Add more CPU — n=50 just needs power",
                    "Recognize the exponential: naive recursion recomputes the same subproblems ~2^n times — n=50 needs ~10^10 calls. Memoize or go iterative",
                    "Rewrite it in a faster language",
                    "Cache the results in a database"
                ],
                "correct": 1,
                "explain": "Each call doubles the work: O(2^n). n=30 is a billion-ish operations (fine); n=50 is a quadrillion (not fine). The bug is not in the logic — it is in the complexity class. Memoization drops it to O(n) because each subproblem gets solved once."
            },
            {
                "symptom": "Memoized: fib(50) returns instantly. But a teammate asks: 'Is recursion itself the problem?'",
                "evidence": [
                    ["Ask", "'Should we ban recursion?'"]
                ],
                "options": [
                    "Yes — recursion is dangerous",
                    "'No — the problem was repeated work, not recursion. Memoized recursion is O(n) time and O(n) space; iterative is O(n) time and O(1) space. Pick by the trade-off, not by fear.'",
                    "Rewrite everything iteratively to be safe",
                    "Limit recursion depth globally"
                ],
                "correct": 1,
                "explain": "Blaming recursion misses the lesson: the enemy was exponential repeated work. Compare the actual trade-offs (time vs. space, clarity vs. constants) instead of banning the technique. Complexity analysis, not superstition."
            },
            {
                "symptom": "Fixed and fast. What do you add to code review so the next exponential does not ship?",
                "evidence": [
                    ["Ask", "Team: 'How do we catch these in review?'"]
                ],
                "options": [
                    "Ban recursion in review guidelines",
                    "Add a review checklist item: for any recursive or nested-loop code, state the complexity in Big-O in the PR description — and test at 10x the expected input size",
                    "Require benchmarks for every PR",
                    "Trust senior reviewers to spot it"
                ],
                "correct": 1,
                "explain": "Make complexity explicit and testable: Big-O in the PR description forces the author to think, and 10x input tests turn 'works on my data' into 'works at scale.' Exponentials hide at small n — test at large n."
            }
        ],
        "debrief": "You diagnosed the complexity class, not the code; defended recursion with trade-offs; and made Big-O explicit in review. Performance bugs are complexity bugs wearing a trench coat.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "Two generals, one deploy",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Two data centers must switch traffic at the same instant — but the link between them can drop any message. The plan requires perfect coordination. Decide what is actually achievable.",
        "steps": [
            {
                "symptom": "The cutover plan: DC-A and DC-B flip simultaneously at midnight, confirmed by message. The link drops ~1% of messages.",
                "evidence": [
                    ["Plan", "DC-A and DC-B flip at 00:00, coordinated by messages\nLink: 1% message loss | requirement: 'perfectly simultaneous'"]
                ],
                "options": [
                    "Add retries — with enough retries it will be simultaneous",
                    "Recognize the Two Generals impossibility: no finite message exchange guarantees common knowledge over a lossy link — design for the impossibility instead of against it",
                    "Use a longer timeout",
                    "Get a better link"
                ],
                "correct": 1,
                "explain": "The Two Generals problem proves perfect coordination over unreliable messaging is impossible — the last acknowledgment is always uncertain. More retries shrink the doubt; they never eliminate it. Impossibility results are design constraints, not problems to out-stubborn."
            },
            {
                "symptom": "Perfect simultaneity is impossible. The business still needs a cutover Friday.",
                "evidence": [
                    ["Constraint", "Cutover: Friday | simultaneity: impossible\nNeed: safe, not perfect"]
                ],
                "options": [
                    "Cancel the cutover",
                    "Design around it: make the flip idempotent and time-bounded — either DC can flip safely alone, both flip within a window, and the system converges instead of coordinating",
                    "Flip both and hope the messages arrive",
                    "Flip one, wait an hour, flip the other"
                ],
                "correct": 1,
                "explain": "When coordination is impossible, design systems that do not need it: idempotent flips, convergence windows, and either-side-safe operations. The great distributed-systems trick is replacing 'agree then act' with 'act safely without agreeing.'"
            },
            {
                "symptom": "Cutover succeeded via convergence. An architect asks: 'So when CAN two systems agree?'",
                "evidence": [
                    ["Ask", "'When is coordination possible?'"]
                ],
                "options": [
                    "'Never — give up on distributed systems.'",
                    "'With majorities and retries: consensus protocols (Paxos/Raft-style) give practical agreement with high probability under partial synchrony — not perfect certainty, but engineered reliability. Theory sets the ceiling; protocols work the room below it.'",
                    "'With a perfect network.'",
                    "'With blockchain.'"
                ],
                "correct": 1,
                "explain": "Impossibility of perfection does not mean impossibility of practice: consensus protocols deliver agreement that is reliable enough to bet businesses on, under stated assumptions. The honest answer names both the ceiling and the room."
            }
        ],
        "debrief": "You accepted the impossibility, designed for convergence instead of coordination, and explained the practical middle. Theory's 'impossible' is the beginning of engineering, not the end.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "The regex that ate the server",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A user submitted a 40-character string and the validation regex has been running for six minutes at 100% CPU. It is catastrophic backtracking. Respond.",
        "steps": [
            {
                "symptom": "One 40-character input, one regex, six minutes of 100% CPU. The pattern: ^(a+)+$ against 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab'.",
                "evidence": [
                    ["Incident", "Pattern: ^(a+)+$ | input: 31 a's + 'b'\nCPU: 100% for 6+ min | service: validation endpoint"]
                ],
                "options": [
                    "Kill the process and move on",
                    "Kill it, then understand: nested quantifiers create exponential backtracking paths — the engine tries every way to split the a's before failing. This is ReDoS, and the fix is structural",
                    "Add more CPU so it finishes faster",
                    "Ban the user who submitted the string"
                ],
                "correct": 1,
                "explain": "Catastrophic backtracking is exponential: (a+)+ against a non-matching string explores ~2^n partitions. Killing the process stops the bleeding; understanding the mechanism prevents the recurrence. The input was not an attack — it was a fuzzer doing you a favor."
            },
            {
                "symptom": "Understood. Now fix the validation so this class of incident dies.",
                "evidence": [
                    ["Goal", "Kill the ReDoS class, not just this regex"]
                ],
                "options": [
                    "Rewrite this one regex more carefully",
                    "Defense in depth: rewrite without nested quantifiers (^a+$), add a regex timeout to the engine, and cap input length before matching — one fix is a patch, three is a posture",
                    "Remove regex validation entirely",
                    "Only allow alphanumeric input everywhere"
                ],
                "correct": 1,
                "explain": "One careful regex is one careful regex — the next author writes the next bomb. Structural defenses (no nested quantifiers as a lint rule, engine timeouts, input caps) protect against the whole class. Fix the instance AND the category."
            },
            {
                "symptom": "Fixed. A teammate asks: 'How do I know if MY regex is dangerous?'",
                "evidence": [
                    ["Ask", "'What is the rule of thumb?'"]
                ],
                "options": [
                    "'Regexes are fine, don't worry.'",
                    "'Nested quantifiers (a+)+, (a*)*, (a|b+)+ are the smell — and test every regex against a long near-miss input. If it does not return instantly, it is exponential.'",
                    "'Avoid regex entirely.'",
                    "'Only use regexes from Stack Overflow.'"
                ],
                "correct": 1,
                "explain": "Teach the smell and the test: nested quantifiers are the warning sign, and the near-miss stress test (long input that almost matches) is the detector. Theory made visible: exponential blowup you can feel in your terminal."
            }
        ],
        "debrief": "You killed the process, learned the mechanism, defended the whole class, and taught the smell. A 40-character string taught the team more about complexity than a semester of lectures.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-code-1",
        "title": "Breakpoint the loop",
        "console": "code-editor",
        "domain_id": D,
        "difficulty": 1,
        "brief": "You are studying how total() accumulates. Open app.py and set a breakpoint on line 3 — the loop header — to watch each iteration.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Open the file app.py.",
                "validate": {"action": "open-file", "params": {"name": "app.py"}},
                "hint": "Open app.py in the editor."
            },
            {
                "id": "t2",
                "instruction": "Set a breakpoint on line 3 of app.py.",
                "validate": {"action": "toggle-breakpoint", "params": {"file": "app.py", "line": 3}},
                "hint": "Toggle a breakpoint: FILE=app.py, LINE=3 (the loop header)."
            }
        ],
        "debrief": "Breakpoints on loop headers let you watch iteration happen. Observing execution is how abstract complexity becomes concrete."
    },
    {
        "id": f"{SLUG}-csim-code-2",
        "title": "Retarget the service port",
        "console": "code-editor",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The deployment spec moved the service to port 9090. Open config.yaml and change line 2 to set the port — precision matters in configuration.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Open the file config.yaml.",
                "validate": {"action": "open-file", "params": {"name": "config.yaml"}},
                "hint": "Open config.yaml in the editor."
            },
            {
                "id": "t2",
                "instruction": "Fix line 2 of config.yaml to read exactly: two spaces, then 'port: 9090'.",
                "validate": {"action": "fix-line", "params": {"file": "config.yaml", "line": 2, "text": "  port: 9090"}},
                "hint": "Fix line 2: FILE=config.yaml, LINE=2, TEXT='  port: 9090' (keep the two-space indent)."
            }
        ],
        "debrief": "Configuration is code: exact, reviewed, and precise. One wrong character and the theory meets reality."
    },
    {
        "id": f"{SLUG}-csim-sql-1",
        "title": "Query the truth table",
        "console": "sql-studio",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Relational logic is logic made executable. Run a SELECT query — the console validates that your SQL actually selects.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Run a SQL query beginning with SELECT.",
                "validate": {"action": "run-query", "params": {"match": "SELECT"}},
                "hint": "Type a query containing SELECT, e.g. SELECT * FROM measurements."
            }
        ],
        "debrief": "SELECT is existential quantification with a WHERE clause. Logic, but it returns rows."
    },
    {
        "id": f"{SLUG}-csim-web-1",
        "title": "File the complexity worksheet",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Every algorithm you study gets a worksheet: its complexity class and your contact. Set the fields and submit — written analysis beats remembered analysis.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the site_name field to 'Complexity worksheet'.",
                "validate": {"action": "set-field", "params": {"id": "site_name", "value": "Complexity worksheet"}},
                "hint": "Set field: FIELD=site_name, VALUE='Complexity worksheet'."
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
        "debrief": "Write the complexity down. An analysis that lives only in your head cannot be checked."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Read the algorithm",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Before analyzing complexity, read the code. Display app.py — know what you are reasoning about.",
        "objectives": ["Read app.py"],
        "checks": [
            {
                "command_pattern": "^cat\\s+app\\.py$",
                "expect_contains": "for i in range(3)",
                "hint": "Run: cat app.py — read the algorithm first."
            }
        ],
        "success_message": "Algorithm read. Analysis begins with the text, not the conclusion."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Find the loop",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Complexity lives in loops. Search app.py for the loop construct — find where the iteration happens.",
        "objectives": ["Locate the loop"],
        "checks": [
            {
                "command_pattern": "^grep\\s+for\\s+app\\.py$",
                "expect_contains": "for i in range(3)",
                "hint": "Run: grep for app.py — find the iteration."
            }
        ],
        "success_message": "Loop found. Every complexity argument starts by locating the repetition."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Count the steps",
        "domain_id": D,
        "difficulty": 1,
        "brief": "How many steps does this program take? Count the lines in app.py — the first crude measure of size.",
        "objectives": ["Count the lines"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+app\\.py$",
                "expect_contains": "5 app.py",
                "hint": "Run: wc -l app.py (pass the file; stdin is not simulated)."
            }
        ],
        "success_message": "5 lines. Size is not complexity — but you measure size first anyway."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Read the signature",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The interface tells you what varies. Read the first two lines of app.py — the function signature defines the input the complexity is measured against.",
        "objectives": ["Read the function signature"],
        "checks": [
            {
                "command_pattern": "^head\\s+-n\\s+2\\s+app\\.py$",
                "expect_contains": "def greet",
                "hint": "Run: head -n 2 app.py — what is the input?"
            }
        ],
        "success_message": "Signature read. Complexity is always 'in terms of what' — name the input first."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Read the driver",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The bottom of the file drives the top. Read the last two lines of app.py — see how the algorithm is actually invoked.",
        "objectives": ["Read the driver code"],
        "checks": [
            {
                "command_pattern": "^tail\\s+-n\\s+2\\s+app\\.py$",
                "expect_contains": "print(greet(",
                "hint": "Run: tail -n 2 app.py — how is it called?"
            }
        ],
        "success_message": "Driver read. Theory meets practice at the call site."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "State the complexity",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The loop in app.py runs exactly 3 times — a constant, independent of any input. State the complexity class with echo: O(1).",
        "objectives": ["State the complexity class"],
        "checks": [
            {
                "command_pattern": "^echo\\s+O\\(1\\)$",
                "expect_contains": "O(1)",
                "hint": "The loop bound is a constant (3), so the class is constant time — run: echo O(1)"
            }
        ],
        "success_message": "O(1) stated. Constant work is constant work — name the class, do not just feel it."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Attest the proof",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Proofs get attested, not asserted. Hash the token 'attest' and confirm digest bcc7930764b9b7a8b9bbd0161b568e869466d0c4efaee8006a56f3e8e6d82b69 — commit to the reasoning.",
        "objectives": ["Hash the attestation token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+attest$",
                "expect_contains": "bcc7930764b9b7a8b9bbd0161b568e869466d0c4efaee8006a56f3e8e6d82b69",
                "hint": "Run: sha256sum attest — the digest must match character for character."
            }
        ],
        "success_message": "Proof attested. In theory as in systems: verify, do not trust."
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
