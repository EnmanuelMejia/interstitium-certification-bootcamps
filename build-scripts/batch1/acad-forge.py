#!/usr/bin/env python3
"""Batch 1 builder: acad-forge — 5 simulations, 4 consoleSims, 7 terminalMissions."""
import json, os

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SLUG = 'acad-forge'
D = 'acad-forge'

simulations = [
    {
        "id": f"{SLUG}-sim-1",
        "title": "The broken build",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A first-time contributor opened a great PR — and CI is red. They are embarrassed and going quiet. Fix the build without crushing the contributor.",
        "steps": [
            {
                "symptom": "PR #214 from a new contributor: solid feature, failing tests. The contributor just commented 'sorry, I'll close it.'",
                "evidence": [
                    ["CI log", "PR #214 | 3 tests failing: test_total_empty, test_total_floats\nContributor: first PR ever | comment: 'sorry, I'll close it'"]
                ],
                "options": [
                    "Let them close it — the tests must pass",
                    "Reproduce the failures locally, identify the real cause, and coach them through the fix in the PR",
                    "Merge it anyway — the feature works",
                    "Rewrite their PR yourself and push to their branch"
                ],
                "correct": 1,
                "explain": "Red CI on a first PR is a teaching moment, not a rejection. You reproduce, you find the actual cause, and you coach in the open so the contributor learns and stays. Rewriting it yourself teaches them that their work was not worth fixing."
            },
            {
                "symptom": "Reproduced: their total() breaks on empty lists and floats — the tests are right, the code needs two small guards.",
                "evidence": [
                    ["Repro", "total([]) -> error (should be 0)\ntotal([1.5, 2.5]) -> 3 (should be 4.0)\nFix: ~4 lines"]
                ],
                "options": [
                    "Comment: 'Fix the edge cases' and wait",
                    "Point at the exact lines, explain why empty and float inputs matter, and let them write the fix",
                    "Push the fix to their branch yourself — faster",
                    "Disable the failing tests"
                ],
                "correct": 1,
                "explain": "Specific, kind, and hands-off the keyboard: show them where, explain why edge cases matter (empty input is the most common real-world input), and let them own the fix. The goal is a contributor who can do the next one alone."
            },
            {
                "symptom": "They fixed it. CI is green. The PR is ready to merge.",
                "evidence": [
                    ["PR #214", "CI: green | review: approved\nContributor: 'Thanks for the help — that was fun actually'"]
                ],
                "options": [
                    "Merge quietly",
                    "Merge with a genuine thank-you that names what was good about the work — then invite them to pick up another issue",
                    "Ask them to squash, rebase, and re-verify first",
                    "Hold the merge until they add more tests"
                ],
                "correct": 1,
                "explain": "The merge message is culture: name what was good, thank them publicly, and hand them the next rung on the ladder. Contributors who feel seen come back; contributors who feel processed do not."
            }
        ],
        "debrief": "You protected the contributor, taught in the open, and turned a red build into a returning contributor. Maintainers do not just merge code — they grow people.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-2",
        "title": "Merge or close?",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 2,
        "brief": "PR #220 is a good feature wrapped in 800 lines of scope creep, drive-by refactors, and a new dependency. The author is a senior engineer who 'just fixed things while in there.' Decide.",
        "steps": [
            {
                "symptom": "The core feature is 150 lines and excellent. The other 650 lines: refactored helpers, renamed variables, and a new utility library.",
                "evidence": [
                    ["PR #220", "+812 / -340 lines | core feature: ~150 lines\nExtras: refactored helpers, renames, new dep 'quickutil'\nAuthor: senior, 'fixed things while in there'"]
                ],
                "options": [
                    "Merge it — the feature is good and the author is senior",
                    "Ask for the split: feature in this PR, refactors and the new dependency in follow-ups with their own reviews",
                    "Close it — scope creep is disrespectful",
                    "Merge and revert the extras yourself later"
                ],
                "correct": 1,
                "explain": "Review the change you were asked to review. Splitting is not punishment — it is how each change gets the review it deserves, and how the next person can revert the refactor without reverting the feature. Seniority does not exempt anyone from small PRs."
            },
            {
                "symptom": "The author pushes back: 'Splitting will take me all day. Just merge it.'",
                "evidence": [
                    ["Pushback", "Author: 'This is bureaucracy. The code is good.'"]
                ],
                "options": [
                    "Cave — they are senior and busy",
                    "Hold the line kindly: offer to pair on the split for 30 minutes, and explain the new dependency needs its own security look",
                    "Escalate to their manager",
                    "Merge but leave a passive-aggressive comment"
                ],
                "correct": 1,
                "explain": "Standards held with kindness beat standards abandoned for comfort. Offering 30 minutes of pairing turns 'bureaucracy' into teamwork — and the new dependency genuinely needs its own review, which is a technical argument, not a power move."
            },
            {
                "symptom": "Split done: three clean PRs, all merged. The author thanks you.",
                "evidence": [
                    ["Outcome", "3 PRs merged | dependency reviewed separately\nAuthor: 'Okay, that was actually easier to review myself too'"]
                ],
                "options": [
                    "Say nothing — it worked out",
                    "Note the win publicly: small PRs reviewed faster and caught a real issue in the refactor",
                    "Write a policy banning large PRs",
                    "Require all PRs under 200 lines from now on"
                ],
                "correct": 1,
                "explain": "Reinforce the behavior you want with evidence, not policy. A hard line-count rule would have blocked the original 150-line feature too — judgment scales, rules do not."
            }
        ],
        "debrief": "You split scope without splitting the relationship, held the standard with an offer of help, and reinforced with evidence. Code review is leadership in small doses.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-3",
        "title": "Release day rollback",
        "kind": "respond",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The release went out at 10:00. By 10:20, the error rate is climbing and support tickets are landing. You are the release captain. Respond.",
        "steps": [
            {
                "symptom": "Error rate 1% -> 8% in 20 minutes post-release. The change: a 'small' config tweak bundled with the feature.",
                "evidence": [
                    ["Release", "v2.14.0 deployed 10:00 | errors climbing since 10:05\nSuspect: config tweak bundled with feature\nRollback: one command, ~3 min"]
                ],
                "options": [
                    "Roll back now — the release is guilty until proven innocent",
                    "Forward-fix: patch the config in production",
                    "Wait for more data — 8% might stabilize",
                    "Blame the config author"
                ],
                "correct": 0,
                "explain": "A release correlated with errors gets rolled back first and diagnosed second. Rollback is the cheapest, fastest, most reversible action you have — forward-fixing in production is surgery during an earthquake."
            },
            {
                "symptom": "Rolled back at 10:25. Errors flat again. The team wants to re-ship immediately with the config fixed.",
                "evidence": [
                    ["Status", "10:25 rollback complete | errors back to baseline\nTeam: 'We know the fix, let's re-ship now'"]
                ],
                "options": [
                    "Re-ship immediately — the fix is known",
                    "Hold the re-ship: reproduce the failure in staging, verify the fix there, then ship on the normal cadence",
                    "Ship only the config fix with no review",
                    "Cancel the release entirely"
                ],
                "correct": 1,
                "explain": "The urgency that caused the incident cannot be the urgency that fixes it. Reproduce in staging, verify the fix where it is safe, ship on cadence. 'We know the fix' is exactly what was said about the config tweak."
            },
            {
                "symptom": "Re-shipped cleanly the next day. What changes about the release process?",
                "evidence": [
                    ["Retro", "Cause: untested config bundled with feature\nDetection: 20 min (user reports beat the alerts)"]
                ],
                "options": [
                    "Ban config changes in releases",
                    "Unbundle config from code releases, add a canary stage, and alert on error-rate deltas — not user reports",
                    "Require VP approval for every release",
                    "Go back to monthly releases"
                ],
                "correct": 1,
                "explain": "Fix the system, not the symptom: config ships separately from code, canaries catch what CI cannot, and alerts should fire before users do. The rollback worked — now make sure you need it less often."
            }
        ],
        "debrief": "You rolled back instead of hero-fixing, resisted the rushed re-ship, and fixed the process that allowed the incident. Release captains are judged by reversibility, not velocity.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-4",
        "title": "The abandoned dependency",
        "kind": "troubleshoot",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Your most critical service depends on a library whose maintainer just archived the repo: 'no time, thanks all.' A CVE in it drops next week. Work the problem.",
        "steps": [
            {
                "symptom": "Library 'leftpad-plus' archived by its maintainer. Your auth service depends on it. A CVE affecting it publishes in 7 days.",
                "evidence": [
                    ["Dependency", "leftpad-plus: archived, single maintainer\nUsed by: auth service (critical path)\nCVE publishes in 7 days | no patch coming upstream"]
                ],
                "options": [
                    "Fork it immediately and patch the CVE yourself",
                    "First assess: how deep is the dependency, what does it actually do, and can it be replaced or vendored?",
                    "Ignore it — archived does not mean broken",
                    "Rewrite the auth service from scratch"
                ],
                "correct": 1,
                "explain": "Assess before you act: a 40-line string helper gets vendored in an afternoon; a deep framework integration needs a real migration plan. Forking first and understanding later leaves you maintaining a fork you did not need."
            },
            {
                "symptom": "Assessment: it is 200 lines, does one thing well, and the CVE is in a code path you actually use. No maintained alternative exists.",
                "evidence": [
                    ["Assessment", "Size: ~200 lines, single purpose\nCVE: in the used code path | alternatives: none maintained\nUsage: 3 call sites in auth service"]
                ],
                "options": [
                    "Vendor the 200 lines into your repo, patch the CVE, add tests around the vendored code, and document why",
                    "Fork the repo and publish your fork as the new official version",
                    "Wait for the community to fork it",
                    "Pin the vulnerable version and hope"
                ],
                "correct": 0,
                "explain": "For 200 lines with no alternative, vendoring wins: the code lives in your repo, under your tests, with your patch — no fork-maintenance theater. Document the why so the next person does not 'clean up' the vendored code."
            },
            {
                "symptom": "Vendored and patched. Now protect the rest of the dependency tree.",
                "evidence": [
                    ["Goal", "No more single-maintainer surprises"]
                ],
                "options": [
                    "Audit the tree for single-maintainer and archived dependencies, set up vulnerability scanning in CI, and define a policy for adopting new deps",
                    "Ban all third-party dependencies",
                    "Vendor everything preemptively",
                    "Trust that this was a one-off"
                ],
                "correct": 0,
                "explain": "One abandoned dep is a warning about the tree: audit for bus-factor-one maintainers, scan continuously in CI, and make dependency adoption a conscious decision with criteria. You cannot prevent abandonment — you can prevent surprise."
            }
        ],
        "debrief": "You assessed before forking, vendored surgically with tests, and turned one scare into dependency policy. Supply-chain thinking is maintenance thinking.",
        "points": 30
    },
    {
        "id": f"{SLUG}-sim-5",
        "title": "First open-source contribution",
        "kind": "decide",
        "domain_id": D,
        "difficulty": 1,
        "brief": "You want your first open-source contribution to count — for the project and for your portfolio. Three options are on the table. Choose well.",
        "steps": [
            {
                "symptom": "Option A: a trendy repo with 40k stars and 300 open PRs. Option B: a small tool you actually use, with 3 friendly maintainers. Option C: starting your own project from zero.",
                "evidence": [
                    ["Options", "A: 40k stars, 300 open PRs, maintainer burnout visible\nB: small tool you use daily, 3 active kind maintainers\nC: your own project, zero users"]
                ],
                "options": [
                    "A — the stars will look great on the resume",
                    "B — a used tool with kind maintainers: your PR gets reviewed, merged, and used",
                    "C — build your own thing instead",
                    "Contribute to all three at once"
                ],
                "correct": 1,
                "explain": "First contributions should optimize for merged and mentored, not stars. A small project you actually use gives you context, kind reviewers, and a merged PR that real users touch. The 40k-star repo will still be there for contribution number ten."
            },
            {
                "symptom": "You picked B. The issue list has: a typo fix, a confusing error message, and a feature request marked 'help wanted.'",
                "evidence": [
                    ["Issues", "#88: typo in README | #91: confusing error message\n#94: feature request, 'help wanted', 2 months old"]
                ],
                "options": [
                    "The feature — biggest impact for the portfolio",
                    "The error message — small, well-scoped, touches real code, and shows you care about users",
                    "The typo — safest",
                    "All three in one PR"
                ],
                "correct": 1,
                "explain": "The error-message fix is the sweet spot: real code, clear scope, visible user benefit, and reviewable in one sitting. Typos do not demonstrate much; the stale feature request is probably stale for a reason. Start where you can finish well."
            },
            {
                "symptom": "PR merged. The maintainer thanked you publicly. What goes in the portfolio?",
                "evidence": [
                    ["Result", "PR merged | maintainer thanks in the release notes"]
                ],
                "options": [
                    "'Contributed to open source' — keep it vague",
                    "Link the merged PR, describe the problem and your fix in two sentences, and note the maintainer's review — evidence, not adjectives",
                    "Claim you are a core contributor now",
                    "Do not mention it — it was small"
                ],
                "correct": 1,
                "explain": "Portfolios run on evidence: the linked PR, the problem, the fix, the review. 'Contributed to open source' says nothing; a merged PR with a maintainer's thanks says everything. Small and merged beats big and abandoned."
            }
        ],
        "debrief": "You optimized for merged over famous, scoped for finishable, and documented with evidence. That is how a portfolio gets built: one real contribution at a time.",
        "points": 30
    }
]

