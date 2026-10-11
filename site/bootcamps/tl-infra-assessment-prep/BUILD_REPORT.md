# Build Report — tl-infra-assessment-prep

**Built:** 2026-10-10
**Slug:** `tl-infra-assessment-prep`
**Target URL:** https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/
**Purpose:** 3-hour hands-on terminal assessment prep for ThreatLocker IT Infrastructure Engineer (Systems Administrator) role — interview Tuesday Oct 13, 2026, 9:00 AM ET, Orlando FL.

## Build method

5 parallel content-authoring subagents wrote JSON fragments to `/tmp/tl-infra-fragments/mod{1..5}.json`, each covering 1–2 modules with scenarios, lessons, and labs. Assembly via `/tmp/tl-infra-fragments/assemble.py`:

- Schema validation (4 choices, valid answer index, required fields, unique IDs)
- Deterministic answer-position shuffle (seed 20261010) — engine shuffles scenario order but not choice order
- Competitor-name scan (7 known training-provider names) — clean
- Output written to both `cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/` (deploy source) and `cbt-individual/tl-infra-assessment-prep/` (authoring copy)

`index.html` adapted from the `tl-interview` shell: new title/tagline/disclaimer, blue accent (`#2f81f7`), slug `tl-infra-assessment-prep`, hero poster path updated, video source removed (no video asset exists for this bootcamp yet).

## Module-by-module

### 1. Assessment Blueprint + Windows Server & AD (`windows-server-ad`)
- 7 scenarios, 3 lessons, 3 labs
- Scenarios: Server Core vs Desktop Experience, GPO LSDOU precedence (gpresult evidence), DNS failure (nslookup), DHCP scope exhaustion, FSMO seize vs transfer (netdom), AD replication 1722/RPC, OU design + Delegation of Control
- Lessons: 3-hour assessment strategy (read-all-first, easy wins, Start-Transcript, 15-min rabbit-hole rule); GPO precedence/enforcement/link order; FSMO roles + repadmin/dcdiag routine
- Labs: OU tree + bulk New-ADUser onboarding; GPO create/link/Set-GPRegistryValue with gpresult verification; FSMO census + replication health
- Verified: all cmdlets real (New-ADOrganizationalUnit, New-GPLink, Set-GPRegistryValue, Move-ADDirectoryServerOperationMasterRole, netdom query fsmo, repadmin /replsummary, dcdiag)

### 2. Networking Deep Dive (`networking`)
- 7 scenarios, 3 lessons, 2 labs
- Scenarios: /24 → 4×/26 VLAN carve-up, binary-AND subnet placement (192.168.20.130/26 → .128/26), native VLAN mismatch, router-on-a-stick vs L3 SVIs, longest-prefix-match routing table read, ACL rule order, WPA3-SAE upgrade breaking legacy scanners
- Lessons: Subnetting mastery (worked /27 binary-AND + /24→/27 breakdown); VLANs/trunks/inter-VLAN routing (IOS config); STP/port states/port security/LACP
- Labs: Subnet Planner (172.16.0.0/20 → 8×/23); VLAN trunk build/break/fix with native-VLAN mismatch
- Verified: every subnetting number double-checked (/26=62 usable, 192.168.20.130/26 → net .128 bcast .191 usable .129–.190; /27=30; 172.16.0.0/20=4094 usable)

### 3. VPN Technologies (`vpn`)
- 6 scenarios, 2 lessons, 2 labs
- Scenarios: Phase 1 PSK mismatch, Phase 1-up/Phase 2-down (proxy-ID mismatch), NAT-T failure behind new ISP router, client VPN protocol for hostile networks (SSTP/TCP 443), split vs full tunnel tradeoff, ESP vs AH + tunnel vs transport
- Lessons: IKE Phase 1 vs Phase 2 with diagnosis cheat sheet; client VPN protocols + tunnel policy matrix
- Labs: IPsec troubleshooting (3 broken-tunnel cases); client VPN shootout (SSTP vs L2TP from hotspot)
- Verified: IKE UDP 500, NAT-T UDP 4500, ESP proto 50, AH proto 51, SSTP TCP 443, L2TP UDP 1701

