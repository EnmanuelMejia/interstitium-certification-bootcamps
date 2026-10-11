#!/usr/bin/env python3
"""Part 10: Main driver - assembles all 10 CBTs to full-stack standard."""
import json, sys, importlib
sys.path.insert(0, '/home/hatch/workspace/cert-bootcamps')
from expand_batch1 import (L, S, LB, CHECK, start_here_lessons, mock_domain,
    mock_briefing_lessons, capstone_domain, capstone_lessons, ensure_domains,
    add_lessons, add_scenarios, add_labs, counts)
from expand_batch7a import (CBT_CONFIG, EXTRA_DOMAINS_SMALL, career_roadmap_lessons,
    tools_ecosystem_lessons)
from expand_batch7b import extra_domain_lessons
from expand_batch8 import topup_secplus, topup_netplus, topup_infra, extra_labs_batch8
from expand_batch9 import (topup_data_analyst, topup_data_engineering, topup_cpp,
    topup_data_analyst as _t, extra_labs_batch9)

import expand_batch9 as b9
import expand_batch11 as b11

TOPUP_FNS = {
    "comptia-security-plus": topup_secplus,
    "comptia-network-plus": topup_netplus,
    "comptia-infra": topup_infra,
    "cpp": b9.topup_cpp,
    "creative-code": b11.topup_creative,
    "cybernetics": b11.topup_cybernetics,
    "data-analyst": topup_data_analyst,
    "data-analyst-to-ml": b11.topup_daml,
    "data-engineering": topup_data_engineering,
    "data-science-certs": b11.topup_dsc,
}

BASE = '/home/hatch/workspace/cert-bootcamps/site/bootcamps'

# ---------------------------------------------------------------- third lessons for new topical domains (to reach 3 each)
def third_lessons():
    T = {}
    # security-plus new domains
    T["exam-strategy-sec"] = [
        L("Test-Day Protocol: The Final 24 Hours",
          "exam-strategy",
          ["No new material in the final 24 hours: review the error log, flashcards, and exam strategy only. Novelty now creates anxiety, not knowledge.",
           "Logistics beat last-minute study: ID, confirmation, route, parking, backup plan. A forgotten ID fails you before question one.",
           "Sleep is the study: 8 hours the last 2-3 nights. Memory consolidation happens in sleep \u2014 the all-nighter trades retention for exhaustion.",
           "Exam morning: normal routine, real breakfast, arrive 30 minutes early. In the waiting room: breathe deeply, not cram."],
          "T-24h checklist:\n  [ ] Error log reviewed (all entries answerable)\n  [ ] ID + confirmation + route confirmed\n  [ ] 8h sleep x2 nights banked\n  [ ] Strategy card: time budget, flag-and-move, no blanks\n  [ ] Nothing new after 8 PM",
          "The final day is about arriving ready, not getting ready. Trust the weeks of work.",
          ["Cramming new topics \u2014 anxiety, not learning.",
           "All-nighter \u2014 costs more points than any cram gains.",
           "Skipping logistics \u2014 the forgotten ID is the most preventable fail."],
          "Write your T-24h checklist now with your exam's actual logistics."),
    ]
    return T

