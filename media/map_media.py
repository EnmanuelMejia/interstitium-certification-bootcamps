# -*- coding: utf-8 -*-
"""Worker 2 mapper: picks a fitting, technically-accurate diagram per lesson and
writes content/<slug>/assets/diagrams/*.svg + content/<slug>/fragments/media.json.

Never edits content/<slug>.json. All diagram content is original; labels use
well-established technical facts (ports, protocols, layer orders, real commands).
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'media'))
import gen_diagrams as G  # noqa: E402


def safe(name):
    return re.sub(r'[^a-z0-9]+', '-', str(name).lower()).strip('-')


def short_title(title):
    t = re.sub(r'\s+[—–-]\s+Core concepts\s*$', '', str(title or ''))
    return t.strip() or 'Overview'


def headline(concept):
    """Split a lesson concept into a (head, detail) pair for card diagrams."""
    parts = re.split(r'\s+[—–-]\s+|:\s+|;\s+', str(concept).strip(), maxsplit=1)
    h = parts[0].strip()
    d = parts[1].strip() if len(parts) > 1 else ''
    if len(h) > 92:
        h = h[:89].rstrip() + '…'
    if len(d) > 150:
        d = d[:147].rstrip() + '…'
    if not d and len(str(concept)) > 92:
        d = str(concept)[len(h):].strip()[:150]
    return h, d


KB = {}


def K(slug, did, kind, title, caption='', **kw):
    """Register an exact curated diagram for (slug, domain_id)."""
    KB[(slug, did)] = (kind, dict(title=title, caption=caption, **kw))


# ---------------------------------------------------------------------------
# Shared, vendor-neutral technical-fact blocks (accuracy self-reviewed)
# ---------------------------------------------------------------------------
OSI_LAYERS = [
    ('7 · Application', 'HTTP, DNS, SMTP — user-facing services'),
    ('6 · Presentation', 'TLS, JPEG, ASCII — data format & encryption'),
    ('5 · Session', 'NetBIOS, RPC — dialogs and sessions'),
    ('4 · Transport', 'TCP / UDP — ports, segments, reliability'),
    ('3 · Network', 'IP, ICMP — addressing, routing, packets'),
    ('2 · Data Link', 'Ethernet, MAC — frames, switching'),
    ('1 · Physical', 'Cables, hubs, NICs — bits on the wire'),
]
TCPIP_LAYERS = [
    ('Application', 'HTTP, DNS, SSH, FTP — application protocols'),
    ('Transport', 'TCP / UDP — ports and delivery guarantees'),
    ('Internet', 'IP, ICMP — addressing and routing'),
    ('Network Access', 'Ethernet, Wi-Fi — frames on the medium'),
]
PORT_ROWS = [
    ['SSH', '22 / TCP', 'Encrypted remote administration'],
    ['DNS', '53 / TCP+UDP', 'Name resolution'],
    ['HTTP', '80 / TCP', 'Unencrypted web traffic'],
    ['HTTPS', '443 / TCP', 'TLS-protected web traffic'],
    ['RDP', '3389 / TCP', 'Windows Remote Desktop'],
    ['SMB', '445 / TCP', 'Windows file sharing'],
    ['MySQL', '3306 / TCP', 'MySQL / MariaDB database'],
    ['PostgreSQL', '5432 / TCP', 'PostgreSQL database'],
]
TCP_UDP = dict(headers=['Aspect', 'TCP', 'UDP'], rows=[
    ['Connection', 'Connection-oriented', 'Connectionless'],
    ['Reliability', 'Guaranteed, ordered', 'Best-effort, unordered'],
    ['Overhead', 'Higher (slower)', 'Lower (faster)'],
    ['Typical use', 'Web, email, file transfer', 'DNS, VoIP, gaming'],
])
IPV4_V6 = dict(headers=['Aspect', 'IPv4', 'IPv6'], rows=[
    ['Address size', '32-bit (~4.3B)', '128-bit (vast)'],
    ['Notation', 'Dotted decimal', 'Hexadecimal colons'],
    ['Loopback', '127.0.0.1', '::1'],
    ['NAT', 'Widely needed', 'Not needed (plenty)'],
])
SYM_ASYM = dict(headers=['Aspect', 'Symmetric', 'Asymmetric'], rows=[
    ['Keys', 'One shared secret', 'Public + private pair'],
    ['Examples', 'AES-256, ChaCha20', 'RSA-2048, ECC'],
    ['Speed', 'Fast', 'Slow'],
    ['Key exchange', 'Hard (shared secret)', 'Solved (public key)'],
    ['Main uses', 'Bulk data encryption', 'Key exchange, signatures'],
])
RAID = dict(headers=['Level', 'Layout', 'Fault tolerance'], rows=[
    ['RAID 0', 'Striping', 'None — any disk loss kills array'],
    ['RAID 1', 'Mirroring', 'Survives 1 disk failure'],
    ['RAID 5', 'Striping + parity', 'Survives 1 disk failure'],
    ['RAID 6', 'Striping + dual parity', 'Survives 2 disk failures'],
    ['RAID 10', 'Mirrored stripes', 'Survives 1+ per mirror'],
])
HTTP_STATUS = dict(headers=['Class', 'Meaning', 'Examples'], rows=[
    ['2xx', 'Success', '200 OK · 201 Created · 204 No Content'],
    ['3xx', 'Redirection', '301 Moved · 302 Found · 304 Not Modified'],
    ['4xx', 'Client error', '400 Bad Request · 401 · 403 · 404'],
    ['5xx', 'Server error', '500 Internal · 502 Bad Gateway · 503'],
])
REST_VERBS = dict(headers=['Verb', 'Purpose', 'Idempotent'], rows=[
    ['GET', 'Read a resource', 'Yes'],
    ['POST', 'Create a resource', 'No'],
    ['PUT', 'Replace a resource', 'Yes'],
    ['PATCH', 'Partial update', 'No'],
    ['DELETE', 'Remove a resource', 'Yes'],
])
KILL_CHAIN = [
    ('Reconnaissance', 'Gather intel on the target'),
    ('Weaponization', 'Craft the malicious payload'),
    ('Delivery', 'Deliver via email, web, USB'),
    ('Exploitation', 'Trigger the vulnerability'),
    ('Installation', 'Persist malware on host'),
    ('Command & Control', 'Beacon out to attacker'),
    ('Actions on Objectives', 'Exfiltrate / disrupt / ransom'),
]
IR_PHASES = [
    ('Preparation', 'Plans, tools, team, comms'),
    ('Detection & Analysis', 'Triage alerts, scope incident'),
    ('Containment', 'Isolate: short- then long-term'),
    ('Eradication', 'Remove root cause'),
    ('Recovery', 'Restore systems, monitor'),
    ('Post-Incident', 'Lessons learned, improve'),
]
CIA = [
    ('Confidentiality', 'Only authorized access — encryption, access control.'),
    ('Integrity', 'Data stays accurate — hashing, digital signatures.'),
    ('Availability', 'Systems stay reachable — redundancy, backups, DDoS defense.'),
]
AAA = [
    ('Authentication', 'Who are you? — passwords, MFA, certificates.'),
    ('Authorization', 'What may you do? — roles, permissions, policies.'),
    ('Accounting', 'What did you do? — logs, audits, billing.'),
]
DNS_FLOW = [
    ('Client query', 'App asks: what is the IP?'),
    ('Recursive resolver', 'ISP / 1.1.1.1 looks it up'),
    ('Root (.)', 'Points to the TLD servers'),
    ('TLD server', 'Points to authoritative NS'),
    ('Authoritative', 'Returns the A / AAAA record'),
]
DHCP_FLOW = [
    ('Discover', 'Client broadcasts for a server'),
    ('Offer', 'Server proposes an IP + lease'),
    ('Request', 'Client accepts the offer'),
    ('Acknowledge', 'Server confirms — lease active'),
]
TCP_HANDSHAKE = [
    ('SYN', 'Client → server, seq=x'),
    ('SYN-ACK', 'Server → client, seq=y, ack=x+1'),
    ('ACK', 'Client → server, ack=y+1'),
    ('Established', 'Reliable byte stream begins'),
]
TLS12_FLOW = [
    ('ClientHello', 'Cipher suites + random offered'),
    ('ServerHello + Certificate', 'Cipher chosen, X.509 cert sent'),
    ('Key exchange', 'Premaster secret encrypted to server'),
    ('Finished', 'Both switch to encrypted session'),
]
CIDR_T = dict(headers=['CIDR', 'Usable hosts', 'Typical use'], rows=[
    ['/32', '1', 'Single host route'],
    ['/24', '254', 'Small LAN / subnet'],
    ['/16', '65,534', 'Large network'],
    ['/8', '16,777,214', 'Very large network'],
])
PRIVATE_IP = dict(headers=['Range', 'CIDR', 'Addresses'], rows=[
    ['10.0.0.0 – 10.255.255.255', '/8', '~16.7 million'],
    ['172.16.0.0 – 172.31.255.255', '/12', '~1.0 million'],
    ['192.168.0.0 – 192.168.255.255', '/16', '65,536'],
])
JWT_CRYPTO = dict(left='Header + Payload', left_sub='JSON, base64url-encoded',
                  key_label='Secret / private key', key_sub='HMAC or RSA signature',
                  right='Signature', right_sub='Verifies integrity & origin')
OAUTH_FLOW = [
    ('User login', 'Authorize at the auth server'),
    ('Auth code', 'Code returned to the client'),
    ('Token exchange', 'Code + client secret → tokens'),
    ('API calls', 'Access token on resource server'),
]
IAM_EVAL = [
    ('Request arrives', 'Who, what action, which resource'),
    ('Explicit DENY?', 'Any deny wins — stop here'),
    ('Explicit ALLOW?', 'An allow grants access'),
    ('Default', 'Otherwise: implicit DENY'),
]
SHARED_RESP = dict(headers=['Area', 'AWS (of the cloud)', 'Customer (in the cloud)'], rows=[
    ['Physical / facilities', 'Yes', '—'],
    ['Network infrastructure', 'Yes', '—'],
    ['Guest OS patching', '—', 'Yes (on EC2)'],
    ['IAM users & policies', '—', 'Yes'],
    ['Data encryption', '—', 'Yes'],
    ['Firewall / SG rules', '—', 'Yes'],
])
SDLC = [
    ('Plan', 'Requirements, scope, estimates'),
    ('Design', 'Architecture, data models'),
    ('Build', 'Write and review code'),
    ('Test', 'Unit, integration, security'),
    ('Deploy', 'Release to production'),
    ('Maintain', 'Monitor, patch, improve'),
]
SCRUM = [
    ('Backlog', 'Prioritized work items'),
    ('Sprint planning', 'Commit to a sprint goal'),
    ('Daily standup', 'Sync: done, next, blockers'),
    ('Sprint review', 'Demo the increment'),
    ('Retrospective', 'Improve the process'),
]
STAR = [
    ('Situation', 'Set the context briefly'),
    ('Task', 'Your responsibility'),
    ('Action', 'What YOU did, specifically'),
    ('Result', 'Outcome + what you learned'),
]
SMART = [
    ('Specific', 'Exactly what will be achieved.'),
    ('Measurable', 'A metric proves it happened.'),
    ('Achievable', 'Realistic with available resources.'),
    ('Relevant', 'Aligned with the bigger goal.'),
    ('Time-bound', 'Has a clear deadline.'),
]
SWOT = [
    ('Strengths', ['Skills you own', 'Proven results']),
    ('Weaknesses', ['Gaps to close', 'Honest limits']),
    ('Opportunities', ['Market demand', 'New roles']),
    ('Threats', ['Competition', 'Skill decay']),
]
HERMETIC_7 = [
    ('I · Mentalism', 'All is mind — the universe is mental.'),
    ('II · Correspondence', 'As above, so below.'),
    ('III · Vibration', 'Nothing rests; everything moves.'),
    ('IV · Polarity', 'Opposites are degrees of one thing.'),
    ('V · Rhythm', 'Everything flows in and out.'),
    ('VI · Cause & Effect', 'Every cause has its effect.'),
    ('VII · Gender', 'Masculine and feminine principles.'),
]
FEEDBACK_LOOP = [
    ('Sense', 'Measure the output'),
    ('Compare', 'Against the goal'),
    ('Act', 'Correct the input'),
]
AGENT_LOOP = [
    ('Perceive', 'Read state + user goal'),
    ('Reason', 'LLM plans the next step'),
    ('Act', 'Call a tool / API'),
    ('Observe', 'Read the result'),
]
RAG_TIERS = [
    ('Ingest', ['Chunk documents', 'Create embeddings', 'Store in vector DB']),
    ('Retrieve', ['Embed the query', 'Top-k similarity search']),
    ('Generate', ['Prompt + retrieved context', 'LLM writes the answer']),
]
TRANSFORMER_FLOW = [
    ('Tokens', 'Text → token IDs'),
    ('Embeddings', '+ positional encoding'),
    ('Self-attention', 'Tokens attend to context'),
    ('Feed-forward', 'Per-position transform'),
    ('Output', 'Logits → next token'),
]
ML_LIFECYCLE = [
    ('Prepare', 'Collect, clean, split data'),
    ('Train', 'Fit model on training set'),
    ('Validate', 'Tune on validation set'),
    ('Test', 'Final score on held-out data'),
    ('Deploy', 'Serve behind an API'),
    ('Monitor', 'Drift, quality, retrain'),
]
FINETUNE_FLOW = [
    ('Base model', 'Pretrained foundation'),
    ('SFT', 'Supervised fine-tuning'),
    ('Preference', 'RLHF / DPO alignment'),
    ('Evaluate', 'Benchmarks + red team'),
    ('Deploy', 'Serve the adapter/model'),
]
EVAL_T = dict(headers=['Metric', 'What it measures'], rows=[
    ['Accuracy', 'Overall correct predictions'],
    ['Precision', 'True positives ÷ predicted positive'],
    ['Recall', 'True positives ÷ actual positive'],
    ['F1', 'Harmonic mean of precision/recall'],
    ['ROC-AUC', 'Ranking quality across thresholds'],
])
ETL_FLOW = [
    ('Extract', 'Pull from sources / APIs'),
    ('Transform', 'Clean, join, validate'),
    ('Load', 'Write to warehouse / lake'),
]
KAFKA_FLOW = [
    ('Producer', 'Publishes records'),
    ('Broker / Topic', 'Durable ordered log'),
    ('Consumer group', 'Parallel processing'),
    ('Sink', 'Warehouse / search / alerts'),
]
STAR_SCHEMA = [
    ('fact_sales', [('sale_id', 'PK'), ('date_id', 'FK'), ('product_id', 'FK'), ('amount', '')]),
    ('dim_date', [('date_id', 'PK'), ('day', ''), ('month', ''), ('year', '')]),
    ('dim_product', [('product_id', 'PK'), ('name', ''), ('category', '')]),
]
JOINS_T = dict(headers=['Join', 'Keeps'], rows=[
    ['INNER', 'Only matching rows'],
    ['LEFT', 'All left rows + matches'],
    ['RIGHT', 'All right rows + matches'],
    ['FULL OUTER', 'All rows, both sides'],
    ['CROSS', 'Cartesian product'],
])
SQL_ORDER = [
    ('FROM', 'Tables first'),
    ('WHERE', 'Filter rows'),
    ('GROUP BY', 'Form groups'),
    ('HAVING', 'Filter groups'),
    ('SELECT', 'Choose columns'),
    ('ORDER BY', 'Sort output'),
]
ACID = [
    ('Atomicity', 'All-or-nothing: a transaction fully commits or fully rolls back.'),
    ('Consistency', 'Only valid state transitions — constraints always hold.'),
    ('Isolation', 'Concurrent transactions do not see each other mid-flight.'),
    ('Durability', 'Committed data survives crashes — written to durable storage.'),
]
ISOLATION_T = dict(headers=['Level', 'Read guarantees'], rows=[
    ['Read Uncommitted', 'Dirty reads possible'],
    ['Read Committed', 'Only committed data'],
    ['Repeatable Read', 'Stable reads in transaction'],
    ['Serializable', 'Full isolation, strictest'],
])
MONGO_AGG = [
    ('$match', 'Filter documents'),
    ('$group', 'Aggregate by key'),
    ('$sort', 'Order results'),
    ('$project', 'Shape output fields'),
    ('$limit', 'Cap result count'),
]
VOLATILITY = [
    ('Registers / cache', 'Most volatile — gone instantly'),
    ('RAM', 'Capture before power-off'),
    ('Network state', 'Connections, ARP tables'),
    ('Running processes', 'Process list, handles'),
    ('Disk', 'Image with write blocker'),
    ('Logs', 'System + app logs'),
    ('Backups', 'Least volatile'),
]
VULN_MGMT = [
    ('Identify', 'Scan assets for vulns'),
    ('Assess', 'Score with CVSS, context'),
    ('Prioritize', 'Risk-rank the findings'),
    ('Remediate', 'Patch / mitigate / accept'),
    ('Verify', 'Rescan to confirm closure'),
]
CVSS_BANDS = [
    ('None 0.0', 'No impact scored.'),
    ('Low 0.1–3.9', 'Minor impact, hard to exploit.'),
    ('Medium 4.0–6.9', 'Realistic exploit path.'),
    ('High 7.0–8.9', 'Easy exploit, serious impact.'),
    ('Critical 9.0–10.0', 'Trivial exploit, total compromise.'),
]
PTES = [
    ('Pre-engagement', 'Scope, rules of engagement'),
    ('Intel gathering', 'OSINT on the target'),
    ('Threat modeling', 'Attack paths, assets'),
    ('Vuln analysis', 'Scan + manual validation'),
    ('Exploitation', 'Prove impact safely'),
    ('Post-exploitation', 'Pivot, persistence, loot'),
    ('Reporting', 'Findings + remediation'),
]
OWASP21 = [
    ('A01 Broken Access Control', 'Missing authorization checks — #1 risk.'),
    ('A02 Cryptographic Failures', 'Weak hashing, plaintext secrets.'),
    ('A03 Injection', 'SQLi, command, LDAP injection.'),
    ('A05 Security Misconfiguration', 'Defaults, verbose errors, open S3.'),
    ('A07 Auth Failures', 'Credential stuffing, weak MFA.'),
    ('A10 SSRF', 'Server tricked into internal requests.'),
]
XSS_TYPES = [
    ('Stored', 'Payload persisted — hits every viewer.'),
    ('Reflected', 'Payload bounced off a URL parameter.'),
    ('DOM-based', 'Payload executes purely client-side.'),
]
SQLI_TYPES = [
    ('In-band', 'UNION / error-based — data in response.'),
    ('Blind boolean', 'True/false inferred from behavior.'),
    ('Blind time-based', 'SLEEP() delays reveal data.'),
    ('Out-of-band', 'DNS/HTTP exfiltration channel.'),
]
MITRE_T = [
    ('Initial Access', 'Phishing, exploit, valid accounts.'),
    ('Execution', 'Run attacker code on host.'),
    ('Persistence', 'Survive reboots — services, tasks.'),
    ('Privilege Escalation', 'Get SYSTEM / root.'),
    ('Lateral Movement', 'Spread to other hosts.'),
    ('Exfiltration', 'Stage and steal data out.'),
]
THREAT_INTEL = [
    ('Tactical', 'IOCs: hashes, IPs, domains.'),
    ('Operational', 'Campaigns and TTPs.'),
    ('Strategic', 'Trends for leadership.'),
    ('IOCs vs TTPs', 'Indicators expire; behaviors persist.'),
]
SIEM_FLOW = [
    ('Collect', 'Agents forward logs'),
    ('Normalize', 'Parse to common schema'),
    ('Correlate', 'Rules link related events'),
    ('Alert', 'Create a case / ticket'),
    ('Investigate', 'Analyst hunts in timeline'),
]
SOC_TIERS = [
    ('Tier 1 — Triage', 'Monitor queues, classify, escalate.'),
    ('Tier 2 — Investigation', 'Deep-dive, contain, coordinate.'),
    ('Tier 3 — Hunting & IR', 'Proactive hunts, forensics, malware.'),
]
NICE_CATS = [
    ('SP · Securely Provision', 'Design and build secure systems.'),
    ('OM · Operate & Maintain', 'Keep systems running and patched.'),
    ('OV · Oversee & Govern', 'Policy, risk, and leadership.'),
    ('PR · Protect & Defend', 'Defend networks and data.'),
    ('AN · Analyze', 'Analyze threats and intel.'),
    ('CO · Collect & Operate', 'Collect and operate capabilities.'),
]
DOD_BASELINE = dict(headers=['Level', 'Example baseline certs'], rows=[
    ['IAT I', 'A+ CE'],
    ['IAT II', 'Security+ CE'],
    ['IAT III', 'CASP+ CE · CISSP'],
    ['IAM II / III', 'CISSP · CISM'],
])
CONSENSUS_T = dict(headers=['Mechanism', 'How it agrees', 'Example'], rows=[
    ['Proof of Work', 'Miners solve hash puzzles', 'Bitcoin'],
    ['Proof of Stake', 'Validators stake coins', 'Ethereum'],
    ['BFT voting', '2/3+ validator votes', 'Tendermint / Fabric'],
    ['UNL consensus', 'Trusted validator lists', 'XRP Ledger'],
])
BLOCK_FLOW = [
    ('Transactions', 'Users broadcast transfers'),
    ('Merkle root', 'Txs hashed into one root'),
    ('Block header', 'Prev hash + nonce + root'),
    ('Hash puzzle', 'Find hash below target'),
    ('Chain link', 'Block appended immutably'),
]
EVM_FLOW = [
    ('Solidity', 'Write the contract'),
    ('Compile', 'solc → EVM bytecode'),
    ('Deploy', 'Transaction creates address'),
    ('Call', 'Transactions execute code'),
    ('State', 'Storage updated on-chain'),
]
PLAYBOOK_FLOW = [
    ('Inventory', 'Hosts and groups listed'),
    ('Play', 'Targets + variables set'),
    ('Tasks', 'Ordered steps run'),
    ('Modules', 'yum, copy, service do work'),
    ('Handlers', 'Restart on change only'),
]
TERRAFORM_FLOW = [
    ('init', 'Download providers, setup backend'),
    ('validate', 'Check HCL syntax'),
    ('plan', 'Preview the changes'),
    ('apply', 'Provision real infrastructure'),
    ('destroy', 'Tear it all down'),
]
LVM_FLOW = [
    ('Disk / partition', 'Raw block device'),
    ('Physical Volume', 'pvcreate initializes it'),
    ('Volume Group', 'vgcreate pools PVs'),
    ('Logical Volume', 'lvcreate carves space'),
    ('Filesystem', 'mkfs, then mount'),
]
BOOT_FLOW = [
    ('Firmware', 'UEFI / BIOS POST'),
    ('Bootloader', 'GRUB2 loads kernel'),
    ('Kernel', 'Initializes hardware'),
    ('systemd', 'PID 1 starts services'),
    ('Target', 'multi-user / graphical login'),
]
PERMS = [
    ('rwx = 4, 2, 1', 'Read=4, write=2, execute=1 per class.'),
    ('Owner / group / other', 'Three classes, three digit slots.'),
    ('chmod 755', 'rwxr-xr-x — standard for dirs.'),
    ('chmod 644', 'rw-r--r-- — standard for files.'),
    ('umask 022', 'Default mask: strips write for group/other.'),
]
FHS = [
    ('/bin · /sbin', 'Essential user & system binaries'),
    ('/etc', 'Host-specific configuration'),
    ('/home', 'User home directories'),
    ('/var', 'Variable data: logs, spool, mail'),
    ('/tmp', 'Temporary files (cleared on boot)'),
    ('/usr', 'Read-only user programs & libs'),
    ('/opt', 'Optional add-on software'),
    ('/boot', 'Kernel & bootloader files'),
]
DOCKERFILE_FLOW = [
    ('FROM', 'Start from a base image'),
    ('RUN', 'Install packages at build'),
    ('COPY', 'Add your code in'),
    ('EXPOSE', 'Document the port'),
    ('CMD', 'Default run command'),
]
CI_FLOW = [
    ('Commit', 'Push to the repo'),
    ('Build', 'Compile / package'),
    ('Test', 'Unit + integration suites'),
    ('Artifact', 'Immutable build stored'),
    ('Stage', 'Deploy to staging'),
    ('Prod', 'Promote to production'),
]
JENKINS_FLOW = [
    ('Checkout', 'Pull the Jenkinsfile + code'),
    ('Build', 'Compile the project'),
    ('Test', 'Run automated suites'),
    ('Package', 'Create the artifact'),
    ('Deploy', 'Push to environments'),
]
MIDDLEWARE_FLOW = [
    ('Request in', 'HTTP arrives at the server'),
    ('Exception handler', 'Catch-all safety net'),
    ('Routing', 'Match URL to endpoint'),
    ('Auth', 'Identity + authorization'),
    ('Endpoint', 'Controller runs, response out'),
]
REST_LIFECYCLE = [
    ('Client request', 'GET /api/orders/42'),
    ('Route match', 'Framework maps URL'),
    ('Controller', 'Handler logic runs'),
    ('Service + DB', 'Business logic, queries'),
    ('Response', 'JSON + status code back'),
]
AUTH_JWT = [
    ('Login', 'User submits credentials'),
    ('Verify', 'Server checks password hash'),
    ('Sign JWT', 'header.payload.signature issued'),
    ('Store', 'Client keeps the token'),
    ('Authorize', 'Bearer token on each request'),
]
COND_ACCESS = [
    ('Signals', 'User, device, location, risk'),
    ('Policy match', 'Which CA policies apply?'),
    ('Grant controls', 'Require MFA / compliant device'),
    ('Decision', 'Allow, or block access'),
]
MFA_FLOW = [
    ('Factor 1', 'Password submitted'),
    ('Challenge', 'TOTP / push / SMS sent'),
    ('Verify', 'Code checked server-side'),
    ('Session', 'Token issued, device remembered'),
]
RBAC = [
    ('Assignment = principal + role + scope', 'The three parts of every grant.'),
    ('Built-in roles', 'Owner, Contributor, Reader — prefer least.'),
    ('Least privilege', 'Grant the minimum that works.'),
    ('Deny assignments', 'Explicit blocks override allows.'),
]
PIM = [
    ('Eligible vs Active', 'Eligible = can activate; active = now.'),
    ('Just-in-time', 'Elevate only when needed.'),
    ('Approval', 'Manager / owner approves request.'),
    ('Access reviews', 'Recertify access on schedule.'),
]
SENTINEL_FLOW = [
    ('Connect', 'Data connectors onboard logs'),
    ('Collect', 'Tables fill in the workspace'),
    ('Detect', 'Analytics rules fire incidents'),
    ('Investigate', 'Entity graph + timeline'),
    ('Respond', 'Playbooks automate response'),
]
NIST_CSF = [
    ('Govern', 'Strategy, policy, oversight.'),
    ('Identify', 'Know assets and risks.'),
    ('Protect', 'Safeguards and controls.'),
    ('Detect', 'Find events quickly.'),
    ('Respond', 'Contain and eradicate.'),
    ('Recover', 'Restore and learn.'),
]
DEFENSE_DEPTH = [
    ('Physical', 'Badges, locks, cameras'),
    ('Network', 'Firewalls, segmentation, IDS'),
    ('Host', 'EDR, patching, hardening'),
    ('Application', 'WAF, secure code, auth'),
    ('Data', 'Encryption, DLP, backups'),
]
ZERO_TRUST = [
    ('Verify explicitly', 'Authenticate every request.'),
    ('Least privilege', 'Minimum access, just in time.'),
    ('Assume breach', 'Design as if already compromised.'),
]
BLA = [
    ('Bell-LaPadula', 'No read up, no write down — confidentiality.'),
    ('Biba', 'No read down, no write up — integrity.'),
    ('Clark-Wilson', 'Well-formed transactions, separation of duties.'),
]
SLI_SLO = [
    ('SLI', 'The measurement — e.g. 99.9% success.'),
    ('SLO', 'The target you promise.'),
    ('Error budget', 'Allowed failures = 1 − SLO.'),
    ('SLA', 'Contract with consequences.'),
]
RED_USE = [
    ('RED: Rate / Errors / Duration', 'Request-scoped service health.'),
    ('USE: Utilization / Saturation / Errors', 'Resource-scoped host health.'),
    ('MELT: Metrics, Events, Logs, Traces', 'The four observability pillars.'),
]
INCIDENT_FLOW = [
    ('Detect', 'Alert fires / report arrives'),
    ('Triage', 'Severity, scope, owner'),
    ('Mitigate', 'Stop the bleeding'),
    ('Resolve', 'Fix root cause, verify'),
    ('Postmortem', 'Blameless review, actions'),
]
BACKUP_321 = [
    ('3 copies', 'Original + two backups.'),
    ('2 media types', 'Disk + tape / cloud.'),
    ('1 offsite', 'Survives site loss.'),
    ('Test restores', 'A backup you never tested is hope.'),
]
RTO_RPO = [
    ('RTO', 'Max time to restore service.'),
    ('RPO', 'Max data loss tolerated.'),
    ('MTTR', 'Mean time to repair.'),
    ('MTBF', 'Mean time between failures.'),
]
DR_T = dict(headers=['Strategy', 'Recovery speed', 'Cost'], rows=[
    ['Backup & restore', 'Hours', '$'],
    ['Pilot light', 'Tens of minutes', '$$'],
    ['Warm standby', 'Minutes', '$$$'],
    ['Active / active', 'Near-zero', '$$$$'],
])
K8S_ARCH = [
    ('Control plane', ['kube-apiserver', 'etcd', 'kube-scheduler', 'kube-controller-manager']),
    ('Worker node', ['kubelet', 'kube-proxy', 'container runtime']),
    ('Workloads', ['Pod', 'Deployment', 'Service']),
]
K8S_SVC_T = dict(headers=['Service type', 'Scope'], rows=[
    ['ClusterIP', 'In-cluster only (default)'],
    ['NodePort', 'Exposed on each node port'],
    ['LoadBalancer', 'Cloud load balancer IP'],
    ['ExternalName', 'DNS alias to external name'],
])
K8S_SEC = [
    ('RBAC', 'Least-privilege roles & bindings.'),
    ('NetworkPolicies', 'Default-deny pod traffic.'),
    ('Pod Security', 'Enforce baseline/restricted standards.'),
    ('Secrets', 'Base64 is not encryption — use external KMS.'),
    ('Image scanning', 'Scan for CVEs before deploy.'),
]
K8S_SCHED = [
    ('kube-scheduler', 'Assigns pods to nodes.'),
    ('Requests / limits', 'Guarantee vs cap resources.'),
    ('Taints / tolerations', 'Repel pods from nodes.'),
    ('Affinity', 'Attract pods to nodes/zones.'),
]
PROBES = [
    ('livenessProbe', 'Unhealthy → container restarted.'),
    ('readinessProbe', 'Unready → removed from service.'),
    ('startupProbe', 'For slow-starting containers.'),
]
ROLLING_FLOW = [
    ('v1 running', 'Stable replicas serve traffic'),
    ('v2 rollout', 'New pods surge within limits'),
    ('Health checks', 'Probes gate each batch'),
    ('v1 scaled down', 'Old pods drain away'),
]
GITOPS_FLOW = [
    ('Git', 'Desired state committed'),
    ('Sync', 'ArgoCD / Flux pulls state'),
    ('Apply', 'Cluster converges to git'),
    ('Drift detect', 'Diffs flagged automatically'),
]
ROUTE_FLOW = [
    ('External', 'Client hits the route hostname'),
    ('Route', 'OpenShift edge termination'),
    ('Service', 'Stable virtual IP'),
    ('Pod', 'Application container'),
]
VAULT_AUTH = [
    ('Client', 'App or user requests access'),
    ('Auth method', 'Token / LDAP / Kubernetes'),
    ('Policy check', 'HCL policy allows path?'),
    ('Token + lease', 'Short-lived token issued'),
    ('Secrets engine', 'Read kv / dynamic creds'),
]
VAULT_ENGINES = [
    ('kv', 'Static secrets, versioned.'),
    ('database', 'Dynamic creds with TTL.'),
    ('pki', 'Certificates as a service.'),
    ('transit', 'Encryption without storing data.'),
]
EXCEPT_FLOW = [
    ('try', 'Run the risky code'),
    ('except', 'Handle the failure path'),
    ('else', 'Runs only if no error'),
    ('finally', 'Always runs — cleanup'),
]
C_BUILD = [
    ('Preprocess', 'gcc -E: macros expanded'),
    ('Compile', 'gcc -S: C → assembly'),
    ('Assemble', 'as: assembly → object'),
    ('Link', 'ld: objects → binary'),
]
POINTERS = [
    ('& address-of', 'Gives the memory address of a variable.'),
    ('* dereference', 'Reads/writes through a pointer.'),
    ('malloc / free', 'Heap allocation must be freed.'),
    ('Pointer arithmetic', 'p+1 steps by element size.'),
    ('NULL checks', 'Never dereference blindly.'),
]
SMART_PTRS = [
    ('unique_ptr', 'Exclusive ownership, zero overhead.'),
    ('shared_ptr', 'Reference-counted sharing.'),
    ('weak_ptr', 'Non-owning observer, breaks cycles.'),
    ('RAII', 'Resources tied to object lifetime.'),
]
STL_T = dict(headers=['Container', 'Access', 'Insert'], rows=[
    ['vector', 'O(1) indexed', 'O(1) amortized back'],
    ['list', 'O(n) walk', 'O(1) anywhere'],
    ['map', 'O(log n) keyed', 'O(log n)'],
    ['unordered_map', 'O(1) avg keyed', 'O(1) avg'],
])
COLLECTIONS_T = dict(headers=['Interface', 'Implementations'], rows=[
    ['List', 'ArrayList · LinkedList'],
    ['Set', 'HashSet · TreeSet'],
    ['Map', 'HashMap · TreeMap'],
    ['Queue', 'ArrayDeque · PriorityQueue'],
])
STREAM_FLOW = [
    ('Source', 'Collection / generator'),
    ('Intermediate', 'filter · map · sorted'),
    ('Terminal', 'collect · forEach · reduce'),
]
OOP_PILLARS = [
    ('Abstraction', 'Expose what, hide how'),
    ('Encapsulation', 'Bundle data + methods, guard state'),
    ('Inheritance', 'Reuse behavior via base classes'),
    ('Polymorphism', 'One interface, many implementations'),
]
PY_TYPES_T = dict(headers=['Type', 'Mutable', 'Use'], rows=[
    ['list', 'Yes', 'Ordered sequence'],
    ['tuple', 'No', 'Fixed records'],
    ['dict', 'Yes', 'Key → value mapping'],
    ['set', 'Yes', 'Unique members'],
])
PY_DEBUG_FLOW = [
    ('Reproduce', 'Trigger it reliably'),
    ('Traceback', 'Read bottom-up: last call first'),
    ('Isolate', 'breakpoint() / pdb, bisect input'),
    ('Fix', 'Change one thing at a time'),
    ('Regression test', 'Prove it stays fixed'),
]
GIT_CMDS = [
    ('git init', 'Create a new repository'),
    ('git clone <url>', 'Copy a remote repo locally'),
    ('git status', 'Show working-tree state'),
    ('git add .', 'Stage changes'),
    ('git commit -m "msg"', 'Snapshot staged changes'),
    ('git branch', 'List / create branches'),
    ('git checkout -b <name>', 'Create + switch branch'),
    ('git merge <branch>', 'Join branch into current'),
    ('git push', 'Upload commits to remote'),
    ('git pull', 'Fetch + merge from remote'),
]
KUBECTL_CMDS = [
    ('kubectl get pods', 'List pods in namespace'),
    ('kubectl describe pod <n>', 'Full pod details + events'),
    ('kubectl apply -f app.yaml', 'Declare desired state'),
    ('kubectl delete -f app.yaml', 'Remove declared resources'),
    ('kubectl logs <pod>', 'Read container logs'),
    ('kubectl exec -it <p> -- sh', 'Shell inside a container'),
    ('kubectl rollout status', 'Watch a deployment rollout'),
    ('kubectl port-forward', 'Tunnel a port locally'),
    ('kubectl scale --replicas=3', 'Change replica count'),
    ('kubectl top pods', 'Live resource usage'),
]
DOCKER_CMDS = [
    ('docker build -t app .', 'Build image from Dockerfile'),
    ('docker run -d -p 80:80 app', 'Start detached container'),
    ('docker ps', 'List running containers'),
    ('docker images', 'List local images'),
    ('docker exec -it <c> sh', 'Shell in running container'),
    ('docker logs <c>', 'Read container output'),
    ('docker stop <c> / rm', 'Stop / remove container'),
    ('docker pull / push', 'Registry download / upload'),
    ('docker volume ls', 'Manage named volumes'),
    ('docker network ls', 'List networks'),
]
TERRAFORM_CMDS = [
    ('terraform init', 'Install providers, init backend'),
    ('terraform validate', 'Check configuration syntax'),
    ('terraform plan', 'Preview infrastructure changes'),
    ('terraform apply', 'Provision real resources'),
    ('terraform destroy', 'Tear down managed infra'),
    ('terraform fmt', 'Canonical HCL formatting'),
    ('terraform state list', 'Inspect tracked resources'),
    ('terraform output', 'Show output values'),
]
AWSCLI_CMDS = [
    ('aws ec2 describe-instances', 'List EC2 instances'),
    ('aws s3 ls / cp / sync', 'List, copy, sync objects'),
    ('aws iam list-users', 'List IAM users'),
    ('aws cloudformation deploy', 'Deploy a stack'),
    ('aws logs tail /aws/lambda/f', 'Stream CloudWatch logs'),
]
AZCLI_CMDS = [
    ('az login', 'Authenticate to Azure'),
    ('az group create -n rg', 'Create a resource group'),
    ('az vm list -o table', 'List virtual machines'),
    ('az storage account create', 'Create a storage account'),
    ('az aks create', 'Create a managed K8s cluster'),
    ('az monitor metrics list', 'Query platform metrics'),
]
LINUX_CMDS = [
    ('ls -la', 'List files incl. hidden'),
    ('cp / mv / rm', 'Copy, move, remove'),
    ('mkdir -p / touch', 'Create dirs / files'),
    ('chmod 755 / chown u:g', 'Permissions / ownership'),
    ('ps aux / top', 'Process listing / live view'),
    ('systemctl status sshd', 'Service state'),
    ('ip addr / ss -tulpn', 'Addresses / listening ports'),
    ('grep -R / sed / awk', 'Search / edit streams'),
    ('tar czf / rsync -a', 'Archive / sync trees'),
    ('find / -name "*.log"', 'Locate files by name'),
]
BASH_CMDS = [
    ('#!/bin/bash', 'Shebang: run with bash'),
    ('name="val"', 'Variable assignment (no spaces)'),
    ('$? / $# / $@', 'Exit code / argc / argv'),
    ('if [ -f f ]; then … fi', 'File-exists conditional'),
    ('for f in *.log; do … done', 'Loop over matches'),
    ('cmd1 | cmd2', 'Pipe stdout to stdin'),
    ('> out 2>&1 / >>', 'Redirect / append output'),
]
GDB_CMDS = [
    ('gdb ./a.out', 'Start debugging the binary'),
    ('break main', 'Breakpoint at main()'),
    ('run [args]', 'Start the program'),
    ('next / step', 'Step over / into'),
    ('print var', 'Inspect a variable'),
    ('backtrace', 'Show the call stack'),
    ('continue / quit', 'Resume / exit gdb'),
]
SQL_CMDS = [
    ('SELECT a, b FROM t WHERE x > 5', 'Filter rows, pick columns'),
    ('GROUP BY d HAVING COUNT(*) > 1', 'Aggregate + filter groups'),
    ('t1 JOIN t2 ON t1.id = t2.id', 'Combine related rows'),
    ('INSERT / UPDATE / DELETE', 'Write, change, remove rows'),
    ('CREATE TABLE t (…)', 'Define schema'),
    ('ROW_NUMBER() OVER (PARTITION BY d ORDER BY t)', 'Window ranking'),
]
MONGOSH_CMDS = [
    ('show dbs / use shop', 'List / switch databases'),
    ('db.orders.find({status:"A"})', 'Query documents'),
    ('db.orders.insertOne({...})', 'Insert a document'),
    ('db.orders.updateOne({_id:1}, {$set:{s:"B"}})', 'Update fields'),
    ('db.orders.aggregate([{$match:{}}, {$group:{}}])', 'Pipeline aggregation'),
    ('db.orders.createIndex({email:1})', 'Speed up queries'),
]
KQL_CMDS = [
    ('SigninLogs | take 10', 'Sample the table'),
    ('| where ResultType != 0', 'Filter failures'),
    ('| summarize count() by UserPrincipalName', 'Group + count'),
    ('| project TimeGenerated, User', 'Pick columns'),
    ('| sort by TimeGenerated desc', 'Newest first'),
    ('| join kind=inner (… ) on $left.Id == $right.Id', 'Correlate tables'),
    ('| render timechart', 'Visualize results'),
]
SYSTEMD_CMDS = [
    ('systemctl start nginx', 'Start a service now'),
    ('systemctl enable nginx', 'Start at boot'),
    ('systemctl status nginx', 'State + recent logs'),
    ('systemctl restart sshd', 'Restart a service'),
    ('journalctl -u nginx -f', 'Follow service logs'),
    ('systemctl daemon-reload', 'Reload unit files'),
]
IP_CMDS = [
    ('ip addr show', 'Interfaces + addresses'),
    ('ip route show', 'Routing table'),
    ('ss -tulpn', 'Listening sockets + PIDs'),
    ('ping -c 4 8.8.8.8', 'L3 reachability test'),
    ('traceroute example.com', 'Path to destination'),
    ('dig +short example.com', 'DNS lookup'),
    ('curl -I https://x', 'HTTP headers only'),
]
USER_CMDS = [
    ('useradd -m jdoe', 'Create user + home dir'),
    ('passwd jdoe', 'Set the password'),
    ('usermod -aG wheel jdoe', 'Append to a group'),
    ('chmod 755 /home/jdoe', 'Directory permissions'),
    ('chown jdoe:jdoe file', 'Change ownership'),
    ('id jdoe', 'Show uid, gid, groups'),
]
PODMAN_CMDS = [
    ('podman run -d nginx', 'Daemonless container run'),
    ('podman ps', 'Running containers'),
    ('podman images', 'Local images'),
    ('podman build -t app .', 'Build from Containerfile'),
    ('podman exec -it <c> sh', 'Shell in container'),
    ('podman pod create', 'Group containers in a pod'),
]
ADF_FLOW = [
    ('Linked service', 'Connection to the source'),
    ('Dataset', 'Pointer to the data'),
    ('Pipeline', 'The workflow container'),
    ('Activity', 'Copy / transform task'),
    ('Trigger', 'Schedule or event start'),
]
DP203_T = dict(headers=['Service', 'Use'], rows=[
    ['Data Factory', 'Orchestrate pipelines'],
    ['Synapse Analytics', 'Warehouse + big data'],
    ['Databricks', 'Spark notebooks at scale'],
    ['Event Hubs', 'Streaming ingestion'],
    ['ADLS Gen2', 'Data lake storage'],
    ['Cosmos DB', 'Global NoSQL'],
])
PLSQL_FLOW = [
    ('DECLARE', 'Variables, cursors, types'),
    ('BEGIN', 'Executable statements'),
    ('EXCEPTION', 'Error handlers'),
    ('END;', 'Block terminator'),
]
TRIGGERS = [
    ('BEFORE / AFTER', 'Fire before or after the DML.'),
    ('Row vs statement', 'FOR EACH ROW or once per statement.'),
    ('INSERT / UPDATE / DELETE', 'The triggering event.'),
    ('INSTEAD OF', 'On views — custom logic.'),
]
ORACLE_ARCH = [
    ('Instance (memory)', ['SGA — shared memory', 'PGA — per-process', 'Background processes']),
    ('Database (storage)', ['Datafiles', 'Control files', 'Redo log files']),
]
RMAN_FLOW = [
    ('Configure', 'Retention + backup destination'),
    ('BACKUP DATABASE', 'Full / incremental backup'),
    ('Validate', 'RESTORE … VALIDATE checks'),
    ('Recover', 'Restore + apply redo'),
    ('Test', 'Trial recovery on standby'),
]
CONSUL_TOPO_SPOKE = ['Service discovery', 'Health checks', 'KV store', 'Connect mesh (mTLS)', 'DNS interface']
AWS_CORE_SPOKE = ['EC2 · compute', 'S3 · object storage', 'RDS · databases', 'Lambda · serverless',
                  'VPC · networking', 'IAM · identity', 'CloudWatch · monitoring', 'Route 53 · DNS']
VPC_SPOKE = ['Public subnet + IGW', 'Private subnet + NAT GW', 'Route tables', 'Security groups',
             'NACLs (stateless)', 'VPC endpoints']
VNET_SPOKE = ['Subnets + NSGs', 'VNet peering', 'VPN Gateway', 'ExpressRoute', 'Private Endpoint', 'Azure Firewall']
OCI_VCN_SPOKE = ['Public subnet + IGW', 'Private subnet + NAT GW', 'Service gateway', 'DRG (on-prem link)',
                 'Security lists', 'Route tables']
S3_CLASSES_T = dict(headers=['Storage class', 'Use case'], rows=[
    ['Standard', 'Frequent access'],
    ['Intelligent-Tiering', 'Unknown / changing patterns'],
    ['Standard-IA', 'Infrequent, fast when needed'],
    ['Glacier Flexible', 'Archive, minutes–hours'],
    ['Glacier Deep Archive', 'Long-term, lowest cost'],
])
EC2_BUY_T = dict(headers=['Option', 'Commitment', 'Saving'], rows=[
    ['On-Demand', 'None', 'Baseline price'],
    ['Reserved (1/3 yr)', 'Capacity + term', 'Up to ~72%'],
    ['Spot', 'None — interruptible', 'Up to ~90%'],
    ['Savings Plans', 'Spend / hr, 1/3 yr', 'Flexible discount'],
])
COMPUTE_T = dict(headers=['Service', 'Model', 'Best for'], rows=[
    ['EC2', 'Virtual machines', 'Full OS control'],
    ['Lambda', 'Functions', 'Event-driven, no servers'],
    ['ECS', 'Containers', 'Docker at scale'],
    ['Fargate', 'Serverless containers', 'No EC2 to manage'],
])
STORAGE_T = dict(headers=['Service', 'Type', 'Use'], rows=[
    ['S3', 'Object', 'Unlimited flat storage'],
    ['EBS', 'Block', 'EC2 volumes'],
    ['EFS', 'File (NFS)', 'Shared Linux filesystem'],
    ['RDS', 'Relational', 'Managed SQL databases'],
    ['DynamoDB', 'NoSQL key-value', 'Millisecond scale'],
])
AZURE_COMPUTE_T = dict(headers=['Service', 'Model'], rows=[
    ['Virtual Machines', 'IaaS — full control'],
    ['App Service', 'PaaS web hosting'],
    ['Functions', 'Serverless events'],
    ['Container Instances', 'Fast single containers'],
    ['AKS', 'Managed Kubernetes'],
])
AZURE_STORAGE_T = dict(headers=['Type', 'Use'], rows=[
    ['Blob', 'Object storage (Hot/Cool/Cold/Archive)'],
    ['Files', 'SMB file shares'],
    ['Queues', 'Message queuing'],
    ['Tables', 'NoSQL key-value'],
    ['Disks', 'VM persistent disks'],
])
SECURE_STACK = [
    ('Edge', 'WAF, Shield, CloudFront'),
    ('Network', 'Security groups, NACLs'),
    ('Identity', 'IAM roles, MFA, least privilege'),
    ('Data', 'KMS encryption, Macie'),
    ('Detective', 'CloudTrail, Config, GuardDuty'),
]
RESILIENT_TIERS = [
    ('DNS', ['Route 53 health checks', 'Multi-region failover']),
    ('Load balancing', ['ALB across AZs']),
    ('Compute', ['Auto Scaling in 2+ AZs']),
    ('Data', ['RDS Multi-AZ', 'S3 cross-region replication']),
]
DATA_PROT = [
    ('KMS', 'Managed encryption keys, envelope encryption.'),
    ('CloudHSM', 'Dedicated hardware key control.'),
    ('Macie', 'Finds sensitive data in S3.'),
    ('TLS everywhere', 'Encrypt data in transit.'),
    ('Backup + versioning', 'Recover from deletion / ransomware.'),
]
DOP_POLICY = [
    ('AWS Config', 'Record + evaluate resource compliance.'),
    ('Organizations SCPs', 'Guardrails across accounts.'),
    ('CloudFormation Guard', 'Policy-as-code checks.'),
    ('Tag policies', 'Enforce cost/owner tags.'),
]
MONITOR_CW = [
    ('Metrics', 'CPU, latency, custom namespaces.'),
    ('Alarms', 'Threshold → SNS action.'),
    ('Logs', 'Centralized, Insights queries.'),
    ('X-Ray', 'Distributed tracing.'),
    ('Dashboards', 'Single-pane operations view.'),
]
DEPLOY_AWS = [
    ('CodeCommit', 'Source in git'),
    ('CodeBuild', 'Compile + test'),
    ('CodeDeploy', 'Rolling / blue-green deploy'),
    ('CodePipeline', 'Wire stages together'),
]
HA_DOP = [
    ('Multi-AZ', 'Survive a zone failure'),
    ('Auto Scaling', 'Match capacity to demand'),
    ('Health checks', 'Replace bad instances'),
    ('Backups', 'RDS snapshots, AMIs'),
]
GOVERNANCE_AZ = [
    ('Management groups', 'Hierarchy over subscriptions.'),
    ('Azure Policy', 'Enforce / audit compliance.'),
    ('RBAC', 'Least-privilege role grants.'),
    ('Locks', 'CanNotDelete / ReadOnly guards.'),
    ('Tags', 'Owner, cost center, env.'),
]
ENTRA_FLOW = [
    ('Sign-in', 'User hits the app'),
    ('Entra ID auth', 'Password / passwordless check'),
    ('Conditional Access', 'Policy: MFA? compliant?'),
    ('Token', 'ID + access tokens issued'),
    ('Resource', 'App / API authorized'),
]
M365_COMP = [
    ('DLP', 'Block sensitive data leaks.'),
    ('Retention', 'Keep / delete on schedule.'),
    ('eDiscovery', 'Legal hold + search.'),
    ('Sensitivity labels', 'Classify + encrypt.'),
    ('Defender', 'XDR across M365.'),
]
INTUNE = [
    ('Enroll', 'Devices join management.'),
    ('Compliance', 'Policies check health.'),
    ('Config profiles', 'Push settings at scale.'),
    ('App deploy', 'Required / available apps.'),
    ('Wipe / retire', 'Offboard securely.'),
]

# ---------------------------------------------------------------------------
# Curated diagrams: cloud providers (AWS, Azure, OCI, M365, SC)
# ---------------------------------------------------------------------------

# --- aws-clf ---
K('aws-clf', 'cloud-concepts', 'tiers', 'Cloud Service Models',
  'The three cloud service models, from most to least customer control.',
  tiers=[('IaaS', ['EC2', 'VPC', 'EBS']), ('PaaS', ['Elastic Beanstalk', 'RDS', 'Lambda']),
         ('SaaS', ['WorkMail', 'QuickSight', 'Connect'])])
K('aws-clf', 'shared-responsibility', 'table', 'Shared Responsibility Model',
  'AWS secures the cloud itself; the customer secures what they put in it.', **SHARED_RESP)
K('aws-clf', 'core-services', 'topology', 'AWS Core Services',
  'The foundational services every AWS workload touches.', center='AWS Cloud (Region)',
  spokes=AWS_CORE_SPOKE)
K('aws-clf', 'pricing-billing', 'keypoints', 'AWS Pricing Fundamentals',
  'How AWS charges: pay-as-you-go with tools to track it.',
  items=[('Pay as you go', 'No upfront cost; billed per second/minute of use.'),
         ('Cost Explorer', 'Visualize spend by service, tag, account.'),
         ('Budgets', 'Alert (or act) when spend crosses thresholds.'),
         ('Pricing Calculator', 'Estimate before you build.'),
         ('Free Tier', '12-month + always-free allowances for new accounts.')])
K('aws-clf', 'security-basics', 'layers', 'Defense in Depth on AWS',
  'Security controls stacked from the edge down to the data.', layers=SECURE_STACK)
K('aws-clf', 'support-plans', 'table', 'AWS Support Plans',
  'Higher tiers add faster response and proactive guidance.', headers=['Plan', 'Response / perks'],
  rows=[['Basic', 'Docs + 7 core checks'], ['Developer', 'Business-hours email'],
        ['Business', '24/7, <1h urgent'], ['Enterprise On-Ramp', 'Pool of TAMs, <30m'],
        ['Enterprise', 'Dedicated TAM, <15m']])

# --- aws-saa ---
K('aws-saa', 'resilient-architectures', 'tiers', 'Multi-AZ Resilient Architecture',
  'Design so the failure of one Availability Zone changes nothing for users.', tiers=RESILIENT_TIERS)
K('aws-saa', 'high-performing-architectures', 'keypoints', 'High-Performing Architectures',
  'Elasticity plus caching at every layer.',
  items=[('Auto Scaling', 'Add/remove capacity on demand or schedule.'),
         ('Caching', 'CloudFront + ElastiCache cut latency and DB load.'),
         ('Read replicas', 'RDS/Aurora replicas absorb read traffic.'),
         ('Right instance types', 'Match compute, memory, or I/O profile.'),
         ('Decouple', 'SQS/SNS buffer bursts between tiers.')])
K('aws-saa', 'secure-architectures', 'layers', 'Secure Architecture Layers',
  'Controls from the edge down to detective monitoring.', layers=SECURE_STACK)
K('aws-saa', 'cost-optimized-architectures', 'table', 'EC2 Purchasing Options',
  'Match commitment to workload steadiness.', **EC2_BUY_T)
K('aws-saa', 'compute', 'table', 'AWS Compute Options',
  'Pick by control needs and operational appetite.', **COMPUTE_T)
K('aws-saa', 'storage-database', 'table', 'AWS Storage & Database',
  'Object, block, file, relational, NoSQL — each has one job.', **STORAGE_T)

# --- aws-data ---
K('aws-data', 'data-ingestion', 'flow', 'Data Ingestion on AWS',
  'Getting data into AWS reliably, batch or streaming.',
  steps=[('Sources', 'Apps, DBs, IoT, files'), ('Kinesis / MSK', 'Streaming intake'),
         ('DMS / DataSync', 'DB migration / file sync'), ('S3 (raw zone)', 'Durable landing'),
         ('Glue catalog', 'Schema registered')],
  note='Batch: DataSync / Transfer Family · Streaming: Kinesis, MSK')
K('aws-data', 'data-lakes-warehouses', 'tiers', 'Lake → Warehouse on AWS',
  'Raw data lands cheap in S3; curated marts serve analytics.',
  tiers=[('Lake (S3)', ['Raw zone', 'Curated zone']), ('Catalog + ETL', ['Glue catalog', 'Glue jobs']),
         ('Serve', ['Athena (serverless SQL)', 'Redshift (warehouse)'])])
K('aws-data', 'processing-frameworks', 'flow', 'Batch & Stream Processing',
  'Transform raw data into queryable form.',
  steps=[('EMR / Spark', 'Big batch jobs'), ('Glue ETL', 'Serverless Spark'),
         ('Lambda', 'Micro-batch / events'), ('Athena views', 'Query in place')])
K('aws-data', 'data-governance', 'keypoints', 'Data Governance on AWS',
  'Know what you have, who touches it, and whether it complies.',
  items=[('Glue Data Catalog', 'Central schema + table registry.'),
         ('Lake Formation', 'Fine-grained access to lakes.'),
         ('Macie', 'Discovers PII/PHI in S3.'),
         ('CloudTrail', 'Who did what, when.'),
         ('Tagging', 'Owner, sensitivity, lifecycle tags.')])
K('aws-data', 'orchestration', 'flow', 'Pipeline Orchestration',
  'Schedule and coordinate data workflows.',
  steps=[('EventBridge', 'Schedule / event trigger'), ('Step Functions', 'Coordinate steps'),
         ('Glue / Lambda', 'Do the work'), ('SNS', 'Alert on failure')])
K('aws-data', 'analytics', 'keypoints', 'Analytics on AWS',
  'Query and visualize without moving data twice.',
  items=[('Athena', 'Serverless SQL directly on S3.'),
         ('Redshift', 'Petabyte-scale warehouse.'),
         ('QuickSight', 'BI dashboards, pay per session.'),
         ('OpenSearch', 'Log + full-text analytics.')])

# --- aws-dop ---
K('aws-dop', 'sdlc-automation', 'flow', 'AWS CI/CD Pipeline',
  'CodeCommit → CodeBuild → CodeDeploy, wired by CodePipeline.', steps=DEPLOY_AWS)
K('aws-dop', 'iac-config-management', 'commands', 'IaC & Config Commands',
  'CloudFormation and Systems Manager are the DOP workhorses.',
  cmds=[('aws cloudformation deploy --template-file t.yaml --stack-name s',
         'Deploy a stack from a template'),
        ('aws cloudformation describe-stacks', 'Inspect stack status'),
        ('aws ssm send-command --instance-ids i-1 --document-name AWS-RunShellScript',
         'Run commands fleet-wide'),
        ('aws ssm get-parameter --name /app/db', 'Read Parameter Store'),
        ('sam build && sam deploy', 'Build + deploy serverless apps')])
K('aws-dop', 'monitoring-logging', 'keypoints', 'Monitoring on AWS',
  'Metrics, logs, and traces feeding alarms and dashboards.', items=MONITOR_CW)
K('aws-dop', 'policies-standards', 'keypoints', 'Policies & Standards',
  'Guardrails that keep accounts compliant by default.', items=DOP_POLICY)
K('aws-dop', 'incident-response', 'flow', 'Incident Response (NIST 800-61)',
  'The standard six-phase incident lifecycle.', steps=IR_PHASES)
K('aws-dop', 'high-availability-recovery', 'keypoints', 'HA & Recovery Patterns',
  'Survive failures without heroics.', items=HA_DOP)

# --- aws-ml ---
K('aws-ml', 'ml-concepts', 'flow', 'ML Workflow on AWS',
  'The standard machine-learning lifecycle.', steps=ML_LIFECYCLE)
K('aws-ml', 'sagemaker', 'tiers', 'Amazon SageMaker Platform',
  'Managed ML from labeling to hosting.',
  tiers=[('Prepare', ['Ground Truth (labeling)', 'Data Wrangler']),
         ('Build + Train', ['Training jobs', 'Experiments', 'Feature Store']),
         ('Deploy', ['Endpoints (real-time)', 'Batch Transform', 'Pipelines (MLOps)'])])
K('aws-ml', 'data-prep', 'keypoints', 'Data Prep for ML',
  'Models are only as good as their training data.',
  items=[('Data Wrangler', 'Visual data prep for ML.'),
         ('Feature Store', 'Share features train ↔ serve.'),
         ('Ground Truth', 'Human labeling workflows.'),
         ('Class balance', 'Fix skew before training.')])
K('aws-ml', 'model-training', 'keypoints', 'Training on SageMaker',
  'Managed training with experiment tracking.',
  items=[('Training jobs', 'Managed compute, spot support.'),
         ('Hyperparameter tuning', 'Automatic search (Bayesian).'),
         ('Distributed', 'Data/model parallel libraries.'),
         ('Experiments', 'Track runs, params, metrics.')])
K('aws-ml', 'deployment-mlops', 'flow', 'Deploying Models (MLOps)',
  'From trained artifact to monitored endpoint.',
  steps=[('Model registry', 'Versioned artifacts'), ('Endpoint', 'Real-time inference'),
         ('Batch Transform', 'Offline scoring'), ('Model Monitor', 'Drift + quality')])
K('aws-ml', 'genai-on-aws', 'tiers', 'Generative AI on AWS (Bedrock)',
  'Foundation models as a managed API.',
  tiers=[('Models', ['Anthropic, Meta, Mistral', 'Amazon Titan/Nova']),
         ('Customize', ['Knowledge Bases (RAG)', 'Agents', 'Guardrails']),
         ('Consume', ['Bedrock API', 'Your application'])])

# --- aws-scs ---
K('aws-scs', 'threat-detection', 'flow', 'Threat Detection Services',
  'Layered detection across accounts and workloads.',
  steps=[('GuardDuty', 'ML anomaly findings'), ('Security Hub', 'Aggregated posture'),
         ('Macie', 'Sensitive data in S3'), ('Inspector', 'EC2/ECR vuln scans'),
         ('Detective', 'Investigation graphs')])
K('aws-scs', 'logging-monitoring', 'flow', 'Security Logging Pipeline',
  'Every API call recorded, centralized, and queryable.',
  steps=[('CloudTrail', 'API activity log'), ('CloudWatch Logs', 'Central ingestion'),
         ('S3 (archive)', 'Immutable long-term store'), ('Athena', 'Ad-hoc forensics')])
K('aws-scs', 'infrastructure-security', 'layers', 'Infrastructure Security Layers',
  'Filter hostile traffic before it reaches workloads.', layers=SECURE_STACK)
K('aws-scs', 'iam', 'flow', 'IAM Policy Evaluation',
  'How AWS decides allow vs deny — order matters.', steps=IAM_EVAL)
K('aws-scs', 'data-protection', 'keypoints', 'Data Protection on AWS',
  'Encrypt, classify, and retain deliberately.', items=DATA_PROT)
K('aws-scs', 'incident-response', 'flow', 'Incident Response (NIST 800-61)',
  'Detect, contain, eradicate, recover — then learn.', steps=IR_PHASES)

# --- aws-soa ---
K('aws-soa', 'monitoring-reporting', 'keypoints', 'Monitoring & Reporting',
  'Operate with metrics, alarms, and dashboards.', items=MONITOR_CW)
K('aws-soa', 'high-availability', 'keypoints', 'High Availability Operations',
  'Design and operate for failure.', items=HA_DOP)
K('aws-soa', 'deployment-provisioning', 'flow', 'Deployment & Provisioning',
  'Repeatable, automated releases.', steps=DEPLOY_AWS)
K('aws-soa', 'storage-data', 'table', 'AWS Storage & Database',
  'Right store for the access pattern.', **STORAGE_T)
K('aws-soa', 'security-compliance', 'keypoints', 'Security & Compliance Ops',
  'Continuous guardrails, not one-time audits.', items=DOP_POLICY + DATA_PROT[:2])
K('aws-soa', 'networking', 'topology', 'VPC Networking',
  'Subnets, gateways, and stateless/stateful filters.', center='VPC 10.0.0.0/16',
  spokes=VPC_SPOKE)

# --- az-104 ---
K('az-104', 'identity', 'flow', 'Microsoft Entra ID Sign-In',
  'Authenticate, evaluate policy, then issue tokens.', steps=ENTRA_FLOW)
K('az-104', 'governance-compliance', 'keypoints', 'Governance & Compliance',
  'Keep subscriptions organized and compliant.', items=GOVERNANCE_AZ)
K('az-104', 'storage', 'table', 'Azure Storage Types',
  'One account, five data services; blob tiers by access frequency.', **AZURE_STORAGE_T)
K('az-104', 'compute', 'table', 'Azure Compute Options',
  'From VMs to serverless — pick your control level.', **AZURE_COMPUTE_T)
K('az-104', 'networking', 'topology', 'Azure Virtual Network',
  'The software-defined network everything attaches to.', center='VNet 10.0.0.0/16',
  spokes=VNET_SPOKE)
K('az-104', 'monitoring', 'keypoints', 'Azure Monitor',
  'Metrics, logs, and alerts across the estate.',
  items=[('Metrics', 'Platform + custom time series.'),
         ('Log Analytics', 'KQL over centralized logs.'),
         ('Alerts', 'Metric / log / activity triggers.'),
         ('Action groups', 'Email, SMS, webhook, runbook.'),
         ('Application Insights', 'App-level telemetry.')])

# --- az-305 ---
K('az-305', 'identity-security-design', 'flow', 'Identity & Security Design',
  'Design flow: identify actors, then layer controls.',
  steps=[('Actors', 'Users, apps, workloads'), ('Entra ID', 'Single identity plane'),
         ('Conditional Access', 'Risk-based policy'), ('Privileged access', 'PIM, just-in-time'),
         ('Monitoring', 'Identity Protection, logs')])
K('az-305', 'data-solutions', 'table', 'Azure Data Platform Choices',
  'Relational, NoSQL, lake — by consistency and scale needs.',
  headers=['Service', 'Best for'],
  rows=[['Azure SQL Database', 'Relational, PaaS SQL'], ['Cosmos DB', 'Global NoSQL, multi-model'],
        ['ADLS Gen2', 'Analytics data lake'], ['Synapse', 'Warehouse + big data']])
K('az-305', 'business-continuity', 'keypoints', 'Business Continuity Design',
  'RTO/RPO drive every continuity decision.', items=RTO_RPO + BACKUP_321[:2])
K('az-305', 'infrastructure-design', 'tiers', 'Landing Zone Design',
  'Enterprise-scale structure for Azure estates.',
  tiers=[('Management', ['Management groups', 'Policy', 'Blueprints']),
         ('Connectivity', ['Hub VNet', 'ExpressRoute / VPN']),
         ('Workloads', ['Spoke VNets', 'App tiers'])])
K('az-305', 'integration', 'flow', 'Integration Services Flow',
  'Events in, orchestrated actions out.',
  steps=[('Event Grid', 'Event routing'), ('Service Bus', 'Reliable messaging'),
         ('Logic Apps', 'Workflow orchestration'), ('API Management', 'Governed APIs')])
K('az-305', 'migration', 'flow', 'Cloud Migration Stages',
  'Assess, move, then optimize — in waves.',
  steps=[('Assess', 'Azure Migrate discovery'), ('Migrate', 'Rehost / refactor waves'),
         ('Optimize', 'Rightsize, reserved pricing'), ('Secure', 'Policy + Defender')])

# --- az-700 ---
K('az-700', 'vnet-design', 'topology', 'Hub-and-Spoke VNet Design',
  'Shared services in the hub; workloads peered as spokes.', center='Hub VNet',
  spokes=['Spoke: apps', 'Spoke: data', 'VPN Gateway', 'ExpressRoute', 'Azure Firewall', 'DNS (private zones)'])
K('az-700', 'connectivity', 'table', 'Azure Connectivity Options',
  'Private paths between VNets and on-premises.', headers=['Option', 'Use'],
  rows=[['VNet peering', 'Low-latency VNet ↔ VNet'], ['VPN Gateway', 'Encrypted over internet'],
        ['ExpressRoute', 'Private dedicated circuit'], ['Virtual WAN', 'Global transit hub']])
K('az-700', 'routing', 'flow', 'Traffic Routing Decisions',
  'How Azure picks the path for each packet.',
  steps=[('System routes', 'Default Azure routes'), ('UDR', 'Custom next hop'),
         ('BGP', 'On-prem routes via gateway'), ('Effective routes', 'NIC-effective set')])
K('az-700', 'private-access', 'keypoints', 'Private Access to PaaS',
  'Keep platform traffic off the public internet.',
  items=[('Private Endpoint', 'NIC in your VNet for PaaS.'),
         ('Private Link', 'The service-side counterpart.'),
         ('Service endpoints', 'VNet identity to Azure services.'),
         ('Private DNS zones', 'Resolve privatelink names.')])
K('az-700', 'monitoring', 'keypoints', 'Network Monitoring',
  'Watch connectivity, not just uptime.',
  items=[('Network Watcher', 'Topology, packet capture, flow logs.'),
         ('Connection Monitor', 'Probes between endpoints.'),
         ('Traffic Analytics', 'Flow-log insights.'),
         ('NSG flow logs', 'Who talked to whom.')])
K('az-700', 'security', 'layers', 'Network Security Layers',
  'Filter at the edge, the subnet, and the host.', layers=[
      ('Edge', 'Azure Firewall, DDoS Protection'), ('Subnet', 'NSGs — allow/deny rules'),
      ('Host', 'App Gateway WAF, JIT access'), ('Monitor', 'Sentinel, flow logs')])

# --- azure-developer ---
K('azure-developer', 'app-service-functions', 'tiers', 'App Service & Functions',
  'Host web apps and event-driven code without servers.',
  tiers=[('App Service', ['Web Apps', 'Slots (staging)']), ('Functions', ['HTTP triggers', 'Timer/queue triggers']),
         ('Shared', ['App Service plan', 'Application Insights'])])
K('azure-developer', 'storage-sdks', 'keypoints', 'Azure Storage for Developers',
  'SDK patterns that show up in every app.',
  items=[('BlobClient', 'Upload/download blobs.'),
         ('Connection strings', 'Prefer managed identity instead.'),
         ('SAS tokens', 'Time-boxed delegated access.'),
         ('Azurite', 'Local emulator for dev.')])
K('azure-developer', 'auth-managed-identity', 'flow', 'Managed Identity Auth',
  'No secrets in code — Azure issues the identity.',
  steps=[('App', 'Runs with managed identity'), ('Entra ID', 'Issues token for resource'),
         ('Key Vault', 'Token grants secret access'), ('API call', 'Authenticated request')])
K('azure-developer', 'containers', 'flow', 'Container Delivery on Azure',
  'Build once, run on ACI, ACA, or AKS.',
  steps=[('ACR', 'Private registry'), ('Build', 'az acr build / pipelines'),
         ('Deploy', 'ACI / Container Apps / AKS'), ('Monitor', 'Container Insights')])
K('azure-developer', 'azure-openai', 'tiers', 'Azure OpenAI Integration',
  'Managed frontier models behind your VNet.',
  tiers=[('Models', ['GPT-class', 'Embeddings']), ('Deploy', ['Deployments', 'Content filters']),
         ('App', ['Chat completions API', 'Your UX'])])
K('azure-developer', 'monitoring', 'keypoints', 'App Monitoring',
  'Know before your users tell you.',
  items=[('Application Insights', 'Requests, deps, exceptions.'),
         ('Live Metrics', 'Real-time stream.'),
         ('Availability tests', 'URL pings from probes.'),
         ('Smart Detection', 'Anomaly alerts.')])

# --- oracle-oci ---
K('oracle-oci', 'regions-ads', 'topology', 'OCI Region & Availability Domains',
  'Each region holds isolated ADs for fault tolerance.', center='OCI Region',
  spokes=['AD-1', 'AD-2', 'AD-3', 'Compartments', 'IAM policies', 'Object Storage (regional)'])
K('oracle-oci', 'compute', 'keypoints', 'OCI Compute',
  'Bare metal to flexible VMs.',
  items=[('Bare Metal', 'No hypervisor, HPC-grade.'),
         ('VM shapes', 'Fixed + Flex (custom OCPU/RAM).'),
         ('Container Engine (OKE)', 'Managed Kubernetes.'),
         ('Functions', 'Serverless Fn Project.'),
         ('Autoscaling', 'Instance pools scale out.')])
K('oracle-oci', 'networking', 'topology', 'OCI Virtual Cloud Network',
  'VCNs, subnets, and gateways per region design.', center='VCN 10.0.0.0/16', spokes=OCI_VCN_SPOKE)
K('oracle-oci', 'storage', 'table', 'OCI Storage Options',
  'Block, object, and file — by access pattern.', headers=['Service', 'Use'],
  rows=[['Block Volume', 'Boot + data volumes'], ['Object Storage', 'Unlimited objects'],
        ['File Storage', 'NFS shares'], ['Archive Storage', 'Rare access, cheap']])
K('oracle-oci', 'iam-security', 'flow', 'OCI IAM Authorization',
  'Policies in compartments grant groups permissions.',
  steps=[('User', 'Authenticates to tenancy'), ('Group', 'Membership checked'),
         ('Compartment', 'Scope of the policy'), ('Policy', 'Allow group to verb in compartment'),
         ('Decision', 'Allow or deny')])
K('oracle-oci', 'pricing-governance', 'keypoints', 'OCI Pricing & Governance',
  'Track spend and enforce structure.',
  items=[('Universal Credits', 'Prepaid, flexible drawdown.'),
         ('Cost Analysis', 'Spend by compartment/tag.'),
         ('Budgets', 'Alert on forecast overrun.'),
         ('Compartments', 'Isolation + cost boundaries.')])

# --- oracle-db ---
K('oracle-db', 'architecture', 'tiers', 'Oracle Database Architecture',
  'Instance (memory) vs database (files) — the core distinction.', tiers=ORACLE_ARCH)
K('oracle-db', 'installation', 'flow', 'Oracle Installation Flow',
  'Plan, install software, then create the database.',
  steps=[('Prereqs', 'OS, users, kernel params'), ('Software', 'Run installer / RPM'),
         ('Listener', 'Configure net services'), ('DBCA', 'Create the database'),
         ('Verify', 'Connect, check alert log')])
K('oracle-db', 'storage', 'keypoints', 'Oracle Storage Structures',
  'Logical units map to physical files.',
  items=[('Tablespaces', 'Logical containers (SYSTEM, SYSAUX, USERS).'),
         ('Datafiles', 'Physical files backing tablespaces.'),
         ('Control files', 'Database structure metadata.'),
         ('Redo logs', 'Every change recorded for recovery.'),
         ('ASM', 'Automatic Storage Management option.')])
K('oracle-db', 'backup-recovery', 'flow', 'RMAN Backup & Recovery',
  'Configure, back up, validate, and rehearse restores.', steps=RMAN_FLOW)
K('oracle-db', 'performance', 'keypoints', 'Performance Tuning Basics',
  'Measure first, then tune the top wait events.',
  items=[('AWR reports', 'Snapshot-based diagnostics.'),
         ('ASH', 'Active session history sampling.'),
         ('Execution plans', 'EXPLAIN PLAN before tuning SQL.'),
         ('Indexes', 'Right index, right columns.'),
         ('SGA sizing', 'Buffer cache vs shared pool.')])
K('oracle-db', 'dataguard', 'topology', 'Oracle Data Guard',
  'Physical standby kept in sync via redo transport.', center='Data Guard',
  spokes=['Primary database', 'Physical standby', 'Redo transport', 'Fast-start failover', 'Observer', 'Switchover tests'])

# --- oracle-sql ---
K('oracle-sql', 'select', 'commands', 'SELECT Essentials',
  'The core query building blocks.',
  cmds=[('SELECT col1, col2 FROM employees', 'Pick columns from a table'),
        ('SELECT * FROM t WHERE hire_date > DATE \'2020-01-01\'', 'Filter rows'),
        ('SELECT DISTINCT dept FROM emp', 'Unique values only'),
        ('SELECT … ORDER BY salary DESC', 'Sort results'),
        ('SELECT … FETCH FIRST 10 ROWS ONLY', 'Top-N rows (12c+)'),
        ('SELECT COUNT(*) FROM t', 'Row count')])
K('oracle-sql', 'joins-subqueries', 'table', 'JOIN Types',
  'How tables combine — and what survives.', **JOINS_T)
K('oracle-sql', 'ddl-dml', 'commands', 'DDL & DML Statements',
  'Define structures, then manipulate rows.',
  cmds=[('CREATE TABLE t (id NUMBER PRIMARY KEY, n VARCHAR2(50))', 'Define a table'),
        ('ALTER TABLE t ADD (c DATE)', 'Change structure'),
        ('INSERT INTO t VALUES (1, \'a\')', 'Add a row'),
        ('UPDATE t SET n=\'b\' WHERE id=1', 'Change rows'),
        ('DELETE FROM t WHERE id=1', 'Remove rows'),
        ('TRUNCATE TABLE t', 'Fast full-table empty'),
        ('COMMIT / ROLLBACK', 'Persist or undo a transaction')])
K('oracle-sql', 'functions', 'keypoints', 'SQL Functions',
  'Single-row and group functions you will use daily.',
  items=[('TO_CHAR / TO_DATE', 'Format conversions.'),
         ('NVL / COALESCE', 'Handle NULLs safely.'),
         ('SUBSTR / INSTR', 'String slicing + search.'),
         ('ROUND / TRUNC', 'Number + date rounding.'),
         ('DECODE / CASE', 'Conditional expressions.')])
K('oracle-sql', 'plsql-blocks', 'flow', 'PL/SQL Block Structure',
  'Every anonymous block follows this skeleton.', steps=PLSQL_FLOW)
K('oracle-sql', 'packages-triggers', 'keypoints', 'Packages & Triggers',
  'Modular PL/SQL and automatic reactions.', items=TRIGGERS)

# --- m365 ---
K('m365', 'tenant-identity', 'flow', 'Microsoft 365 Identity',
  'Entra ID is the front door to every M365 workload.', steps=ENTRA_FLOW)
K('m365', 'exchange-online', 'keypoints', 'Exchange Online',
  'Cloud mail with enterprise controls.',
  items=[('Mailboxes', '50–100 GB, archive options.'),
         ('Mail flow', 'Connectors, transport rules.'),
         ('Defender for Office', 'Anti-phish, Safe Links/Attachments.'),
         ('Shared mailboxes', 'Team addresses, no license.'),
         ('Retention', 'MRM policies per mailbox.')])
K('m365', 'sharepoint-onedrive', 'keypoints', 'SharePoint & OneDrive',
  'Files with versioning, sharing, and governance.',
  items=[('OneDrive', 'Personal cloud storage per user.'),
         ('SharePoint sites', 'Team + communication sites.'),
         ('Versioning', 'Restore earlier file versions.'),
         ('Sharing links', 'Anyone / people / specific links.'),
         ('Migration', 'SharePoint Migration Tool.')])
K('m365', 'teams', 'keypoints', 'Microsoft Teams',
  'Chat, meetings, and collaboration hub.',
  items=[('Teams & channels', 'Organize by workstream.'),
         ('Meetings', 'Schedule, record, transcribe.'),
         ('Phone System', 'PSTN calling via Teams.'),
         ('Policies', 'Messaging, meeting, app policies.'),
         ('Admin center', 'Usage, call quality dashboard.')])
K('m365', 'compliance', 'keypoints', 'Microsoft Purview Compliance',
  'Protect and govern data across M365.', items=M365_COMP)
K('m365', 'endpoint-intune', 'keypoints', 'Endpoint Management (Intune)',
  'Manage devices without on-prem servers.', items=INTUNE)

# --- ms-fundamentals ---
K('ms-fundamentals', 'azure-concepts', 'tiers', 'Azure Building Blocks',
  'Regions, resources, and the management hierarchy.',
  tiers=[('Geography', ['Regions', 'Availability Zones']), ('Management', ['Management groups', 'Subscriptions', 'Resource groups']),
         ('Resources', ['Compute', 'Storage', 'Network'])])
K('ms-fundamentals', 'ai-fundamentals', 'keypoints', 'AI Fundamentals',
  'Core vocabulary before touching any AI service.',
  items=[('Machine learning', 'Learn patterns from data.'),
         ('Computer vision', 'Images → labels, objects, OCR.'),
         ('NLP', 'Language understanding + generation.'),
         ('Generative AI', 'Creates text, images, code.'),
         ('Responsible AI', 'Fairness, reliability, safety.')])
K('ms-fundamentals', 'data-fundamentals', 'keypoints', 'Data Fundamentals',
  'Relational vs non-relational, batch vs streaming.',
  items=[('Relational', 'Tables, SQL, ACID.'),
         ('NoSQL', 'Documents, key-value, graph.'),
         ('Data warehouse', 'Structured analytics store.'),
         ('Data lake', 'Raw, any format.'),
         ('ETL / ELT', 'Move + transform pipelines.')])
K('ms-fundamentals', 'security-fundamentals', 'layers', 'Defense in Depth',
  'No single control is enough — stack them.', layers=DEFENSE_DEPTH)
K('ms-fundamentals', 'pricing-sla', 'keypoints', 'Pricing & SLAs',
  'Pay for use; SLAs promise uptime.',
  items=[('Pay-as-you-go', 'Metered consumption.'),
         ('Reserved instances', 'Commit for discounts.'),
         ('Spot VMs', 'Spare capacity, cheap, evictable.'),
         ('SLA', 'Uptime % with service credits.'),
         ('Composite SLA', 'Multiply component SLAs.')])
K('ms-fundamentals', 'governance', 'keypoints', 'Azure Governance',
  'Organize, control, and audit at scale.', items=GOVERNANCE_AZ)

# --- sc-200 ---
K('sc-200', 'sentinel-workspaces', 'flow', 'Microsoft Sentinel Workflow',
  'From log onboarding to automated response.', steps=SENTINEL_FLOW)
K('sc-200', 'kql-hunting', 'commands', 'KQL Hunting Essentials',
  'The query language behind Sentinel investigations.',
  cmds=KQL_CMDS, note='KQL is read-only: it queries, never changes data.')
K('sc-200', 'incidents-playbooks', 'flow', 'Incident → Playbook Response',
  'Triage once, automate the repeatable parts.',
  steps=[('Incident', 'Analytics rule fires'), ('Triage', 'Assign severity, owner'),
         ('Playbook', 'Logic App runs steps'), ('Enrich', 'Add TI + entity data'),
         ('Close', 'Resolve with classification')])
K('sc-200', 'defender-xdr', 'keypoints', 'Microsoft Defender XDR',
  'Correlated defense across endpoints, identity, email, apps.',
  items=[('Defender for Endpoint', 'EDR on devices.'),
         ('Defender for Identity', 'AD threat detection.'),
         ('Defender for Office', 'Email + collaboration.'),
         ('Defender for Cloud Apps', 'SaaS visibility (CASB).'),
         ('Incidents', 'Cross-product correlation.')])
K('sc-200', 'threat-intel', 'keypoints', 'Threat Intelligence in Sentinel',
  'Turn external intel into detections.', items=THREAT_INTEL)
K('sc-200', 'response', 'flow', 'Response Actions',
  'Contain first, then eradicate and recover.',
  steps=[('Isolate', 'Device / account isolation'), ('Block', 'IPs, URLs, hashes'),
         ('Revoke', 'Sessions + credentials'), ('Collect', 'Forensic artifacts'),
         ('Restore', 'Reimage, reset, monitor')])

# --- sc-300 ---
K('sc-300', 'user-group-lifecycle', 'flow', 'Identity Lifecycle',
  'Joiner → mover → leaver, automated.',
  steps=[('Joiner', 'Account + access provisioned'), ('Mover', 'Role change updates access'),
         ('Access reviews', 'Managers recertify'), ('Leaver', 'Access revoked promptly')])
K('sc-300', 'authentication', 'flow', 'Modern Authentication Flow',
  'Passwords plus a second factor — or none at all.', steps=MFA_FLOW)
K('sc-300', 'conditional-access', 'flow', 'Conditional Access Policy',
  'If-then rules evaluated at every sign-in.', steps=COND_ACCESS)
K('sc-300', 'pim-access-reviews', 'keypoints', 'PIM & Access Reviews',
  'Just-in-time privilege with oversight.', items=PIM)
K('sc-300', 'app-integration', 'flow', 'SSO App Integration',
  'Wire SaaS apps into Entra ID once.',
  steps=[('Register', 'Enterprise app created'), ('SSO mode', 'SAML or OIDC chosen'),
         ('Attributes', 'Claims mapped'), ('Assign', 'Users/groups granted'),
         ('Test', 'Single sign-on verified')])
K('sc-300', 'monitoring', 'keypoints', 'Identity Monitoring',
  'Watch the front door continuously.',
  items=[('Sign-in logs', 'Who, where, result.'),
         ('Audit logs', 'Admin + config changes.'),
         ('Identity Protection', 'Risk detections + policies.'),
         ('Access reviews', 'Scheduled recertification.')])

# ---------------------------------------------------------------------------
# Curated diagrams: security (CISSP, CISM, pentest, SOC, zero trust, CompTIA)
# ---------------------------------------------------------------------------

# --- cissp (8) ---
K('cissp', 'risk-gov', 'keypoints', 'Risk & Governance Essentials',
  'Governance sets direction; risk management quantifies the exposure.',
  items=[('Governance', 'Policies flow from business objectives.'),
         ('Risk = threat × vulnerability × impact', 'The core formula.'),
         ('Qualitative vs quantitative', 'Scales vs dollars (ALE = SLE × ARO).'),
         ('Risk responses', 'Avoid, transfer, mitigate, accept.'),
         ('Security frameworks', 'NIST CSF, ISO 27001, COBIT.')])
K('cissp', 'asset-sec', 'keypoints', 'Asset Security',
  'You cannot protect what you have not classified.',
  items=[('Classification', 'Public / internal / confidential / restricted.'),
         ('Ownership', 'Every asset has an accountable owner.'),
         ('Handling', 'Labeling, storage, transport rules.'),
         ('Retention', 'Keep per policy, destroy securely.'),
         ('Data states', 'At rest, in transit, in use.')])
K('cissp', 'sec-arch', 'keypoints', 'Security Architecture Models',
  'Formal models that define allowed information flow.', items=BLA)
K('cissp', 'net-sec', 'layers', 'OSI Model — Security View',
  'Know what lives at each layer to place controls correctly.', layers=OSI_LAYERS)
K('cissp', 'iam', 'keypoints', 'Identity & Access Management',
  'Identification, authentication, authorization, accountability.', items=AAA + RBAC[:2])
K('cissp', 'assess-test', 'keypoints', 'Assessment & Testing',
  'Prove controls work — on a schedule, not on faith.',
  items=[('Vulnerability scans', 'Automated, frequent, noisy.'),
         ('Penetration tests', 'Human-led, scoped, goal-driven.'),
         ('Audits', 'Independent control validation.'),
         ('Log review', 'Continuous detective control.'),
         ('Misuse testing', 'Abuse-case validation.')])
K('cissp', 'sec-ops', 'flow', 'Security Operations: Incident Response',
  'The NIST 800-61 lifecycle every SOC follows.', steps=IR_PHASES)
K('cissp', 'sw-sec', 'flow', 'Secure SDLC',
  'Security activities woven into each SDLC phase.',
  steps=[('Requirements', 'Abuse cases, security reqs'), ('Design', 'Threat modeling'),
         ('Code', 'Secure coding, SAST'), ('Test', 'DAST, pen test'),
         ('Deploy', 'Hardened config, secrets mgmt')])

# --- cism (4) ---
K('cism', 'governance', 'keypoints', 'Information Security Governance',
  'Security serves the business — governed from the top.',
  items=[('Board oversight', 'Accountability starts at the top.'),
         ('Security strategy', 'Aligned to business objectives.'),
         ('Policies & standards', 'The governance backbone.'),
         ('Metrics', 'Report risk in business terms.')])
K('cism', 'risk-mgmt', 'keypoints', 'Risk Management (CISM)',
  'Identify, assess, treat, and monitor information risk.',
  items=[('Risk assessment', 'Threats, vulns, impact, likelihood.'),
         ('ALE = SLE × ARO', 'Annualized loss expectancy.'),
         ('Treatment options', 'Mitigate, transfer, avoid, accept.'),
         ('Risk register', 'Living record of decisions.'),
         ('Emerging risk', 'Reassess on change.')])
K('cism', 'program-dev', 'flow', 'Security Program Development',
  'Build the program in deliberate stages.',
  steps=[('Assess', 'Current-state gap analysis'), ('Design', 'Roadmap + resource plan'),
         ('Implement', 'Controls + awareness'), ('Measure', 'Metrics + audits'),
         ('Improve', 'Continuous refinement')])
K('cism', 'incident-mgmt', 'flow', 'Incident Management (CISM)',
  'Detect, respond, recover — with business coordination.', steps=IR_PHASES)

# --- pentest ---
K('pentest', 'recon-enum', 'commands', 'Recon & Enumeration Commands',
  'Passive first, then careful active probing — always in scope.',
  cmds=[('whois example.com', 'Registrar + contact intel'),
        ('dig +short example.com ANY', 'DNS records overview'),
        ('nmap -sV -O target', 'Service + OS fingerprinting'),
        ('nmap --top-ports 1000 target', 'Fast common-port sweep'),
        ('gobuster dir -u https://t -w wordlist', 'Directory brute-forcing'),
        ('theHarvester -d example.com -b all', 'OSINT email/host harvest')],
  note='Only against targets you are authorized to test.')
K('pentest', 'vuln-analysis', 'flow', 'Vulnerability Analysis Workflow',
  'Scan broadly, then validate manually.', steps=VULN_MGMT)
K('pentest', 'exploitation', 'keypoints', 'Exploitation Fundamentals',
  'Prove impact — carefully, within scope.',
  items=[('Metasploit', 'Framework: exploit + payload + session.'),
         ('Manual > automated', 'Validate every scanner finding.'),
         ('Payload types', 'Bind vs reverse shells.'),
         ('Post modules', 'Privilege, persistence, loot.'),
         ('Scope discipline', 'Stop at the engagement boundary.')])
K('pentest', 'post-exploitation', 'flow', 'Post-Exploitation Sequence',
  'What happens after the first shell.',
  steps=[('Stabilize', 'Upgrade to a full TTY shell'), ('Enumerate', 'Users, creds, network'),
         ('Escalate', 'Local privesc to SYSTEM/root'), ('Persist', 'Only if in scope'),
         ('Pivot', 'Move laterally carefully')])
K('pentest', 'web-attacks', 'keypoints', 'Top Web Attack Classes',
  'OWASP Top 10 (2021) — six of ten shown; full list in the lesson.', items=OWASP21)
K('pentest', 'reporting', 'keypoints', 'Pen Test Reporting',
  'The report is the product — findings must drive fixes.',
  items=[('Executive summary', 'Risk in business language.'),
         ('Findings', 'Severity, evidence, impact.'),
         ('Reproduction', 'Steps to reproduce each issue.'),
         ('Remediation', 'Concrete fix guidance.'),
         ('Retest', 'Verify fixes closed the holes.')])

# --- comptia-cyber ---
K('comptia-cyber', 'threat-intel', 'keypoints', 'Threat Intelligence Levels',
  'Different consumers need different intel.', items=THREAT_INTEL)
K('comptia-cyber', 'vuln-mgmt', 'flow', 'Vulnerability Management Lifecycle',
  'A loop, not a project.', steps=VULN_MGMT)
K('comptia-cyber', 'siem', 'flow', 'SIEM Data Pipeline',
  'From raw logs to analyst-ready alerts.', steps=SIEM_FLOW)
K('comptia-cyber', 'pentest-method', 'flow', 'Penetration Testing Methodology',
  'The PTES phases in order.', steps=PTES)
K('comptia-cyber', 'exploitation', 'keypoints', 'Exploitation Basics',
  'Understand the classes to defend against them.',
  items=[('Buffer overflows', 'Overwrite memory past bounds.'),
         ('Injection', 'Untrusted input becomes code.'),
         ('Password attacks', 'Spraying, stuffing, cracking.'),
         ('Social engineering', 'The human attack surface.')])
K('comptia-cyber', 'reporting', 'keypoints', 'Security Reporting',
  'Communicate risk so it gets fixed.',
  items=[('Severity ratings', 'CVSS + business context.'),
         ('Evidence', 'Screenshots, logs, commands.'),
         ('Remediation', 'Prioritized, actionable steps.'),
         ('Trends', 'Track posture over time.')])

# --- comptia-core ---
K('comptia-core', 'hardware', 'keypoints', 'Hardware Fundamentals',
  'Know the parts before you troubleshoot them.',
  items=[('CPU', 'Cores, threads, cache, sockets.'),
         ('RAM', 'DDR generations, capacity, ECC.'),
         ('Storage', 'SSD/NVMe vs HDD; interfaces.'),
         ('Motherboard', 'Chipset, buses, form factors.'),
         ('Power', 'Wattage, rails, redundancy.')])
K('comptia-core', 'networking', 'layers', 'OSI Model (7 Layers)',
  'Memorize top-to-bottom: All People Seem To Need Data Processing.', layers=OSI_LAYERS)
K('comptia-core', 'os', 'keypoints', 'Operating System Basics',
  'Windows, Linux, macOS — same jobs, different tools.',
  items=[('Processes', 'Task Manager / ps manage them.'),
         ('File systems', 'NTFS, ext4, APFS.'),
         ('Permissions', 'NTFS ACLs vs rwx.'),
         ('Boot', 'UEFI → bootloader → kernel.'),
         ('Updates', 'Patch on a schedule.')])
K('comptia-core', 'sec-fund', 'keypoints', 'Security Fundamentals',
  'The CIA triad plus the controls that enforce it.', items=CIA)
K('comptia-core', 'ops', 'flow', 'Operational Procedures',
  'Work like a professional: document and communicate.',
  steps=[('Plan', 'Scope the change / ticket'), ('Implement', 'Follow the procedure'),
         ('Document', 'Record what changed'), ('Verify', 'Confirm the outcome'),
         ('Communicate', 'Notify stakeholders')])
K('comptia-core', 'pbq', 'keypoints', 'PBQ Strategy',
  'Performance-based questions reward method, not memorization.',
  items=[('Read twice', 'Understand the actual ask.'),
         ('Eliminate', 'Rule out impossible options.'),
         ('Hands-on first', 'Practice in labs, not just books.'),
         ('Timebox', 'Flag and return if stuck.')])

# --- comptia-infra ---
K('comptia-infra', 'cloud-arch', 'tiers', 'Cloud Service Models',
  'Who manages what in each model.',
  tiers=[('IaaS', ['VMs', 'Virtual networks']), ('PaaS', ['Databases', 'App platforms']),
         ('SaaS', ['Email', 'CRM', 'Collaboration'])])
K('comptia-infra', 'linux-admin', 'commands', 'Linux Admin Essentials',
  'Daily-driver commands for servers.',
  cmds=[('ls -la / df -h / du -sh', 'List, disk free, dir size'),
        ('chmod 644 / chown app:app', 'Permissions + ownership'),
        ('ps aux / kill -15', 'Processes + graceful kill'),
        ('systemctl enable --now svc', 'Service now + at boot'),
        ('journalctl -xe / tail -f', 'Logs: errors / live tail'),
        ('ip addr / ss -tulpn', 'Network state')])
K('comptia-infra', 'server-hw', 'table', 'RAID Levels Compared',
  'Redundancy costs capacity — choose deliberately.', **RAID)
K('comptia-infra', 'virtualization', 'tiers', 'Virtualization Stack',
  'Hypervisor types and what runs on them.',
  tiers=[('Type 1 (bare metal)', ['Hyper-V', 'ESXi', 'KVM']), ('Type 2 (hosted)', ['VirtualBox', 'VMware Workstation']),
         ('Guests', ['VMs with guest OS'])])
K('comptia-infra', 'data', 'keypoints', 'Data Protection Basics',
  'Backups you test beat backups you hope about.', items=BACKUP_321)
K('comptia-infra', 'ops-sec', 'keypoints', 'Operations Security',
  'Harden the day-to-day, not just the perimeter.',
  items=[('Patching', 'OS + apps on schedule.'),
         ('Least privilege', 'Admin only where needed.'),
         ('Logging', 'Centralize and review.'),
         ('Change control', 'Approve before production.')])

# --- soc-analyst ---
K('soc-analyst', 'soc-workflow', 'flow', 'SOC Analyst Workflow',
  'Alert in, verdict out — with escalation paths.',
  steps=[('Alert', 'SIEM fires a case'), ('Triage', 'True/false positive?'),
         ('Investigate', 'Timeline + entities'), ('Contain', 'Isolate if real'),
         ('Escalate / close', 'Tier 2 or documented close')])
K('soc-analyst', 'log-analysis', 'keypoints', 'Log Analysis Essentials',
  'Read logs like timelines, not text files.',
  items=[('Normalize time', 'UTC everywhere; mind zones.'),
         ('Pivot on entities', 'IP, user, host, hash.'),
         ('Baseline first', 'Know normal to spot abnormal.'),
         ('Correlate', 'One event is noise; chains are signal.')])
K('soc-analyst', 'detection-engineering', 'flow', 'Detection Engineering Loop',
  'Write, tune, and retire detections deliberately.',
  steps=[('Hypothesis', 'What attacker behavior?'), ('Data', 'Which logs cover it?'),
         ('Rule', 'Write the detection'), ('Tune', 'Cut false positives'),
         ('Measure', 'Precision + coverage review')])
K('soc-analyst', 'triage-escalation', 'flow', 'Triage & Escalation',
  'Fast, consistent decisions under alert volume.',
  steps=[('Severity', 'Impact × confidence'), ('Scope', 'One host or many?'),
         ('Contain?', 'Isolate now if spreading'), ('Escalate', 'Tier 2 with context'),
         ('Document', 'Timeline in the ticket')])
K('soc-analyst', 'containment', 'keypoints', 'Containment Playbook',
  'Stop the bleeding without destroying evidence.',
  items=[('Isolate host', 'Network quarantine first.'),
         ('Disable accounts', 'Cut attacker access.'),
         ('Block IOCs', 'Firewall / proxy / mail.'),
         ('Preserve memory', 'Capture before reboot.'),
         ('Communicate', 'Notify per the runbook.')])
K('soc-analyst', 'threat-intel', 'keypoints', 'Threat Intel for SOC',
  'Intel is only useful when it drives action.', items=THREAT_INTEL)

# --- zerotrust ---
K('zerotrust', 'zt-principles', 'keypoints', 'Zero Trust Principles',
  'Never trust, always verify — every request.', items=ZERO_TRUST)
K('zerotrust', 'identity-ad', 'flow', 'Identity-First Access',
  'Identity is the new perimeter.',
  steps=[('Authenticate', 'Strong, phishing-resistant MFA'), ('Device check', 'Compliant + healthy?'),
         ('Policy', 'Conditional Access evaluates'), ('Least privilege', 'Scoped, time-boxed grant'),
         ('Monitor', 'Continuous session risk')])
K('zerotrust', 'segmentation', 'tiers', 'Segmentation Tiers',
  'Blast-radius control from network to workload.',
  tiers=[('Identity', ['Per-user access']), ('Network', ['Microsegmentation', 'Software-defined perimeter']),
         ('Workload', ['Pod / container isolation', 'Service mesh policy'])])
K('zerotrust', 'cryptography', 'table', 'Cryptography Choices',
  'Right algorithm for the job.', **SYM_ASYM)
K('zerotrust', 'allowlisting', 'keypoints', 'Allowlisting Strategy',
  'Default-deny beats default-allow.',
  items=[('Application allowlist', 'Only approved binaries run.'),
         ('Network allowlist', 'Egress to known-good only.'),
         ('Maintenance', 'Update lists with change control.'),
         ('Exceptions', 'Time-boxed, approved, logged.')])
K('zerotrust', 'redblue', 'keypoints', 'Red vs Blue Teams',
  'Attackers and defenders sharpening each other.',
  items=[('Red team', 'Emulate real adversaries.'),
         ('Blue team', 'Detect, respond, harden.'),
         ('Purple team', 'Collaborative improvement.'),
         ('Assume breach', 'Exercises start compromised.')])

# --- hackers-arise ---
K('hackers-arise', 'linux-hardening', 'commands', 'Linux Hardening Commands',
  'Reduce attack surface on every host.',
  cmds=[('ufw enable / firewall-cmd', 'Host firewall on'),
        ('chmod 600 ~/.ssh/*', 'Lock down SSH keys'),
        ('passwd -l root', 'Lock the root account'),
        ('apt update && apt upgrade', 'Patch promptly'),
        ('ss -tulpn', 'Audit listening services'),
        ('lastlog / lastb', 'Login + failed-login review')])
K('hackers-arise', 'networking-security', 'keypoints', 'Network Security Basics',
  'See the traffic before you trust it.',
  items=[('Segmentation', 'VLANs isolate trust zones.'),
         ('Firewall rules', 'Default deny, allow by need.'),
         ('IDS/IPS', 'Snort/Suricata detect + block.'),
         ('VPN', 'Encrypt remote access.')])
K('hackers-arise', 'scripting', 'commands', 'Bash Scripting Essentials',
  'Automate the boring, audit the rest.', cmds=BASH_CMDS)
K('hackers-arise', 'crypto-basics', 'crypto', 'Symmetric Encryption',
  'One shared key locks and unlocks the data.',
  left='Plaintext', left_sub='Readable data', key_label='AES-256 key',
  key_sub='Shared secret, 256-bit', right='Ciphertext', right_sub='Unreadable without key')
K('hackers-arise', 'forensics-intro', 'flow', 'Order of Volatility',
  'Collect the most ephemeral evidence first.', steps=VOLATILITY)
K('hackers-arise', 'defensive-mindset', 'keypoints', 'Defensive Mindset',
  'Think like the attacker to defend like a pro.',
  items=[('Assume breach', 'Hunt, do not just wait.'),
         ('Least privilege', 'Everywhere, always.'),
         ('Patch fast', 'Known vulns are gifts.'),
         ('Backups', 'Tested restores beat ransom.')])

# --- nsa-codebreaker (puzzle-oriented: safe concept maps) ---
K('nsa-codebreaker', 'crypto-puzzles', 'keypoints', 'Cryptographic Puzzle Tools',
  'Techniques that crack classical ciphers.',
  items=[('Frequency analysis', 'Letter counts betray substitution.'),
         ('Known plaintext', 'Cribs anchor the key.'),
         ('Brute force', 'Small keyspaces fall fast.'),
         ('Pattern words', 'Repeated cribs reveal structure.')])
K('nsa-codebreaker', 'reversing', 'flow', 'Reverse Engineering Workflow',
  'From binary to understanding.',
  steps=[('Strings', 'Extract readable hints'), ('Disassemble', 'objdump / Ghidra'),
         ('Trace', 'Follow control flow'), ('Dynamic', 'Debugger + breakpoints'),
         ('Reconstruct', 'Document the logic')])
K('nsa-codebreaker', 'net-analysis', 'keypoints', 'Network Traffic Analysis',
  'Packets do not lie — if you capture them.',
  items=[('pcap capture', 'tcpdump / Wireshark.'),
         ('Follow streams', 'Reassemble conversations.'),
         ('Protocol dissectors', 'Decode the layers.'),
         ('Anomalies', 'Beaconing, odd ports, exfil.')])
K('nsa-codebreaker', 'forensics', 'flow', 'Forensic Challenge Approach',
  'Methodical beats clever.', steps=VOLATILITY[:5])
K('nsa-codebreaker', 'web-exploit', 'keypoints', 'Web Challenge Patterns',
  'Common footholds in web puzzles.',
  items=[('Input reflection', 'XSS / template injection.'),
         ('Auth bypass', 'Logic flaws, JWT tricks.'),
         ('IDOR', 'Change the ID, change the data.'),
         ('Source review', 'Comments leak secrets.')])
K('nsa-codebreaker', 'programming', 'keypoints', 'Puzzle Programming Toolkit',
  'Script the tedium away.',
  items=[('Python', 'The lingua franca of puzzles.'),
         ('pwntools', 'Exploit dev scaffolding.'),
         ('Requests', 'Automate web interaction.'),
         ('Iterate fast', 'REPL-driven solving.')])

# --- dod-8140 ---
K('dod-8140', 'framework-8140', 'keypoints', 'DoD 8140 Framework',
  'Seven workforce categories structure cyber work roles.',
  items=NICE_CATS + [('Qualification', 'Cert + training + experience per role.')])
K('dod-8140', 'work-roles', 'keypoints', '8140 Work Roles',
  'Roles map to categories, each with tasks and KSAs.',
  items=[('Role definition', 'Tasks, knowledge, skills, abilities.'),
         ('Categories', 'SP, OM, OV, PR, AN, CO, IN.'),
         ('Position coding', 'Billets coded to work roles.'),
         ('Career paths', 'Roles ladder within categories.')])
K('dod-8140', 'baseline-certs', 'table', 'DoD Baseline Certifications',
  '8140/8570 baseline certs by workforce level.', **DOD_BASELINE)
K('dod-8140', 'cssp-roles', 'keypoints', 'CSSP Roles',
  'Cybersecurity Service Provider functions.',
  items=[('CSSP Analyst', 'Monitor + analyze events.'),
         ('CSSP Incident Responder', 'Handle incidents.'),
         ('CSSP Auditor', 'Assess compliance.'),
         ('CSSP Manager', 'Lead the provider team.')])
K('dod-8140', 'continuing-ed', 'keypoints', 'Continuing Education',
  'Certifications expire — stay qualified.',
  items=[('CEUs', 'Earn via training, teaching, writing.'),
         ('Renewal cycles', 'Typically 3 years.'),
         ('Track early', 'Do not scramble at deadline.'),
         ('Employer support', 'Many fund CE activities.')])
K('dod-8140', 'career-mapping', 'flow', '8140 Career Mapping',
  'From current role to target work role.',
  steps=[('Current role', 'Code your billet'), ('Target role', 'Pick the work role'),
         ('Gap analysis', 'Certs + KSAs missing'), ('Training plan', 'Close the gaps'),
         ('Qualify', 'Earn + document')])

# --- nice-framework (8) ---
K('nice-framework', 'framework-structure', 'keypoints', 'NICE Framework Structure',
  'Categories → specialty areas → work roles.',
  items=NICE_CATS + [('Specialty areas', '33 focus areas within categories.'),
                     ('Work roles', '52 detailed roles with KSAs.')])
K('nice-framework', 'securely-provision', 'keypoints', 'Securely Provision (SP)',
  'Conceptualize, design, and build secure IT systems.',
  items=[('Secure architecture', 'Design security in.'),
         ('Software development', 'Secure coding practices.'),
         ('Systems development', 'Secure lifecycle.'),
         ('Test & evaluation', 'Verify before deploy.')])
K('nice-framework', 'operate-maintain', 'keypoints', 'Operate & Maintain (OM)',
  'Keep systems available and performing.',
  items=[('System administration', 'Day-to-day operations.'),
         ('Network services', 'Keep traffic flowing.'),
         ('Systems analysis', 'Improve performance.')])
K('nice-framework', 'oversee-govern', 'keypoints', 'Oversee & Govern (OV)',
  'Leadership, law, and strategy.',
  items=[('Cybersecurity management', 'Run the program.'),
         ('Legal / privacy', 'Compliance and counsel.'),
         ('Executive leadership', 'Set direction.')])
K('nice-framework', 'protect-defend', 'keypoints', 'Protect & Defend (PR)',
  'Defend the enterprise in real time.',
  items=[('Incident response', 'Handle active incidents.'),
         ('Defense analysis', 'Tune defenses.'),
         ('Vuln assessment', 'Find weaknesses first.')])
K('nice-framework', 'analyze', 'keypoints', 'Analyze (AN)',
  'Turn data into decisions.',
  items=[('Threat analysis', 'Understand adversaries.'),
         ('Exploitation analysis', 'Study attacker tools.'),
         ('Forensics analysis', 'Reconstruct events.')])
K('nice-framework', 'collect-operate', 'keypoints', 'Collect & Operate (CO)',
  'Collect and operate specialized capabilities.',
  items=[('Collection ops', 'Gather cyber intel.'),
         ('Cyber operations', 'Offensive/defensive ops.')])
K('nice-framework', 'investigate', 'keypoints', 'Investigate (IN)',
  'Digital forensics and investigation.',
  items=[('Cyber investigation', 'Pursue cybercrime.'),
         ('Digital forensics', 'Evidence-grade analysis.')])

# ---------------------------------------------------------------------------
# Curated diagrams: languages, web, data, AI
# ---------------------------------------------------------------------------

# --- python ---
K('python', 'fundamentals', 'table', 'Python Core Types',
  'Mutability decides what you can change in place.', **PY_TYPES_T)
K('python', 'data-structures', 'keypoints', 'Choosing Data Structures',
  'Pick by access pattern and uniqueness needs.',
  items=[('list', 'Ordered, mutable — the default sequence.'),
         ('tuple', 'Ordered, immutable — safe records.'),
         ('dict', 'Key → value, O(1) average lookup.'),
         ('set', 'Unique members, fast membership.'),
         ('Comprehensions', '[x for x in …] builds them fast.')])
K('python', 'functions-modules', 'keypoints', 'Functions & Modules',
  'Organize code into reusable units.',
  items=[('def + return', 'Functions encapsulate logic.'),
         ('*args / **kwargs', 'Flexible signatures.'),
         ('import', 'Modules namespace code.'),
         ('__name__ == "__main__"', 'Script vs import guard.'),
         ('Decorators', '@wrap functions with behavior.')])
K('python', 'oop', 'layers', 'OOP Pillars in Python',
  'Four ideas that structure object-oriented design.', layers=OOP_PILLARS)
K('python', 'stdlib-files', 'commands', 'Stdlib & Files Cheat Sheet',
  'Batteries included — reach for these first.',
  cmds=[('open("f.txt") / pathlib.Path', 'Read/write files safely'),
        ('import json / csv', 'Parse common formats'),
        ('import os / sys', 'OS + interpreter access'),
        ('import shutil / glob', 'Copy trees / match files'),
        ('datetime.now()', 'Timestamps done right'),
        ('with open(...) as f:', 'Auto-close file handles')])
K('python', 'errors-debugging', 'flow', 'Exception Handling Flow',
  'try → except → else → finally, in order.', steps=EXCEPT_FLOW)

# --- c-lang ---
K('c-lang', 'syntax-types', 'table', 'C Type Sizes (typical)',
  'Exact sizes vary by platform — these are the common LP64 values.',
  headers=['Type', 'Size', 'Use'],
  rows=[['char', '1 byte', 'Characters, bytes'], ['int', '4 bytes', 'General integers'],
        ['long', '8 bytes', 'Large integers'], ['float / double', '4 / 8 bytes', 'Reals']])
K('c-lang', 'pointers-memory', 'keypoints', 'Pointers & Memory',
  'C gives you the address — and the responsibility.', items=POINTERS)
K('c-lang', 'arrays-strings', 'keypoints', 'Arrays & Strings in C',
  'Arrays decay to pointers; strings end with \\0.',
  items=[('int a[10]', 'Fixed-size, stack array.'),
         ('a[i] == *(a+i)', 'Indexing is pointer math.'),
         ('char s[] = "hi"', 'String = chars + null terminator.'),
         ('strcpy/strncpy', 'Copy with bounds care.'),
         ('No bounds checking', 'You enforce the limits.')])
K('c-lang', 'structs-files', 'keypoints', 'Structs & File I/O',
  'Group data; stream bytes deliberately.',
  items=[('struct', 'Group heterogeneous fields.'),
         ('typedef', 'Name your types.'),
         ('fopen modes', 'r, w, a, r+, binary b.'),
         ('fread / fwrite', 'Binary I/O by element.'),
         ('fclose', 'Flush + release the handle.')])
K('c-lang', 'preprocessor-build', 'flow', 'C Build Pipeline',
  'Source to binary in four stages.', steps=C_BUILD)
K('c-lang', 'debugging', 'commands', 'GDB Essentials',
  'Debug compiled C with confidence.', cmds=GDB_CMDS)

# --- cpp ---
K('cpp', 'core-syntax', 'keypoints', 'C++ Core Syntax',
  'C with classes — and a few sharp edges filed down.',
  items=[('References (&)', 'Aliases, safer than raw pointers.'),
         ('const correctness', 'Mark what must not change.'),
         ('Namespaces', 'std:: organizes the library.'),
         ('auto', 'Let the compiler deduce types.'),
         ('Range-for', 'for (auto& x : v) iterate cleanly.')])
K('cpp', 'oop-cpp', 'layers', 'OOP Pillars in C++',
  'Plus virtual dispatch for runtime polymorphism.', layers=OOP_PILLARS)
K('cpp', 'stl-containers', 'table', 'STL Container Complexities',
  'Pick containers by access and insertion cost.', **STL_T)
K('cpp', 'memory-smart-pointers', 'keypoints', 'Smart Pointers & RAII',
  'Ownership expressed in types — leaks become compile-time thinking.', items=SMART_PTRS)
K('cpp', 'templates-lambdas', 'keypoints', 'Templates & Lambdas',
  'Generic code without runtime cost.',
  items=[('Function templates', 'template<typename T> …'),
         ('Class templates', 'vector<T> pattern.'),
         ('Lambdas', '[capture](args){ body }'),
         ('STL algorithms', 'sort, find_if, transform.')])
K('cpp', 'build-toolchain', 'flow', 'C++ Build Toolchain',
  'From sources to executable.',
  steps=[('Preprocess', 'Headers expanded'), ('Compile', 'Objects built'),
         ('Link', 'Executable linked'), ('CMake', 'Cross-platform builds'),
         ('Sanitizers', 'ASan/UBSan catch bugs')])

# --- java ---
K('java', 'language-core', 'keypoints', 'Java Language Core',
  'Write once, run on the JVM.',
  items=[('Bytecode', 'javac compiles to .class files.'),
         ('JVM', 'Interprets/JITs bytecode per platform.'),
         ('Garbage collection', 'Automatic memory management.'),
         ('Strong typing', 'Checked at compile time.'),
         ('Packages', 'Namespace organization.')])
K('java', 'oop-design', 'layers', 'OOP Pillars in Java',
  'Interfaces and abstract classes shape the design.', layers=OOP_PILLARS)
K('java', 'collections-generics', 'table', 'Java Collections',
  'Interface first, implementation by need.', **COLLECTIONS_T)
K('java', 'streams-lambdas', 'flow', 'Stream Pipeline',
  'Source → intermediate ops → terminal op.', steps=STREAM_FLOW)
K('java', 'concurrency-virtual-threads', 'keypoints', 'Java Concurrency',
  'From platform threads to virtual threads.',
  items=[('Thread', 'OS-backed, expensive.'),
         ('Virtual threads', 'Lightweight, millions possible.'),
         ('ExecutorService', 'Pool + submit tasks.'),
         ('synchronized', 'Mutual exclusion keyword.'),
         ('CompletableFuture', 'Async composition.')])
K('java', 'modules-jars-io', 'keypoints', 'Modules, JARs & I/O',
  'Package and ship Java applications.',
  items=[('JAR', 'Zip of classes + manifest.'),
         ('JPMS modules', 'module-info.java boundaries.'),
         ('NIO.2', 'Modern file I/O (Paths, Files).'),
         ('Serialization', 'Object → bytes, carefully.')])

# --- dotnet ---
K('dotnet', 'csharp-language', 'keypoints', 'C# Language Essentials',
  'Modern, expressive, and null-aware.',
  items=[('Nullable refs', 'string? forces null thinking.'),
         ('async/await', 'Non-blocking I/O idioms.'),
         ('Records', 'Immutable data carriers.'),
         ('Pattern matching', 'switch expressions.'),
         ('Top-level statements', 'Less ceremony in scripts.')])
K('dotnet', 'oop-linq', 'keypoints', 'OOP + LINQ',
  'Query collections like a database.',
  items=[('Where / Select', 'Filter + project sequences.'),
         ('OrderBy / GroupBy', 'Sort + aggregate.'),
         ('First / Single', 'Pick elements safely.'),
         ('Deferred execution', 'Queries run on enumeration.'),
         ('IEnumerable<T>', 'The core abstraction.')])
K('dotnet', 'aspnet-core', 'flow', 'ASP.NET Core Middleware Pipeline',
  'Each middleware sees the request in order.', steps=MIDDLEWARE_FLOW)
K('dotnet', 'entity-framework', 'keypoints', 'Entity Framework Core',
  'Code-first data access with change tracking.',
  items=[('DbContext', 'Unit of work + session.'),
         ('DbSet<T>', 'Queryable entity sets.'),
         ('Migrations', 'Schema as code versions.'),
         ('Change tracking', 'Detect + persist edits.'),
         ('LINQ to SQL', 'Queries translated to SQL.')])
K('dotnet', 'testing', 'keypoints', 'Testing in .NET',
  'xUnit is the default; structure tests well.',
  items=[('xUnit', 'Facts + theories.'),
         ('Arrange-Act-Assert', 'Test anatomy.'),
         ('Moq', 'Isolate dependencies.'),
         ('Coverage', 'Measure what tests touch.')])
K('dotnet', 'deploy-tooling', 'flow', 'Build & Deploy Flow',
  'From source to running service.',
  steps=[('dotnet build', 'Compile the solution'), ('dotnet test', 'Run the suite'),
         ('dotnet publish', 'Trimmed output'), ('Container', 'Ship as image'),
         ('Deploy', 'App Service / AKS / VM')])

# --- spring ---
K('spring', 'core-di', 'keypoints', 'Spring Core & DI',
  'Inversion of control: the container wires beans.',
  items=[('@Component', 'Marks a bean for scanning.'),
         ('@Autowired', 'Constructor injection preferred.'),
         ('Bean scopes', 'Singleton vs prototype.'),
         ('@Configuration', 'Java-based config.'),
         ('Profiles', 'dev / prod bean variants.')])
K('spring', 'web-rest', 'flow', 'Spring REST Request Flow',
  'DispatcherServlet to controller to response.',
  steps=[('DispatcherServlet', 'Front controller'), ('@RestController', 'Handler mapping'),
         ('@Service', 'Business logic'), ('@Repository', 'Data access'),
         ('JSON response', 'Jackson serialization')])
K('spring', 'data-jpa', 'keypoints', 'Spring Data JPA',
  'Repositories without boilerplate.',
  items=[('@Entity', 'Maps class to table.'),
         ('JpaRepository', 'CRUD + paging free.'),
         ('Derived queries', 'findByName… parsed.'),
         ('@Query', 'Custom JPQL when needed.'),
         ('Transactions', '@Transactional boundaries.')])
K('spring', 'security', 'flow', 'Spring Security Filter Chain',
  'Requests pass through security filters first.',
  steps=[('Authentication', 'Who: login / token'), ('Authorization', 'What: roles, rules'),
         ('CSRF / CORS', 'Web protections'), ('Session / JWT', 'State strategy'),
         ('Access granted', 'Controller executes')])
K('spring', 'testing', 'keypoints', 'Testing Spring Apps',
  'Slice tests for speed, full context sparingly.',
  items=[('@SpringBootTest', 'Full context integration.'),
         ('@WebMvcTest', 'Controller slice + MockMvc.'),
         ('@DataJpaTest', 'Repository slice.'),
         ('Mockito', 'Mock collaborators.')])
K('spring', 'actuator-deploy', 'keypoints', 'Actuator & Deployment',
  'Production-ready endpoints and packaging.',
  items=[('/actuator/health', 'Liveness for orchestrators.'),
         ('/actuator/metrics', 'Micrometer telemetry.'),
         ('Fat JAR', 'java -jar ships all deps.'),
         ('Profiles', 'Externalized configuration.')])

# --- dsa ---
K('dsa', 'complexity-analysis', 'table', 'Big-O Complexities',
  'Growth rates you must recognize instantly.',
  headers=['Complexity', 'Name', 'Example'],
  rows=[['O(1)', 'Constant', 'Hash lookup'], ['O(log n)', 'Logarithmic', 'Binary search'],
        ['O(n)', 'Linear', 'Single scan'], ['O(n log n)', 'Linearithmic', 'Merge sort'],
        ['O(n²)', 'Quadratic', 'Nested loops'], ['O(2ⁿ)', 'Exponential', 'Naive recursion']])
K('dsa', 'arrays-strings-dsa', 'keypoints', 'Array & String Patterns',
  'The five patterns that solve most array problems.',
  items=[('Two pointers', 'Converge from both ends.'),
         ('Sliding window', 'Fixed/variable window max.'),
         ('Prefix sums', 'O(1) range queries.'),
         ('In-place', 'O(1) extra space edits.'),
         ('Run-length', 'Compress repetitions.')])
K('dsa', 'linked-structures', 'keypoints', 'Linked Structures',
  'Nodes + pointers: flexible but cache-unfriendly.',
  items=[('Singly linked', 'Next pointer only.'),
         ('Doubly linked', 'Prev + next, O(1) delete.'),
         ('Fast/slow pointers', 'Cycle + middle detection.'),
         ('Dummy head', 'Simplifies edge cases.')])
K('dsa', 'trees-graphs', 'keypoints', 'Trees & Graphs',
  'Traversals first, algorithms second.',
  items=[('BFS', 'Level order, shortest unweighted.'),
         ('DFS', 'Depth-first: pre/in/post-order.'),
         ('BST', 'Ordered: O(log n) average.'),
         ('Heap', 'Priority queue in array form.'),
         ('Dijkstra', 'Weighted shortest path.')])
K('dsa', 'sorting-searching', 'table', 'Sorting Algorithms',
  'Know the trade-offs, not just the names.',
  headers=['Algorithm', 'Average', 'Stable?'],
  rows=[['Quicksort', 'O(n log n)', 'No'], ['Merge sort', 'O(n log n)', 'Yes'],
        ['Heap sort', 'O(n log n)', 'No'], ['Bubble / insertion', 'O(n²)', 'Yes'],
        ['Binary search', 'O(log n)', '— (search)']])
K('dsa', 'dynamic-programming', 'keypoints', 'Dynamic Programming',
  'Overlapping subproblems + optimal substructure.',
  items=[('Memoization', 'Top-down recursion + cache.'),
         ('Tabulation', 'Bottom-up table fill.'),
         ('State definition', 'Name what dp[i] means.'),
         ('Classic set', 'Knapsack, LCS, LIS, coin change.')])

# --- sql ---
K('sql', 'queries', 'commands', 'SQL Query Essentials',
  'Read and filter with precision.', cmds=SQL_CMDS[:5])
K('sql', 'aggregations', 'commands', 'Aggregation Queries',
  'GROUP BY turns rows into summaries.',
  cmds=[('SELECT dept, COUNT(*) FROM emp GROUP BY dept', 'Count per group'),
        ('… HAVING COUNT(*) > 5', 'Filter groups, not rows'),
        ('SELECT AVG(salary) FROM emp', 'Average over rows'),
        ('SELECT MAX(hire_date) FROM emp', 'Latest date'),
        ('COUNT(DISTINCT dept)', 'Unique values count')])
K('sql', 'joins', 'table', 'JOIN Types Compared',
  'What each join keeps from each side.', **JOINS_T)
K('sql', 'windows', 'commands', 'Window Functions',
  'Compute across rows without collapsing them.',
  cmds=[('ROW_NUMBER() OVER (ORDER BY salary DESC)', 'Rank rows 1..n'),
        ('RANK() / DENSE_RANK()', 'Rank with/without gaps'),
        ('LAG(salary) OVER (PARTITION BY dept)', 'Previous row value'),
        ('SUM(sales) OVER (PARTITION BY region)', 'Running group totals')])
K('sql', 'tsql', 'keypoints', 'T-SQL Specifics',
  'SQL Server dialect notes.',
  items=[('TOP n', 'Limit rows (vs LIMIT).'),
         ('GETDATE()', 'Current timestamp.'),
         ('ISNULL / COALESCE', 'NULL handling.'),
         ('Stored procedures', 'Reusable server-side logic.')])
K('sql', 'performance', 'keypoints', 'Query Performance',
  'Make the slow query fast — methodically.',
  items=[('Indexes', 'B-tree on filter/join columns.'),
         ('Execution plans', 'Read before tuning.'),
         ('SARGable', 'Keep predicates index-friendly.'),
         ('Avoid SELECT *', 'Fetch only needed columns.')])

# --- mongodb ---
K('mongodb', 'documents-schema', 'schema', 'MongoDB Document Model',
  'Documents nest; _id is the primary key.',
  tables=[('orders', [('_id', 'PK'), ('customer_id', 'FK'), ('items[]', ''), ('total', '')]),
          ('customers', [('_id', 'PK'), ('email', ''), ('address{}', '')])],
  note='Embed for read-together data; reference for shared data.')
K('mongodb', 'crud', 'commands', 'mongosh CRUD',
  'The document operations you will run daily.', cmds=MONGOSH_CMDS)
K('mongodb', 'aggregation', 'flow', 'Aggregation Pipeline',
  'Documents flow through stages in order.', steps=MONGO_AGG)
K('mongodb', 'indexes', 'keypoints', 'MongoDB Indexes',
  'Index the queries you actually run.',
  items=[('Single field', 'db.c.createIndex({a:1})'),
         ('Compound', 'Order matters: equality → sort → range.'),
         ('_id', 'Always indexed, unique.'),
         ('Explain', ' winning plan before shipping.')])
K('mongodb', 'replication-sharding', 'topology', 'Replica Set',
  'Automatic failover via election.', center='Replica set',
  spokes=['Primary (writes)', 'Secondary (reads)', 'Secondary', 'Arbiter (votes)', 'Oplog sync'])
K('mongodb', 'administration', 'keypoints', 'MongoDB Administration',
  'Keep the cluster healthy and backed up.',
  items=[('mongodump / restore', 'Logical backups.'),
         ('Ops Manager', 'Managed monitoring.'),
         ('Users & roles', 'RBAC per database.'),
         ('Sharding', 'Shard key choice is forever-ish.')])

# --- data-analyst ---
K('data-analyst', 'sql-analysis', 'commands', 'Analyst SQL Toolkit',
  'The queries behind every dashboard.', cmds=SQL_CMDS)
K('data-analyst', 'spreadsheets', 'keypoints', 'Spreadsheet Power Moves',
  'Fast answers without a database.',
  items=[('Pivot tables', 'Drag-and-drop aggregation.'),
         ('VLOOKUP / XLOOKUP', 'Join-like lookups.'),
         ('Clean first', 'Trim, dedupe, fix types.'),
         ('Charts', 'Right chart for the question.')])
K('data-analyst', 'visualization', 'keypoints', 'Choosing the Right Chart',
  'Match the visual to the question.',
  items=[('Line', 'Trends over time.'),
         ('Bar', 'Compare categories.'),
         ('Scatter', 'Relationships.'),
         ('Histogram', 'Distributions.'),
         ('Avoid', '3D, dual axes, pie overload.')])
K('data-analyst', 'statistics', 'keypoints', 'Statistics for Analysts',
  'Describe data honestly.',
  items=[('Mean / median / mode', 'Center, robust center, common.'),
         ('Std dev', 'Spread around the mean.'),
         ('Correlation ≠ causation', 'The eternal caveat.'),
         ('Sampling', 'Random beats convenient.'),
         ('p-values', 'Evidence strength, not truth.')])
K('data-analyst', 'bi-tools', 'keypoints', 'BI Tool Concepts',
  'Power BI / Tableau share the same ideas.',
  items=[('Data model', 'Relationships between tables.'),
         ('DAX / LOD', 'Calculation languages.'),
         ('Dashboards', 'One screen, one story.'),
         ('Refresh', 'Scheduled data updates.')])
K('data-analyst', 'storytelling', 'flow', 'Data Storytelling Flow',
  'From raw numbers to a decision.',
  steps=[('Question', 'What decision needs data?'), ('Explore', 'Slice the dataset'),
         ('Insight', 'The non-obvious finding'), ('Narrative', 'Context → insight → ask'),
         ('Visual', 'One chart per message')])

# --- data-engineering ---
K('data-engineering', 'modeling', 'schema', 'Star Schema',
  'Facts in the center, dimensions around it.', tables=STAR_SCHEMA,
  note='Denormalized dims make analytics queries fast.')
K('data-engineering', 'etl', 'flow', 'ETL Pipeline',
  'Extract, transform, load — in that order.', steps=ETL_FLOW)
K('data-engineering', 'warehouses-lakes', 'table', 'Warehouse vs Lake vs Lakehouse',
  'Structure and cost trade-offs.', headers=['Aspect', 'Warehouse', 'Lake', 'Lakehouse'],
  rows=[['Data', 'Structured', 'Any format', 'Open formats'],
        ['Schema', 'On write', 'On read', 'Enforced on read'],
        ['Cost', 'Higher', 'Cheap', 'Cheap + governed'],
        ['Example', 'Snowflake', 'S3 + Athena', 'Delta Lake']])
K('data-engineering', 'streaming', 'flow', 'Streaming with Kafka',
  'Durable logs decouple producers and consumers.', steps=KAFKA_FLOW)
K('data-engineering', 'orchestration', 'flow', 'Orchestration (Airflow-style)',
  'DAGs schedule and retry pipeline tasks.',
  steps=[('DAG', 'Directed acyclic graph'), ('Tasks', 'Operators do work'),
         ('Schedule', 'Cron / event triggers'), ('Retry', 'Automatic on failure'),
         ('Monitor', 'UI + alerts')])
K('data-engineering', 'quality-governance', 'keypoints', 'Data Quality & Governance',
  'Trustworthy data is a feature.',
  items=[('Tests', 'Nulls, ranges, uniqueness checks.'),
         ('Lineage', 'Where did this column come from?'),
         ('Contracts', 'Schema agreements with producers.'),
         ('Catalog', 'Discoverable, documented datasets.')])

# --- datascience-ml ---
K('datascience-ml', 'math', 'keypoints', 'Math for ML',
  'The minimum viable mathematics.',
  items=[('Linear algebra', 'Vectors, matrices, dot products.'),
         ('Calculus', 'Derivatives, gradients, chain rule.'),
         ('Probability', 'Distributions, Bayes, expectation.'),
         ('Statistics', 'Hypothesis tests, confidence.')])
K('datascience-ml', 'supervised', 'table', 'Supervised Learning Map',
  'Labeled data in, predictions out.',
  headers=['Task', 'Algorithms'],
  rows=[['Regression', 'Linear, trees, gradient boosting'],
        ['Classification', 'Logistic, SVM, kNN, forests'],
        ['Deep learning', 'MLPs, CNNs, transformers']])
K('datascience-ml', 'unsupervised', 'keypoints', 'Unsupervised Learning',
  'Find structure without labels.',
  items=[('K-means', 'Partition into k clusters.'),
         ('DBSCAN', 'Density-based, finds outliers.'),
         ('PCA', 'Dimensionality reduction.'),
         ('Association', 'Market-basket rules.')])
K('datascience-ml', 'evaluation', 'table', 'Classification Metrics',
  'Accuracy alone lies on imbalanced data.', **EVAL_T)
K('datascience-ml', 'features', 'keypoints', 'Feature Engineering',
  'Better features beat fancier models.',
  items=[('Encoding', 'One-hot, ordinal, target.'),
         ('Scaling', 'Standardize for distance models.'),
         ('Selection', 'Drop noise, keep signal.'),
         ('Leakage', 'No future info in training.')])
K('datascience-ml', 'deployment', 'flow', 'Model Deployment Lifecycle',
  'From notebook to production.', steps=ML_LIFECYCLE)

# --- llm-engineering ---
K('llm-engineering', 'transformers', 'flow', 'Transformer Forward Pass',
  'How tokens become predictions.', steps=TRANSFORMER_FLOW)
K('llm-engineering', 'prompting', 'keypoints', 'Prompt Engineering',
  'Steer the model with structure, not hope.',
  items=[('Zero-shot', 'Ask directly, no examples.'),
         ('Few-shot', 'Show 2–5 examples.'),
         ('Chain-of-thought', '"Think step by step."'),
         ('System prompts', 'Set role + constraints.'),
         ('Temperature', 'Lower = deterministic.')])
K('llm-engineering', 'rag', 'tiers', 'RAG Architecture',
  'Ground the model in your documents.', tiers=RAG_TIERS)
K('llm-engineering', 'finetuning', 'flow', 'Fine-Tuning Pipeline',
  'Adapt a base model to your domain.', steps=FINETUNE_FLOW)
K('llm-engineering', 'agents', 'cycle', 'Agent Loop',
  'Perceive → reason → act → observe, until done.', steps=AGENT_LOOP)
K('llm-engineering', 'selfhosting', 'keypoints', 'Self-Hosting LLMs',
  'Run models on your own hardware.',
  items=[('vLLM / Ollama', 'Serving runtimes.'),
         ('VRAM math', 'Params × bytes ÷ GPU memory.'),
         ('Quantization', 'FP16/INT8/INT4 trade-offs.'),
         ('Licensing', 'Check commercial terms.')])

# --- ai-product ---
K('ai-product', 'llm-apis', 'keypoints', 'LLM API Fundamentals',
  'Build on hosted models without training anything.',
  items=[('Chat completions', 'Messages in, text out.'),
         ('Streaming', 'Token-by-token UX.'),
         ('Function calling', 'Structured tool use.'),
         ('Embeddings', 'Text → vectors for search.'),
         ('Rate limits', 'Design for retries + budgets.')])
K('ai-product', 'prompt-engineering', 'keypoints', 'Prompt Engineering for Products',
  'Prompts are product surface — version them.',
  items=[('System prompts', 'Persistent instructions.'),
         ('Few-shot', 'Examples beat explanations.'),
         ('Output schemas', 'JSON mode / function calls.'),
         ('Eval sets', 'Test prompts like code.')])
K('ai-product', 'rag-basics', 'tiers', 'RAG Product Pattern',
  'Your docs + a model = grounded answers.', tiers=RAG_TIERS)
K('ai-product', 'agent-loops', 'cycle', 'Agent Product Loop',
  'Autonomy with guardrails.', steps=AGENT_LOOP)
K('ai-product', 'evals', 'table', 'LLM Evaluation Metrics',
  'Measure quality before you ship.',
  headers=['Metric', 'Use'],
  rows=[['Accuracy / F1', 'Classification-style tasks'], ['BLEU / ROUGE', 'Text overlap (rough)'],
        ['Human eval', 'Gold standard, expensive'], ['Latency / cost', 'Production viability']])
K('ai-product', 'ai-coding-workflows', 'cycle', 'AI Coding Workflow',
  'Plan, generate, test, review — on repeat.',
  steps=[('Plan', 'Decompose the task'), ('Generate', 'Draft with the model'),
         ('Test', 'Run the suite'), ('Review', 'Human reads the diff')])

# --- nvidia-ai ---
K('nvidia-ai', 'gpu-computing', 'layers', 'GPU Memory Hierarchy',
  'Closer to the cores = faster and smaller.', layers=[
      ('Registers', 'Per-thread, fastest'), ('Shared memory', 'Per-block scratchpad'),
      ('L1 / L2 cache', 'On-chip caches'), ('HBM / GDDR', 'Device memory, GBs'),
      ('Host RAM', 'PCIe away — slowest')])
K('nvidia-ai', 'cuda-basics', 'keypoints', 'CUDA Basics',
  'Massive parallelism, one kernel at a time.',
  items=[('Kernels', 'Functions run on the GPU.'),
         ('Threads / blocks / grids', 'The launch hierarchy.'),
         ('Memory copies', 'Host ↔ device transfers.'),
         ('cuDNN / cuBLAS', 'Optimized DL primitives.'),
         ('NCCL', 'Multi-GPU communication.')])
K('nvidia-ai', 'dl-workflows', 'flow', 'Deep Learning Workflow',
  'Data to deployed model on GPUs.', steps=ML_LIFECYCLE)
K('nvidia-ai', 'inference-opt', 'keypoints', 'Inference Optimization',
  'Serve faster and cheaper.',
  items=[('Quantization', 'FP16 / INT8 precision cuts.'),
         ('TensorRT', 'Fused, optimized engines.'),
         ('Batching', 'Amortize launch overhead.'),
         ('KV cache', 'Reuse attention state.')])
K('nvidia-ai', 'rag-agents', 'tiers', 'GPU-Accelerated RAG Agents',
  'Embeddings and generation both love GPUs.', tiers=RAG_TIERS)
K('nvidia-ai', 'mlops-gpus', 'flow', 'MLOps on GPUs',
  'Train, optimize, serve, monitor.',
  steps=[('Train', 'Multi-GPU data parallel'), ('Checkpoint', 'Save + version'),
         ('Optimize', 'Quantize / TensorRT'), ('Serve', 'Triton / vLLM'),
         ('Monitor', 'Latency, drift, cost')])

# --- fullstack ---
K('fullstack', 'http-apis', 'table', 'HTTP Essentials',
  'Verbs and status codes you will use daily.',
  headers=['Topic', 'Key facts'],
  rows=[['Verbs', 'GET read · POST create · PUT replace · DELETE remove'],
        ['2xx', '200 OK · 201 Created · 204 No Content'],
        ['4xx', '400 Bad Request · 401 · 403 · 404'],
        ['Headers', 'Authorization, Content-Type, Cache-Control']])
K('fullstack', 'frontend-integration', 'keypoints', 'Frontend Integration',
  'Talk to APIs without the jank.',
  items=[('fetch / axios', 'Promise-based HTTP.'),
         ('Loading states', 'Never leave users guessing.'),
         ('Error handling', 'Show actionable messages.'),
         ('Caching', 'SWR / React Query patterns.')])
K('fullstack', 'backend-services', 'tiers', 'Backend Service Tiers',
  'Separation of concerns, layer by layer.',
  tiers=[('API', ['Routes', 'Validation']), ('Services', ['Business logic']),
         ('Data', ['Repositories', 'Database'])])
K('fullstack', 'databases', 'schema', 'App Database Schema',
  'Users own posts; posts have comments.',
  tables=[('users', [('id', 'PK'), ('email', ''), ('password_hash', '')]),
          ('posts', [('id', 'PK'), ('user_id', 'FK'), ('title', ''), ('body', '')]),
          ('comments', [('id', 'PK'), ('post_id', 'FK'), ('user_id', 'FK'), ('text', '')])],
  note='Foreign keys keep relationships consistent.')
K('fullstack', 'auth-sessions', 'flow', 'JWT Auth Flow',
  'Stateless auth for APIs and SPAs.', steps=AUTH_JWT)
K('fullstack', 'cicd-hosting', 'flow', 'CI/CD to Hosting',
  'Ship on every green main.', steps=CI_FLOW)

# --- python-web ---
K('python-web', 'framework-setup', 'commands', 'Python Web Setup Commands',
  'Scaffold a Django / Flask / FastAPI project.',
  cmds=[('python -m venv .venv && source .venv/bin/activate', 'Isolated environment'),
        ('pip install fastapi uvicorn sqlalchemy', 'Core web stack'),
        ('django-admin startproject shop', 'New Django project'),
        ('flask --app app run --debug', 'Dev server with reload'),
        ('uvicorn app:app --reload', 'ASGI dev server')])
K('python-web', 'routing-views', 'flow', 'Request Lifecycle (Python Web)',
  'URL to response in five steps.', steps=REST_LIFECYCLE)
K('python-web', 'models-orm', 'keypoints', 'Models & ORM',
  'Python classes, database tables.',
  items=[('Models', 'Class = table, attribute = column.'),
         ('Migrations', 'Schema changes as code.'),
         ('QuerySets', 'Lazy, chainable queries.'),
         ('Relationships', 'FK, M2M declarations.')])
K('python-web', 'templates-forms', 'keypoints', 'Templates & Forms',
  'Render HTML safely.',
  items=[('Jinja2 / Django templates', 'Autoescaped by default.'),
         ('CSRF tokens', 'Protect every POST form.'),
         ('Validation', 'Server-side always; client-side for UX.'),
         ('File uploads', 'Size + type limits.')])
K('python-web', 'auth-security', 'flow', 'Web Auth & Security',
  'Sessions or tokens — both need care.', steps=AUTH_JWT)
K('python-web', 'deploy-scale', 'flow', 'Deploy & Scale',
  'From laptop to production.',
  steps=[('WSGI/ASGI', 'Gunicorn / Uvicorn serve app'), ('Reverse proxy', 'Nginx in front'),
         ('Workers', 'Scale processes, not threads'), ('Static files', 'CDN / object storage'),
         ('Monitor', 'Logs + APM from day one')])

# --- react-frontend ---
K('react-frontend', 'components-jsx', 'keypoints', 'Components & JSX',
  'UI as composable functions.',
  items=[('Components', 'Functions returning UI.'),
         ('Props', 'One-way data in.'),
         ('JSX', 'HTML-like syntax, compiled.'),
         ('Composition', 'Children over inheritance.')])
K('react-frontend', 'state-effects', 'flow', 'Render → Effect Lifecycle',
  'How state drives the UI.',
  steps=[('Render', 'JSX from state/props'), ('Commit', 'DOM updated'),
         ('Effects', 'useEffect runs after paint'), ('Cleanup', 'Unsubscribe on change'),
         ('Re-render', 'State change restarts')])
K('react-frontend', 'routing-data', 'keypoints', 'Routing & Data',
  'Navigate and fetch like a pro.',
  items=[('React Router', 'Declarative routes.'),
         ('Loaders', 'Fetch before render.'),
         ('Params', 'Dynamic URL segments.'),
         ('Code splitting', 'Lazy-load routes.')])
K('react-frontend', 'performance', 'keypoints', 'React Performance',
  'Render less, memoize more.',
  items=[('memo', 'Skip unchanged renders.'),
         ('useMemo / useCallback', 'Cache values + fns.'),
         ('Virtualize', 'Long lists render windows.'),
         ('Bundle', 'Analyze + split chunks.')])
K('react-frontend', 'testing', 'keypoints', 'Testing React',
  'Test behavior, not implementation.',
  items=[('Vitest / Jest', 'Unit test runners.'),
         ('Testing Library', 'Query like a user.'),
         ('Mock server', 'MSW for API fakes.'),
         ('E2E', 'Playwright for flows.')])
K('react-frontend', 'build-deploy', 'flow', 'Build & Deploy Frontend',
  'From source to CDN edge.',
  steps=[('Build', 'Vite / webpack bundle'), ('Optimize', 'Minify, tree-shake'),
         ('Preview', 'Staging deploy'), ('CDN', 'Edge-cached static'),
         ('Monitor', 'RUM + error tracking')])

# --- creative-code ---
K('creative-code', 'canvas-drawing', 'keypoints', 'Canvas Drawing Basics',
  'Immediate-mode 2D graphics.',
  items=[('getContext("2d")', 'The drawing API handle.'),
         ('Paths', 'beginPath, moveTo, lineTo, stroke.'),
         ('Transforms', 'translate, rotate, scale.'),
         ('Pixels', 'getImageData for effects.')])
K('creative-code', 'animation', 'flow', 'Animation Loop',
  'The requestAnimationFrame heartbeat.',
  steps=[('Setup', 'Size canvas, init state'), ('Update', 'Advance positions/time'),
         ('Draw', 'Clear + render frame'), ('Loop', 'requestAnimationFrame(tick)')])
K('creative-code', 'generative-systems', 'keypoints', 'Generative Systems',
  'Rules + randomness = endless variation.',
  items=[('Seeded random', 'Reproducible outputs.'),
         ('Noise', 'Perlin for organic flow.'),
         ('Agents', 'Particles with behaviors.'),
         ('Parameters', 'Expose knobs, explore.')])
K('creative-code', 'interaction', 'keypoints', 'Interaction Design',
  'Make it respond beautifully.',
  items=[('Pointer events', 'Mouse + touch unified.'),
         ('Hit testing', 'What did the user touch?'),
         ('Easing', 'Motion with feeling.'),
         ('State', 'Idle / hover / active modes.')])
K('creative-code', 'math-for-art', 'keypoints', 'Math for Creative Code',
  'A little math goes a long way.',
  items=[('Trig', 'sin/cos for oscillation.'),
         ('Lerp', 'Smooth interpolation.'),
         ('Vectors', 'Position + velocity.'),
         ('Color spaces', 'HSL for pleasing palettes.')])
K('creative-code', 'showcase', 'timeline', 'Showcase Milestones',
  'Ship a portfolio piece in stages.',
  events=[('Sketch', 'Prototype the idea'), ('System', 'Build the engine'),
          ('Polish', 'Refine motion + color'), ('Publish', 'Share + document')])

# --- git-devops ---
K('git-devops', 'git-core', 'commands', 'Git Core Commands',
  'The ten commands behind 95% of Git work.', cmds=GIT_CMDS)
K('git-devops', 'branching-merging', 'git_branch', 'Branching & Merging',
  'Isolate work on branches; integrate with merges.',
  main='main', feature='feature/login')
K('git-devops', 'remotes-collab', 'keypoints', 'Remotes & Collaboration',
  'Git is distributed — remotes are the meeting point.',
  items=[('origin', 'Your default remote.'),
         ('upstream', 'The source you forked.'),
         ('fetch vs pull', 'Download vs download+merge.'),
         ('PRs', 'Review before merging.')])
K('git-devops', 'ci-concepts', 'flow', 'CI Concepts Pipeline',
  'Every commit gets built and tested.', steps=CI_FLOW)
K('git-devops', 'jenkins-basics', 'flow', 'Jenkins Pipeline Stages',
  'Jenkinsfile declares the pipeline as code.', steps=JENKINS_FLOW)
K('git-devops', 'release-flow', 'git_branch', 'Release Flow: GitFlow vs Trunk',
  'Long-lived release branches vs short-lived trunk commits.',
  main='main', feature='release/2.4')

# --- blockchain-dev ---
K('blockchain-dev', 'blockchain-basics', 'flow', 'How Blocks Chain Together',
  'Each block commits to the one before it.', steps=BLOCK_FLOW)
K('blockchain-dev', 'bitcoin', 'keypoints', 'Bitcoin Essentials',
  'Digital scarcity enforced by proof of work.',
  items=[('21M cap', 'Fixed supply schedule.'),
         ('~10 min blocks', 'Difficulty retargets.'),
         ('Halving ~4 years', 'Issuance cuts in half.'),
         ('SHA-256 PoW', 'Miners compete on hashes.'),
         ('UTXO model', 'Unspent outputs = balance.')])
K('blockchain-dev', 'xrpl', 'keypoints', 'XRP Ledger Essentials',
  'Fast settlement without mining.',
  items=[('UNL consensus', 'Trusted validator lists agree.'),
         ('3–5 s settlement', 'Near-instant finality.'),
         ('XRP', 'Native asset, tiny fees.'),
         ('No mining', 'Energy-light consensus.')])
K('blockchain-dev', 'solidity-evm', 'flow', 'Solidity → EVM Execution',
  'Write, compile, deploy, call.', steps=EVM_FLOW)
K('blockchain-dev', 'chain-security', 'keypoints', 'Smart Contract Security',
  'Code is law — audit like it.',
  items=[('Reentrancy', 'Guard external calls.'),
         ('Access control', 'Ownable / roles on sensitive fns.'),
         ('Oracles', 'Trust-minimized price feeds.'),
         ('Key management', 'Multisig for admin keys.'),
         ('Audits', 'Independent review before mainnet.')])
K('blockchain-dev', 'hyperledger', 'tiers', 'Hyperledger Fabric',
  'Permissioned blockchain for enterprises.',
  tiers=[('Network', ['Peers', 'Orderers']), ('Privacy', ['Channels', 'Private data collections']),
         ('Logic', ['Chaincode', 'Endorsement policies'])])

# ---------------------------------------------------------------------------
# Curated diagrams: infrastructure, DevOps, Linux, misc
# ---------------------------------------------------------------------------

# --- cka ---
K('cka', 'cluster-arch', 'tiers', 'Kubernetes Cluster Architecture',
  'Control plane decides; nodes execute.', tiers=K8S_ARCH)
K('cka', 'workloads-scheduling', 'keypoints', 'Workloads & Scheduling',
  'Declare desired state; controllers converge.',
  items=K8S_SCHED + [('Deployments', 'Rolling updates, replicas.'),
                     ('DaemonSets / Jobs', 'Per-node / run-to-complete.')])
K('cka', 'services-networking', 'table', 'Kubernetes Service Types',
  'How pods get stable endpoints.', **K8S_SVC_T)
K('cka', 'storage', 'keypoints', 'Kubernetes Storage',
  'Persistent data survives pod churn.',
  items=[('PV / PVC', 'Admin provisions, dev claims.'),
         ('StorageClass', 'Dynamic provisioning.'),
         ('Access modes', 'RWO, ROX, RWX.'),
         ('StatefulSets', 'Stable identity + storage.')])
K('cka', 'troubleshooting', 'flow', 'Pod Troubleshooting Flow',
  'Describe, logs, events — in that order.',
  steps=[('kubectl get pods', 'Find the failing pod'), ('kubectl describe', 'Events + state'),
         ('kubectl logs', 'Container output'), ('Exec / debug', 'Ephemeral debug container'),
         ('Fix + rollout', 'Patch manifest, redeploy')])
K('cka', 'security', 'keypoints', 'Cluster Security Hardening',
  'Secure the control plane and the workloads.', items=K8S_SEC)

# --- ckad ---
K('ckad', 'app-design', 'keypoints', 'Cloud-Native App Design',
  'Design for failure and scale from day one.',
  items=PROBES + [('12-factor', 'Config in env, stateless processes.'),
                  ('Graceful shutdown', 'Handle SIGTERM cleanly.')])
K('ckad', 'deployment', 'flow', 'Rolling Deployment',
  'Zero-downtime updates, batch by batch.', steps=ROLLING_FLOW)
K('ckad', 'observability', 'keypoints', 'Observability for Apps',
  'Instrument before you need it.', items=RED_USE)
K('ckad', 'services-networking', 'table', 'Kubernetes Service Types',
  'Expose pods the right way.', **K8S_SVC_T)
K('ckad', 'state-config', 'keypoints', 'Configuration & State',
  'Separate config from code.',
  items=[('ConfigMaps', 'Non-secret configuration.'),
         ('Secrets', 'Sensitive data, base64.'),
         ('Volumes', 'Mount config + data.'),
         ('Env vars', '12-factor config path.')])
K('ckad', 'security', 'keypoints', 'Application Security on K8s',
  'Secure defaults in every manifest.', items=K8S_SEC[:4])

# --- k8s-associate ---
K('k8s-associate', 'k8s-basics', 'tiers', 'Kubernetes Building Blocks',
  'The smallest units, composed upward.', tiers=K8S_ARCH)
K('k8s-associate', 'cloudnative-arch', 'keypoints', 'Cloud-Native Architecture',
  'Principles behind the ecosystem.',
  items=[('Microservices', 'Small, independently deployable.'),
         ('Containers', 'Portable runtime packaging.'),
         ('Declarative APIs', 'Describe desired state.'),
         ('CNCF', 'Graduated + incubating projects.')])
K('k8s-associate', 'security-concepts', 'keypoints', 'Kubernetes Security Concepts',
  'The 4 Cs: code, container, cluster, cloud.', items=K8S_SEC[:4])
K('k8s-associate', 'observability', 'keypoints', 'Observability Basics',
  'See inside distributed systems.', items=RED_USE)
K('k8s-associate', 'gitops-basics', 'flow', 'GitOps Basics',
  'Git as the single source of truth.', steps=GITOPS_FLOW)
K('k8s-associate', 'servicemesh-intro', 'topology', 'Service Mesh Intro',
  'Sidecars handle traffic policy and mTLS.', center='Service mesh',
  spokes=['Sidecar proxy', 'Control plane', 'mTLS between services', 'Traffic splitting', 'Retries / timeouts', 'Telemetry'])

# --- openshift ---
K('openshift', 'platform-concepts', 'tiers', 'OpenShift Platform',
  'Kubernetes plus enterprise opinion.',
  tiers=[('Control plane', ['API server', 'etcd', 'Operators']),
         ('Compute', ['MachineSets', 'Nodes']), ('Workloads', ['Projects', 'Deployments', 'Routes'])])
K('openshift', 'projects-rbac', 'keypoints', 'Projects & RBAC',
  'Projects are namespaces with guardrails.',
  items=[('Projects', 'K8s namespaces + quotas.'),
         ('Roles', 'admin / edit / view defaults.'),
         ('Bindings', 'Grant roles to users/groups.'),
         ('oc adm policy', 'Manage from CLI.')])
K('openshift', 'builds-imagestreams', 'flow', 'Builds & ImageStreams',
  'Source to runnable image, in-cluster.',
  steps=[('BuildConfig', 'Defines the build'), ('Source', 'Git repo input'),
         ('Build', 'S2I / Dockerfile strategy'), ('ImageStream', 'Versioned image ref'),
         ('Deploy', 'Trigger on new image')])
K('openshift', 'routes-networking', 'flow', 'Route → Service → Pod',
  'External traffic finds your app.', steps=ROUTE_FLOW)
K('openshift', 'operators', 'keypoints', 'Operators',
  'Encode operational knowledge as code.',
  items=[('OLM', 'Operator Lifecycle Manager.'),
         ('CRDs', 'Custom resources = APIs.'),
         ('Reconcile loop', 'Controller drives to desired.'),
         ('OperatorHub', 'Curated operator catalog.')])
K('openshift', 'pipelines', 'flow', 'OpenShift Pipelines (Tekton)',
  'K8s-native CI as custom resources.',
  steps=[('Pipeline', 'DAG of tasks'), ('Task', 'Steps in containers'),
         ('PipelineRun', 'One execution'), ('Workspace', 'Shared volumes'),
         ('Trigger', 'EventListener starts runs')])

# --- docker ---
K('docker', 'images-dockerfiles', 'flow', 'Dockerfile → Image Layers',
  'Each instruction adds a cached layer.', steps=DOCKERFILE_FLOW)
K('docker', 'registries', 'keypoints', 'Container Registries',
  'Store and share images securely.',
  items=[('Docker Hub', 'Public default registry.'),
         ('ECR / ACR / GAR', 'Cloud-managed registries.'),
         ('Tags', 'Version your images.'),
         ('Scanning', 'CVE scan on push.')])
K('docker', 'compose', 'keypoints', 'Docker Compose',
  'Multi-container apps in one YAML.',
  items=[('services', 'Each container defined.'),
         ('networks', 'Isolated app networks.'),
         ('volumes', 'Persistent data mounts.'),
         ('docker compose up', 'One command to run all.')])
K('docker', 'networking', 'table', 'Docker Network Drivers',
  'Isolation level per driver.', headers=['Driver', 'Scope'],
  rows=[['bridge', 'Single-host, default'], ['host', 'Shares host network'],
        ['overlay', 'Multi-host (swarm)'], ['none', 'Fully isolated']])
K('docker', 'volumes', 'keypoints', 'Docker Volumes',
  'Data that outlives containers.',
  items=[('Named volumes', 'Managed by Docker.'),
         ('Bind mounts', 'Host path mapped in.'),
         ('tmpfs', 'Memory-only, ephemeral.'),
         ('Backups', 'Volume contents need backups too.')])
K('docker', 'security-bp', 'keypoints', 'Container Security Best Practices',
  'Small, signed, scanned, non-root.',
  items=[('Minimal base', 'distroless / alpine.'),
         ('Non-root USER', 'Drop privileges.'),
         ('No secrets in layers', 'Use mounts / secrets.'),
         ('Scan images', 'Block CVEs in CI.')])

# --- terraform ---
K('terraform', 'iac-concepts', 'keypoints', 'Infrastructure as Code Concepts',
  'Version your infrastructure like software.',
  items=[('Declarative', 'Describe desired state.'),
         ('Idempotent', 'Same result every run.'),
         ('Drift', 'Manual changes detected.'),
         ('Immutable', 'Replace, do not mutate.')])
K('terraform', 'hcl-resources', 'keypoints', 'HCL & Resources',
  'The building blocks of configuration.',
  items=[('resource', 'Managed infrastructure object.'),
         ('data', 'Read existing infra.'),
         ('variable', 'Parameterize configs.'),
         ('output', 'Expose values.'),
         ('locals', 'Computed constants.')])
K('terraform', 'state-management', 'keypoints', 'Terraform State',
  'The map between config and reality.',
  items=[('terraform.tfstate', 'JSON mapping, sensitive.'),
         ('Remote backend', 'S3 + DynamoDB locking.'),
         ('Locking', 'Prevent concurrent writes.'),
         ('Import', 'Adopt existing resources.')])
K('terraform', 'modules', 'keypoints', 'Terraform Modules',
  'Reusable, versioned infrastructure packages.',
  items=[('Root module', 'Your working directory.'),
         ('Child modules', 'source = "./vpc".'),
         ('Registry', 'Public + private modules.'),
         ('Version pins', 'Reproducible applies.')])
K('terraform', 'workflows-cloud', 'flow', 'Terraform Workflow',
  'Init once, plan always, apply deliberately.', steps=TERRAFORM_FLOW)
K('terraform', 'gitops', 'keypoints', 'GitOps with Terraform',
  'PRs become infrastructure changes.',
  items=[('Plan on PR', ' Atlantis / CI comments diff.'),
         ('Apply on merge', 'Automation, not laptops.'),
         ('Drift detection', 'Scheduled plan checks.'),
         ('Policy as code', 'OPA / Sentinel gates.')])

# --- vault-consul ---
K('vault-consul', 'secrets-engines', 'keypoints', 'Vault Secrets Engines',
  'Where secrets live and how they are made.', items=VAULT_ENGINES)
K('vault-consul', 'auth-methods', 'flow', 'Vault Authentication Flow',
  'Prove identity, get a scoped token.', steps=VAULT_AUTH)
K('vault-consul', 'policies', 'keypoints', 'Vault Policies',
  'HCL paths grant capabilities.',
  items=[('path "secret/*"', 'Scope to a mount.'),
         ('capabilities', 'create, read, update, delete, list.'),
         ('Deny by default', 'No policy = no access.'),
         ('Tokens carry policies', 'Identity → policies → token.')])
K('vault-consul', 'dynamic-secrets', 'flow', 'Dynamic Secrets Lifecycle',
  'Credentials minted on demand, revoked on TTL.',
  steps=[('Request', 'App asks for DB creds'), ('Mint', 'Vault creates role user'),
         ('Lease', 'TTL attached to secret'), ('Renew / revoke', 'Lifecycle managed'),
         ('Audit', 'Every access logged')])
K('vault-consul', 'consul-service-mesh', 'topology', 'Consul Service Mesh',
  'Discovery, config, and mTLS mesh.', center='Consul cluster', spokes=CONSUL_TOPO_SPOKE)
K('vault-consul', 'operations', 'keypoints', 'Vault Operations',
  'Run it like production.',
  items=[('Seal / unseal', 'Shamir shares protect the key.'),
         ('HA', 'Raft integrated storage.'),
         ('Backup', 'Raft snapshots regularly.'),
         ('Audit devices', 'Log every request.')])

# --- sre-platform ---
K('sre-platform', 'slis-slos', 'keypoints', 'SLIs, SLOs & Error Budgets',
  'Reliability as a measurable target.', items=SLI_SLO)
K('sre-platform', 'incident-response', 'flow', 'Incident Response (SRE)',
  'Detect to postmortem without blame.', steps=INCIDENT_FLOW)
K('sre-platform', 'observability', 'keypoints', 'Observability Pillars',
  'Ask new questions without shipping code.', items=RED_USE)
K('sre-platform', 'capacity-performance', 'keypoints', 'Capacity & Performance',
  'Provision for peaks, not averages.',
  items=[('Load testing', 'Know the breaking point.'),
         ('Autoscaling', 'React to demand signals.'),
         ('Quotas', 'Protect shared resources.'),
         ('Profiling', 'Find the hot path.')])
K('sre-platform', 'platform-design', 'tiers', 'Platform Engineering',
  'Golden paths for product teams.',
  tiers=[('Foundation', ['Kubernetes', 'Network', 'IAM']),
         ('Platform', ['CI/CD', 'Observability', 'Backstage/IDP']),
         ('Product', ['Services teams ship'])])
K('sre-platform', 'toil-automation', 'keypoints', 'Toil vs Automation',
  'Automate toil; keep engineering creative.',
  items=[('Toil defined', 'Manual, repetitive, no judgment.'),
         ('50% cap', 'SREs limit ops toil.'),
         ('Automate', 'Runbooks → code.'),
         ('Measure', 'Track toil hours.')])

# --- rhcsa ---
K('rhcsa', 'core-tools', 'commands', 'RHCSA Core Tool Commands',
  'The commands behind the exam objectives.', cmds=LINUX_CMDS)
K('rhcsa', 'users-groups', 'commands', 'Users, Groups & Permissions',
  'Identity and access on Linux.', cmds=USER_CMDS)
K('rhcsa', 'storage', 'flow', 'LVM Storage Stack',
  'Disk to mount in five layers.', steps=LVM_FLOW)
K('rhcsa', 'services-boot', 'commands', 'systemd Service Management',
  'Control services and inspect boots.', cmds=SYSTEMD_CMDS)
K('rhcsa', 'networking', 'commands', 'Linux Networking Commands',
  'Addresses, routes, and sockets.', cmds=IP_CMDS)
K('rhcsa', 'containers-security', 'commands', 'Podman Containers',
  'Daemonless containers on RHEL.', cmds=PODMAN_CMDS)

# --- rhce ---
K('rhce', 'inventory-config', 'keypoints', 'Ansible Inventory & Config',
  'Describe your fleet as data.',
  items=[('Inventory', 'INI/YAML host lists.'),
         ('Groups', 'webservers, dbservers…'),
         ('ansible.cfg', 'Defaults: inventory, forks.'),
         ('Variables', 'Group/host vars layer.')])
K('rhce', 'playbooks', 'flow', 'Ansible Playbook Anatomy',
  'Plays contain tasks; tasks call modules.', steps=PLAYBOOK_FLOW)
K('rhce', 'variables-facts', 'keypoints', 'Variables & Facts',
  'Data-driven automation.',
  items=[('vars', 'Play-level variables.'),
         ('Facts', 'ansible_facts discovered.'),
         ('Precedence', '21 levels — know the order.'),
         ('Jinja2', '{{ var }} templating.')])
K('rhce', 'roles', 'keypoints', 'Ansible Roles',
  'Reusable playbook packages.',
  items=[('Structure', 'tasks/, handlers/, templates/.'),
         ('Galaxy', 'Community role sharing.'),
         ('Defaults vs vars', 'Override hierarchy.'),
         ('Dependencies', 'meta/main.yml.')])
K('rhce', 'vault-security', 'keypoints', 'Ansible Vault & Security',
  'Encrypt secrets, run least-privilege.',
  items=[('ansible-vault', 'Encrypt vars files.'),
         ('become', 'Privilege escalation.'),
         ('No plaintext', 'Never commit secrets.'),
         ('Vault IDs', 'Multiple passwords.')])
K('rhce', 'troubleshooting', 'flow', 'Ansible Troubleshooting',
  'Debug failed plays methodically.',
  steps=[('Syntax', 'ansible-playbook --syntax-check'), ('Verbose', '-vvv reveals module args'),
         ('Check mode', '--check dry run'), ('Isolate', 'Run one host, one task'),
         ('Fix + rerun', 'Idempotent retries')])

# --- linux-essentials ---
K('linux-essentials', 'community-careers', 'keypoints', 'Linux Community & Careers',
  'Open source is a people system too.',
  items=[('Distributions', 'Ubuntu, Fedora, Debian, RHEL…'),
         ('Upstream', 'Contribute fixes back.'),
         ('Certifications', 'LPI, RHCSA, LFCA paths.'),
         ('Roles', 'Admin, SRE, DevOps, embedded.')])
K('linux-essentials', 'finding-your-way', 'layers', 'Filesystem Hierarchy',
  'Where everything lives on Linux.', layers=FHS)
K('linux-essentials', 'cli-power', 'commands', 'CLI Power Commands',
  'Pipes turn small tools into pipelines.', cmds=BASH_CMDS)
K('linux-essentials', 'files-ownership', 'keypoints', 'Files, Ownership & Permissions',
  'rwx for user, group, and other.', items=PERMS)
K('linux-essentials', 'processes-text', 'commands', 'Processes & Text Processing',
  'Manage jobs and slice text streams.',
  cmds=[('ps aux / top / htop', 'See processes live'),
        ('kill -15 PID / kill -9', 'Graceful vs force kill'),
        ('jobs / fg / bg / &', 'Job control'),
        ('grep -R "err" /var/log', 'Search log trees'),
        ('sed / awk', 'Edit + report on streams')])
K('linux-essentials', 'networking-basics', 'commands', 'Linux Networking Basics',
  'Connectivity checks in order.', cmds=IP_CMDS)

# --- systems-cs ---
K('systems-cs', 'computer-organization', 'layers', 'Memory Hierarchy',
  'Faster is smaller and closer to the CPU.', layers=[
      ('Registers', 'CPU-internal, instant'), ('L1 / L2 / L3 cache', 'KBs–MBs, nanoseconds'),
      ('RAM', 'GBs, ~100ns'), ('SSD', 'Fast persistent'), ('HDD / tape', 'Slow, cheap, huge')])
K('systems-cs', 'operating-systems', 'keypoints', 'Operating Systems Core',
  'What the kernel does for you.',
  items=[('Processes', 'Isolated address spaces.'),
         ('Threads', 'Shared-memory execution.'),
         ('Scheduling', 'Round-robin, priorities.'),
         ('Virtual memory', 'Paging + page tables.'),
         ('File systems', 'ext4, XFS, NTFS.')])
K('systems-cs', 'networking-basics', 'layers', 'TCP/IP Model',
  'The four-layer view of networking.', layers=TCPIP_LAYERS)
K('systems-cs', 'software-engineering', 'flow', 'Software Development Lifecycle',
  'Plan to maintain — not just to ship.', steps=SDLC)
K('systems-cs', 'databases', 'keypoints', 'Database Essentials',
  'ACID, indexes, and normalization.',
  items=ACID + [('Indexes', 'B-trees speed lookups.')])
K('systems-cs', 'theory-essentials', 'keypoints', 'Theory Essentials',
  'The ideas behind the practice.',
  items=[('P vs NP', 'Verify fast vs solve fast.'),
         ('Turing machines', 'The model of computation.'),
         ('Automata', 'Regex = regular languages.'),
         ('Halting problem', 'Some questions are undecidable.')])

# --- math-tech ---
K('math-tech', 'algebra', 'keypoints', 'Algebra Essentials',
  'Manipulate expressions with confidence.',
  items=[('Equations', 'Isolate the variable.'),
         ('Functions', 'Domain, range, composition.'),
         ('Exponents / logs', 'Inverse operations.'),
         ('Quadratics', 'Factor or formula.')])
K('math-tech', 'discrete', 'keypoints', 'Discrete Mathematics',
  'Math of the countable — CS native.',
  items=[('Sets', 'Union, intersection, complement.'),
         ('Logic', 'AND/OR/NOT, truth tables.'),
         ('Graphs', 'Vertices + edges model networks.'),
         ('Combinatorics', 'Count without listing.')])
K('math-tech', 'statistics', 'keypoints', 'Statistics Essentials',
  'Summarize data without lying.',
  items=[('Mean / median / mode', 'Center measures.'),
         ('Variance / std dev', 'Spread measures.'),
         ('Normal distribution', '68-95-99.7 rule.'),
         ('p-values', 'Strength of evidence.'),
         ('Correlation ≠ causation', 'Always.')])
K('math-tech', 'linear-algebra', 'keypoints', 'Linear Algebra Essentials',
  'The language of ML and graphics.',
  items=[('Vectors', 'Magnitude + direction.'),
         ('Matrices', 'Linear transformations.'),
         ('Dot product', 'Similarity measure.'),
         ('Eigenvalues', 'Characteristic directions.')])
K('math-tech', 'calculus', 'keypoints', 'Calculus Essentials',
  'Rates of change and accumulation.',
  items=[('Derivatives', 'Instantaneous rate of change.'),
         ('Gradients', 'Direction of steepest ascent.'),
         ('Chain rule', 'Backpropagation\'s engine.'),
         ('Integrals', 'Area under the curve.')])
K('math-tech', 'quant', 'keypoints', 'Quantitative Methods',
  'Numbers that drive decisions.',
  items=[('Expected value', 'Probability-weighted outcome.'),
         ('Distributions', 'Model uncertainty.'),
         ('Hypothesis testing', 'Reject the null?'),
         ('Regression', 'Fit relationships in data.')])

# --- hermetica ---
K('hermetica', 'hermetic-principles', 'layers', 'The Seven Hermetic Principles',
  'From the Kybalion — the classic esoteric framework.', layers=HERMETIC_7)
K('hermetica', 'enochian-system', 'keypoints', 'The Enochian System',
  'Dee and Kelley\'s angelic language framework.',
  items=[('Calls / Keys', '19 invocations.'),
         ('Tablets', 'Elemental + spirit tablets.'),
         ('Aethyrs', '30 layered realms.'),
         ('Alphabet', '21-letter script.')])
K('hermetica', 'cybernetics-hyperstition', 'cycle', 'Cybernetic Feedback Loop',
  'Steering through circular causality.', steps=FEEDBACK_LOOP)
K('hermetica', 'symbol-systems', 'keypoints', 'Symbol Systems',
  'How meaning gets encoded and transmitted.',
  items=[('Alphabets', 'Letters as number + concept.'),
         ('Tarot arcana', '22 major archetypes.'),
         ('Astrology', 'Planets, signs, houses.'),
         ('Sigils', 'Compressed intention.')])
K('hermetica', 'critical-reading', 'keypoints', 'Critical Reading of Esoterica',
  'Read strange texts with clear eyes.',
  items=[('Context', 'Who wrote it, when, why?'),
         ('Symbol vs literal', 'Do not flatten metaphor.'),
         ('Sources', 'Trace claims upstream.'),
         ('Practice', 'Test ideas, keep notes.')])
K('hermetica', 'esoteric-programming', 'keypoints', 'Esoteric Programming',
  'Code as ritual and play.',
  items=[('Esolangs', 'Brainfuck, Befunge, Malbolge.'),
         ('Constraints', 'Creativity through limits.'),
         ('Quines', 'Programs that print themselves.'),
         ('Code poetry', 'Aesthetics in syntax.')])

# --- career-launch ---
K('career-launch', 'career-strategy', 'quadrants', 'Career SWOT',
  'Know yourself before you market yourself.', quads=SWOT)
K('career-launch', 'interview-skills', 'flow', 'STAR Interview Method',
  'Answer behaviorals with structure.', steps=STAR)
K('career-launch', 'self-knowledge', 'keypoints', 'Self-Knowledge Toolkit',
  'Clarity about strengths and direction.',
  items=[('Values', 'What work must honor.'),
         ('Strengths', 'Evidence-backed claims.'),
         ('Gaps', 'Named + being closed.'),
         ('Story', 'Your narrative arc.')])
K('career-launch', 'fde-work', 'keypoints', 'FDE Work Principles',
  'Full-stack delivery, end to end.',
  items=[('Own outcomes', 'Not just tickets.'),
         ('Ship iteratively', 'Small, frequent releases.'),
         ('Measure', 'Instrument from day one.'),
         ('Communicate', 'Write clearly, often.')])
K('career-launch', 'entrepreneurship', 'flow', 'Founder Loop',
  'Build, measure, learn — on repeat.',
  steps=[('Problem', 'Pain worth paying for'), ('MVP', 'Smallest testable thing'),
         ('Launch', 'Get it in hands'), ('Learn', 'Metrics + interviews'),
         ('Iterate', 'Pivot or persevere')])
K('career-launch', 'professional-practice', 'keypoints', 'Professional Practice',
  'Goals and habits that compound.', items=SMART)

# --- ides-tooling ---
K('ides-tooling', 'vscode', 'keypoints', 'VS Code Essentials',
  'The editor most developers live in.',
  items=[('Command palette', 'Ctrl/Cmd+Shift+P does all.'),
         ('Extensions', 'Language packs + linters.'),
         ('Integrated terminal', 'No context switching.'),
         ('Settings sync', 'Dotfiles for your editor.')])
K('ides-tooling', 'intellij-pycharm', 'keypoints', 'IntelliJ / PyCharm',
  'JetBrains power for JVM + Python.',
  items=[('Refactoring', 'Rename/move safely.'),
         ('Inspections', 'Deep static analysis.'),
         ('Run configs', 'One-click debug.'),
         ('Database tools', 'Query inside the IDE.')])
K('ides-tooling', 'visual-studio', 'keypoints', 'Visual Studio',
  'The .NET heavyweight.',
  items=[('Solution explorer', 'Multi-project management.'),
         ('NuGet', 'Package management.'),
         ('Profiler', 'Find hot paths.'),
         ('Live Share', 'Collaborative coding.')])
K('ides-tooling', 'debugging-workflows', 'flow', 'Debugging Workflow',
  'Reproduce, isolate, fix, verify.',
  steps=[('Reproduce', 'Reliable trigger first'), ('Breakpoint', 'Pause at suspicion'),
         ('Inspect', 'Variables + call stack'), ('Step', 'Walk the execution'),
         ('Fix + test', 'Change, then regression-test')])
K('ides-tooling', 'extensions-settings', 'keypoints', 'Extensions & Settings',
  'Tune the tool to the task.',
  items=[('Linters', 'Catch bugs as you type.'),
         ('Formatters', 'Consistent style automatically.'),
         ('Keymaps', 'Vim bindings if you like.'),
         ('Profiles', 'Per-language setups.')])
K('ides-tooling', 'terminal-tasks', 'commands', 'Terminal & Task Commands',
  'Build and run without leaving the IDE.',
  cmds=[('npm run dev / build', 'JS dev + production build'),
        ('dotnet run / test', '.NET run + test'),
        ('python -m pytest', 'Python test suite'),
        ('docker compose up', 'Local dependencies'),
        ('git status / diff', 'Review before commit')])

# ---------------------------------------------------------------------------
# plan(): exact KB -> slug-scoped heuristics -> global heuristics -> fallback
# ---------------------------------------------------------------------------

# Slug-scoped heuristics for domain_ids whose meaning depends on the bootcamp.
SLUG_HEUR = {
    'aws-saa': [('network', 'topology', dict(title='VPC Networking', caption='',
                center='VPC 10.0.0.0/16', spokes=VPC_SPOKE))],
    'az-104': [('network', 'topology', dict(title='Azure Virtual Network', caption='',
               center='VNet 10.0.0.0/16', spokes=VNET_SPOKE))],
    'az-700': [('monitor', 'keypoints', dict(title='Network Monitoring', caption='',
               items=[('Network Watcher', 'Topology, capture, flow logs.'),
                      ('Connection Monitor', 'Endpoint probes.'),
                      ('Traffic Analytics', 'Flow-log insights.')]))],
    'rhcsa': [('network', 'commands', dict(title='Linux Networking Commands', caption='',
              cmds=IP_CMDS))],
    'linux-essentials': [('network', 'commands', dict(title='Linux Networking Basics', caption='',
                         cmds=IP_CMDS))],
    'docker': [('network', 'table', dict(title='Docker Network Drivers', caption='',
               headers=['Driver', 'Scope'],
               rows=[['bridge', 'Single-host'], ['host', 'Host network'],
                     ['overlay', 'Multi-host'], ['none', 'Isolated']]))],
    'oracle-oci': [('network', 'topology', dict(title='OCI Virtual Cloud Network', caption='',
                   center='VCN 10.0.0.0/16', spokes=OCI_VCN_SPOKE))],
    'dp-203': [('stream', 'flow', dict(title='Stream Processing (Event Hubs)', caption='',
                steps=[('Event Hubs', 'Ingest millions of events'),
                       ('Stream Analytics', 'Real-time SQL jobs'),
                       ('Synapse / Power BI', 'Serve + visualize')]))],
    'data-engineering': [('stream', 'flow', dict(title='Streaming with Kafka', caption='',
                         steps=KAFKA_FLOW))],
}

# Global keyword heuristics: (keywords in domain_id or title) -> builder spec.
GLOBAL_HEUR = [
    (['osi'], 'layers', dict(title='OSI Model (7 Layers)', caption='', layers=OSI_LAYERS)),
    (['tcp/ip', 'tcpip'], 'layers', dict(title='TCP/IP Model', caption='', layers=TCPIP_LAYERS)),
    (['subnet', 'cidr'], 'table', dict(title='CIDR & Subnet Sizes', caption='', **CIDR_T)),
    (['private ip', 'rfc1918', 'ip address'], 'table', dict(title='Private IPv4 Ranges (RFC 1918)', caption='', **PRIVATE_IP)),
    (['dns'], 'flow', dict(title='DNS Resolution', caption='', steps=DNS_FLOW)),
    (['dhcp', 'dora'], 'flow', dict(title='DHCP DORA Process', caption='', steps=DHCP_FLOW)),
    (['3-way', 'handshake', 'three-way'], 'flow', dict(title='TCP Three-Way Handshake', caption='', steps=TCP_HANDSHAKE)),
    (['tls'], 'flow', dict(title='TLS 1.2 Handshake', caption='', steps=TLS12_FLOW)),
    (['tcp vs', 'tcp/udp', 'udp vs'], 'table', dict(title='TCP vs UDP', caption='', **TCP_UDP)),
    (['ipv4 vs', 'ipv6'], 'table', dict(title='IPv4 vs IPv6', caption='', **IPV4_V6)),
    (['port'], 'table', dict(title='Common Ports & Protocols', caption='',
                             headers=['Service', 'Port', 'Use'], rows=PORT_ROWS)),
    (['symmetric', 'asymmetric'], 'table', dict(title='Symmetric vs Asymmetric Crypto', caption='', **SYM_ASYM)),
    (['jwt'], 'crypto', dict(title='JWT Structure', caption='', **JWT_CRYPTO)),
    (['oauth'], 'flow', dict(title='OAuth 2.0 Authorization Code Flow', caption='', steps=OAUTH_FLOW)),
    (['raid'], 'table', dict(title='RAID Levels Compared', caption='', **RAID)),
    (['http status', 'status code'], 'table', dict(title='HTTP Status Code Classes', caption='', **HTTP_STATUS)),
    (['rest verb', 'http verb', 'http method'], 'table', dict(title='REST Verbs', caption='', **REST_VERBS)),
    (['kill chain'], 'flow', dict(title='Cyber Kill Chain', caption='', steps=KILL_CHAIN)),
    (['incident response', 'incident-response'], 'flow', dict(title='Incident Response (NIST 800-61)', caption='', steps=IR_PHASES)),
    (['cia triad'], 'keypoints', dict(title='CIA Triad', caption='', items=CIA)),
    (['aaa'], 'keypoints', dict(title='AAA Framework', caption='', items=AAA)),
    (['bell-lapadula', 'bell lapadula'], 'keypoints', dict(title='Security Models', caption='', items=BLA)),
    (['sdlc'], 'flow', dict(title='Software Development Lifecycle', caption='', steps=SDLC)),
    (['scrum'], 'cycle', dict(title='Scrum Cycle', caption='', steps=SCRUM)),
    (['smart goal'], 'keypoints', dict(title='SMART Goals', caption='', items=SMART)),
    (['swot'], 'quadrants', dict(title='SWOT Analysis', caption='', quads=SWOT)),
    (['star method', 'star interview'], 'flow', dict(title='STAR Interview Method', caption='', steps=STAR)),
    (['3-2-1'], 'keypoints', dict(title='3-2-1 Backup Rule', caption='', items=BACKUP_321)),
    (['rto', 'rpo'], 'keypoints', dict(title='RTO / RPO / MTTR / MTBF', caption='', items=RTO_RPO)),
    (['disaster recovery', ' dr '], 'table', dict(title='DR Strategies', caption='', **DR_T)),
    (['melt', 'red/', 'red method'], 'keypoints', dict(title='Observability: RED / USE / MELT', caption='', items=RED_USE)),
    (['sli', 'slo'], 'keypoints', dict(title='SLIs, SLOs & Error Budgets', caption='', items=SLI_SLO)),
    (['xss'], 'keypoints', dict(title='XSS Types', caption='', items=XSS_TYPES)),
    (['sql injection', 'sqli'], 'keypoints', dict(title='SQL Injection Classes', caption='', items=SQLI_TYPES)),
    (['owasp'], 'keypoints', dict(title='OWASP Top 10 (2021) — Selected', caption='Six of ten shown; full list in the lesson.', items=OWASP21)),
    (['mitre', 'att&ck'], 'keypoints', dict(title='MITRE ATT&CK Tactics (Selected)', caption='Six of fourteen tactics shown.', items=MITRE_T)),
    (['cvss'], 'keypoints', dict(title='CVSS Severity Bands', caption='', items=CVSS_BANDS)),
    (['vulnerability management', 'vuln-mgmt', 'vuln mgmt'], 'flow', dict(title='Vulnerability Management Lifecycle', caption='', steps=VULN_MGMT)),
    (['ptes', 'pentest method'], 'flow', dict(title='Pen Test Methodology (PTES)', caption='', steps=PTES)),
    (['siem'], 'flow', dict(title='SIEM Data Pipeline', caption='', steps=SIEM_FLOW)),
    (['order of volatility', 'volatility'], 'flow', dict(title='Order of Volatility', caption='', steps=VOLATILITY)),
    (['threat intel'], 'keypoints', dict(title='Threat Intelligence Levels', caption='', items=THREAT_INTEL)),
    (['playbook'], 'flow', dict(title='Ansible Playbook Anatomy', caption='', steps=PLAYBOOK_FLOW)),
    (['dockerfile'], 'flow', dict(title='Dockerfile → Image Layers', caption='', steps=DOCKERFILE_FLOW)),
    (['lvm'], 'flow', dict(title='LVM Storage Stack', caption='', steps=LVM_FLOW)),
    (['boot'], 'flow', dict(title='Linux Boot Sequence', caption='', steps=BOOT_FLOW)),
    (['permission'], 'keypoints', dict(title='Linux Permissions', caption='', items=PERMS)),
    (['filesystem hierarchy', 'fhs'], 'layers', dict(title='Filesystem Hierarchy', caption='', layers=FHS)),
    (['middleware'], 'flow', dict(title='Middleware Pipeline', caption='', steps=MIDDLEWARE_FLOW)),
    (['rag'], 'tiers', dict(title='RAG Architecture', caption='', tiers=RAG_TIERS)),
    (['transformer'], 'flow', dict(title='Transformer Forward Pass', caption='', steps=TRANSFORMER_FLOW)),
    (['fine-tun', 'finetun'], 'flow', dict(title='Fine-Tuning Pipeline', caption='', steps=FINETUNE_FLOW)),
    (['agent loop', 'agent-loop'], 'cycle', dict(title='Agent Loop', caption='', steps=AGENT_LOOP)),
    (['prompt'], 'keypoints', dict(title='Prompt Engineering', caption='',
                                   items=[('Zero-shot', 'Ask directly.'), ('Few-shot', 'Show examples.'),
                                          ('Chain-of-thought', 'Think step by step.'), ('System prompts', 'Set role + rules.')])),
    (['consensus'], 'table', dict(title='Consensus Mechanisms', caption='', **CONSENSUS_T)),
    (['block anatomy', 'block structure'], 'flow', dict(title='How Blocks Chain Together', caption='', steps=BLOCK_FLOW)),
    (['replica set'], 'topology', dict(title='Replica Set', caption='', center='Replica set',
                                       spokes=['Primary (writes)', 'Secondary', 'Secondary', 'Arbiter', 'Oplog'])),
    (['conditional access'], 'flow', dict(title='Conditional Access Policy', caption='', steps=COND_ACCESS)),
    (['pim'], 'keypoints', dict(title='Privileged Identity Management', caption='', items=PIM)),
    (['rbac'], 'keypoints', dict(title='RBAC Essentials', caption='', items=RBAC)),
    (['mfa'], 'flow', dict(title='Multi-Factor Authentication Flow', caption='', steps=MFA_FLOW)),
    (['kql'], 'commands', dict(title='KQL Essentials', caption='', cmds=KQL_CMDS,
                               note='KQL is read-only: it queries, never changes data.')),
    (['sentinel'], 'flow', dict(title='Microsoft Sentinel Workflow', caption='', steps=SENTINEL_FLOW)),
    (['probe'], 'keypoints', dict(title='Kubernetes Probes', caption='', items=PROBES)),
    (['rolling'], 'flow', dict(title='Rolling Deployment', caption='', steps=ROLLING_FLOW)),
    (['gitops'], 'flow', dict(title='GitOps Basics', caption='', steps=GITOPS_FLOW)),
    (['etl'], 'flow', dict(title='ETL Pipeline', caption='', steps=ETL_FLOW)),
    (['star schema'], 'schema', dict(title='Star Schema', caption='', tables=STAR_SCHEMA,
                                     note='Denormalized dims make analytics fast.')),
    (['normalization', 'normal form'], 'keypoints', dict(title='Normalization Forms', caption='',
         items=[('1NF', 'Atomic values, no repeating groups.'), ('2NF', 'No partial dependency on key.'),
                ('3NF', 'No transitive dependencies.')])),
    (['acid'], 'keypoints', dict(title='ACID Properties', caption='', items=ACID)),
    (['isolation level'], 'table', dict(title='Transaction Isolation Levels', caption='', **ISOLATION_T)),
    (['cap theorem'], 'keypoints', dict(title='CAP Theorem', caption='',
         items=[('Consistency', 'Every read gets the latest write.'),
                ('Availability', 'Every request gets a response.'),
                ('Partition tolerance', 'Works despite network splits.'),
                ('Pick two', 'Distributed systems trade one off.')])),
    (['crud'], 'commands', dict(title='CRUD Operations', caption='', cmds=MONGOSH_CMDS[:4])),
    (['aggregation pipeline', '$match'], 'flow', dict(title='Aggregation Pipeline', caption='', steps=MONGO_AGG)),
    (['index'], 'keypoints', dict(title='Database Indexes', caption='',
         items=[('B-tree', 'The default index structure.'),
                ('Index the filters', 'WHERE / JOIN / ORDER BY columns.'),
                ('Write cost', 'Each index slows writes.'),
                ('Explain plans', 'Verify the index is used.')])),
    (['join'], 'table', dict(title='JOIN Types Compared', caption='', **JOINS_T)),
    (['window function'], 'commands', dict(title='Window Functions', caption='',
         cmds=[('ROW_NUMBER() OVER (ORDER BY x)', 'Rank rows 1..n'),
               ('RANK() / DENSE_RANK()', 'Rank with/without gaps'),
               ('LAG(col) OVER (…)', 'Previous row value'),
               ('SUM(x) OVER (PARTITION BY y)', 'Group running totals')])),
    (['big-o', 'complexity'], 'table', dict(title='Big-O Complexities', caption='',
         headers=['Complexity', 'Name', 'Example'],
         rows=[['O(1)', 'Constant', 'Hash lookup'], ['O(log n)', 'Logarithmic', 'Binary search'],
               ['O(n)', 'Linear', 'Single scan'], ['O(n log n)', 'Linearithmic', 'Merge sort'],
               ['O(n²)', 'Quadratic', 'Nested loops'], ['O(2ⁿ)', 'Exponential', 'Naive recursion']])),
    (['sorting'], 'table', dict(title='Sorting Algorithms', caption='',
         headers=['Algorithm', 'Average', 'Stable?'],
         rows=[['Quicksort', 'O(n log n)', 'No'], ['Merge sort', 'O(n log n)', 'Yes'],
               ['Heap sort', 'O(n log n)', 'No'], ['Insertion sort', 'O(n²)', 'Yes']])),
    (['branch'], 'git_branch', dict(title='Branching & Merging', caption='', main='main', feature='feature/work')),
    (['ci/', 'continuous integration', 'ci concepts'], 'flow', dict(title='CI Pipeline', caption='', steps=CI_FLOW)),
    (['shared responsibility'], 'table', dict(title='Shared Responsibility Model', caption='', **SHARED_RESP)),
    (['defense in depth', 'defence in depth'], 'layers', dict(title='Defense in Depth', caption='', layers=DEFENSE_DEPTH)),
    (['zero trust'], 'keypoints', dict(title='Zero Trust Principles', caption='', items=ZERO_TRUST)),
    (['nist csf', 'csf 2.0'], 'keypoints', dict(title='NIST CSF 2.0 Functions', caption='', items=NIST_CSF)),
]


def _matches(haystack, keywords):
    # Left word-boundary match: 'rag' must not fire inside 'storage-design',
    # 'port' must not fire inside 'support'. Right side may extend
    # ('branch' matches 'branching').
    h = haystack.lower()
    for k in keywords:
        if re.search(r'(?<![a-z0-9])' + re.escape(k.lower()), h):
            return True
    return False


def plan(slug, domain_id, title, concepts):
    """Return (kind, kwargs) for the lesson's diagram."""
    if (slug, domain_id) in KB:
        return KB[(slug, domain_id)]
    hay = domain_id + ' ' + (title or '')
    for kw, kind, kwd in SLUG_HEUR.get(slug, []):
        if kw in domain_id.lower() or kw in (title or '').lower():
            return kind, dict(kwd)
    for keywords, kind, kwd in GLOBAL_HEUR:
        if _matches(hay, keywords):
            return kind, dict(kwd)
    # Fallback: concept-derived key-points diagram (accurate by construction).
    items = []
    for c in concepts[:6]:
        items.append(headline(c))
    if not items:
        items = [('Overview', short_title(title))]
    t = short_title(title)
    return 'keypoints', dict(title=t, caption='', items=items)


