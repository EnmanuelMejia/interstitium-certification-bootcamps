# -*- coding: utf-8 -*-
"""Batch 3: append 4 consoleSims each to 6 bootcamps (consoleSims key missing -> insert after 'simulations')."""
import json, collections, sys

BASE = '/home/hatch/workspace/cert-bootcamps/site/bootcamps'

def T(tid, instruction, action, params, hint):
    return {"id": tid, "instruction": instruction,
            "validate": {"action": action, "params": params}, "hint": hint}

def S(sid, title, console, domain, diff, brief, tasks, debrief):
    return {"id": sid, "title": title, "console": console, "domain_id": domain,
            "difficulty": diff, "brief": brief, "tasks": tasks, "debrief": debrief}

DATA = {}

# ---------------- cisco-ccna (switch-cli heavy) ----------------
DATA["cisco-ccna"] = [
S("ccna-csim-1","Carve out the guest VLAN","switch-cli","cisco-ccna",1,
"A new guest Wi-Fi access point uplinks on interface Gi1/0/12. Guest traffic must live on its own broadcast domain, VLAN 50, named GUEST — then save the running config so a power cycle doesn't undo your work.",
[T("t1","Create VLAN 50 and name it GUEST.","create-vlan",{"id":"50","name":"GUEST"},
   "In the terminal type: vlan 50 name GUEST — then click Run."),
 T("t2","Put interface Gi1/0/12 into access mode on VLAN 50.","assign-port",{"port":"Gi1/0/12","vlan":"50"},
   "Type: interface Gi1/0/12 access vlan 50 — the switch refuses if VLAN 50 doesn't exist yet."),
 T("t3","Save the configuration.","save-config",{},
   "Type: write memory — then check the Ports tab shows the config as saved.")],
"One VLAN, one access port, one save. Segmenting broadcast domains with VLANs is the most-tested switching skill on the CCNA — and the unsaved running-config is the most common lab mistake."),

S("ccna-csim-2","Trunk the uplink to the core","switch-cli","cisco-ccna",1,
"Gi1/0/48 is the fiber uplink to the core switch. Right now it carries only VLAN 1, so every other VLAN goes dark across the link. Make it a trunk that carries all VLANs, then save.",
[T("t1","Set interface Gi1/0/48 to trunk mode.","set-trunk",{"port":"Gi1/0/48"},
   "Type: interface Gi1/0/48 trunk — then Run."),
 T("t2","Save the configuration.","save-config",{},
   "Type: write memory.")],
"Trunks carry tagged frames for many VLANs over one link; access ports carry one. A single untagged uplink is the classic 'VLAN works locally but not across the switch' failure."),

S("ccna-csim-3","Voice and data on floor 2","switch-cli","cisco-ccna",2,
"Floor 2 gets IP phones with PCs daisy-chained behind them. Voice traffic belongs on VLAN 20 (named VOICE) so QoS can prioritize it. Gi1/0/20 and Gi1/0/21 are the two wall jacks — put both ports on the voice VLAN and save.",
[T("t1","Create VLAN 20 named VOICE.","create-vlan",{"id":"20","name":"VOICE"},
   "Type: vlan 20 name VOICE"),
 T("t2","Assign interface Gi1/0/20 to VLAN 20.","assign-port",{"port":"Gi1/0/20","vlan":"20"},
   "Type: interface Gi1/0/20 access vlan 20"),
 T("t3","Assign interface Gi1/0/21 to VLAN 20.","assign-port",{"port":"Gi1/0/21","vlan":"20"},
   "Type: interface Gi1/0/21 access vlan 20"),
 T("t4","Save the configuration.","save-config",{},
   "Type: write memory")],
"Separating voice and data into VLANs is how real networks prioritize phone traffic and keep broadcast chatter away from call quality. Same motion, twice — muscle memory is the point."),

S("ccna-csim-4","Overnight port move for Finance","switch-cli","cisco-ccna",3,
"Finance moves to a new office overnight. Their PCs plug into Gi1/0/30 and must land on VLAN 40 (named FINANCE). The old uplink on Gi1/0/47 now feeds the new IDF closet, so it becomes a trunk. Do all three, then save — the morning crew arrives at 7.",
[T("t1","Create VLAN 40 named FINANCE.","create-vlan",{"id":"40","name":"FINANCE"},
   "Type: vlan 40 name FINANCE"),
 T("t2","Put interface Gi1/0/30 on VLAN 40.","assign-port",{"port":"Gi1/0/30","vlan":"40"},
   "Type: interface Gi1/0/30 access vlan 40"),
 T("t3","Make interface Gi1/0/47 a trunk.","set-trunk",{"port":"Gi1/0/47"},
   "Type: interface Gi1/0/47 trunk"),
 T("t4","Save the configuration.","save-config",{},
   "Type: write memory — no save, no change survives the next reboot.")],
"Real changes chain VLAN creation, port assignment, trunk setup, and a save into one change window. Miss the save and the 7 a.m. power blip erases everything — CCNA simlets punish exactly that."),
]

