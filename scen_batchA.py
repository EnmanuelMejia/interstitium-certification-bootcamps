"""Batch A scenarios + lessons for CompTIA Security+ and Network+ CBTs.
Structure: SCENARIOS[cbt][domain] -> list of scenario dicts;
           LESSONS[cbt][domain] -> list of lesson dicts.
Applied additively by cbt_apply.py; IDs use sc8+ numbering to avoid collisions.
"""

SCENARIOS = {
"comptia-security-plus": {
"concepts": [
{
    "id": "secplus-concepts-sc8",
    "title": "Layered Defense for a Small Clinic",
    "domain_id": "concepts",
    "situation": "A 25-person medical clinic has one aging perimeter firewall and nothing else. Last month a receptionist opened a malicious attachment and ransomware encrypted two workstations before IT pulled the network cable. The owner has budget for exactly one security improvement this quarter.",
    "prompt": "Which single investment gives the clinic the best defense-in-depth value for the money?",
    "choices": [
        "Replace the firewall with a top-tier next-generation model",
        "Deploy MFA on all accounts, automated offline backups, and a managed patching cadence",
        "Buy an expensive EDR platform and install it on the two previously infected workstations only",
        "Hire a part-time security guard to watch the server closet"
    ],
    "answer": 1,
    "why": "Defense in depth means layering independent controls so one failure doesn't equal compromise. MFA blocks credential theft, offline backups neutralize ransomware's leverage, and patching closes exploit paths — three layers covering identity, recovery, and prevention. A better firewall is still one layer at one point; the attack last month bypassed the perimeter entirely via email. Guards and partial EDR don't address the actual attack paths.",
    "hint": "The attack came in through email, not through the firewall — where would independent layers have stopped it?",
    "objectives": ["Apply defense-in-depth reasoning", "Compare control categories by attack path"],
    "mins": 12,
    "evidence": ["Selected a layered control set that addresses the actual email-borne attack path"],
},
],
"threats": [
{
    "id": "secplus-threats-sc8",
    "title": "The Urgent Call from 'IT'",
    "domain_id": "threats",
    "situation": "A finance clerk receives a call from someone claiming to be from the company's IT security team. The caller knows her name and manager's name, says her workstation is beaconing to a known malicious server, and urgently needs her to install a 'diagnostic tool' from a link he texts her. She is about to click.",
    "prompt": "What is the most effective control against this specific attack?",
    "choices": [
        "A stronger email spam filter",
        "Endpoint antivirus with real-time protection",
        "A verification procedure: hang up, call the IT help desk on the published internal number, and confirm before acting",
        "Blocking all text-message links on company phones"
    ],
    "answer": 2,
    "why": "This is vishing — voice phishing, a social engineering attack that exploits authority and urgency, not a technical vulnerability. Technical controls can't reliably stop a willing user from installing attacker software, but an out-of-band verification procedure breaks the attacker's core leverage: impersonated authority. Spam filters and AV don't address phone-based social engineering, and blocking SMS links treats a symptom while the same con works over a voice call.",
    "hint": "The attacker's weapon is persuasion over the phone, not malware delivery through a technical channel.",
    "objectives": ["Identify vishing/social engineering", "Select human-layer controls for social attacks"],
    "mins": 10,
    "evidence": ["Chose out-of-band verification as the control against a vishing attack"],
},
],
"architecture": [
{
    "id": "secplus-architecture-sc8",
    "title": "Segmenting the Smart Hospital Wing",
    "domain_id": "architecture",
    "situation": "A hospital wing just deployed 200 IoT devices — infusion pumps, smart thermostats, badge readers — that only the vendor can patch, and several run firmware with known vulnerabilities. They currently sit on the same flat network as nurse workstations and the billing system.",
    "prompt": "What architecture change best reduces risk from these unpatchable devices?",
    "choices": [
        "Give every IoT device a public IP so the vendor can reach them directly for support",
        "Move the IoT devices to an isolated VLAN/segment with strict ACLs allowing only required vendor and monitoring traffic",
        "Install host antivirus on each IoT device",
        "Require nurses to use VPN when accessing the billing system"
    ],
    "answer": 1,
    "why": "Segmentation contains the blast radius: devices that cannot be hardened get network-level containment instead. A dedicated VLAN with deny-by-default ACLs limits lateral movement so a compromised thermostat can't reach billing systems or workstations, while still permitting the few flows the devices genuinely need. Public IPs expand exposure; host AV isn't installable on embedded firmware; nurse VPN does nothing about device-to-device lateral movement on the flat LAN.",
    "hint": "When you can't fix the endpoint, contain it with the network — what's the network-layer way to isolate?",
    "objectives": ["Apply segmentation to unpatchable IoT", "Evaluate lateral-movement controls"],
    "mins": 12,
    "evidence": ["Designed an isolated segment with ACLs to contain vulnerable IoT devices"],
},
],
"operations": [
{
    "id": "secplus-operations-sc8",
    "title": "The Friday-Afternoon Critical Patch",
    "domain_id": "operations",
    "situation": "At 3 PM on a Friday, the vendor publishes a critical remote-code-execution patch for the VPN concentrator that all remote staff use. Active exploitation is reported in the wild. The normal change window is Sunday 2 AM, and the change advisory board won't meet until Monday.",
    "prompt": "What is the correct operational response?",
    "choices": [
        "Wait for the Sunday window and the Monday CAB meeting — process must be followed",
        "Have an engineer patch it immediately with no documentation to save time",
        "Invoke the emergency change process: assess, get expedited approval, patch, and document everything",
        "Disable the VPN entirely until Monday and tell staff to come to the office"
    ],
    "answer": 2,
    "why": "Operations security balances speed and control through the emergency change process — it exists precisely for critical, actively-exploited vulnerabilities where waiting invites compromise. It preserves the key safeguards (impact assessment, approval, rollback plan, documentation) while compressing the timeline. Skipping process entirely removes accountability and rollback safety; waiting leaves a known-exploited remote entry point open all weekend; killing the VPN is a disproportionate availability hit when a controlled emergency patch is available.",
    "hint": "There's a formal process designed exactly for 'patch now, but stay controlled' — which option uses it?",
    "objectives": ["Apply change-management types", "Balance availability vs security under active exploitation"],
    "mins": 10,
    "evidence": ["Selected the emergency change process for an actively exploited critical vulnerability"],
},
],
"governance": [
{
    "id": "secplus-governance-sc8",
    "title": "The Risk the Board Must Own",
    "domain_id": "governance",
    "situation": "A penetration test found the company's legacy order-entry system has unfixable vulnerabilities, but replacing it costs $2M and the business can't operate without it. The security team estimates a 10% annual chance of a breach costing $500K. Leadership asks for a recommendation.",
    "prompt": "What is the correct governance recommendation?",
    "choices": [
        "Accept the risk: document it, apply compensating controls, and get formal sign-off from senior leadership",
        "Quietly ignore the finding since the system can't be replaced anyway",
        "Have the security analyst sign the risk acceptance on behalf of the company",
        "Buy a $50K firewall and declare the risk mitigated"
    ],
    "answer": 0,
    "why": "Risk acceptance is a legitimate strategy, but governance requires it to be explicit, documented, owned at the right level, and paired with compensating controls (monitoring, segmentation, backups) that reduce likelihood or impact. A $50K expected annual loss ($500K x 10%) may rationally be cheaper than a $2M replacement — but only senior leadership can own that business decision, never the analyst, and never silently. Declaring a firewall 'mitigates' unfixable app flaws misrepresents residual risk to decision-makers.",
    "hint": "Risk acceptance is valid — but who must own it, and what must accompany it?",
    "objectives": ["Apply risk treatment options", "Identify proper risk ownership and documentation"],
    "mins": 12,
    "evidence": ["Recommended documented risk acceptance with compensating controls and executive sign-off"],
},
],
"systems-anatomy": [
{
    "id": "secplus-systems-anatomy-sc8",
    "title": "Kerberos: Where the Ticket Breaks",
    "domain_id": "systems-anatomy",
    "situation": "Users in a branch office suddenly can't access any file shares. They can log in to their workstations, ping the file server, and resolve its name — but every share access fails with an authentication error. The branch's link to headquarters, where the domain controllers live, went down 30 minutes ago and just came back up.",
    "prompt": "Walking the Kerberos flow as a system, where is the failure?",
    "choices": [
        "The file server's disk — authentication errors mean the data is unreachable",
        "The client can't reach a KDC to get a service ticket, so it has no valid ticket to present to the file server",
        "DNS is broken, so the workstation can't find the file server",
        "The user's password expired during the outage"
    ],
    "answer": 1,
    "why": "Kerberos is a ticket-based journey: the client first contacts the KDC (AS exchange for a TGT, then TGS exchange for a service ticket) and only then presents the service ticket to the file server. Login worked because cached credentials allow local logon, and ping/DNS work because those don't need Kerberos — but every new service ticket request fails without KDC reachability. The system view pinpoints the break at the ticket-granting step, not at the server or the password.",
    "hint": "Trace the journey: before the client ever talks to the file server, who must it talk to first?",
    "objectives": ["Trace the Kerberos ticket flow", "Isolate failures by system step"],
    "mins": 14,
    "evidence": ["Located an authentication failure at the KDC ticket-granting step of the Kerberos flow"],
},
{
    "id": "secplus-systems-anatomy-sc9",
    "title": "Packet Journey Through the Firewall",
    "domain_id": "systems-anatomy",
    "situation": "A web server in the DMZ needs to pull updates from the internet, and internal users need to reach it on HTTPS. The firewall admin wrote the rules top-down: (1) deny all, (2) allow internal-to-DMZ 443, (3) allow DMZ-to-internet 80/443. Return traffic for the update downloads is being dropped.",
    "prompt": "Following the packet's journey through the firewall as a system, what is wrong?",
    "choices": [
        "Rule 3's ports are wrong — updates need port 22",
        "The deny-all rule is first, so nothing below it is ever evaluated",
        "The firewall has no stateful inspection handling, so return traffic has no matching allow rule",
        "The DMZ server needs a public IP address"
    ],
    "answer": 2,
    "why": "A firewall processes each packet as a journey: ingress interface → rule evaluation top-down → state table check → NAT → egress. Stateful inspection automatically permits return traffic for established sessions, but if this firewall is evaluating statelessly (or the state engine isn't engaged), the inbound SYN-ACK from the update server hits the rule base as a new connection and dies at 'deny all'. The fix is stateful handling (or explicit return rules), not port or addressing changes — and rule order matters, but 'deny all' belongs at the END, while here the scenario states it's listed first as the design, which combined with no statefulness kills return traffic.",
    "hint": "The outbound SYN leaves fine, but the reply SYN-ACK arrives as a stranger — what firewall feature normally recognizes it?",
    "objectives": ["Trace packet flow through firewall processing", "Apply stateful inspection and rule-order logic"],
    "mins": 14,
    "evidence": ["Diagnosed dropped return traffic as a stateful-inspection gap in the firewall packet journey"],
},
{
    "id": "secplus-systems-anatomy-sc10",
    "title": "VPN Tunnel Anatomy: Phase 1 Up, Phase 2 Down",
    "domain_id": "systems-anatomy",
    "situation": "A site-to-site IPsec VPN between headquarters and a new branch shows Phase 1 (IKE) as established, but no traffic passes and Phase 2 never completes. Both sides insist their configuration is correct. The branch admin mentions they 'hardened' their crypto settings last week.",
    "prompt": "As a system, where do you look first?",
    "choices": [
        "The physical WAN link — Phase 1 must be a false positive",
        "Compare Phase 2 proposals: encryption, integrity, DH group, and lifetimes must match on both sides",
        "Reboot both VPN gateways to clear the SA table",
        "Increase the Phase 1 lifetime so the tunnel stays up longer"
    ],
    "answer": 1,
    "why": "An IPsec tunnel is a two-phase system: Phase 1 (IKE) builds the secure management channel, Phase 2 (IPsec SAs) negotiates the actual data-protection parameters. Phase 1 succeeding proves connectivity and peer authentication work — the break is inside the Phase 2 negotiation, where mismatched proposals (AES-256 vs AES-128, SHA-256 vs SHA-1, DH group, lifetimes, or proxy IDs/traffic selectors) cause the negotiation to fail. The branch's 'hardening' very likely changed one side's proposal set. Reboots and lifetimes don't fix a parameter mismatch.",
    "hint": "Phase 1 is the handshake about HOW to talk securely; Phase 2 negotiates the actual data protection — which negotiation is failing, and what must both sides agree on?",
    "objectives": ["Distinguish IKE Phase 1 vs Phase 2", "Troubleshoot proposal mismatches"],
    "mins": 14,
    "evidence": ["Isolated a VPN failure to mismatched Phase 2 proposals after successful Phase 1"],
},
{
    "id": "secplus-systems-anatomy-sc11",
    "title": "DNS Resolution Chain: The Poisoned Step",
    "domain_id": "systems-anatomy",
    "situation": "Employees report that the company's banking portal intermittently loads a convincing fake login page. The real site's certificate is valid and the bank confirms no compromise. Internal DNS servers forward to the ISP resolver, and the fake page appears for about an hour at a time, then disappears.",
    "prompt": "Walking the DNS resolution chain, what best explains the symptom?",
    "choices": [
        "The bank's authoritative DNS server was hacked permanently",
        "A cache-poisoning attack on a resolver in the chain injected a bogus record with a TTL of about an hour",
        "Employees' browsers have a malicious extension rewriting the page",
        "The company's firewall is redirecting HTTPS traffic"
    ],
    "answer": 1,
    "why": "DNS resolution is a chain: client → local resolver → (forwarders) → root → TLD → authoritative, with caching at each hop. Cache poisoning injects a forged answer into one resolver's cache, and the lie persists exactly until the record's TTL expires — matching the 'about an hour, then disappears' pattern. A hacked authoritative server wouldn't self-heal hourly; a browser extension wouldn't be intermittent across many users; and a firewall redirect would break the valid certificate (TLS would warn). The TTL-bound intermittence is the signature of a poisoned cache entry aging out.",
    "hint": "What DNS mechanism makes a lie temporary — lasting a fixed time, then vanishing on its own?",
    "objectives": ["Trace the DNS resolution chain", "Recognize cache-poisoning symptoms and TTL behavior"],
    "mins": 14,
    "evidence": ["Attributed intermittent DNS redirection to cache poisoning via TTL-bound symptom analysis"],
},
{
    "id": "secplus-systems-anatomy-sc12",
    "title": "SOC Alert Pipeline: From Log to Analyst",
    "domain_id": "systems-anatomy",
    "situation": "A SOC manager complains analysts are drowning: 40,000 alerts a day, most never reviewed. The pipeline is: endpoints/servers forward logs → SIEM ingests → correlation rules fire → every rule hit creates a ticket → analysts work the queue oldest-first.",
    "prompt": "Where is the highest-leverage fix in this pipeline as a system?",
    "choices": [
        "Hire more analysts to work the queue faster",
        "Tune and tier the pipeline: suppress known-benign patterns, deduplicate, enrich with asset/threat intel, and risk-score before ticket creation",
        "Forward more log sources into the SIEM for better visibility",
        "Work the queue newest-first instead of oldest-first"
    ],
    "answer": 1,
    "why": "The pipeline's bottleneck isn't analyst speed — it's that raw rule hits flow straight to humans with no signal processing. The highest-leverage fix sits between detection and ticketing: tuning out false positives, deduplicating repeat hits, enriching with context (is this a crown-jewel server? does threat intel flag the IOC?), and risk-scoring so analysts see the 200 alerts that matter instead of 40,000 undifferentiated ones. More analysts or more logs just scale the noise; queue order doesn't change the signal-to-noise ratio.",
    "hint": "40,000 tickets a day means the problem is upstream of the analysts — what stage turns raw detections into workable signal?",
    "objectives": ["Map the SOC alert pipeline", "Apply tuning/enrichment to reduce alert fatigue"],
    "mins": 14,
    "evidence": ["Redesigned the alert pipeline with tuning, dedup, enrichment, and risk scoring before ticketing"],
},
{
    "id": "secplus-systems-anatomy-sc13",
    "title": "Incident Response as a Feedback System",
    "domain_id": "systems-anatomy",
    "situation": "A company has handled three separate phishing-to-ransomware incidents in six months. Each time the IR team contained and recovered well, but the same entry vector keeps working. The CISO asks why incidents keep recurring despite good response.",
    "prompt": "Viewing IR as a system, what is broken?",
    "choices": [
        "The containment phase — they should isolate faster",
        "The lessons-learned phase isn't feeding back into prevention: findings aren't becoming new controls, training, or detection rules",
        "The eradication phase — malware keeps surviving",
        "They need a bigger IR team"
    ],
    "answer": 1,
    "why": "Incident response is a closed-loop system: preparation → detection → containment → eradication → recovery → lessons learned → back into preparation. When the loop is open — lessons learned produces a report that nobody converts into hardened email filtering, phishing simulations, MFA enforcement, or new SIEM rules — each incident is handled well but the system never learns, so the same attack re-enters. Faster containment or more staff improves the response without changing the recurrence; the missing feedback arrow is the defect.",
    "hint": "Good response, same incident three times — which IR phase is supposed to make the NEXT attack harder?",
    "objectives": ["Model IR as a feedback loop", "Connect lessons-learned to control improvement"],
    "mins": 14,
    "evidence": ["Identified the broken lessons-learned feedback loop behind recurring incidents"],
},
],
"exam-strategy": [
{
    "id": "secplus-exam-strategy-sc8",
    "title": "The 90-Minute Budget",
    "domain_id": "exam-strategy",
    "situation": "You sit down for Security+: up to 90 questions in 90 minutes, including several performance-based questions (PBQs) that each can take 5-10 minutes. Twenty minutes in, you've answered 12 questions and are stuck on a tricky log-analysis PBQ.",
    "prompt": "What is the best time-management move right now?",
    "choices": [
        "Finish the PBQ no matter what — it's worth more points",
        "Flag the PBQ, move on, and answer all multiple-choice first; return to PBQs with remaining time",
        "Rush through the next 20 questions to catch up",
        "Skip every PBQ entirely and focus on multiple choice"
    ],
    "answer": 1,
    "why": "PBQs are time-expensive but not worth sacrificing dozens of multiple-choice questions you can answer quickly — each unanswered question is a guaranteed zero. The winning strategy is two passes: sweep the multiple-choice (roughly a minute each) to bank points, then spend remaining time on PBQs where partial credit is possible. Rushing creates careless errors on easy points, and skipping PBQs abandons partial-credit opportunities. Flag-and-return keeps both point sources alive.",
    "hint": "Every blank answer scores zero — which approach banks the most certain points first?",
    "objectives": ["Apply exam time budgeting", "Sequence PBQs vs multiple-choice"],
    "mins": 10,
    "evidence": ["Applied a two-pass time strategy that prioritizes bankable multiple-choice points"],
},
{
    "id": "secplus-exam-strategy-sc9",
    "title": "Attacking a Firewall-Rule PBQ",
    "domain_id": "exam-strategy",
    "situation": "A PBQ shows a network diagram and asks you to drag firewall rules into the correct order to allow web traffic to a DMZ server while blocking everything else. There are six rule tiles and the interface is unfamiliar.",
    "prompt": "What is the best approach to this PBQ?",
    "choices": [
        "Place the rules in the order that 'looks right' and submit quickly to save time",
        "Read the goal first, identify the required allows, put the specific allows before the final deny-all, then verify each traffic flow against your ordering",
        "Put deny-all first to be safe, then the allow rules",
        "Skip it — PBQs are experimental and don't count"
    ],
    "answer": 1,
    "why": "PBQs reward method: state the goal, translate it into rule logic (firewalls evaluate top-down, first match wins), place specific allows before the terminal deny-all, then mentally test each required flow — 'does HTTPS from internet reach the DMZ? does anything else get through?' Deny-first blocks everything below it; 'looks right' wastes the partial credit these questions offer; and PBQs absolutely count. The verification pass is what converts a guess into points.",
    "hint": "Firewalls read rules top-down, first match wins — how must allows and the final deny be ordered?",
    "objectives": ["Apply PBQ methodology", "Order firewall rules correctly"],
    "mins": 12,
    "evidence": ["Constructed and verified a top-down firewall rule ordering in a PBQ"],
},
{
    "id": "secplus-exam-strategy-sc10",
    "title": "Elimination Under Pressure",
    "domain_id": "exam-strategy",
    "situation": "Question 47: 'Which control BEST mitigates credential theft via phishing?' The options are: A) Annual security awareness training, B) Mandatory MFA on all remote access, C) A stronger password complexity policy, D) Quarterly phishing simulations. You're unsure between two of them with 40 seconds left.",
    "prompt": "What is the best elimination reasoning?",
    "choices": [
        "Pick the longest answer — longest is usually correct",
        "Eliminate C (passwords don't stop phishing credential reuse well) and A/D (awareness helps but is weaker than a technical control), leaving B — MFA neutralizes stolen credentials",
        "Pick A because training is the cheapest control",
        "Choose randomly — all four sound plausible"
    ],
    "answer": 1,
    "why": "Elimination works by comparing control strength against the threat mechanism: phishing steals credentials, and MFA makes stolen credentials insufficient — a technical control that directly breaks the attack chain. Complexity policies don't stop harvested passwords from being reused; awareness training and simulations reduce click rates but never to zero, making them weaker 'best' answers. The exam constantly asks for the BEST/MOST effective control, which usually means the technical control that neutralizes the mechanism, not the cheapest or most educational one.",
    "hint": "The question asks what BEST mitigates stolen credentials — which option makes a stolen password useless?",
    "objectives": ["Apply elimination strategy", "Rank controls by mechanism effectiveness"],
    "mins": 10,
    "evidence": ["Eliminated weaker controls to select the mechanism-neutralizing answer"],
},
{
    "id": "secplus-exam-strategy-sc11",
    "title": "Flag, Don't Sink",
    "domain_id": "exam-strategy",
    "situation": "Question 23 describes a complex multi-site VPN and PKI scenario with a long paragraph. You've read it twice and still can't pin down what's being asked. The clock shows you've spent 3 minutes on it.",
    "prompt": "What should you do?",
    "choices": [
        "Read it a third time carefully — understanding will come",
        "Flag it, pick your best guess for now, move on, and return with fresh eyes if time remains",
        "Leave it blank and come back — a blank is better than a wrong guess",
        "Ask the proctor for clarification on the scenario"
    ],
    "answer": 1,
    "why": "Three minutes on one question is a budget emergency: at that burn rate you forfeit multiple easier questions. Flag-and-guess preserves the possibility of points (there's no penalty for wrong answers) while freeing you to bank certain points elsewhere; returning later often unlocks the question because subsequent questions prime relevant concepts. Leaving it blank guarantees zero, re-reading under stress rarely helps, and proctors can't explain content.",
    "hint": "No penalty for wrong answers, and every minute has an opportunity cost — what preserves both?",
    "objectives": ["Apply flag-and-review discipline", "Manage per-question time budget"],
    "mins": 8,
    "evidence": ["Flagged a time-sink question with a provisional answer instead of burning the time budget"],
},
{
    "id": "secplus-exam-strategy-sc12",
    "title": "Parsing the Scenario Question",
    "domain_id": "exam-strategy",
    "situation": "A question gives you a half-page scenario: company size, industry, three systems, two recent incidents, a budget constraint, and a compliance requirement. The final sentence asks: 'Which of the following should the analyst do FIRST?'",
    "prompt": "What is the most reliable parsing technique?",
    "choices": [
        "Memorize every detail in the paragraph before looking at the options",
        "Read the final question sentence first, identify the action word (FIRST/NEXT/BEST), then scan the scenario only for facts relevant to sequencing",
        "Pick the answer mentioning the compliance requirement — compliance always wins",
        "Choose the most technically advanced option"
    ],
    "answer": 1,
    "why": "Scenario questions bury the actual task in context — the final sentence defines it. Reading it first tells you what to hunt for: 'FIRST' means sequencing/triage logic (contain before eradicate, identify before contain), so you scan for facts that order actions and ignore decorative detail. Compliance and advanced tech are classic distractors that feel important but don't answer 'what comes first in the workflow.' Question-first parsing cuts through the noise reliably.",
    "hint": "The last sentence is the real question — what does the word FIRST tell you to look for?",
    "objectives": ["Parse scenario questions efficiently", "Recognize sequencing keywords"],
    "mins": 10,
    "evidence": ["Used question-first parsing to isolate the sequencing task in a scenario question"],
},
{
    "id": "secplus-exam-strategy-sc13",
    "title": "Spotting the Distractor Pattern",
    "domain_id": "exam-strategy",
    "situation": "Four answer choices for an incident-response question: A) 'Immediately wipe and rebuild all 500 workstations,' B) 'Isolate affected hosts and preserve volatile memory for analysis,' C) 'Ignore the alert; it's probably a false positive,' D) 'Shut down the entire corporate network.'",
    "prompt": "Which pattern identifies the distractors here?",
    "choices": [
        "The correct answer is always the middle option",
        "Extreme, absolute, or disproportionate actions (wipe everything, shut down everything, ignore entirely) are classic distractors; the measured, procedural option is usually correct",
        "The longest option is always the distractor",
        "Options with technical terms are distractors"
    ],
    "answer": 1,
    "why": "CompTIA distractors follow patterns: absolutes ('always,' 'never,' 'all,' 'immediately wipe everything') and disproportionate responses signal wrong answers, because real security practice is measured and procedural. Option B follows the actual IR sequence — contain, preserve evidence — while A and D nuke availability for no reason and C abandons duty of care. Recognizing the 'extreme action' pattern lets you eliminate two or three options in seconds, even when you're unsure of the exact right answer.",
    "hint": "Which options nuke everything or do nothing — and what does real incident response actually look like?",
    "objectives": ["Recognize distractor patterns", "Apply proportionality reasoning"],
    "mins": 8,
    "evidence": ["Eliminated extreme-action distractors to identify the procedural IR answer"],
},
{
    "id": "secplus-exam-strategy-sc14",
    "title": "Test-Day Final Decisions",
    "domain_id": "exam-strategy",
    "situation": "You've finished all 90 questions with 12 minutes left. You flagged 8 questions. On review, one flagged answer 'feels' wrong but you can't articulate why, and another you now think you misread.",
    "prompt": "What is the evidence-based review strategy?",
    "choices": [
        "Change every flagged answer — first instincts are usually wrong",
        "Never change any answer — first instincts are usually right",
        "Change only answers where re-reading reveals a concrete misread or new understanding; leave 'feels wrong' gut changes alone",
        "Submit immediately — reviewing only causes second-guessing"
    ],
    "answer": 2,
    "why": "Research on answer-changing shows changes help when driven by new information (you misread 'FIRST' as 'BEST,' you recall the port number correctly on second thought) and hurt when driven by anxiety alone. The disciplined rule: re-read each flagged question fully, change only if you can state the specific reason, and use remaining time to verify you answered every question rather than churning guesses. Abandoning review wastes the easiest points on the exam — catching misreads.",
    "hint": "Gut feelings mislead; concrete re-reads don't — what distinguishes a good change from a bad one?",
    "objectives": ["Apply evidence-based answer review", "Use remaining time effectively"],
    "mins": 8,
    "evidence": ["Changed only answers with a concrete, articulable reason during review"],
},
],
"soc-playbook": [
{
    "id": "secplus-soc-playbook-sc8",
    "title": "Triage: Which Alert Burns First",
    "domain_id": "soc-playbook",
    "situation": "Monday 8 AM, the queue holds: (1) critical-severity malware alert on a receptionist's PC, (2) medium-severity 'impossible travel' login for the CFO's account, (3) high-severity port scan against a DMZ web server, (4) critical-severity alert for Mimikatz-like behavior on a domain controller.",
    "prompt": "In what order should the analyst triage these?",
    "choices": [
        "1, 3, 4, 2 — work criticals first in arrival order",
        "4, 2, 1, 3 — domain controller compromise and executive account takeover outrank workstation malware and noisy scans",
        "3, 1, 2, 4 — external-facing issues first",
        "2, 4, 3, 1 — user accounts before systems"
    ],
    "answer": 1,
    "why": "Triage ranks by blast radius and asset criticality, not raw severity or arrival order. A domain controller showing credential-dumping behavior threatens the entire identity infrastructure — that's an enterprise-wide compromise in progress. The CFO's impossible-travel login suggests executive account takeover with access to sensitive data. Workstation malware is contained to one host; port scans against a DMZ are constant background noise. Severity labels without asset and impact context mislead; triage must weigh what falls if the alert is real.",
    "hint": "Forget the severity labels for a moment — if each alert is real, which one costs the company the most?",
    "objectives": ["Prioritize alerts by impact and asset criticality", "Look past raw severity scores"],
    "mins": 12,
    "evidence": ["Triaged a mixed alert queue by blast radius, ranking DC compromise first"],
},
{
    "id": "secplus-soc-playbook-sc8b",
    "title": "Escalation: L1 to Incident Response",
    "domain_id": "soc-playbook",
    "situation": "An L1 analyst sees an alert: PowerShell downloading an encoded payload on an HR workstation, followed by outbound connections to an unknown external IP. The user says they 'just opened a resume.' The playbook says L1 can handle isolated adware, but must escalate suspected command-and-control.",
    "prompt": "What is the correct escalation decision?",
    "choices": [
        "Close it as user-initiated adware — the user admitted opening the file",
        "Escalate to L2/IR immediately: encoded PowerShell plus outbound C2-like connections meets the escalation criterion regardless of the user's story",
        "Quarantine the host and wait to see if more alerts fire before escalating",
        "Email the user asking them not to open resumes anymore"
    ],
    "answer": 1,
    "why": "Escalation criteria exist so L1 doesn't have to be certain — the pattern (encoded PowerShell download + external beaconing) matches the playbook's C2 definition, and user explanations never override technical indicators (attackers rely on exactly this social cover). Waiting for more alerts gives the adversary dwell time to move laterally. The analyst's job is to recognize the pattern matches the escalation threshold and hand off with full context, not to investigate to certainty alone.",
    "hint": "The playbook defines what gets escalated — does this pattern match it, no matter what the user says?",
    "objectives": ["Apply escalation criteria", "Distinguish L1 containment from IR handoff"],
    "mins": 10,
    "evidence": ["Escalated a C2-pattern alert to IR per playbook criteria despite user explanation"],
},
{
    "id": "secplus-soc-playbook-sc9",
    "title": "SIEM Query: Hunting Lateral Movement",
    "domain_id": "soc-playbook",
    "situation": "Threat intel reports a group that, after initial access, moves laterally using SMB and WMI with stolen credentials, typically within 2 hours of landing. The SOC lead asks you to write a hunt query covering the last 7 days.",
    "prompt": "What query logic best hunts this behavior?",
    "choices": [
        "Search all firewall logs for any blocked outbound traffic in the last 7 days",
        "Correlate: successful logons (event 4624, type 3/10) to a host, followed within 2 hours by that same account making SMB (445) or WMI (135) connections to additional hosts it never touched before",
        "Alert on every PowerShell execution across the fleet",
        "Search email gateways for phishing lures from the last 7 days"
    ],
    "answer": 1,
    "why": "Threat hunting translates adversary behavior into log correlation: the intel gives you the technique (SMB/WMI lateral movement), the timing (within 2 hours), and the anomaly (new host-to-host paths). A good hunt query joins authentication logs with network connection logs on account + time window + first-seen host pairs — that finds the behavior whether or not any signature fired. Firewall blocks and blanket PowerShell alerts are too noisy or miss the point; email lures hunt the wrong phase (initial access, not lateral movement).",
    "hint": "The intel describes a sequence: logon, then new connections, within a time window — what logs, joined how, would reveal that sequence?",
    "objectives": ["Build hypothesis-driven SIEM correlations", "Map intel to log sources"],
    "mins": 14,
    "evidence": ["Wrote a correlated hunt query for SMB/WMI lateral movement within a 2-hour window"],
},
{
    "id": "secplus-soc-playbook-sc10",
    "title": "Ticket Prioritization Matrix",
    "domain_id": "soc-playbook",
    "situation": "Two tickets land simultaneously. Ticket A: ransomware detected on a single kiosk PC in the lobby (low business value, isolated VLAN). Ticket B: suspicious OAuth consent grants on the CEO's mailbox (no malware, but potential email takeover). The SLA matrix scores impact x urgency.",
    "prompt": "How should they be prioritized?",
    "choices": [
        "Ticket A first — ransomware is always the top priority word",
        "Ticket B first — a mailbox takeover of the CEO has far higher impact (fraud, data theft, reputation) even without malware",
        "Work both simultaneously — priority matrices don't apply to security",
        "Ticket A first — it has the scarier alert name"
    ],
    "answer": 1,
    "why": "The impact x urgency matrix exists precisely to defeat scary-word bias. Ticket A's blast radius is one isolated, low-value kiosk — high urgency word, low actual impact. Ticket B threatens the CEO's entire communications, enabling wire fraud, sensitive data access, and reputational damage — high impact even at moderate urgency. Prioritization must score the business consequence of the alert being real, not react to the alert's vocabulary.",
    "hint": "Score each ticket: if real, what does the business actually lose?",
    "objectives": ["Apply impact-urgency prioritization", "Resist alert-vocabulary bias"],
    "mins": 10,
    "evidence": ["Prioritized a CEO mailbox-takeover ticket over isolated kiosk ransomware via impact scoring"],
},
{
    "id": "secplus-soc-playbook-sc11",
    "title": "The Shift Handoff Note",
    "domain_id": "soc-playbook",
    "situation": "Your 12-hour SOC shift ends. During it you: triaged 60 alerts, escalated one possible C2 case (host isolated, IR engaged, awaiting forensics), tuned a noisy rule, and noticed a slow uptick in failed VPN logins from one country that hasn't crossed any threshold yet.",
    "prompt": "What belongs in the handoff note to the next shift?",
    "choices": [
        "A full list of all 60 alerts triaged, in order",
        "The escalated C2 case status and next expected action, the rule tuned (so they know alert volume changed), and the VPN-login uptick as a watch item with the current count",
        "Just the C2 escalation — everything else is routine",
        "Nothing — the ticketing system has it all"
    ],
    "answer": 1,
    "why": "A handoff transfers state the next analyst can't reconstruct: open investigations and their pending next steps, environmental changes (a tuned rule changes what the queue looks like — without this note the next shift misreads volume changes), and sub-threshold trends that only become visible across shifts. A 60-alert dump is noise; 'nothing' assumes the next analyst will discover the trend from scratch; C2-only omits the context that prevents tomorrow's miss. Good handoffs carry open loops, changed baselines, and emerging patterns.",
    "hint": "What would the next analyst need to know that they can't figure out from the ticket queue alone?",
    "objectives": ["Write effective SOC handoffs", "Track sub-threshold trends across shifts"],
    "mins": 10,
    "evidence": ["Wrote a handoff covering open escalation, baseline change, and a sub-threshold trend"],
},
{
    "id": "secplus-soc-playbook-sc12",
    "title": "Tuning the Noisy Rule",
    "domain_id": "soc-playbook",
    "situation": "A SIEM rule 'Mass file encryption detected' fires 300 times a day — 299 are the backup agent compressing archives at 2 AM, and 1 last month was real ransomware caught late because analysts had muted the rule's notifications out of fatigue.",
    "prompt": "What is the correct tuning action?",
    "choices": [
        "Delete the rule — it's 99.7% false positives",
        "Keep the rule as-is and tell analysts to pay more attention",
        "Tune the rule: exclude the known backup agent process/path, add a velocity or entropy threshold, and keep alerting on the remainder",
        "Lower the rule's severity so it stops paging anyone"
    ],
    "answer": 2,
    "why": "False-positive tuning is surgery, not amputation: the rule detects a genuinely critical behavior, so deleting it blinds you to ransomware, and muting it (what analysts did informally) caused the late catch. The fix adds context the rule lacks — allowlist the known-good backup process, require stronger signals (encryption velocity, entropy, mass extension renames) — so the 299 benign firings stop and the 1 real one pages loudly. Severity-lowering without tuning just changes which queue the noise lands in.",
    "hint": "The rule's logic is right but too broad — how do you keep the detection while removing the known-benign pattern?",
    "objectives": ["Tune detection rules", "Distinguish tuning from disabling"],
    "mins": 12,
    "evidence": ["Tuned a noisy ransomware rule with allowlisting and thresholds instead of disabling it"],
},
{
    "id": "secplus-soc-playbook-sc13",
    "title": "Threat Hunting Hypothesis",
    "domain_id": "soc-playbook",
    "situation": "Your threat intel feed reports a ransomware affiliate targeting healthcare, entering via exposed RDP, then disabling backup services before encrypting. Your hospital has RDP exposed on two jump hosts 'temporarily' for a vendor, and backups run nightly.",
    "prompt": "What is the best-structured hunt hypothesis?",
    "choices": [
        "Search for ransomware — it's the biggest threat",
        "Hypothesis: the affiliate is already inside via the exposed RDP jump hosts; hunt for RDP logons from unusual sources followed by backup-service tampering (event logs for stopped VSS/backup services) on servers",
        "Block RDP at the firewall and consider the hunt done",
        "Scan the whole network for malware signatures"
    ],
    "answer": 1,
    "why": "Hypothesis-driven hunting starts from intel + your own exposure and predicts the adversary's observable steps: IF they're inside via our known-exposed RDP, THEN we'd see anomalous RDP logons followed by backup tampering (their pre-encryption ritual). That gives you specific logs to query (RDP 4624s, service-stop events) and a falsifiable outcome. 'Search for ransomware' is unfocused; blocking RDP is remediation, not hunting (and doesn't tell you if they're already in); signature scanning hunts tools, not the described behavior chain.",
    "hint": "A good hypothesis names the entry point you actually have exposed and the observable steps the intel says come next.",
    "objectives": ["Form hypothesis-driven hunts", "Map intel TTPs to log evidence"],
    "mins": 12,
    "evidence": ["Built a falsifiable hunt hypothesis linking exposed RDP to backup-tampering indicators"],
},
],
"crypto-lab": [
{
    "id": "secplus-crypto-lab-sc8",
    "title": "Killing Old TLS",
    "domain_id": "crypto-lab",
    "situation": "A vulnerability scan flags the company's public web servers for supporting TLS 1.0 and 1.1. The e-commerce team worries that disabling them will break old customer browsers, but the compliance team says auditors will fail them if the protocols stay enabled.",
    "prompt": "What is the correct decision?",
    "choices": [
        "Keep TLS 1.0/1.1 enabled — customer compatibility comes first",
        "Disable TLS 1.0 and 1.1, keep TLS 1.2 and 1.3; publish a deprecation notice and monitor handshake failures for genuinely affected clients",
        "Disable all TLS and switch the site to plain HTTP for maximum compatibility",
        "Enable SSL 3.0 as a fallback for the oldest clients"
    ],
    "answer": 1,
    "why": "TLS 1.0 and 1.1 are deprecated (RFC 8996) with known vulnerabilities like BEAST, and PCI DSS requires 1.2+ — keeping them fails audits and exposes customers. TLS 1.2 (properly configured) and 1.3 cover effectively all modern clients; the compatibility risk is real but measurable, so you deprecate with notice and monitor rather than guessing. Plain HTTP or SSL 3.0 (POODLE) would be catastrophic downgrades. Crypto decisions weigh protocol security against measured — not feared — compatibility impact.",
    "hint": "Two of these protocol versions are formally deprecated and audit-failing — which ones, and what's the safe floor?",
    "objectives": ["Select appropriate TLS versions", "Balance deprecation with compatibility"],
    "mins": 12,
    "evidence": ["Chose to disable TLS 1.0/1.1 while retaining 1.2/1.3 with monitored deprecation"],
},
{
    "id": "secplus-crypto-lab-sc9",
    "title": "The Certificate Name Mismatch",
    "domain_id": "crypto-lab",
    "situation": "After a website migration, users get browser warnings: 'certificate name mismatch.' The certificate is valid, unexpired, issued by a trusted public CA — but it was issued for shop.example.com while the site now also serves customers at store.example.com.",
    "prompt": "What is the correct fix?",
    "choices": [
        "Tell users to click through the warning — the certificate is valid",
        "Reissue the certificate with a Subject Alternative Name (SAN) covering both shop.example.com and store.example.com",
        "Disable HTTPS on store.example.com to stop the warnings",
        "Install the same certificate on more servers"
    ],
    "answer": 1,
    "why": "TLS clients validate that the certificate's subject matches the hostname in the URL bar — the modern mechanism is the Subject Alternative Name extension, which can list multiple DNS names on one certificate. A name mismatch means the presented identity doesn't match the requested site, and training users to click through destroys the entire authentication value of TLS (attackers rely on exactly that habit). Reissuing with proper SANs is the fix; disabling HTTPS or duplicating the wrong cert doesn't address the identity mismatch.",
    "hint": "The certificate proves identity — but for which name? What certificate field lists all the names it covers?",
    "objectives": ["Troubleshoot certificate validation errors", "Apply SAN concepts"],
    "mins": 10,
    "evidence": ["Diagnosed a name-mismatch warning and prescribed SAN reissuance"],
},
{
    "id": "secplus-crypto-lab-sc10",
    "title": "Keys After the Admin Leaves",
    "domain_id": "crypto-lab",
    "situation": "The sole systems administrator — who personally generated and held the company's disk-encryption recovery keys, the CA's offline root key passphrase, and several service-account API keys — resigns abruptly on bad terms. Nothing appears compromised, but he had full access until his last day.",
    "prompt": "What is the correct key-management response?",
    "choices": [
        "Do nothing — there's no evidence of compromise",
        "Rotate all keys and credentials he could have accessed or copied: reissue API keys, rotate service passwords, re-key encryption where feasible, and change CA operational credentials under dual control",
        "Just disable his user account",
        "Change only the keys he explicitly asks about in the exit interview"
    ],
    "answer": 1,
    "why": "Key management treats privileged departure as a compromise of key confidentiality by default: keys he held must be considered known to him, and 'no evidence of misuse' is not evidence of safety. Rotation must be comprehensive (everything he touched, not just what he mentions) and the new key custody must enforce separation of duties — no more single-person key holdings, with the root CA key under dual control in an HSM or safe. Disabling the account stops future logins but does nothing about keys already in his possession.",
    "hint": "He doesn't need his account to use a copied key — what does that imply about which keys are still trustworthy?",
    "objectives": ["Apply key rotation on personnel change", "Enforce separation of duties in key custody"],
    "mins": 12,
    "evidence": ["Ordered comprehensive key rotation and dual-control custody after privileged departure"],
},
{
    "id": "secplus-crypto-lab-sc11",
    "title": "Hashing: Passwords vs File Integrity",
    "domain_id": "crypto-lab",
    "situation": "A developer proposes using SHA-256 for everything: storing user passwords as SHA-256 hashes and verifying software downloads with SHA-256 checksums. A reviewer flags half of this plan.",
    "prompt": "Which half is wrong, and what should replace it?",
    "choices": [
        "Both uses are fine — SHA-256 is secure for everything",
        "Password storage is the problem: fast hashes like SHA-256 fall to GPU brute force, so passwords need a slow, salted KDF like bcrypt/argon2; SHA-256 checksums for file integrity are correct",
        "File integrity is the problem: checksums should use MD5 for speed; password hashing with SHA-256 is fine",
        "Replace both with encryption — hashing is obsolete"
    ],
    "answer": 1,
    "why": "Hashing choices depend on the threat model. Password storage faces offline brute-force attacks where the attacker has the hash — fast hashes (SHA-256 does billions/sec on GPUs) collapse, so you need deliberately slow, salted, memory-hard functions (bcrypt, argon2, PBKDF2) that make each guess expensive. File-integrity verification faces a different threat (detecting tampering), where SHA-256's collision resistance and speed are exactly right. MD5 is broken for integrity (collisions); encryption doesn't replace hashing (different purpose — reversibility vs one-way verification).",
    "hint": "One use case gives the attacker unlimited fast guesses; the other just needs tamper evidence — which needs slowness?",
    "objectives": ["Choose hashing algorithms by use case", "Distinguish KDFs from fast hashes"],
    "mins": 12,
    "evidence": ["Selected bcrypt/argon2 for passwords and SHA-256 for integrity based on threat models"],
},
{
    "id": "secplus-crypto-lab-sc12",
    "title": "Designing the Internal PKI",
    "domain_id": "crypto-lab",
    "situation": "A 500-person company wants an internal PKI for VPN client certs, Wi-Fi (EAP-TLS), and code signing. The proposed design: a single online root CA on a domain-joined server, issuing directly to end users, with the CA admin also approving their own certificate requests.",
    "prompt": "What are the critical design fixes?",
    "choices": [
        "The design is fine — one CA keeps it simple",
        "Take the root CA offline (air-gapped, powered down except for rare signing), use online intermediate CAs for day-to-day issuance, and enforce separation of duties on approvals",
        "Buy public certificates for everything instead",
        "Make the root CA highly available with 99.99% uptime"
    ],
    "answer": 1,
    "why": "PKI security concentrates in the root: whoever controls the root key can mint trusted identities for the entire organization, so the root must be offline (minimizing exposure) with intermediates handling daily issuance (so a compromised intermediate can be revoked without rebuilding trust). Separation of duties prevents a single admin from self-approving fraudulent certs. A public CA can't issue for internal-only names/purposes cost-effectively and outsources your internal trust; high-availability on the root increases its attack surface — the opposite of what's wanted.",
    "hint": "The root key is the crown jewel — should it be online issuing certs daily, or locked away with subordinates doing the work?",
    "objectives": ["Design PKI hierarchy", "Apply root protection and separation of duties"],
    "mins": 14,
    "evidence": ["Redesigned PKI with offline root, intermediates, and separation of duties"],
},
{
    "id": "secplus-crypto-lab-sc13",
    "title": "Encryption at Rest vs in Transit",
    "domain_id": "crypto-lab",
    "situation": "A startup stores customer PII in a cloud database, replicates it to analysts' laptops for reporting, and serves it through a web API. The founder says 'we use HTTPS, so the data is encrypted' and considers the job done.",
    "prompt": "What is the encryption gap analysis?",
    "choices": [
        "HTTPS is sufficient — encryption is encryption",
        "HTTPS covers in-transit only; they also need at-rest encryption (database/volume encryption) and protection for the laptop copies (full-disk encryption, or better: stop replicating PII to laptops)",
        "They need to encrypt the HTTPS traffic a second time",
        "At-rest encryption is unnecessary in the cloud — the provider handles everything"
    ],
    "answer": 1,
    "why": "Encryption has three states and each needs its own control: in-transit (TLS/HTTPS — they have this), at-rest (volume/database encryption for the cloud DB — protects against stolen disks, snapshots, misconfigured storage), and the endpoint copies on laptops, which are the highest-risk state (lost/stolen devices). The founder's mental model covers one of three. The strongest fix for the laptops isn't just FDE — it's eliminating the PII replication entirely (analysts query masked views), removing the risk rather than encrypting it.",
    "hint": "HTTPS protects data moving across the wire — what protects it sitting on the disk, or on a laptop left in a taxi?",
    "objectives": ["Distinguish encryption states", "Apply data minimization to endpoint risk"],
    "mins": 12,
    "evidence": ["Identified missing at-rest and endpoint encryption beyond existing TLS coverage"],
},
{
    "id": "secplus-crypto-lab-sc14",
    "title": "Crypto Agility: The Algorithm Sunset",
    "domain_id": "crypto-lab",
    "situation": "The company's flagship product hardcodes SHA-1 for document signatures and RSA-1024 for license keys deep in the codebase and in shipped client software. Industry bodies have deprecated both, and a major customer now contractually requires SHA-256 minimum and quantum-readiness planning.",
    "prompt": "What is the correct crypto-agility response?",
    "choices": [
        "Do nothing until an actual break is demonstrated — deprecation is theoretical",
        "Patch just the server side to SHA-256 and leave shipped clients as-is",
        "Plan a migration: abstract crypto into a swappable module, ship dual-support (accept old, prefer new) during transition, reissue signatures/keys, and roadmap post-quantum algorithms — treating algorithm agility as an architecture property",
        "Switch everything to a proprietary in-house cipher to avoid standards churn"
    ],
    "answer": 2,
    "why": "Crypto agility is the architectural ability to replace algorithms without rebuilding the product — hardcoded primitives are the anti-pattern that turns every deprecation into a crisis. The migration needs a transition strategy (dual support avoids bricking shipped clients overnight), re-issuance of artifacts signed with weak algorithms, and forward planning for post-quantum migration. Server-only patching leaves the trust chain broken at the client; in-house ciphers violate Kerckhoffs's principle and every audit standard; waiting for a demonstrated break means migrating during an active compromise.",
    "hint": "Hardcoded algorithms turn every deprecation into a rewrite — what architecture property would have made this a config change?",
    "objectives": ["Apply crypto agility principles", "Plan algorithm migration"],
    "mins": 14,
    "evidence": ["Designed an algorithm migration with abstraction, dual support, and PQC roadmap"],
},
],
"incident-response": [
{
    "id": "secplus-incident-response-sc8",
    "title": "Scoping the Compromised Account",
    "domain_id": "incident-response",
    "situation": "The help desk confirms a sales rep's credentials were phished. The attacker logged into webmail and the VPN over 6 hours. The rep had access to the CRM, the file share, and (via a shared admin password the team passed around) two servers.",
    "prompt": "What is the correct scoping approach?",
    "choices": [
        "Reset the rep's password and close the ticket — the account is the scope",
        "Scope to everything the credentials could touch: review VPN/webmail/CRM/file-share logs for the attacker's session, treat the shared admin password as compromised (rotate it, check both servers), and expand if logs show lateral movement",
        "Wipe the rep's laptop immediately",
        "Notify all customers that their data was stolen"
    ],
    "answer": 1,
    "why": "Scoping answers 'how far did it go' by following the credentials' reach, not the user's story: every system those credentials (and the shared admin password) can access is in scope until logs prove otherwise. The shared password is critical — its compromise extends scope to both servers and anyone else who used it. Wiping the laptop destroys evidence before scoping; customer notification before knowing what was accessed is premature and potentially legally mishandled. Scope via log review of each reachable system, then contain.",
    "hint": "The scope isn't the person — it's every system those credentials (including the shared one) could reach.",
    "objectives": ["Scope an incident via credential reach", "Handle shared-credential complications"],
    "mins": 12,
    "evidence": ["Scoped a phishing incident across all systems reachable by compromised and shared credentials"],
},
{
    "id": "secplus-incident-response-sc9",
    "title": "Contain: Pull the Plug or Isolate?",
    "domain_id": "incident-response",
    "situation": "A database server shows active ransomware encryption in progress — files renaming by the second. The server holds the only copy of today's transactions (backup runs at midnight). The network team can either yank the power/network cable now or do a graceful host isolation via EDR.",
    "prompt": "What is the best containment choice?",
    "choices": [
        "Pull the power immediately — stop the encryption at all costs",
        "Isolate the host from the network via EDR/switch port shutdown while keeping it powered on, preserving volatile memory for forensics",
        "Let it finish encrypting so you have a 'complete' incident to analyze",
        "Disconnect the backups first, then decide"
    ],
    "answer": 1,
    "why": "Containment must stop the bleeding without destroying evidence or recovery options. Network isolation (EDR quarantine, port shutdown) halts spread and C2 while preserving RAM — which holds encryption keys, process lists, and network connections that forensics and possible decryption need. Yanking power kills volatile evidence and risks database corruption on top of the encryption; letting it finish is negligence; and the backups should already be isolated/offline by design — touching them mid-incident risks the recovery path.",
    "hint": "You need to stop the spread AND keep what's in memory — which action does both?",
    "objectives": ["Choose containment methods", "Apply order of volatility"],
    "mins": 12,
    "evidence": ["Selected network isolation over power-pull to preserve volatile forensic evidence"],
},
{
    "id": "secplus-incident-response-sc10",
    "title": "Preserving the Evidence",
    "domain_id": "incident-response",
    "situation": "HR reports a departing employee may have exfiltrated customer lists to a personal USB drive. The employee's workstation is still powered on at their desk. Legal wants the evidence to hold up if this goes to court.",
    "prompt": "What is the correct evidence-preservation sequence?",
    "choices": [
        "Let HR search the desk and copy interesting files to a thumb drive for legal",
        "Photograph the scene, capture volatile data (RAM, network connections) first per order of volatility, then create a forensic bit-stream image with a write blocker, hash it, and maintain chain of custody",
        "Turn the workstation off immediately to 'freeze' everything",
        "Remote-wipe the machine to prevent further exfiltration"
    ],
    "answer": 1,
    "why": "Forensic soundness follows the order of volatility (RAM and live state first — they vanish at power-off) then a bit-for-bit image through a write blocker so the original is never altered, with cryptographic hashes proving the copy matches and a chain-of-custody log proving who handled it. HR copying files alters timestamps and destroys admissibility; powering off kills the volatile evidence (open connections, mounted drives, in-memory artifacts); wiping is destruction of evidence and potentially a crime. Legal admissibility requires provable non-alteration at every step.",
    "hint": "Courts ask 'prove you didn't change anything' — which sequence creates that proof?",
    "objectives": ["Apply order of volatility", "Maintain chain of custody"],
    "mins": 12,
    "evidence": ["Sequenced volatile capture, write-blocked imaging, hashing, and chain of custody"],
},
{
    "id": "secplus-incident-response-sc11",
    "title": "Who Gets Told, and When",
    "domain_id": "incident-response",
    "situation": "Forensics confirms attackers accessed a database with 50,000 customer records including SSNs. It's 9 PM. The CEO wants to 'wait until we know everything' before telling anyone. Legal, PR, and the incident commander disagree on timing.",
    "prompt": "What is the correct communication approach?",
    "choices": [
        "Wait until the investigation is 100% complete — premature disclosure causes panic",
        "Follow the communication plan: notify legal and executive leadership immediately, prepare customer/regulator notifications on the legally required timelines (state breach laws often 30-60 days), and keep all external messaging through designated spokespeople",
        "Have the SOC analyst tweet about it to get ahead of the story",
        "Tell customers individually as each record is confirmed"
    ],
    "answer": 1,
    "why": "Breach communication is governed by law and plan, not by comfort: most US states require consumer notification within 30-60 days of discovery, and regulators/contractual obligations add their own clocks — 'wait until we know everything' risks legal liability. The IR communication plan designates who speaks (never ad-hoc tweets from analysts), sequences internal (legal, execs) before external, and prepares holding statements while facts develop. Notification content evolves with the investigation, but the timelines start at discovery, not at certainty.",
    "hint": "Breach-notification clocks start at discovery, not at full understanding — whose timelines govern here?",
    "objectives": ["Apply breach communication planning", "Recognize legal notification timelines"],
    "mins": 12,
    "evidence": ["Initiated plan-driven notifications on legal timelines instead of waiting for full certainty"],
},
{
    "id": "secplus-incident-response-sc12",
    "title": "Eradicate or Rebuild?",
    "domain_id": "incident-response",
    "situation": "Forensics finds a kernel-mode rootkit on three production servers. The antivirus 'cleaned' the detected files and the servers appear to be behaving normally. The business pushes to put them back in service tonight to avoid downtime.",
    "prompt": "What is the correct eradication decision?",
    "choices": [
        "Return them to service — the AV cleaned the malware and they're behaving normally",
        "Rebuild from known-good images/gold builds: a kernel-mode rootkit compromises the OS's own reporting, so 'clean' and 'normal behavior' are untrustworthy; restore data from verified clean backups",
        "Run a second, different antivirus scan to double-check, then return to service",
        "Reinstall only the visibly affected application"
    ],
    "answer": 1,
    "why": "A kernel-mode rootkit subverts the operating system's own perception — every tool running on that OS, including AV and 'normal behavior' observations, reports through compromised eyes. 'Cleaned' is meaningless when the cleaner can't trust what it sees. The only trustworthy eradication is rebuilding from known-good media and restoring data from backups verified predating the compromise. Business pressure for uptime is real, but returning a rootkitted server to production risks re-infection, persistent access, and a far worse second incident.",
    "hint": "If the malware controls the kernel, can any tool on that machine tell you the truth about it?",
    "objectives": ["Decide eradication vs rebuild", "Reason about rootkit trust boundaries"],
    "mins": 12,
    "evidence": ["Ordered rebuild from known-good media for kernel-compromised servers despite uptime pressure"],
},
{
    "id": "secplus-incident-response-sc13",
    "title": "The Blameless Postmortem",
    "domain_id": "incident-response",
    "situation": "The ransomware incident is closed: entry via unpatched VPN, 4-hour dwell, contained by network isolation, recovered from offline backups. The VP wants a lessons-learned meeting and suggests starting with 'who forgot to patch the VPN.'",
    "prompt": "How should lessons-learned be run to actually improve security?",
    "choices": [
        "Focus on individual accountability — name who missed the patch so it doesn't happen again",
        "Run a blameless review: reconstruct the timeline, identify systemic gaps (patch process, VPN exposure, detection delay), assign corrective actions with owners and dates, and feed them into the risk register and control improvements",
        "Skip the meeting — the incident is over and everyone is tired",
        "Write a one-paragraph summary for the file and move on"
    ],
    "answer": 1,
    "why": "Blameless postmortems work because blame shuts down honesty — engineers hide near-misses when the meeting is a tribunal, and the systemic causes (why was the VPN internet-facing and unpatched? why did detection take 4 hours?) never surface. The output must be structural: timeline, contributing system conditions, and tracked corrective actions (patch SLA enforcement, VPN hardening, backup test restores) with owners and deadlines, fed back into governance. A paragraph or a skipped meeting guarantees the identical incident next quarter — which is exactly what the systems-anatomy feedback loop predicts.",
    "hint": "Blame finds a person; the next attack exploits a system — which does the review need to fix?",
    "objectives": ["Conduct blameless lessons-learned", "Convert findings into tracked corrective actions"],
    "mins": 12,
    "evidence": ["Ran a blameless postmortem producing tracked systemic corrective actions"],
},
],
},
"comptia-network-plus": {
"concepts": [
{
    "id": "netplus-concepts-sc8",
    "title": "Which Layer Is Actually Broken?",
    "domain_id": "concepts",
    "situation": "Users report they can't reach the company intranet by name, but they CAN reach it by IP address. They can also browse the public internet normally, ping the intranet server's IP, and other subnets work fine.",
    "prompt": "Using the OSI model to isolate the fault, which layer is implicated?",
    "choices": [
        "Layer 1 — a cable must be damaged",
        "Layer 3 — IP routing is failing",
        "Layer 7 (application-layer name resolution) — DNS is failing while Layers 1-3 demonstrably work",
        "Layer 2 — the switch MAC table is corrupt"
    ],
    "answer": 2,
    "why": "The OSI model is a fault-isolation tool: working IP connectivity (ping by IP, internet browsing) proves Layers 1-3 are functional end-to-end. Name resolution failing while IP works isolates the fault to the application-layer service that maps names to addresses — DNS. Layer 1/2/3 faults would break IP connectivity too, not selectively break names. On the exam, 'works by IP, fails by name' is the canonical DNS-at-Layer-7 signature.",
    "hint": "IP works, names don't — what service translates between them, and at which layer does it live?",
    "objectives": ["Isolate faults with the OSI model", "Recognize DNS failure signatures"],
    "mins": 10,
    "evidence": ["Isolated a name-resolution failure to the application layer using OSI reasoning"],
},
],
"implementation": [
{
    "id": "netplus-implementation-sc8",
    "title": "Wiring the New Warehouse",
    "domain_id": "implementation",
    "situation": "A warehouse needs 12 new drops: 8 for PoE security cameras along a 90-meter run, 2 for APs in a high-interference area near the loading dock, and 2 uplinks between IDF closets 400 meters apart through conduit shared with power lines.",
    "prompt": "What is the correct media plan?",
    "choices": [
        "Cat5e for everything — cheapest option that 'works'",
        "Cat6A for the PoE camera runs (heat/bundle and distance headroom) and APs, plus multimode fiber for the 400m IDF uplinks (distance + EMI immunity in the power conduit)",
        "Coaxial cable throughout for maximum shielding",
        "Wireless bridges for everything to avoid cable runs"
    ],
    "answer": 1,
    "why": "Media selection is constraint-matching: 90m PoE camera bundles need Cat6A's headroom for heat dissipation and alien crosstalk (Cat5e at length limit with PoE bundles risks failures); the 400m IDF link exceeds copper's 100m limit outright, requiring fiber; and conduit shared with power lines means EMI, which fiber is immune to. Coax is obsolete for new Ethernet; all-wireless can't reliably backhaul PoE cameras. Each choice follows from a physical constraint, not brand preference.",
    "hint": "Three constraints: 100m copper limit, PoE heat in bundles, EMI near power — which media survives each?",
    "objectives": ["Select media by distance/EMI/power constraints", "Apply copper distance limits"],
    "mins": 12,
    "evidence": ["Designed a mixed Cat6A/fiber plant matched to distance, PoE, and EMI constraints"],
},
],
"net-security": [
{
    "id": "netplus-net-security-sc8",
    "title": "The Rogue Switch in the Conference Room",
    "domain_id": "net-security",
    "situation": "Someone plugged a $20 unmanaged switch into a conference-room wall jack to connect extra laptops. Now the help desk sees intermittent outages: some users get IP addresses in a strange range, and the network team spots two devices claiming to be the default gateway.",
    "prompt": "What happened, and what is the best preventive control?",
    "choices": [
        "A broadcast storm; enable storm control",
        "A rogue DHCP server on the cheap switch is handing out bad leases and a rogue gateway; enable DHCP snooping with trusted ports plus Dynamic ARP Inspection",
        "The switch is too slow; replace it with a managed switch and leave the port open",
        "Normal behavior; unmanaged switches are safe on enterprise networks"
    ],
    "answer": 1,
    "why": "The symptoms are textbook rogue DHCP: wrong IP ranges mean a second DHCP server is answering faster than the legitimate one, and a rogue gateway enables man-in-the-middle traffic interception. DHCP snooping builds a binding table of legitimate DHCP servers on trusted (uplink) ports and drops DHCP offers from untrusted access ports — killing the rogue server at the switch. Dynamic ARP Inspection uses that binding table to stop the gateway spoofing. Storm control addresses a different problem; replacing the switch without port controls just legitimizes the hole.",
    "hint": "Wrong IPs plus a second 'gateway' — what device is answering requests it shouldn't, and what switch feature silences it?",
    "objectives": ["Diagnose rogue DHCP", "Apply DHCP snooping and DAI"],
    "mins": 12,
    "evidence": ["Diagnosed rogue DHCP/gateway spoofing and prescribed DHCP snooping with DAI"],
},
],
"net-troubleshoot": [
{
    "id": "netplus-net-troubleshoot-sc8",
    "title": "Methodology: The Intermittent Drop",
    "domain_id": "net-troubleshoot",
    "situation": "A branch office loses connectivity for 2-3 minutes, several times a day, then recovers on its own. The last tech 'fixed' it by rebooting the router, which changed nothing. You arrive with a structured methodology: identify, theorize, test, establish plan, implement, verify, document.",
    "prompt": "What is the correct next step after identifying the symptom pattern?",
    "choices": [
        "Immediately replace the router — reboots suggest hardware failure",
        "Theorize probable causes from the pattern (e.g., DHCP lease expiry, STP reconvergence, WAN flaps, scheduled interference) and test by correlating outage times with logs before changing anything",
        "Reboot all network devices in sequence",
        "Escalate to the ISP immediately"
    ],
    "answer": 1,
    "why": "The CompTIA troubleshooting methodology exists to prevent exactly what the last tech did — random action without theory. Intermittent, self-recovering drops point at time-correlated causes (DHCP lease timers, STP topology changes, cron-like interference), so the next step is forming probable-cause theories and testing them against logs/timestamps. Replacing hardware or rebooting everything without evidence wastes resources and can mask the real fault; ISP escalation comes after you've ruled out your own infrastructure with data.",
    "hint": "The methodology step after 'identify the problem' is 'establish a theory' — what does the intermittent pattern suggest you check first?",
    "objectives": ["Apply the CompTIA troubleshooting methodology", "Correlate intermittent faults with timed causes"],
    "mins": 10,
    "evidence": ["Formed and log-tested theories for an intermittent outage instead of swapping hardware"],
},
],
"systems-anatomy": [
{
    "id": "netplus-systems-anatomy-sc8",
    "title": "Packet Journey: LAN to WAN",
    "domain_id": "systems-anatomy",
    "situation": "A user opens a web page hosted in another country. The packet leaves the PC, crosses a campus LAN, passes the core, exits through the edge firewall and ISP router, and traverses the internet to the server.",
    "prompt": "Walking the packet's journey, at which handoff does the source MAC address change while the source IP stays the same?",
    "choices": [
        "At the user's PC when the packet is first created",
        "At every router hop: each router strips the old Layer 2 frame and builds a new one with its own egress MAC, while the Layer 3 source IP is preserved end-to-end",
        "At the firewall, which rewrites both MAC and IP",
        "Never — MAC addresses are end-to-end like IP addresses"
    ],
    "answer": 1,
    "why": "This is the fundamental L2/L3 journey distinction: MAC addresses are hop-local (each router re-frames the packet for the next link with new source/destination MACs), while IP addresses are end-to-end (source IP stays the user's, destination IP stays the server's, across the whole journey — NAT aside). Visualizing the packet as a traveler that changes its 'local vehicle' (frame) at every router while keeping its 'passport' (IP) is the systems view that makes routing, ARP, and switching click together.",
    "hint": "Frames are local to each link; packets are global — which header gets rewritten at each router?",
    "objectives": ["Trace L2 vs L3 addressing across hops", "Explain frame rewrite at routers"],
    "mins": 12,
    "evidence": ["Traced MAC rewrite vs IP preservation across router hops"],
},
{
    "id": "netplus-systems-anatomy-sc9",
    "title": "DNS Resolution Chain",
    "domain_id": "systems-anatomy",
    "situation": "A workstation needs to resolve www.example.com for the first time today. Its local DNS cache is empty, and the configured resolver has nothing cached either.",
    "prompt": "What is the correct sequence of the resolution journey?",
    "choices": [
        "Workstation asks the authoritative server directly, which answers immediately",
        "Workstation → recursive resolver → root servers (where is .com?) → .com TLD servers (where is example.com?) → example.com authoritative server (what is www's IP?) → answer cached at each level on the way back",
        "Workstation broadcasts on the LAN asking who knows www.example.com",
        "The resolver guesses from its hosts file and returns that"
    ],
    "answer": 1,
    "why": "DNS resolution is a delegation chain walked top-down: the recursive resolver starts at the roots (which only know where TLD servers are), follows the referral to the .com servers (which only know example.com's nameservers), and finally asks the authoritative server that actually holds the www record. Each hop caches its answer, which is why the second lookup is instant — the systems view shows caching as the chain 'remembering' each handoff. Direct-to-authoritative skips how resolvers discover authority; LAN broadcast is LLMNR/NetBIOS, not DNS.",
    "hint": "Nobody knows the full answer at first — who knows who to ask next, starting from the top?",
    "objectives": ["Sequence iterative DNS resolution", "Explain caching at each chain level"],
    "mins": 12,
    "evidence": ["Sequenced root-to-authoritative DNS resolution with per-level caching"],
},
{
    "id": "netplus-systems-anatomy-sc10",
    "title": "DHCP Handshake: DORA in Motion",
    "domain_id": "systems-anatomy",
    "situation": "A laptop connects to the office Wi-Fi. It has no IP address. Within seconds it's online with address 10.20.30.45, gateway 10.20.30.1, and DNS servers — all assigned automatically.",
    "prompt": "What is the four-step handshake that just happened, in order?",
    "choices": [
        "Request → Offer → Discover → Acknowledge",
        "Discover (broadcast: any DHCP server out there?) → Offer (server proposes an address) → Request (client claims it) → Acknowledge (server confirms lease with gateway/DNS options)",
        "The AP assigns the address directly from its own pool",
        "Authenticate → Associate → Encrypt → Address"
    ],
    "answer": 1,
    "why": "DORA is a negotiation journey: the client shouts into the dark (Discover broadcast — it has no address yet, so it must broadcast), servers answer with proposals (Offer), the client selects and formally claims one (Request — this step matters because it also handles declines/relays), and the server commits the lease plus options like gateway and DNS (Acknowledge). The AP is just a bridge — it doesn't assign addresses. Seeing it as discover-then-negotiate explains why DHCP fails across routers without a helper address (broadcasts don't cross routers).",
    "hint": "The client starts with no address and must shout — what four messages turn that shout into a confirmed lease?",
    "objectives": ["Sequence the DORA handshake", "Explain why DHCP needs broadcast/helper addresses"],
    "mins": 12,
    "evidence": ["Sequenced the DORA handshake and explained broadcast behavior"],
},
{
    "id": "netplus-systems-anatomy-sc11",
    "title": "TCP Three-Way Handshake Anatomy",
    "domain_id": "systems-anatomy",
    "situation": "A packet capture shows a client trying to open an HTTPS session: you see SYN, then SYN-ACK, then ACK — but immediately after, the client sends RST and the connection dies. The server admin insists 'the server is up and listening.'",
    "prompt": "Reading the handshake as a system, what does the RST after a completed handshake tell you?",
    "choices": [
        "The network dropped the handshake packets",
        "The handshake completed (both sides agreed on sequence numbers), so the failure is above TCP — the application rejected the connection (e.g., wrong SNI/host, TLS failure, or app-level refusal)",
        "TCP is unreliable and handshakes often fail randomly",
        "The client's SYN was malformed"
    ],
    "answer": 1,
    "why": "The three-way handshake is TCP's agreement ceremony: SYN (here's my starting sequence number), SYN-ACK (acknowledged, here's mine), ACK (acknowledged) — after which both sides have synchronized state and the connection is ESTABLISHED. A RST after that point means TCP did its job and something higher up killed the session: the classic case is a TLS/SNI mismatch or an application with no listener on the requested host. The systems view separates 'the transport handshake worked' from 'the application refused' — different layers, different fixes.",
    "hint": "SYN, SYN-ACK, ACK all completed — so which layer's job is done, and which layer killed it?",
    "objectives": ["Interpret the TCP handshake in captures", "Separate transport success from application refusal"],
    "mins": 12,
    "evidence": ["Diagnosed a post-handshake RST as application-layer refusal, not TCP failure"],
},
{
    "id": "netplus-systems-anatomy-sc12",
    "title": "VLAN Trunking Flow",
    "domain_id": "systems-anatomy",
    "situation": "Two switches connect via a single cable. Switch A has VLAN 10 (sales) and VLAN 20 (engineering) access ports; Switch B has the same VLANs. A sales PC on Switch A can't reach a sales server on Switch B, but engineering-to-engineering across the switches works fine.",
    "prompt": "Following the frame's journey across the trunk, what is the most likely fault?",
    "choices": [
        "The trunk cable is unplugged",
        "VLAN 10 isn't allowed (or isn't tagged) on the trunk — the frame's 802.1Q tag for VLAN 10 is missing or pruned, so Switch B drops it, while VLAN 20's tags pass",
        "The sales PC has the wrong IP address",
        "Spanning tree blocked the trunk port"
    ],
    "answer": 1,
    "why": "A trunk carries multiple VLANs by tagging each frame with an 802.1Q VLAN ID as it crosses the inter-switch link — the tag is the frame's 'which broadcast domain do I belong to' label. If VLAN 10 is pruned from the allowed list or there's a native-VLAN mismatch affecting it, VLAN 10 frames die at the trunk while VLAN 20 flows normally — exactly the 'one VLAN works, one doesn't' symptom. A dead cable or blocked port would kill both VLANs; a wrong PC IP wouldn't be VLAN-selective across switches.",
    "hint": "One VLAN crosses the link fine, the other doesn't — what per-VLAN mechanism on the trunk could differ?",
    "objectives": ["Trace tagged frames across trunks", "Diagnose per-VLAN trunk faults"],
    "mins": 12,
    "evidence": ["Diagnosed selective VLAN failure as trunk allowed-list/tagging issue"],
},
{
    "id": "netplus-systems-anatomy-sc13",
    "title": "Routing Decision Chain",
    "domain_id": "systems-anatomy",
    "situation": "A router's table has: 10.0.0.0/8 via OSPF, 10.20.0.0/16 via a static route, 10.20.30.0/24 via EIGRP, and 0.0.0.0/0 toward the ISP. A packet arrives destined for 10.20.30.99.",
    "prompt": "Walking the router's decision chain, which route wins and why?",
    "choices": [
        "0.0.0.0/0 — the default route is the ultimate fallback and always wins",
        "10.0.0.0/8 via OSPF — OSPF has the best administrative distance",
        "10.20.30.0/24 via EIGRP — longest prefix match wins regardless of protocol or AD",
        "10.20.0.0/16 static — static routes beat dynamic protocols"
    ],
    "answer": 2,
    "why": "The routing decision chain has a strict order: first, longest prefix match (most specific network wins — /24 beats /16 beats /8 beats /0); only when two routes have the SAME prefix length does administrative distance break the tie. 10.20.30.0/24 is the most specific match for 10.20.30.99, so it wins before AD is ever consulted. This ordering is why route summarization and specific static overrides work — specificity outranks protocol preference every time.",
    "hint": "The router checks prefix length before it ever compares protocols — which entry is most specific?",
    "objectives": ["Apply longest-prefix-match", "Order the routing decision chain"],
    "mins": 12,
    "evidence": ["Selected the winning route via longest prefix match before administrative distance"],
},
],
"exam-strategy": [
{
    "id": "netplus-exam-strategy-sc8",
    "title": "Subnetting Under Time Pressure",
    "domain_id": "exam-strategy",
    "situation": "Question 12 asks: 'How many usable hosts in 10.44.0.0/19?' You've spent 45 seconds and the binary math is getting tangled. There are 20 more questions and two wiring-diagram PBQs ahead.",
    "prompt": "What is the fastest reliable technique?",
    "choices": [
        "Write out all 32 bits and count — accuracy over speed",
        "Use the memorized block-size method: /19 → block size 32 in the third octet (256-224), hosts = 32×256 - 2 = 8,190; drill the /24–/30 table so this takes 15 seconds",
        "Skip all subnetting questions — they're too time-expensive",
        "Guess C and move on"
    ],
    "answer": 1,
    "why": "Network+ subnetting questions are high-frequency and formulaic — they reward a memorized shortcut table, not first-principles binary math under pressure. The block-size method (256 minus the interesting-octet mask value = block size; hosts = block size × remaining-octet multiples − 2) turns every 'how many hosts/subnets' question into 15 seconds of arithmetic. Skipping them abandons some of the exam's most predictable points; full binary expansion burns the time budget two PBQs need.",
    "hint": "The exam asks the same five subnetting question shapes repeatedly — what turns them into 15-second arithmetic?",
    "objectives": ["Apply block-size subnetting shortcuts", "Budget time for PBQs"],
    "mins": 10,
    "evidence": ["Solved a /19 host-count question with the block-size method in seconds"],
},
{
    "id": "netplus-exam-strategy-sc9",
    "title": "PBQ: The Wiring Diagram",
    "domain_id": "exam-strategy",
    "situation": "A PBQ shows a floor plan and asks you to drag cable types to each run: a 120-meter backbone between closets, desktop drops, and a fiber uplink to the ISP demarc. The interface lets you place each cable once.",
    "prompt": "What is the best PBQ approach?",
    "choices": [
        "Place cables by what 'looks standard' — most runs are Cat6",
        "Map each run to its constraint first (120m exceeds copper's 100m → fiber; desktops → Cat6/Cat6A; demarc uplink → ISP-specified, usually fiber), place, then re-verify each run against its constraint",
        "Do the PBQ last with whatever time remains, rushing placement",
        "Use the same cable for every run for consistency"
    ],
    "answer": 1,
    "why": "Network+ PBQs test constraint-matching, not memorized diagrams: the 120m run is a deliberate trap (copper's hard 100m limit), the demarc uplink tests knowing the ISP handoff is typically fiber, and desktop drops test standard Cat6. The method is: read every label, translate each run into its governing constraint, place deliberately, then verify each placement against the constraint before submitting — PBQs give partial credit, so even uncertain placements earn points when reasoned. Rushing or uniform placement throws away the exam's most generous scoring.",
    "hint": "One of those runs breaks a hard physical limit — which run, and what does the limit force?",
    "objectives": ["Apply constraint-mapping to wiring PBQs", "Earn partial credit deliberately"],
    "mins": 12,
    "evidence": ["Mapped each cable run to its physical constraint in a wiring PBQ"],
},
{
    "id": "netplus-exam-strategy-sc10",
    "title": "Troubleshooting-Methodology Questions",
    "domain_id": "exam-strategy",
    "situation": "A question describes a technician who, faced with a downed switch, immediately replaced it — only to find the real cause was a tripped breaker. It asks: 'What should the technician have done FIRST?'",
    "prompt": "How do you reliably answer methodology questions?",
    "choices": [
        "Pick the most technical-sounding first step",
        "Map to the CompTIA methodology sequence: identify the problem (gather info, question users, check logs/power) comes before any theory, testing, or action — so the answer is an information-gathering step",
        "Pick 'replace the switch' — it was a reasonable guess",
        "Pick the last step — documentation"
    ],
    "answer": 1,
    "why": "Methodology questions are among the exam's most predictable: they test the ORDER of the troubleshooting steps (identify → establish theory → test → plan → implement → verify → document). 'What first?' almost always wants an identify-the-problem action — check power, question the user, review logs — because every wrong answer in these questions is a later step done prematurely (testing, implementing, escalating). Memorizing the seven-step sequence converts a whole question family into free points.",
    "hint": "The methodology is a sequence — what step must precede every theory, test, and fix?",
    "objectives": ["Recall the troubleshooting methodology order", "Answer 'what first' questions"],
    "mins": 8,
    "evidence": ["Selected the identify-the-problem step as the correct first action"],
},
{
    "id": "netplus-exam-strategy-sc11",
    "title": "Port and Protocol Recall",
    "domain_id": "exam-strategy",
    "situation": "A question asks which port must be opened for a new LDAPS-based directory sync through the firewall. The options are 389, 636, 443, and 3268. You're blanking under pressure.",
    "prompt": "What recall technique works best for port questions?",
    "choices": [
        "Reason from pairs and patterns: LDAP 389 → LDAPS is LDAP-over-TLS like HTTPS is to HTTP, and the 'secure' variants cluster (443/636/993/995); 636 is the memorized secure-LDAP port",
        "Pick 443 — it's the most common secure port",
        "Pick 389 — LDAP is LDAP",
        "Memorize all 65,535 ports"
    ],
    "answer": 0,
    "why": "Port questions reward pattern-grouped memory, not brute memorization: learn the base protocols (LDAP 389, HTTP 80, FTP 21, SMTP 25, DNS 53, DHCP 67/68) plus the secure-variant pattern (add TLS → 636, 443, 990, 465/587, 993, 995). LDAPS = LDAP + TLS = 389's secure sibling = 636, just as HTTPS is 443 to HTTP's 80. The exam tests the ~30 common ports in these relational clusters; reasoning 'secure variant of X' resolves most of them even when the exact number is fuzzy.",
    "hint": "Secure variants of protocols cluster together (443, 636, 993, 995) — what's the secure sibling of LDAP 389?",
    "objectives": ["Recall common ports via pattern groups", "Distinguish secure protocol variants"],
    "mins": 8,
    "evidence": ["Derived LDAPS 636 from the secure-variant port pattern"],
},
{
    "id": "netplus-exam-strategy-sc12",
    "title": "Parsing the Network Scenario",
    "domain_id": "exam-strategy",
    "situation": "A half-page scenario describes a three-site company, its ISP links, a recent VoIP deployment, user complaints about call quality, and a budget note. The final line asks: 'Which QoS marking should voice traffic receive?'",
    "prompt": "What is the most efficient parsing technique?",
    "choices": [
        "Study the topology details first — the answer is hidden in the site descriptions",
        "Read the final question first, recognize it asks a recall fact (voice = DSCP EF / CoS 5), and ignore the decorative topology and budget context",
        "Calculate bandwidth from the user counts before answering",
        "Focus on the budget note — it determines the answer"
    ],
    "answer": 1,
    "why": "Network+ scenario questions pad simple recall questions with realistic context — the topology, user counts, and budget are atmosphere, not inputs. Reading the question sentence first reveals this is a 'which marking' fact question: voice traffic gets DSCP EF (Expedited Forwarding), the highest-priority marking, because voice is jitter-sensitive. The parsing skill is distinguishing questions that need the scenario data (subnetting, troubleshooting) from ones where the scenario is camouflage for a memorized fact.",
    "hint": "Does the question ask you to compute something from the scenario, or to recall a standard?",
    "objectives": ["Distinguish camouflage context from needed data", "Recall voice QoS markings"],
    "mins": 8,
    "evidence": ["Identified a scenario question as a recall fact (DSCP EF) despite padded context"],
},
{
    "id": "netplus-exam-strategy-sc13",
    "title": "'MOST Likely Cause' Questions",
    "domain_id": "exam-strategy",
    "situation": "'A user can't connect to the network. The link light is off, the cable is Cat6, the switch port shows no errors, and other users on the same switch are fine. What is the MOST likely cause?' Options: faulty NIC, VLAN misconfiguration, DNS failure, duplex mismatch.",
    "prompt": "How do you reason through 'most likely' questions?",
    "choices": [
        "Pick the most complex cause — exams test hard concepts",
        "Work bottom-up through the evidence: link light off + one user affected = Layer 1 on that drop (bad cable, bad NIC, unplugged) — faulty NIC/cable outranks VLAN/DNS/duplex, which would show a link light",
        "Pick DNS — it's the most common network problem",
        "Pick duplex mismatch — it causes the subtlest symptoms"
    ],
    "answer": 1,
    "why": "'MOST likely' questions are evidence-weighted: each clue eliminates layers. Link light OFF is a Layer 1 verdict — no electrical connectivity — which instantly rules out VLAN (L2 config, link would be up), DNS (L7, link would be up), and duplex mismatch (link would be up but slow/erroring). Single-user scope rules out switch-wide faults. The exam rewards this bottom-up elimination: the physical evidence constrains the answer before you ever weigh the options' sophistication.",
    "hint": "The link light is a Layer 1 witness — what does 'off' rule out?",
    "objectives": ["Weight evidence in 'most likely' questions", "Apply bottom-up elimination"],
    "mins": 10,
    "evidence": ["Eliminated upper-layer causes using Layer 1 link-light evidence"],
},
{
    "id": "netplus-exam-strategy-sc14",
    "title": "The Flag-and-Return Pass",
    "domain_id": "exam-strategy",
    "situation": "You're 40 minutes into Network+: 45 questions answered, 8 flagged (mostly subnetting and a PBQ), and a fresh question about EIGRP metrics has you stuck between two answers.",
    "prompt": "What is the optimal use of the remaining time?",
    "choices": [
        "Debate the EIGRP question until certain — metrics questions are heavily weighted",
        "Flag it with a provisional guess, finish all unanswered questions first, then return to flagged items with remaining time — unanswered questions score zero and later questions often prime earlier ones",
        "Submit now — 45 answered is probably enough to pass",
        "Change all flagged provisional guesses to your second choice"
    ],
    "answer": 1,
    "why": "The two-pass strategy maximizes expected score: every unanswered question is a certain zero, while flagged questions already have provisional answers banked. Finishing the sweep first also exploits priming — a later question about routing protocols often triggers the memory needed for the earlier EIGRP question. Submitting early abandons ~half the exam's points; mass-changing guesses without new information is statistically harmful. Discipline here is worth more than any single question's content knowledge.",
    "hint": "Blank = zero, always — which sequence banks the most points before the clock runs out?",
    "objectives": ["Execute the two-pass exam strategy", "Exploit question priming on review"],
    "mins": 8,
    "evidence": ["Completed the full question sweep before returning to flagged items"],
},
{
    "id": "netplus-exam-strategy-sc15",
    "title": "Wireless Standard Alphabet Soup",
    "domain_id": "exam-strategy",
    "situation": "A question asks which Wi-Fi standard introduced OFDMA and operates in the 6 GHz band. Options: 802.11ac, 802.11ax, 802.11n, 802.11be. You know 'ax = Wi-Fi 6' but the 6 GHz detail is nagging you.",
    "prompt": "What is the best reasoning?",
    "choices": [
        "802.11be — newest standard, so it must have the newest features",
        "802.11ax (Wi-Fi 6/6E): ax introduced OFDMA and MU-MIMO uplink; the 6E extension added 6 GHz operation — be (Wi-Fi 7) builds on ax but the OFDMA+6GHz combination points to ax/6E",
        "802.11ac — it was the big speed jump",
        "802.11n — it introduced MIMO, close enough"
    ],
    "answer": 1,
    "why": "The exam tests standards by their signature innovations: n = MIMO/channel bonding (Wi-Fi 4), ac = wider channels/MU-MIMO downlink/5 GHz focus (Wi-Fi 5), ax = OFDMA + 6 GHz via the 6E extension (Wi-Fi 6/6E), be = 320 MHz channels/multi-link (Wi-Fi 7). The question's two clues (OFDMA, 6 GHz) are both ax/6E signatures — be inherits OFDMA but its headline is multi-link operation. Memorizing one signature innovation per standard resolves these questions without memorizing spec sheets.",
    "hint": "Each standard has one headline innovation — which standard's headline is OFDMA?",
    "objectives": ["Map 802.11 standards to signature features", "Distinguish Wi-Fi 6/6E from Wi-Fi 7"],
    "mins": 8,
    "evidence": ["Matched OFDMA + 6 GHz to 802.11ax/Wi-Fi 6E via signature features"],
},
],
"subnetting-mastery": [
{
    "id": "netplus-subnetting-sc8",
    "title": "VLSM: Sizing the Branch Offices",
    "domain_id": "subnetting-mastery",
    "situation": "From 192.168.10.0/24 you must carve subnets for: HQ LAN (100 hosts), Branch A (50 hosts), Branch B (25 hosts), and three point-to-point WAN links (2 hosts each). The design must waste as few addresses as possible.",
    "prompt": "What is the correct VLSM approach?",
    "choices": [
        "Split into four equal /26 subnets — simple and uniform",
        "Allocate largest-first: HQ 192.168.10.0/25 (126 hosts), Branch A 192.168.10.128/26 (62), Branch B 192.168.10.192/27 (30), WAN links 192.168.10.224/30, .228/30, .232/30 — each sized to its need",
        "Give every site a /24 — plenty of room to grow",
        "Use /30 for everything including the LANs"
    ],
    "answer": 1,
    "why": "VLSM (variable-length subnet masking) exists to right-size each subnet: allocate from largest requirement to smallest so each block fits its host count with minimal waste (HQ needs 100 → /25 gives 126; /26's 62 would starve it). Equal-size splits waste massively on small needs (a /26 for a 2-host WAN link burns 60 addresses); /30s can't hold LAN host counts. Largest-first ordering prevents fragmentation that strands unusable gaps. This is the core VLSM exam skill: match mask to host count, descending.",
    "hint": "Which requirement is biggest, and what's the smallest mask that holds it? Work downward from there.",
    "objectives": ["Design VLSM allocations largest-first", "Match prefix length to host count"],
    "mins": 14,
    "evidence": ["Built a waste-minimized VLSM plan allocating largest requirements first"],
},
{
    "id": "netplus-subnetting-sc9",
    "title": "Supernetting the Route Table",
    "domain_id": "subnetting-mastery",
    "situation": "A router advertises four contiguous networks: 172.16.0.0/24, 172.16.1.0/24, 172.16.2.0/24, 172.16.3.0/24. The routing table is bloating across the WAN, and the engineer wants one summary route.",
    "prompt": "What is the correct summary (supernet)?",
    "choices": [
        "172.16.0.0/16 — summarizes everything, simplest",
        "172.16.0.0/22 — the four /24s share the first 22 bits (third octet 0-3 = 000000xx), covering exactly the four networks",
        "172.16.0.0/24 — just advertise the first one",
        "172.16.0.0/23 — close enough, covers most of it"
    ],
    "answer": 1,
    "why": "Route summarization finds the longest prefix covering exactly the component networks: the four /24s span third-octet values 0-3, whose binary (00000000-00000011) shares the first 6 bits of that octet → /16 + 6 = /22. A /22 covers precisely 172.16.0.0-172.16.3.255 with no extras. /16 would also swallow 172.16.4.0-172.16.255.255 — advertising reachability you may not have (a black-hole risk). /23 covers only 0-1. The exam tests this exact bit-boundary reasoning.",
    "hint": "Write the third octet (0-3) in binary — how many leading bits do all four share?",
    "objectives": ["Compute summary routes", "Avoid over-summarization"],
    "mins": 12,
    "evidence": ["Summarized four /24s to an exact /22 without over-aggregation"],
},
{
    "id": "netplus-subnetting-sc10",
    "title": "The Wrong Mask Mystery",
    "domain_id": "subnetting-mastery",
    "situation": "PC-A (10.10.10.50/24) can't reach PC-B (10.10.11.60/24), but both reach the internet fine. The network design says both PCs should be in the same subnet. PC-B's mask was typed by hand during a late-night change.",
    "prompt": "What is the most likely misconfiguration?",
    "choices": [
        "PC-B's default gateway is wrong",
        "PC-B's mask should be /23 (255.255.254.0), not /24 — with /24, 10.10.11.x is a different network than 10.10.10.x, so PC-B routes locally-destined traffic to the gateway instead of ARPing directly",
        "The switch port is bad",
        "DNS is misconfigured on PC-B"
    ],
    "answer": 1,
    "why": "A wrong subnet mask changes a host's definition of 'local': with /24, PC-B believes 10.10.10.50 is remote and sends the traffic to its gateway (which may not route it back correctly or at all), while both hosts' gateways still give them internet. The design intent (/23 covering 10.10.10.0-10.10.11.255) makes them local to each other. 'Same subnet on paper, can't talk, internet works' is the signature of a mask mismatch — the host's local-vs-remote decision is wrong, not its gateway or DNS.",
    "hint": "With a /24 mask, does PC-B consider 10.10.10.50 local or remote — and what does it do with 'remote' traffic?",
    "objectives": ["Diagnose subnet mask mismatches", "Explain local vs remote forwarding decisions"],
    "mins": 12,
    "evidence": ["Diagnosed a /24-vs-/23 mask mismatch from local/remote forwarding behavior"],
},
{
    "id": "netplus-subnetting-sc11",
    "title": "CIDR Aggregation at the Edge",
    "domain_id": "subnetting-mastery",
    "situation": "Your company owns 203.0.113.0/24 through 203.0.113.0/27... (four /27 blocks: .0/27, .32/27, .64/27, .96/27) wait — actually the allocation is 203.0.113.0/27, 203.0.113.32/27, 203.0.113.64/27, 203.0.113.96/27. The ISP asks for a single aggregated announcement.",
    "prompt": "What single CIDR block aggregates all four /27s?",
    "choices": [
        "203.0.113.0/24",
        "203.0.113.0/25 — the four /27s span .0-.127, sharing the first 25 bits",
        "203.0.113.0/26",
        "203.0.113.0/27 — announce them individually"
    ],
    "answer": 1,
    "why": "Four contiguous /27s (.0, .32, .64, .96) fill exactly the .0-.127 range — the lower half of the fourth octet (00000000-01111111), sharing the first bit of that octet → /24 + 1 = /25. The /25 covers precisely the allocated space with nothing extra, which is what the ISP wants (announcing /24 would claim .128-.255 that you don't own — a route leak). Aggregation is supernetting applied to public address announcements: exact fit, no more.",
    "hint": "The four blocks fill .0 through .127 — what prefix covers exactly that half?",
    "objectives": ["Aggregate CIDR blocks", "Prevent route leaks via exact-fit aggregation"],
    "mins": 12,
    "evidence": ["Aggregated four /27s into an exact-fit /25 announcement"],
},
{
    "id": "netplus-subnetting-sc12",
    "title": "Subnet Math Under Pressure",
    "domain_id": "subnetting-mastery",
    "situation": "Exam question: 'A /26 network is subnetted with a /28 mask. How many subnets, and how many usable hosts per subnet?' The clock is ticking.",
    "prompt": "What is the 20-second solution?",
    "choices": [
        "4 subnets, 14 hosts each — borrowed 2 bits (28-26) → 2² = 4 subnets; host bits 32-28=4 → 2⁴-2 = 14 usable",
        "2 subnets, 30 hosts each",
        "8 subnets, 6 hosts each",
        "16 subnets, 14 hosts each"
    ],
    "answer": 0,
    "why": "The two formulas answer every 'subnetting a subnet' question: borrowed bits = new mask − old mask (28−26 = 2 → 2² = 4 subnets); host bits = 32 − new mask (4 → 2⁴ − 2 = 14 usable, subtracting network and broadcast). Twenty seconds, no binary needed. The common trap is forgetting the −2 (counting network/broadcast as usable) or borrowing from /24 instead of the given /26. Drill: subnets = 2^(borrowed), hosts = 2^(host bits) − 2.",
    "hint": "Two formulas: 2^(borrowed bits) for subnets, 2^(host bits) − 2 for hosts — what did you borrow from?",
    "objectives": ["Apply subnet-borrowing formulas", "Avoid the network/broadcast counting trap"],
    "mins": 10,
    "evidence": ["Computed subnet and host counts from borrowed bits under time pressure"],
},
{
    "id": "netplus-subnetting-sc13",
    "title": "Wildcard vs Subnet Mask",
    "domain_id": "subnetting-mastery",
    "situation": "An ACL must permit traffic from 192.168.5.0/26. The junior admin writes 'permit 192.168.5.0 255.255.255.192' and the ACL rejects it. A senior rewrites it as 'permit 192.168.5.0 0.0.0.63'.",
    "prompt": "Why is the senior's version correct?",
    "choices": [
        "ACLs use inverse (wildcard) masks: 0 = must match, 1 = ignore — the wildcard for /26 is 0.0.0.63 (inverse of 255.255.255.192)",
        "The senior just prefers shorter numbers",
        "Subnet masks don't work in ACLs at all",
        "0.0.0.63 is the broadcast address"
    ],
    "answer": 0,
    "why": "Cisco-style ACLs use wildcard masks — the bitwise inverse of subnet masks, with flipped semantics: 0 means 'this bit must match,' 1 means 'don't care.' For /26 (255.255.255.192 = 11000000 in the last octet), the inverse is 00111111 = 63 → 0.0.0.63. The junior's error is the classic exam trap: subnet-mask thinking (1s = network) applied where wildcard thinking (0s = match) is required. Quick conversion: wildcard = 255.255.255.255 − subnet mask.",
    "hint": "In a wildcard mask, 0 means 'must match' — the opposite of a subnet mask. What's the inverse of 255.255.255.192?",
    "objectives": ["Convert subnet masks to wildcard masks", "Explain wildcard semantics"],
    "mins": 10,
    "evidence": ["Converted a /26 to wildcard 0.0.0.63 and explained match semantics"],
},
{
    "id": "netplus-subnetting-sc14",
    "title": "The /31 Point-to-Point Link",
    "domain_id": "subnetting-mastery",
    "situation": "Two routers need a point-to-point WAN link. The addressing plan is tight — only a /29 block is free, and four such links are needed. The engineer proposes /31s (RFC 3021) instead of the traditional /30s.",
    "prompt": "Is /31 correct here, and why?",
    "choices": [
        "No — every subnet needs network and broadcast addresses, so /30 is the minimum",
        "Yes — on point-to-point links there are only two hosts and no broadcast domain semantics needed, so RFC 3021 allows /31 (2 addresses, zero waste); four /31s fit in the /29 with room to spare, while /30s would need 16 addresses",
        "Yes, but only for Ethernet links",
        "/31s are only for IPv6"
    ],
    "answer": 1,
    "why": "RFC 3021 recognizes that point-to-point links have no broadcast domain: with exactly two endpoints, network and broadcast addresses are meaningless, so a /31 provides 2 usable addresses with zero waste versus a /30's 50% waste (2 usable of 4). Four /31 links consume 8 addresses — fitting comfortably in the /29 (8 addresses) — while four /30s would need 16. The exam tests /31 as the 'most efficient point-to-point' answer and expects you to know it doesn't apply to multi-access (Ethernet LAN) segments.",
    "hint": "On a link with exactly two devices, what are network and broadcast addresses actually for?",
    "objectives": ["Apply /31 addressing per RFC 3021", "Optimize point-to-point address use"],
    "mins": 10,
    "evidence": ["Justified /31 subnets for point-to-point links to eliminate address waste"],
},
],
"wireless-deep": [
{
    "id": "netplus-wireless-sc8",
    "title": "2.4 GHz Channel Planning",
    "domain_id": "wireless-deep",
    "situation": "A small office deploys three APs in a row down a hallway, all on 2.4 GHz. The installer left them all on channel 6 'for consistency.' Users complain of slow speeds despite strong signal bars.",
    "prompt": "What is the correct channel plan?",
    "choices": [
        "Keep all on channel 6 — same channel means seamless roaming",
        "Move them to non-overlapping channels 1, 6, and 11 — 2.4 GHz channels overlap, and only 1/6/11 are non-overlapping, so co-channel APs contend for airtime",
        "Use channels 3, 7, and 9 for finer granularity",
        "Disable 2.4 GHz entirely"
    ],
    "answer": 1,
    "why": "2.4 GHz channels are 5 MHz apart but each signal is ~22 MHz wide — adjacent channels overlap and interfere. Only channels 1, 6, and 11 are non-overlapping in the US, so three nearby APs must use exactly those (or fewer APs on 5 GHz). Same-channel APs don't 'roam seamlessly' — they share one collision domain and take turns talking (co-channel contention), which is why signal looks strong but throughput collapses. Channels 3/7/9 overlap with everything and are worse than sharing.",
    "hint": "Strong signal but slow speed with three APs on one channel — are they cooperating or contending?",
    "objectives": ["Plan non-overlapping 2.4 GHz channels", "Explain co-channel contention"],
    "mins": 12,
    "evidence": ["Redesigned a 2.4 GHz deployment onto channels 1, 6, 11"],
},
{
    "id": "netplus-wireless-sc9",
    "title": "Interference: The Microwave Mystery",
    "domain_id": "wireless-deep",
    "situation": "Every day at noon, the 2.4 GHz WLAN near the break room degrades sharply for 3-5 minutes, then recovers. Signal strength stays high throughout. The 5 GHz WLAN in the same area is unaffected.",
    "prompt": "What is the most likely cause?",
    "choices": [
        "Too many clients associating at lunch",
        "Non-Wi-Fi interference in 2.4 GHz — e.g., a microwave oven (2.4 GHz magnetron) in the break room leaking RF during lunchtime use",
        "The AP is overheating",
        "A rogue AP appears at noon"
    ],
    "answer": 1,
    "why": "The signature is precise: time-correlated (noon, 3-5 min = heating food), band-specific (2.4 GHz only — microwave magnetrons radiate ~2.45 GHz; 5 GHz unaffected), and signal stays high (the AP's signal is fine; the NOISE floor rises, crushing SNR). Wi-Fi tools show this as interference, not weak signal — high signal + low throughput + time pattern = non-802.11 interferer. Client count wouldn't be so sharply timed; overheating wouldn't spare 5 GHz; a rogue AP wouldn't follow a lunch schedule.",
    "hint": "High signal, crushed throughput, same time daily, only 2.4 GHz — what non-Wi-Fi device lives in break rooms and radiates at 2.4 GHz?",
    "objectives": ["Diagnose non-Wi-Fi interference", "Read the time/band/signal signature"],
    "mins": 12,
    "evidence": ["Attributed time-correlated 2.4 GHz degradation to microwave-oven interference"],
},
{
    "id": "netplus-wireless-sc10",
    "title": "The Sticky Client Roaming Problem",
    "domain_id": "wireless-deep",
    "situation": "In a warehouse with many APs, handheld scanners cling to a distant AP at -85 dBm instead of roaming to a nearby AP at -60 dBm. Voice calls drop as workers walk the aisles. The APs' transmit power is set to maximum.",
    "prompt": "What fixes roaming?",
    "choices": [
        "Increase AP transmit power further so the distant AP is even stronger",
        "Lower AP transmit power to match client power, enable 802.11r/k/v (fast roaming, neighbor reports, BSS transition), and set minimum-RSSI disassociation so clients roam instead of clinging",
        "Add more APs at maximum power",
        "Switch everything to 2.4 GHz for better range"
    ],
    "answer": 1,
    "why": "Roaming is the CLIENT's decision, and clients roam based on what they hear: max-power APs create huge overlapping cells where the client sees no reason to leave (sticky client). Lowering AP power to match the client's weaker transmit power creates right-sized cells with clean handoff boundaries; 802.11k gives clients neighbor lists, 802.11v suggests better APs, 802.11r makes the handoff fast enough for voice; min-RSSI kicks hopelessly distant clients. More power worsens stickiness; 2.4 GHz's longer range worsens it further.",
    "hint": "Who decides to roam — the AP or the client? And what does maximum power do to cell boundaries?",
    "objectives": ["Fix sticky-client roaming", "Apply 802.11r/k/v and power tuning"],
    "mins": 12,
    "evidence": ["Designed a roaming fix with balanced power, 802.11r/k/v, and min-RSSI"],
},
{
    "id": "netplus-wireless-sc11",
    "title": "WPA2 vs WPA3 Configuration",
    "domain_id": "wireless-deep",
    "situation": "A company is refreshing its WLAN security. The fleet is mixed: new laptops support WPA3, but warehouse scanners and some IoT sensors only support WPA2. Compliance requires the strongest feasible encryption on the corporate SSID.",
    "prompt": "What is the correct security configuration?",
    "choices": [
        "WPA3-only on the corporate SSID — security first, replace the old devices",
        "WPA2-Personal with a shared password everyone knows",
        "WPA3-SAE with transition mode (WPA3/WPA2 compatibility) for the mixed corporate SSID, plus a separate WPA2-only IoT SSID segmented via VLAN — and WPA2-Enterprise (802.1X) where a RADIUS server exists for per-user auth",
        "WEP with MAC filtering — lightweight for old devices"
    ],
    "answer": 2,
    "why": "WPA3's SAE handshake fixes WPA2's offline dictionary-attack weakness (captured handshakes can't be brute-forced offline), but a hard WPA3-only cutover bricks legacy devices — transition mode negotiates the best each client supports. Segmentation matters independently: IoT on its own SSID/VLAN contains their weaker posture. Where infrastructure allows, WPA2/WPA3-Enterprise with 802.1X/RADIUS replaces the shared PSK (one leaked password compromises everyone) with per-user credentials. WEP is broken in minutes; MAC filtering is trivially spoofed.",
    "hint": "You need the strongest handshake for new devices without bricking old ones — and should the scanners share the corporate SSID at all?",
    "objectives": ["Configure WPA3 transition mode", "Segment IoT wireless"],
    "mins": 12,
    "evidence": ["Designed WPA3-SAE transition with segmented IoT SSID and Enterprise auth path"],
},
{
    "id": "netplus-wireless-sc12",
    "title": "Reading the Site Survey",
    "domain_id": "wireless-deep",
    "situation": "A predictive site survey heatmap shows strong -55 dBm coverage in all offices, but the conference room shows -80 dBm with a neighboring floor's AP bleeding through at -75 dBm. Users report the conference room 'connects but barely works.'",
    "prompt": "What does the survey tell you to do?",
    "choices": [
        "Nothing — the whole floor has coverage",
        "Add/relocate an AP to serve the conference room (fix the -80 dBm dead zone) and reduce the bleeding AP's power or channel-separate it — the client hears the neighbor louder than its own AP, causing contention and poor SNR",
        "Turn up the conference room clients' Wi-Fi adapters",
        "Switch the conference room to a different SSID"
    ],
    "answer": 1,
    "why": "Heatmaps reveal two distinct problems: a coverage hole (-80 dBm is below the -67 dBm voice/data design threshold) and co-channel/containment failure (a foreign AP at -75 dBm is LOUDER than the serving signal — clients contend with it and suffer terrible signal-to-noise). The fix is physical/RF: place an AP to cover the room properly and tame the bleeder (lower its power, move it to a non-overlapping channel). Client-side tweaks and SSID changes don't fix an RF physics problem the survey has already localized.",
    "hint": "The client hears the neighbor's AP louder than its own — what does that do to usable signal?",
    "objectives": ["Interpret heatmap survey data", "Fix coverage holes and AP bleed"],
    "mins": 12,
    "evidence": ["Prescribed AP placement and power/channel changes from heatmap analysis"],
},
{
    "id": "netplus-wireless-sc13",
    "title": "The DFS Radar Event",
    "domain_id": "wireless-deep",
    "situation": "An office near an airport runs 5 GHz APs on channel 120. Several times a week, all 5 GHz clients simultaneously drop for exactly 30 minutes, then reconnect on their own. Logs show 'DFS radar detected, vacating channel.'",
    "prompt": "What is happening and what is the fix?",
    "choices": [
        "The APs are defective — replace them",
        "DFS (Dynamic Frequency Selection) is legally required on radar-shared 5 GHz channels: when the AP detects radar pulses (airport weather radar), it must vacate for 30 minutes (non-occupancy period). Fix: move APs to non-DFS channels (36-48, 149-165) to avoid radar-channel disruptions",
        "Increase channel width to 160 MHz to power through the radar",
        "Disable DFS in the AP settings"
    ],
    "answer": 1,
    "why": "Channels 52-144 in 5 GHz are shared with weather/military radar — regulators mandate DFS: detect radar, vacate immediately, stay off for 30 minutes. Near an airport, radar hits are routine, so DFS channels cause exactly this periodic mass-drop signature. The fix is architectural: use non-DFS UNII-1/UNII-3 channels (36-48, 149-165) where no radar sharing exists. Disabling DFS is illegal and firmware usually prevents it; wider channels on DFS spectrum just widen the outage; the APs are behaving correctly.",
    "hint": "The 30-minute outage is a regulatory timer, not a bug — which channels don't share spectrum with radar?",
    "objectives": ["Explain DFS behavior", "Select non-DFS channels near radar sources"],
    "mins": 12,
    "evidence": ["Diagnosed DFS radar vacating and moved APs to non-DFS channels"],
},
{
    "id": "netplus-wireless-sc14",
    "title": "Antenna Choice for the Hallway",
    "domain_id": "wireless-deep",
    "situation": "A long, narrow warehouse aisle needs Wi-Fi for scanners. The installer proposes high-gain omnidirectional antennas on the APs, reasoning 'more gain = better coverage everywhere.'",
    "prompt": "What is the correct antenna guidance?",
    "choices": [
        "High-gain omni is right — gain helps in all directions",
        "Use directional (patch/yagi) antennas aimed down the aisle: high-gain omnis flatten the radiation donut, wasting energy above/below and overshooting into neighboring aisles (more interference); directionals focus energy where clients actually are",
        "Antennas don't matter — only transmit power does",
        "Remove the antennas for a cleaner look"
    ],
    "answer": 1,
    "why": "Antenna gain doesn't create energy — it reshapes it. High-gain omnis squash the doughnut pattern flat: great for a single open floor, terrible for a narrow aisle (energy sprays sideways into adjacent aisles causing co-channel interference, while the aisle ends get little). Directional antennas concentrate the pattern down the aisle where the scanners are, improving both signal and isolation. EIRP regulations also cap total radiated power, so 'more gain + full power' can violate limits — another reason to shape rather than blast.",
    "hint": "Gain reshapes coverage, it doesn't create it — what shape does a long aisle need?",
    "objectives": ["Select antennas by coverage geometry", "Explain gain pattern trade-offs"],
    "mins": 10,
    "evidence": ["Specified directional antennas matched to aisle geometry over high-gain omnis"],
},
],
"wan-edge": [
{
    "id": "netplus-wan-sc8",
    "title": "MPLS vs Broadband Internet",
    "domain_id": "wan-edge",
    "situation": "A company connects 6 branches. Today they use expensive MPLS for everything. The CIO asks whether to move to business broadband with VPN, keep MPLS, or do both. Traffic is 70% cloud SaaS (internet-bound anyway) and 30% inter-branch.",
    "prompt": "What is the best WAN link decision?",
    "choices": [
        "Keep MPLS for everything — it's the most reliable",
        "Move everything to cheap broadband — cost wins",
        "Hybrid: keep MPLS (or SLA-backed links) for the latency-sensitive inter-branch traffic and shift internet-bound SaaS to broadband with VPN backup — match link quality and cost to traffic needs",
        "Drop all WAN links and use dial-up backup"
    ],
    "answer": 2,
    "why": "Link selection is traffic-matching: MPLS buys SLA-backed latency/jitter guarantees that matter for inter-branch real-time traffic, but it's wasted money for SaaS traffic that breaks out to the internet anyway (where the MPLS SLA ends at the provider edge). Broadband + VPN handles internet-bound traffic at a fraction of the cost with acceptable reliability. The hybrid design pays for guarantees only where guarantees matter — the core WAN design trade-off the exam tests.",
    "hint": "70% of traffic goes to the internet regardless — does it need an expensive private SLA to get there?",
    "objectives": ["Compare MPLS vs broadband VPN", "Match link type to traffic profile"],
    "mins": 12,
    "evidence": ["Designed a hybrid WAN matching link SLAs to traffic types"],
},
{
    "id": "netplus-wan-sc9",
    "title": "SD-WAN Policy: App-Aware Routing",
    "domain_id": "wan-edge",
    "situation": "A branch has two links: MPLS (low latency, expensive, 50 Mbps) and broadband (variable latency, cheap, 200 Mbps). The company runs VoIP, video conferencing, bulk file replication, and guest Wi-Fi backhaul over the WAN.",
    "prompt": "What SD-WAN policy best uses both links?",
    "choices": [
        "Active/passive: all traffic on MPLS, broadband only if MPLS fails",
        "Application-aware policies: VoIP/video pinned to MPLS (or steered by real-time latency/jitter measurements), bulk replication and guest traffic on broadband, with automatic failover and per-packet steering as link quality changes",
        "Round-robin load balancing ignoring traffic type",
        "Send everything over broadband — it's faster on paper"
    ],
    "answer": 1,
    "why": "SD-WAN's value is application-aware, measurement-driven path selection: it continuously probes both links (loss, latency, jitter) and steers each application to the path meeting its SLA — real-time voice/video get the stable low-jitter path, bulk traffic gets the fat cheap pipe. Active/passive wastes the broadband investment; round-robin sends voice down a jittery path half the time; 'faster on paper' ignores that broadband's 200 Mbps comes with variable latency that kills call quality. Policy = match app sensitivity to measured path quality, dynamically.",
    "hint": "Voice cares about jitter, backups care about bandwidth — should they take the same path?",
    "objectives": ["Design SD-WAN app-aware policies", "Explain dynamic path selection"],
    "mins": 12,
    "evidence": ["Built SD-WAN policies steering apps by SLA with dynamic failover"],
},
{
    "id": "netplus-wan-sc10",
    "title": "Failover Design: When the Primary Dies",
    "domain_id": "wan-edge",
    "situation": "A retail store's POS system needs WAN to the data center. The design has a primary fiber link and a 4G LTE backup. During a fiber cut last month, failover took 6 minutes — the POS was down, and the LTE link came up with a different public IP, breaking the site-to-site VPN.",
    "prompt": "What is the correct failover design fix?",
    "choices": [
        "Remove the LTE backup — it caused the VPN problem",
        "Faster failure detection (BFD/IP SLA tracking) for sub-minute failover, and run the site-to-site VPN with DPD/aggressive-mode or SD-WAN so the tunnel re-establishes automatically over the LTE link's new IP (design for dynamic endpoints)",
        "Manually reconfigure the VPN during each outage",
        "Buy a second fiber link from the same provider in the same trench"
    ],
    "answer": 1,
    "why": "Two defects: slow detection (6 minutes suggests dead-timer-based detection instead of BFD/IP SLA sub-second probes) and a VPN design that assumed static endpoints (LTE CGNAT IPs change — the tunnel must tolerate dynamic peers via DPD, dynamic DNS, or SD-WAN orchestration). A second fiber in the same trench shares the same backhoe fate (no path diversity). Failover design = detect fast + re-establish automatically + diverse paths; manual reconfiguration during an outage is not a design.",
    "hint": "Six minutes to notice, plus a VPN that can't handle the backup link's changing IP — which two mechanisms fix each?",
    "objectives": ["Design fast WAN failover", "Handle dynamic backup endpoints"],
    "mins": 12,
    "evidence": ["Designed sub-minute failover with BFD and dynamic-endpoint VPN"],
},
{
    "id": "netplus-wan-sc11",
    "title": "QoS for Voice: Taming Jitter",
    "domain_id": "wan-edge",
    "situation": "A 20 Mbps WAN link carries VoIP (needs ~2 Mbps) plus large file transfers. During backups, calls garble and drop. The router currently treats all traffic FIFO.",
    "prompt": "What QoS design fixes call quality?",
    "choices": [
        "Buy more bandwidth — QoS is a workaround",
        "Classify and mark voice with DSCP EF at the edge, give it strict priority queuing (LLQ) with a policed cap, and shape/deprioritize bulk traffic — bandwidth alone doesn't fix jitter and burst contention",
        "Block file transfers during business hours",
        "Enable QoS only on the LAN switches"
    ],
    "answer": 1,
    "why": "Voice's enemy isn't average bandwidth — it's jitter and burst contention: a file-transfer burst fills the FIFO queue and voice packets wait behind it, arriving late and garbled. The fix is a QoS chain: classify at the trusted edge, mark voice DSCP EF (the exam's voice marking), service it with low-latency priority queuing (with a policer so voice can't starve everything else), and shape bulk traffic. More bandwidth helps but a single burst still causes jitter without queuing; LAN-only QoS misses the WAN bottleneck where the contention actually happens.",
    "hint": "Calls need 2 Mbps of 20 — so why do they garble? Think about what a burst does to a FIFO queue.",
    "objectives": ["Design voice QoS with LLQ", "Explain jitter vs bandwidth"],
    "mins": 12,
    "evidence": ["Designed DSCP EF marking with priority queuing to protect voice from bulk bursts"],
},
{
    "id": "netplus-wan-sc12",
    "title": "VPN Tunnel Troubleshooting",
    "domain_id": "wan-edge",
    "situation": "A new site-to-site VPN shows Phase 1 up but Phase 2 won't establish. The remote admin 'hardened' their crypto last week. Local proposal: AES-256/SHA-256/DH14, lifetime 3600. You finally get their config: AES-128/SHA-1/DH2, lifetime 28800.",
    "prompt": "What is the diagnosis and fix?",
    "choices": [
        "The WAN link is too slow for Phase 2",
        "Phase 2 proposal mismatch on every parameter (encryption, integrity, DH group, lifetime) — both sides must agree on an identical transform set; align them (preferably to the stronger suite) on both ends",
        "Reboot both firewalls",
        "Phase 1 being up means Phase 2 should work — wait longer"
    ],
    "answer": 1,
    "why": "IPsec Phase 2 (Quick Mode) negotiates the actual data-protection SA: encryption algorithm, integrity algorithm, PFS DH group, and lifetimes must match exactly — here literally every parameter differs, so negotiation cannot succeed. Phase 1 only proves IKE connectivity and peer authentication; it says nothing about Phase 2 agreement. The fix is configuration alignment (and the 'hardening' story explains the drift — one side changed without coordinating). Reboots and patience don't reconcile mismatched crypto parameters.",
    "hint": "Phase 1 is the secure channel to negotiate over; Phase 2 negotiates the data protection — compare the two proposals line by line.",
    "objectives": ["Troubleshoot IPsec Phase 2 mismatches", "Align transform sets"],
    "mins": 12,
    "evidence": ["Diagnosed a four-parameter Phase 2 mismatch and prescribed transform-set alignment"],
},
{
    "id": "netplus-wan-sc13",
    "title": "Bandwidth Planning: Sizing the Link",
    "domain_id": "wan-edge",
    "situation": "A 30-person branch needs WAN sizing. Measured needs: VoIP 3 Mbps, video conferencing 8 Mbps peak, SaaS/cloud apps 15 Mbps, plus 25% growth headroom and headroom for bursts. The carrier offers 25, 50, or 100 Mbps.",
    "prompt": "What link size is correct, and why?",
    "choices": [
        "25 Mbps — close to today's 26 Mbps total, cheapest",
        "50 Mbps — covers the 26 Mbps measured need plus 25% growth (~33 Mbps) with burst headroom, without paying for 100 Mbps of idle capacity",
        "100 Mbps — never be constrained",
        "25 Mbps plus 'burst to 50' with no QoS"
    ],
    "answer": 1,
    "why": "Capacity planning = measured peak demand + growth factor + burst headroom, then the next standard tier up: 26 Mbps × 1.25 ≈ 33 Mbps → 50 Mbps tier. Sizing exactly to today's number guarantees congestion at the first growth spurt or burst (and 25 < 26 already fails). 100 Mbps wastes budget that could fund redundancy or QoS. The exam tests this disciplined method — measure, add growth, round up one tier — not 'buy the biggest' or 'squeeze into the cheapest.'",
    "hint": "Add the peaks, add growth, then pick the next tier up — what does the math say?",
    "objectives": ["Size WAN links with growth headroom", "Avoid under/over-provisioning"],
    "mins": 10,
    "evidence": ["Sized a WAN link from measured demand plus growth to the next standard tier"],
},
],
}
}

