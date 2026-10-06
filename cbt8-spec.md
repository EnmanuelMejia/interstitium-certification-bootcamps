# CBT-8 Build Spec — 8 Certification Training Courses for Interstitium Labs

You are a content author building ONE OR TWO interactive computer-based training (CBT) courses
for Interstitium Labs' certification bootcamp platform. Each CBT is a single JSON file that the
platform generator turns into a full interactive course (adaptive drills, lessons, labs, simulated
terminal, timed exam-prep mode, chat companion).

## Your assignment (which CBTs you are building) is in the task message that spawned you.
Write each CBT to: `/home/hatch/workspace/cert-bootcamps/content/<slug>.json`

## Reference implementation (READ FIRST)
- `/home/hatch/workspace/cert-bootcamps/content/aws-clf.json` — complete working example. Copy its
  top-level key set and the shapes of `lessons`, `labs`, `terminalMissions`, `simulations`,
  `consoleSims`, `behavioral`, `chat`, `media`, `resources`.
- `/home/hatch/workspace/cert-bootcamps/docs/content-schema.md` — the schema doc.

## Hard rules (violations fail validation or damage trust)
1. **ORIGINAL CONTENT ONLY.** Never reproduce real exam questions — no braindumps, for CompTIA,
   Cisco, ISC2, AWS, Microsoft, or any vendor. Write original scenario-style questions that teach
   the underlying concepts from the official PUBLIC exam objectives (objectives are public;
   your questions must be yours).
2. **No invented facts.** Commands, flags, API names, default ports, protocol numbers, exam
   formats, and limits must be REAL. If unsure about a trivia detail, write the scenario around
   the concept instead of the trivia. Examples of real facts you may rely on: DNS 53, HTTP 80,
   HTTPS 443, SSH 22, RDP 3389, SMB 445, DHCP 67/68, FTP 20/21, SMTP 25, POP3 110, IMAP 143,
   SNMP 161/162, LDAP 389, LDAPS 636, Telnet 23, TFTP 69, NTP 123, Syslog 514; private IPv4
   ranges 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16; APIPA 169.254.0.0/16; loopback 127.0.0.1;
   IPv6 loopback ::1; common subnet masks /24=255.255.255.0, /16, /8.
3. **No affiliation claims.** Every file carries the disclaimer (given per-CBT below). Never claim
   endorsement, partnership, or official status with any vendor. The course confers NO certificate.
4. **No personal data.** Generic any-candidate framing. Do NOT mention the founder's name or claim
   anyone holds any certification. (The founder holds CompTIA A+ CE; the courses must not claim
   he holds any other cert — simply say nothing about it.)
5. **Valid JSON.** UTF-8, no trailing commas, double quotes. After writing, run:
   `python3 -c "import json; d=json.load(open('/home/hatch/workspace/cert-bootcamps/content/<slug>.json')); print('OK', len(d['domains']), 'domains')"`
   Fix any parse error before finishing.

## Top-level JSON (all keys required unless noted)
```json
{
  "slug": "<slug>",
  "title": "<Title>",
  "tagline": "<one-line hook>",
  "vendor": {"name": "<Vendor>", "certs": "<exam codes>", "docs": "<vendor cert URL>"},
  "disclaimer": "Independent practice material by Interstitium Labs. Not affiliated with, endorsed by, or sponsored by <Vendor>. Confers no certificate. All scenarios are original; no exam content is reproduced.",
  "accent": "<hex color>",
  "simulation": {"items": 40, "minutes": 60},
  "domains": [ ... 5-6 domains ... ],
  "lessons": [ ... one per domain ... ],
  "behavioral": [ ... 8 prompts ... ],
  "chat": {"persona": "...", "topics": [ ... one per domain ... ]},
  "labs": [ ... 4-6 guided labs ... ],
  "terminalMissions": [ ... 3-6 CLI missions ... ],
  "simulations": [ ... 2-4 multi-step troubleshooting sims ... ],
  "foundations": [ ... 1-2 optional math/concept refreshers ... ],
  "resources": [{"label": "Official exam objectives", "url": "<vendor objectives URL>"}]
}
```
- `simulation.items`/`minutes`: timed exam-prep mode config (values given per-CBT below).
- `sections`, `media`, `consoleSims` are optional; include `consoleSims` (2) only if you have a
  genuinely useful console interaction, else omit.