# ---------------- comptia-a-plus (hardware/OS troubleshooting) ----------------
DATA["comptia-a-plus"] = [
S("aplus-csim-1","Triage the morning ticket queue","ticketing","comptia-a-plus",1,
"Monday 8 a.m.: the queue has a jammed floor-3 printer blocking invoices. Open a P2 ticket for it, take ownership, and move it to in-progress.",
[T("t1","Create a P2 ticket titled exactly: Printer queue jam — floor 3","create-ticket",{"title":"Printer queue jam — floor 3","priority":"P2"},
   "Use the New ticket tab: TITLE=Printer queue jam — floor 3, PRIORITY=P2. Copy the title character for character — it becomes INC-9002."),
 T("t2","Assign ticket INC-9002 to yourself.","assign-ticket",{"id":"INC-9002","assignee":"you"},
   "Queue tab → Assign form: TICKET ID=INC-9002, ASSIGNEE=you"),
 T("t3","Move INC-9002 to in-progress.","update-status",{"id":"INC-9002","status":"in-progress"},
   "Update status form: TICKET ID=INC-9002, STATUS=in-progress")],
"Triage is a Core 2 staple: prioritize, own, and track. A ticket that never moves status is a ticket nobody is working."),

S("aplus-csim-2","Document and lock down the cleanup","linux-desktop","comptia-a-plus",1,
"The scareware on WKS-117 is gone. Write a cleanup log at /home/user/cleanup-log.txt, then lock it down so only the owner can read or write it.",
[T("t1","Create the file /home/user/cleanup-log.txt.","create-file",{"path":"/home/user/cleanup-log.txt"},
   "Files tab → Create file form: PATH=/home/user/cleanup-log.txt"),
 T("t2","Set its permissions to 600 (owner read/write only).","chmod",{"path":"/home/user/cleanup-log.txt","mode":"600"},
   "chmod form: PATH=/home/user/cleanup-log.txt, MODE=600")],
"Least privilege applies to files too: 600 means owner-only. On A+, know your octal — 7 is rwx, 6 is rw-, 4 is r--, 0 is nothing."),

S("aplus-csim-3","Log the new workstation in the asset console","generic-web","comptia-a-plus",2,
"Imaging is done on WS-F3-042. Record the asset in the web console: asset tag, team contact email, and the site timezone — then submit.",
[T("t1","Set the asset-tag field to WS-F3-042.","set-field",{"id":"site_name","value":"WS-F3-042"},
   "Settings tab → 'Set site name' form: FIELD=site_name, VALUE=WS-F3-042"),
 T("t2","Set the contact email to endpoint-team@contoso.local.","set-field",{"id":"admin_email","value":"endpoint-team@contoso.local"},
   "'Set admin email' form: FIELD=admin_email, VALUE=endpoint-team@contoso.local"),
 T("t3","Set the timezone to America/New_York.","set-field",{"id":"timezone","value":"America/New_York"},
   "'Set timezone' form: FIELD=timezone, VALUE=America/New_York"),
 T("t4","Submit the form.","submit-form",{},
   "Click 'Submit settings'.")],
"Asset documentation is unglamorous and exam-relevant: every deployed device gets an inventory record with owner, location, and timezone for log correlation."),

S("aplus-csim-4","Close out the malware cleanup ticket","ticketing","comptia-a-plus",2,
"WKS-117 scanned clean after the scareware removal. Open the closeout ticket, add the verification note, and resolve it.",
[T("t1","Create a P3 ticket titled exactly: WKS-117 disinfected — verification","create-ticket",{"title":"WKS-117 disinfected — verification","priority":"P3"},
   "New ticket tab — copy the title exactly, it becomes INC-9002."),
 T("t2","Add the note: Full scan clean; user briefed on phishing links.","add-note",{"id":"INC-9002","text":"Full scan clean; user briefed on phishing links."},
   "Queue tab → Add note form: TICKET ID=INC-9002, NOTE=Full scan clean; user briefed on phishing links."),
 T("t3","Resolve INC-9002.","resolve-ticket",{"id":"INC-9002"},
   "Click the Resolve button on the INC-9002 row.")],
"Closing the loop means documentation: what was done, what was verified, and who was briefed. A+ incident response ends with lessons learned, not just a clean scan."),
]

