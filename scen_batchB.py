# Cert bootcamp content batch B: scenarios + lessons
# Generated 2026-10-10 for comptia-infra and cpp CBTs.

SCENARIOS = {
    "comptia-infra": {
        "cloud-arch": [
            {
                "id": "infra-cloudarch-sc1",
                "title": "Multi-Region Checkout Resilience",
                "domain_id": "cloud-arch",
                "situation": "Your e-commerce checkout service runs in a single cloud region behind a load balancer. During a regional incident last month, checkout was down for 90 minutes and the postmortem blamed a single AZ dependency. Management now demands checkout stay up during any single-region failure, but the database team warns that splitting the order database across regions could corrupt orders.",
                "prompt": "Which architecture keeps checkout available through a regional outage without risking order integrity?",
                "choices": [
                    "Active-passive with DNS failover and a synchronous multi-region relational database for orders",
                    "Active-active checkout front ends in two regions, region-local payment intake queues, and a single authoritative order ledger reconciled by idempotency keys",
                    "Replicate the full checkout stack into three regions with asynchronous eventual-consistency replication of the order database",
                    "Move checkout to a single larger region with three availability zones and double the instance count"
                ],
                "answer": 1,
                "why": "Payment intake can be parallelized per region (each queue holds durable, idempotent requests), while money movement requires exactly-one canonical ledger — idempotency keys let the single ledger absorb duplicate intake safely. Option A stalls on cross-region latency of synchronous commits and DNS failover is slow; C risks split-brain order state; D still dies with the region.",
                "hint": "Ask which part of checkout tolerates parallelism and which part demands exactly-once.",
                "objectives": ["Design multi-region resilient architectures", "Apply idempotency to distributed transactions"],
                "mins": 14,
                "evidence": ["Explains split intake-vs-ledger design"]
            },
            {
                "id": "infra-cloudarch-sc2",
                "title": "Burst Traffic on a Fixed Budget",
                "domain_id": "cloud-arch",
                "situation": "A marketing site gets 200 visitors per hour normally, but TV ad spots drive 40x spikes for 20 minutes, three times a week. The current fleet is statically provisioned for peak and finance wants the idle spend cut by half. The app is stateless except for sessions stored on local disk.",
                "prompt": "What combination handles the spikes and satisfies finance?",
                "choices": [
                    "Keep the peak fleet but convert half of it to spot instances",
                    "Auto-scaling group with target-tracking on request count, sessions moved to a shared session store, plus a CDN in front of static content",
                    "Scheduled scaling that doubles instances for the 20-minute ad windows",
                    "Containerize and run everything on a single large instance with burstable CPU"
                ],
                "answer": 1,
                "why": "Auto-scaling on a real demand metric matches capacity to the spike while sessions in a shared store let any instance serve any user (local-disk sessions break under scaling). A CDN absorbs the bulk of read traffic cheaply. Spot instances (A) get reclaimed exactly when ads air is not guaranteed and scheduled scaling (C) misses unscheduled spikes; a single box (D) is a failure domain.",
                "hint": "What breaks first when instances come and go mid-session?",
                "objectives": ["Design elastic architectures", "Separate stateless compute from session state"],
                "mins": 12,
                "evidence": ["Identifies session-state and scaling fix"]
            }
        ],
        "linux-admin": [
            {
                "id": "infra-linuxadmin-sc1",
                "title": "Web Service Won't Start After Reboot",
                "domain_id": "linux-admin",
                "situation": "After a kernel update and reboot, the company's nginx-based portal refuses to start. `systemctl status nginx` shows 'failed' and the journal mentions 'bind() to 0.0.0.0:443 failed (13: Permission denied)'. The config hasn't changed and the service ran fine before the reboot. SELinux is in enforcing mode.",
                "prompt": "What is the most likely cause, and the correct first fix?",
                "choices": [
                    "The update wiped the SSL certificate; regenerate the cert and restart",
                    "A stale PID file survived the reboot; delete it and start the service",
                    "nginx is running as a non-root user via a changed systemd unit, or SELinux is blocking the port bind; check the unit's User= and audit logs with ausearch",
                    "Port 443 is already in use by another service; kill whatever holds it"
                ],
                "answer": 2,
                "why": "Permission denied on bind to a privileged port (<1024) means the process lacks the capability — either the systemd unit now drops privileges before binding, or SELinux denies the socket bind (check `ausearch -m avc -ts recent`). Certs (A) produce TLS errors, not bind errors; PID files (B) don't survive reboots meaningfully; another listener (D) gives 'address already in use', not permission denied.",
                "hint": "Read the exact errno message — it says permission, not conflict.",
                "objectives": ["Troubleshoot systemd services", "Diagnose SELinux and privilege issues"],
                "mins": 12,
                "evidence": ["Interprets journal bind error correctly"]
            },
            {
                "id": "infra-linuxadmin-sc2",
                "title": "Disk Full But du Disagrees",
                "domain_id": "linux-admin",
                "situation": "Monitoring alerts that /var is 100% full on a database server, yet `du -sh /var/*` totals only 60% of the filesystem. The database is still writing and a junior admin suggests rebooting to 'clear it up'. Application logs are being written to /var/log/app at high volume.",
                "prompt": "What explains the mismatch, and what is the safe fix?",
                "choices": [
                    "Filesystem corruption; run fsck on /var immediately",
                    "Deleted-but-still-open log files held by the app process; find them with lsof and have the app reopen logs (e.g., via logrotate copytruncate or SIGHUP)",
                    "Reserved blocks for root; lower the reserved percentage with tune2fs",
                    "Inode exhaustion; delete small files to free inodes"
                ],
                "answer": 1,
                "why": "When a file is deleted while a process holds it open, `du` can't see it but the space isn't freed — the classic df-vs-du gap. `lsof | grep deleted` finds the culprits; rotating with copytruncate or signaling the app to reopen logs releases the space without data loss. fsck (A) needs downtime and addresses corruption, not this; reserved blocks (C) show as unavailable in df, not a du gap; inodes (D) show 'no space left' with df space free.",
                "hint": "The space is invisible to du but still allocated — who is holding it?",
                "objectives": ["Diagnose disk space discrepancies", "Manage log rotation safely"],
                "mins": 12,
                "evidence": ["Uses lsof to find deleted open files"]
            }
        ],
        "server-hw": [
            {
                "id": "infra-serverhw-sc1",
                "title": "RAID Choice for a Write-Heavy Database",
                "domain_id": "server-hw",
                "situation": "You're speccing local storage for a write-heavy transactional database server with eight SSDs. The DBA demands both strong write performance and survival of a double-disk failure. The hardware RAID controller has a battery-backed cache. Budget allows any RAID level.",
                "prompt": "Which RAID level best meets the requirements?",
                "choices": [
                    "RAID 5: striping with single parity, best usable capacity",
                    "RAID 6: striping with double parity, survives two disk failures",
                    "RAID 10: mirrored stripes, survives one failure per mirror pair",
                    "RAID 0: pure striping, maximum write throughput"
                ],
                "answer": 1,
                "why": "RAID 6 is the only option that both tolerates two simultaneous disk failures and keeps striping throughput. RAID 5 dies on a second failure during the long rebuild window; RAID 10 survives only if the second failure lands in a different mirror pair — the wrong pair fails and the array is gone; RAID 0 has no redundancy at all. The battery-backed cache mitigates RAID 6's write-parity penalty.",
                "hint": "Which option guarantees survival when ANY two specific disks fail?",
                "objectives": ["Select RAID levels for workload requirements", "Evaluate fault-tolerance trade-offs"],
                "mins": 10,
                "evidence": ["Justifies RAID 6 over RAID 10/5"]
            },
            {
                "id": "infra-serverhw-sc2",
                "title": "Mysterious Throttling Under Load",
                "domain_id": "server-hw",
                "situation": "A 2U application server performs fine for 10 minutes under load, then throughput collapses to 40% and stays there until idle for a while. CPU frequency monitoring shows the cores dropping to their minimum P-state during the collapse. Ambient datacenter temperature is normal and no alerts fire.",
                "prompt": "What is the most likely hardware-level cause?",
                "choices": [
                    "A failing power supply dropping to redundant-half capacity",
                    "Thermal throttling: heatsink clogged or thermal paste degraded, so the CPU hits its thermal limit under sustained load",
                    "Bad RAM triggering ECC corrections that stall the pipeline",
                    "The RAID controller battery failing, forcing write-through mode"
                ],
                "answer": 1,
                "why": "The time-delayed onset plus recovery after idle is the signature of heat soak: the CPU runs full speed until the heatsink saturates, then firmware clamps frequency to protect the chip. PSU issues (A) would trip immediately or reboot; ECC errors (C) log correctable-error counters and don't follow a clean 10-minute curve; write-through cache (D) affects disk writes, not CPU P-states.",
                "hint": "What physical process takes 10 minutes to build up and dissipates when idle?",
                "objectives": ["Diagnose thermal throttling", "Read hardware telemetry signals"],
                "mins": 10,
                "evidence": ["Links P-state drop to heat soak"]
            }
        ],
        "virtualization": [
            {
                "id": "infra-virtualization-sc1",
                "title": "VM Sluggish Despite Free Host CPU",
                "domain_id": "virtualization",
                "situation": "A Linux VM on a lightly loaded ESXi host shows high application latency. Inside the guest, `top` shows 70% idle CPU, but `%steal` is consistently above 25%. The VM was recently migrated to this host. Other VMs on the same host are fine.",
                "prompt": "What does high %steal with idle guest CPU indicate, and what should you check first?",
                "choices": [
                    "The guest kernel is misreporting; reinstall VMware Tools",
                    "CPU overcommit or a CPU limit/reservation on this VM: the hypervisor isn't scheduling its vCPUs; check resource limits and host ready-time",
                    "Memory ballooning is swapping guest pages; add more vRAM",
                    "Network contention on the vSwitch; check packet drops"
                ],
                "answer": 1,
                "why": "%steal measures time the guest wanted CPU but the hypervisor gave it to someone else. Idle guest + high steal means the VM is ready to run but isn't being scheduled — check CPU limits, reservations, shares, and ESXi CPU ready time for this VM (a limit set before migration is the classic cause). Tools (A) don't cause steal; ballooning (C) shows as swap/guest memory pressure, not steal; network (D) doesn't produce CPU steal.",
                "hint": "Steal time means the guest is waiting on the hypervisor, not on work.",
                "objectives": ["Interpret virtualization performance metrics", "Troubleshoot CPU scheduling contention"],
                "mins": 12,
                "evidence": ["Diagnoses CPU limit from %steal"]
            },
            {
                "id": "infra-virtualization-sc2",
                "title": "Snapshot Chain Eating the Datastore",
                "domain_id": "virtualization",
                "situation": "A VM's datastore usage has grown 300GB in a week although the guest reports only 40GB of new data. You find a chain of 11 snapshots, the oldest 8 months old. Deleting snapshots one by one is projected to take hours and the datastore is at 92%.",
                "prompt": "What is the safest remediation order?",
                "choices": [
                    "Delete the oldest snapshots first to reclaim the most space immediately",
                    "Power off the VM, then delete all snapshots at once",
                    "Consolidate: use 'Delete All' so the hypervisor merges the chain in one pass, after verifying backups and free space headroom",
                    "Clone the VM to a new datastore and delete the original"
                ],
                "answer": 2,
                "why": "'Delete All' collapses the entire delta chain into the base disk in a single consolidation pass, which is faster and safer than sequential deletes that each rewrite the chain (each intermediate delete risks a long, fragile merge). Verify a current backup first and confirm enough headroom, since consolidation needs working space. Deleting oldest-first (A) is the slowest path; powering off (B) adds downtime without changing the merge math; cloning (C) copies the bloat.",
                "hint": "Each per-snapshot delete rewrites the chain — think about merging it once.",
                "objectives": ["Manage VM snapshot lifecycle", "Recover datastore space safely"],
                "mins": 10,
                "evidence": ["Chooses single-pass consolidation"]
            }
        ],
        "data": [
            {
                "id": "infra-data-sc1",
                "title": "Backup That Can't Restore in Time",
                "domain_id": "data",
                "situation": "A file server holds 8TB. Full backups run weekly to tape, differentials nightly. The business RTO is 4 hours and RPO is 24 hours. During a drill, restoring the latest full plus six differentials took 11 hours. The backup admin proposes switching to incrementals to 'make backups faster'.",
                "prompt": "What backup change actually meets the 4-hour RTO?",
                "choices": [
                    "Switch nightly differentials to incrementals to reduce backup windows",
                    "Move to synthetic fulls or frequent fulls on disk-based storage so restore is a single image copy, and verify with timed restore drills",
                    "Keep the current scheme but buy a faster tape drive",
                    "Replicate the file server to a warm standby instead of backups"
                ],
                "answer": 1,
                "why": "The RTO problem is restore time, not backup time: incrementals (A) make restores SLOWER (full + every incremental). A disk-based synthetic or frequent full turns restore into one sequential copy that can hit 4 hours, and only timed drills prove it. A faster tape drive (C) helps marginally but tape seek times still dominate; replication (D) is great for DR but isn't a backup — it replicates corruption and gives no point-in-time recovery.",
                "hint": "Optimize the restore path, not the backup path — and notice what incrementals do to restores.",
                "objectives": ["Design backup schemes to RTO/RPO", "Distinguish backup from replication"],
                "mins": 12,
                "evidence": ["Identifies restore-time bottleneck"]
            },
            {
                "id": "infra-data-sc2",
                "title": "Tiering Cold Data Without Breaking Access",
                "domain_id": "data",
                "situation": "A 60TB NAS is 85% full. Analysis shows 70% of files haven't been touched in 18 months, but legal requires 7-year retention and users occasionally request old project files with a 24-hour SLA. The CFO won't approve buying another shelf of fast disk.",
                "prompt": "What storage strategy satisfies retention, access SLA, and budget?",
                "choices": [
                    "Compress everything in place and hope for 3:1 savings",
                    "Policy-based tiering: auto-move files untouched for 12+ months to cheaper object/archive storage, with transparent recall meeting the 24-hour SLA",
                    "Delete the oldest 30% and rely on legal to object if needed",
                    "Migrate the whole NAS to archive storage and accept slower access for everything"
                ],
                "answer": 1,
                "why": "Automated tiering keeps hot data on fast disk (preserving performance) while cold data lands on cheap capacity with recall inside the 24-hour SLA — exactly matching the access pattern and the retention mandate. Compression (A) is unpredictable and doesn't fix growth; deleting (C) violates legal retention; moving everything to archive (D) punishes daily users for cold data's sake.",
                "hint": "Match storage cost to access temperature, not to the whole dataset.",
                "objectives": ["Apply storage tiering policies", "Balance retention, SLA, and cost"],
                "mins": 10,
                "evidence": ["Designs tiering with SLA recall"]
            }
        ],
        "ops-sec": [
            {
                "id": "infra-opssec-sc1",
                "title": "SSH Keys Everywhere",
                "domain_id": "ops-sec",
                "situation": "An audit finds 40 engineers with permanent SSH access to production, keys never rotated in 3 years, several ex-employees' keys still authorized, and shared 'deploy' keys in a wiki. The team deploys 20 times a day and fears any change will break the pipeline.",
                "prompt": "What is the highest-leverage first step that doesn't halt deployments?",
                "choices": [
                    "Immediately revoke all keys and reissue per-engineer keys",
                    "Remove ex-employee keys, put the shared deploy key behind the CI system with a short-lived credential, and start key rotation with expiry",
                    "Move all SSH behind a VPN and call it done",
                    "Require hardware tokens for every SSH login starting tomorrow"
                ],
                "answer": 1,
                "why": "Kill the known-compromised credentials (ex-employees) and the highest-risk shared secret (the wiki key) first, scoping the deploy key to the CI system that actually uses it with short-lived credentials — this removes the worst exposure without touching the deploy flow. Mass revocation (A) halts deploys; a VPN (C) adds a perimeter but leaves the stolen keys valid inside; hardware tokens (D) are the end state but need a rollout plan, not a flag day.",
                "hint": "Sequence by risk: what's already compromised, and what secret is one wiki read away from abuse?",
                "objectives": ["Remediate credential sprawl", "Sequence security fixes by risk"],
                "mins": 12,
                "evidence": ["Prioritizes ex-employee and shared keys"]
            },
            {
                "id": "infra-opssec-sc2",
                "title": "Patch Window vs. Uptime SLA",
                "domain_id": "ops-sec",
                "situation": "A critical kernel CVE drops on Tuesday with public exploit code. Your fleet of 200 web servers carries a 99.95% uptime SLA (about 22 minutes of monthly downtime budget). The app can't drain connections gracefully — any reboot drops in-flight requests. Security demands patching within 48 hours.",
                "prompt": "How do you patch within 48 hours while honoring the SLA?",
                "choices": [
                    "Patch and reboot all 200 servers in one maintenance window at 2 AM",
                    "Rolling reboot in small batches behind the load balancer, draining each batch first, accepting the dropped in-flight requests on drained nodes as the cost of the window",
                    "Apply a live-patching service (e.g., kernel live patch) for the CVE now, then schedule the full reboot into the next normal window",
                    "Wait for the vendor's next scheduled patch bundle to avoid emergency churn"
                ],
                "answer": 2,
                "why": "Live patching closes the CVE exposure immediately with zero reboots, and deferring the real reboot to a planned window keeps the SLA intact. A flag-day reboot (A) blows the downtime budget and drops traffic; rolling reboots (B) still drop the in-flight requests the app can't drain; waiting (D) misses the 48-hour mandate with exploit code public.",
                "hint": "Separate 'stop the bleeding' from 'finish the surgery' — the CVE needs closing, not necessarily a reboot.",
                "objectives": ["Handle emergency patching under SLA", "Apply live patching appropriately"],
                "mins": 12,
                "evidence": ["Separates CVE closure from reboot"]
            }
        ],
        "systems-anatomy": [
            {
                "id": "infra-sysanat-sc1",
                "title": "Boot Process Anatomy: Where Did It Hang?",
                "domain_id": "systems-anatomy",
                "situation": "A Linux server powers on, shows the vendor logo, then sits at a black screen with a blinking cursor — no GRUB menu, no kernel messages. The admin has already reseated the RAM. The disk activity LED never blinks.",
                "prompt": "Using the boot sequence (firmware -> bootloader -> kernel -> init), where is the failure and what do you check?",
                "choices": [
                    "Kernel stage: boot a rescue image and rebuild the initramfs",
                    "Bootloader stage: firmware finished (logo shown) but GRUB never loaded — check boot device order, EFI boot entries, and whether the bootloader files exist",
                    "Init stage: systemd is hanging on a service; boot with systemd.unit=emergency.target",
                    "Hardware: the CPU is dead since nothing printed"
                ],
                "answer": 1,
                "why": "The vendor logo means firmware/POST completed; the disk LED staying dark and no GRUB menu means control never reached the bootloader — the failure is between firmware and bootloader. Check that the firmware is actually pointing at a bootable device (boot order, EFI NVRAM entries, GRUB files on the EFI partition). Kernel (A) and init (C) stages come later and would print messages; a dead CPU (D) wouldn't show the logo.",
                "hint": "Map each visible symptom to exactly one handoff in the boot chain.",
                "objectives": ["Trace the Linux boot sequence", "Localize boot failures by stage"],
                "mins": 12,
                "evidence": ["Places failure at firmware-to-bootloader handoff"]
            },
            {
                "id": "infra-sysanat-sc2",
                "title": "Linux I/O Stack: Slow Disk, Fast Disk",
                "domain_id": "systems-anatomy",
                "situation": "An app reads 1GB files. `hdparm`-style raw device reads hit 500 MB/s, but the app sees 80 MB/s. `iostat` shows high await and low %util on the device. The filesystem is ext4 with default mount options, and the app does small 4KB random reads.",
                "prompt": "Which layer of the I/O stack (app -> VFS -> page cache -> filesystem -> block layer -> driver -> device) best explains the gap?",
                "choices": [
                    "The device layer: the SSD is worn out and slow",
                    "The app/VFS layer: 4KB random reads defeat readahead and the page cache can't help first-touch data; the app should use larger sequential reads or mmap",
                    "The block layer: the I/O scheduler is misconfigured for SSDs",
                    "The filesystem: ext4 journaling is throttling reads"
                ],
                "answer": 1,
                "why": "Raw sequential device speed (500 MB/s) proves the hardware is fine — the app's 4KB random access pattern means every read is a seek-like operation with syscall overhead, and readahead/page cache can't prefetch randomly. The fix is at the app layer: bigger reads, sequential access, or mmap. The block scheduler (C) matters far less on SSDs; ext4 journaling (D) affects writes, not reads.",
                "hint": "The device proved itself fast — so which layer transforms the app's requests into something slow?",
                "objectives": ["Trace the Linux I/O stack", "Diagnose I/O pattern vs device capability"],
                "mins": 12,
                "evidence": ["Attributes gap to access pattern at app layer"]
            },
            {
                "id": "infra-sysanat-sc3",
                "title": "Hypervisor Flow: The Noisy Neighbor",
                "domain_id": "systems-anatomy",
                "situation": "Two VMs share a host. VM-A runs a latency-sensitive trading app; VM-B runs nightly batch compression. When VM-B's batch starts, VM-A's p99 latency triples, though VM-A's vCPU usage stays under 40% and memory is plentiful. CPU pinning is not in use.",
                "prompt": "Following the hypervisor scheduling flow, what is the most likely interference mechanism?",
                "choices": [
                    "VM-B is ballooning memory away from VM-A",
                    "Last-level cache and memory-bandwidth contention: VM-B's streaming workload evicts VM-A's cache lines, so VM-A stalls on memory despite idle vCPUs",
                    "VM-B's virtual disk I/O is saturating the shared datastore",
                    "The virtual switch is dropping VM-A's packets under load"
                ],
                "answer": 1,
                "why": "Idle vCPUs plus spiking latency with a streaming neighbor is the classic shared-cache/memory-bandwidth contention signature — the hypervisor schedules both fine, but VM-B's sequential streaming evicts VM-A's working set from the LLC, turning cache hits into DRAM stalls. Ballooning (A) would show guest memory pressure; datastore saturation (C) shows as disk await; vSwitch drops (D) show as packet loss, not CPU-idle latency.",
                "hint": "The vCPUs are idle — so what shared resource below the scheduler is exhausted?",
                "objectives": ["Explain hypervisor resource contention", "Diagnose noisy-neighbor cache effects"],
                "mins": 12,
                "evidence": ["Identifies LLC/memory-bandwidth contention"]
            },
            {
                "id": "infra-sysanat-sc4",
                "title": "Cloud Request Path: Where Did 300ms Go?",
                "domain_id": "systems-anatomy",
                "situation": "A user request to your cloud-hosted API takes 450ms; the app server logs show 120ms of processing. The path is: client -> CDN -> WAF -> load balancer -> app -> database. Each hop was 'fast when we built it' but nobody has measured per-hop since.",
                "prompt": "What is the disciplined way to attribute the missing ~330ms across the request path?",
                "choices": [
                    "Add more app servers; the app is probably queuing",
                    "Enable distributed tracing with per-hop spans (or at minimum synchronized access logs with request IDs) and read the waterfall before changing anything",
                    "Move the database to a bigger instance since DB is usually the bottleneck",
                    "Enable CDN caching for the API responses"
                ],
                "answer": 1,
                "why": "You cannot optimize what you haven't measured per hop — distributed tracing (or correlated request-ID logs) produces a waterfall showing exactly which of CDN/WAF/LB/app/DB owns the 330ms. Guessing app (A) or DB (C) scaling wastes money if the time is in TLS handshakes at the WAF; caching (D) changes semantics and may be wrong for the endpoint. Measure the path, then fix the slowest hop.",
                "hint": "The app already accounted for its 120ms — where's the receipt for the rest?",
                "objectives": ["Trace requests across cloud tiers", "Apply measure-before-optimize discipline"],
                "mins": 12,
                "evidence": ["Demands per-hop attribution first"]
            },
            {
                "id": "infra-sysanat-sc5",
                "title": "Storage I/O Journey: Write Latency Spike",
                "domain_id": "systems-anatomy",
                "situation": "A database on a SAN sees write latency jump from 2ms to 40ms every day at 14:00 for 30 minutes. Host CPU, memory, and network are flat. The SAN admin says array cache hit rate drops during the window. Nothing in the database changes at 14:00.",
                "prompt": "Tracing the write path (app -> filesystem -> HBA -> fabric -> array cache -> disks), where should you investigate?",
                "choices": [
                    "The app: add write-back caching in the database",
                    "Off-host: something else shares the SAN — a 14:00 backup or replication job is flooding array cache and forcing write-through to disk",
                    "The HBA: replace the fiber-channel card in the DB host",
                    "The filesystem: the journal is checkpointing at 14:00"
                ],
                "answer": 1,
                "why": "Host-side metrics are flat and the symptom is array cache hit rate collapsing on a fixed schedule — the write path is fine until the array, where a competing workload (backup snapshot, replication, another host's batch) evicts cache and forces destaging to spinning disk. Check SAN performance graphs for other initiators at 14:00. HBA (C) or journal (D) faults wouldn't follow a clock; app caching (A) papers over a shared-infrastructure problem.",
                "hint": "The host is innocent and the clock is suspicious — who else uses the array?",
                "objectives": ["Trace SAN write paths", "Identify shared-storage contention"],
                "mins": 12,
                "evidence": ["Correlates schedule with array cache eviction"]
            },
            {
                "id": "infra-sysanat-sc6",
                "title": "Packet Through a Virtual Switch",
                "domain_id": "systems-anatomy",
                "situation": "VM-A can't reach VM-B on the same host and VLAN, but both reach the physical network fine. The vSwitch port groups look correct. VM-A's ARP table has no entry for VM-B, and a packet capture on VM-B's vNIC shows zero incoming packets from VM-A.",
                "prompt": "Where in the virtual-switch path (source vNIC -> port -> vSwitch forwarding -> destination vNIC) is the packet being dropped?",
                "choices": [
                    "At the physical uplink: the upstream switch is blocking inter-VM traffic",
                    "Between source vNIC and the vSwitch, or in vSwitch policy: check promiscuous mode, MAC learning/security policy, and whether VM-A's vNIC is actually connected",
                    "At VM-B's guest firewall: it's dropping the packets silently",
                    "In the VLAN trunk: the VLAN tag is being stripped"
                ],
                "answer": 1,
                "why": "Both VMs reach the physical network, so uplinks and VLAN tagging work — and VM-B's vNIC sees nothing, ruling out its guest firewall (which would show arrivals in the capture). The drop is at the source side: a disconnected vNIC, a vSwitch security policy rejecting the MAC, or forged-transmit/MAC-change settings. ARP failing with no traffic arriving downstream localizes it before the vSwitch fabric.",
                "hint": "VM-B's capture is the witness — nothing arrives, so eliminate everything at or after arrival.",
                "objectives": ["Trace packets through virtual switches", "Apply vSwitch security policy knowledge"],
                "mins": 12,
                "evidence": ["Localizes drop to source-side vSwitch policy"]
            }
        ],
        "exam-strategy": [
            {
                "id": "infra-examstrategy-sc1",
                "title": "PBQ: Rebuild the Broken Service",
                "domain_id": "exam-strategy",
                "situation": "The exam presents a performance-based question: a terminal with a Linux VM where the web stack is down. You have `systemctl`, `journalctl`, `ss`, and config files. The clock shows 38 minutes left and 40 questions remaining, and this PBQ is marked as high-value.",
                "prompt": "What is the best exam-room strategy for this PBQ?",
                "choices": [
                    "Skip it entirely — PBQs take too long and the multiple-choice questions are safer points",
                    "Spend up to 10 focused minutes: check service status, read the journal error, verify ports with ss, fix the config, then move on regardless",
                    "Solve it completely no matter how long it takes, since it's high-value",
                    "Answer the remaining multiple-choice questions first, then return with whatever time is left"
                ],
                "answer": 1,
                "why": "PBQs carry heavy weight but have diminishing returns: a disciplined 10-minute triage (status -> logs -> ports -> config) captures most partial-credit checkpoints without cannibalizing 40 other questions. Skipping (A) forfeits high-value points; unlimited time (C) starves the rest of the exam; doing all MCQs first (D) risks leaving zero time for the PBQ's easy early checkpoints.",
                "hint": "Think in checkpoints and opportunity cost, not perfection.",
                "objectives": ["Manage PBQ time budget", "Apply systematic CLI triage"],
                "mins": 10,
                "evidence": ["Describes 10-minute PBQ triage flow"]
            },
            {
                "id": "infra-examstrategy-sc2",
                "title": "The 90-Second Multiple Choice",
                "domain_id": "exam-strategy",
                "situation": "You're 25 questions into a Cloud+ exam with 75 minutes left. A long scenario stem describes a company's storage growth, compliance needs, and budget, followed by four dense answer choices. You've already re-read the stem twice and two choices both look plausible.",
                "prompt": "What should you do right now?",
                "choices": [
                    "Keep re-reading until you're certain — accuracy beats speed",
                    "Flag it, pick your best instinct, and move on; return only if time remains after the first pass",
                    "Eliminate the two implausible choices and guess randomly between the remaining two",
                    "Skip it with no answer to avoid a wrong-answer penalty"
                ],
                "answer": 1,
                "why": "Banked time is the scarcest exam resource: flag-and-move preserves momentum and your subconscious keeps working on it, while a second pass with fresh eyes often resolves the ambiguity. Re-reading (A) burns minutes for marginal gain; there's no wrong-answer penalty on CompTIA exams so (D) is pure loss; and (C) is fine as the instinct pick inside the flag-and-move, not as the whole strategy.",
                "hint": "The exam rewards completed passes over perfect single questions.",
                "objectives": ["Apply flag-and-move technique", "Manage exam pacing"],
                "mins": 8,
                "evidence": ["Explains pacing trade-off"]
            },
            {
                "id": "infra-examstrategy-sc3",
                "title": "Troubleshooting Methodology Under Pressure",
                "domain_id": "exam-strategy",
                "situation": "A PBQ drops you into a broken three-tier app: users can't log in. You have 8 minutes budgeted. Logs show the web tier returning 500s, the app tier logging 'connection refused' to the database, and the database host responding to ping.",
                "prompt": "Following a top-down vs bottom-up methodology, what is the correct next step?",
                "choices": [
                    "Restart the database — connection refused means it's down",
                    "Bottom-up: verify the DB service is listening (ss/netstat on the DB host), then check firewall rules and credentials layer by layer",
                    "Top-down: rewrite the web tier's connection string first since 500s start there",
                    "Check DNS resolution between tiers"
                ],
                "answer": 1,
                "why": "The evidence localizes the break between app and DB ('connection refused' = reached host, nothing listening or blocked). Bottom-up verification — is the DB process listening on the expected port, then is the path clear (firewall), then are credentials valid — tests each layer exactly once. Restarting (A) is a guess that destroys evidence; starting at the web tier (C) works the wrong end; DNS (D) would give resolution errors, not connection refused.",
                "hint": "'Connection refused' already tells you the network path works — what's the next layer?",
                "objectives": ["Apply structured troubleshooting methodology", "Interpret connection error semantics"],
                "mins": 10,
                "evidence": ["Walks bottom-up from connection refused"]
            },
            {
                "id": "infra-examstrategy-sc4",
                "title": "Reading Logs Against the Clock",
                "domain_id": "exam-strategy",
                "situation": "A PBQ gives you a 400-line log file and asks which service caused an outage. Timestamps show errors cascading across web, cache, and database services within 90 seconds. You have 6 minutes left on your PBQ budget.",
                "prompt": "How do you find the root cause fast?",
                "choices": [
                    "Read the log top to bottom carefully",
                    "Jump to the FIRST error in chronological order — cascades propagate forward, so the earliest failure is the likely root cause",
                    "Search for the most frequent error — volume indicates the culprit",
                    "Check the last lines — the final error is what killed the system"
                ],
                "answer": 1,
                "why": "Cascading failures propagate forward in time: the web tier's errors at 10:02 are effects of the database's first failure at 10:00. The earliest anomaly is the root-cause candidate; everything after is fallout. Reading linearly (A) wastes the budget; frequency (C) just measures which service complains loudest; the last line (D) is the final victim, not the cause.",
                "hint": "Causes precede effects — sort by time, not by volume.",
                "objectives": ["Analyze cascading log failures", "Identify root cause chronologically"],
                "mins": 8,
                "evidence": ["Finds earliest error as root cause"]
            },
            {
                "id": "infra-examstrategy-sc5",
                "title": "Parsing the Scenario Stem",
                "domain_id": "exam-strategy",
                "situation": "A question stem is a full paragraph: a hospital needs a new backup system; HIPAA compliance is mentioned; RTO 2 hours; the WAN link is 100 Mbps; the answer choices are four backup architectures. You've seen similar questions where one detail is a distractor.",
                "prompt": "What is the reliable way to extract what the question actually tests?",
                "choices": [
                    "Read the last sentence first to find the actual question, then scan the stem only for constraints that discriminate between choices",
                    "Memorize every detail — the exam punishes missed facts",
                    "Pick the choice mentioning HIPAA since compliance was emphasized",
                    "Choose the most technically advanced architecture"
                ],
                "answer": 0,
                "why": "The final sentence defines the decision being asked; the stem's job is to supply discriminating constraints (RTO 2h over a 100 Mbps WAN rules out off-site full restores). Reading question-first prevents distractor details (HIPAA matters for encryption, not for the architecture choice here) from anchoring you. Memorizing everything (B) wastes time; keyword-matching (C) and tech-shine (D) are classic wrong-answer traps.",
                "hint": "The question is at the end; the constraints are the filter.",
                "objectives": ["Parse scenario stems efficiently", "Identify discriminating constraints"],
                "mins": 8,
                "evidence": ["Reads question first, filters constraints"]
            },
            {
                "id": "infra-examstrategy-sc6",
                "title": "Command-Line PBQ: Fix the Network",
                "domain_id": "exam-strategy",
                "situation": "PBQ: a Linux VM has no network. `ip addr` shows the interface UP with no IP address. `ip route` is empty. There's a DHCP server on the network and the exam gives you root. You've budgeted 7 minutes.",
                "prompt": "What is the fastest correct fix sequence?",
                "choices": [
                    "Assign a static IP with ip addr add, add a default route, and write resolv.conf",
                    "Restart the whole VM and hope DHCP works on boot",
                    "Run dhclient (or systemctl restart the DHCP client / NetworkManager) to request a lease, then verify with ip addr",
                    "Edit /etc/network/interfaces and reboot the networking service twice"
                ],
                "answer": 2,
                "why": "Interface UP with no address and an empty route table on a DHCP network means the DHCP client never completed — re-running dhclient (or restarting NetworkManager/systemd-networkd) requests a fresh lease in seconds, which is the minimal fix matching the environment. Static config (A) works but fights the stated DHCP design and takes longer; rebooting (B/D) wastes minutes on an 7-minute budget.",
                "hint": "Match the fix to the environment's design: DHCP network, DHCP-shaped symptom.",
                "objectives": ["Troubleshoot Linux networking in PBQs", "Use DHCP client tools"],
                "mins": 10,
                "evidence": ["Restores DHCP lease via dhclient"]
            },
            {
                "id": "infra-examstrategy-sc7",
                "title": "When Two Answers Both Work",
                "domain_id": "exam-strategy",
                "situation": "A scenario asks for the BEST way to secure management access to 50 switches. Choice B (SSH with key auth) and choice D (a jump host with MFA) are both genuinely good practices. You've narrowed it to these two with 60 seconds spent.",
                "prompt": "How do you break the tie?",
                "choices": [
                    "Pick the longer, more detailed answer — exams reward completeness",
                    "Re-read the stem for scale/scope words (50 switches, management access): the BEST answer is the one that scales and centralizes — the jump host with MFA",
                    "Pick B because SSH keys are the more fundamental skill",
                    "Always pick the answer mentioning MFA — security questions want MFA"
                ],
                "answer": 1,
                "why": "CompTIA 'BEST/MOST' questions are decided by the stem's scope constraints: at 50 switches, per-device SSH keys become a management nightmare while a jump host centralizes access control, auditing, and MFA in one place. Length (A) and keyword superstitions (C, D) are traps; the tiebreaker is always which choice the stem's scale and constraints uniquely favor.",
                "hint": "BEST means 'best given the stem's scale' — whose advantage grows with 50 devices?",
                "objectives": ["Answer BEST/MOST questions", "Weigh scalability in security design"],
                "mins": 8,
                "evidence": ["Uses scale constraint as tiebreaker"]
            },
            {
                "id": "infra-examstrategy-sc8",
                "title": "The Final 15 Minutes",
                "domain_id": "exam-strategy",
                "situation": "Fifteen minutes remain. You have 6 flagged questions, one half-finished PBQ (you fixed the service but didn't verify), and 3 unanswered questions at the end you never reached. Your first-pass instinct answers are marked on the flagged ones.",
                "prompt": "What is the optimal order of operations?",
                "choices": [
                    "Finish the PBQ verification first, then flagged questions, then the unanswered",
                    "Answer the 3 unanswered questions first (a blank is a guaranteed zero), then the PBQ verification, then flagged review with remaining time",
                    "Review all flagged questions carefully — they're the ones you were unsure about",
                    "Redo the PBQ from scratch to make sure the fix was right"
                ],
                "answer": 1,
                "why": "Expected-value ordering: unanswered questions are guaranteed zeros — even 30-second instinct answers have positive expected value. The PBQ verification is a cheap checkpoint for partial credit. Flagged review comes last because first instincts are statistically strong and re-litigating risks changing right answers to wrong ones under time pressure. Redoing the PBQ (D) is the worst time investment.",
                "hint": "Rank by expected points per minute: zeros first, cheap verifications second.",
                "objectives": ["Optimize end-of-exam triage", "Apply expected-value thinking"],
                "mins": 8,
                "evidence": ["Sequences blanks, PBQ check, flags"]
            }
        ],
        "capacity-planning": [
            {
                "id": "infra-capplan-sc1",
                "title": "Right-Sizing an Over-Provisioned Fleet",
                "domain_id": "capacity-planning",
                "situation": "Your 120-VM fleet averages 18% CPU and 35% memory utilization. Finance flags the cloud bill; engineering fears performance regressions if you downsize. The workloads are a mix of steady web servers and spiky batch jobs, and you have 90 days of per-VM metrics.",
                "prompt": "What is the defensible right-sizing approach?",
                "choices": [
                    "Downsize every VM one size and watch for complaints",
                    "Downsize based on p95 (not average) utilization per VM, keep batch jobs on burstable classes, and stage the change with rollback per workload group",
                    "Do nothing — headroom is the point of the cloud",
                    "Move everything to the smallest instance size to maximize savings"
                ],
                "answer": 1,
                "why": "Averages hide peaks: p95 sizing preserves headroom for real spikes while still capturing most of the waste, burstable classes match spiky batch economics, and staged rollout with rollback answers engineering's regression fear with evidence. Blanket downsizing (A/D) risks peak-hour outages; doing nothing (C) ignores the data you already paid to collect.",
                "hint": "Averages lie about peaks — which percentile tells the truth about needed headroom?",
                "objectives": ["Right-size using utilization percentiles", "Stage changes with rollback"],
                "mins": 12,
                "evidence": ["Builds p95-based sizing plan"]
            },
            {
                "id": "infra-capplan-sc2",
                "title": "Forecasting Holiday Traffic",
                "domain_id": "capacity-planning",
                "situation": "Last Black Friday, traffic was 6x normal and the site degraded at 4x. This year marketing expects 8x with a new product launch. You have three years of hourly traffic data showing 40% year-over-year peak growth. Infrastructure lead time for new capacity is 3 weeks.",
                "prompt": "How much capacity do you provision, and when?",
                "choices": [
                    "Provision for 8x now — marketing's number is the requirement",
                    "Provision for 10-12x (8x forecast plus headroom), completed 4+ weeks before the event, validated with a load test at the target",
                    "Provision for 6x like last year and auto-scale the rest",
                    "Wait until the week before, then provision based on pre-sale numbers"
                ],
                "answer": 1,
                "why": "Forecast (8x, consistent with 40% YoY growth on 6x) plus explicit headroom (failures happen at peak) gives 10-12x; finishing 4+ weeks early beats the 3-week lead time and leaves room for the load test that actually proves the number. Marketing's number (A) has no safety margin; 6x (C) repeats last year's degradation; waiting (D) collides with lead time.",
                "hint": "Forecast plus headroom, minus lead time — what date does that math give you?",
                "objectives": ["Forecast demand with growth trends", "Plan provisioning lead times"],
                "mins": 12,
                "evidence": ["Computes forecast + headroom + lead time"]
            },
            {
                "id": "infra-capplan-sc3",
                "title": "Finding the Real Bottleneck",
                "domain_id": "capacity-planning",
                "situation": "Checkout latency doubled after a traffic increase. CPU is at 45%, memory at 60%, disk await is normal, but the app server's connection pool to the database is saturated and DB CPU is at 95% with lock waits climbing.",
                "prompt": "Where is the bottleneck, and what proves it?",
                "choices": [
                    "The app servers — add more to spread the load",
                    "The database: saturated connection pool plus 95% DB CPU with lock waits shows the DB can't serve the offered load; app CPU is idle because threads wait on the DB",
                    "The network — latency doubled, so packets are being lost",
                    "The disk — databases are always disk-bound"
                ],
                "answer": 1,
                "why": "The saturated pool and 95% DB CPU with lock waits are direct evidence the database is the constraint; app servers at 45% CPU are starved, not overloaded — adding app servers (A) just adds more waiters to the same saturated pool. Disk await is normal (ruling out D) and there's no packet-loss evidence (C). Fix the DB: query optimization, indexing, read replicas, or connection pooling.",
                "hint": "Which component's queue is full while the others sit idle?",
                "objectives": ["Identify bottlenecks from metrics", "Avoid scaling the wrong tier"],
                "mins": 12,
                "evidence": ["Traces saturation to database tier"]
            },
            {
                "id": "infra-capplan-sc4",
                "title": "Scale Up or Scale Out?",
                "domain_id": "capacity-planning",
                "situation": "A stateful legacy application is hitting CPU limits on its single large VM. The vendor supports active-passive clustering with a 30-second failover. Rewriting for horizontal scale would take 6 months. Traffic grows 10% per quarter.",
                "prompt": "What scaling decision fits the constraints?",
                "choices": [
                    "Scale out immediately with a load balancer — horizontal is always better",
                    "Scale up (bigger VM) now for headroom, and run the vendor's active-passive cluster for availability; revisit scale-out with the rewrite",
                    "Do nothing and let the vendor handle performance",
                    "Shard the database across multiple VMs this weekend"
                ],
                "answer": 1,
                "why": "The app is stateful and the vendor only supports active-passive — scale-out (A) would break session state and void support, and sharding (D) is a rewrite in disguise. Scaling up buys quarters of headroom at 10% growth while the supported cluster covers availability; the real scale-out waits for the 6-month rewrite. Doing nothing (C) lets growth eat the remaining headroom.",
                "hint": "What does the vendor actually support, and what does statefulness forbid?",
                "objectives": ["Choose scale-up vs scale-out", "Respect application architecture constraints"],
                "mins": 12,
                "evidence": ["Justifies scale-up given stateful vendor limits"]
            },
            {
                "id": "infra-capplan-sc5",
                "title": "Cost vs Performance: The Database Tier",
                "domain_id": "capacity-planning",
                "situation": "The analytics database runs on premium SSD storage at $4,000/month. Profiling shows 90% of queries hit the last 30 days of data; older data is queried rarely but must stay online per policy. Moving cold data to standard storage cuts the bill to $1,200/month with a 3x latency hit on cold queries.",
                "prompt": "What is the right cost-performance trade?",
                "choices": [
                    "Keep everything on premium SSD — performance is never worth risking",
                    "Tier by age: last 90 days on premium SSD, older data on standard storage; 90% of queries keep full speed and the bill drops ~60%",
                    "Move everything to standard storage and accept the latency",
                    "Delete data older than a year to shrink the bill"
                ],
                "answer": 1,
                "why": "Access temperature maps cleanly to storage tiers: the hot 30-day working set keeps premium performance for 90% of queries while cold data's 3x latency is invisible in practice since it's rarely touched — and policy retention is preserved. All-premium (A) wastes money on cold bytes; all-standard (C) punishes the hot path; deletion (D) violates retention policy.",
                "hint": "Which queries pay the latency price, and how often do they run?",
                "objectives": ["Trade cost against performance", "Tier data by access temperature"],
                "mins": 10,
                "evidence": ["Designs age-based storage tiering"]
            },
            {
                "id": "infra-capplan-sc6",
                "title": "Alert Thresholds That Don't Cry Wolf",
                "domain_id": "capacity-planning",
                "situation": "The ops team gets 200 CPU alerts a week; 95% are transient spikes that self-resolve. Real incidents have been missed because engineers mute the channel. The service can tolerate 5 minutes of high CPU, but sustained 85%+ for 15 minutes precedes outages.",
                "prompt": "How do you set thresholds that catch real problems without the noise?",
                "choices": [
                    "Lower the threshold to 70% so nothing is ever missed",
                    "Alert on sustained 85%+ for 15 minutes (matching the known failure precursor), and convert transient spikes to a dashboard, not pages",
                    "Disable CPU alerts entirely and rely on user complaints",
                    "Page on any single 90% reading to be safe"
                ],
                "answer": 1,
                "why": "Alert on the failure precursor you actually observed (85% for 15 min), not on raw spikes — duration-based thresholds filter transients while catching the real pattern, and dashboards preserve visibility without paging. Lowering (A) or single-reading (D) thresholds multiplies the noise that caused the muting; disabling (C) blinds you. Alert fatigue is a reliability bug; fix the signal.",
                "hint": "You know the exact precursor pattern — alert on that, not on CPU in general.",
                "objectives": ["Design actionable alert thresholds", "Combat alert fatigue"],
                "mins": 10,
                "evidence": ["Sets duration-based threshold from observed precursor"]
            }
        ],
        "hybrid-cloud": [
            {
                "id": "infra-hybrid-sc1",
                "title": "Where Does This Workload Live?",
                "domain_id": "hybrid-cloud",
                "situation": "A hospital runs a patient-scheduling app (steady load, PHI data, strict audit rules) and a research analytics pipeline (spiky, de-identified data, needs 200 GPUs for 6 hours weekly). The CIO wants a hybrid strategy but the team is split: 'everything on-prem for compliance' vs 'everything in cloud for agility'.",
                "prompt": "What workload placement best serves both requirements?",
                "choices": [
                    "Everything on-prem: compliance demands it",
                    "Everything in cloud: agility demands it",
                    "Scheduling stays on-prem (steady, PHI, audit-friendly); analytics bursts to cloud GPUs (spiky, de-identified, pay-per-use)",
                    "Split both workloads 50/50 across on-prem and cloud for redundancy"
                ],
                "answer": 2,
                "why": "Placement follows workload shape: the steady PHI system gains nothing from cloud elasticity and stays where audit controls exist; the spiky GPU pipeline would force buying 200 idle GPUs on-prem, while cloud pay-per-use matches its 6-hour weekly shape and the data is de-identified. Absolutist options (A/B) optimize one workload at the other's expense; 50/50 (D) doubles operational burden with no rationale.",
                "hint": "Match each workload's shape (steady vs spiky, PHI vs de-identified) to the platform's economics.",
                "objectives": ["Place workloads by shape and sensitivity", "Evaluate hybrid economics"],
                "mins": 12,
                "evidence": ["Maps workload traits to placement"]
            },
            {
                "id": "infra-hybrid-sc2",
                "title": "Migration Wave Sequencing",
                "domain_id": "hybrid-cloud",
                "situation": "You're migrating 80 applications to cloud over a year. The inventory: 10 stateless web apps, 30 internal tools with local file dependencies, 25 tightly-coupled legacy client-server apps, and 15 regulated apps requiring re-certification after any move. Leadership wants 'quick wins' in Q1.",
                "prompt": "What wave order minimizes risk while showing early progress?",
                "choices": [
                    "Migrate the 25 legacy client-server apps first — hardest first",
                    "Wave 1: the 10 stateless web apps (easy wins, prove the pipeline); Wave 2: internal tools after remediating file dependencies; legacy and regulated last with dedicated plans",
                    "Migrate all 80 in parallel to finish in one quarter",
                    "Start with the 15 regulated apps to get compliance out of the way"
                ],
                "answer": 1,
                "why": "Stateless web apps are low-risk, high-learning migrations that prove the landing zone, networking, and runbooks — the 'quick wins' leadership wants. Internal tools need dependency remediation first; legacy coupling and re-certification are the long poles that deserve dedicated waves, not rushed starts. Hardest-first (A) risks a year-one failure; parallel (C) exceeds team capacity; regulated-first (D) burns the timeline on certification.",
                "hint": "Which wave teaches the team the migration pattern at the lowest blast radius?",
                "objectives": ["Sequence migration waves", "Balance quick wins with risk"],
                "mins": 12,
                "evidence": ["Orders waves by risk and learning"]
            },
            {
                "id": "infra-hybrid-sc3",
                "title": "Connectivity: VPN vs Direct Link",
                "domain_id": "hybrid-cloud",
                "situation": "The datacenter must connect to the cloud region for a hybrid database cluster with synchronous replication. The replication needs 2 Gbps sustained and under 5ms latency variance. A site-to-site VPN over the 1 Gbps internet link is already configured and 'works fine' for admin traffic.",
                "prompt": "What connectivity choice meets the replication requirements?",
                "choices": [
                    "Keep the VPN — it's already working and free",
                    "Provision a dedicated private interconnect (Direct Connect / ExpressRoute class) sized for 2+ Gbps with an SLA, and keep the VPN as backup",
                    "Bond two VPN tunnels for 2 Gbps",
                    "Switch replication to asynchronous so the VPN suffices"
                ],
                "answer": 1,
                "why": "Synchronous replication with tight latency variance needs deterministic private connectivity — a dedicated interconnect provides committed bandwidth and an SLA, which internet VPNs can't guarantee (jitter kills sync replication). Bonded VPNs (C) add bandwidth but not latency determinism; async replication (D) changes the RPO contract silently; the existing VPN (A) meets admin needs, not replication needs.",
                "hint": "Synchronous replication fails on jitter, not just on average speed.",
                "objectives": ["Select hybrid connectivity", "Match network SLA to replication mode"],
                "mins": 10,
                "evidence": ["Requires dedicated link for sync replication"]
            },
            {
                "id": "infra-hybrid-sc4",
                "title": "Identity Federation Across the Divide",
                "domain_id": "hybrid-cloud",
                "situation": "Engineers now manage resources both on-prem (Active Directory) and in two cloud providers. They're juggling three sets of credentials; helpdesk tickets for password resets doubled. Security found shared admin accounts in the cloud consoles. The CISO mandates MFA everywhere and no standing cloud admin credentials.",
                "prompt": "What identity architecture fixes this?",
                "choices": [
                    "Create matching local accounts in each cloud with strong passwords",
                    "Federate: AD as the identity provider via SAML/OIDC to both clouds, enforce MFA at the IdP, and replace standing admin credentials with just-in-time elevation",
                    "Give everyone the shared admin accounts but add MFA to them",
                    "Sync passwords from AD to the clouds nightly"
                ],
                "answer": 1,
                "why": "Federation gives one identity, one MFA enforcement point, and no cloud-local passwords to phish or share — plus JIT elevation eliminates the standing admin credentials the CISO banned. Mirrored accounts (A) triple the credential sprawl; shared admins with MFA (C) still share the credential; password sync (D) propagates AD passwords into two more breach surfaces.",
                "hint": "One identity, enforced once — where should the MFA decision live?",
                "objectives": ["Design federated hybrid identity", "Eliminate standing credentials"],
                "mins": 12,
                "evidence": ["Designs SAML/OIDC federation with JIT admin"]
            },
            {
                "id": "infra-hybrid-sc5",
                "title": "Data Gravity Pulls Back",
                "domain_id": "hybrid-cloud",
                "situation": "The team moved analytics compute to the cloud but left the 40TB data warehouse on-prem. Every nightly job pulls 3TB across the interconnect, jobs miss their SLA, and egress/transfer costs spiked. The architect suggests 'just get a bigger pipe'.",
                "prompt": "What actually solves the data-gravity problem?",
                "choices": [
                    "Buy a bigger interconnect — bandwidth fixes everything",
                    "Move the compute to the data or the data to the compute: replicate the warehouse to cloud storage near the analytics cluster (or run analytics on-prem)",
                    "Compress the 3TB transfer to make it fit the window",
                    "Run the jobs less often"
                ],
                "answer": 1,
                "why": "Data gravity means the 40TB dataset dictates placement — compute must sit next to the data or the data must move once (replication) instead of 3TB nightly forever. A bigger pipe (A) treats the symptom at recurring cost; compression (C) is marginal against terabytes; reducing frequency (D) degrades the business SLA. Co-locate compute and data, then the transfer problem disappears.",
                "hint": "The 3TB moves every night — what if it only had to move once?",
                "objectives": ["Apply data gravity principles", "Co-locate compute with data"],
                "mins": 10,
                "evidence": ["Proposes one-time replication over nightly transfer"]
            },
            {
                "id": "infra-hybrid-sc6",
                "title": "DR Across Clouds",
                "domain_id": "hybrid-cloud",
                "situation": "Primary runs in Cloud A (us-east). The board wants DR that survives a full Cloud A regional failure, with RTO 4 hours and RPO 1 hour for the order system. The team proposes warm standby in Cloud A us-west — 'different region, same cloud, half the work'.",
                "prompt": "Does the us-west plan meet the requirement, and if not, what does?",
                "choices": [
                    "Yes — different region satisfies DR",
                    "No: same-cloud DR shares control-plane and vendor-wide failure modes; use warm standby in Cloud B with cross-cloud replication and tested failover runbooks",
                    "No — but active-active across Cloud A regions is enough",
                    "Yes, as long as backups are copied to us-west"
                ],
                "answer": 1,
                "why": "The requirement is surviving a Cloud A regional failure — but region-wide cloud incidents (control plane, IAM, DNS) routinely span regions of the same provider. True isolation needs a second provider (Cloud B) with independent control plane, plus replication that actually meets RPO 1h and runbooks tested against the 4h RTO. Same-cloud options (A/C) and backups alone (D, which can't meet a 4h RTO restore) miss the failure mode.",
                "hint": "What failures take down two regions of one cloud at once?",
                "objectives": ["Design multi-cloud DR", "Evaluate failure-domain independence"],
                "mins": 12,
                "evidence": ["Rejects same-cloud DR for shared control plane"]
            }
        ],
        "automation-iaac": [
            {
                "id": "infra-automation-sc1",
                "title": "Should This Be Automated?",
                "domain_id": "automation-iaac",
                "situation": "A senior engineer wants to automate the quarterly firewall rule review: it takes 4 hours, involves judgment calls about business justification, and the rules change based on audit findings. Meanwhile, VM provisioning (30 min, 40x/month, identical steps) is still manual and error-prone.",
                "prompt": "Where should automation effort go first?",
                "choices": [
                    "Automate the firewall review — senior work deserves automation",
                    "Automate VM provisioning first: high frequency x consistent steps x current errors = the best ROI; assist (not replace) the judgment-heavy firewall review",
                    "Automate both in parallel",
                    "Automate neither — automation always introduces risk"
                ],
                "answer": 1,
                "why": "Automation ROI = frequency x consistency x error cost. Provisioning (40x/month, identical, error-prone) is the textbook target; the firewall review is infrequent, judgment-heavy, and variable — automate the data-gathering around it but keep the human decision. Automating judgment work first (A) encodes bad decisions at speed; parallel (C) splits focus; (D) ignores the provisioning errors already costing the team.",
                "hint": "Multiply frequency by consistency — which task scores higher?",
                "objectives": ["Evaluate automation candidates", "Calculate automation ROI"],
                "mins": 10,
                "evidence": ["Ranks provisioning over review by ROI"]
            },
            {
                "id": "infra-automation-sc2",
                "title": "The Script That Worked Twice",
                "domain_id": "automation-iaac",
                "situation": "A deployment script creates a VM, attaches a disk, and installs the app. Run once, it works. Run twice (after a partial failure), it creates a duplicate VM and fails attaching the disk. The team now 'just knows' to clean up manually before re-running.",
                "prompt": "What principle is violated, and what is the fix?",
                "choices": [
                    "The script needs more logging",
                    "Idempotency: the script must check current state first (VM exists? disk attached? app installed?) and converge toward desired state instead of blindly executing steps",
                    "The script needs to run faster so partial failures don't happen",
                    "Manual cleanup is fine — document it in the runbook"
                ],
                "answer": 1,
                "why": "Non-idempotent scripts turn every retry into a new mess — the fix is state checks before each action so re-runs converge instead of duplicating. Logging (A) observes the problem without fixing it; speed (C) doesn't prevent partial failures; manual cleanup (D) institutionalizes the fragility. Idempotency is what makes automation safe to retry, which is the whole point of automating recovery.",
                "hint": "What should the second run do differently from the first?",
                "objectives": ["Apply idempotency", "Design retry-safe automation"],
                "mins": 10,
                "evidence": ["Adds state checks for convergence"]
            },
            {
                "id": "infra-automation-sc3",
                "title": "State File Showdown",
                "domain_id": "automation-iaac",
                "situation": "Two engineers run Terraform against the same environment from their laptops. After a week, `terraform plan` shows it wants to destroy and recreate the production database — neither engineer changed the DB config. The state file lives on a shared drive with no locking.",
                "prompt": "What went wrong, and what is the correct state management?",
                "choices": [
                    "Terraform is buggy with databases; manage the DB manually instead",
                    "Concurrent runs with an unlocked, shared state file caused state drift/corruption; move to remote state backend with locking (e.g., S3 + DynamoDB / Terraform Cloud) and one pipeline",
                    "Delete the state file and re-import everything",
                    "Have the engineers coordinate over chat before running Terraform"
                ],
                "answer": 1,
                "why": "Without locking, two writers interleave state updates — each engineer's local run bases its plan on a stale/corrupted view, producing phantom destroy plans. Remote state with locking serializes access and makes the state the single source of truth; running through one CI pipeline removes the laptop variance. Manual management (A) abandons IaC; re-import (C) is painful and doesn't prevent recurrence; chat coordination (D) doesn't scale and already failed.",
                "hint": "Two writers, no lock — what happens to the shared record of truth?",
                "objectives": ["Manage Terraform state safely", "Implement state locking"],
                "mins": 12,
                "evidence": ["Moves to locked remote state + pipeline"]
            },
            {
                "id": "infra-automation-sc4",
                "title": "Secrets in the Repo",
                "domain_id": "automation-iaac",
                "situation": "A code search finds a production database password in a Terraform variables file committed 6 months ago, plus an API key in a CI log. The repo is private 'so it's fine' according to the team. The password hasn't been rotated since.",
                "prompt": "What is the correct remediation sequence?",
                "choices": [
                    "Delete the commit from git history and move on",
                    "Rotate the exposed credentials immediately, purge them from history, move secrets to a vault with dynamic/short-lived credentials, and scan for other exposures",
                    "Make the repo more private with stricter access controls",
                    "Rotate the password next quarter during the scheduled rotation"
                ],
                "answer": 1,
                "why": "Exposed secrets are compromised secrets — rotation comes FIRST because history rewrites don't un-expose anything (clones and logs already escaped). Then purge history, move to a secrets manager with short-lived dynamic credentials so future leaks self-expire, and scan for more. History surgery alone (A) leaves the live password valid; tighter repo ACLs (C) don't revoke what's out; waiting (D) leaves a known-compromised credential active.",
                "hint": "The secret has been readable for 6 months — what must happen before any cleanup matters?",
                "objectives": ["Remediate secret exposure", "Implement secrets management"],
                "mins": 12,
                "evidence": ["Sequences rotate-first remediation"]
            },
            {
                "id": "infra-automation-sc5",
                "title": "Rollback Plan for the Big Apply",
                "domain_id": "automation-iaac",
                "situation": "Friday 4 PM: a Terraform apply will replace 30 production VMs with a new image containing an OS upgrade. The plan looks clean. The change window is 2 hours and the team has no tested rollback — 'we can just re-apply the old config if needed'.",
                "prompt": "What should happen before anyone approves this apply?",
                "choices": [
                    "Approve it — the plan is clean and re-apply is a valid rollback",
                    "Require: a tested rollback (previous image kept bootable, data backup verified), staged rollout (canary group first), and a go/no-go checkpoint — or defer to Monday",
                    "Apply it now but have everyone on video call",
                    "Skip the OS upgrade entirely to avoid risk"
                ],
                "answer": 1,
                "why": "'Re-apply the old config' is not a rollback plan — re-applying takes as long as the forward change, may not restore data state, and is untested under pressure. A real plan keeps the old image bootable, verifies backups, rolls in stages with a canary, and defines the abort criteria upfront. Friday 4 PM with a 2-hour window and no plan is how outages become weekend outages. More eyes (C) don't create a plan; skipping (D) avoids this risk by accepting all future CVE risk.",
                "hint": "How long does the 'rollback' actually take, and has anyone ever run it?",
                "objectives": ["Plan IaC rollbacks", "Stage risky applies safely"],
                "mins": 12,
                "evidence": ["Defines tested rollback + canary criteria"]
            },
            {
                "id": "infra-automation-sc6",
                "title": "GitOps Gone Sideways",
                "domain_id": "automation-iaac",
                "situation": "The team adopted GitOps: git is the source of truth, an agent syncs the cluster. But engineers keep `kubectl apply`-ing hotfixes directly 'just this once', and now git and the cluster disagree. The agent is set to auto-sync, and last night it reverted a hotfix that was keeping payments up.",
                "prompt": "How do you restore GitOps discipline without breaking the on-call's ability to respond?",
                "choices": [
                    "Disable auto-sync so hotfixes survive",
                    "Keep auto-sync; require hotfixes to go through git (even expedited PRs), make the agent's diff visible/alerting, and give on-call a documented emergency git path",
                    "Let engineers keep using kubectl and sync git from the cluster periodically",
                    "Remove the GitOps agent and go back to manual kubectl"
                ],
                "answer": 1,
                "why": "GitOps only works if git is the single writer — every kubectl hotfix is a fork of the truth that auto-sync will eventually clobber (as payments learned). The answer isn't disabling sync (A) but making the git path fast enough for emergencies: expedited PRs, visible diffs, and a practiced emergency flow. Syncing git from the cluster (C) inverts the model; removing the agent (D) surrenders the consistency GitOps bought.",
                "hint": "The agent did exactly what it was told — so which writer broke the contract?",
                "objectives": ["Enforce GitOps discipline", "Handle emergency changes in GitOps"],
                "mins": 12,
                "evidence": ["Routes hotfixes through git with expedited path"]
            },
            {
                "id": "infra-automation-sc7",
                "title": "Testing the Untestable Infra Code",
                "domain_id": "automation-iaac",
                "situation": "The Terraform modules manage production networking. There are no tests — 'you can't test infrastructure'. Last month a module change opened an overly broad security group in production. The team wants tests but fears slowing down delivery.",
                "prompt": "What testing strategy fits infrastructure code without grinding delivery to a halt?",
                "choices": [
                    "No tests — manual review is enough for infra code",
                    "Layered: static analysis + policy-as-code checks (e.g., no 0.0.0.0/0 ingress) on every PR, plan-output review, and ephemeral-environment smoke tests for network modules",
                    "Full production mirror environment for every PR",
                    "Only test after deploying to production and watching metrics"
                ],
                "answer": 1,
                "why": "Policy-as-code on every PR would have caught the 0.0.0.0/0 rule in seconds at near-zero cost; plan review catches logic errors; ephemeral environments validate the risky modules without a permanent mirror. Manual review alone (A) already failed; a full mirror per PR (C) is prohibitively slow/expensive; testing in prod (D) is how the incident happened. Fast cheap gates on every change, expensive gates where risk justifies them.",
                "hint": "Which check would have caught the open security group in under a minute?",
                "objectives": ["Test infrastructure code", "Apply policy-as-code"],
                "mins": 10,
                "evidence": ["Designs layered infra test gates"]
            }
        ]
    },
    "cpp": {
        "core-syntax": [
            {
                "id": "cpp-coresyntax-sc1",
                "title": "The Dangling Else of Integer Division",
                "domain_id": "core-syntax",
                "situation": "A junior's telemetry function computes `double ratio = packets / total;` where both are `int`. With packets=3, total=4, the dashboard shows 0.0 instead of 0.75. The junior 'fixes' it by changing the return type to double, which changes nothing.",
                "prompt": "What is the real bug and the minimal correct fix?",
                "choices": [
                    "The function signature is wrong; make the parameters double",
                    "Integer division happens before the assignment: cast one operand — `double ratio = static_cast<double>(packets) / total;`",
                    "The compiler optimizes the division away; disable -O2",
                    "Use float instead of double for the ratio variable"
                ],
                "answer": 1,
                "why": "In C++, `packets / total` with two ints performs integer division (result 0) and only then converts to double — the cast must happen on an operand, not the result. Changing the variable type (or float vs double) doesn't touch the division itself. This is the classic exam/interview trap: the conversion happens too late.",
                "hint": "When does the int-to-double conversion happen relative to the division?",
                "objectives": ["Apply integer promotion rules", "Use static_cast correctly"],
                "mins": 8,
                "evidence": ["Places cast on operand, not result"]
            },
            {
                "id": "cpp-coresyntax-sc2",
                "title": "const Correctness Breaks the Build",
                "domain_id": "core-syntax",
                "situation": "You're adding a `getName()` accessor to a class. The codebase calls it on const objects in several places, and the build fails with 'discards qualifiers'. A teammate suggests removing const from the calling objects to 'make it compile'.",
                "prompt": "What is the correct fix?",
                "choices": [
                    "Remove const from the calling objects as suggested",
                    "Mark the accessor const: `std::string getName() const;` — the method promises not to mutate, so it works on const objects",
                    "Make getName() a static method",
                    "const_cast away constness inside the accessor"
                ],
                "answer": 1,
                "why": "A non-const member function cannot be called on a const object — the fix is declaring the accessor const, which is a compile-time promise of non-mutation. Stripping const from callers (A) weakens the whole codebase's guarantees; static (C) loses access to members; const_cast (D) lies to the compiler and risks UB on genuinely-const objects.",
                "hint": "The method's contract should say 'I won't modify anything' — where does that promise go?",
                "objectives": ["Apply const correctness", "Read qualifier-discard errors"],
                "mins": 8,
                "evidence": ["Adds const to accessor signature"]
            }
        ],
        "oop-cpp": [
            {
                "id": "cpp-oop-sc1",
                "title": "The Missing Virtual Destructor",
                "domain_id": "oop-cpp",
                "situation": "A plugin system holds `std::vector<Base*>` where Derived classes allocate buffers in their constructors and free them in their destructors. `Base` has virtual methods but a non-virtual destructor. Memory profiling shows a steady leak proportional to plugin reloads.",
                "prompt": "What is the root cause and fix?",
                "choices": [
                    "The vector should store unique_ptr<Base> instead of raw pointers",
                    "Deleting through a Base* with a non-virtual destructor invokes only ~Base(), so Derived's buffer is never freed — make ~Base() virtual",
                    "Derived destructors should be public instead of the current access level",
                    "The leak is in the vector reallocation; call shrink_to_fit()"
                ],
                "answer": 1,
                "why": "Deleting a derived object through a base pointer without a virtual destructor is undefined behavior in practice manifesting as a skipped derived destructor — the buffer leaks every reload. unique_ptr (A) is good hygiene but doesn't fix the destructor dispatch. This is the canonical interview question: any class designed as a polymorphic base needs a virtual (or protected non-virtual) destructor.",
                "hint": "Which destructor actually runs when you delete through the base pointer?",
                "objectives": ["Apply virtual destructor rule", "Diagnose polymorphic leaks"],
                "mins": 10,
                "evidence": ["Makes base destructor virtual"]
            },
            {
                "id": "cpp-oop-sc2",
                "title": "Slicing in the Event Queue",
                "domain_id": "oop-cpp",
                "situation": "An event system declares `std::vector<Event> queue;` and pushes `MouseEvent` and `KeyEvent` derived objects into it. At dispatch time, `dynamic_cast` checks fail and derived-specific data (coordinates, key codes) is garbage. The virtual dispatch table looks correct in the debugger.",
                "prompt": "What happened to the derived objects?",
                "choices": [
                    "The vtable pointer was corrupted by the vector reallocation",
                    "Object slicing: vector<Event> stores only the Event subobject — the derived parts were sliced off at push_back; store pointers (smart) or use std::variant",
                    "dynamic_cast doesn't work on vector elements",
                    "The derived classes need to redeclare the virtual functions"
                ],
                "answer": 1,
                "why": "A `vector<Event>` holds Events, period — pushing a Derived copies only the Base subobject (slicing), discarding derived data and dynamic type. The vtable is fine; there's just no derived object left to dispatch on. Polymorphic collections must hold (smart) pointers or a variant. This is a favorite interview trap because the code compiles cleanly.",
                "hint": "What does vector<Event> physically store — Events or something else?",
                "objectives": ["Recognize object slicing", "Design polymorphic containers"],
                "mins": 10,
                "evidence": ["Switches to pointer/variant storage"]
            }
        ],
        "stl-containers": [
            {
                "id": "cpp-stl-sc1",
                "title": "vector vs list in the Hot Loop",
                "domain_id": "stl-containers",
                "situation": "A particle simulation stores 2M particles in std::list because 'insertion is O(1)'. The update loop iterates all particles each frame and runs 3x slower than the prototype that used a plain array. Profiling shows the time in pointer chasing, not in the physics math.",
                "prompt": "What container decision fixes the performance?",
                "choices": [
                    "Keep std::list but reserve capacity upfront",
                    "Switch to std::vector: contiguous storage makes iteration cache-friendly; the O(1) list insertion never mattered because the loop is iteration-bound",
                    "Use std::deque for a compromise",
                    "Store particles in std::map keyed by ID for faster lookup"
                ],
                "answer": 1,
                "why": "The workload is iterate-all-every-frame: vector's contiguous layout streams through cache lines while list nodes scatter across the heap (pointer chasing + allocation overhead). list's O(1) insertion is irrelevant when nothing inserts mid-frame. list has no reserve (A is a trap — that member doesn't exist); deque helps at the ends but fragments similarly; map adds log-n overhead to a linear scan.",
                "hint": "What does the loop actually do — insert, or iterate?",
                "objectives": ["Match container to access pattern", "Reason about cache locality"],
                "mins": 10,
                "evidence": ["Chooses vector for iteration-bound loop"]
            },
            {
                "id": "cpp-stl-sc2",
                "title": "Iterator Invalidation Crash",
                "domain_id": "stl-containers",
                "situation": "A server loop iterates a std::vector<Connection> and erases timed-out connections inside the loop with `v.erase(it)`. It crashes intermittently under load but never in unit tests. The crash is a heap-use-after-free in the sanitizer.",
                "prompt": "What is the bug and the idiomatic fix?",
                "choices": [
                    "The vector needs a mutex around the loop",
                    "erase() invalidates the iterator (and all after it on reallocation/shift); use the erase-remove idiom or `it = v.erase(it)` which returns the next valid iterator",
                    "Reserve more capacity so erase never reallocates",
                    "Switch to indexing with operator[] instead of iterators"
                ],
                "answer": 1,
                "why": "`erase` invalidates the erased iterator (and following ones as elements shift); continuing to `++it` is use-after-invalidation — intermittent because it depends on timing/size. The idiomatic fixes: assign the return value (`it = v.erase(it)`) or erase-remove for predicate-based removal. A mutex (A) addresses threads, not invalidation; reserve (C) doesn't stop the shift; indexing (D) has the same invalidation problem.",
                "hint": "What does erase() return, and why would it bother?",
                "objectives": ["Handle iterator invalidation", "Apply erase-remove idiom"],
                "mins": 10,
                "evidence": ["Uses erase return value correctly"]
            }
        ],
        "memory-smart-pointers": [
            {
                "id": "cpp-memory-sc1",
                "title": "shared_ptr Cycle in the Scene Graph",
                "domain_id": "memory-smart-pointers",
                "situation": "A scene graph uses shared_ptr for parent->child and child->parent links. Nodes are removed from the scene but memory never drops — the allocator shows every removed subtree still alive. Reference counts on removed nodes stay at 1+.",
                "prompt": "What is the leak mechanism and the fix?",
                "choices": [
                    "shared_ptr is broken; switch everything to raw pointers",
                    "Reference cycle: parent and child keep each other alive; make the child->parent link a weak_ptr (non-owning back-reference)",
                    "Call reset() on every pointer at removal time",
                    "The allocator is fragmenting; switch allocators"
                ],
                "answer": 1,
                "why": "shared_ptr cycles never reach zero — parent owns child, child owns parent, so removal from the scene leaves the cycle self-sustaining. weak_ptr expresses the non-owning back-reference: it observes without keeping alive (lock() to use). Manual reset (C) fights the ownership model instead of fixing it; raw pointers (A) abandon safety; the allocator (D) is innocent.",
                "hint": "Who owns whom — and does the back-link need to own?",
                "objectives": ["Break shared_ptr cycles", "Apply weak_ptr for back-references"],
                "mins": 10,
                "evidence": ["Converts parent link to weak_ptr"]
            },
            {
                "id": "cpp-memory-sc2",
                "title": "unique_ptr Array Gotcha",
                "domain_id": "memory-smart-pointers",
                "situation": "Legacy code does `std::unique_ptr<Widget> p(new Widget[100]);` and fills the array. It runs fine in tests but corrupts the heap on destruction in production builds. The team debates whether unique_ptr is 'safe for arrays'.",
                "prompt": "What is wrong and what is the correct modern form?",
                "choices": [
                    "unique_ptr can't manage arrays at all; use new/delete manually",
                    "Wrong specialization: unique_ptr<Widget> calls delete, not delete[], on an array — use unique_ptr<Widget[]> (or better, std::vector<Widget>)",
                    "The heap corruption is from filling the array, not the deletion",
                    "Add a custom deleter that calls delete[]"
                ],
                "answer": 1,
                "why": "`unique_ptr<T>` uses `delete`; arrays need `delete[]` — mismatching them is undefined behavior (the heap corruption on destruction). The `unique_ptr<T[]>` partial specialization uses `delete[]` and even provides operator[]. A custom deleter (D) works but is obsolete; manual new/delete (A) surrenders the safety; and in practice std::vector is usually the right answer over a managed raw array.",
                "hint": "Which delete does unique_ptr<T> call — and which does an array need?",
                "objectives": ["Use unique_ptr array specialization", "Match new[] with delete[]"],
                "mins": 10,
                "evidence": ["Selects unique_ptr<T[]> or vector"]
            }
        ],
        "templates-lambdas": [
            {
                "id": "cpp-templates-sc1",
                "title": "Template Bloat in the Math Library",
                "domain_id": "templates-lambdas",
                "situation": "A header-only math library templates everything on the scalar type. The binary grew 40MB and builds take 25 minutes — profiling shows hundreds of instantiations of identical logic differing only in float vs double vs long double. Most functions don't actually depend on the scalar type's exact width.",
                "prompt": "How do you cut the bloat without losing genericity?",
                "choices": [
                    "Stop using templates and write three copies of each function",
                    "Factor type-independent logic into non-template base functions (or a common implementation), keep templates as thin wrappers; explicitly instantiate only the needed types in one TU",
                    "Mark everything inline to help the linker",
                    "Split the header into more headers"
                ],
                "answer": 1,
                "why": "Template bloat comes from instantiating identical machine code per type — hoisting the type-independent core into a regular function means one copy, with thin template shims for the type-dependent surface; explicit instantiation in a single translation unit prevents N copies across TUs. Manual copies (A) are unmaintainable; inline (C) can worsen bloat; more headers (D) doesn't change instantiation count.",
                "hint": "Which parts of the logic actually care whether it's float or double?",
                "objectives": ["Control template instantiation bloat", "Apply explicit instantiation"],
                "mins": 12,
                "evidence": ["Hoists common logic out of templates"]
            },
            {
                "id": "cpp-templates-sc2",
                "title": "Lambda Capture Dangling Reference",
                "domain_id": "templates-lambdas",
                "situation": "A function builds a task queue: `for (auto& job : jobs) queue.push([&]{ process(job); });` The queue runs after the function returns. Intermittently, jobs process with garbage data or crash. Capturing by value `[=]` 'fixes' it but copies large job objects.",
                "prompt": "What is the bug and the efficient fix?",
                "choices": [
                    "Lambdas can't be stored; run them immediately instead",
                    "[&] captures job by reference — after the loop/function ends the reference dangles; capture the needed data by value with an init-capture move: `[j = std::move(job)]` (or capture a shared_ptr)",
                    "Make job a global variable",
                    "Add a mutex around the queue"
                ],
                "answer": 1,
                "why": "Default reference capture `[&]` stores references to loop variables that die when the function returns — classic dangling. `[=]` copies (safe but expensive for large jobs). Init-capture with move (`[j = std::move(job)]`) transfers ownership into the lambda: no dangle, no copy. Globals (C) and mutexes (D) don't address lifetime at all.",
                "hint": "How long does the captured reference live versus how long does the lambda live?",
                "objectives": ["Manage lambda capture lifetimes", "Use init-capture move semantics"],
                "mins": 10,
                "evidence": ["Applies move init-capture"]
            }
        ],
        "build-toolchain": [
            {
                "id": "cpp-build-sc1",
                "title": "The ODR Violation That Only Fails on Fridays",
                "domain_id": "build-toolchain",
                "situation": "A function behaves differently in debug vs release, and differently again when a new TU is added. Investigation finds a non-inline function defined in a header included by 12 TUs, with slightly different macro settings per TU. The linker never complained.",
                "prompt": "What rule is violated and what is the fix?",
                "choices": [
                    "The One Definition Rule: a non-inline function defined in a header creates 12 differing definitions (linker picks one silently); mark it inline, or move the definition to one .cpp with a declaration in the header",
                    "The build needs -O0 everywhere for consistency",
                    "Headers should never contain function bodies",
                    "It's a compiler bug; upgrade the toolchain"
                ],
                "answer": 0,
                "why": "ODR requires exactly one definition of a non-inline function program-wide — a header definition included in 12 TUs with different macros yields 12 different definitions, and the linker silently keeps one (no diagnostic required). `inline` explicitly permits multiple identical definitions; otherwise define once in a .cpp. -O0 (B) masks it; 'never bodies in headers' (C) is overbroad (inline/template bodies are fine).",
                "hint": "Twelve translation units, twelve definitions, zero linker errors — which rule allows the linker to stay silent?",
                "objectives": ["Apply the One Definition Rule", "Use inline correctly"],
                "mins": 12,
                "evidence": ["Moves definition to single TU or inline"]
            },
            {
                "id": "cpp-build-sc2",
                "title": "Link Order Linker Errors",
                "domain_id": "build-toolchain",
                "situation": "Linking fails with 'undefined reference to Logger::write' although liblogging.a definitely contains the symbol (verified with nm). The link command lists `-llogging` BEFORE the object files that use it. Reordering fixes it, but nobody understands why.",
                "prompt": "Why does library order matter with static linking?",
                "choices": [
                    "The linker is buggy and order shouldn't matter",
                    "Traditional Unix linkers process left-to-right, pulling from a static archive only the objects resolving currently-undefined symbols — a library before its users contributes nothing",
                    "liblogging.a was built with the wrong architecture",
                    "nm shows symbols the linker can't see due to visibility settings"
                ],
                "answer": 1,
                "why": "Static archives are lazy symbol pools: the linker scans left to right, and when it reaches liblogging.a it only extracts members satisfying undefined symbols seen SO FAR. Listed first, there are no undefined symbols yet, so nothing is extracted — later objects' references stay unresolved. Hence: libraries after the objects that need them (or use --start-group). Shared libraries don't behave this way, which is why the confusion is common.",
                "hint": "What does the linker know at the moment it opens the archive?",
                "objectives": ["Understand static link order", "Diagnose undefined-reference errors"],
                "mins": 10,
                "evidence": ["Places libraries after dependents"]
            }
        ],
        "systems-anatomy": [
            {
                "id": "cpp-sysanat-sc1",
                "title": "Compilation Pipeline: Where Did My Symbol Go?",
                "domain_id": "systems-anatomy",
                "situation": "A build fails at link time: 'undefined reference to Config::load()'. The .cpp file compiles cleanly, the header declares it, and the object file exists. The pipeline stages are: preprocess -> compile -> assemble -> link.",
                "prompt": "Which stage is failing and what does that tell you about the cause?",
                "choices": [
                    "Compile stage: the function body has a syntax error",
                    "Link stage: compilation succeeded (object file exists), so the definition isn't reaching the linker — the .cpp isn't in the build, or the signature/mangling mismatches (e.g., namespace or const mismatch)",
                    "Preprocess stage: the header guard is broken",
                    "Assemble stage: the assembler dropped the symbol"
                ],
                "answer": 1,
                "why": "Clean compilation proves preprocessing, compiling, and assembling all succeeded — the symbol is missing at link time, meaning the definition's object file isn't linked in, or the mangled name differs (namespace, parameter types, or const-qualification mismatch between declaration and definition). Syntax (A) would fail compilation; header guards (C) would break compilation too; assemblers (D) don't drop symbols.",
                "hint": "The object file exists — so which stages already proved themselves innocent?",
                "objectives": ["Trace the compilation pipeline", "Diagnose link-stage failures"],
                "mins": 10,
                "evidence": ["Isolates missing definition at link stage"]
            },
            {
                "id": "cpp-sysanat-sc2",
                "title": "Memory Layout: The Corrupted Global",
                "domain_id": "systems-anatomy",
                "situation": "A global `int config_value = 42;` reads as 0 at startup on an embedded target, while a global `int counter;` (uninitialized) reads garbage instead of 0. The startup code was recently 'optimized'.",
                "prompt": "Using program memory layout (.text / .data / .bss / stack / heap), what broke?",
                "choices": [
                    "The heap allocator is corrupting globals",
                    ".data (initialized globals like config_value) isn't being copied from flash, and .bss (zero-initialized, like counter) isn't being zeroed — the CRT startup routine was gutted",
                    "Stack overflow is overwriting the globals",
                    "The linker script placed .data in RAM that doesn't exist"
                ],
                "answer": 1,
                "why": "Initialized globals live in .data (loaded from the binary image at startup); uninitialized/zero globals live in .bss (zeroed at startup). config_value=0 means .data wasn't copied; garbage counter means .bss wasn't zeroed — both are jobs of the C runtime startup code that runs before main(). The 'optimization' removed it. Heap (A) and stack (C) don't hold globals; a bad linker script (D) would typically fault, not zero.",
                "hint": "Who is responsible for preparing .data and .bss before main() runs?",
                "objectives": ["Explain program memory layout", "Diagnose CRT startup failures"],
                "mins": 10,
                "evidence": ["Attributes symptoms to .data/.bss init"]
            },
            {
                "id": "cpp-sysanat-sc3",
                "title": "Stack Frames: The Vanishing Return Address",
                "domain_id": "systems-anatomy",
                "situation": "A recursive parser crashes with a stack overflow on deeply nested input (10,000 levels). Each frame holds a 4KB parse buffer as a local array. The recursion depth itself is algorithmically necessary.",
                "prompt": "Following stack-frame anatomy (return address, saved registers, locals), what is the minimal fix?",
                "choices": [
                    "Increase the thread stack size to 64MB",
                    "Move the 4KB buffer off the stack (heap-allocate it or make it a reused member) — frame size, not depth, is the multiplier; 10k frames x small frame fits, x 4KB doesn't",
                    "Convert the recursion to iteration",
                    "Add a depth counter and throw at 5,000"
                ],
                "answer": 1,
                "why": "Stack usage = depth x frame size. The depth is required, but the 4KB local is not — moving it to the heap (or reusing one buffer) shrinks each frame to tens of bytes, so 10k frames fit comfortably. Bigger stacks (A) just move the cliff; iteration (C) is a bigger rewrite for the same effect; an arbitrary cap (D) rejects valid input.",
                "hint": "Two factors multiply into stack usage — which one is actually optional here?",
                "objectives": ["Analyze stack frame layout", "Fix stack overflows by frame size"],
                "mins": 10,
                "evidence": ["Moves large local off the stack"]
            },
            {
                "id": "cpp-sysanat-sc4",
                "title": "STL Internals: vector Growth Cliff",
                "domain_id": "systems-anatomy",
                "situation": "A latency-sensitive service does `v.push_back(x)` in a loop without reserve(). p99 latency shows periodic 50ms spikes; between spikes it's 50ns per push. The vector holds 10M elements by end of day.",
                "prompt": "What internal mechanism causes the spikes?",
                "choices": [
                    "The allocator is fragmenting under load",
                    "Geometric growth: when capacity is exhausted, vector allocates a bigger buffer (typically 1.5-2x) and moves all elements — an O(n) reallocation spike, amortized O(1) overall",
                    "push_back is O(n) because it shifts elements",
                    "The CPU cache is being thrashed by sequential writes"
                ],
                "answer": 1,
                "why": "vector grows geometrically: most push_backs are a cheap write, but each capacity exhaustion triggers allocate + move-N-elements + free — the periodic 50ms cliff, amortized to O(1). The fix is reserve() up front. Allocator fragmentation (A) wouldn't be periodic; push_back doesn't shift (C — that's insert at front); sequential writes (D) are the cache-friendliest pattern there is.",
                "hint": "Spikes are periodic and the cost between them is tiny — what grows geometrically?",
                "objectives": ["Explain vector growth strategy", "Use reserve() for latency stability"],
                "mins": 10,
                "evidence": ["Identifies reallocation spikes; adds reserve"]
            },
            {
                "id": "cpp-sysanat-sc5",
                "title": "Linker/Loader Flow: The Slow Startup",
                "domain_id": "systems-anatomy",
                "situation": "A C++ application links 80 shared libraries and takes 12 seconds to start — before main() does anything. Profiling the startup shows the time in symbol resolution, and the binary has 200k exported symbols.",
                "prompt": "Where in the loader flow is the time going, and how do you cut it?",
                "choices": [
                    "The kernel is slow to mmap 80 libraries; use fewer threads",
                    "Dynamic loader symbol relocation: reduce exported symbols (visibility=hidden, version scripts), cut unnecessary library dependencies, consider prelinking/relative relocations",
                    "main() is doing too much static initialization",
                    "The disk is slow; buy faster storage"
                ],
                "answer": 1,
                "why": "Before main(), the dynamic loader maps libraries and performs relocations — with 200k exported symbols across 80 libs, symbol lookup (hash chains, string compares) dominates. -fvisibility=hidden plus version scripts shrink the dynamic symbol table dramatically; pruning unused DT_NEEDED entries shortens the search. Static init (C) happens after relocation; disk (D) is a one-time map cost, not 12s of symbol work.",
                "hint": "The time is before main() and scales with symbol count — what does the loader do with symbols?",
                "objectives": ["Trace dynamic loader startup", "Reduce symbol visibility"],
                "mins": 10,
                "evidence": ["Applies visibility=hidden to cut relocations"]
            },
            {
                "id": "cpp-sysanat-sc6",
                "title": "Cache Hierarchy: The False Sharing Slowdown",
                "domain_id": "systems-anatomy",
                "situation": "Two threads each increment their own counter in a tight loop. The counters are adjacent members of a struct (8 bytes apart). On a 16-core machine the loop runs 5x SLOWER with two threads than one thread does alone. CPU utilization shows both cores busy.",
                "prompt": "What cache-coherence effect explains this?",
                "choices": [
                    "The threads are context-switching too often",
                    "False sharing: both counters share one 64-byte cache line, so each increment invalidates the line in the other core's cache — cores ping-pong the line instead of computing",
                    "The memory bus is saturated by two increment streams",
                    "The compiler didn't vectorize the loop"
                ],
                "answer": 1,
                "why": "Cache coherence works at 64-byte line granularity: two counters in one line mean every write by either core invalidates the other's cached copy, forcing a cross-core transfer per increment — the cores serialize on the interconnect. The fix is padding/alignas(64) to put each counter on its own line. Context switches (A) don't apply to pinned busy loops; two increments can't saturate the bus (C); vectorization (D) is irrelevant to scalar counters.",
                "hint": "Coherence moves 64 bytes at a time — how far apart are the counters?",
                "objectives": ["Diagnose false sharing", "Apply cache-line padding"],
                "mins": 10,
                "evidence": ["Pads counters to separate cache lines"]
            }
        ],
        "interview-prep": [
            {
                "id": "cpp-interview-sc1",
                "title": "Code Review: The Clever Ternary Chain",
                "domain_id": "interview-prep",
                "situation": "In a code review you find: `return x > 0 ? (y > 0 ? a : b) : (y > 0 ? c : d);` The author defends it as 'efficient — no branches'. The function is in a billing path that changes quarterly.",
                "prompt": "What is your review decision?",
                "choices": [
                    "Approve — fewer branches means faster code",
                    "Request changes: rewrite as explicit if/else with named conditions — the ternary chain is unreadable, untestable per-branch, and the compiler generates the same branches anyway",
                    "Approve but add a comment explaining the logic",
                    "Rewrite it yourself using a lookup table"
                ],
                "answer": 1,
                "why": "Nested ternaries don't eliminate branches — the compiler emits the same comparisons; they only eliminate readability. In a quarterly-changing billing path, the cost is future mis-edits and untestable branches. Request explicit control flow with named booleans. A comment (C) documents confusion instead of removing it; rewriting it yourself (D) bypasses the author's learning.",
                "hint": "Who pays the cost of this cleverness — the CPU or the next engineer?",
                "objectives": ["Conduct effective code reviews", "Value readability over cleverness"],
                "mins": 10,
                "evidence": ["Requests if/else rewrite with rationale"]
            },
            {
                "id": "cpp-interview-sc2",
                "title": "Trade-off: Exceptions vs Error Codes",
                "domain_id": "interview-prep",
                "situation": "The interviewer asks: 'Your team is writing a high-frequency trading gateway in C++. Do you use exceptions or error codes?' The gateway processes 1M messages/sec; failures are rare but must be handled precisely.",
                "prompt": "What is the strong interview answer?",
                "choices": [
                    "Exceptions — modern C++ prefers them and they're cleaner",
                    "Error codes (std::expected / status returns): zero-cost on the hot path, deterministic latency with no unwinding; reserve exceptions for truly exceptional, non-performance-critical paths",
                    "assert() and crash on any error",
                    "Mix randomly per developer preference"
                ],
                "answer": 1,
                "why": "This tests trade-off reasoning, not dogma: exceptions have zero cost when not thrown but unpredictable latency when thrown (unwinding, cache effects) — unacceptable where p99 latency is the product. std::expected makes errors explicit, composable, and free on success. The strong answer names the criterion (deterministic latency) and the exception (use exceptions where latency doesn't matter). assert-and-crash (C) is for invariants, not handleable errors.",
                "hint": "What is the product actually selling — clean code or predictable nanoseconds?",
                "objectives": ["Reason about error-handling trade-offs", "Apply std::expected appropriately"],
                "mins": 10,
                "evidence": ["Justifies error codes by latency determinism"]
            },
            {
                "id": "cpp-interview-sc3",
                "title": "Debugging: The Heisenbug That Vanishes",
                "domain_id": "interview-prep",
                "situation": "Interviewer: 'A crash reproduces in release but disappears the moment you attach a debugger or add print statements. Walk me through your debugging.' The crash is a segfault in an optimized multithreaded service.",
                "prompt": "What debugging strategy do you describe?",
                "choices": [
                    "Keep adding prints until it reproduces under the debugger",
                    "Suspect undefined behavior (use-after-free, data race, uninitialized read) whose manifestation depends on timing/layout: run under ASan/TSan/UBSan, capture core dumps with full symbols, and bisect with -O0 vs -O2 to isolate optimizer-sensitive UB",
                    "Blame the optimizer and ship -O0",
                    "Rewrite the crashing module from scratch"
                ],
                "answer": 1,
                "why": "Heisenbugs that flee observation scream UB or races — timing/layout-dependent. Sanitizers (ASan/TSan/UBSan) detect the bug class directly instead of chasing symptoms; core dumps preserve the optimized crash; optimization-level bisection isolates miscompiled-UB cases. More prints (A) perturbs timing further; -O0 (C) hides it in production; rewrite (D) is surrender without diagnosis.",
                "hint": "What class of bug changes behavior when you merely observe it?",
                "objectives": ["Debug heisenbugs systematically", "Apply sanitizers"],
                "mins": 12,
                "evidence": ["Describes sanitizer + core dump workflow"]
            },
            {
                "id": "cpp-interview-sc4",
                "title": "Design: Cache for the Config Service",
                "domain_id": "interview-prep",
                "situation": "Interviewer: 'Design an in-memory cache for a config service: 10k keys, reads 100k/sec, writes 10/sec, values up to 1MB, must never serve stale data older than 1 second.' They watch how you handle the read/write asymmetry.",
                "prompt": "What design do you propose?",
                "choices": [
                    "std::map with a single mutex — simple and correct",
                    "Read-optimized: std::unordered_map with shared_mutex (shared_lock for reads, unique_lock for writes), versioned entries with timestamps, background refresh keeping staleness under 1s",
                    "Lock-free everything with atomics",
                    "Redis — don't build it yourself"
                ],
                "answer": 1,
                "why": "The 10,000:1 read/write ratio demands read-optimized concurrency: shared_mutex lets 100k reads proceed in parallel while rare writes exclude briefly; versioning + timestamps enforce the 1s staleness bound explicitly. A single mutex (A) serializes 100k reads; lock-free (C) is overkill complexity for 10 writes/sec; Redis (D) dodges the design question the interviewer asked.",
                "hint": "Which operation dominates, and what synchronization shape matches a 10000:1 ratio?",
                "objectives": ["Design for read-heavy concurrency", "Apply shared_mutex correctly"],
                "mins": 12,
                "evidence": ["Proposes shared_mutex + versioning design"]
            },
            {
                "id": "cpp-interview-sc5",
                "title": "Behavioral With Teeth: The Production Incident",
                "domain_id": "interview-prep",
                "situation": "Interviewer: 'Tell me about a time you caused a production incident.' You once deployed an O(n^2) config parser that took down a service at scale. They're probing ownership and technical depth, not just storytelling.",
                "prompt": "What makes the answer strong?",
                "choices": [
                    "Emphasize it wasn't really your fault — the reviewer approved it",
                    "STAR with technical depth: what you shipped, the exact failure mode (quadratic blowup at 50k entries), how you detected it, the immediate mitigation, and the systemic fix (load tests with production-scale fixtures + complexity review checklist)",
                    "Keep it vague to avoid looking bad",
                    "Say you've never caused an incident"
                ],
                "answer": 1,
                "why": "Interviewers score ownership + learning + technical precision: naming the exact mechanism (O(n^2) at 50k entries) proves depth, the mitigation shows calm under pressure, and the systemic fix (scale-realistic load tests, checklist) shows you fixed the process, not just the bug. Deflection (A), vagueness (C), and denial (D) all signal the opposite of what's being tested.",
                "hint": "They're grading what you changed afterward, not the mistake itself.",
                "objectives": ["Answer behavioral questions with depth", "Demonstrate ownership"],
                "mins": 8,
                "evidence": ["Gives STAR with mechanism + systemic fix"]
            },
            {
                "id": "cpp-interview-sc6",
                "title": "Rule of Five in the Interview",
                "domain_id": "interview-prep",
                "situation": "Interviewer shows a class managing a raw buffer with a custom destructor and copy constructor, then asks: 'What else does this class need, and what happens if we add a move constructor but nothing else?'",
                "prompt": "What is the complete correct answer?",
                "choices": [
                    "Nothing else — destructor plus copy constructor is sufficient",
                    "Rule of five: it also needs copy assignment, move constructor, and move assignment (or =delete the ones you don't want); adding only a move constructor suppresses the copy operations, silently breaking existing copies",
                    "Just add a move assignment too",
                    "Replace everything with =default"
                ],
                "answer": 1,
                "why": "Managing a resource means owning the full copy/move/destroy set — and the subtle trap: declaring any move operation deletes the copy operations (and vice versa per the rules), so a lone move constructor silently breaks code that copies. The complete answer states the rule of five AND the suppression side-effect. =default (D) on a raw-buffer class would shallow-copy the buffer — the original bug.",
                "hint": "What does declaring a move constructor do to the copy constructor you didn't declare?",
                "objectives": ["Apply rule of five", "Explain special member suppression"],
                "mins": 10,
                "evidence": ["States rule of five + suppression effects"]
            },
            {
                "id": "cpp-interview-sc7",
                "title": "Estimating Live: How Much Memory?",
                "domain_id": "interview-prep",
                "situation": "Interviewer: 'We store 50 million user sessions in std::unordered_map<std::string, Session>. Roughly how much memory is that, and what's your biggest lever to cut it?' Session is 64 bytes; average key length 20 chars.",
                "prompt": "What estimation reasoning do you show?",
                "choices": [
                    "50M x (64 + 20) bytes = ~4.2GB, and that's the answer",
                    "Per-node overhead dominates: node allocation (~32B) + bucket pointer + string's own allocation (~20B + overhead) + 64B session ≈ 150-200B per entry → 8-10GB; biggest lever is a flat_map/sorted vector or string interning to kill per-node and per-key allocations",
                    "It depends on the machine, so you can't estimate",
                    "Use a bigger hash table to reduce memory"
                ],
                "answer": 1,
                "why": "Interview estimation tests overhead-awareness: unordered_map is node-based (each entry a separate allocation with pointer overhead), and std::string usually heap-allocates — the overhead dwarfs the 84 bytes of payload. Naming the components and the lever (contiguous storage, interning) shows systems thinking. The naive multiply (A) misses 2x overhead; 'can't estimate' (C) forfeits the question; bigger tables (D) increase memory.",
                "hint": "Count the allocations per entry, not just the bytes of payload.",
                "objectives": ["Estimate container memory overhead", "Reason about node-based containers"],
                "mins": 12,
                "evidence": ["Breaks down per-entry overhead components"]
            }
        ],
        "concurrency": [
            {
                "id": "cpp-concurrency-sc1",
                "title": "Race Diagnosis: The Flaky Counter",
                "domain_id": "concurrency",
                "situation": "A metrics counter `total_requests++` is incremented from 8 worker threads. The reported total is consistently 5-15% BELOW the true count, and the deficit grows with thread count. No crashes, no sanitizer warnings in the default build.",
                "prompt": "What is the diagnosis and the minimal fix?",
                "choices": [
                    "The threads need joining before reading the counter",
                    "Data race on non-atomic increment: read-modify-write interleavings lose updates; make it std::atomic<long long> (or a sharded per-thread counter summed at read)",
                    "The counter is overflowing; use a bigger type",
                    "CPU caches are stale; add a memory barrier manually"
                ],
                "answer": 1,
                "why": "Non-atomic `++` is load-add-store: two threads can load the same value and both store N+1, losing one update — the deficit scales with contention, exactly the symptom. std::atomic makes the increment indivisible (TSan would have flagged it). Joining (A) doesn't fix the race; overflow (C) would show wraparound, not a deficit; manual barriers (D) are what atomics already provide.",
                "hint": "Three machine instructions, two threads — draw the interleave that loses a count.",
                "objectives": ["Diagnose data races", "Apply std::atomic"],
                "mins": 10,
                "evidence": ["Identifies lost-update interleave"]
            },
            {
                "id": "cpp-concurrency-sc2",
                "title": "Mutex vs Atomic: The Config Flag",
                "domain_id": "concurrency",
                "situation": "A boolean `shutdown_requested` is polled by 32 threads in tight loops and set once by the main thread. A reviewer suggests std::mutex; another suggests std::atomic<bool>; a third says 'bool is one byte, it's already atomic'.",
                "prompt": "Which is correct and why?",
                "choices": [
                    "std::mutex — always the safe default",
                    "std::atomic<bool>: single flag, trivially copyable — atomics give the needed visibility/ordering with near-zero cost; a mutex per poll would serialize 32 tight loops, and plain bool is a data race regardless of size",
                    "Plain bool — single-byte accesses can't tear",
                    "volatile bool — it prevents caching"
                ],
                "answer": 1,
                "why": "'One byte' doesn't mean atomic or visible — without synchronization it's a data race (UB), and the compiler may hoist the read out of the loop entirely. atomic<bool> is the exact tool: lock-free on every major platform, correct visibility, negligible cost. A mutex (A) around a flag poll is massive overkill; volatile (D) is not a synchronization primitive in C++.",
                "hint": "What stops the compiler from reading the flag once and reusing the value forever?",
                "objectives": ["Choose atomic vs mutex", "Reject volatile-as-synchronization"],
                "mins": 10,
                "evidence": ["Selects atomic<bool> with reasoning"]
            },
            {
                "id": "cpp-concurrency-sc3",
                "title": "Deadlock at 3 AM",
                "domain_id": "concurrency",
                "situation": "A service deadlocks roughly weekly. Two mutexes guard the account map (m_accounts) and the audit log (m_audit). Thread 1's transfer path locks accounts then audit; a new reporting path locks audit then accounts. Core dumps show each thread holding one mutex and waiting on the other.",
                "prompt": "What is the deadlock and the robust fix?",
                "choices": [
                    "It's a livelock; add random backoff and retry",
                    "Classic lock-order inversion (AB-BA deadlock): enforce a global lock ordering (always accounts before audit), or use std::lock/std::scoped_lock to acquire both atomically",
                    "Merge the two mutexes into one big lock",
                    "Increase the thread stack so the wait doesn't deadlock"
                ],
                "answer": 1,
                "why": "The dump is the textbook AB-BA cycle: T1 holds A waits B, T2 holds B waits A — inconsistent lock ordering. The robust fix is a single global order (documented and enforced) or std::lock/scoped_lock which acquires multiple mutexes deadlock-free. Backoff (A) misdiagnoses deadlock as livelock; one big lock (C) works but serializes unrelated audit writes — acceptable fallback, not the principled fix.",
                "hint": "Draw who holds what and who waits for what — what shape is it?",
                "objectives": ["Diagnose lock-order deadlocks", "Apply consistent lock ordering"],
                "mins": 12,
                "evidence": ["Maps AB-BA cycle and orders locks"]
            },
            {
                "id": "cpp-concurrency-sc4",
                "title": "Thread Pool Sizing for the Image Pipeline",
                "domain_id": "concurrency",
                "situation": "An image pipeline has two stages: CPU-bound thumbnail generation and I/O-bound cloud upload. The current pool uses 64 threads for everything on a 16-core box. Thumbnails are slow (context switching) and uploads stall (threads blocked on network while thumbnails wait for slots).",
                "prompt": "How do you size the pools?",
                "choices": [
                    "One pool of 16 threads for everything — match core count",
                    "Two pools: ~16 threads for CPU-bound thumbnails (cores + small headroom), larger pool (e.g., 64+) for I/O-bound uploads where threads mostly wait",
                    "256 threads in one pool to keep everything fed",
                    "One thread per stage in a pipeline chain"
                ],
                "answer": 1,
                "why": "CPU-bound work wants ~core count (more threads just context-switch); I/O-bound work wants many threads because each spends most of its life blocked, not computing. Separate pools stop blocked upload threads from starving thumbnail slots and vice versa. A single 16-pool (A) underfeeds uploads; 256 (C) thrashes the CPU stage; a 2-thread chain (D) serializes all throughput.",
                "hint": "What is each thread doing most of the time — computing or waiting?",
                "objectives": ["Size thread pools by workload type", "Separate CPU and I/O pools"],
                "mins": 12,
                "evidence": ["Splits pools by bound type"]
            },
            {
                "id": "cpp-concurrency-sc5",
                "title": "Data Race Fix: The Lazy Cache",
                "domain_id": "concurrency",
                "situation": "A config cache is lazily built on first use: `if (!cache_) cache_ = build(); return *cache_;` Under load, two threads enter simultaneously, both build, one result leaks, and occasionally a thread reads a half-constructed cache. std::call_once was suggested but 'seems heavy'.",
                "prompt": "What is the correct fix?",
                "choices": [
                    "Double-checked locking with a plain bool flag",
                    "std::call_once with std::once_flag — exactly the tool for one-time initialization; or a function-local static (magic statics are thread-safe since C++11)",
                    "Build the cache eagerly at startup and skip laziness",
                    "Wrap the whole thing in a mutex on every access"
                ],
                "answer": 1,
                "why": "Double-checked locking with a plain flag is broken (the half-constructed read is the classic publication-safety failure). std::call_once exists precisely for this — one-time, race-free, and cheap after the first call. Function-local statics give the same guarantee with less code. Eager init (C) is a fine alternative when startup cost is acceptable; per-access mutex (D) pessimizes the hot path.",
                "hint": "The half-constructed read is a publication problem — what guarantees safe publication?",
                "objectives": ["Fix lazy-initialization races", "Apply call_once / magic statics"],
                "mins": 10,
                "evidence": ["Uses call_once for one-time init"]
            },
            {
                "id": "cpp-concurrency-sc6",
                "title": "Condition Variable: The Missed Wakeup",
                "domain_id": "concurrency",
                "situation": "A worker waits for jobs: `if (queue.empty()) cv.wait(lock); job = queue.pop();` Occasionally it pops from an empty queue and crashes, or sleeps forever despite queued jobs. The notifier does `queue.push(j); cv.notify_one();`.",
                "prompt": "What are the two bugs and the fix?",
                "choices": [
                    "notify_one should be notify_all, and the mutex is unnecessary",
                    "`if` must be `while` (spurious wakeups + the check-then-wait race), and the predicate check with wait(lock, pred) is the fix: `cv.wait(lock, [&]{ return !queue.empty(); });`",
                    "The queue needs to be a priority queue",
                    "Wait without holding the lock to avoid deadlock"
                ],
                "answer": 1,
                "why": "Two classic bugs: (1) `if` instead of `while` — spurious wakeups (allowed by the standard) pop an empty queue; (2) the check-then-act race — a job can arrive between empty() and wait(), and the notify fires before wait() sleeps, so it sleeps forever. The predicate form of wait() rechecks atomically under the lock, fixing both. notify_all (A) doesn't fix either; waiting unlocked (D) is itself a race.",
                "hint": "What happens between the empty() check and the wait() — and what does the standard allow wait() to do spontaneously?",
                "objectives": ["Use condition variables correctly", "Handle spurious wakeups"],
                "mins": 12,
                "evidence": ["Converts to predicate-form wait"]
            },
            {
                "id": "cpp-concurrency-sc7",
                "title": "Lock Granularity: The Contended Registry",
                "domain_id": "concurrency",
                "situation": "A service registry uses one mutex guarding a map of 100k services. With 48 threads doing lookups, throughput plateaus at 8 threads and lock contention dominates profiles. Writes (register/unregister) are 0.1% of operations.",
                "prompt": "What concurrency design unlocks the read throughput?",
                "choices": [
                    "Remove the mutex — reads don't modify the map",
                    "Reader-writer shape: std::shared_mutex with shared_lock for lookups and unique_lock for the rare writes; or sharded maps with per-shard mutexes",
                    "A spinlock instead of a mutex for lower latency",
                    "Make the map thread-local in each thread"
                ],
                "answer": 1,
                "why": "99.9% reads means the exclusive mutex serializes work that doesn't conflict — shared_mutex lets concurrent readers proceed while rare writes still exclude. Sharding is the alternative when even reader coordination costs too much. Removing the lock (A) races with the 0.1% writes (and rehashing); spinlocks (C) still serialize; thread-local copies (D) break consistency on writes.",
                "hint": "What fraction of operations actually conflict with each other?",
                "objectives": ["Apply reader-writer locks", "Choose lock granularity"],
                "mins": 10,
                "evidence": ["Proposes shared_mutex for read-heavy map"]
            }
        ],
        "perf-optimization": [
            {
                "id": "cpp-perf-sc1",
                "title": "Reading the Flame Graph",
                "domain_id": "perf-optimization",
                "situation": "A profiler flame graph for a slow request handler shows a wide plateau in `serialize()` taking 60% of samples, with narrow towers for JSON escaping inside it. The team wants to rewrite the JSON library. The handler also does 200 small allocations per request.",
                "prompt": "What does the flame graph actually tell you to do first?",
                "choices": [
                    "Rewrite the JSON library — 60% is 60%",
                    "Attack the width first: reduce how often serialize() runs (cache serialized output, avoid re-serializing unchanged data); the narrow escaping towers are second-order",
                    "Optimize the 200 allocations — allocation is always the bottleneck",
                    "Add more threads to parallelize serialization"
                ],
                "answer": 1,
                "why": "Flame graph width = frequency x cost: a wide plateau means the frame runs often and long — the first question is whether the work can be avoided (caching, dirty-checking), which beats optimizing it. Only after eliminating redundant calls do you optimize the escaping towers. Rewriting the library (A) optimizes necessary work before questioning necessity; allocations (C) may matter but the graph says serialize dominates; threads (D) don't fix per-request CPU.",
                "hint": "Width means 'often' — can the work be skipped instead of sped up?",
                "objectives": ["Interpret flame graphs", "Eliminate work before optimizing"],
                "mins": 12,
                "evidence": ["Prioritizes call reduction over micro-tuning"]
            },
            {
                "id": "cpp-perf-sc2",
                "title": "Cache Optimization: Row vs Column",
                "domain_id": "perf-optimization",
                "situation": "A 4096x4096 matrix is stored row-major in a vector. A column-normalization pass iterates columns in the outer loop and rows in the inner loop. It runs 8x slower than the row pass, with perf showing high cache-miss rates and the CPU stalled on memory.",
                "prompt": "What is the fix?",
                "choices": [
                    "Buy faster RAM",
                    "Transpose the loop order (rows outer, columns inner) or transpose the data layout so the inner loop walks contiguous memory — sequential access prefetches; strided column access defeats it",
                    "Use a bigger L3 cache CPU",
                    "Parallelize the column loop across threads"
                ],
                "answer": 1,
                "why": "Row-major + column-outer traversal strides 16KB per access (4096 x 4 bytes), touching a new cache line every element and defeating the prefetcher — the classic cache-oblivious failure. Walking rows in the inner loop makes access sequential: one miss per 16 floats, then prefetch streams. Hardware (A/C) can't fix an algorithmic access pattern; threading (D) multiplies the memory traffic.",
                "hint": "How many bytes apart are consecutive accesses in the inner loop?",
                "objectives": ["Optimize for cache locality", "Match traversal to layout"],
                "mins": 10,
                "evidence": ["Reorders loops for sequential access"]
            },
            {
                "id": "cpp-perf-sc3",
                "title": "Allocation Reduction in the Parser",
                "domain_id": "perf-optimization",
                "situation": "A log parser processes 500k lines/sec but spends 45% of CPU in malloc/free. Each line creates several std::strings and a vector of tokens. The strings are short-lived — used within one line's processing then discarded.",
                "prompt": "What allocation strategy fits this short-lived pattern?",
                "choices": [
                    "Use a custom global new/delete override",
                    "Reuse buffers: string_views into the line buffer instead of owning strings, reserve() token vectors and clear() them per line, or use a per-line arena/bump allocator",
                    "Switch to a faster malloc implementation only",
                    "Process fewer lines per second"
                ],
                "answer": 1,
                "why": "Short-lived, same-size-ish allocations are the arena/bump-allocator sweet spot — or better, avoid owning allocations entirely with string_view into the input buffer and reused (reserved, cleared) containers. A faster malloc (C) helps marginally but the count is the problem; global new overrides (A) are a blunt instrument; throttling (D) surrenders throughput.",
                "hint": "The allocations all die within microseconds — what allocation pattern matches that lifetime?",
                "objectives": ["Reduce allocation overhead", "Apply arena allocation"],
                "mins": 12,
                "evidence": ["Proposes views + reused buffers/arena"]
            },
            {
                "id": "cpp-perf-sc4",
                "title": "Algorithm Choice Beats Micro-Tuning",
                "domain_id": "perf-optimization",
                "situation": "A deduplication step does a linear scan over a 2M-element vector for each of 500k lookups — 30 minutes runtime. A teammate is hand-unrolling the scan loop with SIMD intrinsics, projecting a 4x speedup to ~7 minutes.",
                "prompt": "What is the right call?",
                "choices": [
                    "Approve the SIMD work — 4x is a big win",
                    "Change the algorithm: sort + binary search or unordered_set turns O(n) lookups into O(log n)/O(1) — from 30 minutes to seconds, dwarfing the 4x micro-tune",
                    "Both: SIMD first, then the algorithm change",
                    "Buy a faster CPU"
                ],
                "answer": 1,
                "why": "Complexity class dominates constants: 500k x 2M linear scans is 10^12 comparisons; a hash set makes it ~500k operations — a 1000x+ win versus the 4x from SIMD heroics. Optimize the algorithm first, then micro-tune the new hot spot if needed. SIMD-first (A/C) polishes a fundamentally wrong approach; hardware (D) buys maybe 30%.",
                "hint": "Compare 4x against the gap between O(n) and O(1) per lookup.",
                "objectives": ["Prioritize algorithmic wins", "Recognize complexity-class issues"],
                "mins": 10,
                "evidence": ["Replaces linear scan with hash set"]
            },
            {
                "id": "cpp-perf-sc5",
                "title": "Branch Prediction: The Sorted Advantage",
                "domain_id": "perf-optimization",
                "situation": "A filter loop `if (data[i] > threshold)` over 100M random floats takes 2.1s. Sorting the data first (0.4s) drops the filter to 0.5s — total 0.9s. The team is uneasy: 'sorting to make a branch faster feels like a hack.'",
                "prompt": "Is the sort-then-filter legitimate, and why does it work?",
                "choices": [
                    "No — it's a hack; rewrite with branchless arithmetic instead",
                    "Yes, when reused: sorted data makes the branch perfectly predictable (all-false then all-true), eliminating mispredict penalties (~15-20 cycles each); it's legitimate if the sorted order is reused or the win exceeds sort cost",
                    "No — the CPU will learn the random pattern eventually",
                    "Yes, always sort before every loop"
                ],
                "answer": 1,
                "why": "Random data mispredicts ~50% of branches at ~15+ cycles each; sorted data predicts ~100% — the physics is real, not a hack. But it's only a win when the math works: sort cost amortized over reuse, or when order doesn't matter. Branchless (A) is the alternative when sorting isn't affordable; CPUs can't learn randomness (C); 'always sort' (D) ignores the cost side.",
                "hint": "What does the branch predictor see in random data versus sorted data?",
                "objectives": ["Understand branch prediction", "Evaluate sort-for-predictability"],
                "mins": 10,
                "evidence": ["Explains predictability win with cost check"]
            },
            {
                "id": "cpp-perf-sc6",
                "title": "Vectorization: Why Isn't It SIMD?",
                "domain_id": "perf-optimization",
                "situation": "A simple loop `for (i) c[i] = a[i] + b[i];` over float arrays isn't auto-vectorized per the optimization report: 'loop not vectorized: possible dependence'. The arrays are raw pointers passed to the function.",
                "prompt": "What blocks vectorization and what is the fix?",
                "choices": [
                    "The CPU doesn't support SIMD",
                    "Pointer aliasing: the compiler can't prove c doesn't overlap a/b, so it can't reorder; fix with __restrict__ (or -fno-strict-aliasing review / std::span with restrict semantics) to promise non-overlap",
                    "The loop is too simple for the vectorizer",
                    "Unroll the loop manually 8x"
                ],
                "answer": 1,
                "why": "The vectorizer must preserve semantics: if c aliases a, vectorized stores could clobber not-yet-loaded elements — so possible aliasing blocks it. __restrict__ (or restructuring to provably-separate spans) gives the compiler the non-overlap guarantee it needs. The CPU (A) surely supports SIMD for float adds; simplicity (C) is what vectorizers love; manual unrolling (D) doesn't resolve the dependence question.",
                "hint": "What can't the compiler prove about three raw pointers?",
                "objectives": ["Diagnose vectorization blockers", "Apply restrict for aliasing"],
                "mins": 10,
                "evidence": ["Adds restrict to enable vectorization"]
            },
            {
                "id": "cpp-perf-sc7",
                "title": "Inlining: The Call Overhead Mirage",
                "domain_id": "perf-optimization",
                "situation": "Profiling shows 12% of time in a tiny 3-line accessor called 2B times. A developer marks it `inline` and sees no change — 'inline is broken'. The function is defined in a .cpp file; the callers are in other TUs.",
                "prompt": "Why didn't inline help, and what actually fixes it?",
                "choices": [
                    "inline is just a hint; use __forceinline everywhere",
                    "inline doesn't cross TU boundaries at compile time without LTO: move the definition to the header (true inline availability) or enable link-time optimization (-flto) so the linker can inline across TUs",
                    "The profiler is wrong about the 12%",
                    "Make the accessor a macro"
                ],
                "answer": 1,
                "why": "`inline` is a linkage/ODR directive, not an inlining command — and crucially, a .cpp-defined function isn't visible to other TUs' optimizers at all, so no inlining decision is even possible there. Header definition makes the body available everywhere; LTO lets the linker optimize across TUs. __forceinline (A) can't inline what it can't see; macros (D) trade a build problem for a correctness problem.",
                "hint": "Can the optimizer inline a function body it was never shown?",
                "objectives": ["Understand inline vs LTO", "Fix cross-TU inlining"],
                "mins": 10,
                "evidence": ["Moves definition to header or enables LTO"]
            }
        ],
        "modern-cpp": [
            {
                "id": "cpp-modern-sc1",
                "title": "Smart Pointer Selection: The Factory",
                "domain_id": "modern-cpp",
                "situation": "A factory creates polymorphic `Renderer` objects. Some callers own the result exclusively; one registry needs shared ownership with weak observers. The current code returns raw pointers with a comment saying 'caller deletes'. Leaks are rampant.",
                "prompt": "What ownership design fixes this?",
                "choices": [
                    "Return shared_ptr everywhere — sharing is safest",
                    "Return unique_ptr by default (explicit exclusive ownership, zero overhead); the registry converts to shared_ptr where genuinely shared, observers hold weak_ptr",
                    "Return raw pointers but document better",
                    "Return shared_ptr and never use weak_ptr"
                ],
                "answer": 1,
                "why": "unique_ptr is the default: it documents exclusive ownership at the type level and costs nothing. shared_ptr everywhere (A) pays atomic refcounting on every copy and invites cycles; observers must be weak_ptr or they keep objects alive. Raw pointers (C) are the status quo that leaks. The rule: unique by default, shared when shared, weak for non-owning observation.",
                "hint": "Which ownership is the common case — and what should the default express?",
                "objectives": ["Select smart pointer types", "Design ownership policies"],
                "mins": 10,
                "evidence": ["Defaults to unique_ptr, shares deliberately"]
            },
            {
                "id": "cpp-modern-sc2",
                "title": "Move Semantics: The Return Trip",
                "domain_id": "modern-cpp",
                "situation": "A function builds a 10MB `std::vector<Result>` and returns it. A reviewer insists on an out-parameter (`void fill(std::vector<Result>&)`) to 'avoid the copy'. The codebase is C++17.",
                "prompt": "Is the out-parameter needed?",
                "choices": [
                    "Yes — returning large vectors always copies",
                    "No: NRVO/RVO elides the copy (guaranteed elision in C++17 for prvalues), and even without elision the move constructor transfers the buffer — the out-parameter is obsolete pessimization",
                    "Yes, but only for vectors over 1MB",
                    "Return a shared_ptr to the vector instead"
                ],
                "answer": 1,
                "why": "C++17 guarantees copy elision for prvalue returns, and named-return (NRVO) is near-universally applied; the fallback is a move, not a copy — the 10MB buffer is transferred, never duplicated. Out-parameters (A) pessimise readability for zero gain and defeat elision reasoning. Size thresholds (C) misunderstand moves; shared_ptr (D) adds refcounting to a value that has one owner.",
                "hint": "What does the move constructor do to a vector's buffer — copy it or steal it?",
                "objectives": ["Apply move semantics", "Trust guaranteed copy elision"],
                "mins": 10,
                "evidence": ["Returns by value, cites elision/move"]
            },
            {
                "id": "cpp-modern-sc3",
                "title": "constexpr: Compile-Time Lookup Table",
                "domain_id": "modern-cpp",
                "situation": "A CRC table of 256 entries is computed at startup on every process launch (~2ms) and in every unit test binary. The computation is pure: no I/O, no randomness. The table never changes.",
                "prompt": "What is the modern C++ fix?",
                "choices": [
                    "Compute it once and hardcode the 256 numbers as literals",
                    "Make the generator constexpr and the table constinit/constexpr — computed at compile time, zero startup cost, and the compiler verifies the computation",
                    "Cache it in a file and load at startup",
                    "It's only 2ms — leave it"
                ],
                "answer": 1,
                "why": "constexpr moves pure computation to compile time: the table lands in the binary ready-made, startup cost vanishes, and the values stay derived from the algorithm (unlike hardcoded literals (A) which rot when the algorithm changes). File caching (C) adds I/O and deployment surface for a pure function; 'only 2ms' (D) ignores the multiplied cost across every test binary and process.",
                "hint": "The computation is pure and the result is constant — when must it run?",
                "objectives": ["Apply constexpr", "Shift pure computation to compile time"],
                "mins": 10,
                "evidence": ["Makes table generation constexpr"]
            },
            {
                "id": "cpp-modern-sc4",
                "title": "Concepts vs SFINAE: The Constrained Template",
                "domain_id": "modern-cpp",
                "situation": "A template `process(T)` must only accept arithmetic types. The legacy code uses `std::enable_if_t<std::is_arithmetic_v<T>>` in the return type. New hires can't read it, and misuse produces 200-line substitution errors. The codebase is C++20.",
                "prompt": "What is the modern replacement?",
                "choices": [
                    "Keep SFINAE — it works and everyone's used to it",
                    "Concepts: `template<std::integral T>` or a requires-clause — constraints are readable, checked at the declaration, and misuse yields a one-line 'constraints not satisfied' error",
                    "static_assert inside the function body",
                    "Overload for every arithmetic type manually"
                ],
                "answer": 1,
                "why": "Concepts check constraints at the point of declaration with clear diagnostics, versus SFINAE's substitution-failure novels buried in overload resolution. Readability for new hires is a real maintenance win. static_assert (C) fires later with worse overload behavior (no SFINAE-friendly exclusion); manual overloads (D) explode combinatorially; 'works' (A) ignores the diagnostic and readability cost.",
                "hint": "Where should the constraint be checked — deep in substitution, or at the declaration?",
                "objectives": ["Apply C++20 concepts", "Replace SFINAE with concepts"],
                "mins": 10,
                "evidence": ["Rewrites constraint as concept"]
            },
            {
                "id": "cpp-modern-sc5",
                "title": "Ranges: The Pipeline Rewrite",
                "domain_id": "modern-cpp",
                "situation": "A data-prep step chains: filter nulls, transform to scores, take top 100, then sort. The current code uses three temporary vectors and four loops. It's correct but allocates heavily and the intermediate steps are hard to follow.",
                "prompt": "How do ranges improve this?",
                "choices": [
                    "Ranges are just syntax sugar; keep the loops",
                    "Compose a lazy view pipeline: `data | filter(...) | transform(...) | take(100)` then sort — no intermediate vectors, single readable expression of intent",
                    "Rewrite with raw for loops but fewer temporaries",
                    "Use ranges but materialize each stage for debuggability"
                ],
                "answer": 1,
                "why": "Views are lazy: the pipeline fuses into essentially one pass with no intermediate allocations, and the composed expression reads as the algorithm itself (filter->transform->take) instead of four loops shuffling temporaries. Materializing stages (D) keeps the allocation cost; raw loops (C) keep the readability cost; dismissing ranges (A) leaves both costs on the table.",
                "hint": "What if the intermediate vectors never had to exist?",
                "objectives": ["Compose ranges pipelines", "Exploit view laziness"],
                "mins": 10,
                "evidence": ["Builds lazy filter/transform/take pipeline"]
            },
            {
                "id": "cpp-modern-sc6",
                "title": "Coroutines: The Async Read Chain",
                "domain_id": "modern-cpp",
                "situation": "A network service chains 5 async reads with callbacks; error handling is scattered across lambdas and the 'flow' is unreadable. The team considers coroutines (C++20) but worries about 'hidden allocations and magic'.",
                "prompt": "When are coroutines the right call here?",
                "choices": [
                    "Never — callbacks are explicit and coroutines hide control flow",
                    "Yes: `co_await` linearizes the chain into straight-line code with normal try/catch error handling; the 'magic' is a well-defined state machine, and allocation concerns are addressed by custom promise allocators / elision",
                    "Only if the team rewrites everything in async style first",
                    "Use threads instead — simpler mental model"
                ],
                "answer": 1,
                "why": "Coroutines turn callback spaghetti into sequential-looking code where errors propagate via exceptions normally — the readability win is exactly for multi-step async chains. The state machine is compiler-generated but deterministic, not magic; frame allocations can be customized away. Threads (D) trade a readability problem for a concurrency problem; 'never' (A) keeps the scattered error handling that's already hurting.",
                "hint": "What does the error-handling code look like in each style?",
                "objectives": ["Evaluate coroutines for async chains", "Address coroutine cost concerns"],
                "mins": 12,
                "evidence": ["Justifies co_await with error-handling win"]
            },
            {
                "id": "cpp-modern-sc7",
                "title": "RAII: The Lock That Leaks",
                "domain_id": "modern-cpp",
                "situation": "A function does `mutex.lock(); ...; if (error) return; ...; mutex.unlock();` A new early-return was added last week and production shows the mutex permanently held after certain errors — the service wedges. The team proposes 'be careful with returns'.",
                "prompt": "What is the durable fix?",
                "choices": [
                    "Audit every return path and add unlock() calls",
                    "RAII: std::lock_guard / std::scoped_lock — the destructor unlocks on every exit path including exceptions; manual lock/unlock is the bug class itself",
                    "Ban early returns in locked regions",
                    "Use a recursive mutex so double-lock is safe"
                ],
                "answer": 1,
                "why": "Manual lock/unlock makes every future edit a potential deadlock — the bug class is 'unpaired unlock on some path', which code review cannot reliably prevent. RAII ties the unlock to scope exit: correct on all paths, including exceptions, by construction. Auditing (A) and banning returns (C) fight human fallibility with policy; recursive mutexes (D) mask rather than fix pairing bugs.",
                "hint": "Which construct makes the wrong code unrepresentable instead of merely discouraged?",
                "objectives": ["Apply RAII to locking", "Eliminate manual lock/unlock"],
                "mins": 8,
                "evidence": ["Replaces manual unlock with lock_guard"]
            },
            {
                "id": "cpp-modern-sc8",
                "title": "string_view: The Substring That Dangles",
                "domain_id": "modern-cpp",
                "situation": "A parser returns `std::string_view` into a temporary: `std::string_view get() { std::string s = build(); return std::string_view(s); }` Tests pass (the memory isn't reused yet in small tests); production crashes intermittently.",
                "prompt": "What is the bug and the rule?",
                "choices": [
                    "string_view is unsafe and should never be used",
                    "The view dangles: the temporary string dies at return, leaving a view of freed memory — string_view is non-owning, so never return it pointing at locals/temporaries; return std::string (moved) or ensure the viewed data outlives the view",
                    "Tests should use bigger inputs",
                    "Make the local static"
                ],
                "answer": 1,
                "why": "string_view is a non-owning (pointer, length) pair — returning one over a destroyed local is use-after-free that small tests mask (freed memory often still mapped). The rule: a view must never outlive its viewed data. Return an owning std::string (moves are cheap) or view into longer-lived storage. Banning string_view (A) discards its real value for parameters; static locals (D) introduce thread-safety and lifetime puzzles.",
                "hint": "Who owns the characters the view points at after the return?",
                "objectives": ["Use string_view safely", "Respect non-owning view lifetimes"],
                "mins": 10,
                "evidence": ["States view-must-not-outlive-data rule"]
            }
        ]
    }
}