consoleSims = [
    {
        "id": f"{SLUG}-csim-git-1",
        "title": "Ship the portfolio update",
        "console": "git-host",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Your portfolio site needs the new project. Create a branch feat/portfolio, then open a pull request against main with the update.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Create a branch named feat/portfolio.",
                "validate": {"action": "create-branch", "params": {"name": "feat/portfolio"}},
                "hint": "Open Branches and create a branch: NAME=feat/portfolio."
            },
            {
                "id": "t2",
                "instruction": "Open a pull request titled 'Add portfolio project' from feat/portfolio into main.",
                "validate": {"action": "open-pr", "params": {"title": "Add portfolio project", "base": "main", "head": "feat/portfolio"}},
                "hint": "Open a PR: TITLE='Add portfolio project', BASE=main, HEAD=feat/portfolio."
            }
        ],
        "debrief": "Branch, then PR: the smallest possible shipping loop. Every portfolio update should flow through review, even your own."
    },
    {
        "id": f"{SLUG}-csim-git-2",
        "title": "Review and merge the health check",
        "console": "git-host",
        "domain_id": D,
        "difficulty": 2,
        "brief": "PR #1 'Add health check endpoint' is reviewed and green. Approve it, then merge it — shipping is a verb.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Approve PR #1.",
                "validate": {"action": "approve-pr", "params": {"pr": 1}},
                "hint": "On PR #1 (Add health check endpoint), approve it: PR=1."
            },
            {
                "id": "t2",
                "instruction": "Merge PR #1.",
                "validate": {"action": "merge-pr", "params": {"pr": 1}},
                "hint": "Merge PR #1 — approve first, then merge."
            }
        ],
        "debrief": "Approved and merged. Reviews are not bureaucracy — they are the last cheap place to catch mistakes."
    },
    {
        "id": f"{SLUG}-csim-cicd-1",
        "title": "Green the pipeline",
        "console": "cicd-pipeline",
        "domain_id": D,
        "difficulty": 2,
        "brief": "The pipeline shows a failed test stage. Trigger a fresh build, then retry the test stage — flaky tests get retried, real failures get fixed.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Trigger a new build.",
                "validate": {"action": "trigger-build", "params": {}},
                "hint": "Trigger a build — resets the stages so you can work them."
            },
            {
                "id": "t2",
                "instruction": "Retry the test stage.",
                "validate": {"action": "retry-stage", "params": {"stage": "test"}},
                "hint": "Retry the failed stage: STAGE=test."
            }
        ],
        "debrief": "Trigger, retry, observe. CI is a feedback loop — keep it fast and keep it honest."
    },
    {
        "id": f"{SLUG}-csim-code-1",
        "title": "Fix the float bug",
        "console": "code-editor",
        "domain_id": D,
        "difficulty": 2,
        "brief": "A reviewer flagged it: total() in app.py starts its accumulator at int 0, so float inputs lose their type. Open app.py and fix line 2 to start from 0.0.",
        "tasks": [
            {
                "id": "t1",
                "instruction": "Open the file app.py.",
                "validate": {"action": "open-file", "params": {"name": "app.py"}},
                "hint": "Open app.py in the editor."
            },
            {
                "id": "t2",
                "instruction": "Fix line 2 of app.py to read exactly: four spaces, then 's = 0.0'.",
                "validate": {"action": "fix-line", "params": {"file": "app.py", "line": 2, "text": "    s = 0.0"}},
                "hint": "Fix line 2: FILE=app.py, LINE=2, TEXT='    s = 0.0' (keep the four-space indent)."
            }
        ],
        "debrief": "Small fix, real review, typed correctly. Most shipped bugs are one-line fixes that nobody reviewed — this one got both."
    }
]