# ---------------- comptia-network-plus (networking) ----------------
DATA["comptia-network-plus"] = [
S("netplus-csim-1","Open DNS for the new resolver","firewall","comptia-network-plus",1,
"The new internal DNS resolver must answer queries from the 192.168.1.0/24 LAN. DNS needs both UDP and TCP port 53. Add both ACCEPT rules on the INPUT chain.",
[T("t1","Allow UDP port 53 from 192.168.1.0/24.","add-rule",{"chain":"INPUT","protocol":"udp","port":"53","source":"192.168.1.0/24","action":"ACCEPT"},
   "Rules tab → Add rule: CHAIN=INPUT, PROTOCOL=udp, PORT=53, SOURCE=192.168.1.0/24, ACTION=ACCEPT"),
 T("t2","Allow TCP port 53 from 192.168.1.0/24.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"53","source":"192.168.1.0/24","action":"ACCEPT"},
   "Same form with PROTOCOL=tcp — zone transfers and large DNS replies need TCP.")],
"DNS is the classic 'works by IP, fails by name' culprit, and it needs both UDP and TCP 53. Network+ loves asking which ports a service needs — memorize the pairs."),

S("netplus-csim-2","Kill legacy Telnet at the border","firewall","comptia-network-plus",2,
"Security policy bans Telnet (port 23) — it sends credentials in cleartext. Block it in both directions on this host: no outbound Telnet, and no inbound Telnet from anywhere.",
[T("t1","DROP outbound TCP port 23.","add-rule",{"chain":"OUTPUT","protocol":"tcp","port":"23","source":"0.0.0.0/0","action":"DROP"},
   "CHAIN=OUTPUT, PROTOCOL=tcp, PORT=23, SOURCE=0.0.0.0/0, ACTION=DROP"),
 T("t2","DROP inbound TCP port 23 from anywhere.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"23","source":"0.0.0.0/0","action":"DROP"},
   "CHAIN=INPUT with the same values — block the listener side too.")],
"Telnet vs SSH is the textbook insecure-vs-secure protocol swap. Blocking both chains closes the loop: nobody can Telnet out, and nobody can Telnet in."),

S("netplus-csim-3","Stand up the management VLAN","switch-cli","comptia-network-plus",2,
"Switch management interfaces are moving to VLAN 99 (named MGMT) for isolation, and the uplink on Gi0/24 must trunk all VLANs to the core. Build the VLAN, trunk the uplink, save.",
[T("t1","Create VLAN 99 named MGMT.","create-vlan",{"id":"99","name":"MGMT"},
   "Type: vlan 99 name MGMT"),
 T("t2","Make Gi0/24 a trunk.","set-trunk",{"port":"Gi0/24"},
   "Type: interface Gi0/24 trunk"),
 T("t3","Save the configuration.","save-config",{},
   "Type: write memory")],
"A dedicated management VLAN keeps admin traffic off user broadcast domains — a Network+ design best practice — and the trunk carries it (plus everything else) upstream."),

S("netplus-csim-4","File the maintenance change ticket","ticketing","comptia-network-plus",1,
"Tonight's core-switch firmware window (22:00–23:00) is approved. File a P2 change ticket, attach the approval note, and assign it to netops.",
[T("t1","Create a P2 ticket titled exactly: Change: core switch firmware 22:00-23:00","create-ticket",{"title":"Change: core switch firmware 22:00-23:00","priority":"P2"},
   "New ticket tab — copy the title exactly, it becomes INC-9002."),
 T("t2","Add the note: Change board approved; rollback plan on file.","add-note",{"id":"INC-9002","text":"Change board approved; rollback plan on file."},
   "Add note form with the exact text."),
 T("t3","Assign INC-9002 to netops.","assign-ticket",{"id":"INC-9002","assignee":"netops"},
   "Assign form: TICKET ID=INC-9002, ASSIGNEE=netops")],
"Network+ change management: every change gets documented, approved, and assigned before it happens — with a rollback plan, always."),
]

