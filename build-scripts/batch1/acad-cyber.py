#!/usr/bin/env python3
"""Batch 1 builder: acad-cyber — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-cyber'
D = 'acad-cyber'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The 2 AM phishing report",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "2:14 AM. The on-call phone buzzes: a finance analyst clicked a link in an email that 'looked like IT'. Work the incident the way a real SOC would — verify first, contain second, learn third.",
        "steps": [
            {
                "symptom": "Analyst: 'I clicked the link. It asked for my login and I typed it in. Is that bad?'",
                "evidence": [
                    ["Ticket #2214", "PHISHING REPORT — user: finance-analyst-02\nClicked link in 'IT password expiry' email | entered credentials\nHost: FIN-1042"]
                ],
                "options": [
                    "Wipe FIN-1042 immediately — scorched earth, questions later",
                    "Verify the email is actually malicious (check the link destination and sender), and force a password reset plus session revocation right away",
                    "Tell the analyst it is probably fine and close the ticket",
                    "Forward the email to the whole company as a warning"
                ],
                "correct": 1,
                "explain": "Verify before you escalate — checking the link destination and sender separates a drill from a breach. But entered credentials are live ammunition: the password dies NOW and the attacker's sessions get revoked with it. Wiping first destroys evidence; dismissing destroys trust."
            },
            {
                "symptom": "The link went to a lookalike domain registered yesterday. The credentials are compromised.",
                "evidence": [
                    ["Verification", "Link destination: it-helpdesk-secure[.]net (registered 2026-10-07)\nSender: spoofed internal display name, external envelope\nVerdict: credential-harvesting phish"]
                ],
                "options": [
                    "Reset the analyst's password and revoke all active sessions",
                    "Only reset the password — sessions expire on their own",
                    "Block the domain and call it done",
                    "Ask the analyst to change the password themselves next week"
                ],
                "correct": 0,
                "explain": "A harvested password stays dangerous until the reset lands AND the attacker's sessions are killed. Session revocation is the step people forget — a reset alone leaves the attacker's already-logged-in session working."
            },
            {
                "symptom": "Contained. Now: three other people received the same email.",
                "evidence": [
                    ["Blast radius", "Same campaign delivered to 4 mailboxes\n1 clicked, 3 unopened"]
                ],
                "options": [
                    "Purge the campaign from all mailboxes and give the three recipients a 60-second briefing",
                    "Do nothing — they did not click",
                    "Name and shame the analyst in the team channel so others learn",
                    "Block all external email company-wide"
                ],
                "correct": 0,
                "explain": "Unexpired threats get removed from every mailbox, and the three recipients get a short briefing while the lesson is fresh. Blame creates silence — the next person who clicks will hide it instead of reporting it."
            }
        ],
        "debrief": "You verified before panicking, killed the compromised credentials and sessions, swept the campaign from every mailbox, and kept the reporter as an ally. That is the defensive loop: detect, verify, contain, learn.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Isolate or observe?",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "EDR flags a developer laptop: a new process is beaconing to an unknown IP every 60 seconds. The developer is mid-demo for a client. Isolate the host now, or watch and gather intelligence? There is no free choice — pick, and own it.",
        "steps": [
            {
                "symptom": "Beaconing detected: 60-second intervals to an unknown external IP. The laptop's owner presents to a client in 20 minutes.",
                "evidence": [
                    ["EDR alert", "ALERT-8812 | host: DEV-2207 | process: updater-svc.exe (unsigned)\nBeacon: 60s interval -> 185.220.101.4 | first seen 40 min ago\nUser: client demo at 10:00"]
                ],
                "options": [
                    "Isolate the host now — kill the demo if you have to",
                    "Let the demo finish, then isolate — 20 minutes will not matter",
                    "Watch silently and collect a full packet capture first",
                    "Remote-wipe the laptop immediately"
                ],
                "correct": 0,
                "explain": "A 60-second beacon to an unknown IP from an unsigned binary is active compromise until proven otherwise. Twenty more minutes of beaconing is twenty minutes of exfiltration. You can explain a dead demo; you cannot un-exfiltrate source code."
            },
            {
                "symptom": "Host isolated. Forensics: the 'updater' was a trojanized build tool downloaded from a forum. It exfiltrated 40 MB before isolation.",
                "evidence": [
                    ["Forensics", "updater-svc.exe: trojanized toolchain, downloaded from a forum link\nExfiltrated ~40 MB before isolation | contained to DEV-2207"]
                ],
                "options": [
                    "Rotate the developer's credentials, scope what the 40 MB touched, and brief the team honestly",
                    "Reimage and move on — 40 MB is nothing",
                    "Escalate to fire the developer for downloading from a forum",
                    "Keep it quiet to avoid alarming the client"
                ],
                "correct": 0,
                "explain": "Isolation stops the bleeding; it does not undo it. You scope what left the building, rotate everything the host touched, and tell the team the true story — quiet cover-ups are how the next incident starts."
            },
            {
                "symptom": "The client asks why the demo died mid-call.",
                "evidence": [
                    ["Comms", "Client: 'Your engineer just vanished from the call. Is everything alright?'"]
                ],
                "options": [
                    "'We detected a security event and contained it — the demo is rescheduled, and your data was not involved'",
                    "Say it was technical difficulties",
                    "Give the client the full forensic detail",
                    "Blame the developer by name"
                ],
                "correct": 0,
                "explain": "Honest, bounded, professional: name the category (security event), the action (contained), the impact boundary (their data not involved), and the next step (reschedule). Clients respect containment; they punish discovered lies."
            }
        ],
        "debrief": "You chose containment over comfort, scoped the real damage instead of hoping, and communicated honestly with the client. Incident response is a series of uncomfortable right calls — this was three of them.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "The shared admin password",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 1,
        "brief": "During a routine review you find it: one admin password, shared by six people, unchanged in two years, sitting in a chat channel. Nobody 'owns' it. Respond like the adult in the room.",
        "steps": [
            {
                "symptom": "The shared credential is confirmed: six users, one password, posted in a chat channel two years ago.",
                "evidence": [
                    ["Finding", "Account: svc-admin | shared by 6 engineers\nLast rotated: 2024 (never) | location: #ops-general chat history\nScope: production database + hypervisor console"]
                ],
                "options": [
                    "Rotate the password immediately, then tell everyone the new value in the same chat",
                    "Rotate the password immediately into a vault, issue individual accounts, and retire the shared one",
                    "Leave it — changing it might break someone's workflow",
                    "Email the password to all six people so everyone has the new one"
                ],
                "correct": 1,
                "explain": "Rotate first, because every hour it lives is another hour of un-attributable access. But the new secret goes in a vault with individual accounts — replacing one shared password with another just resets the clock on the same problem."
            },
            {
                "symptom": "The password is rotated and vaulted. Two engineers complain the new individual logins are 'slower'.",
                "evidence": [
                    ["Feedback", "eng-03: 'It takes me 30 extra seconds to check out the credential.'\neng-05: 'Can we just get the old one back for emergencies?'"]
                ],
                "options": [
                    "Restore the shared password for emergencies",
                    "Hold the line, explain that attribution is the point, and streamline the vault checkout flow",
                    "Exempt senior engineers from the new process",
                    "Stop talking about it and hope the complaints fade"
                ],
                "correct": 1,
                "explain": "Friction complaints are real — so you reduce the friction (faster vault checkout, SSO) instead of restoring the risk. The moment you carve out exceptions, the shared-password culture is back with extra steps."
            },
            {
                "symptom": "Now you must make sure this does not happen again.",
                "evidence": [
                    ["Goal", "Prevent the next shared credential from living two years in a chat channel"]
                ],
                "options": [
                    "Run a one-time scan for secrets in chat history and add a recurring secret-scan to the pipeline",
                    "Send a reminder email about password policy",
                    "Punish whoever posted it originally",
                    "Ban chat channels"
                ],
                "correct": 0,
                "explain": "Culture follows tooling: an automated secret-scan that catches the next one on day one beats a policy email everyone forgets by Friday. Detect the pattern, not the person."
            }
        ],
        "debrief": "You rotated without re-sharing, held the line on individual accountability while reducing friction, and built detection instead of blame. That is how a shared-password culture actually dies.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "Patch Tuesday standoff",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "A critical remote-code-execution flaw drops at noon. One internet-facing server is vulnerable — and there is a change freeze for tomorrow's product launch. Patch now and risk the launch, or hold and risk the breach?",
        "steps": [
            {
                "symptom": "CVE lands with a 9.8 score and a public exploit. The vulnerable service faces the internet. The launch freeze started yesterday.",
                "evidence": [
                    ["Advisory", "CVE-2026-44112 | CVSS 9.8 | RCE | public exploit published\nAffected: public-facing API gateway (1 host)\nChange freeze: in effect until launch, tomorrow 09:00"]
                ],
                "options": [
                    "Patch immediately — freeze or no freeze",
                    "First verify actual exposure: is the vulnerable code path reachable, is there a compensating control?",
                    "Hold the patch until after the launch",
                    "Take the API gateway offline until the launch is over"
                ],
                "correct": 1,
                "explain": "A 9.8 with a public exploit demands urgency, not panic. Verify exposure first: an unreachable code path or a WAF rule in front of it changes the math completely. You cannot make the patch-vs-launch call without knowing the real risk."
            },
            {
                "symptom": "Exposure confirmed: the vulnerable endpoint is reachable, no WAF in front of it. Scans from the internet started 20 minutes ago.",
                "evidence": [
                    ["Telemetry", "Vulnerable endpoint: reachable from internet\nInbound scanning for the exploit signature: started 20 min ago\nNo WAF or compensating control in path"]
                ],
                "options": [
                    "Declare an emergency change, patch now, accept the launch risk",
                    "Wait for the vendor's official patch next week",
                    "Block the exploit signature at the edge as a stopgap and patch in the emergency window tonight",
                    "Hope the scanners are just researchers"
                ],
                "correct": 2,
                "explain": "Both risks are real, so you sequence them: a signature block at the edge buys hours (imperfect but immediate), and the real patch lands in tonight's emergency window. 'Patch now and break the launch' and 'hold and get breached' are both failure modes — the stopgap is the third option."
            },
            {
                "symptom": "The launch team demands a plain-English answer: why are you touching production during the freeze?",
                "evidence": [
                    ["Ask", "Launch lead: 'Explain to me like I am the CEO: why does this override the freeze?'"]
                ],
                "options": [
                    "Quote the CVSS score and the CVE number",
                    "'Attackers are scanning us right now for a flaw that lets them run code on our gateway. We put a shield up and we patch tonight — the launch is protected, not threatened.'",
                    "Refuse to explain — security decisions are not debatable",
                    "Promise the launch will be unaffected"
                ],
                "correct": 1,
                "explain": "Risk translated into business language: who is attacking, what they get, what you did, what happens next. CVSS numbers do not move executives; 'they can run code on our front door and we are handling it tonight' does."
            }
        ],
        "debrief": "You verified exposure before choosing, sequenced a stopgap ahead of the real fix, and translated the risk into language the business could act on. That is vulnerability management under pressure.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "The vendor wants the keys",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A new analytics vendor wants production database access with a shared service account and no expiry. The contract is signed; the business wants the dashboards live this week. Decide the access model.",
        "steps": [
            {
                "symptom": "The vendor's onboarding doc asks for: a production DB login, shared service account, full read on all tables, no expiry.",
                "evidence": [
                    ["Vendor request", "Access: production database, all tables, read\nAccount: single shared 'vendor_svc' login\nExpiry: none requested | MFA: not supported by their tooling"]
                ],
                "options": [
                    "Grant it as requested — the contract is signed and the business is waiting",
                    "Offer a read replica with a scoped, named, expiring service account and IP allowlisting",
                    "Deny all access and kill the project",
                    "Give them the credentials over a screen share so at least it is not in email"
                ],
                "correct": 1,
                "explain": "Least privilege is a negotiation, not a veto: a read replica (never production), a named account (attribution), an expiry (no forever-keys), and IP allowlisting (their office, not the internet). The dashboards still go live this week — on your terms."
            },
            {
                "symptom": "The vendor pushes back: 'Our tool needs production. The replica lags too much for real-time dashboards.'",
                "evidence": [
                    ["Pushback", "Vendor: 'Replica lag is 30 seconds. Our SLA needs under 5.'"]
                ],
                "options": [
                    "Cave and grant production access",
                    "Measure the actual requirement: is any business decision made on sub-5-second data? Offer a scoped production read on the two needed tables, query-audited",
                    "Tell them to rebuild their tool",
                    "Ignore the pushback and hope they adapt"
                ],
                "correct": 1,
                "explain": "Challenge the requirement with data: almost no dashboard decision needs 5-second freshness, but if it genuinely does, you narrow production access to the two tables that need it — with every query logged. Scope follows proven need, not asserted need."
            },
            {
                "symptom": "Access is agreed. Now protect the relationship long-term.",
                "evidence": [
                    ["Ongoing", "Vendor account will exist for the life of the contract"]
                ],
                "options": [
                    "Set a 90-day expiry with a renewal review, alert on anomalous query volume, and document the access in the vendor risk register",
                    "Set it and forget it",
                    "Rotate the password every day to be safe",
                    "Ask the vendor to self-attest annually"
                ],
                "correct": 0,
                "explain": "Third-party access rots: people leave, contracts change, tools get breached. Expiry forces a review, anomaly alerts catch abuse, and the risk register means the next person inherits the context instead of discovering a mystery account."
            }
        ],
        "debrief": "You negotiated least privilege instead of issuing a veto, tested the vendor's real requirements, and built expiry and monitoring into the relationship. Vendor risk management is access design, not access denial.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-fw-1",
        "title": "Default-deny the lab workstation",
        "console": "firewall",
        "domain_id": D,
        "difficulty": 1,
        "brief": "A new lab workstation joins the fleet. Policy is deny-by-default: set the INPUT chain default to DROP, then open exactly one hole — HTTPS (TCP 443) from the corporate network 10.0.0.0/8.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add an ACCEPT rule: chain INPUT, TCP port 443, source 10.0.0.0/8.",
                "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": "443", "source": "10.0.0.0/8", "action": "ACCEPT"}},
                "hint": "Use the Add rule form: CHAIN=INPUT, PROTOCOL=tcp, PORT=443, SOURCE=10.0.0.0/8, ACTION=ACCEPT."
            },
            {
                "id": "t2",
                "instruction": "Set the INPUT chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "INPUT", "policy": "DROP"}},
                "hint": "Open Default policies and set INPUT to DROP — everything not explicitly allowed must fall through to deny."
            }
        ],
        "debrief": "One explicit allow, everything else denied. That is deny-by-default in its purest form: the policy says what may happen, and silence means no."
    },
    {
        "id": f"{SLUG}-csim-fw-2",
        "title": "SSH only from the admin net",
        "console": "firewall",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Audit found SSH open to the world on a jump host. Lock it down: allow TCP 22 only from the admin network 192.168.50.0/24, then set the INPUT default policy to DROP so the old wide-open posture cannot return.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Add an ACCEPT rule: chain INPUT, TCP port 22, source 192.168.50.0/24.",
                "validate": {"action": "add-rule", "params": {"chain": "INPUT", "protocol": "tcp", "port": "22", "source": "192.168.50.0/24", "action": "ACCEPT"}},
                "hint": "Add rule form: CHAIN=INPUT, PROTOCOL=tcp, PORT=22, SOURCE=192.168.50.0/24, ACTION=ACCEPT."
            },
            {
                "id": "t2",
                "instruction": "Set the INPUT chain default policy to DROP.",
                "validate": {"action": "set-default-policy", "params": {"chain": "INPUT", "policy": "DROP"}},
                "hint": "Under Default policies, set INPUT to DROP. The old allow-from-anywhere posture dies with the default."
            }
        ],
        "debrief": "Management-plane services get the smallest possible audience. SSH from one admin network, deny by default — the internet never needs your jump host."
    },
    {
        "id": f"{SLUG}-csim-siem-1",
        "title": "Work the alert queue",
        "console": "siem-dashboard",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Three alerts are sitting open, oldest first. Triage like an analyst: acknowledge the critical malware-hash alert ALT-102, assign it to analyst 'r.okafor', then escalate it to incident response.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Acknowledge alert ALT-102.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-102"}},
                "hint": "In the Alerts table, click Ack on the ALT-102 row (Malware hash match on download)."
            },
            {
                "id": "t2",
                "instruction": "Assign alert ALT-102 to analyst r.okafor.",
                "validate": {"action": "assign-alert", "params": {"id": "ALT-102", "analyst": "r.okafor"}},
                "hint": "Use the Assign alert form: ALERT ID=ALT-102, ANALYST=r.okafor."
            },
            {
                "id": "t3",
                "instruction": "Escalate alert ALT-102 to incident response.",
                "validate": {"action": "escalate", "params": {"id": "ALT-102"}},
                "hint": "Click Escalate on the ALT-102 row — a critical malware match does not sit in the queue."
            }
        ],
        "debrief": "Acknowledge, assign, escalate: the alert is owned, worked, and moved to the team that can contain it. Queues do not clear themselves."
    },
    {
        "id": f"{SLUG}-csim-siem-2",
        "title": "Contain and detect",
        "console": "siem-dashboard",
        "domain_id": D,
        "difficulty": 3,
        "brief": "ALT-103 shows unusual outbound volume from srv-backup-02 — possible exfiltration. Isolate the host now, then write a detection rule so the next one fires faster.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Isolate host srv-backup-02.",
                "validate": {"action": "isolate-host", "params": {"host": "srv-backup-02"}},
                "hint": "Click 'Isolate host' on the ALT-103 row — stop the bleeding before you analyze it."
            },
            {
                "id": "t2",
                "instruction": "Create a detection rule named 'outbound-volume-spike' with a query matching unusual outbound volume.",
                "validate": {"action": "create-rule", "params": {"name": "outbound-volume-spike"}},
                "hint": "Open Detection rules and create a rule: NAME=outbound-volume-spike, QUERY describing unusual outbound bytes (any descriptive query text works)."
            }
        ],
        "debrief": "Contain first, detect forever after. Every real incident should leave a detection rule behind — that is how a SOC gets smarter instead of just busier."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Audit the user database",
        "domain_id": D,
        "difficulty": 1,
        "brief": "A security review starts with knowing who exists. Read the system user database and confirm the candidate account is present with UID 1000.",
        "objectives": ["Read /etc/passwd", "Confirm the candidate account entry"],
        "checks": [
            {
                "command_pattern": "^cat\\s+/etc/passwd$",
                "expect_contains": "candidate:x:1000",
                "hint": "Run: cat /etc/passwd — then look for the candidate account line."
            }
        ],
        "success_message": "Account verified: candidate:x:1000. Every audit starts with an accurate inventory of who can log in."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Triage the application log",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The app.log is noisy. Pull out just the ERROR lines — in an incident, the first skill is filtering signal from noise.",
        "objectives": ["Search logs/app.log for ERROR lines"],
        "checks": [
            {
                "command_pattern": "^grep\\s+ERROR\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep ERROR logs/app.log — one pattern, one file, just the errors."
            }
        ],
        "success_message": "Errors isolated. Triage is a filter, not a reading exercise — grep first, read second."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Verify the evidence hash",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Forensics handed you a token, 'verify-me', and its published SHA-256: d757afa8f14ef7434c81a75fd826537c6b13a8dadd65363b0fd10f1ec2cb211f. Hash the token yourself and confirm it matches — chain of custody starts here.",
        "objectives": ["Compute the SHA-256 of the token", "Confirm it matches the published digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+verify-me$",
                "expect_contains": "d757afa8f14ef7434c81a75fd826537c6b13a8dadd65363b0fd10f1ec2cb211f",
                "hint": "Run: sha256sum verify-me — the output digest must match the published value character for character."
            }
        ],
        "success_message": "Hash matches — the evidence is intact. Never trust a file you have not verified."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Inventory the workspace",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Before you touch anything, know what is here. List the home directory, then read the study notes to see what this workstation is for.",
        "objectives": ["List the home directory contents", "Read notes.txt"],
        "checks": [
            {
                "command_pattern": "^ls$",
                "expect_contains": "logs/",
                "hint": "Run: ls — confirm the workspace layout first."
            },
            {
                "command_pattern": "^cat\\s+notes\\.txt$",
                "expect_contains": "Linux essentials",
                "hint": "Run: cat notes.txt — read the study notes on this machine."
            }
        ],
        "success_message": "Workspace inventoried. Situational awareness before action — always."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Spot the rogue process",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Something on this box is running a web server nobody remembers approving. List the processes and identify the unexpected server process.",
        "objectives": ["List running processes", "Identify the unapproved server process"],
        "checks": [
            {
                "command_pattern": "^ps$",
                "expect_contains": "node server.js",
                "hint": "Run: ps — look for a server process that does not belong on this workstation."
            }
        ],
        "success_message": "Found it: node server.js. Unknown processes get investigated, not ignored."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Resolve the suspicious domain",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The beaconing host from the simulation talked to an unknown domain. Resolve it with dig and record the answer-section IP for the incident report.",
        "objectives": ["Run a DNS lookup on the suspicious domain", "Capture the A-record IP"],
        "checks": [
            {
                "command_pattern": "^dig\\s+\\S+$",
                "expect_contains": "93.184.216.34",
                "hint": "Run: dig <domain> (any domain works in the sandbox) — read the ANSWER SECTION for the A record."
            }
        ],
        "success_message": "Domain resolved and documented. Every indicator goes in the report with its evidence attached."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Reconstruct the timeline",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Incidents are timelines. Read the first three lines of logs/app.log to see how the morning started, then the last two lines to see how it ended — then you can tell the story.",
        "objectives": ["Read the start of the log", "Read the end of the log"],
        "checks": [
            {
                "command_pattern": "^head\\s+-n\\s+3\\s+logs/app\\.log$",
                "expect_contains": "server starting",
                "hint": "Run: head -n 3 logs/app.log — how did the morning begin?"
            },
            {
                "command_pattern": "^tail\\s+-n\\s+2\\s+logs/app\\.log$",
                "expect_contains": "timeout after 30s",
                "hint": "Run: tail -n 2 logs/app.log — how did it end?"
            }
        ],
        "success_message": "Timeline reconstructed: a clean start, a cache failure, a timeout. Incidents are stories — head and tail give you the first and last page."
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
    # validate
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