def build_third_lessons():
    """Additional lessons for new topical domains, keyed by (cbt, domain_id) -> [lessons]."""
    D = {}
    def add(cbt, did, lesson):
        D.setdefault(cbt, {}).setdefault(did, []).append(lesson)

    # ---- security-plus
    add("comptia-security-plus", "exam-strategy", L("Test-Day Protocol: The Final 24 Hours", "exam-strategy",
        ["No new material in the final 24 hours: review the error log, flashcards, and strategy only. Novelty now creates anxiety, not knowledge.",
         "Logistics beat last-minute study: ID, confirmation, route, parking, backup plan. A forgotten ID fails you before question one.",
         "Sleep is the study: 8 hours the last 2-3 nights. Memory consolidation happens in sleep.",
         "Exam morning: normal routine, real breakfast, arrive 30 minutes early. Breathe, don't cram."],
        "T-24h checklist:\n  [ ] Error log reviewable  [ ] ID + route confirmed\n  [ ] 8h sleep x2  [ ] Strategy: time budget, flag-and-move, no blanks",
        "The final day is about arriving ready, not getting ready. Trust the work.",
        ["Cramming new topics \u2014 anxiety, not learning.", "All-nighter \u2014 costs more than it gains.", "Skipping logistics \u2014 preventable fail."],
        "Write your T-24h checklist with your exam's actual logistics."))
    add("comptia-security-plus", "soc-playbook", L("Writing the Incident Report", "soc-playbook",
        ["The incident report has two audiences: executives (impact, timeline, business risk) and engineers (root cause, IOCs, fixes). Write both sections; neither audience reads the other's.",
         "Structure: executive summary (3 bullets) \u2192 timeline (timestamped facts, no speculation) \u2192 root cause \u2192 impact \u2192 remediation (done + planned) \u2192 lessons learned.",
         "Facts vs inference: 'At 09:14 the host beaconed to 203.0.113.44' (fact) vs 'the attacker likely...' (inference \u2014 label it). Mixing them poisons the report.",
         "Blameless language: 'the process allowed' not 'John failed to'. Reports that blame don't get read honestly next time \u2014 and there is always a next time."],
        "Timeline entry:\n  09:12 \u2014 IDS alert: mass file renames on WS-011 (fact)\n  09:18 \u2014 EDR shows C2 beacon to 203.0.113.44 (fact)\n  09:20 \u2014 host isolated from network (action)\n  Inference (labeled): initial access likely via phishing (pending email review).",
        "Write the report within 48 hours while memory is fresh. Late reports are fiction; fast reports are evidence.",
        ["Speculation as fact \u2014 label every inference; facts stand alone.",
         "Blame language \u2014 kills future reporting honesty.",
         "No remediation owners/dates \u2014 findings without owners are wishes."],
        "Outline an incident report for a scenario in this bootcamp using the structure above."))
    add("comptia-security-plus", "crypto-lab", L("PKI in the Enterprise", "crypto-lab",
        ["Enterprise PKI: offline root CA (powered off, in a safe) \u2192 online issuing CAs \u2192 certificates. The root's private key is the kingdom \u2014 protect it like one.",
         "Certificate templates define what gets issued: enrollment permissions, validity periods, key usages. Template misconfiguration (e.g., allowing SAN specification) enables privilege escalation (see: ESC8).",
         "Auto-enrollment via Group Policy: machines and users get certificates transparently. The operational win \u2014 and the reason template security matters so much.",
         "Monitoring PKI health: expiring CA certs, failed enrollments, CRL publication. A PKI nobody watches fails at the worst moment \u2014 usually during an outage when certs matter most.",
         "Key archival and recovery: encryption certificates need key recovery (or data is lost with the key); signing certificates must NOT be archived (non-repudiation). Know the difference."],
        "ESC8-style finding:\n  Template allows requester-supplied SAN + client auth EKU.\n  Attack: request cert as 'administrator', authenticate as admin.\n  Fix: disable SAN specification, restrict enrollment, audit templates.\n  The template WAS the vulnerability \u2014 review them like firewall rules.",
        "Audit certificate templates with the same paranoia as firewall rules: each setting is a potential privilege path.",
        ["Online root CA \u2014 the root should be offline; compromise is then catastrophic and total.",
         "SAN-supplying templates with auth EKUs \u2014 the ESC8-class misconfiguration; audit now.",
         "No key recovery for encryption certs \u2014 lost key = lost data, permanently."],
        "List the certificate templates in your environment (or a lab CA). Flag any allowing SAN specification."))
    add("comptia-security-plus", "incident-response", L("Lessons-Learned That Change Things", "incident-response",
        ["The lessons-learned meeting happens within 2 weeks, blameless, with the responders in the room. Later than that, memory fades and defensiveness hardens.",
         "Structure: what happened (timeline) \u2192 what went well \u2192 what hurt \u2192 30/60/90-day fixes with owners. Every fix needs a name and a date \u2014 or it is not a fix.",
         "Measure the fixes: did MTTD improve? Did the playbook get updated? Did the control get deployed? Lessons without metrics are stories.",
         "Share appropriately: sanitized lessons with the wider org (so other teams benefit), full detail with leadership. The incident's tuition should educate more than the responders.",
         "Track recurrence: the same root cause twice means the lesson failed. Escalate the pattern \u2014 repeated lessons are a management problem, not a technical one."],
        "90-day fix example:\n  Finding: 'No network segmentation let ransomware spread laterally.'\n  30d: segment backups (owner: net-team, done)\n  60d: segment server VLANs (owner: net-team, in progress)\n  90d: zero-trust pilot for crown jewels (owner: arch-team)\n  Each with a date, an owner, and a verification method.",
        "The incident is expensive tuition. The lessons-learned process is how you make sure the tuition wasn't wasted.",
        ["Blame-focused reviews \u2014 participants go silent; the real lessons hide.",
         "Fixes without owners/dates \u2014 the report gathers dust; nothing changes.",
         "No recurrence tracking \u2014 the same incident twice means the process failed."],
        "Write 3 lessons-learned fixes (30/60/90) for an incident you know, each with owner and verification."))
    # ---- network-plus
    add("comptia-network-plus", "exam-strategy", L("Test-Day Protocol: The Final 24 Hours", "exam-strategy",
        ["No new material in the final 24 hours: review subnetting speed, the OSI cheat sheet, and exam strategy only.",
         "Logistics: ID, confirmation, route, parking. Arrive 30 minutes early; breathe, don't cram.",
         "Sleep 8 hours the last 2-3 nights. Subnetting speed comes from a rested brain.",
         "During: budget time per question, flag-and-move on stuck PBQs, no blanks."],
        "T-24h: [ ] subnetting drills (10, timed) [ ] ID + route [ ] 8h sleep [ ] strategy card",
        "Trust the preparation. The final day is logistics and rest.",
        ["Cramming new topics.", "All-nighter.", "Skipping logistics."],
        "Time 10 subnetting problems now. Record your average \u2014 that is your exam pace."))
    add("comptia-network-plus", "subnetting-mastery", L("Supernetting and Route Summarization", "subnetting-mastery",
        ["Supernetting (route summarization) is subnetting in reverse: combine contiguous subnets into one larger advertisement. 192.168.0.0/24 + 192.168.1.0/24 = 192.168.0.0/23.",
         "Why summarize: smaller routing tables, less update traffic, faster convergence. The internet runs on summarization \u2014 BGP would collapse without it.",
         "The rule: summarize where the address plan allows \u2014 contiguous blocks with aligned boundaries. Good addressing plans summarize cleanly; bad ones don't.",
         "Watch for discontiguous subnets: summarizing across a gap creates black holes (traffic for the gap goes nowhere). Summarize only what you actually own contiguously.",
         "Exam pattern: 'which summary route covers these networks?' \u2014 find the common bits, count them, that is the prefix length. Binary is the honest method."],
        "Summarize 10.1.0.0/24, 10.1.1.0/24, 10.1.2.0/24, 10.1.3.0/24:\n  Third octet: 0=00000000, 1=00000001, 2=00000010, 3=00000011\n  Common bits: first 6 of the octet \u2192 /22 (16+6)\n  Summary: 10.1.0.0/22 \u2014 covers .0\u2013.3 exactly.",
        "Summarization rewards good addressing plans and punishes bad ones. Design address space to summarize \u2014 future-you (and BGP) will thank you.",
        ["Summarizing discontiguous space \u2014 black holes for the gaps.",
         "Over-summarization \u2014 advertising space you don't own attracts others' traffic.",
         "Binary-free guessing \u2014 write the bits; the answer is in them."],
        "Summarize 172.16.8.0/24 through 172.16.11.0/24. Show the binary work."))
    add("comptia-network-plus", "wireless-deep", L("Wireless Troubleshooting Toolkit", "wireless-deep",
        ["The toolkit: spectrum analyzer (interference), survey mode (signal/heatmaps), client debugs (why did IT disconnect?), and packet capture (802.11 frames tell the truth).",
         "Client-side first: does the CLIENT see the SSID? At what signal? Client drivers lie less than infrastructure dashboards \u2014 start where the pain is.",
         "Common signatures: slow everywhere = interference or capacity; one area = coverage; one client = driver/config; intermittent = roaming or DFS events.",
         "DFS channels (52-144): radar detection forces channel changes. If clients drop periodically on DFS channels, move to non-DFS or accept the radar dance.",
         "Document the baseline: signal, SNR, channel utilization, client count per AP \u2014 when normal. Troubleshooting compares against baseline, not against hope."],
        "Ticket: 'WiFi slow in Building B, started Tuesday.'\n  Check: channel utilization 85% (was 40%) \u2014 what changed Tuesday?\n  Found: new AP on overlapping channel from the tenant next door.\n  Fix: coordinate or move channels; document the baseline for next time.",
        "'What changed?' is the most powerful troubleshooting question. Baselines make it answerable.",
        ["Blaming the controller for a client driver bug \u2014 check the client side first.",
         "Ignoring DFS behavior \u2014 periodic drops on DFS channels are radar, not ghosts.",
         "No baseline \u2014 without normal, every number is just a number."],
        "Write the 5-item wireless baseline for your environment. What is missing today?"))
    add("comptia-network-plus", "wan-edge", L("SD-WAN Policy Design", "wan-edge",
        ["Policy = business intent in rules: 'voice gets the best path, always; bulk backup uses whatever is cheapest; guest internet breaks out locally.' Write the intent before the config.",
         "Path selection inputs: loss, latency, jitter per tunnel (measured continuously). Policy maps application SLAs to path quality \u2014 voice needs low jitter; backup needs bandwidth.",
         "Failover design: sub-second for critical apps (pre-built standby tunnels), seconds for the rest. Test failover quarterly \u2014 untested failover is hope.",
         "Security policy rides along: which traffic gets inspected where, encryption standards per tunnel, and the zero-trust posture (every site authenticated, every tunnel encrypted).",
         "Start with 3 policies: critical (best path + fast failover), default (balanced), bulk (cheapest path). Complexity grows from there \u2014 earn it."],
        "Policy sketch:\n  VOICE: prefer MPLS; failover to broadband if loss >1%; alert on failover.\n  BUSINESS-APPS: best-quality tunnel; balance across both.\n  BACKUP: cheapest path; deprioritize during business hours.\n  GUEST: local internet breakout; never traverse WAN.\n  Four lines that run the WAN.",
        "Policy design is business translation: SLAs become path rules. Write the intent in English first; the config is just transcription.",
        ["Config before intent \u2014 clicking without the policy written down produces chaos.",
         "No failover testing \u2014 the first real failover should not be during an outage.",
         "One policy for everything \u2014 voice and backups have opposite needs; differentiate."],
        "Write the 4-line policy for a hypothetical 5-site company. What would you measure to validate it?"))
    # ---- infra
    add("comptia-infra", "exam-strategy", L("Test-Day Protocol: The Final 24 Hours", "exam-strategy",
        ["No new material: review command cheat sheets, the PBQ patterns, and exam strategy only.",
         "Logistics: ID, confirmation, route. Arrive early; breathe.",
         "Sleep 8 hours. Command syntax recall needs a rested brain.",
         "During: read PBQ tasks twice, smallest verifiable step first, flag-and-move."],
        "T-24h: [ ] command flashcards [ ] ID + route [ ] 8h sleep [ ] PBQ protocol",
        "Trust the labs. You have executed these commands \u2014 the exam just asks you to recognize them.",
        ["Cramming new commands.", "All-nighter.", "Skipping logistics."],
        "Run through your 10 most-used commands from memory. Any hesitation = flashcard it."))
    add("comptia-infra", "capacity-planning", L("Forecasting Growth", "capacity-planning",
        ["Forecasting needs history: 6-12 months of utilization data minimum. Less than that and you are guessing with extra steps \u2014 say so honestly.",
         "Linear trend + seasonality: most infrastructure grows linearly with seasonal bumps. Fit the trend, note the peaks, plan for peak + headroom \u2014 not the average.",
         "Event-driven growth breaks trends: product launches, acquisitions, viral moments. Keep a 20% buffer for the unplannable \u2014 and a fast procurement path.",
         "Present forecasts as ranges: 'we need 40-60TB by Q3, most likely 48TB.' Ranges are honest; point estimates are lies with decimal places.",
         "Review quarterly: forecasts decay. The Q1 forecast is stale by Q3 \u2014 refresh it on a cadence, not when panic strikes."],
        "Storage forecast:\n  Current: 30TB, growing 1.5TB/quarter (linear, R\u00b2=0.94)\n  Q3 need: 30 + 3\u00d71.5 = 34.5TB \u2192 plan 40TB (headroom)\n  Range: 37-43TB. Procure at 35TB used (lead time!).\n  Honest, ranged, actionable.",
        "Forecasting is applied humility: the range matters more than the point, and the review cadence matters more than the model.",
        ["Point-estimate forecasts \u2014 false precision; always present ranges.",
         "Ignoring lead times \u2014 procurement takes weeks; trigger orders BEFORE need.",
         "Set-and-forget forecasts \u2014 refresh quarterly or the forecast becomes fiction."],
        "Forecast one resource you manage: 4 quarters of history, trend, range for next 2 quarters."))
    add("comptia-infra", "hybrid-cloud", L("Migration Strategies: 6 Rs", "hybrid-cloud",
        ["The 6 Rs: Rehost (lift-and-shift), Replatform (minor tweaks), Repurchase (SaaS swap), Refactor (re-architect), Retain (stay), Retire (decommission). Name the strategy per workload \u2014 no defaults.",
         "Rehost is fastest but imports technical debt to the cloud (and the bill). Use for time pressure; plan the refactor as phase 2 \u2014 or the debt compounds.",
         "Retire first: 20-30% of discovered workloads are unused. Decommission before migrating \u2014 the cheapest migration is the one you don't do.",
         "Wave planning: start with low-risk, low-dependency workloads (dev/test). Learn the process cheaply, then attack the critical systems with experience.",
         "Rollback per wave: each migration needs a backout plan tested BEFORE cutover. 'We'll figure it out' is not a rollback plan."],
        "Wave 1 (learn): dev/test environments \u2014 rehost, low risk.\n  Wave 2 (prove): internal apps \u2014 replatform to managed DB.\n  Wave 3 (earn): customer-facing \u2014 refactor critical paths.\n  Throughout: retire the 25% nobody uses. Discovered, not migrated.",
        "Migration is a portfolio exercise: each workload gets its own R, its own wave, its own rollback. The plan is the project.",
        ["Lift-and-shift everything \u2014 imports debt and maximizes the bill.",
         "No retirement pass \u2014 migrating dead workloads is expensive theater.",
         "Big-bang cutover \u2014 waves exist because big bangs create big outages."],
        "Classify 5 workloads you know into the 6 Rs. Which wave goes first? Why?"))
    add("comptia-infra", "automation-iaac", L("GitOps for Infrastructure", "automation-iaac",
        ["GitOps: git is the source of truth; agents reconcile reality to git. Change = pull request; deploy = merge. The audit trail is free \u2014 it is the git log.",
         "The loop: PR \u2192 review \u2192 CI validates (plan/lint) \u2192 merge \u2192 agent applies \u2192 drift detection alerts on manual changes. Every step is visible and reversible.",
         "Drift detection is the killer feature: manual console changes get flagged (or auto-reverted). The 'quick fix in the console' dies \u2014 and good riddance.",
         "Secrets in GitOps: sealed secrets or external vault references \u2014 never plaintext. The repo is the truth, but some truths are encrypted.",
         "Start small: one non-critical service, full GitOps loop. Prove the workflow, then expand. The cultural shift (no more console cowboys) is the hard part."],
        "GitOps loop:\n  1. Edit infra/values.yaml \u2192 PR\n  2. CI: terraform plan posted as comment\n  3. Review + merge\n  4. Agent applies; dashboard shows sync\n  5. Manual console change \u2192 drift alert in 5 min\n  Every change reviewed, tested, traceable.",
        "GitOps turns infrastructure into software engineering: reviewed, tested, reversible. The console becomes read-only by culture.",
        ["Plaintext secrets in git \u2014 sealed/vault references only; the repo is public to the team.",
         "No drift detection \u2014 without it, GitOps is just 'git-stored' with extra steps.",
         "Big-bang adoption \u2014 one service first; the workflow must prove itself."],
        "Sketch the GitOps loop for one service you manage. What breaks first in your current process?"))
    # ---- cpp
    add("cpp", "interview-prep", L("System Design for C++ Engineers", "interview-prep",
        ["C++ system design interviews test: concurrency architecture, memory layout awareness, and latency thinking \u2014 not just 'which database'.",
         "Lead with constraints: throughput? latency p99? memory budget? The numbers choose the architecture \u2014 1M msg/sec needs lock-free queues; 1K/sec needs clarity.",
         "Talk data flow: where does data live, who mutates it, how do threads coordinate? Draw the ownership and the synchronization \u2014 the diagram IS the answer.",
         "Latency vocabulary: cache misses (~100ns), syscalls (~1\u00b5s), network (~100\u00b5s-1ms). Budget the p99 from these \u2014 interviewers love the arithmetic.",
         "Trade-off close: 'I'd start with X for clarity; if profiling shows Y, I'd switch to Z.' Decisions with escape hatches beat premature optimization."],
        "Design: 100k msg/sec market data fan-out, p99 < 1ms.\n  Ingest: lock-free SPSC queue per producer (no contention)\n  Process: single-threaded matching (no locks, cache-hot)\n  Fan-out: shared-memory ring to consumers\n  p99 budget: queue (100ns) + process (10\u00b5s) + ring (1\u00b5s) \u2014 fits.\n  The numbers justify every choice.",
        "System design for C++ roles is latency arithmetic + concurrency architecture. Lead with numbers, draw the data flow, name the trade-offs.",
        ["No numbers \u2014 'fast' is not a requirement; quantify or guess explicitly.",
         "Locks everywhere \u2014 the default that kills p99; design lock-free first.",
         "Ignoring the memory layout \u2014 cache behavior IS the performance story."],
        "Design a 10k req/sec key-value cache on paper: data structures, threading, p99 budget. Time: 20 min."))
    add("cpp", "concurrency", L("Lock-Free Programming Basics", "concurrency",
        ["Lock-free = at least one thread always progresses (vs wait-free = all do). The goal is usually avoiding mutex contention in hot paths \u2014 not ideology.",
         "The atomics toolkit: load/store, exchange, compare_exchange_weak/strong (CAS loop). CAS is the fundamental primitive \u2014 everything lock-free builds on it.",
         "Memory ordering: seq_cst (safest, slowest), acquire/release (the workhorse pairing), relaxed (counters only, with proof). Default seq_cst until profiling + reasoning justify less.",
         "ABA problem: CAS succeeds but the value changed A\u2192B\u2192A underneath. Solutions: tagged pointers, hazard pointers, epoch reclamation. Know it exists; use libraries for the hard parts.",
         "Rule: use battle-tested lock-free structures (moodycamel queues, folly) before hand-rolling. Hand-rolled lock-free is where careers go to debug."],
        "// Lock-free stack (educational \u2014 use a library in production):\nstd::atomic<Node*> head;\nvoid push(Node* n) {\n  n->next = head.load();\n  while (!head.compare_exchange_weak(n->next, n));\n}\n// The CAS loop: retry until the world stops changing under us.",
        "Lock-free is a scalpel for profiled contention, not a default. Understand CAS and ordering; use libraries for production; hand-roll only to learn.",
        ["Hand-rolled lock-free in production \u2014 subtle, untestable edge cases; use libraries.",
         "Relaxed ordering without proof \u2014 the bugs are heisenbugs; default seq_cst.",
         "Ignoring ABA \u2014 the classic lock-free trap; know it by name."],
        "Implement the lock-free stack above. Then find one bug class it has (hint: ABA/memory reclamation)."))
    add("cpp", "perf-optimization", L("Benchmarking Rigorously", "perf-optimization",
        ["Benchmark with Google Benchmark or equivalent: it handles warmup, repetition, and statistics. Hand-rolled timers lie (cold caches, single runs, noise).",
         "Rules: warm up, many iterations, report median (not mean \u2014 outliers skew), disable CPU frequency scaling, pin to a core, close the browser. Rigor is the result.",
         "Prevent optimization elision: benchmark::DoNotOptimize(result) \u2014 otherwise the compiler deletes your 'work' and you benchmark nothing.",
         "Compare correctly: A/B on the same machine, same load, interleaved runs. 'My laptop vs the server' is not a benchmark \u2014 it is two anecdotes.",
         "Statistical significance: if the error bars overlap, there is no winner. Report confidence intervals, not just means \u2014 honesty in numbers."],
        "google/benchmark skeleton:\n  static void BM_lookup(benchmark::State& s) {\n    auto table = build();\n    for (auto _ : s) {\n      auto r = table.find(s.range(0));\n      benchmark::DoNotOptimize(r);\n    }\n  }\n  BENCHMARK(BM_lookup)->Range(8, 8192);\n  // Median, IQR, done right.",
        "Bad benchmarks are worse than no benchmarks: they justify wrong decisions with numbers. Rigor is not pedantry \u2014 it is the difference between data and decoration.",
        ["Single-run timing \u2014 noise dominates; repeat and take medians.",
         "No DoNotOptimize \u2014 the compiler optimized away your benchmark; you measured nothing.",
         "Mean without variance \u2014 overlapping error bars mean no conclusion; report the spread."],
        "Benchmark vector push_back vs reserve+push_back with Google Benchmark (or a careful manual harness). Report median + spread."))
    add("cpp", "modern-cpp", L("C++23: What's Actually Useful", "modern-cpp",
        ["std::expected: the error-handling upgrade \u2014 return expected<Value, Error> instead of exceptions or error codes. Explicit, composable, no overhead. The biggest practical C++23 feature.",
         "Deducing this: explicit object parameters simplify CRTP and recursive lambdas. `void f(this auto&& self)` \u2014 cleaner forwarding, less boilerplate.",
         "Ranges upgrades: more adaptors (zip, chunk, slide), ranges::to for container conversion. The ranges library keeps growing into the obvious gaps.",
         "std::mdspan: non-owning multidimensional views \u2014 the scientific computing crowd's long wait is over. Think span, but N-dimensional.",
         "Adoption reality: compiler support is rolling out; library features land first. Learn the concepts now, adopt per your toolchain's support \u2014 check, don't assume."],
        "// std::expected: errors as values\nstd::expected<int, std::string> parse(std::string_view s) {\n  if (s.empty()) return std::unexpected(\"empty input\");\n  return 42;\n}\nauto r = parse(\"\");\nif (!r) log(r.error());  // explicit, no exceptions, no codes.",
        "C++23's theme is 'explicit and composable': expected for errors, deducing-this for cleaner generics. Learn the ideas; adopt as toolchains allow.",
        ["Assuming full support \u2014 check your compiler version; C++23 is still rolling out.",
         "Ignoring std::expected \u2014 it is the most broadly useful addition; learn it first.",
         "Chasing every feature \u2014 concepts/ranges (C++20) matter more today than C++23 novelties."],
        "Rewrite one error-code function using std::expected (or sketch it). Compare readability with the old version."))
    # ---- creative-code
    add("creative-code", "showcase-strategy", L("Pricing and Client Work", "showcase-strategy",
        ["Pricing models: day rate (simple, common), project rate (scope-defined), licensing (for reusable work). Never hourly for creative \u2014 it punishes efficiency.",
         "Scope in writing: deliverables, revisions (2-3 included), timeline, kill fee (50% if cancelled). The contract prevents the 'just one more change' death spiral.",
         "Day rates anchor on value + market: research local rates, then price on the value delivered (an installation driving foot traffic is worth more than hours). Raise annually.",
         "The 50/50 payment split: 50% upfront (non-refundable), 50% on delivery. No work without the deposit \u2014 this rule has saved more artists than any technique.",
         "Say no to spec work and 'exposure': portfolio pieces you choose beat free client work. Exposure doesn't pay rent; curation does."],
        "Project quote:\n  Interactive lobby piece: $8,000 project rate\n  Includes: concept, build, install support, 2 revision rounds\n  Terms: 50% deposit, 50% on acceptance; kill fee 50%\n  Timeline: 6 weeks. Overage: $1,200/day.\n  Written, signed, then work begins.",
        "Business skills ARE creative skills: the artists who thrive treat contracts, pricing, and scope as part of the craft. Learn them deliberately.",
        ["Hourly billing for creative \u2014 punishes your speed; price the value.",
         "No written scope \u2014 'just one more tweak' becomes 40 unpaid hours.",
         "Starting without deposit \u2014 the deposit is the client's commitment device."],
        "Write a project quote for hypothetical work using the template. What would you charge per day? Research one data point."))
    add("creative-code", "shaders-intro", L("Post-Processing Effects", "shaders-intro",
        ["Post-processing = fullscreen shader passes over the rendered scene: bloom, vignette, grain, chromatic aberration. The 'cinematic' look is mostly post.",
         "Bloom: bright-pass (threshold) + blur (multi-scale) + add back. Glow without the GPU melting \u2014 the classic.",
         "Vignette + grain: darken edges (focus), add animated grain (film feel). Two cheap effects that add enormous production value.",
         "Chromatic aberration: offset RGB channels radially. Subtle = cinematic; strong = broken-lens aesthetic. A little goes a long way.",
         "Chain order matters: render scene \u2192 bloom \u2192 color grade \u2192 vignette/grain \u2192 output. Each pass is a fullscreen quad \u2014 profile the chain; passes add up."],
        "Minimal post chain (GLSL-ish):\n  vec3 c = texture(scene, uv).rgb;\n  c += bloom(uv) * 0.6;              // glow\n  c = grade(c);                      // lift/gamma/gain\n  c *= 1.0 - 0.4 * length(uv - 0.5); // vignette\n  c += (hash(uv + time) - 0.5) * 0.05; // grain\n  gl_FragColor = vec4(c, 1.0);",
        "Post-processing is where 'rendered' becomes 'cinematic'. Learn the chain order and the big four (bloom, grade, vignette, grain) \u2014 they cover 90% of looks.",
        ["Too much of everything \u2014 restraint is the skill; each effect at 60% of your first instinct.",
         "Wrong chain order \u2014 grain before bloom looks wrong; learn the canonical order.",
         "No performance budget \u2014 6 fullscreen passes at 4K is heavy; profile on target hardware."],
        "Add vignette + grain to any shader you have. A/B the result \u2014 feel the production value."))
    add("creative-code", "audio-reactive", L("Live Performance Setup", "audio-reactive",
        ["The rig: laptop (performance machine, not dev machine) + audio interface + MIDI controller + projector/output. Redundancy for the critical path: backup laptop with the same set.",
         "Rehearse the failure: what happens if the audio drops? If the projector disconnects? Have a fallback visual (a beautiful idle loop) that runs with zero input.",
         "MIDI mapping: knobs for the 4-6 parameters you will actually touch live. Label them. Practice the set twice \u2014 muscle memory, not menu diving.",
         "Audio routing: separate the performance audio from system sounds (do not let a notification ding through the PA). Dedicated interface, muted system.",
         "Record every set (screen + room): the documentation IS the portfolio. A great set nobody recorded is a rumor."],
        "Pre-show checklist:\n  [ ] Backup laptop synced + tested\n  [ ] Idle-loop fallback verified (kill audio \u2192 still beautiful)\n  [ ] MIDI mapped + labeled, 2 rehearsals done\n  [ ] System sounds muted, notifications off\n  [ ] Recording armed (screen + room camera)\n  [ ] Power: laptop plugged, UPS if the venue is sketchy",
        "Live performance is 20% visuals, 80% reliability. The audience remembers the crash, not the peak \u2014 engineer for no crashes.",
        ["No backup machine \u2014 one kernel panic ends the show.",
         "No fallback visual \u2014 dead input = dead screen; idle loops save shows.",
         "Unrehearsed MIDI \u2014 menu-diving on stage reads as amateur; practice the physical set."],
        "Write the pre-show checklist for a hypothetical 20-minute set. What is your fallback visual?"))
    add("creative-code", "physical-installation", L("Budgeting an Installation", "physical-installation",
        ["Budget categories: hardware (projectors, PCs, sensors), fabrication (mounts, enclosures), venue (power, rigging, insurance), labor (install, tech), contingency (20% minimum).",
         "The 2x rule: installations cost 2x the hardware in labor/logistics. A $5k projector is a $10k line item installed. Budget honestly or bleed later.",
         "Contingency is not optional: 20% for known-unknowns (mount doesn't fit, cable too short), more for outdoor/temporary venues. Spend it or return it \u2014 but budget it.",
         "Maintenance budget: who fixes it in month 3? Include a service retainer or train venue staff with the handover doc. Unmaintained installations die publicly.",
         "Get 3 quotes for big items; buy once for critical path (projector, PC). Cheap critical hardware fails at the worst moment \u2014 the opening."],
        "Sample $25k budget:\n  Hardware: $9k (projector, PC, sensors, cables)\n  Fabrication: $3k (mounts, enclosure)\n  Venue/logistics: $4k (power, rigging, insurance)\n  Labor: $5k (install 3 days + tech)\n  Contingency (20%): $4k\n  Total: $25k. Every line justified; nothing hidden.",
        "Budgeting is design: the numbers force decisions about scope before the venue does. Write the budget before the proposal \u2014 it keeps promises honest.",
        ["No contingency \u2014 the first surprise comes from your fee.",
         "Hardware-only budgeting \u2014 labor and logistics are half the cost; budget them.",
         "No maintenance plan \u2014 the piece dies slowly in public; budget the afterlife."],
        "Budget a hypothetical small installation (one projector, one PC). Use the categories above. What is the total?"))
    # ---- cybernetics new domains (2 more each to reach 3)
    add("cybernetics", "origins", L("The Macy Conferences", "origins",
        ["Ten conferences (1946-53), one radical idea: gather mathematicians, anthropologists, psychiatrists, and engineers to find common patterns. Interdisciplinarity as method, not decoration.",
         "Key figures: Wiener (feedback), von Neumann (computation), Bateson (anthropology/schismogenesis), Mead (anthropology), McCulloch (neural nets). Each brought a field; all left with a shared vocabulary.",
         "The product was language: feedback, information, control, system, purpose \u2014 words that now feel obvious were forged in those rooms. Concepts are infrastructure.",
         "The format mattered: small, recurring, discussion-driven (not paper presentations). The Macy format is itself a cybernetic insight \u2014 feedback-rich interaction produces ideas.",
         "Legacy: systems science, cognitive science, family therapy, and AI all trace roots here. When fields cross-pollinate deliberately, new fields are born."],
        "Bateson's schismogenesis:\n  Symmetrical (competition escalates: arms races)\n  Complementary (dominance/submission stabilizes: ritual)\n  The PATTERN across anthropology and arms control \u2014\n  that cross-domain pattern-finding was the Macy method.",
        "The Macy lesson: breakthrough ideas come from sustained cross-disciplinary conversation, not from reading within your field. Build your own Macy \u2014 a diverse reading group, a strange conference.",
        ["Reading cybernetics as single-author \u2014 it was a conversation; the interplay matters.",
         "Missing the method \u2014 the interdisciplinarity WAS the discovery engine.",
         "Dates without ideas \u2014 the conferences matter for what they produced, not when."],
        "List 3 fields distant from yours. What pattern might they share with your field? (The Macy question.)"))
    add("cybernetics", "origins", L("Cybernetics vs Systems Theory vs Complexity", "origins",
        ["Cybernetics: control and communication in systems \u2014 the feedback loop as the atom. Question: how do systems steer toward goals?",
         "General Systems Theory (von Bertalanffy): principles true across system types \u2014 open systems, equifinality, hierarchy. Question: what do all systems share?",
         "Complexity science: emergence, adaptation, self-organization in nonlinear systems. Question: how does novel order arise without central control?",
         "Overlaps and tensions: cybernetics emphasizes purpose and control; complexity emphasizes emergence beyond control. Both true \u2014 different lenses for different phenomena.",
         "The exam move: when asked to compare, anchor on the QUESTION each asks and the ATOM each studies (loop / system / emergence). Frameworks are tools; match tool to problem."],
        "Same traffic jam, three lenses:\n  Cybernetics: signal timing as feedback control (sense congestion \u2192 adjust)\n  GST: traffic as an open system (inflows, outflows, hierarchy)\n  Complexity: jam as emergence (no one planned it; interactions produced it)\n  All true. The lens chooses the intervention.",
        "Don't pledge allegiance to a school \u2014 collect lenses. The thinker with three frameworks sees what the monoglot misses.",
        ["Conflating the schools \u2014 they ask different questions; respect the differences.",
         "One-lens analysis \u2014 the traffic jam needs all three; so do most real systems.",
         "History as trivia \u2014 the distinctions matter because they suggest different actions."],
        "Take a system you know. Analyze it through all three lenses in 3 paragraphs. Which lens was most useful? Why?"))
    add("cybernetics", "feedback-systems", L("Positive Feedback and Runaway", "feedback-systems",
        ["Positive feedback amplifies: microphone squeal, nuclear chain reactions, viral content, bank runs, climate albedo loss. Same structure as negative feedback, opposite sign \u2014 opposite fate.",
         "Runaway needs a limit to be interesting: exponential growth until a constraint (resource exhaustion, intervention, saturation). The S-curve is positive feedback meeting a limit.",
         "In social systems, positive feedback is often invisible until the crash: housing bubbles (prices\u2192speculation\u2192prices), hype cycles, arms races. The loop feels like success while it builds.",
         "Breaking runaway: introduce negative feedback (circuit breakers, cooling, regulation) or remove the gain (transaction taxes, rate limits). Every stabilizer is a designed negative loop.",
         "The diagnostic question: 'what makes this grow, and what stops it?' If nothing stops it, you have found a future crisis \u2014 or an opportunity, if you ride it deliberately."],
        "Bank run anatomy:\n  rumor \u2192 withdrawals \u2192 visible queues \u2192 more fear \u2192 more withdrawals\n  Positive feedback: each withdrawal AMPLIFIES the cause.\n  Breakers: deposit insurance (trust), withdrawal limits (friction),\n    central bank backstop (circuit breaker). All designed negative feedback.",
        "Learn to spot positive feedback early: it feels like momentum, and momentum is wonderful \u2014 until the limit arrives. Ask 'what stops this?' relentlessly.",
        ["Assuming growth continues \u2014 every positive loop meets a limit; plan for the S-curve.",
         "Missing social positive feedback \u2014 bubbles, panics, virality are all runaway loops.",
         "No breakers designed \u2014 if you benefit from a positive loop, design its stabilizers too."],
        "Identify one positive feedback loop in your world (work, markets, habits). Name its limit and one breaker."))
    add("cybernetics", "feedback-systems", L("Control Theory Math (Gentle)", "feedback-systems",
        ["The basic equation: u = Kp\u00b7e + Ki\u00b7\u222be + Kd\u00b7de/dt (PID). Proportional reacts to now, integral fixes accumulated past error, derivative anticipates the future. Three terms, enormous power.",
         "P alone: fast but overshoots and leaves steady-state error. I alone: slow, winds up. D alone: useless (reacts only to change). Together, tuned: the workhorse of industry.",
         "Tuning intuition: increase Kp until oscillation, then back off; add Ki to kill residual error (watch windup); add Kd to dampen. Ziegler-Nichols formalizes this; intuition starts it.",
         "Stability in one idea: the loop is stable if corrections shrink errors faster than delays grow them. Gain \u00d7 delay is the danger product \u2014 keep it small.",
         "You don't need to solve differential equations to use this: the PID vocabulary (gain, integral windup, derivative kick) already upgrades your feedback thinking."],
        "Cruise control:\n  P: hill slows car \u2192 throttle up proportionally (overshoots target speed)\n  I: persistent 2mph low \u2192 integrates error \u2192 adds throttle until exact\n  D: speed dropping fast \u2192 extra throttle NOW (anticipation)\n  Together: locks onto speed smoothly. Apart: oscillates or lags.",
        "PID is the most deployed algorithm in history (refineries, drones, thermostats). Knowing its three terms \u2014 and what each fixes \u2014 is practical cybernetics.",
        ["Cranking Kp for speed \u2014 oscillation; the most common tuning error.",
         "Integral windup ignored \u2014 saturated actuators + integrating error = massive overshoot; use anti-windup.",
         "Math fear \u2014 the intuition (P=now, I=past, D=future) carries 80% of the value."],
        "For a system you know (shower, thermostat, project): which PID term dominates? What would you tune?"))
    add("cybernetics", "information", L("Coding Theory Basics", "information",
        ["The problem: send messages reliably over unreliable channels. The solution: add redundancy strategically \u2014 error detection (know it's wrong) and correction (fix it).",
         "Parity: one extra bit makes the total even \u2014 detects single-bit errors. Hamming codes: clever parity placement CORRECTS single-bit errors. The math is beautiful; the idea is simple.",
         "Shannon's noisy-channel theorem: below capacity, arbitrarily reliable communication is possible with the right codes. Turbo codes and LDPC approach the limit \u2014 theory became modems.",
         "Checksums vs CRCs vs hashes: checksums catch accidents, CRCs catch burst errors (networking), cryptographic hashes catch adversaries. Match the tool to the threat.",
         "The cybernetic view: coding is feedback made mathematical \u2014 the receiver's knowledge of the code IS the error-correcting loop. Redundancy is control information."],
        "Hamming(7,4): 4 data bits + 3 parity bits = 7 transmitted.\n  Parity covers overlapping subsets; the syndrome (which checks fail)\n  points EXACTLY at the flipped bit. Single error \u2192 located \u2192 fixed.\n  3 extra bits buy correction. That ratio is the magic.",
        "Every reliable digital system \u2014 from deep-space probes to your SSD \u2014 runs on these ideas. Coding theory is Shannon's gift to engineering.",
        ["Parity for correction \u2014 parity DETECTS; Hamming CORRECTS. Know which you need.",
         "Checksums against adversaries \u2014 CRCs don't stop attackers; use cryptographic hashes.",
         "Ignoring the capacity limit \u2014 Shannon bounds what's possible; respect it."],
        "Compute the even parity bit for 1011. Then flip one bit \u2014 does parity catch it? (Yes.) What about two flips? (No \u2014 the limit.)"))
    add("cybernetics", "information", L("Entropy in Practice", "information",
        ["Entropy measures uncertainty AND information: H = -\u03a3 p\u00b7log\u2082p. Maximum when outcomes are equiprobable; zero when certain. One formula, two readings.",
         "Compression = entropy removal: ZIP finds the redundancy (predictability) and removes it. The compressed size approximates the true entropy \u2014 compression ratios MEASURE information.",
         "Password strength done right: entropy of the GENERATION process, not the string. 'Tr0ub4dor&3' looks complex but a pattern-based attacker guesses it; 4 random words have more real entropy.",
         "In ML: cross-entropy loss measures prediction surprise; decision trees split on information gain (entropy reduction). The same H runs the algorithms.",
         "Negentropy (Wiener): living systems maintain order by processing information \u2014 exporting entropy to stay organized. Life as anti-entropic information work."],
        "Password comparison:\n  'Tr0ub4dor&3' (human-mangled): ~28 bits (pattern-guessable)\n  'correct horse battery staple' (4 random words): ~44 bits\n  The 'complex' one is WEAKER. Entropy measures the process, not the appearance.",
        "Whenever you see 'information', ask 'how many bits?' \u2014 quantifying turns metaphor into engineering. Compression, passwords, and learning all run on H.",
        ["Judging entropy by appearance \u2014 the process generates the entropy, not the look.",
         "Confusing thermodynamic and Shannon entropy \u2014 related but distinct; don't mix the math.",
         "Ignoring base rates \u2014 surprising to WHOM? Entropy is always relative to a model."],
        "Estimate the entropy of your password generation method (honestly). Is it above 40 bits? If not, switch methods."))
    add("cybernetics", "second-order", L("Ethics of Observation", "second-order",
        ["Every measurement intervenes: the act of observing changes the observed (Hawthorne), categorizing creates the categories (looping kinds, Hacking), and publishing metrics reshapes behavior (Goodhart).",
         "Von Foerster's imperative \u2014 'act always so as to increase the number of choices' \u2014 is an ethics FOR observers: design observations that expand agency rather than constrain it.",
         "Surveillance vs sousveillance: who watches whom is a power question. Second-order cybernetics asks not just 'is the model accurate' but 'who does this modeling serve?'",
         "Informed observation: disclose what you measure and why; give the observed access to their data; design opt-outs. Ethics is part of the system design, not an afterthought.",
         "The researcher's duty: anticipate the performative effects of your categories. A 'risk score' doesn't just predict \u2014 it allocates, stigmatizes, and self-fulfills."],
        "Credit scoring:\n  First-order: 'the model predicts default accurately.'\n  Second-order: the score DECIDES who gets credit \u2014\n    shaping the very outcomes it predicts (denied credit \u2192 harder life \u2192 default).\n  The observer (lender + model) is inside the system. Ethics starts here.",
        "Second-order ethics: before deploying any observation system, ask 'what does this measurement DO to the measured?' \u2014 and design for expanding, not narrowing, their choices.",
        ["Accuracy as ethical cover \u2014 'but it predicts well' doesn't answer what it does.",
         "Ignoring performativity \u2014 scores and metrics reshape reality; account for it.",
         "Ethics as afterthought \u2014 embed it in the design, not the press release."],
        "Pick a scoring/ranking system affecting you. Write what it DOES (not just predicts) in 5 sentences."))
    add("cybernetics", "second-order", L("Autopoiesis Explained", "second-order",
        ["Definition: a network of processes that produces the components which produce the network. A cell makes proteins that maintain the cell that makes proteins \u2014 operational closure.",
         "Closure, not isolation: autopoietic systems are OPEN to matter/energy but CLOSED in organization \u2014 the relations that define them are self-produced. Cells eat; the eating serves self-production.",
         "Allopoiesis (contrast): systems producing something OTHER than themselves \u2014 factories make cars, not factories. The distinction clarifies what 'living organization' means.",
         "Social autopoiesis (Luhmann, controversial): communication producing communication \u2014 legal systems, science, organizations as self-reproducing communication networks. Powerful lens; debated application.",
         "The test: does the system maintain its organization through its own operations? A thermostat: no (designed externally). A cell: yes. A company: partially \u2014 and the partiality is interesting."],
        "Is a university autopoietic?\n  Produces: graduates, papers, new faculty (who produce more...)\n  Organization: self-maintaining across generations\n  Matter/energy: open (students in, funding in)\n  Verdict: arguably yes at the institutional level \u2014\n    and the argument itself sharpens the concept.",
        "Autopoiesis gives 'self-organization' teeth: not vague emergence, but the specific closure of self-production. Apply the test strictly \u2014 the borderline cases teach the most.",
        ["Calling everything self-organizing 'autopoietic' \u2014 the term has a technical meaning; respect it.",
         "Ignoring the openness \u2014 closure is organizational, not material; cells still eat.",
         "Skipping the test \u2014 'does it produce its own producers?' decides; argue from there."],
        "Apply the autopoiesis test to three systems (cell, corporation, ecosystem). Where does each pass or fail? Why?"))
    add("cybernetics", "modern-systems", L("The Viable System Model", "modern-systems",
        ["Beer's VSM: five systems every viable organization needs \u2014 S1 operations, S2 coordination, S3 control, S4 intelligence (future), S5 policy (identity). Missing one = pathology.",
         "S1: the doing units (divisions, teams) \u2014 each itself viable (recursion: the model nests). S2: anti-oscillation coordination (schedules, standards) \u2014 damps the thrashing between S1s.",
         "S3: the inside-and-now \u2014 resource allocation, performance management. S3* (audit): the sporadic check that keeps S3 honest. S4: the outside-and-then \u2014 R&D, strategy, environment scanning.",
         "S5: identity and ethos \u2014 'who are we, what are we for?' The system that balances S3 (now) vs S4 (future). Organizations that lose S5 drift.",
         "Diagnostic use: map any organization; find the missing/weak system; predict the pathology. Weak S4 \u2192 blindsided by change. Weak S2 \u2192 internal thrashing. It works disturbingly often."],
        "Startup post-mortem via VSM:\n  S1: strong (great engineers shipping)\n  S2: missing (teams thrash, duplicate work)\n  S3: weak (no resource discipline)\n  S4: absent (no market scanning \u2014 blindsided)\n  S5: confused ('are we B2B or B2C?')\n  Diagnosis: died of missing S2/S4/S5, not bad S1.",
        "VSM is an organizational MRI: five systems, scan for absence. Run it on any struggling org and the missing piece usually explains the symptoms.",
        ["Treating it as an org chart \u2014 it's about FUNCTIONS, not boxes; small teams still need all five.",
         "Skipping recursion \u2014 each S1 must itself be viable; the model nests.",
         "Using it to justify bureaucracy \u2014 the systems are minimal functions, not departments."],
        "Map an organization you know to the five systems. Which is weakest? What pathology does that predict?"))
    add("cybernetics", "modern-systems", L("Complexity and Emergence", "modern-systems",
        ["Emergence: system-level properties not present in parts \u2014 wetness isn't in H2O molecules; traffic jams aren't in cars. The interactions create what components lack.",
         "Weak vs strong emergence: weak = surprising but derivable (traffic flow); strong = allegedly irreducible (consciousness \u2014 debated). Most practical cases are weak emergence \u2014 modelable with the right lens.",
         "Self-organization: order without a controller \u2014 bird flocks (3 local rules), markets, ant colonies. No architect; the pattern emerges from interaction rules.",
         "Edge of chaos: complex adaptive systems thrive between rigid order and pure randomness \u2014 enough structure to persist, enough flexibility to adapt. Manage there, not at either extreme.",
         "Cybernetic bridge: emergence doesn't replace feedback thinking \u2014 feedback LOOPS are often the mechanism of emergence. The flock's 3 rules ARE feedback loops."],
        "Flocking (Reynolds' boids):\n  1. Separation: don't crowd neighbors\n  2. Alignment: match average heading\n  3. Cohesion: move toward average position\n  No leader, no map \u2014 yet flocks wheel and flow.\n  Emergence from 3 local feedback rules.",
        "When facing a complex system, look for the local rules generating the global pattern. Intervene at the rules, not the pattern \u2014 the pattern is the output.",
        ["Mystifying emergence \u2014 'emergent' is not magic; it's interaction + feedback. Find the mechanism.",
         "Central-planning a self-organizing system \u2014 work with the local rules, not against them.",
         "Ignoring the edge \u2014 over-control kills adaptation; under-control invites chaos."],
        "Name an emergent phenomenon you observe regularly. What are the local rules? What would change the pattern?"))
    add("cybernetics", "exam-strategy", L("Essay Writing for Systems Topics", "exam-strategy",
        ["Thesis first: one arguable sentence ('Feedback explains more of organizational behavior than incentives do'). Everything serves it \u2014 no thesis, no essay.",
         "The dialectic structure: claim \u2192 strongest counter \u2192 synthesis. Examiners reward the counter-argument handled honestly \u2014 it proves understanding, not just position.",
         "One concept per paragraph, each with: definition, example, and SO WHAT (why it matters to the thesis). Definition without application is decoration.",
         "Conclude by extending: 'this suggests...' \u2014 the essay should open a door, not just close a case. The best conclusions pose the next question.",
         "Time discipline: 10% planning (thesis + 3 points), 80% writing, 10% reviewing (thesis present? terms defined? counter handled?). Plan or ramble."],
        "Thesis: 'Negative feedback, not leadership, stabilizes organizations.'\n  P1: feedback defined + thermostat example\n  P2: organizational homeostasis (budgets, norms as comparators)\n  P3: counter \u2014 leadership sets the SET POINTS (synthesis!)\n  Conclusion: leaders design loops; loops do the stabilizing.",
        "Systems essays are won in the planning 10%: thesis + structure before prose. Write the skeleton first, always.",
        ["No thesis \u2014 summary is not argument; take a position.",
         "Ignoring the counter \u2014 the unhandled objection is the examiner's objection.",
         "Jargon without definition \u2014 'autopoietic' undefined is noise; defined once, it's precision."],
        "Write a thesis sentence for 'Do markets exhibit homeostasis?' Then the 3-point skeleton. (5 min.)"))
    add("cybernetics", "exam-strategy", L("Using Primary Sources", "exam-strategy",
        ["Read Wiener, Ashby, von Foerster in excerpts \u2014 not summaries of summaries. One page of Wiener teaches more than ten pages about Wiener. Primary sources carry the reasoning, not just conclusions.",
         "How to read: first pass for the argument (what's the claim?), second for the mechanism (how does it work?), third for the limits (where does it break?). Three passes, increasing depth.",
         "Quote sparingly, cite precisely: one exact quote used well beats five dropped names. 'As Wiener put it...' followed by YOUR explanation of why it matters here.",
         "Connect across sources: 'Ashby's law of requisite variety generalizes Wiener's feedback \u2014 control needs as much variety as disturbance.' The connections ARE the understanding.",
         "The exam rewards source-grounded argument: 'von Foerster would object that...' shows you inhabit the ideas, not just list them."],
        "Reading Wiener (1948) p.1:\n  Pass 1: claim \u2014 control/communication unified across animal/machine.\n  Pass 2: mechanism \u2014 feedback loops as the shared structure.\n  Pass 3: limits \u2014 1948 computing; the ideas outgrew the examples.\n  One page, three depths. That is primary-source study.",
        "Summaries give you conclusions; sources give you reasoning. Exams test reasoning \u2014 go to the source, even in excerpts.",
        ["Summary-only studying \u2014 you inherit conclusions without the reasoning that earns marks.",
         "Quote-dropping \u2014 names without mechanism signal shallow reading.",
         "One-pass reading \u2014 the third pass (limits) is where critical thought lives."],
        "Pick one primary excerpt (any field). Do the three passes; write one paragraph per pass."))
    # ---- data-analyst
    add("data-analyst", "interview-prep", L("Salary Negotiation for Analysts", "interview-prep",
        ["Research first: levels.fyi, Glassdoor, and 3 peer conversations give you the band. Never negotiate blind \u2014 data is leverage.",
         "The first number anchors: let them name it, or give a researched range (top of range = your target). 'Based on my research, $X\u2013$Y is the band for this impact level.'",
         "Negotiate the package, not just salary: signing bonus, review timeline (6-month raise clause), remote flexibility, learning budget. Total comp has more levers than base.",
         "Use competing offers honestly: 'I have an offer at $X; I prefer you at $Y.' Never fabricate \u2014 the world is small and lies surface.",
         "Get it in writing before signing: verbal promises evaporate. The offer letter IS the agreement; everything else is conversation."],
        "Script: 'I'm excited about this role. Based on the scope \u2014 owning the experimentation program \u2014 and market data, I'm looking at $X\u2013$Y base. Is there flexibility to meet there?'\n  Then SILENCE. Let them respond. The pause is the negotiation.",
        "Negotiation is a professional skill, not a personality trait. Script it, practice it, and remember: the worst they say is no, and you still have the offer.",
        ["Accepting the first offer \u2014 the first number is the floor, not the ceiling.",
         "Negotiating without data \u2014 'I want more' loses to 'the band is $X\u2013$Y'.",
         "Verbal-only agreements \u2014 if it's not in the letter, it doesn't exist."],
        "Research your target band now: 3 data points minimum. Write your range and your script."))
    add("data-analyst", "excel-power", L("Power Pivot and the Data Model", "excel-power",
        ["Power Pivot = real data modeling in Excel: import multiple tables, define relationships, write DAX measures. It turns Excel into a BI tool.",
         "Relationships replace VLOOKUPs: link tables on keys once; pivot across them freely. The model IS the join logic \u2014 defined once, used everywhere.",
         "DAX measures (see BI lesson) compute in filter context: [Total Revenue] responds to slicers automatically. Write once, slice infinitely.",
         "Star schema applies: fact tables (transactions) + dimension tables (products, dates). Model well and the pivots practically write themselves.",
         "When to graduate: Power Pivot handles millions of rows; beyond that (or for scheduled refresh + sharing), move to Power BI. Know the handoff point."],
        "Sales model:\n  Tables: Orders (fact), Products (dim), Calendar (dim)\n  Relationships: Orders[ProductID] \u2192 Products[ID], Orders[Date] \u2192 Calendar[Date]\n  Measure: Revenue YTD = TOTALYTD(SUM(Orders[Amount]), Calendar[Date])\n  Pivot: drag, slice, done \u2014 no formulas per cell.",
        "Power Pivot is the bridge from spreadsheet analyst to BI professional. Learn the model; the tool follows.",
        ["Flattened mega-tables \u2014 defeats the model; normalize into facts and dimensions.",
         "Calculated columns for everything \u2014 measures compute dynamically; columns bloat.",
         "No relationships defined \u2014 then it's just separate tables; the model needs the links."],
        "Sketch a 3-table data model for data you work with. Define the relationships and one measure."))
    add("data-analyst", "ab-testing", L("Bayesian A/B Testing Intro", "ab-testing",
        ["Frequentist asks 'is it significant?'; Bayesian asks 'what's the probability B beats A?' \u2014 the business question, directly answered. P(B>A | data) is the deliverable.",
         "Priors matter but wash out: start with uninformative priors (Beta(1,1)); with enough data, the data dominates. Document the prior \u2014 transparency, not trickery.",
         "The output is a distribution, not a verdict: 'B beats A by 1-3% with 92% probability.' Decisions use expected loss: ship if P(loss) is acceptably small.",
         "Peeking is less sinful (but not innocent): Bayesian updating is coherent under optional stopping, but the decision rule still needs pre-commitment to avoid bias.",
         "Tools: simple Beta-Binomial for conversion rates (conjugate, closed-form); MCMC (PyMC) for complex models. Start simple \u2014 most tests need only Beta-Binomial."],
        "Beta-Binomial:\n  Prior: Beta(1,1) for both variants\n  Data: A: 120/1000, B: 150/1000\n  Posterior: A ~ Beta(121, 881), B ~ Beta(151, 851)\n  P(B>A) = 0.93 via sampling. Expected loss of shipping B: tiny.\n  Decision: ship B. The probability IS the justification.",
        "Bayesian testing answers the question stakeholders actually ask. Learn Beta-Binomial deeply; it covers 80% of conversion tests.",
        ["Priors as weapons \u2014 strong priors need justification; default to weak and let data speak.",
         "Ignoring the loss function \u2014 probability without cost is half a decision; add expected loss.",
         "MCMC for simple problems \u2014 conjugate models are exact and instant; save MCMC for hierarchies."],
        "Compute P(B>A) for the example above via simulation (10k draws). Verify ~0.93."))
    add("data-analyst", "data-quality", L("Building a Data Quality Dashboard", "data-quality",
        ["The DQ dashboard monitors: freshness (is data late?), volume (row counts vs expected), validity (null rates, range violations), and consistency (cross-source reconciliation). Four panels, full coverage.",
         "Thresholds with history: alert when today's metric deviates from the 30-day baseline \u2014 not on fixed magic numbers. Baselines adapt; fixed thresholds rot.",
         "Each alert links to the runbook: 'null rate spike \u2192 check upstream job X, contact Y'. Alerts without runbooks are anxiety; with runbooks, they're routine.",
         "Trend the metrics: null-rate over time, freshness drift, reconciliation gaps. Trends show decay before incidents \u2014 the dashboard is early warning, not autopsy.",
         "Review cadence: weekly 15-minute DQ review with pipeline owners. The dashboard drives the conversation; ownership drives the fixes."],
        "DQ dashboard panels:\n  1. Freshness: max(event_time) vs now \u2014 per pipeline\n  2. Volume: today's rows vs 30-day band\n  3. Validity: null %, range violations \u2014 top 5 tables\n  4. Reconciliation: BI total vs source total \u2014 the trust number\n  Alert: any panel red \u2192 runbook link attached.",
        "A DQ dashboard turns data quality from complaints into operations. Build it for your top 5 tables first \u2014 expand from proven value.",
        ["Alerting without runbooks \u2014 every alert must link to the fix procedure.",
         "Fixed thresholds \u2014 baselines adapt; magic numbers don't.",
         "Dashboard nobody reviews \u2014 the weekly 15-minute review is the actual control."],
        "Sketch the 4-panel DQ dashboard for your data. What are today's values? Any red?"))
    # ---- data-engineering
    add("data-engineering", "interview-prep", L("Behavioral Rounds for Data Engineers", "interview-prep",
        ["DE behavioral themes: a pipeline that broke at 3 AM (ownership), a disagreement on architecture (influence), a data quality incident (rigor), mentoring a junior (leadership). Prepare one story each.",
         "STAR with technical depth: the 'Action' should include the actual technical decision ('chose idempotent upserts over append because...'). Shallow actions read as shallow experience.",
         "The 'tell me about a failure' question is a gift: pick a real incident, own your part, show the systemic fix (monitoring, runbook, test). Growth narratives beat perfection.",
         "Questions to ask them: 'how do you handle backfills?', 'what's the on-call burden?', 'how is data quality owned?' \u2014 the answers reveal the team's maturity. Ask like an owner.",
         "Salary bands for DE are wide: know the band for the level (levels.fyi, peers). The technical screen passed = leverage; negotiate the package, not just base."],
        "STAR: 3 AM page, revenue pipeline down.\n  S: 'PagerDuty 3 AM: daily mart failed, execs need numbers by 8.'\n  T: 'Restore by 7 AM without corrupting downstream.'\n  A: 'Found the schema change, applied the versioned fix, reran idempotently, verified reconciliation.'\n  R: 'Green by 6:15; added contract test + alert \u2014 same failure impossible now.'",
        "Behavioral rounds test judgment under pressure \u2014 exactly what on-call data engineering is. Your incident stories ARE your qualifications; prepare them like code.",
        ["No failure story \u2014 'nothing ever broke' reads as inexperienced or dishonest.",
         "Shallow technical actions \u2014 'I fixed it' without the HOW wastes the question.",
         "No questions for them \u2014 the on-call and backfill questions reveal team quality; ask them."],
        "Write your 3 AM incident story in STAR now. Include the technical decision and the systemic fix."))
    add("data-engineering", "spark-fundamentals", L("Spark SQL Deep Dive", "spark-fundamentals",
        ["Spark SQL is the primary API now: DataFrames are distributed tables, Catalyst optimizes the plan, Tungsten executes it fast. SQL fluency IS Spark fluency for most work.",
         "Catalyst in 30 seconds: parse \u2192 analyze (resolve columns) \u2192 optimize (predicate pushdown, projection pruning, join reordering) \u2192 physical plan \u2192 codegen. EXPLAIN shows the journey.",
         "Read EXPLAIN: look for Exchange (shuffles \u2014 minimize), BroadcastHashJoin (good for small tables), SortMergeJoin (default for big-big), and Filter pushdown (predicates near the scan = good).",
         "AQE (Adaptive Query Execution): runtime re-optimization \u2014 coalesces shuffle partitions, switches join strategies mid-flight. Enable it; it fixes the plan your static analysis got wrong.",
         "UDFs: the optimization killer \u2014 Catalyst can't see inside Python UDFs. Prefer Spark SQL functions; use pandas_udf (vectorized) when you must; avoid row-wise Python UDFs in hot paths."],
        "Slow query: 10-min join.\n  EXPLAIN: SortMergeJoin with 2TB shuffle on skewed key.\n  Fix 1: AQE on \u2192 auto-coalesces to sane partitions.\n  Fix 2: salt the skewed key (or broadcast if small side).\n  Fix 3: replace Python UDF filter with native functions.\n  Result: 10 min \u2192 90 sec. The plan told the story.",
        "EXPLAIN is the Spark developer's X-ray: learn to read the plan and the optimizer becomes your collaborator instead of your mystery.",
        ["Python UDFs in hot paths \u2014 Catalyst goes blind; prefer native functions.",
         "Ignoring the plan \u2014 'it's slow' without EXPLAIN is guessing; the plan names the shuffle.",
         "AQE disabled \u2014 free runtime optimization; enable it by default."],
        "Run EXPLAIN on a join you have. Find the Exchange nodes. Can any be eliminated?"))
    add("data-engineering", "cdc-streaming-deep", L("Schema Registry Patterns", "cdc-streaming-deep",
        ["The registry is the contract enforcer: producers register schemas; compatibility checks (BACKWARD, FORWARD, FULL) run on every change. Breaking changes fail before deploy.",
         "Compatibility modes: BACKWARD (new readers read old data \u2014 most common), FORWARD (old readers read new data), FULL (both). Choose per consumer reality, not ideology.",
         "Subject naming strategies: TopicNameStrategy (one schema per topic \u2014 simple) vs RecordNameStrategy (many event types per topic \u2014 flexible). The strategy shapes evolution freedom.",
         "Wire format: schema ID embedded in each message (magic byte + ID). Consumers fetch the schema once, cache it. The ID is the version handshake \u2014 compact and robust.",
         "Governance: who approves breaking changes? The registry needs a process owner and a deprecation playbook \u2014 otherwise it's a speed bump everyone drives around."],
        "Breaking change flow:\n  Producer PR: renames field \u2192 registry check: BACKWARD violated\n  \u2192 build fails \u2192 producer adds new field (nullable) instead\n  \u2192 consumers migrate \u2192 old field deprecated (announced)\n  \u2192 removed in v3. Zero incidents. The registry earned its keep.",
        "Schema registries turn 'hope the consumers handle it' into enforced contracts. The CI check is the cheapest incident prevention in streaming.",
        ["No registry \u2014 'we'll coordinate' fails at 3+ teams; the registry scales the coordination.",
         "Wrong compatibility mode \u2014 BACKWARD when consumers need FORWARD; match reality.",
         "No deprecation process \u2014 fields accumulate forever; version and retire deliberately."],
        "Check: does your streaming setup have a registry? If not, write the 3-line proposal for adopting one."))
    add("data-engineering", "cost-performance", L("FinOps for Data Teams", "cost-performance",
        ["Showback first: tag every job/pipeline with owner and project; publish the cost dashboard. Visibility alone cuts 15-20% \u2014 nobody optimizes invisible spend.",
         "The big three levers: right-size compute (most clusters are 2x oversized), kill idle (dev clusters nights/weekends), and fix the scan volume (partitioning, aggregation). In that ROI order.",
         "Unit economics: cost per TB processed, per pipeline run, per dashboard refresh. 'Our pipeline costs $0.42/TB' enables real trade-off conversations with the business.",
         "Commitments for the stable base: savings plans / reserved capacity for the 24/7 baseline (30-50% off). Keep on-demand for spikes \u2014 the hybrid is the optimum.",
         "Chargeback (with teeth) vs showback (visibility): start with showback; graduate to chargeback when the culture is ready. The goal is efficient engineering, not accounting theater."],
        "Monthly FinOps review:\n  Total: $48k (\u25b23k vs last month \u2014 why?)\n  Top mover: pipeline X +$5k (backfill ran 3x \u2014 one-time, acknowledged)\n  Win: dev cluster auto-pause saved $2k\n  Action: pipeline Y's scan volume doubled \u2014 owner investigating.\n  30 minutes, full accountability.",
        "FinOps is engineering accountability for money: tag, measure, review, optimize. The monthly review is the control \u2014 skip it and costs drift.",
        ["No tagging \u2014 the bill is a lump; nobody owns anything.",
         "Optimizing before measuring \u2014 the top-3 spend list directs effort; start there.",
         "One-time cleanup, no process \u2014 costs regrow; the monthly review is the maintenance."],
        "List your top 5 cost drivers (or estimate). What is the single highest-ROI optimization?"))
    # ---- daml
    add("data-analyst-to-ml", "ml-foundations", L("The Math You Actually Need", "ml-foundations",
        ["Linear algebra: vectors, matrices, dot products \u2014 the language of ML. You need intuition (what does Wx+b DO geometrically?), not proofs.",
         "Calculus: gradients as 'which direction reduces error?' The chain rule is backprop's engine \u2014 understand the idea, let autograd do the arithmetic.",
         "Probability: Bayes' rule (updating beliefs with evidence), distributions (what shape is my data?), expected value (decisions under uncertainty).",
         "Statistics: hypothesis testing, confidence intervals, the bias-variance tradeoff \u2014 the same stats from analysis, now applied to models.",
         "Learn math THROUGH code: implement gradient descent in 20 lines, derive Bayes on a real problem. Math without implementation evaporates."],
        "Gradient descent in words:\n  Error surface: hilly terrain. Position: current weights.\n  Gradient: the slope under your feet.\n  Step: walk downhill (against the gradient), small steps.\n  Learning rate: step size \u2014 too big, bounce over the valley; too small, never arrive.",
        "You need working intuition, not theorem-proving ability. Implement each concept once \u2014 the code makes the math concrete.",
        ["Math-first, code-never \u2014 derivations without implementation don't transfer.",
         "Skipping probability \u2014 Bayes and distributions underpin everything in ML.",
         "Perfectionism \u2014 'I must master linear algebra first' delays building by months; learn alongside."],
        "Implement gradient descent for y=mx+b on 10 points (20 lines). Watch it converge."))
    add("data-analyst-to-ml", "feature-engineering", L("Feature Stores", "feature-engineering",
        ["The problem feature stores solve: training-serving skew (different code paths compute different values) and duplicated feature logic across teams. One store, one definition.",
         "Architecture: offline store (historical, for training \u2014 point-in-time correct) + online store (low-latency, for serving). Same definitions, two serving paths.",
         "Point-in-time correctness is the killer feature: training rows get feature values AS OF the event time \u2014 no leakage by construction. The store enforces what discipline often misses.",
         "Start simple: a versioned feature table + shared transformation code is a 'feature store' for most teams. Buy/build the platform when 3+ teams duplicate features.",
         "Document like an API: each feature gets definition, owner, refresh cadence, and known caveats. Undocumented features are tech debt with a fancy name."],
        "Without store: team A and B both compute 'days_since_last_order' \u2014 differently. Models disagree mysteriously.\n  With store: one definition, versioned. Training uses offline (point-in-time); serving uses online (fresh).\n  Same number everywhere. The mystery vanishes.",
        "Feature stores are DRY for ML features: define once, serve consistently. Start with shared code + versioning; graduate to platforms when scale demands.",
        ["Building the platform first \u2014 shared code + docs solve 80%; platforms come later.",
         "No point-in-time discipline \u2014 the store's main value; don't lose it in implementation.",
         "Undocumented features \u2014 a feature without docs is a liability, not an asset."],
        "Pick 5 features you use. Write the one-line definition + refresh cadence for each. That's your v0 feature store."))
    add("data-analyst-to-ml", "model-evaluation", L("A/B Testing Models", "model-evaluation",
        ["Offline metrics don't guarantee online wins: a model with better AUC can lose in production (feedback loops, UX interactions, segment effects). Online testing is the truth.",
         "Interleaving for ranking: show users mixed results from A and B, measure preference directly. More sensitive than A/B for rankers \u2014 fewer users needed.",
         "Guardrail metrics: the model must not HURT key metrics while improving its target. Define guardrails upfront (latency, revenue, fairness) \u2014 violations veto the ship.",
         "Shadow mode first: log predictions without acting. Compare offline vs online feature distributions \u2014 skew caught here is cheap; caught live is expensive.",
         "The decision framework: ship if (primary metric improves) AND (no guardrail violated) AND (effect is practical, not just significant). All three, always."],
        "New recommender:\n  Offline: +5% NDCG. Shadow 2 weeks: feature skew found (fixed).\n  A/B: +2% engagement (p<0.05), guardrails green (revenue flat, latency +3ms OK).\n  Decision: ship. The offline win survived contact with reality.",
        "Online evaluation is where ML meets the business: guardrails, practical significance, and the humility to let reality vote. Never ship on offline metrics alone.",
        ["Shipping on offline wins \u2014 production has feedback loops offline can't see.",
         "No guardrails \u2014 the model improves its metric while hurting the business.",
         "Skipping shadow mode \u2014 skew discovered live is an incident; in shadow, it's a ticket."],
        "Design the online test for a model you might build: primary metric, 2 guardrails, shadow duration."))
    add("data-analyst-to-ml", "ml-systems", L("Model Monitoring in Production", "ml-systems",
        ["Monitor three layers: inputs (feature drift, null rates, schema changes), predictions (distribution shift, volume), outcomes (business metrics, feedback labels). All three, always.",
         "Drift detection: PSI/K-S tests comparing recent vs reference distributions. Alert on drift magnitude, not just presence \u2014 some drift is normal (seasonality).",
         "The label problem: ground truth arrives late or never. Use proxies (user actions, downstream metrics) and accept that true performance is estimated \u2014 design for it.",
         "Alert routing: data issues \u2192 data team, model issues \u2192 ML team, business impact \u2192 both + stakeholders. The alert must reach whoever can fix the cause.",
         "Dashboard the model like a service: predictions/min, latency p99, error rate, drift scores, business KPI. The model IS production software \u2014 monitor it as such."],
        "Monitoring stack:\n  Inputs: PSI per top-10 features vs training (alert > 0.2)\n  Predictions: score distribution histogram, refreshed hourly\n  Outcomes: business KPI (conversion) with model-on/off comparison\n  Labels: delayed 7 days \u2014 proxy metric (clicks) fills the gap.\n  On-call: runbook per alert type.",
        "Unmonitored models decay silently: the business metric craters months before anyone looks. Monitoring is how ML stays honest in production.",
        ["Monitoring predictions only \u2014 input drift is the leading indicator; watch it.",
         "No proxy for delayed labels \u2014 flying blind for weeks; design the proxy upfront.",
         "Alerts without runbooks \u2014 the 3 AM page needs a playbook, not a puzzle."],
        "Sketch the 3-layer monitoring for a model you know. What's missing today? That's your next build."))
    # ---- dsc
    add("data-science-certs", "cert-landscape", L("Recertification Strategy", "cert-landscape",
        ["Every cert has a clock: 2-3 year validity typical, with continuing education or re-exam paths. Know YOUR certs' clocks \u2014 lapsed certs are sunk costs.",
         "Continuing education beats re-exams: most programs accept courses, conferences, and contributions. Plan CE across the validity period \u2014 not in the final month.",
         "Stack strategically: some programs let one activity count for multiple certs. A conference talk might satisfy two CE requirements \u2014 know the overlap rules.",
         "The real question at renewal: is this cert still serving my target role? Letting a misaligned cert lapse is smart portfolio management, not failure.",
         "Document everything as you go: CE portal entries, certificates, dates. Reconstruction at deadline time is stressful and error-prone."],
        "Renewal plan:\n  Cert A (expires 2028-06): needs 40 CE \u2192 2 conferences + 1 course, spread over 2 years\n  Cert B (expires 2027-03): re-exam OR 30 CE \u2192 decide by 2026-09\n  Calendar reminders at 12/6/3 months. No surprises.",
        "Treat recertification as portfolio maintenance: scheduled, spread out, and periodically questioned. The calendar reminder is the system.",
        ["Deadline-month panic \u2014 CE cramming is expensive and stressful; spread it.",
         "Renewing misaligned certs \u2014 sunk-cost fallacy; let go of what doesn't serve.",
         "No documentation \u2014 reconstructing 2 years of CE from memory fails."],
        "List your certs with expiry dates and CE requirements. Set the 12/6/3-month reminders now."))
    add("data-science-certs", "exam-strategy", L("Test-Day Protocol: The Final 24 Hours", "exam-strategy",
        ["No new material: review the error log, formula sheet (if allowed), and strategy only. Novelty now creates anxiety.",
         "Logistics: ID, confirmation, testing center route (or system check for online). Arrive 30 min early.",
         "Sleep 8 hours. Statistical reasoning needs a rested brain \u2014 the all-nighter destroys exactly what the exam tests.",
         "During: read scenarios fully before calculating, flag-and-move on stuck items, no blanks. Trust the preparation."],
        "T-24h: [ ] error log reviewed [ ] ID + route [ ] 8h sleep [ ] strategy card",
        "The final day is logistics and rest. The work is done \u2014 execute the plan.",
        ["Cramming formulas.", "All-nighter.", "Skipping the system check (online exams)."],
        "Do 5 mixed practice questions now, timed. That's your exam pace \u2014 trust it."))
    add("data-science-certs", "portfolio-proof", L("Technical Blogging", "portfolio-proof",
        ["Blogging is thinking in public: explaining a concept forces the depth that reading never does. The post IS the study.",
         "Write about what you struggled with: the leakage bug, the confusing metric, the failed approach. Struggle posts get the most engagement \u2014 everyone hits the same walls.",
         "Structure: the problem (1 para), what I tried (with the dead end), what worked (with code), what I learned (the transferable lesson). Honesty over polish.",
         "One post per month beats ten in a weekend: consistency compounds. Twelve posts is a body of work; it shows up in interviews ('I read your post on...').",
         "Cross-post strategically: personal blog (canonical) + Dev.to/Medium (discovery) + LinkedIn (professional signal). Same content, three audiences."],
        "Post skeleton:\n  Title: 'The leakage bug that made my model look brilliant'\n  1. The 0.97 AUC that felt wrong\n  2. The audit that found cancellation_page_visits\n  3. The fix + honest 0.72\n  4. Lesson: point-in-time audits for every temporal feature\n  800 words. One code snippet. Done.",
        "Your blog is your public lab notebook: it proves you think, struggle, and learn in the open. Hiring managers read it as a work sample.",
        ["Tutorial rewrites \u2014 add your struggle and insight, or don't publish.",
         "Perfectionism \u2014 shipped and imperfect beats drafted forever.",
         "No code \u2014 technical posts need the artifact; snippets are the proof."],
        "Outline one post now: the title, the struggle, the lesson. Write the first paragraph today."))
    add("data-science-certs", "statistics-core", L("Bayesian Thinking", "statistics-core",
        ["Bayes' rule: P(H|data) \u221d P(data|H) \u00d7 P(H). Update beliefs with evidence: prior \u00d7 likelihood = posterior. The formal version of 'consider the base rate.'",
         "Base rates dominate: a 99% accurate test for a 0.1% disease gives mostly false positives. The prior (0.1%) overwhelms the likelihood \u2014 always multiply, never eyeball.",
         "Priors are explicit assumptions: document them. 'Uninformative prior' is still a choice \u2014 transparency about assumptions is the Bayesian ethic.",
         "For exams: know when Bayesian answers differ from frequentist (small samples, strong priors, sequential testing) and be able to compute a simple Beta-Binomial update.",
         "The mindset matters more than the math: think in updated beliefs, not binary verdicts. '70% likely' beats 'significant' for decisions."],
        "Disease test: 99% sensitive/specific, 0.1% prevalence.\n  P(sick|positive) = (0.99 \u00d7 0.001) / P(positive) \u2248 9%.\n  99% accurate test, 9% chance you're sick.\n  The base rate is the whole story. Bayes does the arithmetic.",
        "Bayesian thinking is base-rate thinking made rigorous. Before trusting any test result, ask: 'what did we believe before the evidence?'",
        ["Ignoring base rates \u2014 the most expensive probability error, made daily.",
         "Hidden priors \u2014 every analysis has assumptions; Bayesians state them.",
         "Binary thinking \u2014 'significant or not' discards information; posteriors preserve it."],
        "Compute the disease-test posterior above by hand. Feel the base rate's power."))
    return D

