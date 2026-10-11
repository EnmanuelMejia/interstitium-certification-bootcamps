#!/usr/bin/env python3
"""Batch 1 builder: acad-systems — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-systems'
D = 'acad-systems'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The full disk at 3 AM",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "3 AM page: the database server's disk is at 100% and writes are failing. The database will not start. Work it like an SRE.",
        "steps": [
            {
                "symptom": "Disk at 100%. Database down. The obvious suspect is the log directory, but 'obvious' has burned you before.",
                "evidence": [
                    ["Alert", "db-primary: disk 100% | postgres: will not start\nUptime: 214 days | last cleanup: unknown"]
                ],
                "options": [
                    "Delete the oldest log files immediately to free space",
                    "Find what is actually consuming the space first — then delete with knowledge, not hope",
                    "Add a bigger disk and go back to sleep",
                    "Restart the database and hope it compacts"
                ],
                "correct": 1,
                "explain": "Deleting before measuring is how you delete the wrong thing at 3 AM. Find the consumers (logs? WAL? a runaway temp file?), then act. A bigger disk without understanding just postpones the next 3 AM page."
            },
            {
                "symptom": "Found it: 400 GB of uncompressed WAL archives from a backup job that broke 6 months ago — plus the actual logs are fine.",
                "evidence": [
                    ["Usage", "/var/lib/postgres/wal_archive: 400 GB (6 months, uncompressed)\nBackup job: broken since April | logs: 12 GB (normal)"]
                ],
                "options": [
                    "Delete all 400 GB now",
                    "Verify the archives are truly unneeded (no replica depends on them, backups exist elsewhere), compress or move a sample first, then clear with a documented command",
                    "Compress them in place and leave them",
                    "Leave them — disk is cheap, just add more"
                ],
                "correct": 1,
                "explain": "Even obvious junk gets verified before deletion: a replica replaying WAL would die if you nuke its archives. Check dependencies, move before you delete when you can, and document the command — 3 AM you is not to be trusted with rm -rf."
            },
            {
                "symptom": "Space freed, database up. Now make sure no human gets this page again.",
                "evidence": [
                    ["Goal", "No more 100%-disk pages"]
                ],
                "options": [
                    "Set a disk alert at 95%",
                    "Fix the broken backup job, add log rotation with retention policy, alert at 80% with a runbook link, and trend disk growth on a dashboard",
                    "Schedule a monthly manual cleanup",
                    "Buy bigger disks for all servers"
                ],
                "correct": 1,
                "explain": "Alerting at 95% pages a human for a problem that started months ago. The real fixes: repair the backup job (the source), rotate logs with retention (the policy), alert at 80% (the lead time), trend the growth (the foresight). Pages should be for surprises, not slow inevitabilities."
            }
        ],
        "debrief": "You measured before deleting, verified before purging, and fixed the source instead of the symptom. Disk-full is never about disk — it is about the process that let it fill.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Split brain",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "A network partition split your cluster: both halves think they are primary, both are taking writes. The partition just healed. Decide how to reconcile two divergent truths.",
        "steps": [
            {
                "symptom": "Partition lasted 40 minutes. Side A took 12,000 writes; side B took 8,000 writes. Both believed they were primary.",
                "evidence": [
                    ["Divergence", "Partition: 40 min | A: 12,000 writes | B: 8,000 writes\nBoth sides: believed primary | conflict rate: unknown"]
                ],
                "options": [
                    "Keep side A (more writes) and discard side B",
                    "Stop writes, measure the actual conflicts (same keys touched on both sides), then reconcile by rule — last-write-wins is a policy decision, not a default",
                    "Merge everything — writes are writes",
                    "Pick side B; fewer writes means less to reconcile"
                ],
                "correct": 1,
                "explain": "More writes does not mean more correct — it means more to lose. You freeze writes first (stop the divergence growing), measure real conflicts key by key, then apply a deliberate reconciliation policy. 'Most writes wins' is how you silently corrupt data."
            },
            {
                "symptom": "Conflict analysis: 3% of keys were written on both sides. The rest are disjoint.",
                "evidence": [
                    ["Conflicts", "Disjoint keys: 97% (safe to merge)\nConflicting keys: 3% (~600 keys)\nOf conflicts: 80% are counters, 20% are user records"]
                ],
                "options": [
                    "Apply last-write-wins to everything",
                    "Merge the disjoint 97% automatically; resolve counters with CRDT-style addition and hand the 120 user-record conflicts to the owning teams with both versions",
                    "Discard all of side B's conflicting keys",
                    "Ask the CEO to decide"
                ],
                "correct": 1,
                "explain": "Different data types get different reconciliation: disjoint keys merge safely, counters add (order does not matter for increments), and true user-record conflicts need human judgment with both versions visible. One rule for all data types is how reconciliation creates new corruption."
            },
            {
                "symptom": "Reconciled. Now prevent the next split-brain.",
                "evidence": [
                    ["Ask", "Team: 'How do we never do this again?'"]
                ],
                "options": [
                    "Add more nodes to each side",
                    "Require a quorum for primary election (no majority, no primary), add fencing so a deposed primary cannot keep writing, and test partitions in game days",
                    "Get a better network",
                    "Run everything on one big server"
                ],
                "correct": 1,
                "explain": "Split-brain is prevented by consensus mechanics, not hope: quorum means a minority partition cannot elect itself primary, fencing means the old primary gets shot before it writes, and game days prove it works. Partitions are inevitable; dual primaries are a choice."
            }
        ],
        "debrief": "You froze the divergence, reconciled by data type, and installed quorum plus fencing. Distributed systems do not avoid partitions — they decide in advance what happens during them.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "The slow query vs the slow network",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The app is slow. The database team blames the network; the network team blames the database. You have one hour and a packet capture. Settle it.",
        "steps": [
            {
                "symptom": "P99 request time tripled overnight. DB team: 'network latency.' Network team: 'slow queries.' Both have graphs.",
                "evidence": [
                    ["Claims", "DB team graph: query times normal (their sampling: 1%)\nNetwork team graph: no packet loss (their window: 5-min avg)\nReality: users see 3x slowdown"]
                ],
                "options": [
                    "Pick a side based on who argues better",
                    "Measure the layers independently: time the query at the database, time the network round-trip separately, and see which one actually moved",
                    "Restart both the database and the routers",
                    "Add caching to hide it"
                ],
                "correct": 1,
                "explain": "Blame tennis ends with independent measurement: query time measured AT the database versus network time measured WITHOUT the query. Each team's graph was technically true and practically useless — 1% sampling and 5-minute averages both hide the thing you are looking for."
            },
            {
                "symptom": "Measured: queries are fast at the database (20ms), but the app-to-DB round trip is 400ms. The network is clean — no loss, no congestion.",
                "evidence": [
                    ["Measurements", "Query at DB: 20ms | app-to-DB round trip: 400ms\nNetwork: 0% loss, no congestion\nGap: 380ms unexplained"]
                ],
                "options": [
                    "Blame the network team anyway",
                    "Look between the layers: connection pool exhaustion, DNS resolution per query, or TLS handshake per connection — the gap lives in the plumbing, not the wire",
                    "Accept 400ms as normal",
                    "Move the database next to the app"
                ],
                "correct": 1,
                "explain": "Fast queries plus a clean network with a slow round trip means the overhead is in the plumbing: exhausted pools queueing, DNS lookups per query, handshakes per connection. The layers are not just 'app, network, DB' — the middleware between them has its own physics."
            },
            {
                "symptom": "Found: the connection pool was sized for the old traffic, and DNS was resolving on every checkout. Fixed both. What do you institutionalize?",
                "evidence": [
                    ["Fix", "Pool resized | DNS cached | round trip: 400ms -> 35ms"]
                ],
                "options": [
                    "Nothing — it is fixed",
                    "Add layered latency breakdown to the standard dashboard (app, pool wait, network, query) so the next slowdown arrives pre-diagnosed",
                    "Write a postmortem blaming the pool defaults",
                    "Double all pool sizes everywhere preemptively"
                ],
                "correct": 1,
                "explain": "The lasting fix is observability shaped like the system: a latency breakdown by layer means the next incident starts with the answer instead of the argument. Diagnose once, instrument forever."
            }
        ],
        "debrief": "You refused the blame tennis, measured each layer independently, found the plumbing overhead, and dashboarded the breakdown. Slow systems are layered — measure the layers.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "Thundering herd on deploy",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The deploy restarted all 200 instances at once. Every instance is cold-starting, hammering the database and the config service simultaneously. The site is flapping. Respond.",
        "steps": [
            {
                "symptom": "All 200 instances restarted in the same minute. Config service is melting; database connections are exhausted; the site flaps up and down.",
                "evidence": [
                    ["Deploy", "200/200 instances restarted simultaneously\nConfig service: overloaded | DB: connection exhaustion\nSite: flapping"]
                ],
                "options": [
                    "Restart everything again — maybe it will settle",
                    "Stop the bleeding: halt the rollout, let the config service and DB recover, then bring instances up in small batches with health gates",
                    "Add more database connections",
                    "Wait for the herd to finish"
                ],
                "correct": 1,
                "explain": "A thundering herd gets worse before it gets better if you let it run: every retry joins the stampede. Halt, let the dependencies breathe, then reintroduce load in batches with health gates. Recovery is sequenced, not simultaneous."
            },
            {
                "symptom": "Batched restart worked — site is stable. The team wants to deploy the same way next time but 'more carefully.'",
                "evidence": [
                    ["Ask", "Team: 'We'll just watch it more closely next time.'"]
                ],
                "options": [
                    "Agree — vigilance is enough",
                    "Change the deploy mechanics: rolling restarts with a batch size and health gates, so a herd is structurally impossible — not just watched for",
                    "Deploy at 3 AM when nobody notices",
                    "Halve the instance count"
                ],
                "correct": 1,
                "explain": "'Watch more carefully' is not a fix — it is a hope with a human attached. Rolling deploys with batch sizes and health gates make the herd impossible by construction. Vigilance does not scale; mechanics do."
            },
            {
                "symptom": "Rolling deploys are in. What about the cold-start storm itself — 200 instances still need config and DB connections eventually?",
                "evidence": [
                    ["Residual", "Rolling deploys spread the load, but each instance still cold-starts hard"]
                ],
                "options": [
                    "Accept it — rolling is enough",
                    "Soften the cold start too: staggered jitter on startup, cached config with graceful fallback, and connection ramp-up instead of instant full pools",
                    "Pre-warm by deploying twice",
                    "Overprovision everything 3x"
                ],
                "correct": 1,
                "explain": "Defense in depth for startup: rolling spreads the herd, jitter desynchronizes it, cached config removes a dependency, and ramped connections protect the database. Each layer is cheap; together they make cold starts boring."
            }
        ],
        "debrief": "You halted the stampede, made herds structurally impossible, and softened the cold start itself. Distributed systems fail in coordinated ways — so you coordinate the recovery.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "To cache or not",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The product page loads in 800ms; the database groans. A cache would cut it to 50ms — but prices change, and stale prices mean angry customers and refunds. Decide.",
        "steps": [
            {
                "symptom": "Page load: 800ms, DB at 70% on peak. Cache proposal: 50ms loads, 5-minute TTL on product data including prices.",
                "evidence": [
                    ["Proposal", "Without cache: 800ms, DB 70% peak\nWith cache (5-min TTL): 50ms, DB 20%\nRisk: price changes visible up to 5 min late"]
                ],
                "options": [
                    "Cache everything for 5 minutes — speed wins",
                    "Split by data type: cache the slow-changing catalog aggressively, keep prices on a short TTL or write-through invalidation — freshness follows the cost of staleness",
                    "Do not cache — correctness first",
                    "Cache for 24 hours — maximum speed"
                ],
                "correct": 1,
                "explain": "Caching is a per-data-type decision driven by the cost of staleness: a stale product description annoys; a stale price costs refunds and trust. Cache the catalog hard, keep prices fresh with short TTLs or invalidation on write. One TTL for everything is how you get the worst of both."
            },
            {
                "symptom": "Split caching approved. Now: what happens when the cache itself fails?",
                "evidence": [
                    ["Question", "Cache cluster: single region, no failover tested"]
                ],
                "options": [
                    "Accept the risk — caches rarely fail",
                    "Design for cache failure: the app must work (slower) with the cache down — cache-aside with DB fallback, never cache-as-requirement",
                    "Buy a bigger cache cluster",
                    "Replicate the cache to three regions"
                ],
                "correct": 1,
                "explain": "A cache is a performance optimization, not a dependency: the system must degrade to 'slow but correct' when it dies. Cache-aside with database fallback means a cache outage is a latency incident, not a data incident."
            },
            {
                "symptom": "Cache is live: 50ms loads, prices fresh, fallback tested. What do you watch?",
                "evidence": [
                    ["Ask", "Team: 'What do we monitor?'"]
                ],
                "options": [
                    "Hit rate only",
                    "Hit rate, stale-serve incidents, invalidation lag, and fallback frequency — the cache's health is measured in correctness, not just speed",
                    "Nothing — it works",
                    "Page load time only"
                ],
                "correct": 1,
                "explain": "Cache monitoring is correctness monitoring: hit rate tells you it is helping, invalidation lag tells you it is fresh, fallback frequency tells you it is fragile. A fast cache serving stale prices is a fast way to lose money."
            }
        ],
        "debrief": "You split caching by staleness cost, designed for cache failure, and monitored correctness over speed. Caching is easy; cache invalidation and failure modes are the actual engineering.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-linux-1",
        "title": "Lock down the app config",
        "console": "linux-desktop",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The app config at /etc/app.conf is world-readable (644) — it contains secrets. Restrict it to owner-only access with chmod 600.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Change /etc/app.conf permissions to 600.",
                "validate": {"action": "chmod", "params": {"path": "/etc/app.conf", "mode": "600"}},
                "hint": "chmod the file: PATH=/etc/app.conf, MODE=600."
            }
        ],
        "debrief": "Config with secrets gets 600: the owner reads it, nobody else does. Permissions are the cheapest security control you own."
    },
    {
        "id": f"{SLUG}-csim-linux-2",
        "title": "Stage the backup directory",
        "console": "linux-desktop",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The backup plan needs a home. Create the directory /home/user/backups, then create a README file inside it documenting the plan.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create the directory /home/user/backups.",
                "validate": {"action": "create-dir", "params": {"path": "/home/user/backups"}},
                "hint": "Create directory: PATH=/home/user/backups."
            },
            {
                "id": "t2",
                "instruction": "Create the file /home/user/backups/README.",
                "validate": {"action": "create-file", "params": {"path": "/home/user/backups/README"}},
                "hint": "Create file: PATH=/home/user/backups/README."
            }
        ],
        "debrief": "Backups start with a place to put them and a README saying what goes there. Boring, deliberate, recoverable."
    },
    {
        "id": f"{SLUG}-csim-switch-1",
        "title": "Segment the server VLAN",
        "console": "switch-cli",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The servers need their own broadcast domain. Create VLAN 20 named 'servers', assign port gi0/5 to it as an access port, then save the config — unsaved configs evaporate on reboot.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create VLAN 20 named servers.",
                "validate": {"action": "create-vlan", "params": {"id": 20, "name": "servers"}},
                "hint": "In the CLI box type: vlan 20 name servers"
            },
            {
                "id": "t2",
                "instruction": "Assign port gi0/5 to VLAN 20 as an access port.",
                "validate": {"action": "assign-port", "params": {"port": "gi0/5", "vlan": 20}},
                "hint": "In the CLI box type: interface gi0/5 access vlan 20"
            },
            {
                "id": "t3",
                "instruction": "Save the running config.",
                "validate": {"action": "save-config", "params": {}},
                "hint": "In the CLI box type: write memory"
            }
        ],
        "debrief": "Segment, assign, save. The unsaved config is the classic outage: everything works until the reboot."
    },
    {
        "id": f"{SLUG}-csim-k8s-1",
        "title": "Deploy the API to prod",
        "console": "k8s-dashboard",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Ship the API: create the prod namespace, deploy api (image api:2.14, 3 replicas) into it, then expose it as a ClusterIP service on port 80.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a namespace named prod.",
                "validate": {"action": "create-namespace", "params": {"name": "prod"}},
                "hint": "Create namespace: NAME=prod."
            },
            {
                "id": "t2",
                "instruction": "Deploy 'api' (image api:2.14, 3 replicas) into the prod namespace.",
                "validate": {"action": "deploy", "params": {"name": "api", "namespace": "prod", "image": "api:2.14", "replicas": 3}},
                "hint": "Deploy: NAME=api, NAMESPACE=prod, IMAGE=api:2.14, REPLICAS=3."
            },
            {
                "id": "t3",
                "instruction": "Expose the api deployment on port 80 as a ClusterIP service.",
                "validate": {"action": "expose-service", "params": {"deployment": "api", "port": 80, "type": "ClusterIP"}},
                "hint": "Expose service: DEPLOYMENT=api, PORT=80, TYPE=ClusterIP."
            }
        ],
        "debrief": "Namespace, deploy, expose: the shipping loop. Namespaces are cheap isolation — prod gets its own."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Audit the users",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Systems work starts with knowing who can log in. Read /etc/passwd and confirm the candidate account.",
        "objectives": ["Read the user database"],
        "checks": [
            {
                "command_pattern": "^cat\\s+/etc/passwd$",
                "expect_contains": "candidate:x:1000",
                "hint": "Run: cat /etc/passwd — audit who exists."
            }
        ],
        "success_message": "Users audited. Identity is the first layer of every system."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "List the workspace",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Know the filesystem you are standing on. List the home directory.",
        "objectives": ["List the home directory"],
        "checks": [
            {
                "command_pattern": "^ls$",
                "expect_contains": "app.py",
                "hint": "Run: ls — see the layout."
            }
        ],
        "success_message": "Filesystem mapped. You operate on what you can see."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "What is running",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A system is its running processes. List them and identify the application server by its PID — the OS never lies about what is alive.",
        "objectives": ["List processes", "Identify the app server PID"],
        "checks": [
            {
                "command_pattern": "^ps$",
                "expect_contains": "1337",
                "hint": "Run: ps — find the PID of the node server process."
            }
        ],
        "success_message": "Process found. When in doubt, ask the kernel — ps does not speculate."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Resolve the service",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Distributed systems run on names. Resolve a service name with dig and confirm the A record — if names do not resolve, nothing else matters.",
        "objectives": ["Resolve the name", "Confirm the A record"],
        "checks": [
            {
                "command_pattern": "^dig\\s+\\S+$",
                "expect_contains": "93.184.216.34",
                "hint": "Run: dig <name> — read the ANSWER SECTION."
            }
        ],
        "success_message": "Name resolves. DNS is the foundation everything distributed stands on."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Is the network up",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Before blaming the application, verify the network. Ping a host and confirm zero packet loss — the simplest test is often the right first one.",
        "objectives": ["Verify connectivity"],
        "checks": [
            {
                "command_pattern": "^ping\\s+\\S+$",
                "expect_contains": "0% packet loss",
                "hint": "Run: ping <host> — look for 0% packet loss."
            }
        ],
        "success_message": "Network verified. Rule out the simple causes first — they are the most common."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Verify the lockdown manifest",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The hardening checklist ships with a manifest token 'lockdown'. Hash it and confirm digest 52698ab8f76cef21fd1c56339814857de43532683064f88ca982bed86b110f16 — hardened systems are verified systems.",
        "objectives": ["Hash the manifest token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+lockdown$",
                "expect_contains": "52698ab8f76cef21fd1c56339814857de43532683064f88ca982bed86b110f16",
                "hint": "Run: sha256sum lockdown — the digest must match character for character."
            }
        ],
        "success_message": "Manifest verified. Trust, but hash."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Read the kernel ring",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The OS keeps its own diary. Read /var/log/syslog for the link-up event, then search it for the backup service start — the kernel log is the ground truth beneath every abstraction.",
        "objectives": ["Read the system log", "Find the backup event"],
        "checks": [
            {
                "command_pattern": "^cat\\s+/var/log/syslog$",
                "expect_contains": "link up",
                "hint": "Run: cat /var/log/syslog — read the kernel's diary."
            },
            {
                "command_pattern": "^grep\\s+Started\\s+/var/log/syslog$",
                "expect_contains": "daily backup",
                "hint": "Run: grep Started /var/log/syslog — find the backup service event."
            }
        ],
        "success_message": "Kernel log read. Beneath every abstraction, the OS is keeping notes — learn to read them."
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