## Domains
5-6 per CBT (per-CBT domain list below — use the exact ids and names). Each domain: **6-8 scenarios**.
Scenario object (all keys required):
```json
{
  "id": "a-plus-ram-seating",
  "title": "The machine that forgot its memory",
  "situation": "A desktop powers on, fans spin, but the screen stays black and you hear three short beeps.",
  "prompt": "What is the most likely cause, and what is your first action?",
  "evidence": [["POST beep log", "3 short beeps, repeating\nNo video output"]],
  "choices": ["Reseat the RAM modules", "Replace the power supply", "Flash the BIOS", "Swap the CMOS battery"],
  "answer": 0,
  "why": "Three short beeps is the classic POST code for a memory fault on most desktop BIOS/UEFI firmware. Reseating the RAM re-establishes contact and is the fastest first check before replacing parts.",
  "hint": "What does the system check before it ever touches the disk?",
  "objectives": ["POST codes", "Memory troubleshooting"],
  "mins": 6
}
```
- `id`: kebab-case, unique within the file. `choices`: exactly 4, plausible distractors, one clearly best.
  `answer`: 0-based index. `evidence`: 0-4 `[label, text]` pairs, each under ~12 lines. `why`: 2-4
  sentences teaching the concept. `hint`: Socratic nudge, never the answer. `mins`: 4-12.
- Vary scenario angles: troubleshooting, design decision, "which tool/command", spot-the-misconfiguration,
  best-practice judgment, cost/risk trade-off. Not every scenario needs evidence.

## Lessons (one per domain, keyed by domain_id)
```json
{
  "domain_id": "hardware",
  "title": "Hardware & Mobile Devices — Core concepts",
  "concepts": ["4-6 crisp concept bullets, each 1-2 sentences, teaching not listing"],
  "example": {"lang": "text", "code": "short realistic snippet", "walkthrough": "2-3 sentences explaining it"},
  "pitfalls": ["3-4 'Common trap: ...' bullets naming mistakes learners make"],
  "try_it": "One-line pointer, e.g. 'Work through this in the Terminal tab →'"
}
```

## Behavioral (exactly 8)
IT-support-role interview prompts with STAR framework, points, pitfalls:
```json
{"prompt": "Tell me about a time you solved a problem under time pressure with an impatient user waiting.",
 "framework": "STAR",
 "points": ["Set the scene in one sentence", "Your specific actions", "Measurable outcome"],
 "pitfalls": ["Blaming the user", "No outcome stated"]}
```
Tailor 2-3 prompts per CBT to the cert's domain (e.g., CCNA: explaining a network outage to non-technical staff).

## Chat companion
```json
{"persona": "You are a friendly but rigorous <Cert> practice coach running a mock assessment.",
 "topics": [{"id": "<domain_id>", "name": "<Domain Name>",
   "key_points": ["4-6 keywords", "..."],
   "followups": ["Can you give an example?", "What would break if...?"]}]}
```
One topic per domain, ids must match domain ids exactly.

## Labs (4-6)
Guided hands-on labs; steps reference the Terminal tab. Shape (copy from aws-clf.json):
```json
{"id": "<slug>-lab-1", "title": "...", "objective": "...",
 "steps": ["...", "Open the Terminal tab ...", "Type exactly: <command> ..."],
 "checks": [{"command_pattern": "<command>", "expect_contains": "<expected output fragment>",
             "hint": "In the Terminal tab, run `<command>`. ..."}]}
```
`command_pattern` is a regex matched against what the learner types; `expect_contains` is a substring
the simulated output must contain — so the "Type exactly" step must produce output containing it.
Keep lab commands REAL (ping, ipconfig/ifconfig/ip addr, nslookup, tracert/traceroute, netstat/ss,
ssh, show ip interface brief, etc.). The simulated terminal echoes plausible output; design checks
so the expected fragment genuinely appears.