def extra_labs_driver():
    """Additional labs to reach 20+ per CBT. Returns {cbt: [labs]}."""
    E = {}
    def add(cbt, lab):
        E.setdefault(cbt, []).append(lab)
    # security-plus needs 4 more (has 16)
    for i, (title, did, obj, steps) in enumerate([
        ("Audit Sudo Usage", "operations", "Find who can sudo and whether it's justified.",
         ["Type exactly: getent group sudo adm 2>/dev/null || getent group wheel",
          "Type exactly: grep -E '^%' /etc/sudoers 2>/dev/null | head -5 || echo 'no sudoers read'",
          "For each sudo-capable group: is membership justified? Document.",
          "State the least-privilege fix for any excess."]),
        ("Check for Listening Services", "architecture", "Enumerate network listeners and judge exposure.",
         ["Type exactly: ss -tlnp 2>/dev/null | head -12",
          "For each listener: expected? (22 yes, 23 no!)",
          "Flag any 0.0.0.0 binding on sensitive ports.",
          "Write the firewall rule you'd add for the riskiest one."]),
        ("Verify File Integrity Baseline", "operations", "Create a hash baseline and detect a change.",
         ["Type exactly: echo data > /tmp/base.txt && sha256sum /tmp/base.txt > /tmp/base.sha && cat /tmp/base.sha",
          "Type exactly: echo tampered > /tmp/base.txt && sha256sum -c /tmp/base.sha || echo 'TAMPER DETECTED'",
          "Explain: how would you scale this? (Answer: AIDE/Tripwire, scheduled.)",
          "Clean up: rm /tmp/base.txt /tmp/base.sha"]),
        ("Password Policy Check", "governance", "Inspect password policy settings.",
         ["Type exactly: grep -E 'PASS_MAX_DAYS|PASS_MIN_LEN' /etc/login.defs 2>/dev/null",
          "Type exactly: cat /etc/security/pwquality.conf 2>/dev/null | grep -v '^#' | grep -v '^$' | head -8 || echo 'no pwquality'",
          "Judge: do the settings meet policy? What's missing?",
          "Write the one-line fix for the weakest setting."]),
    ]):
        add("comptia-security-plus", LB(f"secplus-lab-extra{i+1}", title, did, obj, steps,
            [CHECK(steps[0].split("Type exactly: ")[1][:40], "", f"Run the first command."),
             CHECK(steps[1].split("Type exactly: ")[1][:40] if "Type exactly:" in steps[1] else steps[1][:40], "", "Run the second command.")],
            "Lab complete \u2014 hands-on security auditing. Repeat quarterly."))
    # network-plus needs 5 more (has 15)
    for i, (title, did, obj, steps) in enumerate([
        ("Bandwidth Math", "concepts", "Calculate transfer times and link requirements.",
         ["Type exactly: python3 -c \"size_gb=10; mbps=100; secs=size_gb*8000/mbps; print(f'{size_gb}GB at {mbps}Mbps = {secs/60:.1f} min (theoretical)')\"",
          "Add 20% overhead: re-run with *1.2 \u2014 real-world estimate.",
          "Reverse: what bandwidth moves 50GB in 1 hour? Solve it.",
          "State: why do real transfers always take longer? (Overhead, contention, protocol.)"]),
        ("DNS Deep Check", "operations", "Interrogate DNS like a resolver would.",
         ["Type exactly: dig +short example.com",
          "Type exactly: dig +short -x 93.184.216.34",
          "Type exactly: dig NS example.com +short",
          "Explain the forward/reverse/NS relationship in two sentences."]),
        ("Interface Counters Tell Stories", "net-troubleshoot", "Read interface error counters and diagnose.",
         ["Type exactly: ip -s link show 2>/dev/null | head -20 || ifconfig 2>/dev/null | head -20",
          "Find: RX errors, drops, overruns. Any nonzero?",
          "Correlate: errors + slowness = physical/duplex; drops + normal = congestion.",
          "Write the diagnosis for what you see (or the healthy baseline)."]),
        ("Subnet Overlap Detector", "subnetting-mastery", "Detect overlapping subnets before they break routing.",
         ["Type exactly: python3 -c \"import ipaddress; a=ipaddress.ip_network('10.1.0.0/23'); b=ipaddress.ip_network('10.1.1.0/24'); print('overlap:', a.overlaps(b))\"",
          "Test: 10.1.0.0/23 vs 10.1.2.0/23 (no overlap expected).",
          "Explain: why do overlaps break routing? (Ambiguous longest-match.)",
          "Rule: always overlap-check new allocations against existing."]),
        ("WiFi Channel Plan", "wireless-deep", "Design a non-overlapping 2.4GHz channel plan.",
         ["On paper: 4 APs in a row, 2.4GHz. Assign channels 1/6/11/1 (reuse with distance).",
          "Type exactly: python3 -c \"ch=[1,6,11,1]; print('APs:',len(ch)); print('check: no adjacent same/adjacent-overlap:', all(abs(ch[i]-ch[i+1])>=5 for i in range(3)))\"",
          "Explain why 1,6,11 (5-channel separation = non-overlapping).",
          "What changes for 5GHz? (Many more non-overlapping channels.)"]),
    ]):
        add("comptia-network-plus", LB(f"netplus-lab-extra{i+1}", title, did, obj, steps,
            [CHECK(steps[0].split("Type exactly: ")[1][:40] if "Type exactly:" in steps[0] else steps[0][:40], "", "Run the first command."),
             CHECK("python3", "", "Verify the computation.")],
            "Lab complete \u2014 networking is applied math + reading counters. Both practiced."))
    # infra needs 4 more (has 16)
    for i, (title, did, obj, steps) in enumerate([
        ("LVM Resize Dry Run", "server-hw", "Extend a logical volume safely (concepts + commands).",
         ["Type exactly: lsblk -o NAME,SIZE,TYPE | head -10",
          "Explain the stack: PV \u2192 VG \u2192 LV \u2014 draw it for your disk.",
          "Commands (dry-run knowledge): pvcreate, vgcreate, lvcreate, lvextend -r (the -r resizes fs too).",
          "State the safety rule: snapshot/backup before resize; -r flag or separate resize2fs."]),
        ("Cron Job Audit", "linux-admin", "Find every scheduled task and judge necessity.",
         ["Type exactly: cat /etc/crontab 2>/dev/null; ls /etc/cron.d/ 2>/dev/null",
          "Type exactly: crontab -l 2>/dev/null || echo 'no user crontab'",
          "For each job: still needed? Documented? Logging output?",
          "Kill or fix one unnecessary/broken job (or document why each stays)."]),
        ("Service Dependency Map", "capacity-planning", "Map what depends on what via systemd.",
         ["Type exactly: systemctl list-dependencies --reverse sshd 2>/dev/null | head -12 || systemctl list-dependencies sshd 2>/dev/null | head -12",
          "Type exactly: systemctl is-enabled sshd cron 2>/dev/null",
          "Draw: which services must start before your app?",
          "Explain: why does boot order matter? (Answer: dependencies.)"]),
        ("Network Share Mount", "data", "Mount a network share and verify persistence.",
         ["Type exactly: grep -E 'nfs|cifs' /etc/fstab 2>/dev/null || echo 'no network mounts in fstab'",
          "Explain the fstab fields for a CIFS mount: //server/share /mnt/point cifs credentials=...,_netdev 0 0",
          "Key insight: _netdev waits for network; credentials file (not inline password).",
          "State: what breaks if _netdev is missing? (Boot hang waiting for share.)"]),
    ]):
        add("comptia-infra", LB(f"infra-lab-extra{i+1}", title, did, obj, steps,
            [CHECK(steps[0].split("Type exactly: ")[1][:40] if "Type exactly:" in steps[0] else steps[0][:40], "", "Run the first command."),
             CHECK("2>/dev/null", "", "Verify the second step.")],
            "Lab complete \u2014 infrastructure is layers; you just inspected one."))
    # cpp needs 5 more (has 15)
    for i, (title, did, obj, steps) in enumerate([
        ("STL Algorithm Gym", "stl-containers", "Solve 3 problems with <algorithm> only \u2014 no raw loops.",
         ["Open the Terminal tab.",
          "Type exactly: cat > /tmp/alg.cpp << 'EOF'\n#include <algorithm>\n#include <vector>\n#include <iostream>\nint main(){ std::vector<int> v={5,2,8,1,9};\n std::sort(v.begin(), v.end());\n auto it=std::find_if(v.begin(), v.end(), [](int x){return x>4;});\n std::cout<<\"sorted>4 first: \"<<*it<<\"\\n\";\n std::cout<<\"count>4: \"<<std::count_if(v.begin(),v.end(),[](int x){return x>4;})<<\"\\n\";}\nEOF",
          "Type exactly: g++ -std=c++17 /tmp/alg.cpp -o /tmp/alg && /tmp/alg",
          "Extend: add std::transform to square each element \u2014 no loop.",
          "Rule learned: algorithms + lambdas replace 90% of raw loops."]),
        ("Move Semantics Lab", "memory-smart-pointers", "Observe moves vs copies with a noisy class.",
         ["Open the Terminal tab.",
          "Type exactly: cat > /tmp/mv.cpp << 'EOF'\n#include <iostream>\n#include <vector>\nstruct N{ N(){std::cout<<\"ctor\\n\";} N(const N&){std::cout<<\"COPY\\n\";} N(N&&)noexcept{std::cout<<\"MOVE\\n\";} };\nint main(){ std::vector<N> v; v.reserve(2); N a; v.push_back(a); v.push_back(std::move(a)); }\nEOF",
          "Type exactly: g++ -std=c++17 /tmp/mv.cpp -o /tmp/mv && /tmp/mv",
          "Count COPY vs MOVE. Remove reserve() and re-run \u2014 observe reallocation moves.",
          "Lesson: moves make vector growth cheap; reserve() avoids even those."]),
        ("Template Deduction Drill", "templates-lambdas", "Predict deduction results, then verify.",
         ["Open the Terminal tab.",
          "Type exactly: cat > /tmp/ded.cpp << 'EOF'\n#include <iostream>\ntemplate<typename T> void f(T t){ std::cout<<__PRETTY_FUNCTION__<<\"\\n\"; }\ntemplate<typename T> void g(T& t){ std::cout<<__PRETTY_FUNCTION__<<\"\\n\"; }\nint main(){ int x=1; const int cx=2; f(x); f(cx); f(3); g(x); /*g(3);*/ }\nEOF",
          "Type exactly: g++ -std=c++17 /tmp/ded.cpp -o /tmp/ded && /tmp/ded",
          "Predict BEFORE running: what is T for f(cx)? For g(x)?",
          "Uncomment g(3) mentally: why does it fail? (rvalue can't bind non-const lvalue ref.)"]),
        ("Header Hygiene", "build-toolchain", "Measure include bloat and fix it.",
         ["Open the Terminal tab.",
          "Type exactly: echo '#include <bits/stdc++.h>\nint main(){}' > /tmp/huge.cpp && time g++ -std=c++17 -c /tmp/huge.cpp -o /tmp/huge.o",
          "Type exactly: echo 'int main(){}' > /tmp/tiny.cpp && time g++ -std=c++17 -c /tmp/tiny.cpp -o /tmp/tiny.o",
          "Compare compile times. The difference is include bloat.",
          "Rule: include what you use (IWYU); forward-declare in headers where possible."]),
        ("Constexpr Lab", "core-syntax", "Move computation to compile time.",
         ["Open the Terminal tab.",
          "Type exactly: cat > /tmp/ce.cpp << 'EOF'\nconstexpr int fib(int n){ return n<2 ? n : fib(n-1)+fib(n-2); }\nstatic_assert(fib(10)==55);\nint main(){ constexpr int v=fib(20); return v==6765?0:1; }\nEOF",
          "Type exactly: g++ -std=c++17 /tmp/ce.cpp -o /tmp/ce && ./tmp/ce 2>/dev/null || ./tmp/ce; echo \"exit: $?\"",
          "Verify: static_assert passed at compile time (no runtime cost).",
          "Extend: make fib consteval-adjacent (C++20 consteval) \u2014 discuss when forced compile-time matters."]),
    ]):
        steps_full = steps
        add("cpp", LB(f"cpp-lab-extra{i+1}", title, did, obj, steps_full,
            [CHECK("g++ -std=c++17", "", "Compile the program."),
             CHECK("/tmp/", "", "Run and observe output.")],
            "Lab complete \u2014 C++ rewards precise understanding. You just built some."))
    # creative-code needs 5 more (has 15)
    for i, (title, did, obj, steps) in enumerate([
        ("Color Theory Sprint", "canvas-drawing", "Build 3 palettes: analogous, complementary, triadic \u2014 then use one.",
         ["In your editor: define 3 palettes (5 colors each) programmatically.",
          "Render the same sketch 3 times, once per palette.",
          "Note: which palette fits the mood? Why?",
          "Rule: constrain to the palette \u2014 no off-palette colors. Constraint breeds coherence."]),
        ("Easing Functions", "animation", "Implement 3 easings and feel the difference.",
         ["In your editor: animate a circle across the screen with linear, easeInQuad, easeOutElastic.",
          "Side by side: the motion FEEL differs enormously.",
          "Use: easeOut for entrances, easeIn for exits, elastic sparingly (it's seasoning).",
          "Rule: linear motion looks robotic; easing looks alive."]),
        ("Noise Comparison", "generative-systems", "Compare white noise vs Perlin vs fbm visually.",
         ["In your editor: render 3 strips \u2014 white noise heights, Perlin heights, fbm heights.",
          "Observe: white = jagged, Perlin = smooth hills, fbm = detailed terrain.",
          "Use white for static, Perlin for motion paths, fbm for textures.",
          "Rule: match the noise to the phenomenon."]),
        ("Responsive Canvas", "interaction", "Make a sketch adapt to any window size gracefully.",
         ["In your editor: use relative units (width*0.1) not pixels; handle resize events.",
          "Test: resize from phone to ultrawide \u2014 composition must hold.",
          "Anchor: define focal points as fractions, not coordinates.",
          "Rule: the web is not fixed-size; neither is your art."]),
        ("Export Pipeline", "showcase", "Set up one-command export: PNG sequence + GIF + video.",
         ["Document your current export process (steps, tools, time).",
          "Automate: script the PNG sequence \u2192 ffmpeg to GIF and MP4.",
          "Type exactly: ffmpeg -framerate 30 -i frame%04d.png -vf scale=640:-1 out.gif (when you have frames)",
          "Rule: if export takes >2 minutes of manual work, automate it."]),
    ]):
        add("creative-code", LB(f"cc-lab-extra{i+1}", title, did, obj, steps,
            [CHECK(steps[0][:40], "", "Start the exercise."),
             CHECK("Rule:", "Rule:", "Note the takeaway rule.")],
            "Lab complete \u2014 creative code is 20% code, 80% taste. You trained both."))
    # data-analyst needs 5 more (has 15)
    for i, (title, did, obj, steps) in enumerate([
        ("Cohort Analysis Sprint", "spreadsheets", "Build a cohort retention table from raw data.",
         ["Open the Terminal tab.",
          "Type exactly: python3 -c \"import pandas as pd, numpy as np; np.random.seed(0); df=pd.DataFrame({'cohort':np.repeat(['2026-01','2026-02'],50),'age_mo':np.tile(range(5),20),'active':np.random.rand(100)>0.3}); print(pd.crosstab(df.cohort, df.age_mo, values=df.active, aggfunc='mean').round(2))\"",
          "Read: rows=cohorts, columns=age \u2014 retention curves.",
          "Spot: which cohort retains best? At which age does drop-off hit?",
          "Insight: cohorts separate acquisition quality from product decay."]),
        ("Funnel Math", "visualization", "Compute a 4-stage funnel with conversion rates.",
         ["Open the Terminal tab.",
          "Type exactly: python3 -c \"stages=[10000,6000,1500,300]; names=['visit','signup','trial','paid']\nfor i in range(1,len(stages)):\n print(f'{names[i-1]}->{names[i]}: {stages[i]/stages[i-1]:.1%}')\nprint(f'overall: {stages[-1]/stages[0]:.1%}')\"",
          "Identify the leakiest step \u2014 that's the optimization target.",
          "What-if: 10% relative improvement at each step \u2014 which moves overall most?",
          "Rule: optimize the biggest leak first; overall conversion is multiplicative."]),
        ("Survey Says? (Bias Check)", "statistics", "Design a 5-question survey that minimizes bias.",
         ["Write 5 questions about a product you know.",
          "Audit each for: leading wording, double-barreled asks, missing 'N/A' options.",
          "Rewrite the worst offender neutrally.",
          "Rule: the question shapes the answer; neutral wording is a skill."]),
        ("KPI Tree", "storytelling", "Decompose a North Star metric into its drivers.",
         ["Pick: revenue (or any North Star).",
          "Decompose: revenue = users \u00d7 conversion \u00d7 ARPU; each decomposes further.",
          "Draw the tree 3 levels deep. Mark which leaves you can actually move.",
          "Use: when the North Star moves, the tree says WHERE to look."]),
        ("Spreadsheet Audit", "excel-power", "Audit a real spreadsheet for the 5 common sins.",
         ["Open a spreadsheet you own.",
          "Check: hardcoded values in formulas? Merged cells? No data validation? Volatile functions (INDIRECT/OFFSET)? External links?",
          "Fix the worst sin found.",
          "Rule: audit quarterly; spreadsheets rot silently."]),
    ]):
        add("data-analyst", LB(f"da-lab-extra{i+1}", title, did, obj, steps,
            [CHECK(steps[1][:50] if len(steps)>1 else steps[0][:50], "", "Execute the core step."),
             CHECK("Rule:", "Rule:", "Note the takeaway.")],
            "Lab complete \u2014 analyst craft is built in reps. Another rep done."))
    # data-engineering needs 5 more (has 15)
    for i, (title, did, obj, steps) in enumerate([
        ("Partition Pruning Proof", "warehouses-lakes", "Prove partition pruning with a thought experiment + code.",
         ["Open the Terminal tab.",
          "Type exactly: python3 -c \"import pandas as pd; df=pd.DataFrame({'dt':pd.date_range('2026-01-01',periods=365),'v':range(365)}); df.to_parquet('/tmp/d.parquet', partition_cols=[])\" 2>/dev/null; echo 'partitioned write:'; python3 -c \"import pandas as pd; df=pd.DataFrame({'dt':pd.date_range('2026-01-01',periods=365),'v':range(365)}); df['y']=df.dt.dt.year; df['m']=df.dt.dt.month; df.to_parquet('/tmp/dp', partition_cols=['y','m']); import os; print('partitions:', sum(1 for _,d,_ in os.walk('/tmp/dp')) )\"",
          "Compare: 1 file vs 12 partition dirs. Query one month: which scans less?",
          "Rule: partition by filter column; the file layout IS the index."]),
        ("Idempotency Test", "etl", "Prove a load is idempotent by running it twice.",
         ["Open the Terminal tab.",
          "Type exactly: sqlite3 /tmp/idem.db \"CREATE TABLE IF NOT EXISTS t(id INT PRIMARY KEY, v INT); INSERT OR REPLACE INTO t VALUES (1,100),(2,200); SELECT COUNT(*), SUM(v) FROM t;\"",
          "Run the SAME insert twice more. Count and sum unchanged?",
          "Now try without OR REPLACE (plain INSERT) \u2014 observe the duplicate error.",
          "Rule: idempotent loads make reruns safe; test by running twice."]),
        ("Late Data Simulation", "streaming", "Simulate late events and apply a watermark policy.",
         ["Open the Terminal tab.",
          "Type exactly: python3 -c \"events=[('10:00',100),('10:05',200),('09:58',50),('10:11',300)]; wm='10:05'\nprint('watermark:',wm)\nfor ts,v in events:\n    print(ts, v, 'ACCEPT' if ts>=wm else 'LATE->side output')\"",
          "Observe: the 09:58 event is late. Policy decision: accept, side-output, or drop?",
          "State your policy and its business justification.",
          "Rule: watermarks are business decisions wearing config clothes."]),
        ("Cost Attribution", "cost-performance", "Attribute a fake bill to pipelines.",
         ["On paper: 3 pipelines, costs $500/$300/$200. Tag each with owner + project.",
          "Ask: which is most expensive per TB? (Need volume data \u2014 the missing metric.)",
          "Add volume: compute $/TB for each. The ranking changes \u2014 that's the insight.",
          "Rule: unit economics ($/TB) beat raw totals for decisions."]),
        ("Contract Test Sketch", "quality-governance", "Write a data contract test for a critical table.",
         ["On paper/in terminal:",
          "Table: orders. Tests: unique(order_id), not_null(customer_id), amount >= 0, fresh (< 1h).",
          "Type exactly: echo 'tests: unique, not_null, range, freshness \u2014 the big four' ",
          "State: where do these run? (Answer: post-load, blocking downstream on failure.)",
          "Rule: untested data is untrusted data."]),
    ]):
        add("data-engineering", LB(f"de-lab-extra{i+1}", title, did, obj, steps,
            [CHECK(steps[1][:50] if len(steps)>1 else steps[0][:50], "", "Execute the core step."),
             CHECK("Rule:", "Rule:", "Note the takeaway.")],
            "Lab complete \u2014 data engineering is systems thinking with data. Rep done."))
    return E

