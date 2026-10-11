#!/usr/bin/env python3
"""Batch 1 builder: acad-hermetica — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-hermetica'
D = 'acad-hermetica'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The fix that broke more",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You fixed the slow query with a cache. Latency dropped — then the database fell over, then the retry storm took down the API. Your fix had a feedback loop in it. Find it.",
        "steps": [
            {
                "symptom": "Cache added in front of the slow query. P99 latency halved for an hour — then the database CPU hit 100% and the API started timing out.",
                "evidence": [
                    ["Timeline", "10:00 cache deployed | 10:00-11:00 P99 halved\n11:05 DB CPU 100% | 11:10 API timeouts\nCache hit rate: 95% (the cache is working!)"]
                ],
                "options": [
                    "Remove the cache — it clearly caused this",
                    "Look for the loop: what does the cache change about downstream behavior? Check retries and thundering-herd on expiry",
                    "Add more database capacity",
                    "Increase the cache TTL"
                ],
                "correct": 1,
                "explain": "The cache works — that is the trap. The 5% miss rate on a hot key expires all at once, every miss hammers the DB, slow DB triggers client retries, retries multiply the load: a reinforcing loop. Fixes that change behavior create new dynamics; you have to model the loop, not just the component."
            },
            {
                "symptom": "Confirmed: cache stampede on expiry plus aggressive client retries — each timeout triples the load.",
                "evidence": [
                    ["Loop", "Cache expiry -> 5% misses hit DB at once\nSlow DB -> client timeouts -> 3x retries\nRetries -> more DB load -> more timeouts (reinforcing)"]
                ],
                "options": [
                    "Disable retries entirely",
                    "Break the loop at two points: staggered cache expiry (jitter) plus bounded retries with backoff and circuit-breaking",
                    "Make the cache never expire",
                    "Tell clients to stop retrying"
                ],
                "correct": 1,
                "explain": "Reinforcing loops get broken at multiple points: jittered expiry spreads the stampede, bounded backoff retries stop the multiplication, and a circuit breaker caps the damage. One fix leaves the loop alive; two fixes starve it."
            },
            {
                "symptom": "Loop broken, system stable. What do you change about how the team ships fixes?",
                "evidence": [
                    ["Ask", "Team: 'How do we catch the next feedback loop before production?'"]
                ],
                "options": [
                    "Require a 'second-order effects' section in every change proposal: what behavior does this change, and what loops could that create?",
                    "Ban caches",
                    "Only allow senior engineers to ship fixes",
                    "Add more dashboards"
                ],
                "correct": 0,
                "explain": "Make the thinking explicit and mandatory: every change proposal names its second-order effects and the loops it might create. You cannot outlaw emergence, but you can require people to look for it before shipping."
            }
        ],
        "debrief": "You modeled the loop instead of blaming the component, broke it at two points, and made second-order thinking part of the process. Systems thinking is asking 'and then what?' until the answer stops changing.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Incentives vs intentions",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Support is now bonused on tickets closed per day. Closures are up 40% — and reopen rates tripled. The incentive is working exactly as designed, which is the problem.",
        "steps": [
            {
                "symptom": "Tickets closed/day: +40%. Reopened tickets: 3x. Customer satisfaction: falling.",
                "evidence": [
                    ["Metrics", "Closed/day +40% | reopen rate 3x\nCSAT falling | sample ticket: closed with 'please try restarting'"]
                ],
                "options": [
                    "Raise the bonus — closures are up, the system works",
                    "Recognize the perverse incentive: you are measuring closures, so you get closures — not resolutions. Change what you reward",
                    "Punish agents with high reopen rates",
                    "Close the metrics dashboard so nobody games it"
                ],
                "correct": 1,
                "explain": "Every metric is an incentive, and people optimize the metric, not the intention behind it. 'Tickets closed' measures speed of closing; you wanted resolution. When a measure becomes a target, it ceases to be a good measure."
            },
            {
                "symptom": "You need a better metric. What do you reward instead?",
                "evidence": [
                    ["Goal", "Reward real resolution without creating a new gaming surface"]
                ],
                "options": [
                    "Tickets closed per day, but with a manager reviewing each one",
                    "Resolution confirmed by the customer (no reopen in 7 days), balanced with a quality sample review — slower, harder to game, aligned with the actual goal",
                    "Customer satisfaction scores alone",
                    "Hours worked"
                ],
                "correct": 1,
                "explain": "Good metrics are hard to game and close to the real goal: customer-confirmed resolution, with sampling to catch the rest. Every metric can be gamed — so you pick the one whose gaming still produces value, and you keep watching."
            },
            {
                "symptom": "New metric in place. An agent asks: 'So should I spend longer on each ticket now?'",
                "evidence": [
                    ["Ask", "Agent: 'What does good look like under the new system?'"]
                ],
                "options": [
                    "'Just hit the new numbers.'",
                    "'Solve it properly the first time. A ticket that stays closed is worth five fast ones — the metric now agrees with the craft.'",
                    "'Do whatever the metric rewards.'",
                    "'Ask your manager for each ticket.'"
                ],
                "correct": 1,
                "explain": "Say the principle out loud: the metric now rewards the craft, not the shortcut. People follow incentives, but they also follow clearly stated principles — give them both, aligned."
            }
        ],
        "debrief": "You saw the incentive behind the metric, replaced it with one closer to the real goal, and stated the principle. Systems do what they are rewarded for — design the rewards, design the system.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "The second-order outage",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 3,
        "brief": "A routine certificate rotation took down the monitoring system — which meant nobody saw the REAL outage starting underneath it. Respond to the outage behind the outage.",
        "steps": [
            {
                "symptom": "Cert rotation at 09:00. By 09:15 monitoring is dark. By 09:30, users report the API is down — and you have no telemetry to see why.",
                "evidence": [
                    ["Timeline", "09:00 cert rotation | 09:15 monitoring dark (cert pinned)\n09:30 user reports: API down | telemetry: none\nYou are flying blind"]
                ],
                "options": [
                    "Fix monitoring first — you need visibility",
                    "Check the API directly (logs, health endpoints, user-facing probes) while someone in parallel fixes monitoring — the user outage outranks the visibility outage",
                    "Roll back the cert rotation immediately",
                    "Wait for monitoring to come back on its own"
                ],
                "correct": 1,
                "explain": "Two outages, one priority: users beat dashboards. You work the API directly (logs and probes still exist) while monitoring gets fixed in parallel. Fixing visibility first while users burn is instrumenting the fire instead of fighting it."
            },
            {
                "symptom": "API is back (a stuck deploy queue, cleared manually). Monitoring is back (cert updated). Now the uncomfortable question: why did one rotation break two systems?",
                "evidence": [
                    ["Coupling", "Monitoring agent pinned the old cert (undocumented)\nDeploy queue had no alerting except via the monitoring that was down\nSingle rotation -> dual failure"]
                ],
                "options": [
                    "Blame the rotation engineer",
                    "Map the hidden coupling: monitoring depended on the cert process, the deploy queue depended on monitoring. Fix both couplings — and rotate certs in a drill first next time",
                    "Never rotate certs again",
                    "Add more monitoring to the monitoring"
                ],
                "correct": 1,
                "explain": "Second-order failures come from hidden coupling: A depends on B depends on C, and nobody drew the arrows. The fix is mapping the real dependency graph and drilling the rotation — the outage was a coupling problem wearing a certificate costume."
            },
            {
                "symptom": "Coupling mapped and fixed. What single practice would have caught this cheapest?",
                "evidence": [
                    ["Ask", "Team: 'What is the one thing we add?'"]
                ],
                "options": [
                    "More dashboards",
                    "Pre-mortems for routine changes: before any 'routine' change, ask 'what breaks if this goes wrong?' and trace two levels of dependency",
                    "Longer change-approval forms",
                    "A bigger on-call rotation"
                ],
                "correct": 1,
                "explain": "Pre-mortems are cheap second-order thinking: ten minutes asking 'what breaks two levels down?' before a routine change. The cert rotation was 'routine' — which is exactly why nobody traced its dependencies."
            }
        ],
        "debrief": "You prioritized users over visibility, mapped the hidden coupling, and installed pre-mortems for routine changes. Outages are rarely about the first failure — they are about the second and third.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "Map the system",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The same incident has happened four times this quarter: the queue backs up, someone restarts it, it recovers, everyone moves on. The restart is not a fix — it is a ritual. Find the structure.",
        "steps": [
            {
                "symptom": "Fourth queue backup this quarter. Same symptom, same restart, same recovery. Nobody knows why it backs up.",
                "evidence": [
                    ["History", "Q1: 4 identical incidents | fix each time: restart\nTime to backup: ~3 weeks after each restart\nMonitoring: queue depth only (no consumer metrics)"]
                ],
                "options": [
                    "Restart it again — it works",
                    "Stop treating the event and start treating the pattern: instrument the consumers, and ask what accumulates over three weeks",
                    "Replace the queue with a bigger one",
                    "Add an auto-restart cron job"
                ],
                "correct": 1,
                "explain": "Events are symptoms; patterns are the system talking. Four identical incidents mean a structure is generating them — something accumulates on a three-week cycle. Auto-restart would just make the ritual automatic."
            },
            {
                "symptom": "Instrumented: one consumer slows down over weeks — a memory leak. Each restart resets the leak's clock.",
                "evidence": [
                    ["Finding", "Consumer-3: memory grows 2%/day, GC pauses lengthen\nAfter ~21 days: pauses exceed the poll timeout -> backup\nRestart resets memory -> 'fix'"]
                ],
                "options": [
                    "Keep restarting — now on a schedule, before 21 days",
                    "Fix the leak, add memory alerting on the consumers, and document the pattern so the next 'mystery backup' gets diagnosed in hours not quarters",
                    "Add more consumers to spread the load",
                    "Restart all consumers weekly as hygiene"
                ],
                "correct": 1,
                "explain": "The restart was treating the symptom on a schedule; the leak is the structure. Fix the leak, alert on the leading indicator (memory growth), and write down the pattern — the next slow-accumulation bug will wear a different costume."
            },
            {
                "symptom": "Leak fixed. The team asks what changes about incident review.",
                "evidence": [
                    ["Ask", "Team: 'How do we stop ritual-fixing?'"]
                ],
                "options": [
                    "Ban restarts",
                    "Add a review rule: any incident fixed by restart twice gets a mandatory structural investigation the third time — events get fixed, patterns get studied",
                    "Require root cause for every incident",
                    "Hire a reliability engineer"
                ],
                "correct": 1,
                "explain": "'Root cause for everything' burns people out on trivia; 'patterns get studied' focuses energy where structure hides. Two restarts is data; the third is an investigation. That is the difference between fighting events and understanding systems."
            }
        ],
        "debrief": "You looked past the event to the pattern, found the accumulating structure, and made pattern-investigation a rule. Systems thinking is refusing to be satisfied with the fix that works but explains nothing.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "Borrowed mental models",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Three problems, three borrowed models: a traffic jam, an epidemic, and a bank run. Match each problem to the model that actually fits — models are tools, not truths.",
        "steps": [
            {
                "symptom": "Problem 1: a rumor about layoffs is spreading through the company, and each person who hears it tells two more.",
                "evidence": [
                    ["Problem 1", "Rumor spreading person-to-person, exponential early growth\nQuestion: how do we slow it?"]
                ],
                "options": [
                    "Traffic-jam model: add more lanes (more communication channels)",
                    "Epidemic model: reduce the transmission rate — address the rumor at the source quickly and visibly, like containing an outbreak",
                    "Bank-run model: freeze all communication"
                ],
                "correct": 1,
                "explain": "Person-to-person exponential spread is epidemic dynamics: the lever is transmission rate. A fast, visible, credible correction at the source works like quarantine — it does not convince everyone, but it slows the spread below the panic threshold."
            },
            {
                "symptom": "Problem 2: deploys queue up behind a single manual approval step, and the queue grows every release day.",
                "evidence": [
                    ["Problem 2", "Single approval bottleneck | queue grows on release days\nQuestion: how do we fix throughput?"]
                ],
                "options": [
                    "Epidemic model: quarantine the approver",
                    "Traffic-jam model: the bottleneck sets the throughput — add lanes (more approvers, or automate the check) instead of pushing more cars at it",
                    "Bank-run model: limit withdrawals (fewer deploys)"
                ],
                "correct": 1,
                "explain": "A single constriction with growing queues is traffic dynamics: throughput is set by the narrowest point. You widen the bottleneck (parallel approvers, automated checks) — pushing harder upstream just lengthens the jam."
            },
            {
                "symptom": "Problem 3: users are withdrawing funds after a scary headline, and each withdrawal makes the next user more nervous.",
                "evidence": [
                    ["Problem 3", "Withdrawals accelerate as others withdraw\nQuestion: how do we stop the spiral?"]
                ],
                "options": [
                    "Traffic-jam model: open more teller windows",
                    "Bank-run model: break the feedback loop — credible assurance plus visible liquidity, because the spiral is driven by others' behavior, not the underlying facts",
                    "Epidemic model: quarantine the worriers"
                ],
                "correct": 1,
                "explain": "Self-reinforcing panic is bank-run dynamics: the loop is 'others withdrawing -> I should too.' The fix targets the loop itself — credible, visible assurance that breaks the reinforcement. Facts alone do not stop a run; breaking the feedback does."
            }
        ],
        "debrief": "You matched the model to the dynamics: epidemics for spread, traffic for bottlenecks, bank runs for panic loops. Mental models are borrowed lenses — the skill is picking the right one, and knowing when none of them fit.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-siem-1",
        "title": "Watch for reinforcing patterns",
        "console": "siem-dashboard",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Feedback loops show up in telemetry before they show up in outages. Create a detection rule named 'feedback-loop-watch' for reinforcing patterns, then acknowledge ALT-103 (unusual outbound volume) so it is being worked.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a detection rule named 'feedback-loop-watch'.",
                "validate": {"action": "create-rule", "params": {"name": "feedback-loop-watch"}},
                "hint": "Open Detection rules: NAME=feedback-loop-watch, QUERY describing a reinforcing pattern (any descriptive query works)."
            },
            {
                "id": "t2",
                "instruction": "Acknowledge alert ALT-103.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-103"}},
                "hint": "Click Ack on the ALT-103 row (Unusual outbound volume)."
            }
        ],
        "debrief": "Name the pattern, watch for it, work what fires. Detection rules are mental models made executable."
    },
    {
        "id": f"{SLUG}-csim-tick-1",
        "title": "Log the second-order review",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 1,
        "brief": "A cache change is proposed. Open a ticket for the second-order effects review, then add a note to INC-9001 recording the loop you are watching for.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a ticket titled 'Second-order review: cache change' with priority P3.",
                "validate": {"action": "create-ticket", "params": {"title": "Second-order review: cache change", "priority": "P3"}},
                "hint": "Open New ticket: TITLE='Second-order review: cache change', PRIORITY=P3."
            },
            {
                "id": "t2",
                "instruction": "Add a note to INC-9001: 'Watching for retry amplification loop.'",
                "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "Watching for retry amplification loop."}},
                "hint": "Add a note on INC-9001 with the exact text about the retry loop."
            }
        ],
        "debrief": "Second-order effects get tickets and notes like everything else. What gets written down gets watched."
    },
    {
        "id": f"{SLUG}-csim-web-1",
        "title": "Start the decision journal",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Systems thinkers keep decision journals: what you decided, why, and what you expected. Set the journal title and owner, then submit it.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the site_name field to 'Decision journal'.",
                "validate": {"action": "set-field", "params": {"id": "site_name", "value": "Decision journal"}},
                "hint": "Set field: FIELD=site_name, VALUE='Decision journal'."
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
        "debrief": "A decision journal turns hindsight into foresight: write the expectation down, and reality gets to grade you later."
    },
    {
        "id": f"{SLUG}-csim-git-1",
        "title": "Publish the mental model",
        "console": "git-host",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You wrote up the feedback-loop model from the outage. Create a branch models/feedback-loops, then comment on PR #1 linking the writeup for the team.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a branch named models/feedback-loops.",
                "validate": {"action": "create-branch", "params": {"name": "models/feedback-loops"}},
                "hint": "Open Branches and create: NAME=models/feedback-loops."
            },
            {
                "id": "t2",
                "instruction": "Add a comment to PR #1: 'Feedback-loop writeup linked for review.'",
                "validate": {"action": "add-comment", "params": {"pr": 1, "text": "Feedback-loop writeup linked for review."}},
                "hint": "Comment on PR #1 with the exact text."
            }
        ],
        "debrief": "Models shared are models improved. Publishing the writeup invites the correction you did not think of."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Map the territory",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Every system map starts with the territory as it is, not as you assume. Read the host mappings — what does this machine believe about its network?",
        "objectives": ["Read the host map"],
        "checks": [
            {
                "command_pattern": "^cat\\s+/etc/hosts$",
                "expect_contains": "10.0.0.8",
                "hint": "Run: cat /etc/hosts — map before you model."
            }
        ],
        "success_message": "Territory mapped. Models built on unmapped territory are fiction."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Number the evidence",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Patterns need positions: find the ERROR lines in logs/app.log with their line numbers, so the timeline has anchors.",
        "objectives": ["Find numbered ERROR lines"],
        "checks": [
            {
                "command_pattern": "^grep\\s+-n\\s+ERROR\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep -n ERROR logs/app.log — the -n flag numbers the evidence."
            }
        ],
        "success_message": "Evidence numbered. A pattern with positions is a timeline; without them it is a rumor."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "See the whole loop",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Feedback loops hide in the middle of timelines. Read the first three lines of logs/app.log, then the last two — see the whole arc before you name the pattern.",
        "objectives": ["Read the start", "Read the end"],
        "checks": [
            {
                "command_pattern": "^head\\s+-n\\s+3\\s+logs/app\\.log$",
                "expect_contains": "server starting",
                "hint": "Run: head -n 3 logs/app.log — where did the arc begin?"
            },
            {
                "command_pattern": "^tail\\s+-n\\s+2\\s+logs/app\\.log$",
                "expect_contains": "timeout after 30s",
                "hint": "Run: tail -n 2 logs/app.log — where did it end?"
            }
        ],
        "success_message": "Whole arc seen. Loops are invisible from any single point — step back to see them."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Anchor your map",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A system map is only useful if it is the current one. Hash the token 'baseline-ok' and confirm digest ff2364c94eb5899f1dabdc3895cc5d56d36f1ce7a3a998132c7eb23156779fe1 — anchor the map before you reason from it.",
        "objectives": ["Hash the anchor token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+baseline-ok$",
                "expect_contains": "ff2364c94eb5899f1dabdc3895cc5d56d36f1ce7a3a998132c7eb23156779fe1",
                "hint": "Run: sha256sum baseline-ok — verify the anchor character for character."
            }
        ],
        "success_message": "Map anchored. Reason from verified ground, not assumed ground."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Name the loop",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Unnamed patterns cannot be discussed. State the pattern you have been studying with echo — use the word 'reinforcing' in your statement.",
        "objectives": ["State the pattern"],
        "checks": [
            {
                "command_pattern": "^echo\\s+.*reinforcing.*$",
                "expect_contains": "reinforcing",
                "hint": "Run: echo with a sentence naming the reinforcing loop (e.g. echo \"retries form a reinforcing loop\")."
            }
        ],
        "success_message": "Pattern named. What gets named gets noticed — by you and by the team."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Question your assumptions",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You assume you know what is running here. Verify: list the processes and compare against your mental model — the gap between assumed and actual is where surprises live.",
        "objectives": ["List actual processes"],
        "checks": [
            {
                "command_pattern": "^ps$",
                "expect_contains": "python3 app.py",
                "hint": "Run: ps — what is actually running versus what you assumed?"
            }
        ],
        "success_message": "Assumptions checked against reality. The map is not the territory — verify the territory."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Trace the dependencies",
        "domain_id": D,
        "difficulty": 3,
        "brief": "No system stands alone. Verify this machine's two most basic dependencies: that it can reach the network (ping) and that names resolve (dig). Hidden coupling starts with untested basics.",
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
        "success_message": "Dependencies traced and verified. Systems fail at the couplings nobody tested."
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