## Terminal missions (3-6)
Short CLI challenges. Shape (copy from aws-clf.json):
```json
{"id": "<slug>-mission-1", "title": "...", "domain_id": "<domain_id>", "difficulty": 1,
 "brief": "...", "objectives": ["...", "..."],
 "checks": [{"command_pattern": "^<regex>$", "expect_contains": "<fragment>", "hint": "..."}],
 "success_message": "..."}
```
Difficulty 1-3.

## Simulations (2-4)
Multi-step troubleshooting narratives with evidence and decision options. Shape (copy aws-clf.json
`simulations[0]`): id, title, kind ("troubleshoot"), domain_id, difficulty, brief, steps[] where each
step has symptom, evidence [[label,text]...], options[] (4), answer index, why.

## Foundations (1-2, optional but nice)
Quick refreshers, e.g. binary/decimal conversion for Network+/CCNA, CIA triad for Security+/ISC2.

## Per-CBT definitions

### 1. comptia-a-plus — CompTIA A+
- title: "CompTIA A+", tagline: "220-1201/1202: hardware, operating systems, networking, security, troubleshooting"
- vendor: {"name": "CompTIA", "certs": "A+ (220-1201/220-1202)", "docs": "https://www.comptia.org/certifications/a"}
- accent: "#e8442e", simulation: {"items": 40, "minutes": 60}
- domains:
  - hardware / "Hardware & Mobile Devices": PC components, RAM types, storage (HDD/SSD/NVMe), motherboards, PSUs, mobile devices, printers, ESD safety
  - networking / "Networking": TCP/IP, common ports, Wi-Fi standards, SOHO router setup, cabling (Cat5e/6, fiber), IP addressing basics
  - operating-systems / "Operating Systems": Windows editions and features, installation/upgrade paths, disk management, Linux and macOS basics, command-line tools (ipconfig, chkdsk, sfc, diskpart, grep, chmod)
  - security / "Security": malware types, removal best practices, SOHO wireless security, access control, workstation hardening
  - troubleshooting / "Software & Hardware Troubleshooting": the 6-step CompTIA troubleshooting methodology, common OS/hardware/network symptoms
  - procedures / "Operational Procedures": safety (ESD, power), environmental controls, documentation, professionalism, basic scripting
- terminal missions: Windows CMD/PowerShell + Linux basics (ipconfig, ping, chkdsk, sfc /scannow, ls, chmod, ps)

### 2. comptia-network-plus — CompTIA Network+
- title: "CompTIA Network+", tagline: "N10-009: concepts, implementation, operations, security, troubleshooting"
- vendor: {"name": "CompTIA", "certs": "Network+ (N10-009)", "docs": "https://www.comptia.org/certifications/network"}
- accent: "#2e9de8", simulation: {"items": 40, "minutes": 60}
- domains:
  - concepts / "Networking Concepts": OSI and TCP/IP models, encapsulation, cabling and connectors, topologies
  - implementation / "Network Implementation": IPv4/IPv6 addressing and SUBNETTING (several scenarios), routing concepts, switching, VLANs, wireless configuration
  - operations / "Network Operations": monitoring, performance metrics, documentation/diagrams, high availability, policies
  - net-security / "Network Security": firewalls, IDS/IPS, VPNs, hardening, common attacks (spoofing, MITM, rogue AP)
  - net-troubleshoot / "Network Troubleshooting": methodology, tools (ping, traceroute, nslookup/dig, netstat/ss, Wireshark), cable and interface issues
- foundations: binary-to-decimal and subnetting refresher (REQUIRED — include both)
- terminal missions: ping/traceroute/nslookup/ip addr/ss drills, subnet calculations