# ---------------- comptia-security-plus (security / firewall) ----------------
DATA["comptia-security-plus"] = [
S("secplus-csim-1","Harden the new web server","firewall","comptia-security-plus",1,
"The new web server goes live at noon. Policy is deny-by-default: open exactly one hole — HTTPS (TCP 443) from the corporate network 10.0.0.0/8 — then set the INPUT chain to DROP everything else.",
[T("t1","Add an ACCEPT rule: INPUT, TCP 443, source 10.0.0.0/8.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"443","source":"10.0.0.0/8","action":"ACCEPT"},
   "Rules tab → Add rule: CHAIN=INPUT, PROTOCOL=tcp, PORT=443, SOURCE=10.0.0.0/8, ACTION=ACCEPT"),
 T("t2","Set the INPUT chain default policy to DROP.","set-default-policy",{"chain":"INPUT","policy":"DROP"},
   "Default policies tab: CHAIN=INPUT, POLICY=DROP")],
"Order matters: the explicit allow must exist before the default deny, or you lock yourself out of the very service you're publishing. Least privilege, expressed in firewall rules."),

S("secplus-csim-2","Contain the crypto-miner","siem-dashboard","comptia-security-plus",2,
"The SIEM fired ALT-102: a malware hash match on a download — severity critical, host wkst-117. Work it like an analyst: acknowledge the alert, assign it to soc-tier1, then isolate the host.",
[T("t1","Acknowledge alert ALT-102.","acknowledge-alert",{"id":"ALT-102"},
   "Alerts tab → click Ack on the ALT-102 row."),
 T("t2","Assign ALT-102 to analyst soc-tier1.","assign-alert",{"id":"ALT-102","analyst":"soc-tier1"},
   "Assign alert form: ALERT ID=ALT-102, ANALYST=soc-tier1"),
 T("t3","Isolate host wkst-117.","isolate-host",{"host":"wkst-117"},
   "Click 'Isolate host' on the ALT-102 row.")],
"Acknowledge, assign, contain — the first three moves of incident-response triage. Isolation stops lateral movement while you investigate; it never deletes evidence."),

S("secplus-csim-3","Block the RDP brute-forcer","firewall","comptia-security-plus",2,
"Logs show 203.0.113.45 hammering RDP (TCP 3389). Drop that source on port 3389 — but keep RDP reachable for admins on the corporate network 10.0.0.0/8.",
[T("t1","DROP TCP 3389 from 203.0.113.45.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"3389","source":"203.0.113.45","action":"DROP"},
   "CHAIN=INPUT, PROTOCOL=tcp, PORT=3389, SOURCE=203.0.113.45, ACTION=DROP"),
 T("t2","ACCEPT TCP 3389 from 10.0.0.0/8.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"3389","source":"10.0.0.0/8","action":"ACCEPT"},
   "Same form with SOURCE=10.0.0.0/8, ACTION=ACCEPT — management stays reachable.")],
"Block the attacker, keep the admins: host-based firewall rules can be surgical. (And the long-term fix is never exposing RDP to the internet at all — VPN or jump host.)"),

S("secplus-csim-4","Write the failed-login detector","siem-dashboard","comptia-security-plus",3,
"After last night's VPN login storm, build a detection rule that fires when one source IP racks up more than 20 failed logins — then escalate the open impossible-travel alert ALT-101 to incident response.",
[T("t1","Create a detection rule named exactly: VPN failed-login burst — query: event:authfail | stats count by src_ip | where count > 20","create-rule",{"name":"VPN failed-login burst","query":"event:authfail | stats count by src_ip | where count > 20"},
   "Detection rules tab → Create rule: NAME=VPN failed-login burst, QUERY=event:authfail | stats count by src_ip | where count > 20"),
 T("t2","Escalate alert ALT-101.","escalate",{"id":"ALT-101"},
   "Alerts tab → click Escalate on the ALT-101 row.")],
"Detection engineering is proactive defense: you turned one incident into a rule that catches the next one. Escalation hands the active threat to the incident-response process with full context."),
]

