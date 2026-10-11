#!/usr/bin/env python3
"""Build 26 troubleshooting scenarios + 10 incident scenarios for tl-interview CBT."""
import json

PATH = "/home/hatch/workspace/cert-bootcamps/site/bootcamps/tl-interview/content.json"

with open(PATH) as f:
    data = json.load(f)

# ---------------------------------------------------------------- troubleshooting (26)
T = [
# --- Allowlisting (6) ---
{
 "id": "tl-troubleshoot-01",
 "title": "Legitimate App Blocked After Update",
 "domain_id": "customer-scenarios",
 "situation": "A customer's accounting team reports their invoicing application stopped launching this morning, right after the vendor pushed an automatic update overnight. The ThreatLocker agent shows a block event for the new executable. The previous version ran fine for months.",
 "prompt": "What is the most likely cause, and what should the engineer do first?",
 "choices": [
  "The update is malware; quarantine the machine immediately and wipe it",
  "The application's file hash changed with the update, so the old allowlist entry no longer matches. Verify the new file's signature and publisher, then approve the updated version in the Application Control policy",
  "Disable Allowlisting for the accounting group so updates never break again",
  "Tell the customer to roll back the update and disable automatic updates permanently"
 ],
 "answer": 1,
 "why": "ThreatLocker Allowlisting is deny-by-default and identifies files by hash. When a vendor updates an application, the executable hash changes and the old approval no longer matches, which produces exactly this symptom: worked yesterday, blocked today. The correct response is to verify the new file is legitimate (check the digital signature, publisher, and source) and then approve the new version. Disabling the control or rolling back updates weakens security posture and does not address the root cause.",
 "hint": "What identifies a file to an allowlisting engine? What changed overnight?",
 "objectives": ["Diagnose hash-change blocks after legitimate updates", "Apply the verify-then-approve workflow"],
 "mins": 10,
 "evidence": [
  ["Block event", "Denied: C:\\Program Files\\Invoicer\\invoicer.exe | Reason: File not on allowlist | SHA256: 9f2c...a41b (previous approved hash: 7d11...e903)"],
  ["File properties", "Digital signature: Valid, issued to Invoicer Inc. | Signed: 2026-10-09 23:14 UTC | Source: vendor auto-update channel"]
 ]
},
{
 "id": "tl-troubleshoot-02",
 "title": "New Software Deployment Blocked Org-Wide",
 "domain_id": "customer-scenarios",
 "situation": "An IT admin is rolling out a new approved PDF editor to 300 endpoints via their deployment tool. Installations are failing everywhere with ThreatLocker block events. The software is legitimate and the customer wants it deployed today.",
 "prompt": "How should the engineer enable this deployment without weakening the security posture?",
 "choices": [
  "Put all 300 machines in Disabled Mode until the rollout finishes",
  "Add the installer to the allowlist, or use Learning Mode / an installation policy scoped to the deployment window so the installer and its components are approved as they execute",
  "Tell the admin to install it manually on each machine with local admin rights",
  "Whitelist the entire deployment tool so it can run anything"
 ],
 "answer": 1,
 "why": "The clean approach is to approve the installer (and its child processes) through policy: add the installer hash or certificate to the allowlist, or run a time-scoped Learning Mode / installation policy during the deployment window so legitimate components are learned and approved. This keeps deny-by-default intact for everything else. Disabled Mode or blanket-whitelisting the deployment tool creates a gap where anything the tool touches would execute unchallenged.",
 "hint": "How do you approve something new without turning off the control for everything?",
 "objectives": ["Enable legitimate mass deployments under deny-by-default", "Use scoped learning/installation policies"],
 "mins": 10,
 "evidence": [
  ["Block events (sample)", "Denied: pdfeditor-setup.exe | 214 endpoints | Reason: File not on allowlist"],
  ["Deployment ticket", "Approved software: PDF Editor v4.2 (vendor MSI, signed) | Target: All workstations | Window: today 09:00-17:00"]
 ]
},
{
 "id": "tl-troubleshoot-03",
 "title": "PowerShell Script Blocked",
 "domain_id": "technical-questions",
 "situation": "A sysadmin's logon script that maps drives and sets printers is being blocked on every workstation. The script has not changed in a year. The customer recently tightened their ThreatLocker policies.",
 "prompt": "What is the correct way to allow this legitimate script while keeping script-based attacks blocked?",
 "choices": [
  "Approve the specific script by hash in the policy, or sign it and approve the certificate, so that exact script is allowed while unknown scripts remain denied",
  "Allow powershell.exe unrestricted so all scripts run",
  "Disable script blocking for the entire domain",
  "Convert the script to a batch file, which is not inspected"
 ],
 "answer": 0,
 "why": "The script itself is legitimate, so it should be explicitly approved: allowlisting the script by hash (or better, signing it and trusting the certificate) permits that exact script while every other unknown script stays denied. Allowing powershell.exe broadly or disabling the control would also permit malicious scripts, which defeats the purpose. Batch files are equally subject to policy, so converting the format changes nothing.",
 "hint": "Deny-by-default means unknown scripts are denied. How do you make a known-good script 'known'?",
 "objectives": ["Allow legitimate scripts under application control", "Distinguish script approval from interpreter approval"],
 "mins": 10,
 "evidence": [
  ["Block event", "Denied: C:\\Scripts\\logon.ps1 | Reason: Script not on allowlist | Parent: powershell.exe"],
  ["Policy change log", "2026-10-08: 'Script Control' tightened from Audit to Deny for Workstations group"]
 ]
},
{
 "id": "tl-troubleshoot-04",
 "title": "Driver Installation Blocked",
 "domain_id": "technical-questions",
 "situation": "A customer is installing a new printer fleet. The printer driver installer is blocked on every machine. The driver is signed by the printer manufacturer.",
 "prompt": "What should the engineer check and do?",
 "choices": [
  "Drivers cannot be allowlisted; the customer must use a different printer brand",
  "Verify the driver's signature and approve it through the appropriate kernel/driver control policy, since signed drivers from the legitimate vendor can be explicitly permitted",
  "Disable ThreatLocker on the print server permanently",
  "Install the driver in Safe Mode to bypass the agent"
 ],
 "answer": 1,
 "why": "Signed drivers from a legitimate vendor can be approved through policy. The engineer should verify the signature chains to the expected manufacturer and then permit the driver via the kernel-mode/driver approval path. ThreatLocker does inspect driver loads because malicious drivers are a persistence technique, so there is a deliberate approval workflow rather than an automatic pass. Bypassing via Safe Mode or disabling the agent circumvents the control instead of using it correctly.",
 "hint": "Why would a security product inspect driver loads at all? How do legitimate ones get approved?",
 "objectives": ["Handle driver approvals through proper policy channels", "Explain why driver loads are inspected"],
 "mins": 10,
 "evidence": [
  ["Block event", "Denied: prndrvr.sys | Reason: Driver not approved | Signer: PrinterCorp Inc. (valid)"],
  ["Ticket", "New printer fleet rollout, 45 devices, driver package v2.8 from vendor site"]
 ]
},
{
 "id": "tl-troubleshoot-05",
 "title": "App Works on Some Machines, Blocked on Others",
 "domain_id": "customer-scenarios",
 "situation": "A line-of-business application launches fine on 40 machines but is blocked on 15 others. Same installer, same version. The customer insists the policy is applied everywhere.",
 "prompt": "What is the most likely explanation?",
 "choices": [
  "The 15 machines have a corrupted agent and need to be reinstalled",
  "The machines are in different policy groups. The application is approved in one group's policy but not the other's, so group membership or policy scoping differs between the two sets",
  "The application is randomly choosing whether to run",
  "The 15 machines are infected and the blocks are correct"
 ],
 "answer": 1,
 "why": "Inconsistent behavior across identical software almost always points to policy scoping: the machines sit in different groups with different policies, and the application is approved in one but not the other. The engineer should compare group membership and the effective policy for a working vs. a blocked machine. Jumping to reinstallation or assuming infection skips the obvious configuration check, and application behavior is deterministic, not random.",
 "hint": "Same file, same version, different result. What differs between the machines?",
 "objectives": ["Diagnose policy-scoping inconsistencies", "Compare effective policy across groups"],
 "mins": 10,
 "evidence": [
  ["Working machine", "Group: Workstations-East | Policy: Standard v12 | invoicer.exe: Allowed"],
  ["Blocked machine", "Group: Workstations-West | Policy: Standard v11 | invoicer.exe: Denied (not on allowlist)"]
 ]
},
{
 "id": "tl-troubleshoot-06",
 "title": "Portable App Blocked from USB",
 "domain_id": "customer-scenarios",
 "situation": "A traveling sales rep runs a portable presentation tool from a USB drive. It is blocked on her laptop. The same tool runs fine when copied to the local drive on her colleague's machine.",
 "prompt": "Which two controls are interacting here, and how should the engineer resolve it?",
 "choices": [
  "Only the antivirus is involved; add an exclusion",
  "Storage Control is denying execution from removable media, and Allowlisting has no entry for the portable executable. Resolve by approving the executable's hash and, if business-justified, creating a scoped Storage Control exception for that device or file",
  "USB ports are physically broken on her laptop",
  "The application is incompatible with USB drives"
 ],
 "answer": 1,
 "why": "Two controls intersect: Storage Control governs what removable media can do (many policies block execution from USB outright), and Allowlisting independently requires the executable itself to be approved. The colleague's machine works because the file sits on an allowed path and may already be approved. The fix addresses both layers: approve the file hash and create a narrowly scoped storage exception if the business need justifies it, rather than opening USB execution broadly.",
 "hint": "Two different policies can each independently deny the same action. Which two?",
 "objectives": ["Analyze interacting controls (Storage + Allowlisting)", "Create scoped exceptions instead of broad openings"],
 "mins": 12,
 "evidence": [
  ["Block events", "Denied: E:\\presenter\\present.exe | Reasons: (1) Execution from removable media denied by Storage Control; (2) File not on allowlist"],
  ["Colleague's machine", "C:\\Tools\\present.exe | Allowed (hash approved 2026-09-20)"]
 ]
},
# --- Ringfencing (5) ---
{
 "id": "tl-troubleshoot-07",
 "title": "Outlook Cannot Open Attachments",
 "domain_id": "product-deep-dive",
 "situation": "Users report that double-clicking attachments in Outlook does nothing, or the attachment opens but cannot save changes. This started after the security team enabled stricter application containment.",
 "prompt": "What is happening, and how should it be addressed?",
 "choices": [
  "Outlook is corrupted on all machines and needs repair",
  "Ringfencing is constraining what Outlook is allowed to do: the file leash or application leash is preventing Outlook from launching child processes or writing to certain locations. Review the Ringfence policy for Outlook and adjust the leashes to permit the legitimate attachment workflow while keeping risky behaviors fenced",
  "The email server is down",
  "Users need local admin rights to open attachments"
 ],
 "answer": 1,
 "why": "Ringfencing places per-application boundaries (leashes) on what an app may do: which files it can touch, which processes it can launch, which network destinations it can reach. Overly strict leashes on Outlook break legitimate attachment handling. The fix is surgical: examine which specific leash is denying (file, application, network, or registry) and relax only that behavior for the legitimate workflow, preserving containment of genuinely risky actions like macro-launched PowerShell.",
 "hint": "What control limits what an already-approved application is allowed to DO?",
 "objectives": ["Diagnose Ringfence leash denials", "Tune leashes without removing containment"],
 "mins": 12,
 "evidence": [
  ["Ringfence deny", "outlook.exe attempted to launch winword.exe (child process) | Action: Denied by Application leash"],
  ["User impact", "120 users | Attachment open/save workflow broken since policy v14 applied"]
 ]
},
{
 "id": "tl-troubleshoot-08",
 "title": "Browser Cannot Download Files",
 "domain_id": "product-deep-dive",
 "situation": "After a Ringfencing policy update, users can browse normally but all file downloads fail silently in Chrome. The help desk is flooded.",
 "prompt": "Where should the engineer look first?",
 "choices": [
  "Reinstall Chrome on every machine",
  "Inspect the Ringfence policy for the browser: a file or network leash is likely blocking writes to the Downloads folder or the download stream itself. Identify the denying leash in the audit log and scope an exception for the legitimate download path",
  "The internet connection is too slow for downloads",
  "Chrome needs to be added to the allowlist"
 ],
 "answer": 1,
 "why": "Browsing works but downloads fail, which points squarely at a Ringfence leash on the browser rather than an execution problem (Chrome itself is clearly approved and running). The audit log will show exactly which leash denied the write. The fix is to permit the legitimate download path while keeping the browser fenced from dangerous behaviors like writing executables to startup locations. Reinstalling the browser changes nothing about policy.",
 "hint": "The application runs fine. Only one specific behavior is blocked. Which control governs behavior?",
 "objectives": ["Isolate behavior blocks from execution blocks", "Read Ringfence deny events"],
 "mins": 10,
 "evidence": [
  ["Audit log", "chrome.exe → Write to C:\\Users\\*\\Downloads\\report.pdf | Denied by File leash (policy: Browser-Hardened v3)"],
  ["Scope", "All 400 workstations | Started 2026-10-10 08:02 after policy push"]
 ]
},
{
 "id": "tl-troubleshoot-09",
 "title": "Application Cannot Reach Network Share",
 "domain_id": "product-deep-dive",
 "situation": "A document management client can open local files but fails to connect to the file server share. Other applications on the same machine reach the share without issues. Network connectivity is fine.",
 "prompt": "What is the most likely cause?",
 "choices": [
  "The file server is offline",
  "Ringfencing on the document management application is denying its network access to the share. Other apps work because their own Ringfence policies permit it; this app's network leash needs the file server destination allowed",
  "The user's password expired",
  "DNS is misconfigured on the workstation"
 ],
 "answer": 1,
 "why": "The key clue is that other applications on the same machine reach the share fine, which rules out network, server, credential, and DNS issues — those would affect everything. Ringfencing is per-application, so a network leash on this specific app can block its share access while leaving other apps untouched. The engineer should check the app's Ringfence network leash and add the file server as an allowed destination.",
 "hint": "Same machine, same network, same server — but only one app fails. What is scoped per-application?",
 "objectives": ["Use differential diagnosis with per-app controls", "Configure Ringfence network destinations"],
 "mins": 10,
 "evidence": [
  ["Ringfence deny", "docmgmt.exe → SMB to \\\\fileserver\\share (TCP 445) | Denied by Network leash"],
  ["Control test", "explorer.exe → \\\\fileserver\\share | Allowed (same machine, same user)"]
 ]
},
{
 "id": "tl-troubleshoot-10",
 "title": "Excel Macro Blocked from Running Scripts",
 "domain_id": "product-deep-dive",
 "situation": "A finance user has an Excel workbook with macros that automate monthly reporting. The macros are blocked. The user says the workbook is from a trusted colleague and has worked for two years.",
 "prompt": "How should the engineer respond?",
 "choices": [
  "Unblock macros for Excel across the whole company so finance is never interrupted",
  "Recognize this as Ringfencing working as designed: Office macros launching scripts is a classic attack vector. Verify the workbook's legitimacy, then create a targeted exception (e.g., allow the specific signed macro or the specific workbook) rather than opening macros globally",
  "Tell the user macros are banned and they must do the reporting manually",
  "Disable the agent on the finance user's machine"
 ],
 "answer": 1,
 "why": "Macro-to-script execution is one of the most abused attack chains in existence, so Ringfencing constrains it by default — the control is doing its job. The right move is not to remove the fence but to build a gate: verify the specific workbook is legitimate and create a narrow exception for it (signed macro, known file hash, or approved publisher). A global macro exemption would re-open the exact attack path the control exists to close.",
 "hint": "Is the control broken, or is it doing exactly what it was designed to do?",
 "objectives": ["Distinguish working-as-designed from misconfiguration", "Build narrow exceptions for legitimate macro use"],
 "mins": 12,
 "evidence": [
  ["Ringfence deny", "excel.exe → spawned powershell.exe via macro | Denied by Application leash (Office-Hardened)"],
  ["Workbook info", "Monthly_Report_v8.xlsm | Macros signed by Finance-Dept cert (valid) | In use since 2024"]
 ]
},
{
 "id": "tl-troubleshoot-11",
 "title": "PDF Reader Cannot Print",
 "domain_id": "product-deep-dive",
 "situation": "Users can open PDFs but printing fails with a generic error. The printers work from every other application. The issue appeared after the PDF reader's Ringfence policy was tightened.",
 "prompt": "What should the engineer check?",
 "choices": [
  "Replace all the printers",
  "Check the Ringfence policy for the PDF reader: printing requires the application to communicate with the print spooler (a device/peripheral interaction), and a device or application leash may be denying it. Allow the spooler interaction for the reader while keeping other restrictions",
  "Reinstall the PDF reader on all machines",
  "The PDF files are corrupted"
 ],
 "answer": 1,
 "why": "Printing from an application means talking to the print spooler service, which is a cross-process/device interaction that Ringfencing can restrict. Since printing works from other apps, the printers and spooler are healthy — only this reader's leash is denying the interaction. The fix is to permit the spooler communication for the reader specifically. Reinstalling or replacing printers addresses components that are demonstrably working.",
 "hint": "Printing is an app talking to another service. What governs what an app may talk to?",
 "objectives": ["Diagnose device/peripheral leash denials", "Permit spooler interaction surgically"],
 "mins": 10,
 "evidence": [
  ["Ringfence deny", "reader.exe → interact with spoolsv.exe | Denied by Application leash"],
  ["Control test", "winword.exe → print | Allowed (same printer, same machine)"]
 ]
},
# --- Elevation Control (4) ---
{
 "id": "tl-troubleshoot-12",
 "title": "User Needs Admin for One App Only",
 "domain_id": "technical-questions",
 "situation": "A user needs to run a legacy inventory tool that requires administrator rights, but company policy prohibits making users local admins. The help desk has been manually entering admin credentials for months.",
 "prompt": "What is the proper solution?",
 "choices": [
  "Make the user a local administrator; it is the only way legacy apps work",
  "Create an Elevation Control policy that permits elevation for that specific application only. The user remains a standard user everywhere else, and the elevation is audited",
  "Uninstall the legacy tool and tell the department to buy a modern replacement immediately",
  "Share the local admin password with the user"
 ],
 "answer": 1,
 "why": "Elevation Control exists precisely for this: grant administrative rights to a specific application without making the user an administrator. The policy elevates just that executable, the action is logged in the audit trail, and the user's own account stays standard. Making the user a full admin or sharing the admin password grants far broader rights than needed and destroys accountability.",
 "hint": "How do you give admin rights to an application without giving them to the person?",
 "objectives": ["Apply just-in-time elevation for specific apps", "Preserve least privilege"],
 "mins": 10,
 "evidence": [
  ["Ticket history", "47 manual admin-credential entries for inventory.exe in the last 90 days"],
  ["Policy", "Company standard: no standing local admins (compliance requirement)"]
 ]
},
{
 "id": "tl-troubleshoot-13",
 "title": "Elevation Prompt Not Appearing",
 "domain_id": "technical-questions",
 "situation": "A user right-clicks an installer and chooses 'Run as administrator', but no elevation prompt appears and the installer fails. Elevation Control is deployed. Other users get prompts normally.",
 "prompt": "What should the engineer investigate?",
 "choices": [
  "The user's monitor is too small to display the prompt",
  "Check whether an Elevation Control policy is silently denying (rather than prompting) for this user or application, verify the agent is healthy on the machine, and confirm the user is in the group the elevation policy targets",
  "Reinstall Windows on the machine",
  "The installer is corrupted; download it again"
 ],
 "answer": 1,
 "why": "When prompts appear for others but not this user, the cause is policy or agent state, not the installer. Elevation Control can be configured to auto-deny certain elevations without prompting, the agent might not be running properly on that machine, or the user might fall outside the policy's targeted group. The engineer should check the effective elevation policy for that user/machine and the agent's health before assuming media or OS problems.",
 "hint": "It works for others. What differs for this user or machine?",
 "objectives": ["Troubleshoot missing elevation prompts", "Check policy targeting and agent health"],
 "mins": 10,
 "evidence": [
  ["Agent status", "Machine WKST-1142: agent service running, last check-in 4 min ago"],
  ["Policy", "Elevation policy 'Installers-Standard-Users' targets group 'Branch-Users'; affected user is in 'Branch-Users-Temp'"]
 ]
},
{
 "id": "tl-troubleshoot-14",
 "title": "Developer Needs Local Admin for Dev Tools",
 "domain_id": "technical-questions",
 "situation": "A software developer needs to install SDKs, run debuggers, and modify system paths. IT will not grant standing local admin. The developer is blocked several times per week waiting for help desk elevation.",
 "prompt": "What balanced approach should the engineer propose?",
 "choices": [
  "Grant the developer permanent local admin; developers always need it",
  "Build a scoped Elevation Control policy covering the developer's toolchain (approved IDEs, SDK installers, debuggers), possibly time-bound or ticket-linked, so the developer is unblocked while every elevation is audited and limited to known tools",
  "Tell the developer to do all work on a personal laptop outside company policy",
  "Remove ThreatLocker from developer machines entirely"
 ],
 "answer": 1,
 "why": "Developers genuinely need elevated operations, but standing admin violates least privilege. A scoped elevation policy for the known toolchain gives the developer autonomy for legitimate work while keeping everything else standard and every elevation logged. Time-bounding or tying elevation to change tickets adds further control. Exempting machines or using personal devices removes visibility entirely, which is worse for security.",
 "hint": "How do you unblock legitimate admin work without granting unlimited admin?",
 "objectives": ["Design scoped elevation for power users", "Balance productivity with least privilege"],
 "mins": 12,
 "evidence": [
  ["Ticket volume", "Developer filed 23 elevation requests in 30 days (SDK installs, debugger attaches, PATH edits)"],
  ["Tools list", "Approved: VS Code, .NET SDK, WinDbg, Docker Desktop (all signed, vendor-verified)"]
 ]
},
{
 "id": "tl-troubleshoot-15",
 "title": "Elevation Approved but App Still Fails",
 "domain_id": "technical-questions",
 "situation": "An elevation request for a system utility was approved and the UAC-style prompt was accepted, but the utility still fails with 'Access denied' when writing to a protected directory.",
 "prompt": "Why might an approved elevation still fail?",
 "choices": [
  "Elevation Control is broken and should be uninstalled",
  "Elevation grants the application's process administrative rights, but other controls still apply: Ringfencing leashes on the application can still deny the specific file write, or the destination may be protected by additional policy. Check the audit log for the subsequent deny after the elevation succeeded",
  "The user clicked the wrong button on the prompt",
  "The computer needs more RAM"
 ],
 "answer": 1,
 "why": "Elevation and containment are independent layers. Elevation Control answers 'may this run as admin?' while Ringfencing answers 'what may it do even as admin?'. An elevated process can still be denied a specific action by its Ringfence leashes. The audit log will show two events: the elevation allowed, then the file write denied by a leash. The fix is to adjust the relevant leash, not to re-elevate or remove the controls.",
 "hint": "Two different controls answer two different questions. Which question did elevation answer, and which remains?",
 "objectives": ["Understand elevation vs. containment layering", "Read sequential allow/deny audit trails"],
 "mins": 12,
 "evidence": [
  ["Audit sequence", "10:02:14 Elevation approved: sysutil.exe (user: jdoe) | 10:02:15 Denied: sysutil.exe → write C:\\Windows\\System32\\drivers\\etc\\hosts (File leash)"],
  ["User report", "'I approved the prompt but it still says Access denied'"]
 ]
},
# --- Network Control (4) ---
{
 "id": "tl-troubleshoot-16",
 "title": "Legitimate App Cannot Reach the Internet",
 "domain_id": "product-deep-dive",
 "situation": "A newly deployed CRM client cannot connect to its cloud service. Browsers on the same machine reach the internet fine. The CRM vendor's documentation lists the required domains and ports.",
 "prompt": "What is the likely cause and fix?",
 "choices": [
  "The internet is down",
  "Network Control (the application firewall) has no rule permitting the CRM client. Browsers work because they have their own rules. Create a firewall rule allowing the CRM executable to reach the vendor's documented domains/ports",
  "The CRM license expired",
  "Reinstall the CRM client"
 ],
 "answer": 1,
 "why": "Network Control filters per-application, so one app's blocked traffic does not imply a network outage — the browsers working proves connectivity is fine. The CRM client simply lacks a firewall rule. The fix is to add a rule permitting that executable to the vendor's documented destinations. This is the deny-by-default firewall doing its job: unknown app traffic is denied until explicitly permitted.",
 "hint": "Browsers work, one app does not. What filters traffic per-application?",
 "objectives": ["Diagnose per-app firewall denials", "Create application firewall rules"],
 "mins": 10,
 "evidence": [
  ["Firewall deny", "crmclient.exe → api.vendor.com:443 | Denied: no matching Network Control rule"],
  ["Control test", "chrome.exe → api.vendor.com:443 | Allowed (rule: Browsers-HTTPS)"]
 ]
},
{
 "id": "tl-troubleshoot-17",
 "title": "New SaaS App Blocked",
 "domain_id": "product-deep-dive",
 "situation": "The company adopted a new SaaS HR platform. The web portal works, but the desktop sync client cannot connect. The SaaS vendor provided a list of required URLs and ports.",
 "prompt": "What should the engineer do?",
 "choices": [
  "Tell HR to only use the web portal",
  "Build Network Control rules for the sync client covering the vendor's documented URLs and ports, test connectivity, and document the rules for the next SaaS onboarding",
  "Disable the firewall for the HR department",
  "The SaaS vendor's software is incompatible and must be replaced"
 ],
 "answer": 1,
 "why": "The web portal works because browsers already have HTTPS rules; the sync client is a separate executable with no rule. Using the vendor's published URL/port list, the engineer creates precise firewall rules for the client. This also establishes a repeatable SaaS onboarding pattern: collect vendor network requirements, create scoped rules, test, document. Disabling the firewall for a department trades a small configuration task for a large security gap.",
 "hint": "The browser and the sync client are different executables. What does each need?",
 "objectives": ["Onboard SaaS clients through firewall policy", "Build a repeatable SaaS network-requirements workflow"],
 "mins": 12,
 "evidence": [
  ["Vendor requirements", "sync.hrplatform.com:443, cdn.hrplatform.com:443, push.hrplatform.com:8443"],
  ["Firewall log", "hrsync.exe → push.hrplatform.com:8443 | Denied (no rule)"]
 ]
},
{
 "id": "tl-troubleshoot-18",
 "title": "VPN Client Blocked from Connecting",
 "domain_id": "product-deep-dive",
 "situation": "Remote users cannot establish VPN connections. The VPN client launches but fails during the connection phase. This began after Network Control policies were tightened.",
 "prompt": "What should the engineer check?",
 "choices": [
  "The VPN server is down; call the ISP",
  "Verify Network Control permits the VPN client's required protocols and ports (e.g., UDP 500/4500 for IPsec, or the vendor's ports). A tightened firewall can block the tunnel establishment itself. Add precise rules for the VPN executable",
  "Remote users should come to the office instead",
  "Uninstall the VPN client from all machines"
 ],
 "answer": 1,
 "why": "VPN tunnel establishment needs specific protocols and ports allowed for the VPN client executable. When firewall policies are tightened without accounting for the VPN client, the tunnel cannot form and users see connection failures. The engineer should check the VPN vendor's port/protocol requirements against the current Network Control rules and add what is missing. The timing (right after tightening) strongly implicates the policy change.",
 "hint": "What changed just before the failures started? What does a VPN client need at the network layer?",
 "objectives": ["Correlate policy changes with new failures", "Permit VPN protocols through application firewall"],
 "mins": 12,
 "evidence": [
  ["Change log", "2026-10-09 18:00: Network Control policy 'Strict-Egress' applied to Remote-Users group"],
  ["Firewall deny", "vpnclient.exe → UDP 500 (IKE) | Denied | 84 affected users"]
 ]
},
{
 "id": "tl-troubleshoot-19",
 "title": "Internal App Cannot Cross VLANs",
 "domain_id": "product-deep-dive",
 "situation": "A monitoring dashboard on the IT VLAN cannot collect data from agents on the workstation VLAN. The agents are online and the dashboard worked before the network segmentation project.",
 "prompt": "How should the engineer approach this?",
 "choices": [
  "Flatten the network back to a single VLAN",
  "Treat it as a Network Control rule problem: identify the dashboard executable, the agent ports/protocols, and the direction of traffic, then create rules permitting the dashboard's cross-VLAN collection while keeping the segmentation intact",
  "The agents are all broken and need reinstalling",
  "Monitoring is not important; disable the dashboard"
 ],
 "answer": 1,
 "why": "Segmentation is working as intended by denying cross-VLAN traffic by default; the dashboard simply needs explicit permission as a known-good exception. The engineer maps the exact flow (which executable, which ports, which direction) and writes a narrow rule. Flattening the network would undo the security benefits of segmentation to solve a configuration task, and the agents are demonstrably online.",
 "hint": "Segmentation denies by default. What is the legitimate exception here, and how narrowly can it be drawn?",
 "objectives": ["Permit legitimate cross-VLAN flows", "Preserve segmentation while enabling monitoring"],
 "mins": 12,
 "evidence": [
  ["Firewall deny", "dashboard.exe → 10.20.0.0/16:8443 | Denied (inter-VLAN, no rule)"],
  ["Agent status", "1,204 agents online, last check-in < 5 min (they just cannot be reached FROM the dashboard)"]
 ]
},
# --- Storage Control (3) ---
{
 "id": "tl-troubleshoot-20",
 "title": "USB Drives Blocked for Everyone",
 "domain_id": "customer-scenarios",
 "situation": "After enabling Storage Control, no USB drives work anywhere in the company — including for the IT staff who need them for legitimate work. The security team wants USB restricted but not unusable for authorized purposes.",
 "prompt": "What is the right configuration?",
 "choices": [
  "Disable Storage Control; USB blocking causes too many complaints",
  "Keep the default deny, then build scoped exceptions: allow specific encrypted device models, or specific AD groups (like IT), or require encryption. Deny-by-default stays, legitimate use gets a defined path",
  "Allow all USB drives for everyone to stop the complaints",
  "Physically glue all USB ports shut"
 ],
 "answer": 1,
 "why": "Storage Control's value is deny-by-default on removable media; the complaints come from having no defined legitimate path, not from the control itself. The mature configuration keeps the deny and adds narrow exceptions: approved encrypted drive models, authorized groups, or per-device approvals. This preserves the security benefit (unknown USB devices still blocked) while giving IT and others a workable process.",
 "hint": "The control is not the problem; the missing piece is the legitimate path through it.",
 "objectives": ["Design USB exception workflows", "Balance removable-media security with usability"],
 "mins": 10,
 "evidence": [
  ["Policy", "Storage Control: Deny all removable storage (applied org-wide 2026-10-07)"],
  ["Tickets", "63 USB-related tickets in 3 days, including 11 from IT staff"]
 ]
},
{
 "id": "tl-troubleshoot-21",
 "title": "Encrypted USB Works, Unencrypted Blocked",
 "domain_id": "customer-scenarios",
 "situation": "A user reports their personal unencrypted USB drive is blocked, but the company-issued encrypted drive works fine. They demand the personal drive be allowed.",
 "prompt": "How should the engineer respond?",
 "choices": [
  "Allow the personal drive; the user needs it",
  "Explain this is the policy working as designed: Storage Control permits encrypted, company-approved devices and denies unencrypted personal media to prevent data loss. Offer the approved encrypted drive process instead of making an exception",
  "Disable encryption requirements for everyone",
  "Format the personal drive and hope it starts working"
 ],
 "answer": 1,
 "why": "This is not a malfunction — it is the intended outcome of an encryption-enforcing storage policy. Unencrypted removable media is a data-loss vector, so the policy deliberately permits only encrypted approved devices. The correct response is to explain the design and route the user to the approved device process. Allowing the personal drive would create exactly the gap the policy was built to close.",
 "hint": "Is anything actually broken here? What is the policy trying to achieve?",
 "objectives": ["Recognize working-as-designed vs. misconfiguration", "Communicate policy rationale to users"],
 "mins": 10,
 "evidence": [
  ["Policy", "Storage Control: Allow only BitLocker-encrypted removable drives (company-issued)"],
  ["Device info", "Personal drive: unencrypted, unknown origin | Company drive: BitLocker, issued 2026-06-15"]
 ]
},
{
 "id": "tl-troubleshoot-22",
 "title": "One-Time USB Need for Presentation",
 "domain_id": "customer-scenarios",
 "situation": "An executive needs to present from a USB drive at a client site in two hours. Company policy blocks unapproved USB devices. There is no time for the normal device-approval process.",
 "prompt": "What is the best handling?",
 "choices": [
  "Permanently allow all USB drives so this never happens again",
  "Grant a time-limited, audited exception for the specific device (or copy the presentation to an approved encrypted drive). Log the exception, set it to expire, and review it afterward",
  "Tell the executive to cancel the presentation",
  "Disable Storage Control on the executive's laptop indefinitely"
 ],
 "answer": 1,
 "why": "Urgent legitimate needs should be met through temporary, scoped, audited exceptions — not permanent policy changes. Approving the specific device for a few hours (or moving the files to an approved encrypted drive) solves the immediate need, the expiration automatically restores the secure baseline, and the audit trail records who approved what and why. Permanent changes made under time pressure tend to persist long after the emergency.",
 "hint": "How do you say yes to the emergency without saying yes forever?",
 "objectives": ["Issue time-bound security exceptions", "Keep emergency access audited"],
 "mins": 10,
 "evidence": [
  ["Request", "Exec needs USB access 14:00-18:00 today for client presentation"],
  ["Policy", "Normal device approval SLA: 2 business days (cannot meet the deadline)"]
 ]
},
# --- Portal/Policy (4) ---
{
 "id": "tl-troubleshoot-23",
 "title": "Policy Changes Not Applying",
 "domain_id": "technical-questions",
 "situation": "An admin updated an Application Control policy in the portal two hours ago, but endpoints are still enforcing the old rules. The admin is certain they clicked Save.",
 "prompt": "What should the engineer check, in order?",
 "choices": [
  "Rebuild the entire portal database",
  "Verify the policy was actually deployed/published (not just saved as draft), confirm the agents have checked in since the deployment, and check whether the endpoints are in the group the policy targets",
  "Reinstall the agent on every endpoint",
  "The portal is broken; wait 24 hours"
 ],
 "answer": 1,
 "why": "Policy changes follow a pipeline: edit → save → deploy/publish → agent check-in → enforcement. A break at any stage produces this symptom. The most common causes are a policy left in draft, agents that have not checked in yet, or endpoints sitting outside the targeted group. Walking the pipeline in order isolates the stage quickly, while reinstalling agents or waiting blindly skips the actual diagnostic steps.",
 "hint": "Saving is not deploying, and deploying is not enforcing. What are the stages in between?",
 "objectives": ["Trace the policy deployment pipeline", "Verify publish, check-in, and targeting"],
 "mins": 10,
 "evidence": [
  ["Portal", "Policy 'Standard v15': status Draft (last edited 2h ago, never deployed)"],
  ["Agent check-ins", "Median check-in age: 6 min (agents are communicating fine)"]
 ]
},
{
 "id": "tl-troubleshoot-24",
 "title": "New Computer Not Getting Policies",
 "domain_id": "technical-questions",
 "situation": "A newly imaged workstation has the agent installed and shows in the portal, but none of the customer's policies apply to it. It behaves as if it has no policy at all.",
 "prompt": "What is the most likely cause?",
 "choices": [
  "The agent installer is corrupted; reinstall Windows",
  "The machine is not assigned to the correct group (or any group) in the portal, so no group-targeted policies apply to it. Verify group assignment and onboarding workflow",
  "New computers need 48 hours before policies apply",
  "The portal license is expired"
 ],
 "answer": 1,
 "why": "Policies target groups, not individual machines by default. A new machine that lands in the portal but in no group (or the wrong group) receives no group policies — exactly the 'no policy at all' symptom. The fix is to check the machine's group membership and the onboarding process that should assign it. Agent reinstalls and waiting periods do not address group assignment.",
 "hint": "Policies target groups. Where does a brand-new machine land?",
 "objectives": ["Verify endpoint group assignment", "Audit the onboarding workflow"],
 "mins": 10,
 "evidence": [
  ["Portal", "WKST-2201: agent online, group = 'Ungrouped' (0 policies target this group)"],
  ["Onboarding doc", "Step 7: 'Assign to department group' — marked optional, frequently skipped"]
 ]
},
{
 "id": "tl-troubleshoot-25",
 "title": "Conflicting Policies, Unexpected Denies",
 "domain_id": "technical-questions",
 "situation": "An application is approved in the company's baseline policy but keeps getting denied on a subset of machines. Those machines have an additional departmental policy applied.",
 "prompt": "How should the engineer resolve the conflict?",
 "choices": [
  "Delete all policies and start over",
  "Review policy precedence and merging: determine which policy's deny is winning on the affected machines, then reconcile the two policies (adjust the departmental policy's rule or its precedence) so the intended approval takes effect without weakening the departmental restrictions that matter",
  "Approve the application a second time in the departmental policy and hope it sticks",
  "Remove the departmental policy entirely"
 ],
 "answer": 1,
 "why": "When multiple policies apply, they merge according to precedence rules, and a deny in one can override an allow in another. The engineer must identify which policy is producing the effective deny and understand the merge order before changing anything. Blindly duplicating approvals or deleting policies risks breaking the protections the departmental policy was built for. The goal is a reconciled policy set where both the baseline approval and the departmental intent hold.",
 "hint": "Two policies apply. One says allow, the effective result is deny. What decides the winner?",
 "objectives": ["Analyze policy precedence and merging", "Reconcile conflicting policies safely"],
 "mins": 12,
 "evidence": [
  ["Effective policy (affected machine)", "Baseline: invoicer.exe Allowed | Departmental: *.exe in C:\\DeptApps\\ Denied (precedence: higher)"],
  ["File path", "C:\\DeptApps\\invoicer.exe — matches the departmental deny pattern"]
 ]
},
{
 "id": "tl-troubleshoot-26",
 "title": "Agent Shows Offline in Portal",
 "domain_id": "technical-questions",
 "situation": "Twelve machines show as offline in the portal even though users are actively working on them. The machines were online yesterday.",
 "prompt": "What is the systematic troubleshooting order?",
 "choices": [
  "Reimage all twelve machines immediately",
  "Check in order: is the agent service running on the endpoints, can the endpoints reach the portal (network/proxy/firewall), and did anything change (maintenance window, network change, certificate expiry)? Start with the endpoint service, then connectivity, then recent changes",
  "The portal is down for everyone",
  "Ignore it; offline agents still enforce the last policy"
 ],
 "answer": 1,
 "why": "Offline-in-portal means the heartbeat is not arriving, so the diagnostic order is: endpoint (is the agent service running?), path (can it reach the portal through the network, proxy, and firewall?), and change (what changed since yesterday when it worked?). This ordered approach isolates the layer quickly. Reimaging is disproportionate before knowing the cause, and while offline agents do enforce cached policy, losing visibility and future updates is itself a problem to fix.",
 "hint": "The agent phones home on a schedule. What could stop the call at each stage?",
 "objectives": ["Troubleshoot agent-to-portal connectivity", "Apply ordered diagnostics (endpoint → path → change)"],
 "mins": 12,
 "evidence": [
  ["Portal", "12 machines: last check-in 2026-10-09 17:42 (all same site)"],
  ["Site change log", "2026-10-09 18:00: Firewall rule change on site edge (outbound 443 restricted)"]
 ]
},
]