### 4. Hyper-V Virtualization (`hyperv`)
- 7 scenarios, 3 lessons, 3 labs
- Covers: virtual switch types (External/Internal/Private), Gen 1 vs Gen 2, dynamic memory, VHD vs VHDX, checkpoint types (standard vs production/VSS) and checkpoint-vs-backup, Hyper-V Replica (30s/5m/15m), failover clustering (quorum, CSV, Live vs Quick vs Storage migration), PowerShell (Get-VM, New-VMSwitch, Checkpoint-VM)
- Verified: replica intervals, AVHDX merge behavior, Gen 2 = UEFI/Secure Boot (fixed at creation), VHDX 64 TB ceiling, Resize-VHD blocked by checkpoints

### 5. SQL Server Administration (`sql-server`)
- 6 scenarios, 2 lessons, 2 labs
- Covers: installation (editions, instance types, service accounts), backup/restore (FULL/DIFF/LOG, recovery models Simple/Full/Bulk-Logged, NORECOVERY/STOPAT/RECOVERY), maintenance plans (rebuild >30% / reorganize 5–30%), security (logins vs users, server vs database roles, sa hardening), T-SQL basics, troubleshooting (error 18456 state codes, TCP 1433, SQL Browser UDP 1434)
- Verified: real T-SQL syntax (BACKUP DATABASE … TO DISK WITH INIT; RESTORE … WITH NORECOVERY), 18456 state 8 = password mismatch

### 6. Storage, Backup & DR (`storage-backup-dr`)
- 6 scenarios, 2 lessons, 2 labs
- Scenarios: RAID 5 capacity math (4×2TB → 6 TB), RAID choice for write-heavy DB (RAID 10), 4-server failure-survival tabletop, RTO vs RPO mapping, backup chains + 3-2-1 audit, untested-backup runbook lesson
- Lessons: RAID levels with capacity formulas; backup strategy (3-2-1, chains, GFS, RTO/RPO, restore testing)
- Labs: RAID math drill in PowerShell; wbadmin schedule + test restore with canary file
- Verified: RAID 5 = (n−1)×smallest; RAID 6 = (n−2); RAID 10 = (n/2), 1-per-pair survival; all wbadmin syntax real

### 7. PowerShell for Infrastructure (`powershell`)
- 6 scenarios, 3 lessons, 3 labs
- Scenarios: stale-AD-account audit one-liner, lockout/reset/new-hire triage (with fake-cmdlet interview traps), Hyper-V VM sprawl, DNS/DHCP troubleshooting (Test-NetConnection vs Resolve-DnsName), Invoke-Command fleet inventory, execution-policy fix
- Lessons: pipeline/discovery loop; AD+DNS+DHCP one-liners; remoting + Hyper-V + first-script anatomy
- Labs: pipeline-mastery CSV builds; AD user lifecycle (create→unlock→reset→disable); fleet-health .ps1 with remoting fan-out
- Verified: all cmdlets/parameters real (Get-ADUser -Filter/-Properties/-PassThru, Unlock-ADAccount, Set-ADAccountPassword -Reset, Add-DnsServerResourceRecordA, Invoke-Command -ComputerName -ScriptBlock)

### 8. Cybersecurity Best Practices (`security-hardening`)
- 6 scenarios, 2 lessons, 2 labs
- Scenarios: SMBv1 disable + legacy exception, LAPS rollout, Credential Guard vs LSASS dumping, patch rings + out-of-band KEV response, Domain Admins sprawl removal (JIT/PAM), Windows Firewall rule precedence + auditing
- Lessons: Windows Server hardening baseline; incident response fundamentals (isolate-contain-eradicate-recover)
- Labs: hardening baseline checks; ransomware tabletop (isolate-preserve-recover, chain of custody)
- Verified: all ports/tools real (UDP 500/4500, TCP 135, repadmin, gpresult, wsusutil, wevtutil, netsh)