terminalMissions = [
    {
        "id": f"{SLUG}-mission-1",
        "title": "Inventory the project",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Before you build, know what you have. List the project directory — every build starts with an inventory.",
        "objectives": ["List the project files"],
        "checks": [
            {
                "command_pattern": "^ls$",
                "expect_contains": "app.py",
                "hint": "Run: ls — see what is in the project."
            }
        ],
        "success_message": "Project inventoried. You cannot build on what you have not looked at."
    },
    {
        "id": f"{SLUG}-mission-2",
        "title": "Read the code",
        "domain_id": D,
        "difficulty": 1,
        "brief": "Read app.py before you change anything. Shipping starts with understanding.",
        "objectives": ["Read app.py"],
        "checks": [
            {
                "command_pattern": "^cat\\s+app\\.py$",
                "expect_contains": "def greet",
                "hint": "Run: cat app.py — read before you write."
            }
        ],
        "success_message": "Code read. The cheapest bug fix is the one you understand before touching."
    },
    {
        "id": f"{SLUG}-mission-3",
        "title": "Measure the codebase",
        "domain_id": D,
        "difficulty": 1,
        "brief": "How big is this thing, really? Count the lines in app.py — shipped work gets measured.",
        "objectives": ["Count the lines in app.py"],
        "checks": [
            {
                "command_pattern": "^wc\\s+-l\\s+app\\.py$",
                "expect_contains": "5 app.py",
                "hint": "Run: wc -l app.py (pass the file; stdin is not simulated)."
            }
        ],
        "success_message": "5 lines. Small codebases ship; measure yours as it grows."
    },
    {
        "id": f"{SLUG}-mission-4",
        "title": "Find the TODOs",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Every project has TODOs hiding in the notes. Search notes.txt for TODO — unfinished work should be visible, not buried.",
        "objectives": ["Find TODO markers"],
        "checks": [
            {
                "command_pattern": "^grep\\s+TODO\\s+notes\\.txt$",
                "expect_contains": "TODO",
                "hint": "Run: grep TODO notes.txt — surface the unfinished work."
            }
        ],
        "success_message": "TODOs surfaced. Visible backlogs get finished; hidden ones rot."
    },
    {
        "id": f"{SLUG}-mission-5",
        "title": "Find the dev server",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Something is serving on this machine. List the processes and identify the server — know what is running before you deploy beside it.",
        "objectives": ["Identify the running server"],
        "checks": [
            {
                "command_pattern": "^ps$",
                "expect_contains": "node server.js",
                "hint": "Run: ps — which process is the server?"
            }
        ],
        "success_message": "Server found. Deployments go beside running services, never blind."
    },
    {
        "id": f"{SLUG}-mission-6",
        "title": "Sign the release",
        "domain_id": D,
        "difficulty": 2,
        "brief": "Releases get signed so users can verify them. Hash the release token 'deploy-key' and confirm digest 3e245e375abacce2c31f9db9b063994b9a73c5c19d839a3ce21e77983111bd34.",
        "objectives": ["Hash the release token", "Confirm the digest"],
        "checks": [
            {
                "command_pattern": "^sha256sum\\s+deploy-key$",
                "expect_contains": "3e245e375abacce2c31f9db9b063994b9a73c5c19d839a3ce21e77983111bd34",
                "hint": "Run: sha256sum deploy-key — the digest must match character for character."
            }
        ],
        "success_message": "Release signed. Shipped artifacts are verifiable artifacts."
    },
    {
        "id": f"{SLUG}-mission-7",
        "title": "Verify the release infrastructure",
        "domain_id": D,
        "difficulty": 3,
        "brief": "Before the release goes out, verify the infrastructure it depends on: ping the registry for connectivity, then resolve it with dig. Releases fail on untested dependencies.",
        "objectives": ["Confirm connectivity", "Confirm DNS resolution"],
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
        "success_message": "Infrastructure verified. Ship on tested ground, not hope."
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
