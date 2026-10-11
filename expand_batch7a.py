#!/usr/bin/env python3
"""Part 7A: Main driver + shared career/tools domains + CBT config."""
import json, sys
sys.path.insert(0, '/home/hatch/workspace/cert-bootcamps')
from expand_batch1 import (L, S, LB, CHECK, start_here_lessons, mock_domain,
    mock_briefing_lessons, capstone_domain, capstone_lessons, ensure_domains,
    add_lessons, add_scenarios, add_labs, counts)

# ---------------------------------------------------------------- shared: career + tools
def career_roadmap_lessons(course_name, roles, salary_note=""):
    return [
        L(f"Roles That Hire {course_name} Skills",
          "career-roadmap",
          [
              f"The roles: {', '.join(roles)}. Read 10 job postings and extract the repeated requirements \u2014 that list is your real syllabus.",
              "Titles vary by company; skills cluster by function. Map postings to skill clusters (not titles) to see what the market actually buys.",
              "Entry points differ: some roles hire on certification + projects, others on portfolio + interviews. Know your target's gate before optimizing for it.",
              "Salary bands follow scarcity + impact: specialized + revenue-adjacent pays more. Position yourself at that intersection deliberately.",
              salary_note or "Track the market quarterly: which skills are rising in postings? Your learning backlog should follow the demand signal.",
          ],
          "Posting analysis template:\n  Role: ___\n  Repeated requirements (3+ postings): ___\n  Nice-to-haves: ___\n  My gaps: ___ \u2192 study priority",
          "The job posting is the employer's requirements doc. Analyze it like one \u2014 systematically, not hopefully.",
          [
              "Chasing titles instead of skill clusters \u2014 the same skills hide under five different titles.",
              "Ignoring the 'repeated requirements' \u2014 what 8/10 postings demand is the real bar.",
              "No gap analysis \u2014 studying without knowing your gaps is motion without direction.",
          ],
          "Pull 5 postings for your target role now. List the top 5 repeated requirements."),
        L("Resume & Projects That Get Callbacks",
          "career-roadmap",
          [
              "Resumes get 30 seconds: lead with a skills line matching the posting's keywords, then 3-4 bullets per role with quantified outcomes (not duties).",
              "Projects beat buzzwords: one deployed, documented project outweighs a paragraph of claimed skills. Link the repo AND the live demo.",
              "Tailor per application: mirror the posting's language for the top 5 requirements. ATS filters are literal \u2014 'PostgreSQL' does not match 'postgres' in dumb parsers.",
              "The capstone in this bootcamp IS your resume project: finish it, document it, link it. That single line does more work than any certification bullet.",
              "GitHub profile hygiene: pinned repos with READMEs, green contribution squares, no empty forks. Recruiters do click through.",
          ],
          "Bullet formula: [Action verb] + [what] + [scale] + [outcome]\n  Weak: 'Responsible for databases.'\n  Strong: 'Migrated 2TB analytics DB to Postgres; cut query p95 40%; zero-downtime cutover.'",
          "Every bullet must answer: what did you do, at what scale, to what effect? Duties describe jobs; outcomes get interviews.",
          [
              "Skill lists without evidence \u2014 every claimed skill needs a project or role bullet backing it.",
              "One generic resume for all applications \u2014 tailoring is the highest-ROI 20 minutes in job hunting.",
              "No links \u2014 a project without a URL might as well not exist.",
          ],
          "Rewrite your weakest resume bullet using the formula above. Quantify something."),
        L("Interview Loops: What Actually Happens",
          "career-roadmap",
          [
              "Typical loop: recruiter screen (15 min, fit + comp) \u2192 technical screen (45-60 min, live problems) \u2192 onsite/virtual loop (3-5 rounds: technical depth, system design, behavioral) \u2192 offer.",
              "Technical screens test thinking aloud: narrate your approach before coding/querying. Silence is scored as stuck; structured thinking is scored as senior.",
              "Behavioral rounds use STAR (Situation, Task, Action, Result) \u2014 prepare 5 stories covering: conflict, failure, leadership, ambiguity, and impact. Quantify results.",
              "Questions YOU ask matter: 'what does success look like in 90 days?' and 'what's the hardest problem the team faces?' signal seriousness. Never ask nothing.",
              "Follow up within 24 hours: thank-you note referencing something specific from the conversation. Small effort, real signal.",
          ],
          "STAR story skeleton:\n  S: 'Our deploy pipeline broke weekly...'\n  T: 'I owned stabilizing it in Q3...'\n  A: 'I added staged rollouts + runbook...'\n  R: 'Deploys went from 60% to 99% success; on-call pages dropped 70%.'",
          "Prepare stories, not scripts: know your 5 STAR stories cold enough to adapt to any behavioral question. Rehearse aloud twice.",
          [
              "No questions for them \u2014 reads as disinterest; always ask two.",
              "Rambling technical answers \u2014 structure: approach first, then detail, then verify.",
              "Badmouthing past employers \u2014 the interviewer hears how you will talk about THEM.",
          ],
          "Draft one STAR story now using the skeleton. Time it \u2014 aim for 90 seconds."),
    ]