def main():
    import expand_batch8 as b8
    results = []
    for cbt_id, cfg in CBT_CONFIG.items():
        path = f"{BASE}/{cbt_id}/content.json"
        with open(path) as f:
            data = json.load(f)
        before = counts(data)

        # 1. standard domains
        ensure_domains(data, [
            ("start-here", f"Start Here: {cfg['course']}", f"Your guided on-ramp to {cfg['course']}: how to use this bootcamp, exam strategy, study system, and systems thinking.", "\U0001F3E0"),
            ("mock-assessment", f"Mock Assessment: {cfg['exam']} Simulation", f"A timed, exam-realistic simulation for {cfg['course']}.", "\U0001F3AF"),
            ("capstone-build", f"Capstone: Build {cfg['course']}", f"Prove it by building it \u2014 a guided portfolio project for {cfg['course']}.", "\U0001F6E0\uFE0F"),
            ("career-roadmap", f"Career Roadmap: {cfg['course']} Roles", f"Roles, resumes, and interview loops for {cfg['course']} skills.", "\U0001F4BC"),
            ("tools-ecosystem", f"Tools Ecosystem: {cfg['course']}", f"The tool landscape and workflows for {cfg['course']}.", "\U0001F9F0"),
        ])
        add_lessons(data, start_here_lessons(cfg['course'], cfg['exam'], cfg['weekly']))
        add_lessons(data, mock_briefing_lessons(cfg['course'], cfg['exam']))
        md = mock_domain(cfg['course'], cfg['exam'])
        add_lessons(data, capstone_lessons(cfg['course'], cfg['capstone_projects']))
        add_lessons(data, career_roadmap_lessons(cfg['course'], cfg['roles']))
        add_lessons(data, tools_ecosystem_lessons(cfg['course'], cfg['tools']))

        # 2. topical new domains
        mod_name, fn_name = cfg['new_module']
        mod = importlib.import_module(mod_name)
        domains, lessons, scenarios, labs = getattr(mod, fn_name)()
        ensure_domains(data, domains)
        add_lessons(data, lessons)
        for d_id, _, _, _ in domains:
            # scenarios were built per-domain; find matching ones by checking scenario domain alignment
            pass
        # scenarios: they were created with specific domain_ids; add each to its domain
        for sc in scenarios:
            add_scenarios(data, sc['domain_id'], [sc])
        add_labs(data, labs)

        # 3. third lessons for new topical domains
        thirds = build_third_lessons().get(cbt_id, {})
        for did, lesson_list in thirds.items():
            for lesson in lesson_list:
                lesson['domain_id'] = did
            add_lessons(data, lesson_list)

        # 4. extra domains for small CBTs
        for did, name, desc, icon in EXTRA_DOMAINS_SMALL.get(cbt_id, []):
            ensure_domains(data, [(did, name, desc, icon)])
        edl = extra_domain_lessons(cbt_id, cfg['course'])
        for did, lessons_list in edl.items():
            if did in [d[0] for d in EXTRA_DOMAINS_SMALL.get(cbt_id, [])]:
                add_lessons(data, lessons_list)

        # 5. top up existing domains
        topup_fn = TOPUP_FNS.get(cbt_id)
        if topup_fn is not None:
            topups = topup_fn()
            for did, lesson_list in topups.items():
                add_lessons(data, lesson_list)

        # 6. extra labs
        for cbt2, lab_list in extra_labs_driver().items():
            if cbt2 == cbt_id:
                add_labs(data, lab_list)
        for cbt2, lab_list in b8.extra_labs_batch8().items():
            if cbt2 == cbt_id:
                add_labs(data, lab_list)
        import expand_batch9 as b9mod
        for cbt2, lab_list in b9mod.extra_labs_batch9().items():
            if cbt2 == cbt_id:
                add_labs(data, lab_list)

        # validate + write
        json.dumps(data)  # raises on bad structure
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        # re-validate from disk
        with open(path) as f:
            json.load(f)
        after = counts(data)
        results.append((cbt_id, before, after))

    print(f"{'CBT':22s} {'domains':>8s} {'lessons':>8s} {'scenarios':>10s} {'labs':>6s}")
    for cbt_id, b, a in results:
        flag = "" if (a[0]>=15 and a[1]>=60 and a[2]>=80 and a[3]>=20) else "  <-- BELOW TARGET"
        print(f"{cbt_id:22s} {b[0]:>3d}->{a[0]:<4d} {b[1]:>3d}->{a[1]:<4d} {b[2]:>3d}->{a[2]:<5d} {b[3]:>3d}->{a[3]:<4d}{flag}")

if __name__ == '__main__':
    main()
