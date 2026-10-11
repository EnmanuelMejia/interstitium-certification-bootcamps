# ThreatLocker IT Infrastructure Assessment Prep — Coverage Matrix

**Standard: EXCEED** — an item counts as fully covered only when the CBT delivers
**theory + lab + drill + troubleshooting** on it, not just a mention.
Ratings: **DEEP** (all four) · **ADEQUATE** (theory + ≥1 of lab/drill/troubleshooting, solid) ·
**MENTION** (named in passing, no dedicated content) · **GAP** (absent).

Scope audited: `content.json` (22 lessons, 20 labs, 10 mock simulations, 8 behavioral Qs,
50-command drill set + 10 sequences + 30-task sprint + 12 error-recovery drills + subnet calculator),
plus incoming patch content (`tl-infra-foundations`, `-framework`, `-math`, `-capstone`, `-syntax` patches).

---

## SECTION 1 — JD Key Responsibilities (Special Projects IT Engineer, Req 1004)

| # | Responsibility | Rating | Where it lives |
|---|---|---|---|
| 1 | Diagnose complex customer IT issues | **DEEP** | 10 mock simulations (`mock-vpn-down-dns-fail`, `mock-ad-replication-split`, `mock-dhcp-exhaustion-outage`, `mock-sql-point-in-time-restore`, `mock-ransomware-file-server`, `mock-expired-cert-exchange`, `mock-print-spooler-kev`, `mock-hyperv-checkpoint-sprawl`, `mock-disk-latency-storage`, `mock-gpo-not-applying`); 20 labs each with break/fix steps; 12 error-recovery drills; 65 scenario preambles (foundations patch) |
| 2 | Product research & test programs | **GAP** | Nothing on product research, pilot methodology, feature evaluation, or test programs. A single "test plan" phrase inside the change-documentation framework — not coverage. |
| 3 | Develop/execute test scripts | **GAP** | No Pester, no QA test-script development, no acceptance-test planning. Lab scripts are *admin* scripts (Health-Check.ps1), not *test* scripts. Zero coverage of the JD meaning. |
| 4 | Deploy & manage O365, Active Directory, networking infrastructure | **SPLIT** — AD: **DEEP**; Networking: **DEEP**; O365: **GAP** | AD: lessons (GPO precedence, FSMO/replication) + labs (`lab-ad-ou-build`, `lab-gpo-deploy`, `lab-replication-fsmo`, `lab-ad-user-lifecycle`) + 10 AD drills + capstone phase 3. Networking: lessons (subnetting, VLANs/trunks, STP/EtherChannel) + labs (`lab-subnet-planner`, `lab-vlan-trunk-config`, `lab-ipsec-diagnose`) + 10 Cisco IOS drills + subnet calculator. **O365/M365/Entra ID: zero mentions anywhere in content.json, all patches, and all tools.** |
| 5 | API integrations | **GAP** | Zero. No `Invoke-RestMethod`/`Invoke-WebRequest`, no REST concepts, no JSON parsing, no webhooks, no Graph API. (Regex hits for "API/REST" in labs were false positives — "domain", "15 minutes of logs".) |
| 6 | Expert-level customer support | **PARTIAL** | Behavioral Q&A touches customer-facing scenarios ("balance security vs user convenience", "Why ThreatLocker"); labs are customer-contextualized; 10 troubleshooting simulations practice the diagnostic half. But: no dedicated lesson on support craft — ticket workflows, SLAs, escalation paths, communication under pressure. No lab, no drill. |
| 7 | Creating/maintaining technical documentation, network diagrams, SOPs | **DEEP** | Lessons "SOPs and Runbooks That Survive Contact With On-Call" + "Network Diagrams and Change Records"; lab `lab-branch-office-handover-pack`; capstone phase 7 (handover pack); behavioral Q on documentation; preambles (`sop-under-time-pressure`, `network-diagram-standards`, `change-documentation-backout`, `handover-notes-oncall`) |

---

## SECTION 2 — Required Qualifications → validating lab/drill

| Qualification | CBT validation | Rating |
|---|---|---|
| Deploying/managing O365 | **None — no O365 content exists** | **GAP** |
| Deploying/managing Active Directory | Labs `lab-ad-ou-build`, `lab-gpo-deploy`, `lab-replication-fsmo`, `lab-ad-user-lifecycle`; 10 AD command drills; sequences seq-01/seq-05; mocks `mock-ad-replication-split`, `mock-gpo-not-applying` | **DEEP** |
| Deploying/managing networking infrastructure | Labs `lab-subnet-planner`, `lab-vlan-trunk-config`, `lab-ipsec-diagnose`, `lab-client-vpn-test`; 10 Cisco IOS drills; 30-task subnet sprint; subnet-calculator tool; mocks `mock-vpn-down-dns-fail`, `mock-dhcp-exhaustion-outage` | **DEEP** |
| API integrations + scripting | Scripting: lesson "Remoting, Hyper-V, and Writing Your First Script", labs `lab-pipeline-mastery`, `lab-remoting-hyperv-sweep`, 50-command drill set, error-recovery drills. **API integrations: no validator exists** | Scripting **DEEP** · API **GAP** |
| Troubleshooting ability | 10 timed mock simulations (the 3-hour mock), 12 error-recovery drills ("fix the broken command"), break/fix lab steps, 65 troubleshooting scenario preambles | **DEEP** |
| 5+ years IT support experience | Experience, not CBT-testable | **N/A** |