### 3. comptia-security-plus — CompTIA Security+
- title: "CompTIA Security+", tagline: "SY0-701: threats, architecture, operations, governance"
- vendor: {"name": "CompTIA", "certs": "Security+ (SY0-701)", "docs": "https://www.comptia.org/certifications/security"}
- accent: "#f0a832", simulation: {"items": 40, "minutes": 60}
- domains:
  - concepts / "General Security Concepts": CIA triad, control types (technical/managerial/operational; preventive/detective/corrective), cryptography (symmetric/asymmetric, hashing), PKI and certificates
  - threats / "Threats, Vulnerabilities & Mitigations": malware, social engineering, application attacks (injection, XSS), vulnerability scanning vs pen testing, mitigation techniques
  - architecture / "Security Architecture": Zero Trust, network segmentation, cloud models (IaaS/PaaS/SaaS, shared responsibility), resilience (backups, HA)
  - operations / "Security Operations": SIEM and log analysis, incident response lifecycle, digital forensics basics, vulnerability management
  - governance / "Security Program Management": risk management, policies/standards, compliance (GDPR, PCI-DSS, HIPAA at concept level), third-party risk, awareness training
- terminal missions: reading auth logs, certificate inspection concepts, hashing demos (sha256sum), nmap-style recon reasoning

### 4. cisco-ccna — Cisco CCNA
- title: "Cisco CCNA", tagline: "200-301: routing, switching, IP services, security, automation"
- vendor: {"name": "Cisco", "certs": "CCNA (200-301)", "docs": "https://www.cisco.com/site/US/en/learn/training-certifications/certifications/enterprise/ccna/index.html"}
- accent: "#1ba0d7", simulation: {"items": 40, "minutes": 60}
- domains:
  - fundamentals / "Network Fundamentals": OSI/TCP-IP, cabling, IPv4 addressing and subnetting, IPv6 basics, wireless principles
  - access / "Network Access": VLANs, trunking (802.1Q), EtherChannel, STP/RSTP, WLAN deployment
  - ip-connectivity / "IP Connectivity": routing tables, static routing, OSPFv2 single-area, first-hop redundancy (HSRP)
  - ip-services / "IP Services": NAT/PAT, NTP, DHCP, DNS, QoS concepts, SNMP, SSH vs Telnet
  - sec-fund / "Security Fundamentals": device hardening, AAA, VPNs (site-to-site vs remote-access), wireless security (WPA2/WPA3), Layer 2 attacks (DHCP snooping, DAI)
  - automation / "Automation & Programmability": SDN controllers, REST APIs, JSON data, configuration management basics
- Use REAL Cisco IOS commands in evidence/labs (enable, configure terminal, show ip interface brief, show ip route, ip route, router ospf, network, interface vlan, switchport mode trunk...). Verify syntax carefully.
- foundations: subnetting refresher (REQUIRED)
- terminal missions: IOS command drills (show commands, configuring interfaces/VLANs/OSPF in the simulated terminal)

### 5. isc2-cc — ISC2 Certified in Cybersecurity
- title: "ISC2 Certified in Cybersecurity", tagline: "CC: security principles, access control, incident response"
- vendor: {"name": "ISC2", "certs": "Certified in Cybersecurity (CC)", "docs": "https://www.isc2.org/certifications/cc"}
- accent: "#35c48d", simulation: {"items": 40, "minutes": 60}
- domains:
  - principles / "Security Principles": CIA triad, risk concepts, authentication (MFA, SSO), cryptography basics, IAM
  - bcdr / "Business Continuity & Incident Response": BCP/DRP, backup strategies, incident response lifecycle (prepare/detect/contain/eradicate/recover/lessons)
  - access-control / "Access Control Concepts": DAC/MAC/RBAC, least privilege, separation of duties, physical controls (locks, badges, cameras)
  - network-security / "Network Security": OSI-layer security, firewalls, VPNs, segmentation, wireless security, common network attacks
  - sec-operations / "Security Operations": logging and monitoring, system hardening, security awareness, data handling and classification
- Keep language entry-level (CC is a beginner cert); scenarios should be judgment-oriented.