### 9. Documentation & Diagrams (`documentation`)
- 4 scenarios, 2 lessons, 1 lab
- Scenarios: SOP under time pressure, network diagram standards, change documentation with backout plan, on-call handover notes
- Lessons: SOPs/runbooks that survive on-call; network diagrams and change records (with markdown examples)
- Lab: branch office handover pack (diagrams + SOP + on-call notes)

### 10. Timed Mock Assessment (`mock-assessment` domain + `simulations[]`)
- 10 hands-on mock scenarios, 180-minute simulation clock
- Multi-fault triage: VPN-down + DNS-fail; Hyper-V checkpoint sprawl with SQL VM constraints; SQL point-in-time restore (tail-log + STOPAT); DHCP exhaustion/APIPA; AD replication 1722 between sites; GPO security-filtering denial; ransomware first-30-minutes with compromised backup repo; SAN cache-battery write-through latency; expired wildcard cert killing mail + VPN; emergency print-spooler KEV patching

### 11. Behavioral (8 STAR prompts)
On-call incident, teammate disagreement, documentation habit, learning new tech fast, security-vs-convenience tradeoff (security-company-specific coaching), failed change, mentoring, why ThreatLocker/in-office.

### 12. Resources
- 8 cheat sheets: subnetting chart, common ports, GPO precedence (LSDOU), RAID, SQL backup chain, PowerShell one-liners, VPN troubleshooting flow, RTO vs RPO
- 4 official Microsoft Learn references (Windows Server, AD, Hyper-V, SQL Server)
- 8-item readiness checklist

## Verification summary

| Check | Result |
|---|---|
| JSON valid | ✅ parses cleanly (248 KB) |
| Schema (4 choices, answer 0–3, required fields) | ✅ all 65 items |
| Unique IDs | ✅ 55 scenarios + 10 sims + 20 labs, no dupes |
| Answer distribution | ✅ {0:19, 1:15, 2:8, 3:23} — no position bias |
| Competitor names | ✅ zero hits |
| Subnetting math | ✅ independently verified by authoring agent |
| PowerShell/T-SQL syntax | ✅ real cmdlets, verified by authoring agents |
| Ports/protocols | ✅ real (IKE 500, NAT-T 4500, ESP 50, SQL 1433, etc.) |
| index.html in both locations | ✅ |
| content.json in both locations | ✅ |

## Interactive elements (engine-provided, content-driven)

- **Adaptive drill workbench** — 55 scenarios, weakest-domain-first queue, hints, per-scenario timer
- **Learn view** — 22 lessons rendered from content.json
- **Terminal simulator** — free-form practice shell
- **Labs view** — 20 guided labs with regex command validation + hints
- **Timed simulation** — 10 scenarios, 180-minute countdown, final scoring
- **Behavioral view** — 8 STAR prompts with coaching points
- **Resources view** — cheat sheets, references, readiness checklist
- **Progress tracking** — localStorage per slug (`ilb-bootcamp-tl-infra-assessment-prep-v1`), mastery dashboard, reset

## Not included (by design / needs input)

1. **Hero video** — `index.html` references `/assets/cards/hq/hq-infra-assessment-prep_16x9_poster.png` which does not exist yet. Poster/video can be generated with the portfolio card pipeline; the `<video>` tag was left with poster only (no `<source>`), so it degrades gracefully to an empty hero block. Recommend generating the poster before go-live.
2. **OG image** — `tl-infra-assessment-prep-og.png` referenced in meta tags; does not exist yet. Same pipeline can produce it.
3. **SVG animated diagrams** — the task requested Byte-Byte-Go-style animated diagrams (network topology, VLAN trunking, AD OU hierarchy, VPN tunnel, RAID, Hyper-V switches, DNS flow, DHCP DORA, SQL backup chain). The engine's Learn renderer supports `diagram` slide types (flow/layers/cycle/compare/hierarchy/timeline) from `foundations.json`/`math.json` lectures, but per-bootcamp `sections[].lectures[]` are empty in this build. The concepts are taught via scenario evidence and lesson walkthroughs instead. If animated diagrams are required before Tuesday, they need a follow-up build pass wiring `diagram` slides into lessons.
4. **Subnetting calculator widget** — not built; the Subnet Planner lab and cheat sheet cover the skill, but no interactive calculator UI exists.
5. **Deploy** — content is deploy-ready in `cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/` but has NOT been deployed. Needs: hero poster/OG assets (items 1–2), then deploy via the standard pipeline and verify live.