---

## SECTION 3 — Desirable Qualifications

| Qualification | Coverage status |
|---|---|
| **CCNA or equivalent** | **PARTIAL.** Networking content is CCNA-*adjacent* at real depth: subnetting/CIDR math, VLANs/trunks/802.1Q, STP, port security, EtherChannel, inter-VLAN routing, IPsec/IKE, Cisco IOS command drills. But: no explicit CCNA objective mapping, no dedicated routing-protocol lesson (OSPF appears only in a preamble), thin NAT coverage, no WAN topic. A CCNA holder would recognize the material; the CBT doesn't claim or structure toward the cert. |
| **MCSA or equivalent** | **PARTIAL.** Windows Server/AD coverage is MCSA-*adjacent* at real depth: GPO precedence/enforcement, FSMO roles, replication health, DNS/DHCP administration, server hardening baseline. But: no explicit MCSA/objective mapping, and MCSA is retired — the modern equivalent path (Azure/Entra hybrid identity) is exactly the O365/Entra gap in Section 1. |

---

## SECTION 4 — 6-Week Bootcamp Topics (from research)

| Topic | Rating | Evidence |
|---|---|---|
| OSI model | **GAP** | Exactly one mention (capstone patch). No layers lesson, no layer→protocol→tool mapping. Foundations teach "IP addresses from zero" without ever naming the model. |
| TCP/IP | **PARTIAL** | TCP handshake covered in foundations ("IP Addresses From Zero" / "Cast of Characters" lessons, ~120 handshake/SYN/ACK references across patches) and touched in the Kerberos math lesson. No dedicated lesson on TCP vs UDP, ports, ICMP, MTU/fragmentation. |
| DNS | **COVERED** | Lesson "AD, DNS, and DHCP Administration One-Liners"; 6 DNS drills; preambles `dns-mail-record-failure`, `dns-dhcp-troubleshoot`; mock `mock-vpn-down-dns-fail`; capstone phase 3. Theory + lab + drill + troubleshooting. |
| Active Directory | **COVERED** | See Section 2 — full-stack depth. |
| Registry | **GAP** | 6 incidental hits total (one in the GPO lesson). No hives/keys lesson, no regedit, no GPO→registry mapping, no backup/restore of registry. |
| Hashing | **GAP** | Appears only as an IPsec parameter ("hash: SHA256" in IKE proposals) and backup-checksum context. No conceptual lesson: hash functions, password hashing vs encryption, integrity verification with `Get-FileHash`. |
| Encryption | **PARTIAL** | Kerberos/LDAP math lesson (AES in Kerberos, 9 encryption references), IPsec lesson (AES-256/ESP), WPA3-vs-WPA2 preamble, expired-cert mock (PKI in practice). No unified "crypto for sysadmins" lesson (symmetric vs asymmetric, PKI/certificates, TLS). |
| Application Allowlisting | **GAP** | Zero mentions. |
| Ringfencing | **GAP** | Zero mentions. |
| Network Control | **GAP** | Zero mentions. |
| Elevation Control | **GAP** | Zero mentions. |
| Storage Control | **GAP** | Zero mentions. |
| Zero Trust principles | **GAP** | Zero mentions — despite being the conceptual frame for every ThreatLocker product above. |

---

## SECTION 5 — Gap List (every GAP or MENTION-only item, with recommendations)

> Ordered by interview impact, highest first.

1. **ThreatLocker product suite (Allowlisting, Ringfencing, Network Control, Elevation Control, Storage Control)** — GAP.
   *Recommendation:* Add a "ThreatLocker Platform" domain: one lesson per control explaining what it does and *which underlying OS mechanism it maps to* (allowlisting ≈ AppLocker/WDAC concepts; ringfencing ≈ application containment; Network Control ≈ host firewall/policy; Elevation Control ≈ UAC/privilege management; Storage Control ≈ removable-media policy) + a lab "Map the controls to the OS" + troubleshooting scenarios per control. For a ThreatLocker interview prep, this is the most strategically costly gap.

2. **Zero Trust principles** — GAP.
   *Recommendation:* Add lesson "Zero Trust: Never Trust, Always Verify" (identity as perimeter, device trust, micro-segmentation, least privilege) explicitly framing the five ThreatLocker controls from gap #1 as a Zero Trust implementation. Pairs naturally with the hardening and firewall lessons.

3. **O365 / Microsoft 365 / Entra ID** — GAP (explicit required qualification).
   *Recommendation:* Add lesson "M365 & Entra ID for the On-Prem Admin": licenses, Exchange Online mail-flow basics, Entra Connect sync concepts, Conditional Access fundamentals, and the admin's PowerShell surface (`Connect-ExchangeOnline`, `Get-MgUser`) as drill cards. Even a single lesson + 10-drill set closes an explicit JD line.

