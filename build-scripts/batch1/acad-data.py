#!/usr/bin/env python3
"""Batch 1 builder: acad-data — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-data'
D = 'acad-data'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The dirty CSV",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The nightly pipeline failed at 2 AM. The error says 'malformed row 48,211.' The dashboard the CEO checks at 8 AM is now stale. Fix the pipeline without corrupting the data.",
        "steps": [
            {
                "symptom": "Pipeline failed on row 48,211 of the customer export. The file came from a vendor.",
                "evidence": [
                    ["Pipeline error", "Row 48,211: expected 12 columns, found 14\nSource: vendor export customers_2026-10-07.csv\nDownstream: CEO dashboard (stale since 02:00)"]
                ],
                "options": [
                    "Delete row 48,211 and re-run",
                    "Inspect the row first: quoted commas or embedded newlines are the usual cause — then fix the parser, not the data",
                    "Re-run the pipeline and hope it was transient",
                    "Ask the vendor for a new file and wait"
                ],
                "correct": 1,
                "explain": "Malformed rows are usually a parsing problem, not a data problem: quoted fields containing commas, or embedded newlines splitting one row into two. Deleting the row destroys evidence (and maybe a real customer); fixing the parser fixes every future file too."
            },
            {
                "symptom": "Confirmed: the vendor wraps addresses in quotes, and some contain commas. The parser was splitting on every comma.",
                "evidence": [
                    ["Row sample", '48210,"Acme, Inc.",...  <- quoted comma\nParser: naive split(",") -> 14 columns instead of 12']
                ],
                "options": [
                    "Switch to a proper CSV parser that respects quoting, add a schema check (12 columns), and quarantine bad rows instead of failing the whole run",
                    "Tell the vendor to stop using commas in addresses",
                    "Keep the naive split but skip quoted rows",
                    "Process the file by hand in a spreadsheet"
                ],
                "correct": 0,
                "explain": "Real CSV parsing respects quoting — that is what the format is for. And pipelines should degrade gracefully: schema-check every row, quarantine the bad ones for review, and let the good 48,210 flow. One bad row should never hold a dashboard hostage."
            },
            {
                "symptom": "Pipeline is green. The CEO asks why the dashboard was stale this morning.",
                "evidence": [
                    ["Ask", "CEO: 'The numbers were frozen at 2 AM. What happened?'"]
                ],
                "options": [
                    "'The vendor sent us a bad file.'",
                    "'A malformed vendor row failed the load; we fixed the parser, quarantined the bad rows for review, and added alerting so the next failure pages us instead of greeting you at 8 AM.'",
                    "'These things happen with data.'",
                    "Blame the vendor by name in the all-hands"
                ],
                "correct": 1,
                "explain": "Data incidents get the same honest treatment as outages: what broke, what you changed, and what prevents recurrence. 'The vendor sent a bad file' is true but useless — the fix is yours to own."
            }
        ],
        "debrief": "You diagnosed the parser instead of blaming the data, built graceful degradation into the pipeline, and reported honestly. Messy data is the job — pipelines that survive it are the skill.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Correlation is not causation",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Marketing found it: ice-cream sales and signup spikes move together (r=0.91). They want the all-hands slide to say 'ice cream drives signups.' You own the data. Decide what the chart can honestly say.",
        "steps": [
            {
                "symptom": "The correlation is real: r=0.91 over 12 months. Marketing wants a causal claim for the campaign.",
                "evidence": [
                    ["Analysis", "ice_cream_sales vs signups, monthly, n=12\nPearson r = 0.91, p < 0.01\nMarketing draft: 'Ice cream drives signups — summer campaign approved'"]
                ],
                "options": [
                    "Approve the causal claim — the numbers back it",
                    "Block the causal claim: check for a confounder first (season is the obvious one), and report only what the data supports",
                    "Ask for a bigger sample before deciding",
                    "Let marketing say whatever sells"
                ],
                "correct": 1,
                "explain": "A strong correlation with an obvious confounder — summer drives both — is the textbook trap. The honest move is to test the confounder (seasonality) before anyone prints a causal claim. r=0.91 tells you they move together; it says nothing about why."
            },
            {
                "symptom": "Seasonality confirmed: both series peak in summer, flat otherwise. Within-season correlation is 0.12.",
                "evidence": [
                    ["Deconfounded", "Within-month correlation: r = 0.12 (noise)\nDriver: summer season -> more outings -> both rise"]
                ],
                "options": [
                    "Publish the 0.91 anyway — it is technically accurate",
                    "Report the honest finding: 'No meaningful relationship after accounting for season. Do not base the campaign on this.'",
                    "Bury the analysis so marketing is not embarrassed",
                    "Find a different variable that correlates and pitch that"
                ],
                "correct": 1,
                "explain": "Technically-accurate-but-misleading is still misleading. Your job is the honest finding, delivered plainly, with the evidence attached. Killing a bad campaign with data is one of the highest-value things an analyst does."
            },
            {
                "symptom": "Marketing is disappointed. They ask what analysis WOULD support a campaign decision.",
                "evidence": [
                    ["Ask", "Marketing: 'Fine — what should we measure instead?'"]
                ],
                "options": [
                    "'Nothing — data cannot help marketing.'",
                    "Propose a real test: run the campaign in half the regions (randomized), compare signup lift against control, and pre-register the success metric before launch",
                    "Suggest a bigger correlational study",
                    "Tell them to trust their gut"
                ],
                "correct": 1,
                "explain": "Do not just kill the bad analysis — replace it with a good one. A randomized regional rollout with a pre-registered metric turns 'does it work?' from an argument into an experiment. That is the analyst's real product: better questions, answered honestly."
            }
        ],
        "debrief": "You caught the confounder, refused to launder correlation into causation, and replaced the bad analysis with an experiment. Data literacy is mostly the discipline to say 'not proven' when everyone wants a story.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "PII in the warehouse",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Routine audit, routine horror: the analytics warehouse has unmasked emails and phone numbers in three tables that 40 analysts can query. Respond — carefully, because the data is already everywhere.",
        "steps": [
            {
                "symptom": "Three warehouse tables contain plaintext PII. Forty analysts have query access. The tables feed six dashboards.",
                "evidence": [
                    ["Audit finding", "Tables: users_raw, events_raw, support_tickets\nPII: email + phone, unmasked | access: 40 analysts\nDownstream: 6 dashboards, 2 vendor exports"]
                ],
                "options": [
                    "Delete the tables immediately",
                    "Contain first: revoke broad access to a need-to-know group, mask the columns, then trace every downstream copy before deciding on deletion",
                    "Email all 40 analysts asking them to delete any exports",
                    "Do nothing — the data was collected legitimately"
                ],
                "correct": 1,
                "explain": "You cannot un-spread data, so you sequence it: stop the spread (narrow access, mask columns), map where it already went (dashboards, exports), then remediate. Immediate deletion destroys the evidence of exposure and breaks six dashboards with no plan."
            },
            {
                "symptom": "Contained. Now: who accessed the PII, and was any of it exfiltrated?",
                "evidence": [
                    ["Query logs", "90 days of query history available\n2 vendor exports included the PII columns\n1 analyst downloaded 2M rows last month (says it was for a churn model)"]
                ],
                "options": [
                    "Assume the downloads were innocent",
                    "Review the query logs against business justification, interview the analyst, notify legal/compliance, and follow the incident process",
                    "Fire the analyst who downloaded the rows",
                    "Delete the query logs to limit liability"
                ],
                "correct": 1,
                "explain": "PII exposure is a governance incident, not just a technical one: legal and compliance own the notification decisions, and the query logs are evidence — you preserve them, not purge them. The analyst gets a fair review, not a summary judgment."
            },
            {
                "symptom": "Incident closed. Build the system that prevents the next one.",
                "evidence": [
                    ["Goal", "PII never lands unmasked in the warehouse again"]
                ],
                "options": [
                    "Ban analysts from querying raw tables",
                    "Classify data at ingestion, mask PII by default with an approval flow for unmasking, and add automated PII detection to the pipeline",
                    "Trust the team to be careful now",
                    "Move the warehouse on-premises"
                ],
                "correct": 1,
                "explain": "Governance that works is built into the pipeline: classification at ingestion, masking by default, unmasking by approval, and automated detection as the backstop. 'Be careful' is not a control; a masked-by-default warehouse is."
            }
        ],
        "debrief": "You contained before purging, treated exposure as a governance incident with evidence preserved, and built masking into the pipeline. Data governance is not paperwork — it is architecture.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "The metric that moved",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Activation rate dropped 12 points overnight. Product wants to roll back yesterday's release. But the release touched nothing near activation. Find out what actually moved.",
        "steps": [
            {
                "symptom": "Activation: 64% -> 52% overnight. Yesterday's release changed the billing page only.",
                "evidence": [
                    ["Dashboard", "Activation rate: 64% -> 52% (overnight)\nYesterday's release: billing page copy changes only\nProduct: 'Roll it back now.'"]
                ],
                "options": [
                    "Roll back the billing release immediately",
                    "Check the metric definition and pipeline first — a 12-point overnight move with no plausible cause smells like a measurement change, not a product change",
                    "Blame seasonality",
                    "Wait a week to see if it recovers"
                ],
                "correct": 1,
                "explain": "When the cause cannot plausibly produce the effect, suspect the measurement. Metric definitions, pipeline filters, and event instrumentation change silently — and a broken funnel definition moves the number without moving reality."
            },
            {
                "symptom": "Found it: the analytics SDK update last night renamed the 'activated' event. The funnel counts the old name. Real activations are flat.",
                "evidence": [
                    ["Root cause", "SDK 4.2 renamed event 'activated' -> 'activation_completed'\nFunnel definition: still counts 'activated' (old name)\nTrue activations: flat at 64%"]
                ],
                "options": [
                    "Fix the funnel to count both event names, backfill, and add an event-schema contract test to CI",
                    "Rename the event back in the SDK",
                    "Tell product the metric was wrong and move on",
                    "Freeze all SDK updates"
                ],
                "correct": 0,
                "explain": "Fix the definition (count both names during transition), backfill the history so trends stay true, and add a contract test so the next rename breaks CI instead of the dashboard. Metrics are code — they get tests like code."
            },
            {
                "symptom": "Metric restored. Product still wants someone to blame for the scare.",
                "evidence": [
                    ["Ask", "Product: 'Whose fault was the bad number?'"]
                ],
                "options": [
                    "Blame the SDK team",
                    "'Nobody's — and that's the point. The system allowed a silent metric break. We fixed the definition, backfilled, and added contract tests. The scare is now impossible to repeat.'",
                    "Blame the analyst who built the funnel",
                    "Promise it will never happen again"
                ],
                "correct": 1,
                "explain": "Metric incidents get the blameless treatment too: the failure was systemic (no contract between SDK and funnel), and the fix is systemic. 'Never happen again' is a promise you cannot keep; 'cannot happen silently again' is one you can."
            }
        ],
        "debrief": "You suspected the measurement before the product, fixed the definition with backfill, and turned a scare into contract tests. When a metric moves impossibly, check the ruler before the thing being measured.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "To publish or not",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The research team wants to publish an 'anonymized' dataset of user behavior. You can see the quasi-identifiers from here. Decide whether it ships.",
        "steps": [
            {
                "symptom": "The dataset is 'anonymized': names removed, but zip code, birth date, and gender remain. 50,000 rows.",
                "evidence": [
                    ["Dataset", "Rows: 50,000 | removed: names, emails\nKept: zip code, birth date, gender, behavior events\nClaim: 'anonymized'"]
                ],
                "options": [
                    "Approve — names are gone, so it is anonymous",
                    "Reject as-is: zip + birth date + gender uniquely identifies most Americans (the classic re-identification result). Require k-anonymity or aggregation first",
                    "Approve but add a terms-of-service banning re-identification",
                    "Publish only the summary statistics"
                ],
                "correct": 1,
                "explain": "Removing names is not anonymization — it is pseudonymization theater. The famous result stands: a handful of quasi-identifiers re-identify most people. A ToS ban on re-identification is a legal fig leaf, not a technical protection."
            },
            {
                "symptom": "The researchers push back: 'We need row-level data for the analysis. Aggregation kills the research.'",
                "evidence": [
                    ["Pushback", "Researchers: 'Row-level or the paper dies.'"]
                ],
                "options": [
                    "Cave and publish the rows",
                    "Offer the middle path: a governed research enclave (query access, no downloads, audited) or differential-privacy release with a stated epsilon budget",
                    "Tell them to find another dataset",
                    "Publish and hope nobody re-identifies"
                ],
                "correct": 1,
                "explain": "The honest negotiation: row-level utility without row-level exposure. A governed enclave or differential privacy gives researchers real analytical power with real privacy math. 'Publish and hope' is not a governance position."
            },
            {
                "symptom": "A release path is agreed. What do you document?",
                "evidence": [
                    ["Requirement", "Document the release decision for the audit trail"]
                ],
                "options": [
                    "Nothing — the decision is made",
                    "Document the privacy review: the re-identification risk found, the mitigation chosen, the epsilon budget or enclave controls, and the approval signatures",
                    "Write 'approved by data team'",
                    "Delete the original dataset to be safe"
                ],
                "correct": 1,
                "explain": "Privacy decisions are auditable decisions: what risk you found, what mitigation you chose, who approved it. If a regulator or a researcher asks in two years, the doc — not your memory — is the answer."
            }
        ],
        "debrief": "You recognized quasi-identifiers for what they are, negotiated a real privacy-preserving path, and documented the decision. Data ethics is not saying no — it is finding the yes that does not harm people.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-sql-1",
        "title": "Model the signups table",
        "console": "sql-studio",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The analytics project needs a signups table. Create it with an id, email, and created_at — then index the email column, because every lookup will filter on it.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a table named signups with columns: id INTEGER, email TEXT, created_at TEXT.",
                "validate": {"action": "create-table", "params": {"name": "signups", "columns": "id INTEGER, email TEXT, created_at TEXT"}},
                "hint": "Create table: NAME=signups, COLUMNS='id INTEGER, email TEXT, created_at TEXT'."
            },
            {
                "id": "t2",
                "instruction": "Create an index on the email column of signups.",
                "validate": {"action": "create-index", "params": {"table": "signups", "column": "email"}},
                "hint": "Create index: TABLE=signups, COLUMN=email — index what you filter on."
            }
        ],
        "debrief": "Schema first, indexes on the access patterns. A table modeled around its queries stays fast as it grows."
    },
    {
        "id": f"{SLUG}-csim-sql-2",
        "title": "Count what matters",
        "console": "sql-studio",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The stakeholder asks 'how many signups this week?' Write a query that counts rows in the signups table — the console validates that your SQL actually performs a COUNT.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Run a SQL query that counts the rows in signups (use COUNT).",
                "validate": {"action": "run-query", "params": {"match": "COUNT"}},
                "hint": "Type a query containing COUNT, e.g. SELECT COUNT(*) FROM signups — the console checks your SQL contains COUNT."
            }
        ],
        "debrief": "Every metric is a query. Writing the COUNT yourself — instead of trusting a dashboard — is how you know what the number actually means."
    },
    {
        "id": f"{SLUG}-csim-db-1",
        "title": "Provision the analytics database",
        "console": "db-admin",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The analytics team needs its own database with least-privilege access. Create the analytics database, add a read-only user analyst_ro, and grant them SELECT only.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a database named analytics.",
                "validate": {"action": "create-database", "params": {"name": "analytics"}},
                "hint": "Create database: NAME=analytics."
            },
            {
                "id": "t2",
                "instruction": "Create a user named analyst_ro.",
                "validate": {"action": "create-user", "params": {"name": "analyst_ro"}},
                "hint": "Create user: NAME=analyst_ro."
            },
            {
                "id": "t3",
                "instruction": "Grant SELECT on analytics to analyst_ro.",
                "validate": {"action": "grant-priv", "params": {"db": "analytics", "user": "analyst_ro", "priv": "SELECT"}},
                "hint": "Grant privilege: DB=analytics, USER=analyst_ro, PRIV=SELECT — read-only, nothing more."
            }
        ],
        "debrief": "Databases get owners, users get least privilege. analyst_ro can read and analyze — and cannot accidentally drop anything."
    },
    {
        "id": f"{SLUG}-csim-db-2",
        "title": "Back up before the migration",
        "console": "db-admin",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The warehouse migration starts tomorrow. Create the analytics database in this console, then take a backup — migrations without backups are just hope with extra steps.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a database named analytics.",
                "validate": {"action": "create-database", "params": {"name": "analytics"}},
                "hint": "Create database: NAME=analytics."
            },
            {
                "id": "t2",
                "instruction": "Back up the analytics database.",
                "validate": {"action": "backup", "params": {"db": "analytics"}},
                "hint": "Run a backup on the analytics database."
            }
        ],
        "debrief": "Backup before migration, always. The restore you never test is the restore that fails when you need it."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Profile the dataset",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Every analysis starts with profiling: look at the actual data. Preview the first two lines of logs/access.log — what does a record look like?",
        "objectives": ["Preview the first two records"],
        "checks": [
            {
                "command_pattern": "^head\\s+-n\\s+2\\s+logs/access\\.log$",
                "expect_contains": "GET /health",
                "hint": "Run: head -n 2 logs/access.log — profile before you analyze."
            }
        ],
        "success_message": "Dataset profiled. Never analyze data you have not looked at."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Count the rows",
        "domain_id": D,
        "difficulty": 1,
        "brief": "How big is this dataset, really? Count the lines in logs/access.log — sample sizes matter before conclusions.",
        "objectives": ["Count the records"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+logs/access\\.log$",
                "expect_contains": "3 logs/access.log",
                "hint": "Run: wc -l logs/access.log (pass the file; stdin is not simulated)."
            }
        ],
        "success_message": "3 records. Small sample, honest count — conclusions scale with evidence."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Find the failures",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The access log hides a failed request. Search for the 504 status — in data work, the errors are often the most interesting rows.",
        "objectives": ["Find the 504 record"],
        "checks": [
            {
                "command_pattern": "^grep\\s+504\\s+logs/access\\.log$",
                "expect_contains": "504",
                "hint": "Run: grep 504 logs/access.log — filter to the failure."
            }
        ],
        "success_message": "Failure found. Anomalies first — they are where the insight lives."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Read the latest record",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Data goes stale. Check the newest record in logs/access.log — is this dataset fresh enough to trust?",
        "objectives": ["Read the latest record"],
        "checks": [
            {
                "command_pattern": "^tail\\s+-n\\s+1\\s+logs/access\\.log$",
                "expect_contains": "200 48211",
                "hint": "Run: tail -n 1 logs/access.log — check the freshest data point."
            }
        ],
        "success_message": "Latest record read. Freshness is a data quality dimension — check it every time."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Fingerprint the dataset",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Before you share a dataset, fingerprint it. Hash the token 'evidence' and confirm digest ee8250fb76e094b34b471f13a73dbbe51d1ae142e9df59d7c0d31ec20f0a0a8e — reproducible work starts with verifiable inputs.",
        "objectives": ["Hash the dataset token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+evidence$",
                "expect_contains": "ee8250fb76e094b34b471f13a73dbbe51d1ae142e9df59d7c0d31ec20f0a0a8e",
                "hint": "Run: sha256sum evidence — the digest must match character for character."
            }
        ],
        "success_message": "Dataset fingerprinted. If you cannot verify the input, you cannot trust the output."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "State the error rate",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The app log has 2 ERROR lines out of 6 total. Compute the error rate and state it with echo — analysts turn counts into honest numbers.",
        "objectives": ["Compute and state the error rate"],
        "checks": [
            {
                "command_pattern": "^echo\\s+33.*$",
                "expect_contains": "33",
                "hint": "2 of 6 is about 33% — run: echo 33% (or the precise value)."
            }
        ],
        "success_message": "33% stated. A rate without its denominator is a rumor — you knew yours."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Audit every case variant",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Log formats drift: ERROR, Error, error. A case-sensitive audit misses variants and undercounts. Search logs/app.log case-insensitively for complete coverage.",
        "objectives": ["Case-insensitive error search"],
        "checks": [
            {
                "command_pattern": "^grep\\s+-i\\s+error\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep -i error logs/app.log — catch every variant."
            }
        ],
        "success_message": "Full coverage. Data quality means checking the cases you did not think of."
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