# ---------------------------------------------------------------- incidents (10)
I = [
{
 "id": "tl-incident-01",
 "title": "Ransomware Detained at the Gates",
 "domain_id": "customer-scenarios",
 "situation": "At 09:14, a user opened a weaponized spreadsheet from a phishing email. Within seconds, the ThreatLocker agent blocked a cascade of malicious actions: a macro spawning PowerShell, PowerShell attempting to disable recovery, and an encryption routine targeting network shares. The SOC wants a full timeline of what engaged, in order, and confirmation that nothing executed.",
 "prompt": "Reconstruct the attack chain and map each stage to the ThreatLocker control that stopped it. What do you report to the SOC?",
 "choices": [
  "Report that the antivirus caught everything and no further action is needed",
  "Walk the chain: the spreadsheet arrived (fetch policy), Excel launched (allowlisted, approved), the macro's PowerShell spawn was denied by Ringfencing's application leash, the recovery-disable attempt was denied by the registry/file leashes, and the share-encryption attempt was denied by the network/file leashes. Each deny is logged as a detection. Recommend isolating the machine for forensic imaging, hunting for lateral movement, and reviewing how the phishing email bypassed email filtering",
  "Wipe the machine immediately without investigation",
  "Disable macros for the entire company and close the ticket"
 ],
 "answer": 1,
 "why": "A proper incident report narrates the kill chain against the controls: each stage of the attack met a specific deny, and the audit log holds the evidence. The value is in the ordered mapping — it proves nothing executed and shows exactly where the attack died. Wiping without imaging destroys forensic evidence, and claiming antivirus handled it misattributes the controls. The follow-through (isolate, hunt laterally, fix the email vector) is what separates a block from a resolved incident.",
 "hint": "Map each attacker action to the control that denied it, in order. Then think about what happens AFTER the block.",
 "objectives": ["Map a ransomware kill chain to layered controls", "Produce an ordered incident timeline", "Recommend post-block incident response steps"],
 "mins": 20,
 "evidence": [
  ["09:14:03 Audit", "excel.exe spawned powershell.exe via macro | Denied by Application leash"],
  ["09:14:04 Audit", "powershell.exe attempted vssadmin delete shadows | Denied (process never launched; parent denied)"],
  ["09:14:07 Audit", "Unapproved binary 'enc.exe' attempted execution | Denied by Allowlisting (hash unknown)"],
  ["Email gateway", "Phishing email passed SPF/DKIM; attachment scanned clean by signature (zero-day macro)"]
 ]
},
{
 "id": "tl-incident-02",
 "title": "False Positive on Critical Business App",
 "domain_id": "customer-scenarios",
 "situation": "At 10:30 on month-end close day, the finance team's ERP client is suddenly blocked on all 60 machines. Finance is escalating to the CIO. The block started 20 minutes ago, coinciding with an automatic ERP update. The business cannot close the books.",
 "prompt": "How do you resolve this urgently without creating a lasting security gap?",
 "choices": [
  "Put the whole company in Monitor Only mode until finance is done",
  "Confirm the block is a hash-change from the legitimate ERP update (verify signature and source), push an emergency approval for the new version scoped to the ERP executable, verify finance is unblocked, then schedule a review of the update-approval workflow so future vendor updates are pre-approved",
  "Tell finance to wait until tomorrow",
  "Uninstall ThreatLocker from the finance machines"
 ],
 "answer": 1,
 "why": "This is the classic speed-vs-safety incident: the business is stopped, but the fix must not be a permanent hole. The correct play is verify-then-approve under pressure — confirm the new binary is the legitimate vendor update (signature, source, timing correlation), approve that specific version immediately, and confirm restoration. Monitor Only mode or uninstalling would leave the entire estate unprotected. The post-incident action (pre-approving vendor updates) prevents recurrence.",
 "hint": "What changed 20 minutes ago? How do you fix it fast AND safely?",
 "objectives": ["Execute emergency approval workflows", "Balance urgency with deny-by-default integrity", "Build preventive update-approval processes"],
 "mins": 18,
 "evidence": [
  ["Block events", "Denied: erpclient.exe | 60 endpoints | Started 10:10 | Reason: hash not on allowlist"],
  ["Vendor notice", "ERP vendor pushed auto-update v9.4.1 at 10:05 (signed, legitimate channel)"],
  ["Business impact", "Month-end close blocked | Escalation: CIO | 60 finance users idle"]
 ]
},
{
 "id": "tl-incident-03",
 "title": "Policy Conflict Causes Widespread Blocks",
 "domain_id": "customer-scenarios",
 "situation": "After a junior admin pushed a new 'hardened' policy to the entire organization, hundreds of users report blocked applications. The help desk queue has 400 tickets. The admin who made the change is on leave. You have portal access and 30 minutes before the next status call.",
 "prompt": "What is your incident response sequence?",
 "choices": [
  "Delete the new policy immediately and hope the old one comes back",
  "Triage: identify the new policy's scope and the deny patterns in the audit log, roll back or narrow the policy change (revert to the previous version or scope it to a pilot group), verify blocks stop, then establish a change-control process requiring peer review and staged rollouts for future policy changes",
  "Tell all users to reboot",
  "Wait for the junior admin to return from leave"
 ],
 "answer": 1,
 "why": "A bad policy push is an incident like any other: triage first (what changed, what is it denying), contain (roll back or narrow the scope), verify (confirm blocks stop), then fix the process (change control, peer review, staged rollouts). Deleting policies blindly can leave machines with no policy or create new gaps. The 30-minute status call needs a clear story: cause identified, containment done, prevention planned.",
 "hint": "Treat the bad policy like any incident: triage, contain, verify, then fix the process.",
 "objectives": ["Respond to policy-caused outages", "Execute rollback and scoping", "Establish policy change control"],
 "mins": 18,
 "evidence": [
  ["Change log", "2026-10-10 07:55: Policy 'Hardened-v2' pushed org-wide by jadmin (now on leave)"],
  ["Audit sample", "Denied: 2,140 events in 35 min | Top: chrome.exe updates, teams.exe, vpnclient.exe (all legitimate, previously allowed)"],
  ["Help desk", "400 tickets | Common: 'my apps stopped working after this morning'"]
 ]
},
{
 "id": "tl-incident-04",
 "title": "Agents Offline Across a Site",
 "domain_id": "customer-scenarios",
 "situation": "The entire Springfield branch (85 machines) shows offline in the portal. Users are working normally. The branch manager reports 'the internet was flaky this morning.' No policy changes were made. The SOC is concerned about losing visibility.",
 "prompt": "How do you diagnose and restore visibility?",
 "choices": [
  "Drive to Springfield and reinstall every agent",
  "Work the connectivity chain: confirm the agent services are running locally, test the path to the portal (including the morning's network flakiness, proxy, and firewall), check for anything that changed at the site edge, and restore the path. Note that endpoints continue enforcing cached policy while offline, so protection persists during the visibility gap",
  "Ignore it; the agents will come back on their own eventually",
  "Recreate all 85 computer objects in the portal"
 ],
 "answer": 1,
 "why": "Eighty-five machines going offline together points to a site-level path issue, not 85 individual agent failures — especially with 'flaky internet' reported that morning. The diagnostic chain is endpoint (service running?) → path (can it reach the portal?) → change (what happened at the site edge?). Importantly, offline agents keep enforcing their last policy, so the branch is still protected; the incident is about visibility and future updates, which frames the urgency correctly for the SOC.",
 "hint": "85 machines at one site, same morning the internet was flaky. Individual failure or common cause?",
 "objectives": ["Diagnose site-wide agent connectivity loss", "Distinguish protection continuity from visibility loss"],
 "mins": 15,
 "evidence": [
  ["Portal", "85 machines, site=Springfield: last check-in 08:12 (staggered over 4 min, suggesting network event)"],
  ["Branch report", "'Internet was flaky 08:00-08:30, seems fine now'"],
  ["Spot check", "WKST-SPR-022: agent service running, Test-NetConnection to portal: FAILED (timeout)"]
 ]
},
{
 "id": "tl-incident-05",
 "title": "Zero-Day Execution Attempt",
 "domain_id": "customer-scenarios",
 "situation": "An unknown executable with no signature and no reputation appeared in a user's Downloads folder and attempted to run. ThreatLocker denied it. The file does not match any known malware signature. The user claims they 'don't know where it came from.'",
 "prompt": "The block worked. What is the complete response?",
 "choices": [
  "Close the ticket; the block handled it",
  "Treat the deny as a detection: preserve the file for analysis, image the machine for forensics, hunt for how it arrived (browser history, email, USB), check for lateral movement indicators across the estate, and brief the SOC on the delivery vector so defenses can be tuned",
  "Delete the file and tell the user to be more careful",
  "Approve the file so you can see what it does"
 ],
 "answer": 1,
 "why": "Deny-by-default shines against zero-days precisely because it does not need a signature — unknown means denied. But the block is the beginning of the response, not the end. The file is evidence: its delivery vector (how did it get into Downloads?), its behavior (what did it try to do?), and whether siblings exist elsewhere in the estate. Closing the ticket at the block leaves the intrusion vector open for the next attempt.",
 "hint": "The block is a detection. What does a detection demand next?",
 "objectives": ["Run post-deny incident response", "Hunt delivery vectors for unknown files"],
 "mins": 18,
 "evidence": [
  ["Block event", "Denied: invoice_2026.exe | SHA256: unknown, unsigned, first seen in estate | Downloads folder"],
  ["User interview", "'I don't know where it came from' (browser history shows a typo-squatted domain visit 20 min prior)"],
  ["Estate hunt", "Same hash found on 0 other machines (isolated incident, so far)"]
 ]
},
{
 "id": "tl-incident-06",
 "title": "Insider Data Exfiltration Attempt",
 "domain_id": "customer-scenarios",
 "situation": "HR flagged a departing employee. The audit log shows the employee plugged in a personal USB drive and attempted to copy the customer database export (4 GB) to it. Storage Control denied the copy. The employee claims it was 'just personal files.'",
 "prompt": "What actions should the engineer take, and in what order?",
 "choices": [
  "Allow the copy; the employee says they are personal files",
  "Secure the evidence first: preserve the audit logs and block events, confirm what was and was not copied (was any data actually exfiltrated before the deny?), notify HR/security leadership per the insider-threat playbook, and keep the machine isolated for investigation. The deny is evidence, not the end of the matter",
  "Confront the employee directly and demand an explanation",
  "Delete the audit logs to protect the employee's privacy"
 ],
 "answer": 1,
 "why": "A denied exfiltration attempt is a security incident requiring the insider-threat playbook: preserve evidence before anything else (logs can be the basis for legal action), determine the actual data movement (did anything leave before the deny, via other channels?), and escalate through proper channels rather than confronting the individual. The engineer's role is evidence and containment; HR and legal own the personnel response. Deleting logs would destroy evidence and potentially constitute obstruction.",
 "hint": "The deny stopped this attempt. But what must be established before anyone declares victory?",
 "objectives": ["Handle insider-threat evidence preservation", "Determine actual vs. attempted data movement", "Follow escalation playbooks"],
 "mins": 18,
 "evidence": [
  ["Storage deny", "Denied: copy of C:\\Exports\\customers_2026Q3.csv (4.1 GB) → E:\\ (personal USB, unencrypted)"],
  ["Timeline", "Employee resignation submitted yesterday; drive plugged in 09:40 today"],
  ["Prior activity", "No previous USB usage by this user in 12 months (anomaly)"]
 ]
},
{
 "id": "tl-incident-07",
 "title": "Elevation Abuse Attempt",
 "domain_id": "customer-scenarios",
 "situation": "The audit log shows a standard user repeatedly attempting to elevate an unapproved system tool over three days, including renaming the executable to match an approved application's name. Elevation Control denied each attempt.",
 "prompt": "How should this be handled?",
 "choices": [
  "Approve the elevation; the user is persistent and probably needs it",
  "Recognize the pattern as deliberate bypass attempts (especially the renaming): deny, document the timeline, escalate to the user's manager and security team as a policy violation, and review whether the underlying business need is legitimate (if so, solve it through proper channels, not through the bypass)",
  "Ignore it since every attempt was denied",
  "Rename the approved application so the trick stops working"
 ],
 "answer": 1,
 "why": "Repeated elevation attempts culminating in executable renaming is not a confused user — it is a deliberate bypass attempt and a policy violation. The denials worked, but the behavior must be escalated: document the timeline, involve management and security, and address any legitimate underlying need through proper approval workflows. Ignoring it misses both the personnel issue and the chance to solve the real need legitimately.",
 "hint": "One attempt is confusion. Renaming the file to impersonate an approved app is something else. What?",
 "objectives": ["Identify bypass-attempt patterns", "Escalate policy violations properly"],
 "mins": 15,
 "evidence": [
  ["Audit timeline", "Day 1: 3 elevation attempts (sysutil.exe) denied | Day 2: 5 attempts denied | Day 3: sysutil.exe renamed to notepad.exe, 4 attempts denied"],
  ["User context", "Standard user, no approved business need on file for this tool"]
 ]
},
{
 "id": "tl-incident-08",
 "title": "Lateral Movement Blocked",
 "domain_id": "customer-scenarios",
 "situation": "Overnight, a compromised service account attempted to move laterally: SMB connections to 12 workstations, WMI queries against the domain, and a credential-dumping tool execution attempt. Network Control and application controls denied the movements. The SOC needs to know the blast radius.",
 "prompt": "What is the engineer's role in scoping this incident?",
 "choices": [
  "Nothing was blocked, so there is no incident",
  "Use the deny logs as the incident map: enumerate every denied lateral movement (which targets, which protocols), confirm the attacker's foothold machine, verify no movement succeeded (check for any allows in the same timeframe), and hand the SOC a scoped timeline showing the contained blast radius plus the initial compromise vector to remediate",
  "Shut down the entire network immediately",
  "Reset every password in the company without investigation"
 ],
 "answer": 1,
 "why": "The deny logs are a gift to incident response: they enumerate exactly what the attacker tried and where, which is precisely the blast-radius map the SOC needs. The engineer's job is to turn those logs into a scoped timeline — foothold, attempted movements (all denied), and confirmation that nothing succeeded — plus the initial vector for remediation. Panic responses like shutting down the network or mass resets without scoping cause more damage than the contained attack.",
 "hint": "Every denied attempt is a data point. What story do they tell together?",
 "objectives": ["Scope incidents using deny logs", "Produce attacker-timeline from control telemetry"],
 "mins": 20,
 "evidence": [
  ["Network denies", "svc-backup → SMB (445) to 12 workstations | All denied by Network Control (no rule for this account)"],
  ["App deny", "mimikatz.exe attempted execution on WKST-007 | Denied by Allowlisting"],
  ["Foothold", "WKST-007: svc-backup logged on interactively at 02:14 (anomalous; service accounts should not log on interactively)"]
 ]
},
{
 "id": "tl-incident-09",
 "title": "Mass Deployment Gone Wrong",
 "domain_id": "customer-scenarios",
 "situation": "IT pushed a new VPN client to 500 machines using a Learning Mode window. After the window closed, 120 machines cannot connect to VPN. The deployment team says 'it worked on the pilot group.' The VPN project deadline is tomorrow.",
 "prompt": "What went wrong, and how do you fix it under deadline?",
 "choices": [
  "Reopen Learning Mode indefinitely until it works",
  "Diagnose the delta: the pilot group and the failing 120 likely differ (different OS build, different existing policy, or the learning window missed components that only execute on first real connection). Identify the missing approvals from the deny logs, push targeted approvals for the VPN client's full component set, verify on a failing machine, then roll out. Document the pilot-vs-production gap for next time",
  "Deploy a different VPN product",
  "Tell the 120 users to work from the office"
 ],
 "answer": 1,
 "why": "Learning Mode only learns what actually executes during the window — if the pilot did not exercise every component (e.g., the tunnel driver that loads on first real connection), those components remain unknown and get denied later. The fix is to find the delta via the deny logs, approve the missing pieces deliberately, and verify. Reopening Learning Mode indefinitely reintroduces the risk the window was meant to bound, and the deadline pressure is exactly when deliberate verification matters most.",
 "hint": "Learning Mode learns what runs during the window. What if something important did not run then?",
 "objectives": ["Diagnose Learning Mode coverage gaps", "Compare pilot vs. production execution paths"],
 "mins": 18,
 "evidence": [
  ["Deny logs (failing machines)", "Denied: vpnfilter.sys (driver) | 120 machines | Never executed during learning window"],
  ["Pilot notes", "Pilot group tested 'connect' but not 'reconnect after sleep' (which loads the filter driver)"]
 ]
},
{
 "id": "tl-incident-10",
 "title": "Multi-Vector Attack Simulation (Capstone)",
 "domain_id": "customer-scenarios",
 "situation": "Exercise: a red team simulated a full attack — phishing delivery, macro execution, credential theft attempt, USB drop, and lateral movement — against a ThreatLocker-protected estate. You are given the complete audit log. Walk the exercise as the blue team lead: for each vector, state what the attacker tried, which control engaged, and what residual risk or follow-up remains.",
 "prompt": "What does a complete blue-team readback cover?",
 "choices": [
  "Everything was blocked, so the readback is one sentence: 'We are secure.'",
  "Vector by vector: (1) phishing email → attachment macro → PowerShell spawn denied by Ringfencing application leash; residual: tune email filtering. (2) credential-store read attempt → denied by Ringfencing; residual: verify no cached creds exposed. (3) USB drop with unknown binary → denied by Storage Control + Allowlisting; residual: physical security review. (4) lateral SMB → denied by Network Control; residual: segment review. For each: the deny, the evidence, and the hardening follow-up. The readback proves defense-in-depth with an improvement backlog, not just 'blocked.'",
  "The red team cheated; the exercise is invalid",
  "Delete the audit logs to keep the report short"
 ],
 "answer": 1,
 "why": "A mature readback does not stop at 'blocked' — it walks each vector, names the engaging control, cites the evidence, and extracts the residual risk and hardening action. This is the capstone skill: converting control telemetry into a narrative that both proves the defense worked and produces an improvement backlog. 'We are secure' is a conclusion without evidence; the vector-by-vector walk is the evidence.",
 "hint": "For each attack vector: what was tried, what stopped it, and what still needs hardening?",
 "objectives": ["Synthesize multi-vector telemetry into a narrative", "Extract residual risks from successful defenses", "Deliver executive-grade incident readbacks"],
 "mins": 20,
 "evidence": [
  ["Vector 1", "Macro → powershell.exe spawn | Denied (Ringfencing application leash)"],
  ["Vector 2", "Credential-store read by excel.exe | Denied (Ringfencing file leash)"],
  ["Vector 3", "USB: unknown.exe | Denied (Storage Control + Allowlisting)"],
  ["Vector 4", "SMB lateral to 6 hosts | Denied (Network Control)"]
 ]
},
]

