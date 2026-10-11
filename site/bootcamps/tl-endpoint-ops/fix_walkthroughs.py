import ast, json

P = "/home/hatch/workspace/cert-bootcamps/site/bootcamps/tl-endpoint-ops/build_cbt2.py"
src = open(P).read()
tree = ast.parse(src)

walkthroughs = [
"A learning window sized to the business calendar is what makes enforcement uneventful: the catalog then contains the real footprint, not a 7-day sample of it. Announce it, monitor it, and treat its output as a draft \u2014 the review is where judgment enters.",
"Work the uncommon list entry by entry: owner interview, signer check, install-date sanity. Each verdict (verified, removed, investigate) shrinks the riskiest part of the baseline \u2014 this is the highest-leverage review hour in the project.",
"Apply the strength ladder and the scoping worksheet to every catalog entry, and prune what nobody needs before it gets a rule. The output \u2014 a versioned, dated policy v1.0 \u2014 is what enforcement runs on and what drift diffs against.",
"Run the go/no-go as a formal record: criteria, evidence, decision, date. A no-go with a dated remediation plan is a professional outcome; a go on red criteria is a scheduled outage.",
"Read blocks as patterns, not tickets: ten identical blocks are one policy flaw. Name the pattern from the catalog, then tune the cause \u2014 through change control, with a canary.",
"Quarterly, hold each grant against its usage data: who actually uses it, what it actually covers, whether the need still exists. Squeeze what drifted, document what you changed, and keep the rollback.",
"Run the prune cycle like a change: candidates from the zero-hit report, owner notice with a speak-now window, staged removal, version history kept. Report the reduced attack surface \u2014 pruning is security work.",
"Put every cadence on the calendar with an owner: daily scans, weekly queue metrics, monthly exception reviews, quarterly squeeze-and-prune. Tuning that isn't scheduled doesn't happen.",
"Design the override as an engineered valve: narrow scope, short auto-expiry, ticketed need, and a review at expiry. The valve's usage rate is your policy-pressure gauge \u2014 rising overrides mean the policy needs tuning.",
"Place every request on the tree before deciding: known-good plus urgent gets the narrow override; unknowns get the sandbox; routine gets the queue; repeats get converted. The tree keeps urgency from becoming evidence.",
"Enforce expiry automatically and review every override at its end: convert the durable, extend the continuing with fresh justification, let the dead die. Expired-but-active is a critical finding \u2014 fix the mechanism, not just the instance.",
"Learn the four pressure scripts \u2014 manufactured urgency, borrowed authority, 'just this once,' scope inflation \u2014 and answer each with process: verify urgency, hold the evidence bar, let the expiry enforce, default to narrow. Monitor the valve itself for odd patterns.",
"Sequence every update through the rings with soak times that fit the risk: long soaks for agent binaries, shorter for policy-only changes. Ring 0 eats its own cooking and tests the rollback \u2014 emergencies compress the rings, never skip them.",
"Pre-write the pause criteria on the canary card before the rollout, so the 2 AM decision is already made. Pause is the mechanism working \u2014 investigate, then resume or roll back the tested rollback.",
"Separate the two update types into different windows: agent updates test stability with long soaks; policy updates test correctness with block-rate canaries. Bundled, their failures are unattributable \u2014 one change per window.",
"Treat MDM enrollment and profile approvals as the macOS deployment itself: enroll, push profiles, verify grants, then install. An agent without Full Disk Access is present and blind \u2014 verify capability, not just check-in.",
"Learn the macOS layer cake: Gatekeeper under your allowlist, /Applications versus the writable locations, and the built-in scripting toolkit. Triage names the decider first \u2014 the silent console is the clue.",
"Tune macOS policy with identity rules for Apple and vendor components, treat OS upgrades as policy events with pre-approvals, and check capability (approvals, version) before blaming the policy.",
"Triage macOS agents in order: approvals first (the blind agent), then capability versus assignment (policy not applying), then identity rules for system components. Manual-approval chaos gets the structural fix: MDM profiles.",
"Map every host to its distro family, deploy through the native package manager via your automation, and verify the kernel support matrix before the pilot. The matrix check is what keeps 'installed but unstable' out of production.",
"Split the policy by role: minimal ticketed baselines for servers, toolchain-manager approvals plus a fast lane for dev workstations, and the tightest leashes on the container runtime. One policy for both gives servers holes and workstations friction.",
"Triage from the shell in order: agent status and policy currency, the agent's deny log, then the system reality check with standard tools. Script the routine into a daily health check \u2014 automate the routine, save yourself for the anomalies.",
"Keep the gotcha map handy: the MAC layer may decide before your policy, /tmp and /dev/shm are executable-danger zones, services get ringfenced by user, and distro upgrades are policy events. Check the decider first.",
"Assume both attackers and frustrated users will try to remove the agent: build tamper resistance, require authorized workflows for removal, and alert on attempts. A silently removed agent showing stale-green is worse than a known-unprotected box.",
"Route every legitimate removal through ticket, approver, time-limited token, and verification \u2014 never self-service. The workflow's final step updates the asset record, which is what keeps the ghost fleet from forming.",
"Alert on every tamper attempt and triage who, what, when, and whether a ticket exists: ticketed troubleshooting is legitimate, 3 AM SYSTEM uninstalls are incident-grade. The attempt itself is the signal \u2014 work it.",
"Design for admins' real capability: self-defense plus the ticket-and-token workflow plus detection, with fewer standing admins overall. Document break-glass for true emergencies \u2014 and remember the honest limit: visibility is the real protection.",
"Run the request lifecycle end to end \u2014 intake, evidence, decision, communication \u2014 and read the queue as an instrument: volume shows baseline gaps, decisions show policy errors, repeats show process failures.",
"Publish the SLA, define urgency crisply, staff to the promise, and communicate breaches instead of hiding them. The SLA is the anti-shadow-IT control: users tolerate a visible 4-hour wait; they route around a black hole.",
"Decide fast without deciding sloppy: the 90-second triage, precedent records for repeat vendors, fast lanes for the routine \u2014 and the 60-second decision record on every call. Speed never skips the record.",
"Close every deny with a concrete next step in plain language, and measure deny-to-approval conversion to prove the paths work. A deny without a path is a bypass waiting to happen.",
"Make the sandbox the default for unknowns: submit with provenance context, read the behavior sections (not just the verdict), decide on observed behavior, and communicate plainly. Minutes of detonation beat hours of guessing.",
"Read execution, file, registry, and network sections before the verdict: canary touches reveal intent, network behavior reveals command-and-control, and multi-section patterns decide. Your read comes first; the summary confirms it.",
"Map the report to the decision: clean plus need gets a narrow rule, suspicious gets a deny with the report as evidence plus a provenance hunt, malicious pivots to incident response. Attach the report to every decision.",
"Respect the sandbox's boundaries: evasion techniques, time-bombs past the window, and generic-image fidelity limits mean a clean report is strong evidence, never proof. Extend the detonation or time-box the rule when the stakes warrant it.",
"Extract the six lines \u2014 who, what, rule, when, prevalence, verdict \u2014 before theorizing. The rule-that-fired names the investigation type, prevalence separates systemic from targeted, and signer state sorts in seconds.",
"Let prevalence direct the response: high-plus-signed gets the central rule fix, low-plus-unsigned gets the box investigation, first-seen gets the sandbox queue. The fleet is talking \u2014 the operator listens first.",
"Design retention around the questions you'll be asked, make the audit tamper-evident, and self-audit quarterly. The auditor's two proofs \u2014 the negative and the positive \u2014 come from this audit plus the exception register.",
"Run the daily loop: ten-minute pattern scan, triage by pattern type, ticketed narrow action, and verify tomorrow that the pattern moved. Correlated signals escalate to incident directly \u2014 the audit is a detection source.",
"Know your seat before the page: isolate via policy, freeze and export evidence, contain with emergency rules, and brief the IR lead. Speed on the controls, completeness on the evidence, no freelance hunting.",
"Contain with the toolkit: policy quarantine (management plane excepted), fleet-wide hash block, egress kill on the C2 \u2014 every rule time-boxed, ticketed, with release criteria written at creation.",
"Freeze the host's full audit history in the first hour, packet it as timeline plus binaries plus behaviors plus scope plus actions, and record the chain of custody. Export everything relevant \u2014 your notes annotate, never replace.",
"Write the ops postmortem within 48 hours: which control detected, signal-to-containment time, what the runbooks got wrong, and the concrete improvements. Track the trend \u2014 it's the program's report card.",
]

broken = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "L" and len(node.args) == 6:
        broken.append(node)
broken.sort(key=lambda n: n.lineno)
assert len(broken) == len(walkthroughs), f"{len(broken)} broken vs {len(walkthroughs)} walkthroughs"
for node in broken:
    assert isinstance(node.args[4], ast.List) and isinstance(node.args[5], ast.Constant), f"unexpected shape at {node.lineno}"

lines = src.split("\n")
# insert in reverse so line numbers stay valid
for node, wt in sorted(zip(broken, walkthroughs), key=lambda p: p[0].lineno, reverse=True):
    code_node = node.args[3]
    end_line = code_node.end_lineno  # 1-based; the line ends with '",'
    indent = lines[code_node.lineno - 1][:len(lines[code_node.lineno - 1]) - len(lines[code_node.lineno - 1].lstrip())]
    assert lines[end_line - 1].rstrip().endswith('",'), f"unexpected code end at line {end_line}: {lines[end_line-1][:60]}"
    lines.insert(end_line, indent + json.dumps(wt) + ",")

open(P, "w").write("\n".join(lines))
print("inserted", len(broken), "walkthroughs")