LESSONS = {
"comptia-security-plus": {
"concepts": [
{
    "_id": "secplus-concepts-defense-in-depth",
    "id": "secplus-concepts-defense-in-depth",
    "title": "Defense in Depth: Layering That Actually Works",
    "domain_id": "concepts",
    "concepts": [
        "Defense in depth means independent, overlapping controls across categories — administrative, technical, and physical — so no single failure equals compromise.",
        "Layer by attack path, not by product count: for email-borne attacks, stack filtering, user training, endpoint protection, and backups; each layer catches what the last missed.",
        "Diversity matters: two identical firewalls in series share the same bypass; a firewall plus application allowlisting plus behavioral monitoring fail independently.",
        "Measure layers by residual risk: after each control, ask what attack still succeeds, and place the next layer exactly there.",
        "The exam tests this as control selection: when asked for the BEST additional control, pick the one covering an unaddressed layer or attack path."
    ],
    "example": {
        "code": "Attack path: phishing email → credential theft → VPN login → lateral movement → data theft\nLayer 1 (prevent): email filtering + user training\nLayer 2 (block reuse): MFA on VPN\nLayer 3 (limit blast radius): network segmentation\nLayer 4 (detect): SIEM alert on impossible travel\nLayer 5 (recover): offline backups",
        "walkthrough": "Each layer addresses the attacker's next step. If phishing bypasses the filter, MFA stops the stolen credential; if MFA is bypassed, segmentation contains movement; if movement succeeds, the SIEM catches it; if all fails, backups enable recovery. No single layer is the plan — the overlap is."
    },
    "pitfalls": [
        "Stacking redundant same-type controls (two AV products) while leaving whole categories (backup, MFA) empty.",
        "Treating a bigger firewall as 'more layers' — one control point, however strong, is still one layer.",
        "Forgetting the human and recovery layers: training and backups are controls too, and the exam counts them."
    ],
    "try_it": "Pick ransomware as the threat. List five layers across at least three control categories that each independently blunt it."
}
],
"threats": [
{
    "_id": "secplus-threats-social-engineering",
    "id": "secplus-threats-social-engineering",
    "title": "Social Engineering: The Human Attack Surface",
    "domain_id": "threats",
    "concepts": [
        "Social engineering exploits trust, authority, urgency, and curiosity — not software flaws. Phishing (email), vishing (voice), smishing (SMS), and whaling (executive-targeted) differ only in channel and target.",
        "Pretexting builds a fabricated scenario (fake IT audit) while baiting offers something desirable (free USB, gift card) — the exam distinguishes them by the lure mechanism.",
        "Watering-hole attacks compromise sites the target already trusts; typosquatting registers lookalike domains — both abuse misplaced trust rather than tricking the user directly.",
        "The strongest controls are procedural: out-of-band verification (call back on a known number), least-privilege (limit what a fooled user can do), and tested awareness programs.",
        "On the exam, when the attacker's weapon is persuasion, the answer is almost always a human-layer or procedural control, not a technical product."
    ],
    "example": {
        "code": "Attack: caller claims to be the CEO, urgently needs a wire transfer.\nWeak response: comply fast to please the boss.\nStrong response: 'I'll call you back on your known number to confirm' → verify via org chart / out-of-band channel → escalate to finance controls (dual authorization).",
        "walkthrough": "Authority + urgency is the classic combo. The verification procedure breaks the attacker's leverage — a real CEO reached on a known number either confirms or exposes the fraud. Dual authorization means even a fooled employee can't complete the transfer alone."
    },
    "pitfalls": [
        "Answering social-engineering questions with technical controls (spam filter, AV) when the question asks for the BEST defense — procedure beats product here.",
        "Confusing pretexting (fabricated scenario) with baiting (enticing offer) or whaling (executive target) on definition questions.",
        "Assuming awareness training alone suffices — the exam wants layered answers: training PLUS verification procedures PLUS least privilege."
    ],
    "try_it": "Write a 3-step verification procedure for 'urgent wire transfer' requests and one for 'IT needs your password' calls."
}
],
"architecture": [
{
    "_id": "secplus-architecture-segmentation-zero-trust",
    "id": "secplus-architecture-segmentation-zero-trust",
    "title": "Segmentation and Zero Trust Architecture",
    "domain_id": "architecture",
    "concepts": [
        "Segmentation divides the network into isolated zones (VLANs, subnets, microsegments) so a compromise in one zone can't freely reach others — it contains lateral movement.",
        "A DMZ is a classic segment: public-facing servers live between two firewalls, isolated from both the internet and the internal LAN.",
        "Zero trust assumes breach and verifies every request: identity-based access, microsegmentation, continuous authentication, and least privilege — 'never trust, always verify.'",
        "Jump servers/bastion hosts and data diodes are segmentation tools: concentrate admin access through one hardened path; allow data to flow one way where needed.",
        "Exam logic: unpatchable or high-risk assets (IoT, legacy) get network containment; sensitive assets (databases, backups) get the most restrictive segments."
    ],
    "example": {
        "code": "Flat network:  [IoT] [Workstations] [DB] [Internet]  (one broadcast domain)\nSegmented:    Internet → FW → DMZ(web) → FW → Internal(VLAN10 users) → FW → Restricted(VLAN99 DB, backups)\n              IoT → isolated VLAN50, ACL: only → monitoring server, deny → all else",
        "walkthrough": "Each arrow is a firewall policy enforcement point. The IoT VLAN can't reach the DB VLAN at all — its ACL only permits monitoring traffic. Even if a camera is compromised, the blast radius ends at VLAN50. The DB sits in the most restricted segment with no internet path."
    },
    "pitfalls": [
        "VLANs without ACLs/firewalling between them are just labels — segmentation requires enforcement at the boundaries.",
        "Putting the backup server on the same segment as production — ransomware encrypts both; backups need isolated, ideally offline/air-gapped segments.",
        "Treating zero trust as a product purchase — it's an architecture of identity verification and microsegmentation, not a box."
    ],
    "try_it": "Sketch your home or lab network into 3 segments with firewall rules between them. Which segment holds the crown jewels?"
}
],
"operations": [
{
    "_id": "secplus-operations-patch-change",
    "id": "secplus-operations-patch-change",
    "title": "Patching and Change Management",
    "domain_id": "operations",
    "concepts": [
        "Change management types: standard (pre-approved, routine), normal (CAB-reviewed), and emergency (expedited for critical/active threats) — the exam loves asking which type fits.",
        "Patching priority follows risk: critical + actively exploited + internet-facing goes first; test patches in staging before production to avoid breaking changes.",
        "Every change needs: purpose, risk/impact assessment, backout plan, testing, approval, and documentation — emergency changes compress but don't skip these.",
        "Vulnerability scanning finds the flaws; patch management fixes them; change control governs the fixing — three linked processes, and the exam distinguishes them.",
        "Maintenance windows and SLAs constrain when changes happen — operations security is the art of staying both secure and available."
    ],
    "example": {
        "code": "Emergency change ticket:\n  Change: VPN concentrator CVE-2026-XXXX (RCE, exploited in wild)\n  Risk of change: 30-min VPN outage | Risk of NOT changing: remote compromise\n  Backout: snapshot + previous firmware on standby\n  Approval: on-call director (emergency path) | Test: staging concentrator\n  Implement: 22:00 | Verify: vuln scan + login test | Document: ticket + CMDB",
        "walkthrough": "This is the emergency path done right: the risk comparison justifies the expedite, the backout plan bounds the downside, staging validation catches bad patches, and documentation keeps the audit trail. Speed without these is just recklessness with a ticket number."
    },
    "pitfalls": [
        "Patching production directly with no staging test or backout plan — one bad patch becomes an outage you can't reverse.",
        "Treating emergency change as 'no process' — it still needs approval, risk assessment, and documentation, just faster.",
        "Scanning without remediating: a vulnerability report nobody acts on is just a prioritized attacker shopping list."
    ],
    "try_it": "Write an emergency-change justification for a critical firewall patch in 5 lines: risk of change vs risk of delay, backout, approval, verification."
}
],
"exam-strategy": [
{
    "_id": "secplus-exam-strategy-pbq-mastery",
    "id": "secplus-exam-strategy-pbq-mastery",
    "title": "PBQ Mastery: Earning Partial Credit",
    "domain_id": "exam-strategy",
    "concepts": [
        "PBQs (performance-based questions) simulate real tasks: firewall rules, log analysis, attack-type matching, port/protocol drag-and-drops — and they award partial credit, so every reasoned placement scores.",
        "Method first: read the goal, inventory the given artifacts (diagram, logs, tiles), translate the goal into rules, place deliberately, then verify each requirement against your answer.",
        "Common PBQ types and their keys: firewall rules (top-down, specific-before-deny-all), log analysis (timestamps + source/dest + action tell the story), matching (eliminate the certain ones first).",
        "Time-box PBQs: attempt them in the second pass after banking multiple-choice points; never let one PBQ consume 15 minutes while 20 answerable questions wait.",
        "If the interface confuses you, use the tutorial time before the exam starts — that clock doesn't count against you."
    ],
    "example": {
        "code": "PBQ: 'Order these incident response steps.'\nTiles: Eradicate | Contain | Recover | Identify | Lessons-learned | Prepare\nMethod: recall the lifecycle order → Prepare, Identify, Contain, Eradicate, Recover, Lessons-learned.\nVerify: does containment come before eradication? Yes — stop the bleeding, then remove the cause.",
        "walkthrough": "Even under interface stress, the method holds: the question is really testing the IR lifecycle order you already memorized. Translate tiles into the known sequence, place, then sanity-check adjacent pairs (contain-before-eradicate, recover-before-lessons-learned) before submitting."
    },
    "pitfalls": [
        "Submitting a PBQ with empty slots — partial credit means a reasoned guess beats a blank every time.",
        "Doing PBQs first and running out of time for 30 multiple-choice questions you could have answered in the same minutes.",
        "Misreading the goal (e.g., ordering rules bottom-up) — re-read the objective sentence twice before placing anything."
    ],
    "try_it": "Take any 6-step process from your notes (IR lifecycle, forensics order, risk management). Write the steps on slips, shuffle, and reorder from memory in under 60 seconds."
}
],
"soc-playbook": [
{
    "_id": "secplus-soc-playbook-triage-playbook",
    "id": "secplus-soc-playbook-triage-playbook",
    "title": "The SOC Triage Playbook",
    "domain_id": "soc-playbook",
    "concepts": [
        "Triage in 60 seconds per alert: Is it real (true positive?), does it matter (asset criticality + data sensitivity?), what's the blast radius — then prioritize, contain, or close with a note.",
        "Severity ≠ priority: a 'critical' alert on a lab VM ranks below a 'medium' on the domain controller — always multiply by asset value and data exposure.",
        "Enrich before you escalate: pull asset owner, recent changes, threat intel on the IOC, and related alerts — escalations with context get actioned, bare alerts get bounced.",
        "Know your escalation triggers cold: C2 patterns, credential dumping, ransomware behavior, data exfiltration, executive account anomalies — pattern-match, don't investigate to certainty at L1.",
        "Close the loop: every triaged alert gets a disposition (true/false positive, benign) — dispositions are what tune the SIEM and prove the SOC's value."
    ],
    "example": {
        "code": "Alert: 'Suspicious PowerShell' on WKST-2142 (intern laptop)\n60-second triage:\n  Real? → encoded -enc flag + external IP → yes, suspicious\n  Matters? → intern laptop, no sensitive data → low asset value\n  Blast radius → single host, no lateral signs → contained\n  Action → isolate host (cheap, reversible), escalate to L2 with enrichment\nDisposition: true positive, contained, escalated.",
        "walkthrough": "The triage answers three questions in order and produces a decision plus a paper trail. Isolation is cheap insurance while L2 investigates; the enrichment (encoded flag, external IP, asset context) is what makes the escalation useful instead of a bare forward."
    },
    "pitfalls": [
        "Treating every alert as equal — queue order or raw severity without asset context is how real breaches hide behind noisy lab alerts.",
        "Escalating without enrichment — 'suspicious thing on a host, please advise' wastes everyone's time; add IOC intel and asset context first.",
        "Never dispositioning false positives — the SIEM never learns, the same noise returns tomorrow, and alert fatigue deepens."
    ],
    "try_it": "Take three hypothetical alerts (ransomware on kiosk, impossible travel on CEO, port scan on DMZ). Triage each in 60 seconds: real? matters? blast radius? disposition?"
}
],
"crypto-lab": [
{
    "_id": "secplus-crypto-lab-pki-lifecycle",
    "id": "secplus-crypto-lab-pki-lifecycle",
    "title": "PKI and the Certificate Lifecycle",
    "domain_id": "crypto-lab",
    "concepts": [
        "PKI binds identities to public keys via certificates: the CA signs the binding, and anyone trusting the CA trusts the certificates — trust flows downhill from the root.",
        "Hierarchy: offline root CA (signs rarely, locked away) → online intermediate CAs (daily issuance) → end-entity certificates. Compromise scope shrinks as you go down.",
        "Certificate lifecycle: generate CSR → validate identity → issue → deploy → monitor expiry → renew/reissue → revoke if compromised (CRL or OCSP) — expiry and revocation are the exam's favorite failure points.",
        "Validation types: DV (domain control), OV (organization identity), EV (rigorous vetting) — increasing trust assurance, and the exam asks which fits a scenario.",
        "Key protection: private keys in HSMs or secure stores, never in code repos or emails; key escrow for recovery where policy requires it."
    ],
    "example": {
        "code": "Lifecycle in practice:\n  openssl req -new -newkey rsa:2048 -keyout web.key -out web.csr\n  → submit CSR to CA → CA validates domain (DV) → issues web.crt\n  → deploy cert + key on server → monitor: alert 30 days before expiry\n  → compromise? → revoke: publish to CRL / OCSP responder → reissue",
        "walkthrough": "The private key never leaves your control — only the CSR (containing the public key) goes to the CA. Expiry monitoring prevents the classic outage (expired cert = down site), and revocation via CRL/OCSP is how you kill a compromised certificate's trust before it expires naturally."
    },
    "pitfalls": [
        "Letting certificates expire — the most common PKI outage; automate renewal and alerting.",
        "Generating the private key on the CA or emailing it — the private key must be born and live where it will be used, protected.",
        "Forgetting revocation: a compromised cert that's merely left to expire stays trusted until expiry — revoke immediately via CRL/OCSP."
    ],
    "try_it": "Generate a CSR with openssl, inspect a real site's certificate in your browser (issuer chain, SANs, expiry), and check its OCSP status."
}
],
"incident-response": [
{
    "_id": "secplus-incident-response-ir-lifecycle",
    "id": "secplus-incident-response-ir-lifecycle",
    "title": "The IR Lifecycle as a System",
    "domain_id": "incident-response",
    "concepts": [
        "The lifecycle: Preparation → Detection & Analysis → Containment → Eradication → Recovery → Lessons Learned — and lessons learned feeds back into preparation, closing the loop.",
        "Preparation is the highest-leverage phase: playbooks, contact lists, backup tests, and tabletop exercises decide the incident's outcome before it starts.",
        "Containment (stop the bleeding: isolate, don't power off) precedes eradication (remove the cause) precedes recovery (restore service) — order matters because each step depends on the last.",
        "Communication runs parallel to all phases: internal escalation, legal, PR, customers, regulators — on legally defined timelines, through designated spokespeople.",
        "The exam tests sequencing ('what FIRST?') relentlessly: identify before contain, contain before eradicate, eradicate before recover, and document throughout."
    ],
    "example": {
        "code": "Ransomware at 02:00:\n  Detect: SIEM mass-encryption alert → analyst confirms (Analysis)\n  Contain: EDR-isolate affected hosts, block C2 at firewall (keep powered on!)\n  Eradicate: identify patient zero + persistence, rebuild from gold images\n  Recover: restore from verified-clean offline backups, verify integrity\n  Lessons: blameless review → patch SLA + email filtering + backup tests → update playbook",
        "walkthrough": "Each phase's output feeds the next: analysis tells containment what to isolate; containment preserves the evidence eradication needs; eradication must complete before recovery (restoring onto still-compromised hosts re-infects); lessons learned becomes next quarter's preparation. Skip or reorder a phase and the incident recurs."
    },
    "pitfalls": [
        "Eradicating before containing — you remove one implant while the attacker plants three more through the still-open channel.",
        "Recovering before eradicating — restoring backups onto compromised hosts re-infects immediately.",
        "Skipping lessons learned — the same entry vector works again next quarter; the loop stays open."
    ],
    "try_it": "Run a 20-minute tabletop: 'phishing → ransomware on two hosts.' Walk your team (or yourself) through all six phases with assigned owners."
}
]
},
"comptia-network-plus": {
"concepts": [
{
    "_id": "netplus-concepts-osi-encapsulation",
    "id": "netplus-concepts-osi-encapsulation",
    "title": "OSI Model and Encapsulation",
    "domain_id": "concepts",
    "concepts": [
        "The OSI model's seven layers (Physical, Data Link, Network, Transport, Session, Presentation, Application) give every network problem an address — troubleshooting is the art of finding the right floor.",
        "Encapsulation: each layer wraps the payload with its header (and sometimes trailer) — data → segment (TCP) → packet (IP) → frame (Ethernet) → bits. Decapsulation reverses it at the destination.",
        "The PDU names are exam currency: L4 segment/datagram, L3 packet, L2 frame, L1 bits — questions use them precisely.",
        "TCP (connection-oriented, reliable, sequenced) vs UDP (connectionless, fast, best-effort): the choice follows the application's tolerance for loss vs delay.",
        "Troubleshoot top-down or bottom-up systematically: 'works by IP, fails by name' = upper layers; 'no link light' = Layer 1 — never skip layers randomly."
    ],
    "example": {
        "code": "Sending 'HELLO':\n  L7: data = 'HELLO'\n  L4: + TCP header (ports, seq#)      → segment\n  L3: + IP header (src/dst IP)       → packet\n  L2: + Ethernet header/trailer (MACs, FCS) → frame\n  L1: → bits on the wire\nReceiving reverses: NIC checks FCS → IP checks dst → TCP orders by seq# → app reads 'HELLO'",
        "walkthrough": "Each header answers a question for its layer: TCP's ports identify the application, IP's addresses route across networks, Ethernet's MACs deliver across one link, the FCS detects corruption. The layer that can't answer its question is where the fault lives."
    },
    "pitfalls": [
        "Memorizing the layer names without the PDU names and device mappings (hub=L1, switch=L2, router=L3) — the exam tests all three together.",
        "Confusing TCP and UDP use cases: DNS and VoIP/streaming favor UDP; file transfer and web favor TCP.",
        "Troubleshooting by guessing instead of isolating — 'reboot everything' is never the methodology answer."
    ],
    "try_it": "Take a ping that fails. List one check per OSI layer, bottom-up, that isolates the fault — then run them on a real connectivity problem."
}
],
"implementation": [
{
    "_id": "netplus-implementation-cabling-media",
    "id": "netplus-implementation-cabling-media",
    "title": "Cabling, Media, and Connectors",
    "domain_id": "implementation",
    "concepts": [
        "Copper categories: Cat5e (1 Gbps/100m), Cat6 (10 Gbps/55m), Cat6A (10 Gbps/100m) — pick by speed, distance, and PoE heat; the 100-meter limit includes patch cords.",
        "Fiber: multimode (short, LED/laser, cheaper optics) vs single-mode (long-haul, laser, costlier) — distance and budget decide; connectors: LC (small, common), SC, ST, MPO for high-density.",
        "TIA/EIA 568A vs 568B wiring standards — use one consistently; crossover cables (now largely replaced by Auto-MDIX) swap transmit/receive pairs.",
        "EMI rules: keep copper away from power lines and fluorescent ballasts, respect bend radius, never kink fiber; plenum-rated cable where air-handling spaces require it.",
        "PoE standards (802.3af/at/bt) deliver power with data — verify the switch's PoE budget covers all powered devices before deployment."
    ],
    "example": {
        "code": "Run plan for a 90m camera drop:\n  Distance: 90m < 100m ✓ copper OK\n  PoE++ (cameras + heaters): Cat6A (heat dissipation in bundles)\n  Path crosses electrical room: reroute or use shielded (F/UTP)\n  Termination: 568B both ends (straight-through), test with certifier\n  Budget: camera 25W × 8 = 200W < switch 370W PoE budget ✓",
        "walkthrough": "Every line is a constraint check: distance against the 100m rule, cable category against PoE heat, path against EMI, termination standard for consistency, and power budget against the switch's capacity. Media implementation is constraint satisfaction, not brand shopping."
    },
    "pitfalls": [
        "Exceeding 100m on copper (including patch cords at both ends) and blaming the switch for the resulting flakiness.",
        "Mixing 568A and 568B terminations on one run — creates a crossover where you didn't want one.",
        "Deploying PoE devices without checking the switch's total power budget — the last camera never powers on."
    ],
    "try_it": "Terminate a Cat6 keystone jack to 568B, test with a cable verifier, and measure the full channel length — confirm it's under 100m."
}
],
"net-security": [
{
    "_id": "netplus-net-security-hardening",
    "id": "netplus-net-security-hardening",
    "title": "Hardening the Network",
    "domain_id": "net-security",
    "concepts": [
        "Switch hardening: disable unused ports, enable port security (MAC limiting/sticky), DHCP snooping with trusted uplinks, Dynamic ARP Inspection, and BPDU guard on access ports.",
        "802.1X port-based authentication with RADIUS ensures only authenticated devices (and users) get network access — the answer to 'rogue device on the LAN' questions.",
        "Wireless hardening: WPA3-SAE (or WPA2-Enterprise), disable WPS, change defaults, segment guest/IoT traffic, and manage APs from a controller with rogue-AP detection.",
        "Router/firewall hardening: change default credentials, disable unused services, use ACLs with least privilege, keep firmware patched, and log to a central SIEM.",
        "Physical security counts: lock closets, secure console ports, and control who can plug into wall jacks — the exam treats physical access as a security boundary."
    ],
    "example": {
        "code": "Access-port hardening template:\n  switchport mode access\n  switchport port-security maximum 2\n  switchport port-security violation restrict\n  ip dhcp snooping limit rate 15\n  spanning-tree bpduguard enable\n  authentication port-control auto   (802.1X via RADIUS)",
        "walkthrough": "Each line closes a specific attack: port-security caps MACs (stops CAM flooding and casual rogue devices), DHCP snooping rate-limits plus trusted-port design kills rogue DHCP, BPDU guard stops STP manipulation from access ports, and 802.1X requires authentication before the port forwards anything. Hardening is layered, like everything in security."
    },
    "pitfalls": [
        "Enabling 802.1X without a working RADIUS server or a plan for printers/IoT (MAB) — you lock out the business, not just attackers.",
        "Port security with 'shutdown' violation mode on user ports — one new phone MAC and the port dies until someone re-enables it; 'restrict' is usually safer.",
        "Hardening the network while leaving default credentials on the APs and switches themselves."
    ],
    "try_it": "Audit one switch: list unused ports, check for default credentials, and verify DHCP snooping and port security status."
}
],
"net-troubleshoot": [
{
    "_id": "netplus-net-troubleshoot-methodology",
    "id": "netplus-net-troubleshoot-methodology",
    "title": "The Troubleshooting Methodology",
    "domain_id": "net-troubleshoot",
    "concepts": [
        "The CompTIA sequence: Identify the problem → Establish a theory → Test the theory → Establish a plan of action → Implement (or escalate) → Verify full functionality → Document findings.",
        "Identify means gather: question users, check logs, note recent changes, duplicate the symptom — most 'mysteries' die at this step when someone checks the obvious.",
        "Theorize from evidence, then test cheaply: question the obvious before the exotic, and change one variable at a time so you know what fixed it.",
        "Common utilities map to layers: ping/traceroute (L3 reachability/path), ipconfig/ifconfig (addressing), nslookup/dig (DNS), netstat/ss (ports/connections), cable tester/loopback (L1).",
        "Document everything: symptoms, theories tested, the fix, and preventive measures — documentation is a scored methodology step, not optional paperwork."
    ],
    "example": {
        "code": "Symptom: one user can't reach the intranet.\n  Identify: link light off; only this user; worked yesterday.\n  Theory: Layer 1 fault on this drop (cable/NIC/port).\n  Test: swap cable → link up. (One variable changed.)\n  Plan/Implement: replace the damaged cable.\n  Verify: user reaches intranet; check for collateral issues.\n  Document: ticket notes + replace aging cable batch in that office.",
        "walkthrough": "The methodology prevented a wild goose chase: the link light (identify) pointed at Layer 1, the single-variable test proved the cable, and verification plus documentation closed the loop. Skipping to 'reinstall the OS' would have wasted an hour and taught nothing."
    },
    "pitfalls": [
        "Changing multiple things at once — you 'fix' it but never learn what was broken, and the exam penalizes this.",
        "Skipping verification: the symptom disappears but the root cause persists (e.g., rebooting instead of replacing the failing cable).",
        "Forgetting documentation — on the exam, 'document findings' is explicitly the final step and appears in answer choices."
    ],
    "try_it": "Break something in a lab (unplug a cable, set a wrong mask). Troubleshoot it strictly in methodology order, writing down each step."
}
],
"systems-anatomy": [
{
    "_id": "netplus-systems-anatomy-packet-journey",
    "id": "netplus-systems-anatomy-packet-journey",
    "title": "Anatomy of a Packet's Journey",
    "domain_id": "systems-anatomy",
    "concepts": [
        "Every packet journey has the same acts: host builds it (encapsulation) → switch forwards the frame by MAC → router routes the packet by IP, rewriting the frame → NAT/firewall translate as needed → destination decapsulates.",
        "MAC addresses are hop-local (rewritten at every router); IP addresses are end-to-end (preserved across the journey) — this single distinction unlocks switching vs routing questions.",
        "ARP is the bridge between worlds: 'who has this IP?' asked on the local link, answered with a MAC — routers ARP for next hops, hosts ARP for gateways.",
        "Return traffic mirrors the journey: the server replies to the source IP through its own gateway, and stateful devices (NAT, firewalls) recognize the return flow.",
        "Trace any failure by walking the journey: where does the packet stop? The last device that had it names the fault domain."
    ],
    "example": {
        "code": "PC (10.1.1.10) → web server (203.0.113.80):\n  PC: dst IP not local → ARP for gateway 10.1.1.1 → frame to gateway MAC\n  Switch: forwards frame by MAC table\n  Router: strips frame, routes by dst IP, builds NEW frame to next hop\n  Firewall: state table entry created, NAT src → public IP\n  ISP routers: hop-by-hop MAC rewrite, IP preserved\n  Server: decapsulates → app responds; return path mirrors back",
        "walkthrough": "Watch the two addressing schemes diverge: the frame's MACs change at every router (local delivery vehicles), while the packet's IPs stay constant (the end-to-end passport). NAT is the one place the source IP changes — a deliberate, stateful exception the firewall tracks so replies find their way home."
    },
    "pitfalls": [
        "Thinking MAC addresses travel end-to-end — they don't; each router re-frames.",
        "Forgetting ARP: 'host can't reach its gateway' is often just a failed or poisoned ARP, not a routing problem.",
        "Ignoring the return path — asymmetric or blocked return traffic breaks connections that look fine outbound."
    ],
    "try_it": "Run traceroute to a distant site. For each hop, state which header changed (MAC) and which didn't (IP) — narrate the journey out loud."
}
],
"exam-strategy": [
{
    "_id": "netplus-exam-strategy-subnetting-cheatsheet",
    "id": "netplus-exam-strategy-subnetting-cheatsheet",
    "title": "The 60-Second Subnetting Cheat Sheet",
    "domain_id": "exam-strategy",
    "concepts": [
        "Memorize the CIDR block-size table for the interesting octet: /24=1, /25=128, /26=64, /27=32, /28=16, /29=8, /30=4 — block size = 256 − mask value.",
        "Two formulas solve everything: subnets = 2^(borrowed bits), usable hosts = 2^(host bits) − 2. Borrowed = new mask − old mask.",
        "For 'which subnet does this IP belong to': find the interesting octet, compute block size, count blocks from zero to bracket the address.",
        "During the pre-exam tutorial (clock not running), dump the table and formulas onto the scratch sheet — then it's pure arithmetic under pressure.",
        "Drill target: any standard subnetting question in under 30 seconds. Speed here buys minutes for PBQs."
    ],
    "example": {
        "code": "Q: Subnet, broadcast, and range for 172.16.88.99/20?\n  Interesting octet: 3rd (mask 255.255.240.0). Block size = 256−240 = 16.\n  Blocks: 0,16,32,48,64,80,96 → 88 falls in 80.\n  Subnet: 172.16.80.0 | Broadcast: 172.16.95.255 (next block − 1)\n  Usable: 172.16.80.1 − 172.16.95.254  (20 seconds)",
        "walkthrough": "No binary needed: block size gives the subnet boundaries, the next block minus one gives the broadcast, and .1/first to last-minus-one gives the usable range. The whole question reduces to counting by 16s."
    },
    "pitfalls": [
        "Counting the network and broadcast as usable hosts — the −2 exists for exactly this trap.",
        "Borrowing bits from /24 when the question gives a different starting mask (e.g., subnetting a /20).",
        "Doing binary longhand on exam day — it's accurate but too slow; the block-size method is the exam technique."
    ],
    "try_it": "Dump the /24–/30 block-size table from memory in under 60 seconds. Then solve 10 random subnetting questions against a 30-second timer."
},
{
    "_id": "netplus-exam-strategy-pbq-wiring",
    "id": "netplus-exam-strategy-pbq-wiring",
    "title": "PBQ Tactics: Wiring and Diagrams",
    "domain_id": "exam-strategy",
    "concepts": [
        "Network+ PBQs cluster around: wiring diagrams (media by constraint), device placement (AP/switch/router in a topology), CLI troubleshooting (spot the misconfiguration), and port/protocol matching.",
        "Wiring PBQ method: for each run, name the governing constraint — distance (>100m = fiber), EMI (fiber), PoE/heat (Cat6A), ISP handoff (fiber) — then place and re-verify.",
        "CLI PBQ method: read the config line by line against the symptom; the fault is usually one wrong value (mask, gateway, VLAN, duplex) — diff the config against the requirement.",
        "Partial credit is generous: place everything you can reason about, make your best guess on the rest — blanks score zero.",
        "Do PBQs in the second pass: bank the quick multiple-choice points first, then spend your remaining time where partial credit rewards careful work."
    ],
    "example": {
        "code": "PBQ: place devices in a branch diagram.\n  'Connects 3 VLANs, routes between them' → Layer 3 switch or router\n  'Extends wireless to warehouse aisle' → AP with directional antenna\n  'Connects branch to ISP' → edge router at the demarc\n  Verify: does each device's capability match its job? (AP doesn't route VLANs.)",
        "walkthrough": "Each placement is a job description matched to a device's capabilities. The verification pass catches the classic trap — placing a Layer 2 switch where inter-VLAN routing is required. Reason from function, not from what 'looks right' in the diagram."
    },
    "pitfalls": [
        "Placing devices by familiarity instead of by the stated requirement — re-read each label's job description.",
        "Leaving PBQ slots empty out of perfectionism — partial credit rewards attempted reasoning.",
        "Burning 15 minutes on one PBQ while 20 quick questions wait — time-box and return."
    ],
    "try_it": "Draw a small office floor plan. Label 6 runs/devices with constraints, then have a study partner place media and devices — grade each other's reasoning."
},
{
    "_id": "netplus-exam-strategy-question-patterns",
    "id": "netplus-exam-strategy-question-patterns",
    "title": "Question Patterns and Distractor Traps",
    "domain_id": "exam-strategy",
    "concepts": [
        "'MOST likely' = weigh the evidence: the answer is the cause best supported by ALL the clues, not the scariest or most technical option.",
        "'FIRST'/'NEXT' = methodology order: information-gathering beats action; identify before theory, theory before test, containment of evidence before fixes.",
        "'BEST' = optimize for the stated goal: cheapest, fastest, most secure, least disruptive — the goal word in the question picks the winner among plausible options.",
        "Distractor patterns: the exact-wrong-value (off-by-one mask), the right-concept-wrong-layer (VLAN for a Layer 1 symptom), and the overkill option (replace the router for a bad cable).",
        "Absolute words ('always,' 'never') in answer choices are usually wrong — real networks are conditional, and the exam knows it."
    ],
    "example": {
        "code": "Q: 'Link light off, one user affected. MOST likely cause?'\n  A) Faulty NIC/cable  B) VLAN misconfiguration  C) DNS failure  D) Duplex mismatch\n  Evidence: link light OFF = Layer 1 verdict → B, C, D all need link UP.\n  Answer: A — the evidence eliminates everything above Layer 1.",
        "walkthrough": "The pattern: each clue is a filter. 'Link light off' filters out every answer above Layer 1; 'one user' filters out switch-wide faults. What's left standing after the filters is the answer — you barely need to know what a duplex mismatch is."
    },
    "pitfalls": [
        "Choosing the most technical-sounding answer when the evidence points at something simple — the exam rewards evidence, not sophistication.",
        "Ignoring the goal word (BEST/cheapest vs BEST/most secure) — two options can both 'work' while only one fits the stated optimization.",
        "Second-guessing filtered answers back in — if the evidence eliminated it, keep it eliminated."
    ],
    "try_it": "Take 10 practice questions. Before answering, write the goal word and list which clues eliminate which options — answer from the eliminations."
}
],
"subnetting-mastery": [
{
    "_id": "netplus-subnetting-vlsm-design",
    "id": "netplus-subnetting-vlsm-design",
    "title": "VLSM Design From Scratch",
    "domain_id": "subnetting-mastery",
    "concepts": [
        "VLSM lets each subnet use a different mask, sized to its host count — the alternative (one mask for all) wastes addresses on small subnets and starves large ones.",
        "Design order is largest-first: sort requirements descending, allocate each from where the last ended — this prevents fragmentation that strands unusable gaps.",
        "Size each block: hosts needed → next power of 2 ≥ hosts+2 (network+broadcast) → prefix length = 32 − exponent. 100 hosts → 128 → /25.",
        "Track allocation on paper: network address, mask, usable range, broadcast — then the next block starts at the previous broadcast + 1.",
        "Reserve growth and point-to-point links explicitly: WAN links get /30 (or /31); always leave an unallocated block for the requirement you forgot."
    ],
    "example": {
        "code": "192.168.8.0/24 → LAN-A 60 hosts, LAN-B 28, LAN-C 12, 2× WAN links\n  LAN-A: 60+2 → 64 → /26 → 192.168.8.0/26   (.1–.62, bcast .63)\n  LAN-B: 28+2 → 32 → /27 → 192.168.8.64/27  (.65–.94, bcast .95)\n  LAN-C: 12+2 → 16 → /28 → 192.168.8.96/28  (.97–.110, bcast .111)\n  WAN1:  /30 → 192.168.8.112/30   WAN2: /30 → 192.168.8.116/30\n  Remaining: 192.168.8.120–.255 free for growth ✓",
        "walkthrough": "Largest-first keeps the blocks packed: each allocation starts exactly where the previous broadcast ended. The +2 in the sizing accounts for network and broadcast addresses — the classic off-by-one that undersizes LAN-A to a /27 (30 hosts) and breaks the design. Note the reserved tail: real designs leave room."
    },
    "pitfalls": [
        "Forgetting the +2 (network and broadcast) when sizing — 60 hosts needs 62 addresses minimum, which is a /26, not a /27.",
        "Allocating smallest-first, which fragments the space and strands gaps too small for the big LANs.",
        "Overlapping blocks from arithmetic slips — always verify: next network = previous broadcast + 1."
    ],
    "try_it": "Design VLSM for 10.5.0.0/22 with: 400 hosts, 180 hosts, 90 hosts, 40 hosts, and 4 WAN links. Verify no overlaps."
}
],
"wireless-deep": [
{
    "_id": "netplus-wireless-channel-rf",
    "id": "netplus-wireless-channel-rf",
    "title": "RF Essentials: Channels, Power, and Antennas",
    "domain_id": "wireless-deep",
    "concepts": [
        "2.4 GHz: only channels 1, 6, 11 are non-overlapping — everything else interferes with its neighbors; 5 GHz offers many non-overlapping 20/40/80 MHz channels (minus DFS radar channels near airports).",
        "Channel width trades speed for airtime: wider channels (40/80/160 MHz) are faster but consume more spectrum and suffer more interference — 20 MHz is often right for dense 2.4 GHz.",
        "Power tuning: match AP transmit power to client power so cells are symmetric; too much power creates sticky clients and co-channel interference, too little creates dead zones.",
        "Antennas shape coverage: omnidirectional for open areas, directional (patch/yagi) for aisles and point-to-point bridges, MIMO/multiple streams for throughput.",
        "The exam's RF math is light but real: know dBm direction (higher = stronger), the −67 dBm design target for voice/data, and that 3 dB ≈ double/halve power."
    ],
    "example": {
        "code": "Dense office, 12 APs:\n  2.4 GHz radios: channels 1, 6, 11 reused in a honeycomb pattern, 20 MHz width, medium power\n  5 GHz radios: non-DFS channels 36–48, 149–165, 40 MHz width\n  Survey target: −67 dBm cell edge, 15–20% cell overlap for roaming\n  Result: no co-channel neighbors within earshot, clean handoffs",
        "walkthrough": "The honeycomb reuses the only three non-overlapping 2.4 GHz channels so adjacent APs never share one; 5 GHz gets the wide-open non-DFS channels; medium power keeps cells tight enough that clients roam instead of clinging. Every choice serves the −67 dBm edge target with overlap for handoffs."
    },
    "pitfalls": [
        "Leaving all APs on auto-channel at full power — they cluster on channel 6 and shout over each other.",
        "Using 40 MHz channels in 2.4 GHz in dense areas — you consume two of the three clean channels and interfere with everything.",
        "Deploying high-gain omnis to 'fix' a dead zone — gain reshapes coverage; it doesn't fill holes behind obstructions."
    ],
    "try_it": "With a Wi-Fi analyzer app, map your space: note channels in use, signal at the farthest seat, and whether 1/6/11 discipline is being followed."
}
],
"wan-edge": [
{
    "_id": "netplus-wan-edge-sdwan-qos",
    "id": "netplus-wan-edge-sdwan-qos",
    "title": "SD-WAN and QoS at the Edge",
    "domain_id": "wan-edge",
    "concepts": [
        "SD-WAN replaces static WAN routing with centralized, application-aware policy: the controller steers traffic per-app across MPLS, broadband, and LTE based on real-time link measurements.",
        "Path selection inputs: loss, latency, jitter measured continuously per tunnel — voice goes to the low-jitter path, bulk to the high-bandwidth path, automatically and per-packet if needed.",
        "QoS chain: classify at the trusted edge → mark (DSCP EF for voice, AF for video/data classes) → queue (LLQ priority for voice, CBWFQ for classes) → police/shape to bounds.",
        "Zero-touch provisioning lets branches deploy with an unboxed edge device that pulls config from the controller — the exam contrasts this with manual CLI staging.",
        "Security rides along: SD-WAN builds encrypted overlays (IPsec) across untrusted broadband, so the 'cheap link' gets enterprise-grade confidentiality."
    ],
    "example": {
        "code": "Branch policy:\n  voice (dscp ef): prefer MPLS; failover to broadband if loss <1% & jitter <30ms; LLQ priority 2 Mbps\n  video (dscp af41): prefer broadband; MPLS backup\n  bulk replication: broadband only, deprioritized, capped 50 Mbps\n  guest wifi: broadband, rate-limited, direct internet breakout",
        "walkthrough": "Each application's sensitivity maps to a path and a queue: voice gets the stable path plus priority queuing because jitter kills calls; bulk gets the fat pipe but capped so it can't crowd out interactive traffic; guest traffic never touches the expensive MPLS. The controller enforces this continuously, not just at config time."
    },
    "pitfalls": [
        "Marking traffic but never trusting/enforcing markings end-to-end — an EF mark the WAN ignores is decoration.",
        "Giving voice priority without a policer — a voice flood (or misclassification) can starve all other traffic.",
        "Treating SD-WAN as 'just VPN' — the differentiator is centralized policy plus dynamic, measured path selection."
    ],
    "try_it": "Classify your home traffic into 4 classes (real-time, interactive, bulk, background). Write the marking and queuing policy you'd apply at your router."
}
]
}
}