def tools_ecosystem_lessons(course_name, categories):
    cat_text = "\n".join(f"  {c}: {e}" for c, e in categories)
    return [
        L(f"The {course_name} Tool Landscape",
          "tools-ecosystem",
          [
              "Tools cluster by job-to-be-done, not by vendor. Learn the categories first, then pick one tool per category deeply \u2014 depth in one beats surface in five.",
              "The 80/20 rule: 20% of each tool's features cover 80% of real work. Master the core workflow before exploring the edges.",
              "Free/open tiers are enough to learn: every major platform has a free tier or community edition sufficient for portfolio projects. Never pay to learn the basics.",
              "Tool churn is constant; fundamentals are stable. SQL outlives every BI tool; TCP/IP outlives every cloud console. Invest in fundamentals first.",
              f"For {course_name}, the essential categories:\n{cat_text}",
          ],
          f"Learning order:\n  1. One tool per category, core workflow only\n  2. Build the capstone using exactly these tools\n  3. Add a second tool per category only when a job posting demands it",
          "Resist tool tourism: each new tool costs weeks. The portfolio proves depth; the resume lists breadth honestly.",
          [
              "Learning 5 tools shallowly instead of 2 deeply \u2014 interviews probe depth.",
              "Paying for premium tiers to learn \u2014 free tiers cover 90% of learning needs.",
              "Chasing every new release \u2014 fundamentals first; novelty second.",
          ],
          "List your one-tool-per-category stack now. Identify any category where you have zero depth \u2014 that is your next lab."),
        L("Workflows: Connecting the Tools",
          "tools-ecosystem",
          [
              "Tools in isolation are trivia; workflows are skill. The professional unit is the end-to-end flow: ingest \u2192 transform \u2192 validate \u2192 deliver \u2014 across YOUR tool stack.",
              "Document your workflows as runbooks: trigger, steps, verification, rollback. A runbook turns personal knowledge into team capability.",
              "Automate the toil, not the judgment: repetitive steps get scripted; decisions stay human. If you do it weekly, automate it.",
              "Version everything: code, configs, queries, dashboards. 'Final_v2_ACTUAL' is not version control \u2014 git is.",
              "The workflow IS the portfolio piece: 'here is my pipeline, here is the runbook, here is the monitoring' \u2014 that sentence hires.",
          ],
          "Runbook skeleton:\n  Trigger: ___ (schedule/event/manual)\n  Steps: 1.___ 2.___ 3.___\n  Verify: ___ (how do you know it worked?)\n  Rollback: ___ (how do you undo it?)\n  Owner: ___  Last tested: ___",
          "Write the runbook BEFORE automating: it forces you to understand the workflow well enough to hand it to someone else.",
          [
              "Automating before documenting \u2014 you encode confusion at machine speed.",
              "No verification step \u2014 a workflow without a check is a hope with extra steps.",
              "No rollback plan \u2014 the first failure without one teaches this lesson permanently.",
          ],
          "Write a runbook for one workflow you do regularly, using the skeleton above."),
    ]