# ---------------------------------------------------------------------------
# main generation + validation
# ---------------------------------------------------------------------------
def alt_text(title, kind, kwargs):
    bits = [title]
    for key in ('items', 'steps', 'layers', 'rows', 'spokes', 'tiers', 'events', 'quads', 'tables', 'cmds'):
        v = kwargs.get(key)
        if v:
            if key in ('items', 'steps', 'layers'):
                bits.append('Shows: ' + ', '.join(str(x[0]) for x in v[:6]))
            elif key == 'rows':
                bits.append('Table with %d rows' % len(v))
            elif key in ('spokes', 'events'):
                bits.append('Covers: ' + ', '.join(str(x if isinstance(x, str) else x[0]) for x in v[:6]))
            elif key == 'tiers':
                bits.append('Tiers: ' + ', '.join(str(t[0]) for t in v))
            elif key == 'quads':
                bits.append('Quadrants: ' + ', '.join(str(t[0]) for t in v))
            elif key == 'tables':
                bits.append('Tables: ' + ', '.join(str(t[0]) for t in v))
            elif key == 'cmds':
                bits.append('Commands: ' + ', '.join(str(c[0]) for c in v[:5]))
            break
    return '. '.join(bits) + '.'


def main():
    content_dir = os.path.join(BASE, 'content')
    files = sorted(glob.glob(os.path.join(content_dir, '*.json')))
    report = []
    total_lessons = 0
    total_media = 0
    for f in files:
        d = json.load(open(f))
        slug = d['slug']
        lessons = d['lessons']
        total_lessons += len(lessons)
        diag_dir = os.path.join(content_dir, slug, 'assets', 'diagrams')
        frag_dir = os.path.join(content_dir, slug, 'fragments')
        os.makedirs(diag_dir, exist_ok=True)
        os.makedirs(frag_dir, exist_ok=True)
        media = []
        fallback_count = 0
        for lesson in lessons:
            did = lesson['domain_id']
            title = lesson.get('title', did)
            concepts = lesson.get('concepts', [])
            kind, kwargs = plan(slug, did, title, concepts)
            if (slug, did) not in KB:
                fallback_count += 1
            if not kwargs.get('title'):
                kwargs['title'] = short_title(title)
            svg = G.build(kind, **kwargs)
            ET.fromstring(svg)  # raises if malformed
            assert len(svg.encode('utf-8')) < 60000, 'SVG too large'
            fname = '%s-%s.svg' % (safe(slug), safe(did))
            with open(os.path.join(diag_dir, fname), 'w') as fh:
                fh.write(svg)
            media.append({
                'id': '%s-%s-diag' % (safe(slug), safe(did)),
                'kind': 'diagram',
                'title': kwargs['title'],
                'svg': 'assets/diagrams/%s' % fname,
                'lesson_ref': 'c-%s' % did,
                'caption': kwargs.get('caption') or 'Diagram: %s' % kwargs['title'],
                'alt': alt_text(kwargs['title'], kind, kwargs),
            })
        with open(os.path.join(frag_dir, 'media.json'), 'w') as fh:
            json.dump({'media': media}, fh, indent=1, ensure_ascii=False)
        total_media += len(media)
        report.append((slug, len(lessons), len(media), fallback_count))
    print('bootcamps=%d lessons=%d media=%d' % (len(files), total_lessons, total_media))
    print()
    print('%-22s %8s %8s %10s' % ('slug', 'lessons', 'diagrams', 'fallbacks'))
    for slug, nl, nm, fb in report:
        flag = '  <-- CHECK' if nm < nl else ''
        print('%-22s %8d %8d %10d%s' % (slug, nl, nm, fb, flag))
    bad = [r for r in report if r[2] < r[1]]
    if bad:
        print('\nUNDER-COVERED:', bad)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
