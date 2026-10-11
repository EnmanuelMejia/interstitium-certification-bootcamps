#!/usr/bin/env python3
"""Batch 1 builder: acad-math — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-math'
D = 'acad-math'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The 99% accurate test",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A vendor pitches a threat-detection tool: '99% accurate!' Your CISO wants to buy it for the SOC. You run the numbers. Decide.",
        "steps": [
            {
                "symptom": "The tool is 99% accurate: 99% true-positive rate, 1% false-positive rate. Real attacks are rare: 1 in 10,000 events is an actual attack.",
                "evidence": [
                    ["Vendor claim", "True positive rate: 99% | false positive rate: 1%\nBase rate: 1 real attack per 10,000 events\nCISO: '99% accurate — let's buy it'"]
                ],
                "options": [
                    "Buy it — 99% accuracy speaks for itself",
                    "Run the base-rate math first: with 10,000 events, expect ~1 true alarm and ~100 false alarms — so a positive alert is ~1% likely to be real",
                    "Ask for a demo instead of doing math",
                    "Reject it — no tool is 99% accurate"
                ],
                "correct": 1,
                "explain": "The base rate dominates: 1 true positive drowns in ~100 false positives, so P(attack | alert) is about 1%, not 99%. 'Accuracy' without the base rate is a marketing number. Always multiply by the base rate before you buy — or believe."
            },
            {
                "symptom": "The math is done: 99% 'accurate', ~1% useful. The vendor counters: 'But it catches 99% of real attacks!'",
                "evidence": [
                    ["Counter", "Vendor: 'Missing attacks is worse than false alarms.'\nSOC capacity: 3 analysts, ~40 alerts/day sustainable"]
                ],
                "options": [
                    "Buy it — catching attacks matters most",
                    "Decline on capacity math: ~100 false alarms/day buries 3 analysts, so real attacks get missed in the noise — the tool makes detection worse, not better",
                    "Buy it but turn off the alerts",
                    "Hire 20 more analysts to handle the alerts"
                ],
                "correct": 1,
                "explain": "A detector your team cannot keep up with is not a detector — it is a noise machine that hides the real signal. Expected value includes the cost of acting on the output: 100 false alarms a day at 3 analysts means the 1 true positive dies unread."
            },
            {
                "symptom": "Declined. The CISO asks what a good detection investment looks like.",
                "evidence": [
                    ["Ask", "CISO: 'What should we buy instead?'"]
                ],
                "options": [
                    "'Nothing — detection is hopeless.'",
                    "'Invest where the base rate is favorable: high-signal detections on crown-jewel assets, tuned to our environment, measured by precision in production — not vendor accuracy claims.'",
                    "'The cheapest tool.'",
                    "'Whatever our competitors bought.'"
                ],
                "correct": 1,
                "explain": "Good security spending follows the math: concentrate detection where attacks are likeliest and signals are cleanest, and evaluate on precision in YOUR environment. The lesson generalizes: never buy a rate without asking 'rate of what, out of what?'"
            }
        ],
        "debrief": "You multiplied by the base rate, priced the false alarms in analyst-hours, and redirected the budget to high-signal detection. Base-rate neglect is the most expensive innumeracy in technology.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Expected value of the outage",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A redundancy project costs $80k. Without it, a regional outage costs $500k and happens 'every few years.' Finance wants a yes or no with numbers. Decide with expected value.",
        "steps": [
            {
                "symptom": "Project cost: $80k one-time. Outage cost: $500k per event. Historical frequency: roughly once every 4 years.",
                "evidence": [
                    ["Numbers", "Redundancy: $80k once\nOutage: $500k/event, ~1 per 4 years\nFinance: 'Show me the math'"]
                ],
                "options": [
                    "'$500k is bigger than $80k, so yes.'",
                    "Compute expected annual loss: $500k / 4 = $125k/year. The $80k project pays for itself in under a year of expected loss — yes, with margin",
                    "'Outages are rare, so no.'",
                    "Ask for a consultant's opinion"
                ],
                "correct": 1,
                "explain": "Expected value turns vibes into arithmetic: $125k/year of expected loss versus a one-time $80k. The project pays back in about 8 months of risk. 'Every few years' felt rare; $125k/year does not."
            },
            {
                "symptom": "Finance pushes back: 'Your 1-in-4-years is a guess. What if it is 1 in 10?'",
                "evidence": [
                    ["Challenge", "Finance: 'If the real rate is 1 in 10 years, the math flips.'"]
                ],
                "options": [
                    "Insist the 1-in-4 estimate is right",
                    "Do the sensitivity analysis: at 1 in 10 years the expected loss is $50k/year — still positive over a 2-year horizon, and the break-even rate is 1 in 6.25 years. Show the range, not just the point estimate",
                    "Abandon the project — they might be right",
                    "Find data that supports 1-in-4"
                ],
                "correct": 1,
                "explain": "Point estimates are fragile; ranges are honest. The sensitivity analysis shows the decision survives even pessimistic assumptions (break-even at 1 in 6.25 years). Decisions under uncertainty get ranges, not false precision."
            },
            {
                "symptom": "Approved. But finance adds: 'If no outage happens in 2 years, was the $80k wasted?'",
                "evidence": [
                    ["Ask", "Finance: 'How will we know it was worth it?'"]
                ],
                "options": [
                    "'We won't — that's the deal.'",
                    "'We judge the decision by the information at the time, not the outcome. Fire insurance isn't wasted if the house doesn't burn — and we'll also track leading indicators like failover drill times.'",
                    "'If nothing happens, I'll admit it was wasted.'",
                    "Promise an outage to prove the value"
                ],
                "correct": 1,
                "explain": "Good decisions can have quiet outcomes — that is what insurance means. You evaluate the bet by its expected value at decision time, and you track leading indicators (drill performance) so the capability stays real even when the event stays hypothetical."
            }
        ],
        "debrief": "You priced the risk, stress-tested the estimate, and defended the decision against outcome bias. Expected value is how adults buy down risk.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "The misleading average",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The dashboard says average latency is 120ms — excellent. Users say the app feels broken. Both are telling the truth. Find the statistic that lies.",
        "steps": [
            {
                "symptom": "Mean latency: 120ms. User complaints: 'every few minutes it hangs for seconds.' The dashboard is green.",
                "evidence": [
                    ["Dashboard", "Mean latency: 120ms (SLO: <200ms) — green\nComplaints: periodic multi-second hangs\nSample: 10,000 requests"]
                ],
                "options": [
                    "Trust the dashboard — the users are exaggerating",
                    "Look at the distribution, not the mean: check p95/p99 and the histogram — a good mean can hide a terrible tail",
                    "Lower the SLO to make the dashboard honest",
                    "Add more servers"
                ],
                "correct": 1,
                "explain": "The mean is a liar when distributions skew: 9,900 fast requests and 100 horrible ones average to 'fine.' Users live in the tail, not the mean. Percentiles (p95, p99) describe experience; means describe arithmetic."
            },
            {
                "symptom": "p99 is 4.2 seconds. The histogram shows a clean fast cluster and a long ugly tail — periodic, every few minutes.",
                "evidence": [
                    ["Distribution", "p50: 80ms | p95: 300ms | p99: 4.2s\nPattern: tail spikes every ~5 minutes, then recovers"]
                ],
                "options": [
                    "Report the p99 and call it a day",
                    "Hypothesize from the periodicity: a 5-minute cycle smells like GC pauses, cron jobs, or cache expiry — correlate the spikes with system events",
                    "Average the p99 away with more samples",
                    "Tell users the p99 is acceptable"
                ],
                "correct": 1,
                "explain": "Periodicity is a fingerprint: 5-minute cycles point at scheduled causes (GC, cron, expiry), not random ones. The statistic told you where to look; the pattern tells you what to suspect. Diagnose the tail, not the average."
            },
            {
                "symptom": "Found: a cron job every 5 minutes locks a table the requests need. Fixed. What changes about the dashboard?",
                "evidence": [
                    ["Fix", "Cron rescheduled off-peak, lock removed\np99: 4.2s -> 210ms"]
                ],
                "options": [
                    "Keep the mean dashboard — it is green again",
                    "Replace the mean with p50/p95/p99 on the dashboard, and alert on the tail — the mean hid this for weeks",
                    "Delete the latency dashboard",
                    "Set the SLO on the mean, tighter"
                ],
                "correct": 1,
                "explain": "The dashboard was not wrong, it was the wrong statistic. Percentiles on the dashboard, alerts on the tail: measure what users feel. The mean can stay as a footnote."
            }
        ],
        "debrief": "You distrusted the mean, read the distribution, used periodicity as a fingerprint, and fixed the dashboard's statistic. Averages summarize; percentiles testify.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "A/B test or noise?",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The new checkout flow converted 5.2% vs 4.9% for the old — over 3 days, 2,000 users per side. Product wants to ship it. Is it real?",
        "steps": [
            {
                "symptom": "Variant B: 5.2% (104/2000). Control A: 4.9% (98/2000). Three days of data. Product: 'Ship it, B wins.'",
                "evidence": [
                    ["Test", "A: 98/2000 = 4.9% | B: 104/2000 = 5.2%\nDuration: 3 days | Product: 'B wins, ship it'"]
                ],
                "options": [
                    "Ship B — 5.2 is bigger than 4.9",
                    "Check significance first: a 6-conversion gap on 2,000 users is well within noise — run the test longer or accept you cannot tell",
                    "Ship B but watch it",
                    "Declare the test inconclusive and never test again"
                ],
                "correct": 1,
                "explain": "Six conversions out of two thousand is noise wearing a costume. With this sample size, the standard error swallows the 0.3-point gap — you cannot distinguish B's 'win' from a coin flip. Shipping on noise means shipping randomly."
            },
            {
                "symptom": "You explain it is noise. Product asks: 'How long until we know?'",
                "evidence": [
                    ["Ask", "Product: 'How many users do we need?'"]
                ],
                "options": [
                    "'A few more days should do it.'",
                    "Do the power math: detecting a 0.3-point lift at 5% base needs roughly 100k+ users per side — weeks, not days. Offer the real trade: run longer, accept a bigger minimum effect, or test bigger changes",
                    "'Statistics can't answer that.'",
                    "Peek at the data daily and ship when it looks good"
                ],
                "correct": 1,
                "explain": "Small effects need big samples — that is the iron law. Give the real number (order of 100k per side for a 0.3-point lift) and the real options: longer run, bigger minimum detectable effect, or bolder variants. And never peek-and-ship: peeking inflates false positives."
            },
            {
                "symptom": "The test runs to full power: B wins by 0.4 points, significant. Product wants to ship and move on.",
                "evidence": [
                    ["Result", "B: +0.4pts, p < 0.05, full power\nProduct: 'Ship it'"]
                ],
                "options": [
                    "Ship and forget",
                    "Ship, but record the effect size honestly: a real but small win — and bank the learning about what moves checkout",
                    "Keep testing B variants forever",
                    "Question the p-value"
                ],
                "correct": 1,
                "explain": "Significant is not the same as important: +0.4 points is real and worth shipping, but it is a small win, not a breakthrough. Record the effect size, bank the learning, and keep hunting bigger levers. Statistics tells you it is real; judgment tells you what it is worth."
            }
        ],
        "debrief": "You refused to ship on noise, priced the sample size honestly, and treated significance as the start of judgment, not the end. Most 'wins' are noise — the math tells you which.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "Fermi the migration",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The CTO asks in the hallway: 'Roughly what will the cloud migration cost per month?' You have 30 seconds and no spreadsheet. Estimate like a physicist.",
        "steps": [
            {
                "symptom": "Hallway, CTO, 30 seconds: 'Ballpark the monthly cloud cost for the migration.' You know: ~60 VMs, mostly idle.",
                "evidence": [
                    ["Known", "~60 VMs | mostly idle web/app servers\nCTO wants: order of magnitude, now"]
                ],
                "options": [
                    "'I'll get back to you with a spreadsheet.'",
                    "Fermi it: 60 VMs x ~$50/month average (mix of small sizes, mostly idle) = ~$3k/month compute, double for storage/transfer overhead -> ~$5-10k/month ballpark",
                    "'Probably around a million.'",
                    "'It depends.'"
                ],
                "correct": 1,
                "explain": "Fermi estimation is decomposition with round numbers: count the units, price a typical unit, multiply, add an overhead factor, state the range. $5-10k/month is a decision-useful ballpark in 30 seconds; 'I'll get back to you' is a decision delayed."
            },
            {
                "symptom": "CTO: 'Is that high or low? I need to know if we're in trouble.'",
                "evidence": [
                    ["Follow-up", "CTO: 'Compare it to something.'"]
                ],
                "options": [
                    "'It's just an estimate.'",
                    "Anchor it: 'Current data-center run-rate is ~$25k/month, so $5-10k is a reduction — but the estimate's uncertainty is 2x, and data transfer is the wild card. I'll firm it up this week.'",
                    "'We're definitely fine.'",
                    "Refuse to compare without more data"
                ],
                "correct": 1,
                "explain": "Estimates need anchors and uncertainty bars: compare to the known $25k, state the 2x uncertainty honestly, name the biggest unknown (transfer). A ballpark with error bars beats a precise number built on guesses."
            },
            {
                "symptom": "Back at your desk: how do you firm up the Fermi estimate properly?",
                "evidence": [
                    ["Next step", "Turn the hallway math into a real estimate"]
                ],
                "options": [
                    "Keep the hallway number — it was fine",
                    "Replace each Fermi factor with measured data: actual VM sizes from the inventory, real utilization from monitoring, priced with the provider calculator, plus a 20% contingency",
                    "Ask the vendor for a quote and trust it",
                    "Add 50% to be safe and present that"
                ],
                "correct": 1,
                "explain": "Fermi estimates get refined factor by factor: inventory replaces the VM guess, monitoring replaces the utilization guess, the price calculator replaces the $50 guess. Keep the structure, upgrade the inputs — and keep the contingency explicit, not hidden."
            }
        ],
        "debrief": "You estimated under pressure with round numbers, anchored with uncertainty, and knew exactly how to refine it. Fermi estimation is not guessing — it is structured, upgradable guessing.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-sql-1",
        "title": "Measure the experiment",
        "console": "sql-studio",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The A/B test needs a measurements table. Create it with an id, a value, and a taken_at — then write a query computing the average value. The console checks your SQL actually averages.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a table named measurements with columns: id INTEGER, value REAL, taken_at TEXT.",
                "validate": {"action": "create-table", "params": {"name": "measurements", "columns": "id INTEGER, value REAL, taken_at TEXT"}},
                "hint": "Create table: NAME=measurements, COLUMNS='id INTEGER, value REAL, taken_at TEXT'."
            },
            {
                "id": "t2",
                "instruction": "Run a SQL query that averages the value column (use AVG).",
                "validate": {"action": "run-query", "params": {"match": "AVG"}},
                "hint": "Type a query containing AVG, e.g. SELECT AVG(value) FROM measurements."
            }
        ],
        "debrief": "Schema for the experiment, then the average — but remember the misleading-average simulation: AVG is the start of the analysis, never the end."
    },
    {
        "id": f"{SLUG}-csim-code-1",
        "title": "Breakpoint the accumulator",
        "console": "code-editor",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You are debugging a statistics script. Open app.py and set a breakpoint on line 4 — where the accumulator grows — so you can watch the sum evolve.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Open the file app.py.",
                "validate": {"action": "open-file", "params": {"name": "app.py"}},
                "hint": "Open app.py in the editor."
            },
            {
                "id": "t2",
                "instruction": "Set a breakpoint on line 4 of app.py.",
                "validate": {"action": "toggle-breakpoint", "params": {"file": "app.py", "line": 4}},
                "hint": "Toggle a breakpoint: FILE=app.py, LINE=4 (the accumulator line)."
            }
        ],
        "debrief": "Breakpoints are how you watch math happen. Set them where the state changes — accumulators, loop variables, running totals."
    },
    {
        "id": f"{SLUG}-csim-web-1",
        "title": "File the estimation worksheet",
        "console": "generic-web",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Fermi estimates deserve to be written down. Title the worksheet, set the owner contact, and submit it — estimates with owners get refined; others evaporate.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set the site_name field to 'Estimation worksheet'.",
                "validate": {"action": "set-field", "params": {"id": "site_name", "value": "Estimation worksheet"}},
                "hint": "Set field: FIELD=site_name, VALUE='Estimation worksheet'."
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
        "debrief": "Written estimates beat remembered ones. The worksheet is where the hallway math becomes a plan."
    },
    {
        "id": f"{SLUG}-csim-sql-2",
        "title": "Filter the measurements",
        "console": "sql-studio",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Averages lie when the sample is polluted. Index the taken_at column of measurements for time-window queries, then write a query that filters with WHERE.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create an index on the taken_at column of measurements.",
                "validate": {"action": "create-index", "params": {"table": "measurements", "column": "taken_at"}},
                "hint": "Create index: TABLE=measurements, COLUMN=taken_at."
            },
            {
                "id": "t2",
                "instruction": "Run a SQL query that filters measurements with a WHERE clause.",
                "validate": {"action": "run-query", "params": {"match": "WHERE"}},
                "hint": "Type a query containing WHERE, e.g. SELECT * FROM measurements WHERE value > 100."
            }
        ],
        "debrief": "Filter before you average. The WHERE clause is where data quality lives — every honest analysis starts by defining the sample."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Count the sample",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Statistics starts with n. Count the lines in logs/app.log — every conclusion you draw today rests on this sample size.",
        "objectives": ["Count the sample size"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+logs/app\\.log$",
                "expect_contains": "6 logs/app.log",
                "hint": "Run: wc -l logs/app.log (pass the file; stdin is not simulated)."
            }
        ],
        "success_message": "n = 6. Small sample, known size — conclusions scale with evidence."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Read the sample",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Never analyze data you have not looked at. Preview the first three records of logs/access.log.",
        "objectives": ["Preview the data"],
        "checks": [
            {
                "command_pattern": "^head\\s+-n\\s+3\\s+logs/access\\.log$",
                "expect_contains": "GET /health",
                "hint": "Run: head -n 3 logs/access.log — look before you compute."
            }
        ],
        "success_message": "Sample read. The numbers mean nothing until you have seen the rows."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Weigh the words",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Text is data too. Count the words in notes.txt — quantitative reasoning applies to words as well as numbers.",
        "objectives": ["Count the words"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-w\\s+notes\\.txt$",
                "expect_contains": "56 notes.txt",
                "hint": "Run: wc -w notes.txt — measure the text."
            }
        ],
        "success_message": "56 words. Measure first, characterize second."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Catch every variant",
        "domain_id": D,
        "difficulty": 2,
        "brief": "ERROR, Error, error — case variants hide in real data. Search logs/app.log case-insensitively so your count is complete, not convenient.",
        "objectives": ["Complete case-insensitive count"],
        "checks": [
            {
                "command_pattern": "^grep\\s+-i\\s+error\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep -i error logs/app.log — the -i flag catches every variant."
            }
        ],
        "success_message": "All variants caught. Incomplete counts produce confident wrong answers."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "State the base rate",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The log holds 2 ERROR lines out of 6 total. Compute the base rate and state it with echo — every probability you use later starts here.",
        "objectives": ["Compute and state the base rate"],
        "checks": [
            {
                "command_pattern": "^echo\\s+33.*$",
                "expect_contains": "33",
                "hint": "2 of 6 is about 33% — run: echo 33% (or the precise value)."
            }
        ],
        "success_message": "Base rate stated: ~33%. Write it down — base rates are the first thing people forget and the last thing that matters."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Commit to your estimate",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Fermi estimates get committed, not whispered. Hash the token 'confirm42' and confirm digest 3f3613289908016c540655ae7e24dd32bcd16789ccdfe3ccae559a57eb4bbf40 — commit to the number.",
        "objectives": ["Hash the commitment token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+confirm42$",
                "expect_contains": "3f3613289908016c540655ae7e24dd32bcd16789ccdfe3ccae559a57eb4bbf40",
                "hint": "Run: sha256sum confirm42 — the digest must match character for character."
            }
        ],
        "success_message": "Estimate committed. Numbers you will not sign are numbers you should not use."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Read the tail of the distribution",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Averages hide tails. Read the last three lines of logs/app.log, then pull the numbered ERROR lines — characterize the extreme end of this distribution.",
        "objectives": ["Read the tail", "Number the extremes"],
        "checks": [
            {
                "command_pattern": "^tail\\s+-n\\s+3\\s+logs/app\\.log$",
                "expect_contains": "timeout after 30s",
                "hint": "Run: tail -n 3 logs/app.log — the tail is where the story is."
            },
            {
                "command_pattern": "^grep\\s+-n\\s+ERROR\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep -n ERROR logs/app.log — number the extreme events."
            }
        ],
        "success_message": "Tail characterized. The mean told you nothing; the tail told you everything."
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