# ---------------------------------------------------------------- per-CBT config
CBT_CONFIG = {
    "comptia-security-plus": {
        "course": "CompTIA Security+", "exam": "SY0-701",
        "weekly": "Weekly rhythm: 2 domains + 1 lab per week; mock at week 4 and week 6.",
        "capstone_projects": [
            ("Home SOC Lab", "a virtualized SOC with SIEM, alerts, and triage runbooks", "demo an alert from fire to triage to escalation"),
            ("Hardened Web Server", "a CIS-benchmarked Linux host with documented controls", "walk through each hardening control and its verification"),
            ("Incident Response Tabletop", "a full IR plan with a recorded tabletop exercise", "run the 2 AM ransomware scenario live"),
        ],
        "roles": ["SOC Analyst", "Security Engineer", "IT Auditor", "Incident Responder"],
        "tools": [("SIEM", "Splunk/Wazuh"), ("Endpoint", "EDR platform"), ("Scanning", "Nmap/OpenVAS"), ("Ticketing", "TheHive/Jira")],
        "new_module": ("expand_batch2", "security_plus_new_domains"),
        "topup_domains": ["concepts", "threats", "architecture", "operations", "governance"],
    },
    "comptia-network-plus": {
        "course": "CompTIA Network+", "exam": "N10-009",
        "weekly": "Weekly rhythm: subnetting drills daily (10 min) + 2 domains per week; mock at week 4 and 6.",
        "capstone_projects": [
            ("Branch Office Network", "a designed, subnetted, VLAN'd branch network with documentation", "present the addressing plan and defend the design"),
            ("Home Lab Network", "VLANs, firewall rules, and VPN on real or virtual gear", "demo inter-VLAN routing and the firewall policy"),
            ("Network Monitor Dashboard", "SNMP/flow collection with alerting on a lab network", "trigger an alert and walk through the triage"),
        ],
        "roles": ["Network Technician", "NOC Analyst", "Network Administrator", "Field Engineer"],
        "tools": [("Simulation", "Packet Tracer/GNS3"), ("Monitoring", "Wireshark/PRTG"), ("Documentation", "NetBox/draw.io"), ("Automation", "Ansible")],
        "new_module": ("expand_batch3", "network_plus_new_domains"),
        "topup_domains": ["concepts", "implementation", "operations", "net-security", "net-troubleshoot"],
    },
    "comptia-infra": {
        "course": "CompTIA Infrastructure (Cloud+/Server+)", "exam": "Cloud+ / Server+",
        "weekly": "Weekly rhythm: 2 domains + 1 hands-on lab per week; mock at week 4 and 6.",
        "capstone_projects": [
            ("Hybrid Lab Environment", "virtualized servers + cloud resources with IaC", "deploy the full stack from code, live"),
            ("Monitoring Stack", "metrics, logs, and alerting for a lab infrastructure", "trigger an alert and show the runbook response"),
            ("Backup & Restore Drill", "documented 3-2-1 backup with tested restores", "restore a file and a VM on camera"),
        ],
        "roles": ["Systems Administrator", "Cloud Engineer", "Infrastructure Engineer", "DevOps Engineer"],
        "tools": [("Virtualization", "Proxmox/VMware"), ("Cloud", "AWS/Azure free tier"), ("IaC", "Terraform/Ansible"), ("Monitoring", "Prometheus/Grafana")],
        "new_module": ("expand_batch4", "infra_new_domains"),
        "topup_domains": ["cloud-arch", "linux-admin", "server-hw", "virtualization", "data", "ops-sec"],
    },
    "cpp": {
        "course": "C++ Programming", "exam": "C++ Technical Interview",
        "weekly": "Weekly rhythm: 2 domains + daily coding problems; mock interviews at week 4 and 6.",
        "capstone_projects": [
            ("Custom Container Library", "a tested vector/map implementation with benchmarks", "walk through the memory layout and benchmark vs std"),
            ("Multithreaded Server", "a thread-pool TCP server with clean shutdown", "demo under load and explain the concurrency design"),
            ("Game Engine Subsystem", "an ECS or renderer with modern C++ throughout", "demo + code walk of the trickiest part"),
        ],
        "roles": ["C++ Developer", "Systems Programmer", "Game Engine Developer", "HFT Developer"],
        "tools": [("Compiler", "GCC/Clang"), ("Build", "CMake"), ("Debugger", "GDB/LLDB"), ("Sanitizers", "ASan/TSan/UBSan")],
        "new_module": ("expand_batch6", "cpp_new_domains"),
        "topup_domains": ["core-syntax", "oop-cpp", "stl-containers", "memory-smart-pointers", "templates-lambdas", "build-toolchain"],
    },
    "creative-code": {
        "course": "Creative Coding", "exam": "Portfolio Review",
        "weekly": "Weekly rhythm: 2 domains + one finished sketch per week; portfolio curation at week 4 and 6.",
        "capstone_projects": [
            ("Interactive Installation Piece", "a complete interactive work with documentation", "demo the interaction + show the code architecture"),
            ("Generative Series", "a coherent 12-piece series with process documentation", "present the series narrative and technique evolution"),
            ("Audio-Reactive Performance", "a live audio-visual set with mapping documentation", "perform a 5-minute excerpt live"),
        ],
        "roles": ["Creative Technologist", "New Media Artist", "Interaction Designer", "Technical Artist"],
        "tools": [("Framework", "p5.js/openFrameworks"), ("Shaders", "GLSL/Shadertoy"), ("Audio", "Tone.js/Max"), ("Hardware", "Arduino/Raspberry Pi")],
        "new_module": ("expand_batch6", "creative_new_domains"),
        "topup_domains": ["canvas-drawing", "animation", "generative-systems", "interaction", "math-for-art", "showcase"],
    },
    "cybernetics": {
        "course": "Cybernetics", "exam": "Cybernetics Assessment",
        "weekly": "Weekly rhythm: 2 domains + one essay per week; concept-mapping at week 4 and 6.",
        "capstone_projects": [
            ("Systems Analysis Paper", "a 3000-word analysis of a real system through cybernetic lenses", "defend the analysis in a 15-minute presentation"),
            ("Feedback Loop Simulation", "a coded simulation of a cybernetic system with analysis", "demo the simulation + explain the insights"),
            ("Concept Map Atlas", "a complete visual map of cybernetics concepts and relations", "walk through the map's structure and key links"),
        ],
        "roles": ["Systems Thinker", "Researcher", "Policy Analyst", "Design Strategist"],
        "tools": [("Mapping", "Concept mapping tools"), ("Simulation", "Python/Vensim"), ("Writing", "Structured argumentation"), ("Dialogue", "Seminar discussion")],
        "new_module": ("expand_batch6", "cyber_new_domains"),
        "topup_domains": ["cybernetics"],
    },
    "data-analyst": {
        "course": "Data Analytics", "exam": "Data Analyst Interview",
        "weekly": "Weekly rhythm: 2 domains + one analysis project per week; mock interviews at week 4 and 6.",
        "capstone_projects": [
            ("End-to-End Analysis", "a complete business analysis with dashboard and write-up", "present findings like a stakeholder meeting"),
            ("Automated Reporting Pipeline", "a scheduled pipeline from raw data to dashboard", "demo the refresh + explain the data model"),
            ("Experiment Analysis", "a full A/B test design and analysis", "walk through the experimental discipline"),
        ],
        "roles": ["Data Analyst", "Business Intelligence Analyst", "Analytics Engineer", "Product Analyst"],
        "tools": [("SQL", "Postgres/BigQuery"), ("BI", "Power BI/Tableau"), ("Python", "pandas"), ("Sheets", "Excel/Google Sheets")],
        "new_module": ("expand_batch5", "data_analyst_new_domains"),
        "topup_domains": ["sql-analysis", "spreadsheets", "visualization", "statistics", "bi-tools", "storytelling"],
    },
    "data-analyst-to-ml": {
        "course": "Data Analyst to ML", "exam": "ML Transition Assessment",
        "weekly": "Weekly rhythm: 2 domains + one ML exercise per week; project milestones at week 4 and 6.",
        "capstone_projects": [
            ("Churn Prediction Project", "an end-to-end ML project with honest evaluation", "present the full pipeline including the leakage audit"),
            ("ML-Enhanced Dashboard", "a dashboard with embedded predictions and monitoring", "demo predictions + explain the MLOps minimum"),
            ("Feature Store Prototype", "versioned features with point-in-time correctness", "demo temporal correctness + the feature docs"),
        ],
        "roles": ["ML Engineer", "Data Scientist", "Analytics Engineer (ML)"],
        "tools": [("ML", "scikit-learn"), ("Data", "pandas/SQL"), ("Experiment", "MLflow"), ("Deploy", "FastAPI/Docker")],
        "new_module": ("expand_batch5", "daml_new_domains"),
        "topup_domains": ["data-analyst-to-ml"],
    },
    "data-engineering": {
        "course": "Data Engineering", "exam": "Data Engineering Interview",
        "weekly": "Weekly rhythm: 2 domains + one pipeline build per week; system design practice at week 4 and 6.",
        "capstone_projects": [
            ("Streaming Pipeline", "an end-to-end streaming pipeline with monitoring", "demo late-data handling + the idempotent sink"),
            ("Lakehouse Build", "a partitioned, optimized lakehouse with cost analysis", "show the file-skipping metrics and the bill"),
            ("Data Quality Framework", "automated validation with alerting", "trigger a quality failure and show the alert flow"),
        ],
        "roles": ["Data Engineer", "Analytics Engineer", "Platform Engineer (Data)"],
        "tools": [("Processing", "Spark/Flink"), ("Orchestration", "Airflow"), ("Storage", "Delta/Iceberg"), ("Streaming", "Kafka")],
        "new_module": ("expand_batch5", "data_engineering_new_domains"),
        "topup_domains": ["modeling", "etl", "warehouses-lakes", "streaming", "orchestration", "quality-governance"],
    },
    "data-science-certs": {
        "course": "Data Science Certifications", "exam": "Data Science Certification Exams",
        "weekly": "Weekly rhythm: 2 domains + hands-on labs per week; practice exams at week 4 and 6.",
        "capstone_projects": [
            ("Certification Portfolio Project", "a project proving each cert's syllabus in practice", "walk through the README like an interview"),
            ("Reproducible Research Repo", "a fully reproducible analysis with honest evaluation", "clone-and-run live + discuss limitations"),
            ("Study Guide Contribution", "a written guide for one exam domain", "teach it in 10 minutes"),
        ],
        "roles": ["Data Scientist", "ML Engineer", "Research Analyst"],
        "tools": [("Python", "pandas/scikit-learn"), ("Notebooks", "Jupyter"), ("Viz", "matplotlib/plotly"), ("Versioning", "Git/DVC")],
        "new_module": ("expand_batch5", "dsc_new_domains"),
        "topup_domains": ["data-science-certs"],
    },
}