4. **API integrations** — GAP (explicit required qualification).
   *Recommendation:* Add lab "API Integration Lab: Invoke-RestMethod" — GET a REST API, parse JSON with `ConvertFrom-Json`, POST an incident to a mock webhook, plus a Graph API read (`/users`) tying back to gap #3. Add `Invoke-RestMethod`/`Invoke-WebRequest` cards to the drill set.

5. **Develop/execute test scripts** — GAP (explicit JD responsibility).
   *Recommendation:* Add lesson + lab "Test Scripts with Pester": what a test script is vs an admin script, Pester `Describe/It/Should` structure, writing an infrastructure test (e.g., "GPO applied?", "service running?"), and test-plan templates for the product-research workflow.

6. **Product research & test programs** — GAP (explicit JD responsibility).
   *Recommendation:* Add lesson "Product Research & Test Programs": pilot methodology (lab → pilot group → rollout), feature evaluation scorecards, test-program phases (alpha/beta/pilot), and a template evaluation matrix. Lightweight — one lesson + a capstone tie-in.

7. **OSI model** — GAP (bootcamp weeks 1–2 topic; currently a single mention).
   *Recommendation:* Add lesson "OSI & TCP/IP Model": 7 layers with the protocol and the *tool* at each layer (the CBT already teaches the tools — `ping`, `tracert`, `Test-NetConnection`, Wireshark concepts), plus a drill mapping "symptom → layer → tool".

8. **Hashing fundamentals** — GAP (bootcamp weeks 1–2 topic).
   *Recommendation:* Add lesson "Hashing & Integrity": hash functions, SHA-256/MD5, password hashing vs encryption, file-integrity verification with `Get-FileHash` + drill cards. Small, high-yield, and it reuses the IPsec hash-algorithm references already in the CBT.

9. **Windows Registry** — GAP (bootcamp weeks 1–2 topic; 6 incidental hits).
   *Recommendation:* Add lesson "The Windows Registry for Sysadmins": hives, GPO→registry mapping, `regedit`, `.reg` files, registry backup/restore, and why the CBT's GPO lesson works the way it does underneath.

10. **Encryption fundamentals (unified)** — PARTIAL.
    *Recommendation:* Fold into a "Crypto for Sysadmins" lesson alongside gaps #8–#9: symmetric vs asymmetric, PKI/certificates, TLS — giving theory to the expired-cert mock and the IPsec/WPA3 content that currently carry the load alone.

11. **TCP/IP deep-dive** — PARTIAL.
    *Recommendation:* Add lesson "TCP/IP In Depth": TCP vs UDP, ports/sockets, ICMP, MTU/fragmentation — the handshake is already taught in foundations; this completes the suite.

12. **Expert-level customer support craft** — PARTIAL.
    *Recommendation:* Add lesson "Expert Customer Support: Tickets, SLAs, Escalation": ticket lifecycle, SLA math, escalation paths, communicating with non-technical customers under pressure + 2–3 behavioral drill prompts. The diagnostic skill is DEEP; the *support* wrapper is what's thin.

13. **Explicit CCNA/MCSA objective mapping** — PARTIAL.
    *Recommendation:* No new content needed — add an appendix cross-referencing existing CBT modules to CCNA and (retired) MCSA exam objectives, marking which objectives are covered, partial, or out of scope. Turns adjacent depth into a claimable credential bridge.

---

## Overall Readiness Verdict

**CONDITIONAL — strong core, 13 gaps, 5 critical.**

- **Where it EXCEEDS:** Hands-on infrastructure troubleshooting is genuinely excellent — AD, networking, VPN, Hyper-V, SQL Server, storage/backup/DR, PowerShell, hardening, and documentation each carry theory + lab + drill + troubleshooting depth, backed by a 3-hour mock assessment, a 7-phase capstone build, and a 50-command muscle-memory drill system. Against "can this person survive a 3-hour terminal assessment," the answer is credibly yes.
- **Where it FAILS the JD:** Three explicit required qualifications/responsibilities have **zero** coverage — O365/M365/Entra ID, API integrations, and test-script development — plus product research/test programs. A candidate prepped only on this CBT would walk into the interview unable to speak to named JD lines.
- **Where it FAILS its own premise:** A ThreatLocker interview prep with zero coverage of ThreatLocker's five product controls and zero mention of Zero Trust is a branding-level gap — the one topic cluster no generic infra course can substitute for.
- **Bootcamp-topic fidelity:** DNS and AD are COVERED; TCP/IP and encryption are PARTIAL; OSI, registry, and hashing are GAPs against the CBT's own stated weeks 1–2 curriculum.

**Ship-blockers (fix before calling this EXCEED-ready):** gaps #1–#5.
**Should-fix:** gaps #6–#12. **Nice-to-have:** gap #13.

*Method note: ratings were assigned from lesson concepts, lab steps, simulation scenarios,
drill commands, and patch content — not domain names. Regex hits were manually sampled;
false positives (e.g., "API" matching "domain", "O365" matching "Microsoft decided")
were excluded from coverage claims.*