# ---------------- isc2-cc (cybersecurity fundamentals) ----------------
DATA["isc2-cc"] = [
S("cc-csim-1","Triage the impossible-travel alert","siem-dashboard","isc2-cc",1,
"ALT-101: a user logged in from two countries an hour apart — classic impossible travel, severity high. As the on-call analyst, acknowledge it and assign it to j.chen for review.",
[T("t1","Acknowledge alert ALT-101.","acknowledge-alert",{"id":"ALT-101"},
   "Alerts tab → click Ack on the ALT-101 row."),
 T("t2","Assign ALT-101 to analyst j.chen.","assign-alert",{"id":"ALT-101","analyst":"j.chen"},
   "Assign alert form: ALERT ID=ALT-101, ANALYST=j.chen")],
"Impossible travel is a textbook account-compromise indicator. Acknowledging takes ownership; assigning routes it to a human — the first two steps of the incident-response lifecycle."),

S("cc-csim-2","Report the lost access badge","ticketing","isc2-cc",1,
"You lost your Building B access badge in the parking lot. Physical security is cybersecurity: file a P3 ticket, note that the badge was deactivated, and resolve it once the reissue is scheduled.",
[T("t1","Create a P3 ticket titled exactly: Lost access badge — Building B","create-ticket",{"title":"Lost access badge — Building B","priority":"P3"},
   "New ticket tab — copy the title exactly, it becomes INC-9002."),
 T("t2","Add the note: Badge deactivated in access system; reissue scheduled.","add-note",{"id":"INC-9002","text":"Badge deactivated in access system; reissue scheduled."},
   "Add note form with the exact text."),
 T("t3","Resolve INC-9002.","resolve-ticket",{"id":"INC-9002"},
   "Click the Resolve button on the INC-9002 row.")],
"Access control isn't just passwords — badges are physical credentials. Reporting a lost one fast and deactivating it is the same instinct as rotating a compromised password."),

S("cc-csim-3","Contain the exfiltrating backup server","siem-dashboard","isc2-cc",2,
"ALT-103: unusual outbound volume from srv-backup-02, severity medium. Backup servers shouldn't phone home to strangers. Acknowledge the alert, isolate the host to stop any exfiltration, then escalate.",
[T("t1","Acknowledge alert ALT-103.","acknowledge-alert",{"id":"ALT-103"},
   "Alerts tab → click Ack on the ALT-103 row."),
 T("t2","Isolate host srv-backup-02.","isolate-host",{"host":"srv-backup-02"},
   "Click 'Isolate host' on the ALT-103 row."),
 T("t3","Escalate alert ALT-103.","escalate",{"id":"ALT-103"},
   "Click Escalate on the ALT-103 row.")],
"Data exfiltration is one of the two things attackers want (the other is persistence). Isolating first contains the damage; the escalated alert carries the evidence trail to the IR team."),

S("cc-csim-4","Blocklist the SSH scanner","firewall","isc2-cc",2,
"A scanner at 203.0.113.77 is probing SSH (TCP 22) on this host. Drop SSH from that source — but keep the web management portal (TCP 443) reachable from the corporate network 10.0.0.0/8.",
[T("t1","DROP TCP 22 from 203.0.113.77.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"22","source":"203.0.113.77","action":"DROP"},
   "CHAIN=INPUT, PROTOCOL=tcp, PORT=22, SOURCE=203.0.113.77, ACTION=DROP"),
 T("t2","ACCEPT TCP 443 from 10.0.0.0/8.","add-rule",{"chain":"INPUT","protocol":"tcp","port":"443","source":"10.0.0.0/8","action":"ACCEPT"},
   "Same form with PORT=443, SOURCE=10.0.0.0/8, ACTION=ACCEPT — legitimate management stays up.")],
"Network-layer controls are the cheapest win in defense-in-depth: one rule stops the scanner, another keeps legitimate management working. Precision beats blanket blocking."),
]

