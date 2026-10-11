# ThreatLocker IT Infrastructure Assessment Prep — CBT

**Slug:** `tl-infra-assessment-prep`
**Live URL target:** https://interstitiumlabs.dev/bootcamps/tl-infra-assessment-prep/

Independent interview-prep bootcamp for the **IT Infrastructure Engineer (Systems Administrator)** role — a 3-hour hands-on terminal assessment covering Windows Server, Active Directory, networking, VPNs, Hyper-V, SQL Server, storage/backup/DR, PowerShell, and server hardening.

Built for Enmanuel D. Mejia ahead of his Tuesday, October 13, 2026 interview (via Crawford Thomas / Alex Starr). Personalized to his profile: ~5 years remote IT support, CompTIA A+, strong Windows/AD/networking background; extra depth on Hyper-V, SQL Server administration, enterprise storage/backup/DR, VLAN/VPN configuration, and PowerShell scripting.

## Contents

| Module | Domain ID | Scenarios | Lessons | Labs |
|---|---|---|---|---|
| Assessment Blueprint + Windows Server & AD | `windows-server-ad` | 7 | 3 | 3 |
| Networking Deep Dive | `networking` | 7 | 3 | 2 |
| VPN Technologies | `vpn` | 6 | 2 | 2 |
| Hyper-V Virtualization | `hyperv` | 7 | 3 | 3 |
| SQL Server Administration | `sql-server` | 6 | 2 | 2 |
| Storage, Backup & DR | `storage-backup-dr` | 6 | 2 | 2 |
| PowerShell for Infrastructure | `powershell` | 6 | 3 | 3 |
| Cybersecurity Best Practices | `security-hardening` | 6 | 2 | 2 |
| Documentation & Diagrams | `documentation` | 4 | 2 | 1 |
| **Total** | **9 domains** | **55** | **22** | **20** |

Plus: **10 timed mock-assessment scenarios** (180-minute simulation), **8 behavioral interview prompts** (STAR format), cheat sheets (subnetting, ports, GPO precedence, RAID, SQL backup chain, PowerShell one-liners, VPN troubleshooting flow, RTO/RPO), and a readiness checklist.

## Engine

Uses the shared bootcamp engine (`../_engine/`): adaptive drill workbench, terminal simulator, guided labs with command validation, timed simulation with countdown, behavioral prep, progress tracking via localStorage. Fully offline after load.

## Honest framing

Independent practice material by Interstitium Labs. Not affiliated with, endorsed by, or sponsored by ThreatLocker or Crawford Thomas. Confers no certificate. All scenarios are original; no exam or vendor-training content is reproduced.

## Authoring

Content authored 2026-10-10 across 5 parallel workstreams, assembled via `/tmp/tl-infra-fragments/assemble.py` (deterministic answer-position shuffle, schema validation, competitor-name scan). See `BUILD_REPORT.md` for the full build log.
