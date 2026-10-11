#!/usr/bin/env python3
"""Batch 1 builder: acad-command — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-command'
D = 'acad-command'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The 3 AM page",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "3:07 AM. Your phone is screaming: checkout is down, error rate 100%. You are the incident commander. The next ten minutes set the tone for the next ten hours.",
        "steps": [
            {
                "symptom": "Checkout is fully down. Three engineers are awake in the channel, all talking at once, nobody leading.",
                "evidence": [
                    ["Page", "03:07 — checkout error rate 100% | revenue impact: ~$40k/hour\nChannel: 3 engineers online, no IC declared, parallel theories flying"]
                ],
                "options": [
                    "Start debugging immediately — every minute costs money",
                    "Declare yourself incident commander, open a dedicated channel, and assign roles: one debugger, one comms, one scribe",
                    "Wait for the VP to wake up and decide",
                    "Tell everyone to stay calm and go back to sleep while you look"
                ],
                "correct": 1,
                "explain": "The first job is not the fix — it is the structure. An IC, a channel, and three roles (debug, comms, scribe) turn chaos into a team. Debugging before declaring means five people stepping on each other's theories."
            },
            {
                "symptom": "Structure is up. The debugger thinks it is the database; the comms lead wants to post a status update saying 'we are investigating.'",
                "evidence": [
                    ["Minute 12", "Debugger: 'DB connections spiking, I think it's the primary.'\nComms: 'Can I post that we're investigating?' | Scribe: logging"]
                ],
                "options": [
                    "Post the update and let the debugger keep digging alone",
                    "Approve a factual status ('checkout is down, we are investigating, next update in 30 min'), and ask the debugger for evidence before acting on the DB theory",
                    "Fail over the database now — the theory sounds right",
                    "Tell comms to say nothing until there is a fix"
                ],
                "correct": 1,
                "explain": "Comms cadence is set early: factual, no speculation, next update promised. And theories need evidence before they become actions — failing over a database on a hunch can turn one outage into two."
            },
            {
                "symptom": "Root cause found: a deploy at 02:40 shipped a bad migration. Rollback is ready but the deploy's author is the debugger — and looks shattered.",
                "evidence": [
                    ["Minute 38", "Cause: deploy 02:40, bad migration | Fix: rollback staged, tested\nDebugger (deploy author): 'This is my fault. I'm so sorry.'"]
                ],
                "options": [
                    "Execute the rollback, thank the debugger for finding it fast, and say the postmortem will focus on the system, not the person",
                    "Execute the rollback and reassign the debugger — they are compromised",
                    "Delay the rollback until the author is calmer",
                    "Announce in the channel that the debugger caused it so everyone knows"
                ],
                "correct": 0,
                "explain": "Fix first, humanity always. The rollback is the priority; the debugger who found their own bug fast is an asset, not a liability. And you say out loud, now, that the postmortem will be blameless — psychological safety is built in moments like this."
            }
        ],
        "debrief": "You built structure before chasing the fix, set a comms cadence, demanded evidence over hunches, and protected the human while fixing the system. That is incident command: calm is a strategy.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Deploy or rollback?",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The new release is 80% rolled out when the error budget starts burning — but only in one region, and the dashboards are ambiguous. Roll back a mostly-good deploy, or push through on incomplete information?",
        "steps": [
            {
                "symptom": "Errors climbing in eu-west only. The change looks unrelated to the errors. Rollback takes 20 minutes; the launch event is in an hour.",
                "evidence": [
                    ["Signals", "eu-west error rate: 2% -> 9% in 20 min | other regions: flat\nDeploy: 80% rolled out | correlation with deploy: unclear\nRollback time: ~20 min | launch event: T-60 min"]
                ],
                "options": [
                    "Roll back immediately — errors beat schedules",
                    "Hold the rollout (stop at 80%), investigate eu-west for 15 minutes with a hard timebox, then decide",
                    "Push to 100% — the errors are probably unrelated",
                    "Wait for more data with no timebox"
                ],
                "correct": 1,
                "explain": "Incomplete information calls for buying information cheaply: freeze the rollout (stop adding risk), timebox the investigation (15 minutes, not 'until we know'), then decide. Instant rollback wastes a maybe-good deploy; pushing through gambles the launch."
            },
            {
                "symptom": "Timebox expired. The eu-west errors are a third-party CDN issue — not your deploy. But the rollback window is closing.",
                "evidence": [
                    ["Finding", "eu-west errors: CDN provider incident, confirmed on their status page\nYour deploy: clean | Time left before launch: 40 min"]
                ],
                "options": [
                    "Roll back anyway — better safe",
                    "Resume the rollout to 100% and note the CDN issue in the launch comms",
                    "Freeze at 80% through the launch",
                    "Blame the CDN publicly"
                ],
                "correct": 1,
                "explain": "New information updates the decision: the deploy is clean, the culprit is external. You resume — and you communicate the CDN issue proactively so the launch team is not blindsided. Decisions are bets; update them when the odds change."
            },
            {
                "symptom": "Launch succeeded. Now the team wants a rule: 'never deploy before a launch event again.'",
                "evidence": [
                    ["Proposal", "Team: 'Freeze all deploys 48h before any launch.'"]
                ],
                "options": [
                    "Approve the freeze — it feels safe",
                    "Reject the blanket freeze: this incident was a CDN issue, not a deploy issue. Instead: keep deploys small, keep rollbacks fast, and require a launch-day rollback plan",
                    "Extend the freeze to a full week",
                    "Let the team vote"
                ],
                "correct": 1,
                "explain": "Do not legislate against the last incident — legislate against the class of risk. The lesson was not 'deploys are dangerous'; it was 'have a fast rollback and a timeboxed investigation process.' Blanket freezes just move risk around."
            }
        ],
        "debrief": "You bought information instead of gambling, updated the bet when the facts changed, and refused to turn one scare into a permanent bad policy. Decision-making under uncertainty is a skill — you just practiced it.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "The blameless postmortem",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Yesterday's outage was caused by an engineer running a command on the wrong host. The postmortem is in an hour. The engineer is dreading it. Run it right.",
        "steps": [
            {
                "symptom": "The timeline is clear: at 14:02, an engineer ran the production migration against the wrong host. Two hours of downtime.",
                "evidence": [
                    ["Timeline", "14:02 — migration run against prod instead of staging\n14:05 — errors begin | 16:10 — rollback complete\nEngineer: 6 months tenure, followed the runbook as written"]
                ],
                "options": [
                    "Open the postmortem by naming the engineer and what they did wrong",
                    "Open with: 'We are here to understand the system that allowed this, not to judge the person. Walk us through what you saw.'",
                    "Skip the postmortem — the cause is obvious",
                    "Have the engineer's manager run the session"
                ],
                "correct": 1,
                "explain": "Blameless is stated out loud, at the start, by the leader — otherwise it is just a word in a doc. 'What did you see?' invites the truth; 'what did you do wrong?' invites defensiveness and silence."
            },
            {
                "symptom": "The engineer explains: the runbook's hostnames differed by one character, and the prompt did not show the environment. Three others admit they nearly did the same.",
                "evidence": [
                    ["Testimony", "Runbook: hosts 'db-prod-01' vs 'db-prod-01-stg' — one suffix apart\nPrompt: no environment indicator | 3 others: 'I almost did that last month'"]
                ],
                "options": [
                    "Conclude the engineer should have been more careful",
                    "Name the systemic fixes: environment-colored prompts, a confirmation gate on prod migrations, distinct naming — and assign owners and dates",
                    "Add 'be more careful' to the runbook",
                    "Require two-person approval for every command"
                ],
                "correct": 1,
                "explain": "Three near-misses mean the system was loaded and waiting for someone. The fixes are environmental (make prod unmistakable, gate destructive actions), owned, and dated. 'Be more careful' is not a fix — it is a wish."
            },
            {
                "symptom": "The postmortem doc is written. An executive asks for 'the name of who caused it' for the board report.",
                "evidence": [
                    ["Ask", "Exec: 'The board wants accountability. Who was it?'"]
                ],
                "options": [
                    "Give the name — the board outranks the process",
                    "Refuse and reframe: 'The board gets the systemic causes, the fixes, and the dates. Naming the individual teaches every engineer to hide the next near-miss.'",
                    "Give the name but ask them to keep it quiet",
                    "Say you do not remember"
                ],
                "correct": 1,
                "explain": "This is the moment blamelessness is tested — and it is the leader's job to absorb the pressure, not pass it down. The board gets accountability for the system; the individual gets coaching. Trade one for the other and your next postmortem will be fiction."
            }
        ],
        "debrief": "You protected the person, fixed the system, and held the line when accountability theater came knocking. Blameless postmortems are how organizations learn at full speed — because people tell the truth.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "The stakeholder ambush",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Mid-incident, two VPs join the bridge and demand an ETA. The team is still diagnosing. Handle the ambush without derailing the response.",
        "steps": [
            {
                "symptom": "VP Sales: 'Our biggest customer is threatening to churn. When will this be fixed?' VP Eng is silent. The debugger has a promising lead.",
                "evidence": [
                    ["Bridge", "VP Sales: 'I need a time. The customer is on hold.'\nStatus: diagnosing, one promising lead, no ETA yet"]
                ],
                "options": [
                    "Give an ETA to get them off the bridge — say 30 minutes",
                    "Give a process answer, not a time: 'We have a lead and we are testing it now. Next update in 20 minutes. I will come to you — please let the team work.'",
                    "Hand the bridge to the VP and step back",
                    "Mute the VPs"
                ],
                "correct": 1,
                "explain": "Never invent an ETA under pressure — a missed invented deadline destroys more trust than no deadline. Give them what you do know (the lead, the next update time) and protect the team's focus. Stakeholders need cadence, not fiction."
            },
            {
                "symptom": "VP Sales again: 'Can we just fail over to the backup? The customer does not care about root cause.'",
                "evidence": [
                    ["Proposal", "VP Sales: 'Fail over now, investigate later.'\nReality: failover was never tested; backup is 6 hours stale"]
                ],
                "options": [
                    "Do the failover — the VP outranks you",
                    "Explain the trade honestly: 'Failover is untested and the backup is 6 hours stale — we would trade a fixable outage for data loss. We stay the course unless the lead dies.'",
                    "Fail over quietly and hope",
                    "Ask the VP to sign off in writing first"
                ],
                "correct": 1,
                "explain": "Rank does not convert a bad option into a good one. You translate the technical reality into business consequences (data loss vs. outage) and make a recommendation — that is what the IC role is for. Deferring to rank during incidents is how outages get worse."
            },
            {
                "symptom": "Incident resolved. VP Sales apologizes for the pressure. What do you institutionalize?",
                "evidence": [
                    ["Retro note", "VP Sales: 'Sorry — I panicked. How do we do this better next time?'"]
                ],
                "options": [
                    "Ban VPs from the bridge",
                    "Create a stakeholder protocol: VPs get updates in a separate channel on a fixed cadence, and the IC briefs them — they never join the working bridge uninvited",
                    "Accept the apology and change nothing",
                    "Make the VP do incident training as punishment"
                ],
                "correct": 1,
                "explain": "The VP's instinct (protect the customer) was right; the venue was wrong. A stakeholder protocol gives executives what they actually need — timely, honest updates — without injecting pressure into the working team. Design the system for stressed humans."
            }
        ],
        "debrief": "You gave cadence instead of fiction, overruled rank with evidence, and turned an ambush into a protocol. Leadership under pressure is mostly structure plus honesty, repeated.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "When the runbook lies",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "The runbook says step 4 restarts the service. You ran step 4. The service did not restart — and the runbook has no step 5. Now what?",
        "steps": [
            {
                "symptom": "Step 4 of the failover runbook: 'Restart the queue service.' You ran it. Nothing happened. The runbook ends at step 4.",
                "evidence": [
                    ["Runbook", "FAILOVER-07, last updated 14 months ago\nStep 4: 'Restart the queue service' — no expected output listed\nReality: command ran, service still down, no step 5"]
                ],
                "options": [
                    "Run step 4 again, harder",
                    "Stop, verify the service state directly, and check whether the runbook's assumptions still match reality",
                    "Declare the runbook useless and improvise the whole failover",
                    "Wait for the runbook's author to wake up"
                ],
                "correct": 1,
                "explain": "When the map and the territory disagree, trust the territory. Verify actual state (is the service down? what does the supervisor say?) before running anything again — repeating a step that silently failed is how you compound outages."
            },
            {
                "symptom": "The service manager shows the queue service as 'failed' — it crashed on a config the runbook never mentions. The config was added 6 months ago.",
                "evidence": [
                    ["State", "Service: failed (not just stopped)\nCause: unknown config key 'max_batch_v2' — added 6 months ago\nRunbook age: 14 months (predates the config)"]
                ],
                "options": [
                    "Fix the config and restart — then update the runbook before you forget",
                    "Fix the config and restart; update the runbook later",
                    "Roll back the config change from 6 months ago",
                    "Rebuild the entire service from scratch"
                ],
                "correct": 0,
                "explain": "Fix the immediate problem, then fix the runbook in the same motion — 'later' never comes, and the next person gets the same lie. The scribe notes both the fix and the doc update while it is fresh."
            },
            {
                "symptom": "Service is up. The team asks: how do we stop runbooks from rotting?",
                "evidence": [
                    ["Ask", "Team: 'Half our runbooks are stale. What's the fix?'"]
                ],
                "options": [
                    "Assign someone to re-read all runbooks quarterly",
                    "Make runbooks executable and tested: every runbook gets a drill date, and steps that cannot be run in a drill get flagged. Stale steps are bugs, filed like bugs.",
                    "Delete all runbooks and rely on expertise",
                    "Write longer, more detailed runbooks"
                ],
                "correct": 1,
                "explain": "Runbooks rot because nothing tests them. Treat them like code: drills are the tests, stale steps are bugs with owners and due dates. A runbook that has never been drilled is a rumor, not a procedure."
            }
        ],
        "debrief": "You trusted the territory over the map, fixed the doc in the same motion as the system, and turned rot into process. Runbooks are only as good as their last drill.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-tick-1",
        "title": "Open the incident ticket",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Incident command starts with a paper trail. Open a P1 ticket for the checkout outage, then assign the seeded INC-9001 ticket to yourself as the incident commander.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a ticket titled 'INC: checkout outage' with priority P1.",
                "validate": {"action": "create-ticket", "params": {"title": "INC: checkout outage", "priority": "P1"}},
                "hint": "Open New ticket: TITLE='INC: checkout outage', PRIORITY=P1."
            },
            {
                "id": "t2",
                "instruction": "Assign ticket INC-9001 to m.reyes (the incident commander).",
                "validate": {"action": "assign-ticket", "params": {"id": "INC-9001", "assignee": "m.reyes"}},
                "hint": "On the INC-9001 row, assign it: ID=INC-9001, ASSIGNEE=m.reyes."
            }
        ],
        "debrief": "Every incident gets a ticket and an owner before anything else. Paper trails are how chaos becomes manageable."
    },
    {
        "id": f"{SLUG}-csim-tick-2",
        "title": "Run the incident to resolution",
        "console": "ticketing",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The incident is underway. Move INC-9001 to in-progress, add a status note for the stakeholders, then resolve it when the fix is verified — with a real resolution note.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Set ticket INC-9001 status to in-progress.",
                "validate": {"action": "update-status", "params": {"id": "INC-9001", "status": "in-progress"}},
                "hint": "Update INC-9001: STATUS=in-progress."
            },
            {
                "id": "t2",
                "instruction": "Add a note to INC-9001: 'IC declared; debug and comms roles assigned.'",
                "validate": {"action": "add-note", "params": {"id": "INC-9001", "text": "IC declared; debug and comms roles assigned."}},
                "hint": "Add a note on INC-9001 with the exact status text."
            },
            {
                "id": "t3",
                "instruction": "Resolve INC-9001 with resolution 'Rollback verified; monitoring green.'",
                "validate": {"action": "resolve-ticket", "params": {"id": "INC-9001", "resolution": "Rollback verified; monitoring green."}},
                "hint": "Resolve INC-9001 with the exact resolution text."
            }
        ],
        "debrief": "In-progress, narrated, resolved with evidence. The ticket is the incident's memory — future you will thank present you."
    },
    {
        "id": f"{SLUG}-csim-siem-1",
        "title": "Triage the impossible-travel alert",
        "console": "siem-dashboard",
        "domain_id": D,
        "difficulty": 2,
        "brief": "ALT-101 fired: an impossible-travel login on wkst-042. As IC, make sure it is worked: acknowledge it, assign it to analyst 't.nguyen', and escalate it — authentication anomalies do not wait.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Acknowledge alert ALT-101.",
                "validate": {"action": "acknowledge-alert", "params": {"id": "ALT-101"}},
                "hint": "Click Ack on the ALT-101 row (Impossible travel login)."
            },
            {
                "id": "t2",
                "instruction": "Assign alert ALT-101 to analyst t.nguyen.",
                "validate": {"action": "assign-alert", "params": {"id": "ALT-101", "analyst": "t.nguyen"}},
                "hint": "Assign alert form: ALERT ID=ALT-101, ANALYST=t.nguyen."
            },
            {
                "id": "t3",
                "instruction": "Escalate alert ALT-101.",
                "validate": {"action": "escalate", "params": {"id": "ALT-101"}},
                "hint": "Click Escalate on the ALT-101 row."
            }
        ],
        "debrief": "Acknowledged, owned, escalated. An alert with no owner is just noise with a timestamp."
    },
    {
        "id": f"{SLUG}-csim-siem-2",
        "title": "Contain the exfiltration signal",
        "console": "siem-dashboard",
        "domain_id": D,
        "difficulty": 3,
        "brief": "ALT-103: unusual outbound volume from srv-backup-02. Isolate the host to stop potential exfiltration, then create a detection rule 'backup-egress-watch' so the next spike pages someone.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Isolate host srv-backup-02.",
                "validate": {"action": "isolate-host", "params": {"host": "srv-backup-02"}},
                "hint": "Click 'Isolate host' on the ALT-103 row."
            },
            {
                "id": "t2",
                "instruction": "Create a detection rule named 'backup-egress-watch'.",
                "validate": {"action": "create-rule", "params": {"name": "backup-egress-watch"}},
                "hint": "Open Detection rules: NAME=backup-egress-watch, QUERY describing outbound volume spikes."
            }
        ],
        "debrief": "Contain first, detect permanently. Decisive action on ambiguous signals — followed by a rule so the ambiguity shrinks next time."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Read the latest signal",
        "domain_id": D,
        "difficulty": 1,
        "brief": "An incident commander reads the newest information first. Show the last two lines of logs/app.log — what just happened?",
        "objectives": ["Read the tail of logs/app.log"],
        "checks": [
            {
                "command_pattern": "^tail\\s+-n\\s+2\\s+logs/app\\.log$",
                "expect_contains": "timeout after 30s",
                "hint": "Run: tail -n 2 logs/app.log — the newest lines are the freshest signal."
            }
        ],
        "success_message": "Latest signal read. In an incident, start from now and work backward."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Who is on the bridge",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Before you assign roles, know who is actually here. List the running processes — the responders on this machine.",
        "objectives": ["List running processes"],
        "checks": [
            {
                "command_pattern": "^ps$",
                "expect_contains": "python3 app.py",
                "hint": "Run: ps — see every process currently on the bridge."
            }
        ],
        "success_message": "Bridge roster confirmed. You cannot assign roles to people you have not accounted for."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Declare incident command",
        "domain_id": D,
        "difficulty": 1,
        "brief": "The IC for this drill is M. Reyes. Announce it on the channel with echo — declarations must be explicit and visible, never assumed.",
        "objectives": ["Announce the incident commander"],
        "checks": [
            {
                "command_pattern": "^echo\\s+.*Reyes.*$",
                "expect_contains": "Reyes",
                "hint": "Run: echo with a declaration naming Reyes as incident commander (e.g. echo \"IC: M. Reyes\")."
            }
        ],
        "success_message": "Command declared. If nobody says 'I am the IC,' nobody is."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Establish the timeline",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Every postmortem starts as a timeline. Read the first three lines of logs/app.log — how did this morning begin?",
        "objectives": ["Read the start of logs/app.log"],
        "checks": [
            {
                "command_pattern": "^head\\s+-n\\s+3\\s+logs/app\\.log$",
                "expect_contains": "server starting",
                "hint": "Run: head -n 3 logs/app.log — the beginning of the story."
            }
        ],
        "success_message": "Timeline started. Facts first, theories later — that is the order."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Scope the blast radius",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Leadership asks 'how bad is it?' — answer with data. Pull every ERROR line from logs/app.log to scope the impact.",
        "objectives": ["Extract all ERROR lines"],
        "checks": [
            {
                "command_pattern": "^grep\\s+ERROR\\s+logs/app\\.log$",
                "expect_contains": "ERROR connection refused",
                "hint": "Run: grep ERROR logs/app.log — scope the damage with evidence."
            }
        ],
        "success_message": "Blast radius scoped. 'How bad' is a question you answer with data, not adjectives."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Attest the runbook version",
        "domain_id": D,
        "difficulty": 2,
        "brief": "You are about to follow the on-call runbook — first verify it is the right version. Hash the token 'oncall' and confirm digest 776b17088dc5c42e637829dfb3530b7592b0dd9fba89fad9338e895c241da4b7.",
        "objectives": ["Hash the runbook token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+oncall$",
                "expect_contains": "776b17088dc5c42e637829dfb3530b7592b0dd9fba89fad9338e895c241da4b7",
                "hint": "Run: sha256sum oncall — verify before you trust."
            }
        ],
        "success_message": "Runbook attested. Trust the procedure only after you verify it."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Read the field guide",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Good commanders study before the crisis. Read the study notes, then count their lines — know the depth of the material you are commanding from.",
        "objectives": ["Read notes.txt", "Count its lines"],
        "checks": [
            {
                "command_pattern": "^cat\\s+notes\\.txt$",
                "expect_contains": "Linux essentials",
                "hint": "Run: cat notes.txt — read the field guide."
            },
            {
                "command_pattern": "^wc\\s+-l\\s+notes\\.txt$",
                "expect_contains": "8 notes.txt",
                "hint": "Run: wc -l notes.txt — how deep does the guide go?"
            }
        ],
        "success_message": "Field guide read and measured. Preparation is the part of leadership nobody sees."
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