# ---------------- m365-endpoint-admin (MD-102 endpoint management) ----------------
DATA["m365-endpoint-admin"] = [
S("md102-csim-1","Triage the stuck Autopilot device","ticketing","m365-endpoint-admin",1,
"A new laptop has been stuck at 'Setting up your device' for 40 minutes. Open a P2 ticket, assign it to endpoint-admin, and set it in-progress.",
[T("t1","Create a P2 ticket titled exactly: Autopilot device stuck at 'Setting up your device'","create-ticket",{"title":"Autopilot device stuck at 'Setting up your device'","priority":"P2"},
   "New ticket tab — copy the title exactly, quotes included. It becomes INC-9002."),
 T("t2","Assign INC-9002 to endpoint-admin.","assign-ticket",{"id":"INC-9002","assignee":"endpoint-admin"},
   "Assign form: TICKET ID=INC-9002, ASSIGNEE=endpoint-admin"),
 T("t3","Move INC-9002 to in-progress.","update-status",{"id":"INC-9002","status":"in-progress"},
   "Update status form: TICKET ID=INC-9002, STATUS=in-progress")],
"MD-102 reality: Autopilot enrollment failures are among the most common endpoint-admin tickets. Fast triage — accurate title, right owner, visible status — is half the fix."),

S("md102-csim-2","Log the manually enrolled device","generic-web","m365-endpoint-admin",1,
"LT-1042 wouldn't take Autopilot, so it was enrolled manually. Record it in the web console: asset tag, team contact email, and the device timezone — then submit.",
[T("t1","Set the asset-tag field to MD102-LT-1042.","set-field",{"id":"site_name","value":"MD102-LT-1042"},
   "Settings tab → 'Set site name' form: FIELD=site_name, VALUE=MD102-LT-1042"),
 T("t2","Set the contact email to endpoint-team@contoso.local.","set-field",{"id":"admin_email","value":"endpoint-team@contoso.local"},
   "'Set admin email' form: FIELD=admin_email, VALUE=endpoint-team@contoso.local"),
 T("t3","Set the timezone to America/Chicago.","set-field",{"id":"timezone","value":"America/Chicago"},
   "'Set timezone' form: FIELD=timezone, VALUE=America/Chicago"),
 T("t4","Submit the form.","submit-form",{},
   "Click 'Submit settings'.")],
"Every managed device needs an inventory record with a contact and a timezone — compliance reports and remote-wipe decisions both start from that record."),

S("md102-csim-3","Harden the golden image firewall","firewall","m365-endpoint-admin",2,
"The Windows golden image ships to 400 laptops. Block legacy SMB (TCP 445) from leaving the device — ransomware loves it — while explicitly allowing HTTPS (TCP 443) so Intune and updates keep working.",
[T("t1","DROP outbound TCP 445.","add-rule",{"chain":"OUTPUT","protocol":"tcp","port":"445","source":"0.0.0.0/0","action":"DROP"},
   "CHAIN=OUTPUT, PROTOCOL=tcp, PORT=445, SOURCE=0.0.0.0/0, ACTION=DROP"),
 T("t2","ACCEPT outbound TCP 443.","add-rule",{"chain":"OUTPUT","protocol":"tcp","port":"443","source":"0.0.0.0/0","action":"ACCEPT"},
   "Same form with PORT=443, ACTION=ACCEPT — updates and Intune traffic stay healthy.")],
"Blocking SMB outbound at the host level is a standard ransomware-containment control on managed endpoints — and it's exactly the kind of baseline you bake into an image, not bolt on later."),

S("md102-csim-4","Close out the update-ring ticket","ticketing","m365-endpoint-admin",2,
"The pilot ring finished the feature update with zero rollback events. Open the closeout ticket, add the verification note, and resolve it.",
[T("t1","Create a P3 ticket titled exactly: Feature update landed on pilot ring — verify fleet","create-ticket",{"title":"Feature update landed on pilot ring — verify fleet","priority":"P3"},
   "New ticket tab — copy the title exactly, it becomes INC-9002."),
 T("t2","Add the note: Pilot ring 100% updated; no rollback events.","add-note",{"id":"INC-9002","text":"Pilot ring 100% updated; no rollback events."},
   "Add note form with the exact text."),
 T("t3","Resolve INC-9002.","resolve-ticket",{"id":"INC-9002"},
   "Click the Resolve button on the INC-9002 row.")],
"Ring-based rollouts (pilot → broad) are the MD-102 update doctrine. The closeout note is the evidence: what deployed, what the result was, and whether anything rolled back."),
]