LESSONS = {
    "comptia-infra": {
        "exam-strategy": [
            {
                "_id": "infra-lesson-exam-strategy-pbq-speed",
                "id": "infra-lesson-exam-strategy-pbq-speed",
                "title": "PBQ Command-Line Speed Runs",
                "domain_id": "exam-strategy",
                "concepts": [
                    "PBQs award partial credit per checkpoint: every verified fix (service restarted, port listening, config corrected) scores even if you don't finish the whole scenario, so front-load the easy checkpoints.",
                    "The 10-minute triage loop: status -> logs -> ports -> config. `systemctl status`, `journalctl -xe`, `ss -tlnp`, then read the config the log points at. Never start editing before the log tells you what's wrong.",
                    "Budget PBQs at 8-12 minutes each: set a mental timer, and when it rings, bank your checkpoints and move on — one perfect PBQ is worth less than one good PBQ plus six answered multiple-choice questions.",
                    "Read the PBQ task text twice before touching the terminal: half of PBQ failures come from fixing the wrong thing fast instead of the right thing deliberately."
                ],
                "example": {
                    "code": "systemctl status nginx  # is it running?\njournalctl -u nginx -n 20  # why did it fail?\nss -tlnp | grep 443       # is anything listening?\nnginx -t                  # is the config valid?",
                    "walkthrough": "This four-command sequence answers the four questions that solve 80% of service PBQs: state, cause, network, config. Each command's output tells you whether to go deeper or move to the next check — you never guess, and you never edit blind."
                },
                "pitfalls": [
                    "Pitfall: editing configs before reading logs — you create a second problem on top of the first and lose the trail.",
                    "Pitfall: rebooting the VM 'to fix it' — reboots destroy log evidence, take minutes, and rarely fix config errors.",
                    "Pitfall: perfectionism — spending 25 minutes polishing one PBQ while 15 multiple-choice questions go unanswered."
                ],
                "try_it": "Spin up any Linux VM, break nginx three different ways (bad port, bad config syntax, stopped service), and time yourself diagnosing each with only the four-command sequence — aim for under 3 minutes per break."
            },
            {
                "_id": "infra-lesson-exam-strategy-stem-parsing",
                "id": "infra-lesson-exam-strategy-stem-parsing",
                "title": "Scenario Stem Parsing Under Pressure",
                "domain_id": "exam-strategy",
                "concepts": [
                    "Read the last sentence first: it defines the decision. Everything before it is either a constraint that discriminates between choices or a distractor.",
                    "Constraints are numbers and requirements (RTO 2h, 100 Mbps WAN, 50 switches, HIPAA) — circle them mentally and eliminate any choice that violates one.",
                    "Distractors are impressive-but-irrelevant details (company history, brand names, exact headcount when the question is technical) — notice them, then ignore them.",
                    "For BEST/MOST questions, the tiebreaker is always scale: which choice's advantage grows with the numbers in the stem?"
                ],
                "example": {
                    "code": "Stem: 'Hospital, HIPAA, RTO 2h, 100 Mbps WAN, 8TB data.'\nQ: 'Which backup architecture meets the RTO?'\n-> HIPAA = encryption constraint (not architecture)\n-> 8TB / 100Mbps = ~7.4 days for off-site full restore >> 2h RTO\n-> Eliminate anything requiring off-site full restores.",
                    "walkthrough": "The last sentence asks about RTO, so the discriminating constraint is the math: 8TB over 100 Mbps cannot restore in 2 hours. HIPAA matters for encryption-in-transit, not for the architecture choice. One calculation eliminates two choices instantly."
                },
                "pitfalls": [
                    "Pitfall: keyword matching — picking the choice that repeats a stem buzzword (like HIPAA) instead of the one that satisfies the actual question.",
                    "Pitfall: re-reading the whole stem three times — if you're stuck, you've missed the constraint; re-read only the last sentence and the numbers.",
                    "Pitfall: choosing the most advanced technology — exams test appropriateness, not impressiveness."
                ],
                "try_it": "Take 5 practice scenario questions, cover the choices, and write down in one line what the last sentence asks plus the discriminating numbers — then uncover and eliminate. Track how often the elimination alone picks the answer."
            }
        ],
        "capacity-planning": [
            {
                "_id": "infra-lesson-capacity-right-sizing",
                "id": "infra-lesson-capacity-right-sizing",
                "title": "Right-Sizing VM Resources",
                "domain_id": "capacity-planning",
                "concepts": [
                    "Size on p95 utilization, not averages: averages hide the peaks that cause outages, while p95 captures real demand plus natural headroom.",
                    "Separate steady from spiky workloads: steady VMs get fixed sizes near p95, spiky ones get burstable classes or autoscaling so you pay for peaks only when they happen.",
                    "Memory and CPU size independently: most fleets are CPU-idle but memory-heavy (or vice versa) — right-size each dimension on its own p95.",
                    "Stage every resize with rollback: change one workload group at a time, watch for a full business cycle, and keep the revert command ready — evidence beats arguments with nervous engineering teams."
                ],
                "example": {
                    "code": "# Per-VM p95 over 30 days (example via cloud metrics CLI)\n# vm-web-04: p95 CPU 22% of 8 vCPU -> target 4 vCPU (p95 ~44%)\n# vm-web-04: p95 mem 61% of 32GB  -> target 16GB (p95 ~75%)\n# Rollback: snapshot the sizing change; revert = one API call",
                    "walkthrough": "The p95 math turns 'feels over-provisioned' into a defensible target: halving vCPU still leaves the p95 at 44%, well clear of saturation. Doing it per workload group with a one-command revert is what gets the change approved."
                },
                "pitfalls": [
                    "Pitfall: sizing on averages — a VM averaging 20% CPU with 95% spikes will fall over the first time you halve it.",
                    "Pitfall: resizing everything at once — one bad assumption becomes a fleet-wide incident with no clean rollback.",
                    "Pitfall: ignoring memory — CPU-rightsized VMs that OOM are worse than the waste you started with."
                ],
                "try_it": "Pull 30 days of CPU/memory metrics for 5 VMs you own, compute p95 for each, and propose new sizes with the headroom math written out — then check whether any p95 would exceed 70% after the change."
            }
        ],
        "hybrid-cloud": [
            {
                "_id": "infra-lesson-hybrid-placement-matrix",
                "id": "infra-lesson-hybrid-placement-matrix",
                "title": "Hybrid Workload Placement Matrix",
                "domain_id": "hybrid-cloud",
                "concepts": [
                    "Place by workload shape: steady-state systems (ERP, scheduling, core banking) gain nothing from elasticity and stay where controls exist; spiky systems (analytics, rendering, seasonal web) pay for idle capacity on-prem and belong in cloud.",
                    "Data sensitivity is a placement input, not a veto: PHI/financial data can live in cloud with the right controls, but audit and residency requirements may still anchor it on-prem — evaluate, don't assume.",
                    "Data gravity decides ties: the 40TB dataset's location dictates where its compute runs, because moving terabytes nightly is a permanent tax.",
                    "Revisit placement yearly: workload shapes change (that 'spiky' pipeline becomes 24/7), and last year's right answer rots into this year's waste."
                ],
                "example": {
                    "code": "Workload            | Shape    | Data        | Placement\n--------------------|----------|-------------|------------------\nPatient scheduling  | steady   | PHI, audit  | on-prem\nResearch analytics  | 6h/week  | de-identified| cloud (spot GPUs)\nClaims archive      | cold     | regulated   | cloud archive tier\nCI runners          | spiky    | code        | cloud autoscale",
                    "walkthrough": "Each row scores shape against sensitivity: the steady PHI system stays where the audit controls are, the spiky GPU job rents instead of buying 200 idle GPUs, cold regulated data gets cheap archive storage, and spiky CI scales to zero. No absolutism — every placement earns its row."
                },
                "pitfalls": [
                    "Pitfall: 'cloud-first' or 'on-prem-first' as policy — blanket rules optimize one workload shape at every other shape's expense.",
                    "Pitfall: placing compute far from its data — the nightly terabyte transfer becomes a permanent cost and SLA risk.",
                    "Pitfall: set-and-forget placement — a workload that goes from batch to real-time needs re-placement, not nostalgia."
                ],
                "try_it": "List 6 workloads you know, score each on shape (steady/spiky), data sensitivity, and data gravity, and place each — then find one placement from last year that the scores say should move."
            }
        ],
        "automation-iaac": [
            {
                "_id": "infra-lesson-automation-idempotency",
                "id": "infra-lesson-automation-idempotency",
                "title": "Idempotent Infrastructure Scripts",
                "domain_id": "automation-iaac",
                "concepts": [
                    "Idempotent means re-runnable: running the script twice produces the same end state as running it once — this is what makes automation safe to retry after partial failures.",
                    "The pattern is check-then-converge: every action first reads current state (does the VM exist? is the disk attached? is the package installed?) and only acts on the gap.",
                    "Desired-state tools (Terraform, Ansible) are idempotent by design; imperative scripts must earn it — a bash script that blindly runs `useradd` twice is a bug, not automation.",
                    "Test idempotency explicitly: run the script, run it again, and diff the world — the second run should report zero changes."
                ],
                "example": {
                    "code": "# Non-idempotent: creates dupes on retry\naws ec2 run-instances --count 1 ...\n\n# Idempotent: converge toward desired state\nif ! vm_exists \"web-04\"; then\n  aws ec2 run-instances --tag Name=web-04 ...\nfi\n# Better: let Terraform/Ansible own the state check",
                    "walkthrough": "The first version creates a second VM every retry — the exact failure mode that teaches teams to fear re-running automation. The guarded version checks existence first, so retries converge instead of duplicating. The lesson: retries are normal, so scripts must survive them."
                },
                "pitfalls": [
                    "Pitfall: 'run once' assumptions — every script will eventually be re-run after a partial failure; design for it on day one.",
                    "Pitfall: checking the wrong state — verifying the VM exists but not that the disk attached still duplicates disks.",
                    "Pitfall: manual cleanup runbooks as the idempotency strategy — they institutionalize fragility instead of fixing it."
                ],
                "try_it": "Take any deploy script you own, run it twice against a test environment, and list every duplicate or error the second run creates — then add existence checks until the second run is a clean no-op."
            }
        ],
        "cloud-arch": [
            {
                "_id": "infra-lesson-cloud-arch-ha-patterns",
                "id": "infra-lesson-cloud-arch-ha-patterns",
                "title": "High-Availability Architecture Patterns",
                "domain_id": "cloud-arch",
                "concepts": [
                    "Design for failure domains: spread across availability zones for rack/power/network failures, and across regions only when the business cost of a regional outage justifies the complexity.",
                    "Stateless tiers scale horizontally behind load balancers; stateful tiers need explicit strategies — replication with automated failover for databases, shared/distributed storage for files, externalized sessions for app servers.",
                    "Active-passive is simpler and cheaper but fails over slowly (DNS, promotion lag); active-active is seamless but demands conflict resolution — pick by RTO, not by fashion.",
                    "Health checks are the nervous system: load balancers, auto-scalers, and failover all depend on accurate health signals — a bad health check turns a single failure into a cascading one."
                ],
                "example": {
                    "code": "# Classic 3-tier HA sketch\n# Tier 1: ALB across 3 AZs, health-checked, auto-scaling 3-30\n# Tier 2: app servers stateless, sessions in ElastiCache\n# Tier 3: RDS Multi-AZ (sync standby), read replicas for scale\n# DNS: Route53 health-checked failover to passive region",
                    "walkthrough": "Every tier has its own HA story matched to its statefulness: the stateless web tier just scales, sessions move to a shared store so any server can serve any user, the database uses synchronous standby for failover, and DNS provides the regional escape hatch. No tier depends on a single box."
                },
                "pitfalls": [
                    "Pitfall: single-AZ databases with 'we'll restore from backup' — restores take hours; Multi-AZ failover takes minutes.",
                    "Pitfall: sticky sessions as a substitute for shared session state — they break the moment auto-scaling replaces an instance.",
                    "Pitfall: health checks that always return 200 — the load balancer keeps sending traffic to a dead app."
                ],
                "try_it": "Draw your most important service's architecture, mark every single point of failure (single AZ, single instance, local sessions), and write the one-line fix for each — then rank the fixes by outage cost avoided."
            }
        ],
        "linux-admin": [
            {
                "_id": "infra-lesson-linux-admin-systemd-playbook",
                "id": "infra-lesson-linux-admin-systemd-playbook",
                "title": "systemd Troubleshooting Playbook",
                "domain_id": "linux-admin",
                "concepts": [
                    "Units are the model: services, sockets, timers, and mounts are all units with states (active, failed, inactive) — `systemctl status` is always step one.",
                    "The journal is the memory: `journalctl -u <service>` shows that unit's logs, `-xe` adds explanations, `--since '10 min ago'` bounds the search — most 'mystery' failures confess here.",
                    "Dependencies are the map: `systemctl list-dependencies` and the After=/Requires= directives explain ordering failures — a service that 'randomly' fails at boot usually starts before its dependency.",
                    "Overrides beat edits: never modify vendor unit files in /usr/lib — use `systemctl edit` to create drop-ins in /etc, so updates don't wipe your changes."
                ],
                "example": {
                    "code": "systemctl status app.service        # state + recent log tail\njournalctl -u app.service -n 50   # the failure story\nsystemctl list-dependencies app.service  # what must start first\nsystemctl edit app.service        # safe override drop-in\nsystemctl daemon-reload && systemctl restart app.service",
                    "walkthrough": "This is the complete loop: observe state, read the story, check ordering, fix safely via drop-in, reload, restart. Following it in order means you never edit a unit file that an update will overwrite, and you never restart before understanding the failure."
                },
                "pitfalls": [
                    "Pitfall: editing /usr/lib/systemd unit files directly — the next package update silently reverts your fix.",
                    "Pitfall: `systemctl restart` as the first step — it destroys the failed state that would have told you the cause.",
                    "Pitfall: forgetting daemon-reload after unit changes — systemd keeps running the old definition and your fix 'doesn't work'."
                ],
                "try_it": "Break a test service three ways (bad ExecStart path, missing After= dependency, wrong permissions), and recover each using only status, journalctl, list-dependencies, and edit — no reinstalling."
            }
        ]
    },
    "cpp": {
        "interview-prep": [
            {
                "_id": "cpp-lesson-interview-code-review",
                "id": "cpp-lesson-interview-code-review",
                "title": "Talking Through Code Reviews",
                "domain_id": "interview-prep",
                "concepts": [
                    "Review the code, not the coder: phrase every finding as an observation about the code ('this loop is O(n^2)') plus its consequence ('at 50k entries that's 2.5B comparisons'), never as a judgment of the author.",
                    "Separate blocking from nitpicking: correctness, UB, lifetime, and concurrency issues block; style preferences get labeled 'nit' and never hold up a merge.",
                    "Always propose the fix shape, not just the problem: 'use string_view here to avoid the copy' teaches; 'this copies' just criticizes.",
                    "In interviews, narrate your review out loud in priority order — interviewers score whether you find the dangling reference before you comment on brace style."
                ],
                "example": {
                    "code": "// Review comment, blocking:\n// `process(const std::string& s)` stores a string_view of `s` in the\n// returned struct — the view dangles when the caller's string dies.\n// Suggest: return std::string (moved), or take std::string by value\n// and move from it.",
                    "walkthrough": "This comment names the mechanism (dangling view), the trigger (caller's string lifetime), and two concrete fixes with their trade-offs. That's the bar: mechanism + consequence + fix, in three lines."
                },
                "pitfalls": [
                    "Pitfall: leading with style nits — it signals you missed the lifetime bug on line 12 while bikeshedding line 3.",
                    "Pitfall: 'LGTM' on code with UB — approving a data race makes it your incident too.",
                    "Pitfall: rewriting the author's code in review — suggest the shape, let them own the implementation."
                ],
                "try_it": "Take any 100-line C++ file, review it aloud in 10 minutes with findings ranked blocking/nit, and check you caught lifetime and concurrency issues before style."
            },
            {
                "_id": "cpp-lesson-interview-estimating",
                "id": "cpp-lesson-interview-estimating",
                "title": "Estimating Algorithm Costs Live",
                "domain_id": "interview-prep",
                "concepts": [
                    "Fermi-estimate in layers: payload bytes, then per-entry overhead (allocations, pointers, padding), then container overhead (buckets, nodes) — overhead usually dominates, often 2-3x the payload.",
                    "Know the canonical sizes: pointer 8B, std::string 32B (SSO), unordered_map node ~32B+ overhead, cache line 64B, page 4KB — these are your estimating atoms.",
                    "Time estimates work the same way: operations per second per core (~3B simple ops), memory bandwidth (~20GB/s), network RTT — then divide the workload by the bottleneck resource.",
                    "State assumptions out loud and refine: 'assuming 20-char keys and SSO disabled...' — interviewers grade the reasoning chain, not the final number."
                ],
                "example": {
                    "code": "// 50M sessions in unordered_map<string, Session>\n// per entry: node ~48B + string alloc ~52B + Session 64B + bucket ~8B\n// ≈ 170B/entry x 50M ≈ 8.5GB  (payload alone was ~4.2GB)\n// lever: flat_hash_map or sorted vector -> ~4.5GB",
                    "walkthrough": "The estimate decomposes into named components so the interviewer can follow and correct any atom. The lever falls out naturally: the overhead components (node, string alloc) are exactly what a flat container eliminates."
                },
                "pitfalls": [
                    "Pitfall: multiplying payload only — you'll be 2-3x low and miss the actual design insight.",
                    "Pitfall: false precision — '8.53GB' from guessed inputs is theater; '8-10GB' with named assumptions is engineering.",
                    "Pitfall: freezing on the number — the estimate is a means to the lever, not the deliverable."
                ],
                "try_it": "Estimate the memory of 10M ints in vector vs list vs unordered_set on paper, then verify with a 20-line program using mallinfo or a custom counter — calibrate your atoms."
            }
        ],
        "concurrency": [
            {
                "_id": "cpp-lesson-concurrency-mutex-vs-atomic",
                "id": "cpp-lesson-concurrency-mutex-vs-atomic",
                "title": "Mutex vs Atomic Decision Guide",
                "domain_id": "concurrency",
                "concepts": [
                    "Atomics are for single locations: counters, flags, and simple state machines on trivially-copyable types — one indivisible operation on one word.",
                    "Mutexes are for invariants across locations: 'transfer money' touches two balances that must change together — no atomic spans two words.",
                    "Cost shape differs: uncontended atomics are ~tens of cycles and lock-free; uncontended mutexes are similar, but contended mutexes sleep (good for long waits) while contended atomics spin (good for short waits).",
                    "volatile is not synchronization: it stops some compiler optimizations but provides no atomicity, no ordering, and no visibility guarantees — it has no place in threading decisions."
                ],
                "example": {
                    "code": "std::atomic<long long> total_requests{0};  // single counter -> atomic\ntotal_requests.fetch_add(1, std::memory_order_relaxed);\n\nstd::mutex m; Account a, b;  // two-account invariant -> mutex\n{ std::lock_guard g(m); a -= x; b += x; }",
                    "walkthrough": "The counter is one location: atomic, relaxed ordering since only the count matters. The transfer is a two-location invariant: only a mutex makes both updates indivisible to observers. The decision rule is structural, not stylistic."
                },
                "pitfalls": [
                    "Pitfall: atomic for multi-location invariants — two atomics don't compose into one atomic transaction.",
                    "Pitfall: mutex around a hot flag poll — serializes 32 threads to protect one byte; atomic<bool> exists for this.",
                    "Pitfall: reaching for volatile — it compiles, it runs, and it races."
                ],
                "try_it": "Audit three shared variables in a codebase you know: classify each as single-location or multi-location invariant, and check the primitive matches — convert any mismatches."
            },
            {
                "_id": "cpp-lesson-concurrency-lock-ordering",
                "id": "cpp-lesson-concurrency-lock-ordering",
                "title": "Deadlock-Free Lock Ordering",
                "domain_id": "concurrency",
                "concepts": [
                    "Deadlock needs four conditions (Coffman): mutual exclusion, hold-and-wait, no preemption, circular wait — break any one and deadlock is impossible; lock ordering breaks circular wait.",
                    "The rule: define a global order (by address, by layer, by documented rank) and always acquire in that order — two threads acquiring A-then-B can never deadlock with each other.",
                    "std::lock and std::scoped_lock acquire multiple mutexes atomically without deadlock — use them when the order isn't statically knowable.",
                    "Keep critical sections small and never call unknown code (callbacks, virtuals) while holding a lock — it hides lock acquisitions that violate your ordering."
                ],
                "example": {
                    "code": "// Global order: accounts before audit, always.\nvoid transfer(...) {\n    std::scoped_lock lock(m_accounts, m_audit);  // deadlock-free\n    ...\n}\n// Reporting path uses the SAME order, or the same scoped_lock.",
                    "walkthrough": "scoped_lock internally uses std::lock's deadlock-avoidance algorithm, so even if a future path wants the locks in a different conceptual order, acquisition is safe. The documented global order (accounts before audit) is the human-readable backup."
                },
                "pitfalls": [
                    "Pitfall: 'we'll be careful' instead of an enforced order — the AB-BA inversion always arrives via the new code path nobody reviewed for locking.",
                    "Pitfall: locking in destructors or callbacks — the hidden acquisition site that breaks the documented order.",
                    "Pitfall: try_lock retry loops without backoff — converts deadlock into livelock under contention."
                ],
                "try_it": "Map every mutex in one subsystem, draw the acquisition graph across all code paths, and find any cycle — then fix it with a documented order or scoped_lock."
            }
        ],
        "perf-optimization": [
            {
                "_id": "cpp-lesson-perf-flame-graph",
                "id": "cpp-lesson-perf-flame-graph",
                "title": "Reading a Profiler Flame Graph",
                "domain_id": "perf-optimization",
                "concepts": [
                    "Width is cost: a frame's horizontal width is its share of samples (CPU time) — wide plateaus are where the program lives; narrow towers are details.",
                    "Read top-down for the call chain and scan for width: the widest frame you can eliminate or shrink is the optimization target, not the most interesting-looking tower.",
                    "Eliminate before optimizing: caching a result, skipping redundant work, or choosing a better algorithm beats micro-tuning the wide frame every time.",
                    "Sample, don't guess: profiles must come from production-like workloads — optimizing a benchmark's hot path that never fires in production is negative work."
                ],
                "example": {
                    "code": "$ perf record -F 99 -g ./service   # sample with call graphs\n$ perf script | stackcollapse-perf.pl | flamegraph.pl > out.svg\n# Read: widest plateau = first target. Ask 'can this run less\n# often?' before 'can this run faster?'",
                    "walkthrough": "The workflow is mechanical: capture under realistic load, render, find the widest plateau, and interrogate necessity before speed. Most flame-graph wins come from deleting calls, not accelerating them."
                },
                "pitfalls": [
                    "Pitfall: optimizing the narrow tower because it's 'clearly inefficient' — 2% of samples optimized 10x is 0.2% total.",
                    "Pitfall: profiling debug builds — inlining and optimization change the shape completely; always profile optimized binaries with symbols.",
                    "Pitfall: one profile, permanent conclusions — workloads drift; re-profile after every significant change."
                ],
                "try_it": "Profile any program you own for 60 seconds under realistic load, render the flame graph, and write down the top-3 widest frames with a 'can it run less often?' answer for each."
            },
            {
                "_id": "cpp-lesson-perf-cache-layout",
                "id": "cpp-lesson-perf-cache-layout",
                "title": "Cache-Friendly Data Layout",
                "domain_id": "perf-optimization",
                "concepts": [
                    "CPUs move 64-byte cache lines, not bytes: touching one byte pulls 64, so sequential access gets 16 floats per miss while strided access pays a miss per element.",
                    "Structure-of-arrays beats array-of-structures for hot loops: iterating positions over 1M particles streams 4MB contiguously in SoA, versus striding over 64-byte structs touching 64MB in AoS.",
                    "Match traversal to layout: row-major storage demands row-inner loops; if the algorithm needs column access, transpose the data once instead of paying strided access forever.",
                    "False sharing is the coherence tax: keep independently-written fields on separate cache lines (alignas(64)) or watch cores serialize on the interconnect."
                ],
                "example": {
                    "code": "// AoS: 1M particles x 64B struct = 64MB touched per position pass\nstruct Particle { float x,y,z; /* ... 52 more bytes */ };\n// SoA: positions stream as 12MB contiguous\nstruct Particles { std::vector<float> x, y, z; /* ... */ };\n// Hot loop over x only: 5x fewer cache lines touched.",
                    "walkthrough": "The transform is mechanical: identify the hot field subset, split it into its own contiguous arrays, and watch the miss rate collapse. The win comes from the memory system, not the ALU — the math didn't change at all."
                },
                "pitfalls": [
                    "Pitfall: optimizing the ALU while the memory system starves — a 2x faster inner loop on cache-missing data gains nothing.",
                    "Pitfall: SoA everywhere — it complicates code; apply it to the hot loops the profiler names, not the whole codebase.",
                    "Pitfall: ignoring prefetch-friendliness — even SoA loses if the access pattern jumps randomly; sort or reorder for sequential access."
                ],
                "try_it": "Take a loop over an array-of-structs, measure its cache-miss rate with perf stat, convert to SoA, and measure again — record the miss-rate and wall-time deltas."
            }
        ],
        "modern-cpp": [
            {
                "_id": "cpp-lesson-modern-move-semantics",
                "id": "cpp-lesson-modern-move-semantics",
                "title": "Move Semantics in Practice",
                "domain_id": "modern-cpp",
                "concepts": [
                    "Move = steal the guts: a move constructor transfers the heap buffer pointer instead of copying 10MB, leaving the source in a valid-but-unspecified state — O(1) instead of O(n).",
                    "Return by value freely: C++17 guaranteed elision plus move fallback means `return big_vector;` never copies — out-parameters for 'performance' are obsolete pessimization.",
                    "std::move is a cast, not an action: it marks an lvalue as movable; the move constructor does the work — and moving from an object you still use is a bug.",
                    "Rule of five interaction: declaring a move constructor suppresses the copy operations — if your type should copy, declare or default them explicitly."
                ],
                "example": {
                    "code": "std::vector<Result> build() {\n    std::vector<Result> out;\n    out.reserve(100000);\n    // ... fill ...\n    return out;  // NRVO or move: buffer transferred, never copied\n}\nauto results = build();  // zero copies, zero moves (elided)",
                    "walkthrough": "The return transfers ownership of the buffer: either the compiler constructs directly into the caller's vector (elision) or the move constructor steals the pointer. Either way the 10MB is never duplicated — the code reads naturally and performs optimally."
                },
                "pitfalls": [
                    "Pitfall: `return std::move(out);` — inhibits NRVO and forces a move where elision would have been free.",
                    "Pitfall: moving from const objects — binds to the copy constructor instead, silently copying.",
                    "Pitfall: using a moved-from object beyond destruction/assignment — valid but unspecified state is not 'empty and safe to read'."
                ],
                "try_it": "Write a type with noisy copy/move constructors, return it from a function four ways (plain return, std::move return, out-param, const return), and log which operations actually run under -O2."
            },
            {
                "_id": "cpp-lesson-modern-constexpr",
                "id": "cpp-lesson-modern-constexpr",
                "title": "constexpr and consteval in Practice",
                "domain_id": "modern-cpp",
                "concepts": [
                    "constexpr shifts pure computation to compile time: lookup tables, hash constants, and parser tables get baked into the binary with zero startup cost.",
                    "consteval (C++20) is stricter: the function MUST run at compile time — use it when runtime execution would be a bug (e.g., compile-time-validated format strings).",
                    "constexpr functions can still run at runtime when given runtime arguments — the same code serves both worlds, which is why standard algorithms are increasingly constexpr.",
                    "constinit guarantees static initialization (no static-init-order fiasco) without requiring full constness — the right tool for globals that must be ready before main()."
                ],
                "example": {
                    "code": "constexpr uint32_t crc32_entry(size_t i) { /* pure math */ }\nconstexpr auto CRC_TABLE = [] {\n    std::array<uint32_t, 256> t{};\n    for (size_t i = 0; i < 256; ++i) t[i] = crc32_entry(i);\n    return t;\n}();  // computed once, at compile time",
                    "walkthrough": "The immediately-invoked lambda builds the table in a constexpr context, so the compiler emits 256 constants into .rodata — every process startup and every test binary skips the computation entirely, and the values stay derived from the algorithm."
                },
                "pitfalls": [
                    "Pitfall: assuming constexpr means compile-time — it means compile-time-capable; verify with static_assert or constinit where it matters.",
                    "Pitfall: constexpr with hidden runtime dependencies (RNG, I/O, virtual calls) — fails to constant-evaluate, sometimes silently falling back to runtime.",
                    "Pitfall: over-constexpring huge computations — multi-second compile-time table builds tax every developer's build; keep them proportional."
                ],
                "try_it": "Convert one startup-computed lookup table in a project to constexpr, add a static_assert on two entries, and compare binary startup time before/after."
            }
        ],
        "core-syntax": [
            {
                "_id": "cpp-lesson-core-const-correctness",
                "id": "cpp-lesson-core-const-correctness",
                "title": "const Correctness from Day One",
                "domain_id": "core-syntax",
                "concepts": [
                    "const is a compile-time contract: `const` on a method promises no mutation, `const` on a reference promises no mutation through that reference — the compiler enforces both.",
                    "Read declarations right-to-left: `const std::string&` is a reference to a const string; `std::string* const` is a const pointer to a mutable string — precision here prevents real bugs.",
                    "const-correctness is viral and that's good: one const object requires const accessors, which require const-correct callees — the chain pushes correctness through the whole design.",
                    "Retrofitting const is painful; starting const is free: default to const references for in-parameters and const methods for accessors, and remove const only with a reason."
                ],
                "example": {
                    "code": "class Config {\npublic:\n    const std::string& name() const { return name_; }  // accessor: const method, const ref return\n    void setName(const std::string& n) { name_ = n; }   // in-param: const ref, no copy\nprivate:\n    std::string name_;\n};",
                    "walkthrough": "The accessor is callable on const Config objects and returns without copying; the setter takes a const reference so callers pass temporaries safely. Every const here was a one-word decision that the compiler now enforces forever."
                },
                "pitfalls": [
                    "Pitfall: 'discards qualifiers' errors — they mean a const object met a non-const method; fix the method, not the caller's constness.",
                    "Pitfall: const_cast to 'fix' compilation — lies to the compiler; mutating a genuinely-const object is undefined behavior.",
                    "Pitfall: returning const values from functions — blocks move semantics for no benefit in modern C++."
                ],
                "try_it": "Take one class you wrote, make every accessor const and every in-parameter a const reference, and fix each compiler error by adding const (not removing it) — count how many latent mutation risks surface."
            }
        ],
        "stl-containers": [
            {
                "_id": "cpp-lesson-stl-choosing-containers",
                "id": "cpp-lesson-stl-choosing-containers",
                "title": "Choosing the Right Container",
                "domain_id": "stl-containers",
                "concepts": [
                    "Default to std::vector: contiguous storage gives the best iteration speed, cache behavior, and memory density — most programs' access pattern is 'iterate everything'.",
                    "Reach for node-based containers (list, map) only for iterator stability across insertions or true O(1) middle insertion with existing iterators — and measure, because cache misses often erase the theoretical win.",
                    "unordered_* trades ordering for average O(1) lookup but pays node overhead and hash cost; for small sizes (<~100 elements) a sorted vector with binary search often wins outright.",
                    "Know the invalidation rules cold: vector invalidates on reallocation (fix with reserve), deque invalidates on ends-insertion, node containers never invalidate on insert — pick by what your iterators must survive."
                ],
                "example": {
                    "code": "// Decision flow:\n// iterate-all hot loop?            -> vector (+ reserve)\n// frequent lookup by key, big N?    -> unordered_map\n// lookup by key, small N?           -> sorted vector + binary_search\n// stable iterators across inserts?  -> list / node-based map\n// insert at both ends?              -> deque",
                    "walkthrough": "The flowchart starts from the access pattern, not the data: iteration favors contiguity, lookup favors hashing (at scale), stability favors nodes. Running any new container choice through these five questions takes ten seconds and prevents most container mistakes."
                },
                "pitfalls": [
                    "Pitfall: std::list by default 'because insertion is O(1)' — iteration-bound code runs 3-10x slower from pointer chasing.",
                    "Pitfall: std::map for everything keyed — unordered_map is usually faster for pure lookup; map only when ordering matters.",
                    "Pitfall: ignoring reserve() — a vector that reallocates 20 times during fill pays for the container choice twice."
                ],
                "try_it": "Benchmark inserting 1M ints and then iterating them in vector vs list vs deque on your machine — record the wall times and explain the ratios from cache behavior."
            }
        ]
    }
}