# ---------------------------------------------------------------- apply
# Map: troubleshooting -> domains as specified; incidents -> customer-scenarios
added_t = 0
added_i = 0
existing_ids = set()
for d in data["domains"]:
    for s in d.get("scenarios", []):
        existing_ids.add(s["id"])

for sc in T:
    assert sc["id"] not in existing_ids, f"duplicate {sc['id']}"
    # find domain
    dom = next(d for d in data["domains"] if d["id"] == sc["domain_id"])
    dom.setdefault("scenarios", []).append(sc)
    existing_ids.add(sc["id"])
    added_t += 1

for sc in I:
    assert sc["id"] not in existing_ids, f"duplicate {sc['id']}"
    dom = next(d for d in data["domains"] if d["id"] == sc["domain_id"])
    dom.setdefault("scenarios", []).append(sc)
    existing_ids.add(sc["id"])
    added_i += 1

# Update simulation config to 10 items / 180 minutes
data["simulation"] = {"items": 10, "minutes": 180, "evidence_cost_mins": 2}

with open(PATH, "w") as f:
    json.dump(data, f, indent=2)

print(f"Added {added_t} troubleshooting scenarios")
print(f"Added {added_i} incident scenarios")
print("Simulation config:", data["simulation"])

# final validation
with open(PATH) as f:
    d2 = json.load(f)
total = sum(len(d.get("scenarios", [])) for d in d2["domains"])
print(f"Total scenarios now: {total}")
print(f"Domains: {len(d2['domains'])}, Lessons: {len(d2['lessons'])}, Labs: {len(d2['labs'])}")
# verify answer distribution
answers = []
for d in d2["domains"]:
    for s in d.get("scenarios", []):
        if s["id"].startswith("tl-troubleshoot-") or s["id"].startswith("tl-incident-"):
            assert 0 <= s["answer"] <= 3, s["id"]
            assert len(s["choices"]) == 4, s["id"]
            answers.append(s["answer"])
from collections import Counter
print("Answer distribution:", dict(Counter(answers)))
# no letter refs in why
import re
bad = [s["id"] for d in d2["domains"] for s in d.get("scenarios", [])
       if (s["id"].startswith("tl-troubleshoot-") or s["id"].startswith("tl-incident-"))
       and re.search(r"[Aa]nswer [A-D]\b|Correct is [A-D]\b", s.get("why", ""))]
print("Letter references in new 'why' fields:", bad if bad else "none")
