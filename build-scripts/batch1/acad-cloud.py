#!/usr/bin/env python3
"""Batch 1 builder: acad-cloud — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-cloud'
D = 'acad-cloud'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The surprise bill",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Monday morning: last month's cloud bill is 4x the forecast. Finance is asking questions and engineering says 'nothing changed.' Find the money before the meeting at noon.",
        "steps": [
            {
                "symptom": "The bill jumped from $12k to $48k in one month. Nobody admits to launching anything new.",
                "evidence": [
                    ["Billing summary", "Last month: $48,210 (forecast $12,000)\nTop mover: compute +$31,000 | data transfer +$4,200\nTags: 62% of spend untagged"]
                ],
                "options": [
                    "Blame the forecast model and ask finance for a bigger budget",
                    "Break the bill down by service and tag, then hunt the untagged compute first",
                    "Shut down all non-production resources immediately",
                    "Open a support ticket with the cloud provider asking for a refund"
                ],
                "correct": 1,
                "explain": "You cannot fix what you cannot attribute. Service-by-service, tag-by-tag: the untagged 62% is where surprises live. Most 'mystery' bills are one forgotten resource type, not a pricing conspiracy."
            },
            {
                "symptom": "Found it: a load-test cluster from six weeks ago, still running at full size — 40 instances, untagged, in the account nobody watches.",
                "evidence": [
                    ["Cost explorer", "Resource: loadtest-cluster-07 | 40 instances x 24h x 42 days\nOwner tag: (none) | Created: 6 weeks ago by ex-contractor\nCost: $30,800"]
                ],
                "options": [
                    "Delete it immediately with no notice",
                    "Snapshot anything worth keeping, terminate the cluster, and notify the team first",
                    "Leave it running until the contractor confirms",
                    "Downsize it to 2 instances 'just in case'"
                ],
                "correct": 1,
                "explain": "Terminate, but like a professional: snapshot what might matter, tell the team before you pull the plug (someone's demo might depend on it), then kill it. 'Just in case' infrastructure is how you got a $48k bill."
            },
            {
                "symptom": "The cluster is gone. Now make sure this never happens again.",
                "evidence": [
                    ["Goal", "No more untagged, ownerless resources burning money silently"]
                ],
                "options": [
                    "Mandate cost tags at creation, add a budget alert at 80% of forecast, and schedule a weekly idle-resource review",
                    "Require VP approval for every instance launch",
                    "Move everything back on-premises",
                    "Trust the team to remember next time"
                ],
                "correct": 0,
                "explain": "FinOps is guardrails, not gates: mandatory tags make spend attributable, budget alerts make overruns visible early, and a weekly idle-resource review makes cleanup routine. VP-approval for every VM just teaches people to work around you."
            }
        ],
        "debrief": "You attributed the spend, killed the zombie cluster professionally, and built guardrails instead of gates. That is FinOps: make the costs visible, then make waste impossible to ignore.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Lift-and-shift or re-platform?",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The company is migrating 60 VMs to the cloud in 90 days. The deadline is fixed; the architecture is 15 years old. Choose the migration strategy — and defend it.",
        "steps": [
            {
                "symptom": "Sixty VMs, one 90-day deadline, a monolith nobody fully understands, and two architects arguing: 'just move them' vs 'fix them first.'",
                "evidence": [
                    ["Assessment", "60 VMs | monolithic app, 15 yrs old | no automated tests\nDeadline: 90 days (data-center contract ends)\nTeam cloud experience: low"]
                ],
                "options": [
                    "Re-platform everything to containers and managed services in 90 days",
                    "Lift-and-shift (rehost) now to hit the deadline, then modernize in waves after",
                    "Rewrite the application cloud-native before migrating",
                    "Delay the migration until the architecture is modern"
                ],
                "correct": 1,
                "explain": "The deadline is the constraint that matters: the data-center contract ends. Rehost gets you out in 90 days with the lowest risk, and modernization happens in waves once you are safe. Big-bang rewrites against fixed deadlines are how migrations die."
            },
            {
                "symptom": "Rehost chosen. But three VMs run a licensed database that costs 5x in the cloud under bring-your-own-license rules.",
                "evidence": [
                    ["Licensing", "3 VMs: commercial DB, per-core licensing\nCloud cost under BYOL: 5x current | Managed alternative: 0.4x current\nEffort to switch: 3 weeks"]
                ],
                "options": [
                    "Rehost them anyway — consistency beats optimization",
                    "Carve out an exception: re-platform just the database tier to the managed service",
                    "Stay on-premises for those three VMs forever",
                    "Switch database vendors entirely this week"
                ],
                "correct": 1,
                "explain": "Strategy is allowed to have exceptions: rehost the 57 VMs that behave, re-platform the 3 that bankrupt you. The managed database is cheaper AND removes the licensing trap. Uniformity is a means, not a goal."
            },
            {
                "symptom": "Migration complete. The CFO asks: 'Are we actually better off?'",
                "evidence": [
                    ["Ask", "CFO: 'We spent $400k migrating. Prove it was worth it.'"]
                ],
                "options": [
                    "'The data center contract ended, so we had no choice'",
                    "Show the before/after: eliminated data-center costs, deployment time from weeks to hours, and the wave-1 modernization already cut the database bill 60%",
                    "Promise savings will appear next year",
                    "Blame the licensing costs"
                ],
                "correct": 1,
                "explain": "Migrations are judged on outcomes, not effort: cost deltas, speed deltas, risk deltas. You measured the baseline before you moved (or you reconstructed it), and now you show the numbers. 'Trust us' is not a business case."
            }
        ],
        "debrief": "You let the deadline pick the strategy, made a surgical exception where the economics demanded it, and closed the loop with measured outcomes. Migration strategy is constraint management, not architecture fashion.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "Region failover drill",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Game day: the primary region just 'failed' (your chaos tool killed it). Customers are hitting errors. Run the failover like it is real — because one day it will be.",
        "steps": [
            {
                "symptom": "Health checks are red in us-east. Error rate climbing. The runbook says: declare, redirect, verify.",
                "evidence": [
                    ["Status", "us-east health: 0/12 checks passing | error rate: 34% and climbing\nRunbook: 1) declare incident 2) shift DNS to us-west 3) verify"]
                ],
                "options": [
                    "Follow the runbook: declare the incident, shift traffic to us-west, verify health there",
                    "Wait ten minutes to see if us-east recovers on its own",
                    "Restart everything in us-east first",
                    "Tweet that you are investigating"
                ],
                "correct": 0,
                "explain": "Drills exist so you do not improvise during the real thing: declare (so everyone knows), redirect (stop the bleeding), verify (trust the new region, do not assume it). Waiting 'to see' turns a drill into an outage."
            },
            {
                "symptom": "Traffic is in us-west. Health checks are green — but the checkout service is throwing errors for 5% of users.",
                "evidence": [
                    ["us-west status", "Health: 12/12 passing | checkout errors: 5%\nClue: checkout reads a cache that was only ever warmed in us-east"]
                ],
                "options": [
                    "Fail back to us-east — the drill is broken",
                    "Identify the cold-cache dependency, warm it in us-west, and add cache-warming to the runbook",
                    "Accept 5% errors as the cost of failover",
                    "Blame the checkout team"
                ],
                "correct": 1,
                "explain": "Failover surfaced a hidden regional dependency: the cold cache. You fix it (warm it), and more importantly you write it into the runbook so the next failover does not re-learn it. Drills are for finding exactly these."
            },
            {
                "symptom": "All green. The drill ends. What do you do with what you learned?",
                "evidence": [
                    ["Outcome", "Failover time: 11 min | data loss: 0 | gap found: cold cache\nNext real incident: unknown"]
                ],
                "options": [
                    "File it away — the drill passed",
                    "Write the blameless postmortem: what worked, the cache gap, the runbook update, and schedule the next drill sooner",
                    "Punish whoever built the cache dependency",
                    "Declare the architecture 'multi-region ready' in the all-hands"
                ],
                "correct": 1,
                "explain": "A drill that finds nothing is a drill that taught nothing — yours found a real gap. The postmortem converts a lucky catch into a permanent fix, and scheduling the next drill keeps the muscle trained."
            }
        ],
        "debrief": "You ran the runbook instead of improvising, fixed the hidden dependency the drill exposed, and turned the lesson into process. Game days are how 'multi-region' stops being a slide and starts being a capability.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "The open bucket",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "A security researcher emails you: 'Your storage bucket is public. Call me.' Inside: customer exports. Work it.",
        "steps": [
            {
                "symptom": "The researcher's screenshot shows your bucket listing customer export files, world-readable.",
                "evidence": [
                    ["Report", "Bucket: customer-exports-prod | ACL: public-read\nContents: 214 CSV exports with customer data\nResearcher: 'Found via search engine. No bounty expected, just fix it.'"]
                ],
                "options": [
                    "Make the bucket private immediately, then assess what was exposed",
                    "Delete the bucket and all its contents right now",
                    "Email the researcher back asking for proof first",
                    "Restrict access to the researcher's IP so they cannot see it anymore"
                ],
                "correct": 0,
                "explain": "Stop the bleeding first: private now. Deleting destroys the evidence you need for the exposure assessment; demanding proof wastes the researcher's goodwill while the data sits open. Private first, forensics second."
            },
            {
                "symptom": "Bucket is private. Now: how long was it open, and who looked?",
                "evidence": [
                    ["Access logs", "Bucket created 8 months ago | public since creation\nAccess log: 1,204 GET requests from 38 unique IPs\nYour own app: 900 of those (legitimate)"]
                ],
                "options": [
                    "Assume the worst quietly and say nothing",
                    "Scope it honestly: 304 non-app requests from 38 IPs over 8 months — treat as a breach, notify per policy, and document",
                    "Only count it as a breach if you can prove data was downloaded",
                    "Blame the engineer who created the bucket"
                ],
                "correct": 1,
                "explain": "You cannot prove a negative — 304 unexplained requests over 8 months is exposure until proven otherwise. Honest scoping, notification per your incident policy, and documentation. 'Probably nobody looked' is not a finding."
            },
            {
                "symptom": "Incident closed. Harden the storage posture for good.",
                "evidence": [
                    ["Goal", "No bucket is ever public-by-default again"]
                ],
                "options": [
                    "Enable block-public-access at the account level, add a policy check to the deployment pipeline, and inventory every existing bucket",
                    "Send a reminder about bucket permissions",
                    "Move all storage on-premises",
                    "Hire someone to watch the buckets"
                ],
                "correct": 0,
                "explain": "Defense in depth for storage: an account-level block makes 'public' impossible by default, a pipeline check catches the drift, and the inventory finds the ones already out there. One control is a hope; three is a posture."
            }
        ],
        "debrief": "You closed the exposure before investigating it, scoped honestly instead of hopefully, and built three layers so it cannot recur. That is cloud security done right: fast hands, honest scope, durable guardrails.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "The multi-cloud exit",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Leadership wants 'multi-cloud' to avoid lock-in. Engineering wants to go deep on one provider's managed services. The board meets Friday. Make the call.",
        "steps": [
            {
                "symptom": "Two proposals: (A) run everything on both clouds for 'leverage'; (B) go all-in on one provider's managed services for speed.",
                "evidence": [
                    ["Proposals", "A: active-active multi-cloud, +60% engineering cost, portable-by-design\nB: single cloud, managed services, -40% ops load, deep lock-in\nTeam size: 8 engineers"]
                ],
                "options": [
                    "Pick A — lock-in is the bigger risk",
                    "Pick B — with 8 engineers, operational leverage beats theoretical portability",
                    "Do both: half the team on each cloud",
                    "Delay the decision until the team is bigger"
                ],
                "correct": 1,
                "explain": "Multi-cloud is a strategy for organizations that can afford two of everything — two skill sets, two bills, two failure modes. With 8 engineers, the real risk is not lock-in, it is drowning in undifferentiated operations. Go deep, ship fast, revisit at 10x scale."
            },
            {
                "symptom": "Single cloud chosen. Now address the lock-in fear without building a second cloud.",
                "evidence": [
                    ["Concern", "Board: 'What if they raise prices 30%?'"]
                ],
                "options": [
                    "Keep all infrastructure as code, use open interfaces at the boundaries, and keep the data exportable — portability without a second cloud",
                    "Build a shadow deployment on the other cloud just in case",
                    "Negotiate a price lock and stop worrying",
                    "Accept the lock-in as the cost of doing business"
                ],
                "correct": 0,
                "explain": "The cheap version of multi-cloud is exit-readiness: everything as code, open interfaces, exportable data, and a tested restore somewhere else. You do not need two clouds running — you need one cloud you could leave."
            },
            {
                "symptom": "Friday board meeting. One slide to defend the decision.",
                "evidence": [
                    ["Ask", "Board: 'Why not multi-cloud like our competitors?'"]
                ],
                "options": [
                    "'Because our competitors are bigger than us'",
                    "'Active-active multi-cloud costs us 60% more engineering for insurance we cannot collect: with our team size we would run both clouds badly. Instead we are exit-ready — portable code, exportable data, tested restores — at a fraction of the cost.'",
                    "'We will revisit it next year'",
                    "'The engineers prefer one cloud'"
                ],
                "correct": 1,
                "explain": "Decisions presented as trade-offs with numbers survive board meetings; preferences do not. You named the cost of the alternative, the risk of the chosen path, and the mitigation — that is a strategy, not a preference."
            }
        ],
        "debrief": "You sized the strategy to the team, bought exit-readiness instead of a second cloud, and defended it with economics. Multi-cloud is a means; the goal is leverage without fragility.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-vpc-1",
        "title": "Build the landing zone network",
        "console": "aws-vpc",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Every cloud migration starts with the network. Create a VPC named lab-vpc (10.1.0.0/16), then carve a public subnet 10.1.1.0/24 in us-east-1a inside it.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a VPC named lab-vpc with CIDR 10.1.0.0/16.",
                "validate": {"action": "create-vpc", "params": {"name": "lab-vpc", "cidr": "10.1.0.0/16"}},
                "hint": "Open the VPC section and create a VPC: NAME=lab-vpc, CIDR=10.1.0.0/16."
            },
            {
                "id": "t2",
                "instruction": "Create a subnet 10.1.1.0/24 in lab-vpc, availability zone us-east-1a.",
                "validate": {"action": "create-subnet", "params": {"vpc": "lab-vpc", "cidr": "10.1.1.0/24", "az": "us-east-1a"}},
                "hint": "Create a subnet inside lab-vpc: VPC=lab-vpc, CIDR=10.1.1.0/24, AZ=us-east-1a."
            }
        ],
        "debrief": "Network first, everything else second. A VPC with a real subnet is the foundation every workload after this will stand on."
    },
    {
        "id": f"{SLUG}-csim-vpc-2",
        "title": "Lock down the web tier",
        "console": "aws-vpc",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The web tier needs a security group that allows HTTPS from anywhere — and nothing else. Create the group web-sg on a VPC, then add the single inbound rule.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a VPC named web-vpc with CIDR 10.3.0.0/16 (the group needs a home).",
                "validate": {"action": "create-vpc", "params": {"name": "web-vpc", "cidr": "10.3.0.0/16"}},
                "hint": "Create a VPC first: NAME=web-vpc, CIDR=10.3.0.0/16."
            },
            {
                "id": "t2",
                "instruction": "Create a security group named web-sg on web-vpc.",
                "validate": {"action": "create-sg", "params": {"vpc": "web-vpc", "name": "web-sg"}},
                "hint": "Create a security group: VPC=web-vpc, NAME=web-sg."
            },
            {
                "id": "t3",
                "instruction": "Add an inbound rule to web-sg: TCP port 443 from 0.0.0.0/0.",
                "validate": {"action": "add-sg-rule", "params": {"sg": "web-sg", "protocol": "tcp", "port": 443, "cidr": "0.0.0.0/0"}},
                "hint": "Add an inbound rule on web-sg: PROTOCOL=tcp, PORT=443, CIDR=0.0.0.0/0."
            }
        ],
        "debrief": "Security groups are whitelists: one explicit allow, everything else denied. The web tier gets exactly HTTPS and nothing more."
    },
    {
        "id": f"{SLUG}-csim-iam-1",
        "title": "Onboard the deploy bot",
        "console": "aws-iam",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Automation needs an identity too. Create a user named deploy-bot for the CI system, then enable MFA on it — bots get the same identity hygiene as humans.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a user named deploy-bot.",
                "validate": {"action": "create-user", "params": {"name": "deploy-bot"}},
                "hint": "Open Users and create a user: NAME=deploy-bot."
            },
            {
                "id": "t2",
                "instruction": "Enable MFA for deploy-bot.",
                "validate": {"action": "enable-mfa", "params": {"user": "deploy-bot"}},
                "hint": "Enable MFA on the deploy-bot user — find the MFA action on the user row."
            }
        ],
        "debrief": "Every identity — human or machine — gets MFA. The deploy bot is one of the most powerful accounts you own; protect it like one."
    },
    {
        "id": f"{SLUG}-csim-az-1",
        "title": "Stand up the migration resource group",
        "console": "azure-portal",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The migration's second region lives in Azure. Create a resource group migration-rg in eastus, then a virtual network 10.2.0.0/16 inside it.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a resource group named migration-rg in location eastus.",
                "validate": {"action": "create-rg", "params": {"name": "migration-rg", "location": "eastus"}},
                "hint": "Create a resource group: NAME=migration-rg, LOCATION=eastus."
            },
            {
                "id": "t2",
                "instruction": "Create a virtual network with CIDR 10.2.0.0/16 in migration-rg.",
                "validate": {"action": "create-vnet", "params": {"rg": "migration-rg", "cidr": "10.2.0.0/16"}},
                "hint": "Create a VNet: RG=migration-rg, CIDR=10.2.0.0/16."
            }
        ],
        "debrief": "Resource groups are the unit of lifecycle: everything for the migration lives, gets tagged, and can be deleted together. Multi-cloud starts with tidy foundations."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Map the landing zone",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Before migrating anything, map the territory. List the home directory, then check the host mappings to see what this machine thinks the network looks like.",
        "objectives": ["List the home directory", "Read the host mappings"],
        "checks": [
            {
                "command_pattern": "^ls$",
                "expect_contains": "logs/",
                "hint": "Run: ls — see the workspace layout."
            },
            {
                "command_pattern": "^cat\\s+/etc/hosts$",
                "expect_contains": "10.0.0.8",
                "hint": "Run: cat /etc/hosts — check how this host resolves names."
            }
        ],
        "success_message": "Territory mapped. Migrations fail when people move things they never inventoried."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Check the network path",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The new region endpoint must be reachable before cutover. Ping it and confirm zero packet loss — a migration over a lossy path is a corruption incident waiting to happen.",
        "objectives": ["Ping the target and confirm connectivity"],
        "checks": [
            {
                "command_pattern": "^ping\\s+\\S+$",
                "expect_contains": "0% packet loss",
                "hint": "Run: ping <host> (any host works in the sandbox) — look for 0% packet loss in the statistics."
            }
        ],
        "success_message": "Path is clean: 0% packet loss. Never cut over on an untested network."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Size the logs before migration",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Cloud storage bills by the byte. Count the lines in logs/app.log so the migration plan includes the real log volume — no surprises on the storage bill.",
        "objectives": ["Count the lines in logs/app.log"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+logs/app\\.log$",
                "expect_contains": "6 logs/app.log",
                "hint": "Run: wc -l logs/app.log — count lines (pass the file; stdin is not simulated)."
            }
        ],
        "success_message": "6 lines — small now, but measured. FinOps starts with measuring before you move."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Find the warnings",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Warnings are tomorrow's incidents. Search logs/app.log for WARN lines — the migration runbook needs every known flake documented before cutover.",
        "objectives": ["Find WARN lines in logs/app.log"],
        "checks": [
            {
                "command_pattern": "^grep\\s+WARN\\s+logs/app\\.log$",
                "expect_contains": "retry 1/3",
                "hint": "Run: grep WARN logs/app.log — surface every warning."
            }
        ],
        "success_message": "Warning found and documented. Known flakes go in the runbook; unknown ones become incidents."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Attest the migration baseline",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The migration baseline token is 'baseline'. Hash it and confirm the digest matches the published value 8ba8496a2525ae171ffd104d632dede6ef418d9b95962a9d88e2fcdbc8d48d24 — baselines you cannot verify are not baselines.",
        "objectives": ["Hash the baseline token", "Confirm the published digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+baseline$",
                "expect_contains": "8ba8496a2525ae171ffd104d632dede6ef418d9b95962a9d88e2fcdbc8d48d24",
                "hint": "Run: sha256sum baseline — the digest must match character for character."
            }
        ],
        "success_message": "Baseline attested. Verify the starting point, or you will never know what the migration changed."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Resolve the new region endpoint",
        "domain_id": D,
        "difficulty": 2,
        "brief": "DNS is the first dependency of every migration. Resolve the new region's endpoint and confirm the A record answers — cutover day is not the time to discover DNS is broken.",
        "objectives": ["Resolve the endpoint", "Confirm the A record"],
        "checks": [
            {
                "command_pattern": "^dig\\s+\\S+$",
                "expect_contains": "93.184.216.34",
                "hint": "Run: dig <endpoint> (any name works in the sandbox) — read the ANSWER SECTION."
            }
        ],
        "success_message": "Endpoint resolves. DNS first, everything else second."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Audit the log case-insensitively",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Log formats drift — 'ERROR', 'Error', 'error' all mean the same thing to the customer. Search logs/app.log case-insensitively so no variant escapes the pre-migration audit.",
        "objectives": ["Case-insensitive search for errors"],
        "checks": [
            {
                "command_pattern": "^grep\\s+-i\\s+error\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep -i error logs/app.log — the -i flag catches every case variant."
            }
        ],
        "success_message": "All variants caught. Audits that miss a case variant miss the incident."
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