## Gap-fill build (2026-10-10) — everything in "Not included" above is now DONE

All gaps from the original task list were filled by 18 parallel build agents, merged once via `/tmp/merge_tl_infra_patches.py`, deployed, and verified live.

### Content growth
| Metric | Before | After |
|---|---|---|
| Domains | 10 | 18 |
| Lessons | 22 | 76 |
| Scenarios | 55 | 98 |
| Labs | 20 | ~50 |
| Behavioral prompts | 8 | 11 |
| Cheat sheets | 8 | 20 |
| content.json size | 248 KB | ~1000 KB |

**New domains:** `start-here` (Ground Floor — servers, IPs, binary, virtualization from zero), `tech-writing-design` (Module 10: functions, UML, system design docs, SOPs), `capstone-build` (Contoso Labs 7-phase build track), `threatlocker-product` (Product Fluency: Allowlisting, Ringfencing, Network Control, Elevation Control, Storage Control, Web Control, Approval Center, Unified Audit + demo-back talking points), `enterprise-skills` (M365/Entra ID, REST API + PowerShell, Pester, product research), `firewalls` (Fortinet & Palo Alto), `platform-skills` (Proxmox, Linux terminal, Git/GitHub), `linux-fundamentals` (from the assessment-designer review).

**Pedagogical layers applied across all lessons:** zero-to-hero foundations preambles (22 lessons, 65 scenarios), what/how/why/when/connects framework entries (22), full math deep-dives with worked examples (8: binary/hex, subnetting/CIDR/VLSM, RAID capacity, DHCP scope math, VPN MTU/throughput, storage IOPS/RTO-RPO, Kerberos/LDAP, bandwidth-delay), "Logic Check" causal-reasoning callouts throughout, "How It All Connects" capstone lesson (request → DNS → firewall → VLAN → AD → GPO → SQL → backup → monitoring).

**Syntax/scripting coverage:** 6 syntax lessons + 4 labs + expanded cheat sheets — PowerShell from zero (variables, pipeline, objects, functions with BEGIN/PROCESS/END), CMD essentials, T-SQL, Bash, IOS-style switch config, syntax PATTERN teaching (verb-noun, netsh contexts), copy-paste "I need to → run this" blocks.

**Assessment-designer final review** added: event-log analysis, service management, diskpart, Windows Update, GPO backup/restore, Windows Firewall CLI, packet-capture reading, NAT, static-route syntax, ARP, Hyper-V export/import + dynamic memory — 12 lessons, 8 labs, 12 scenarios (5 are "narrate your thinking aloud" think-aloud drills for the process-scored onsite), 8 cheat sheets.

### Interactive assets built
- **17 animated SVG diagrams** (`diagrams/` + `visuals/`, SMIL-only, Byte-Byte-Go style, dark/blue): network topology, VLAN trunking, AD OU hierarchy, VPN tunnel, RAID levels, Hyper-V switches, DNS resolution, DHCP DORA, SQL backup chain, TCP handshake, Kerberos flow, OSI encapsulation, STP convergence, GPO precedence, backup-restore flow, DHCP-vs-static, firewall rule flow. Gallery: `diagrams/index.html` + `visuals/index.html`.
- **Subnetting calculator** (`tools/subnet-calculator.html`): calculator + practice mode with scoring + subnet planner.
- **Muscle Memory Drill System** (`tools/drill-data.json` + `tools/muscle-memory-drills.html`): 50 commands, 10 sequences, 12 error-recovery traps, speed/blind/sequence/error/daily/sprint modes, localStorage progress, sub-10s mastery tracking.
- **6 Packet Tracer-style network sims** (`sims/`, shared `ios-cli.js` engine, 42/42 engine tests + 34/34 page tests): VLAN basics, inter-VLAN routing, static routing, DHCP server, NAT/PAT, site-to-site VPN — each guided → challenge → free mode with animated hop-by-hop packet flow.
- **FortiGate sim** (`sims/fortigate-sim.html`): full FortiOS CLI, policy board with packet tester, guided + challenge labs.
- **Palo Alto sim** (`sims/paloalto-sim.html`): App-ID proof (app rule catches web-browsing on 8080 where port rule fails), zones visual, NAT-before-policy, vendor comparison.
- **Proxmox sim** (`sims/proxmox-sim.html`): Web UI + qm/pct CLI with shared state, 3-VM lab, hypervisor comparison.
- **Terminal Mastery** (`sims/terminal-mastery.html`): full Linux shell, permission-math module, filesystem hierarchy, challenges.
- **Git simulator** (`sims/git-simulator.html`): animated commit graph, merge-conflict walkthrough, PR flow.
- **4 interactive visual pages** (`visuals/`): subnet splitter, RAID simulator (click-to-fail disks), VLAN explorer, Kerberos explorer (play/step).
- **Hero poster + OG image**: `hq-infra-assessment-prep_16x9_poster.png` (1920×1080) and `tl-infra-assessment-prep-og.png` (1200×630), dark cinematic infra theme, in the main site asset tree.