EXTRA_DOMAINS_SMALL = {
    "cybernetics": [
        ("cybernetics-in-tech", "Cybernetics in Technology", "Where the ideas live now: recommendation loops, control systems, and algorithmic feedback.", "\U0001F4BB"),
        ("case-studies", "Case Studies in Systems", "Real systems analyzed cybernetically: successes, failures, and the loops behind them.", "\U0001F4CB"),
    ],
    "data-analyst-to-ml": [
        ("python-for-analysts", "Python for Analysts", "The Python you need for ML: pandas fluency, sklearn basics, and the notebook discipline.", "\U0001F40D"),
        ("statistics-refresh", "Statistics Refresh", "The stats that matter for ML: distributions, inference, and the intuition behind the math.", "\U0001F9EE"),
        ("ml-project-playbook", "ML Project Playbook", "Run an ML project end-to-end: scoping, baselines, iteration, and the demo.", "\U0001F4CB"),
        ("transition-roadmap", "Analyst-to-ML Transition Roadmap", "Your 6-month plan: what to learn in what order, and how to prove it.", "\U0001F5FA\uFE0F"),
    ],
    "data-science-certs": [
        ("hands-on-labs", "Hands-On Lab Series", "The applied skills exams increasingly test: notebooks, SQL, and model interpretation under time.", "\U0001F9EA"),
        ("study-plans", "Study Plans by Exam", "Week-by-week plans tuned to each major exam's blueprint weights.", "\U0001F4C5"),
        ("practice-exams", "Practice Exam Strategy", "How to use practice exams as diagnostics, not just scores.", "\U0001F3AF"),
        ("ml-algorithms", "Core ML Algorithms", "The algorithms every exam assumes: when to use each, and what breaks them.", "\u2699\uFE0F"),
    ],
}