### 6. m365-endpoint-admin — Microsoft 365 Endpoint Administrator Associate
- title: "Microsoft 365 Endpoint Administrator", tagline: "MD-102: deploy, manage, and protect modern endpoints with Intune"
- vendor: {"name": "Microsoft", "certs": "Endpoint Administrator Associate (MD-102)", "docs": "https://learn.microsoft.com/credentials/certifications/modern-desktop/"}
- accent: "#0078d4", simulation: {"items": 30, "minutes": 45}
- domains:
  - deploy / "Deploy Windows Client": deployment options, Windows Autopilot, provisioning packages, imaging concepts, Windows edition upgrade paths
  - identity / "Manage Identity & Compliance": Microsoft Entra ID, device join types (Entra joined, hybrid), Conditional Access concepts, compliance policies
  - manage-devices / "Manage & Protect Devices": Intune enrollment, configuration profiles, update rings and Windows Update for Business, Microsoft Defender for Endpoint concepts, remote actions (retire/wipe/lock)
  - apps / "Manage Applications": app deployment with Intune (Win32, Store, web), app protection policies, app configuration
- terminal missions: PowerShell-flavored admin reasoning (Get-, Set- cmdlets at concept level), Intune portal navigation decisions

### 7. aws-clf — AWS Certified Cloud Practitioner (ENHANCE IN PLACE)
- Read the existing `/home/hatch/workspace/cert-bootcamps/content/aws-clf.json` FIRST. Preserve ALL
  existing scenarios, lessons, labs, missions, and simulations (do not delete or rewrite them).
- Upgrade additively: (a) set "accent" to "#ff9900" and "simulation" to {"items": 30, "minutes": 45}
  if absent; (b) top up any domain with fewer than 6 scenarios to 6; (c) ensure at least 6 labs
  (add exam-focused ones: shared-responsibility drill, pricing-calculator reasoning, support-plan
  selection); (d) add a "foundations" entry with an exam-strategy refresher (how CLF-C02 is
  structured, time management, eliminating distractors); (e) fix any technical inaccuracy you spot.
- Keep slug "aws-clf", title "AWS Cloud Practitioner", vendor as-is.

### 8. ms-fundamentals — Microsoft Fundamentals (RESTRUCTURE into 4 exam tracks)
- Read the existing `/home/hatch/workspace/cert-bootcamps/content/ms-fundamentals.json` FIRST.
- Restructure its domains into FOUR explicit exam tracks, reusing/adapting existing scenarios where
  they fit and writing new ones to reach 8 scenarios per track (32 total):
  - az-900 / "AZ-900: Azure Fundamentals": cloud concepts, Azure architecture and services (compute, networking, storage), governance, pricing/SLAs
  - ai-900 / "AI-900: Azure AI Fundamentals": ML concepts, computer vision, NLP, conversational AI, responsible AI
  - dp-900 / "DP-900: Azure Data Fundamentals": core data concepts, relational vs non-relational, analytics workloads, Azure data services
  - sc-900 / "SC-900: Security, Compliance & Identity": Zero Trust, identity (Entra ID), Microsoft Defender, compliance and data governance
- Rewrite lessons (one per track), behavioral (8), chat topics (4, ids matching), labs (4-6 across tracks),
  terminalMissions (3-4: Azure CLI-flavored reasoning), simulations (2-3).
- Keep slug "ms-fundamentals", title "Microsoft Fundamentals", vendor as-is; set accent "#00a4ef",
  simulation {"items": 30, "minutes": 45}.

## After writing each file
1. `python3 -c "import json; json.load(open('...'))"` — must parse.
2. Report: slug, scenario count per domain, lesson/behavioral/lab/mission/sim counts, file size.
3. Do NOT edit catalog.json, do NOT run the generator — the coordinator handles build/deploy.

## Style notes
- Titles should be vivid ("The VLAN that leaked") not dry ("VLAN question 3").
- Situations: 1-3 sentences, concrete, workplace-realistic. Prompts: ask for a decision or diagnosis.
- Distractors: plausible mistakes a real learner makes — never joke options, never two correct answers.
- `why`: teach, don't just justify. `hint`: nudge toward the concept.
- Keep each file under ~600KB.