# ---------------- validation ----------------
VALID_CONSOLES = {
 "aws-vpc":["create-vpc","create-subnet","create-igw","attach-igw","create-route-table","add-route","associate-route-table","create-sg","add-sg-rule","launch-instance"],
 "aws-iam":["create-user","create-group","add-user-to-group","create-role","create-policy","attach-policy","enable-mfa"],
 "azure-portal":["create-rg","create-vnet","create-vm","create-nsg","add-nsg-rule","assign-rbac"],
 "k8s-dashboard":["create-namespace","deploy","expose-service","scale","create-configmap"],
 "firewall":["add-rule","delete-rule","set-default-policy"],
 "switch-cli":["create-vlan","assign-port","set-trunk","save-config"],
 "linux-desktop":["select","chmod","chown","create-file","create-dir","delete"],
 "sql-studio":["create-table","create-index","run-query"],
 "git-host":["create-branch","open-pr","approve-pr","request-changes","add-comment","merge-pr"],
 "cicd-pipeline":["trigger-build","retry-stage","approve-stage","set-variable"],
 "siem-dashboard":["acknowledge-alert","assign-alert","escalate","isolate-host","create-rule"],
 "ticketing":["create-ticket","assign-ticket","update-status","add-note","resolve-ticket"],
 "code-editor":["open-file","toggle-breakpoint","step-over","run-to-breakpoint","fix-line","inspect-variable"],
 "db-admin":["create-database","create-user","grant-priv","backup","set-parameter"],
 "generic-web":["set-field","submit-form"],
}

def main():
    all_ids = set()
    for slug, arr in DATA.items():
        assert len(arr) == 4, slug
        for sim in arr:
            assert sim["domain_id"] == slug, sim["id"]
            assert sim["id"] not in all_ids, "dup " + sim["id"]
            all_ids.add(sim["id"])
            assert sim["console"] in VALID_CONSOLES, sim["console"]
            assert sim["difficulty"] in (1,2,3)
            assert sim["brief"] and sim["debrief"] and sim["title"]
            assert len(sim["tasks"]) >= 2, sim["id"]
            for t in sim["tasks"]:
                assert t["hint"] and t["hint"].strip(), "missing hint " + sim["id"] + "/" + t["id"]
                assert t["instruction"] and t["validate"]["action"] and isinstance(t["validate"]["params"], dict)
                assert t["validate"]["action"] in VALID_CONSOLES[sim["console"]], \
                    "bad action %s for %s" % (t["validate"]["action"], sim["id"])
    print("pre-inject validation OK:", len(all_ids), "unique sim ids")

    for slug, arr in DATA.items():
        path = BASE + "/" + slug + "/content.json"
        raw = open(path, encoding="utf-8").read()
        trail = raw[len(raw.rstrip("\n")):]
        d = json.loads(raw, object_pairs_hook=collections.OrderedDict)
        assert "consoleSims" not in d, "already present in " + slug
        nd = collections.OrderedDict()
        for k, v in d.items():
            nd[k] = v
            if k == "simulations":
                nd["consoleSims"] = arr
        out = json.dumps(nd, indent=1, ensure_ascii=False) + trail
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        # re-validate from disk
        d2 = json.load(open(path, encoding="utf-8"))
        cs = d2["consoleSims"]
        assert isinstance(cs, list) and len(cs) == 4
        ids = [s["id"] for s in cs]
        assert len(set(ids)) == 4
        for s in cs:
            assert all(t.get("hint") for t in s["tasks"])
        # sanity: rest of doc untouched
        for k in d:
            if k != "consoleSims":
                assert d2[k] == d[k], "key changed: " + k
        print(slug, "consoleSims=4 OK")
    print("ALL DONE")

main()