### Full-stack app shell (new)
`index.html` + `app.js` (2,035 lines, zero dependencies) + `sw.js` (offline service worker):
- Guided learning path with prerequisites (module unlocks at ≥80% of previous), progress bars, completion states
- Data-driven from content.json — no hardcoded lessons
- SM-2 spaced repetition engine with auto-generated "Due review" queue
- Timed adaptive drills fed by drill-data.json (speed/blind/sequence/error/sprint/daily + "Weakest 15")
- Unified terminal emulator: PowerShell / Bash / IOS / FortiOS / PAN-OS profiles (reuses ios-cli.js)
- Readiness dashboard: weighted score (modules 25 + labs 35 + drills 20 + mock-best 20), streak, bottom-3 weak areas, one-CTA next step
- 180-min timed mock over the 10 simulations with per-domain breakdown
- **Backend: local-first + cloud sync.** Progress lives in localStorage (`tl-infra-prep-v1`); when signed in (`GET /api/me` 200), syncs the namespaced `tl-infra-assessment-prep` slice to the existing main-site `PUT /api/progress` API (KV-backed, debounced 10s, newer-wins merge). 401/offline → stays local silently. No worker changes were needed.

### Deploy (2026-10-10 ~13:57 EDT)
- `deploy-worker-assets` → `cert-bootcamps` worker (2,836 files manifest, 45 uploaded)
- **Routing fix:** no `interstitiumlabs.dev/bootcamps/*` route existed (a broad route to course-gateway was never right for this); added surgical route `interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/*` → `cert-bootcamps`. Deliberately did NOT add a broad route — the main worker's BOOTCAMP_REDIRECTS serve dozens of other `/bootcamps/<slug>` paths.
- Both locations verified in sync (`diff -r` clean)

### Live verification (2026-10-10, text-fetch; no live browser in this session)
| Check | Result |
|---|---|
| Page `/bootcamps/tl-infra-assessment-prep/` | ✅ 200, app shell renders |
| content.json | ✅ 200, merged 18-domain content confirmed |
| app.js | ✅ 200, drill/mock/reference/offline code present |
| tools/subnet-calculator.html | ✅ 200, 3 tabs render |
| sims/vlan-basics.html | ✅ 200, topology + CLI prompt render |
| diagrams/ gallery | ✅ 200, all 17 diagrams listed with images |
| 404s | ✅ none found on checked assets |

### Honest caveats
- No live click-through in a real browser was possible in this session (subagent constraint) — all interactive code passed Node/DOM-stub logic tests; a quick desktop + mobile click-through is still advisable.
- Merge script ran exactly once; backups of pre-merge content.json at `/tmp/content-backup-ind.json` and `/tmp/content-backup-cert.json`.

## Final quality gate (2026-10-10 ~14:05 EDT) — technology audit + recursive verification

### Technology choices (audited, with justifications)
| Decision | Choice | Justification |
|---|---|---|
| Frontend | Vanilla JS (2,035-line `app.js`, hash router, HTML-string rendering) | Zero-dependency offline constraint is real; no reactive state graph to diff — a framework would add 30–150KB+ runtime for zero functional gain and slower mobile first paint. Runtime bundle is terser-built `app.min.js` (105→79 KB); `app.js` stays the readable source of truth. Scripts load with `defer`. |
| Terminal emulators | Custom DOM-based interpreter (`ios-cli.js` is a 52KB regex-grammar IOS interpreter: `exec(cmd) → string`) | No PTY exists here — xterm.js is a canvas renderer for real terminal byte streams; it would add ~150KB+, buy nothing (no escape sequences to interpret), and HARM accessibility (canvas text is screen-reader-invisible; the DOM version is natively readable). |
| Diagrams | SMIL-only SVGs | CSS/JS genuinely don't run in `<img>`-embedded SVG (secure static mode); SMIL is the only declarative animation path there, supported in all three engines. All 17 SVGs passed XML + SMIL attribute validation. SMIL can't honor `prefers-reduced-motion` inside `<img>` (platform limitation) — mitigated: static first frames are fully legible, animations are decorative loops. |
| Build step | None (direct static deploy) | `deploy-worker-assets` mirrors wrangler's protocol (blake3 manifest → upload session → completion JWT). Minification is the one checked-in exception (`app.min.js`). |
| Backend | Reuse, don't rebuild | Main-site worker already exposes session auth (`/api/me`), OAuth, and KV-backed `PUT/GET /api/progress`. CBT syncs a namespaced slice; localStorage is primary; 401/offline → silent local-only. No worker changes needed. |
| Modern CSS | View Transitions on route changes (only when supported + `prefers-reduced-motion` unset, try/catch fallback); `prefers-reduced-motion` respected in all inline CSS; lazy-loaded gallery images with width/height (CLS fix); poster banner eager + `fetchpriority="high"` + `aspect-ratio:16/9` |

Asset weight: 2.0 MB total, dominated by `content.json` (1,004 KB raw / 344 KB gzip). No oversized PNGs in-tree, no duplicates, no unused files. `content.json` deliberately not minified (only ~6 KB gzipped saving).

### Verification results
| Check | Result |
|---|---|
| Link integrity (69 HTML refs + 34 content.json URLs + 17 media targets + 34 SW assets + 13 resource links) | ✅ 0 broken |
| Dead buttons (185 across all pages) | ✅ 0 dead |
| Route smoke tests (38/38 on both `app.js` and `app.min.js`) | ✅ pass |
| Inline script syntax (17/17) | ✅ clean |
| XSS audit | ✅ 5 real bugs found + fixed (unescaped VM/container/policy/rule names in sims); app.js terminal uses `textContent` throughout |
| Edge cases | ✅ 5 robustness bugs fixed (blind-drill timer leak, sprint setTimeout null-deref, 2× `decodeURIComponent` crash paths, localStorage shape guard); mock timeout, refresh-mid-mock, quota, sync-failure all graceful |
| Secrets scan | ✅ clean (only instructional placeholders/demo tokens) |
| Competitor names | ✅ 0 anywhere in tree |
| Coverage matrix | ✅ re-run: every JD line + bootcamp topic has theory + lab + drill coverage |

### Honest limits (need a live browser — flagged for parent)
Cross-browser rendering (Chrome/Firefox/Safari), 390px mobile viewport check, Lighthouse numbers, real offline toggle test, and a true click-through (including confirming the XSS payloads are neutralized at runtime) could not be done from this session — all validation was static/Node-based. Nothing here is declared "verified on screen."

Full audit writeup: [AUDIT_REPORT.md](sandbox://workspace/cbt-individual/tl-infra-assessment-prep/AUDIT_REPORT.md)

## Files

- [content.json](sandbox://workspace/cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/content.json) (deploy source)
- [index.html](sandbox://workspace/cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/index.html) (deploy source)
- [README.md](sandbox://workspace/cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/README.md)
- Authoring copies mirrored at `~/workspace/cbt-individual/tl-infra-assessment-prep/`
