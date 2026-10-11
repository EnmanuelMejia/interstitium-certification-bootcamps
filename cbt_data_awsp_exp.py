#!/usr/bin/env python3
"""Expansion lessons for the existing aws-cloud-practitioner-plus domain.

The existing domain covers migration strategy (Six R's, CAF, TCO, landing
zone, wave planning); these 4 lessons teach that strategy layer.
"""
from cbt_builder import L

def build_expansion_awsp():
    lessons = []
    scenarios = {}  # did -> [scenario dicts]; no new scenarios here

    did = "aws-cloud-practitioner-plus"
    specs = [
        ("The Six R's: Migration Strategies",
         ["Rehost (lift-and-shift): move as-is — fastest, least change; start here for undifferentiated servers",
          "Replatform (lift-and-reshape): small optimizations in the move — RDS instead of self-managed DB, no architecture change",
          "Repurchase: move to SaaS — drop the app entirely for a service (email to WorkMail, CRM to SaaS)",
          "Refactor/Re-architect: rebuild cloud-native — highest effort, highest payoff; for apps needing scale and agility",
          "Retain and Retire: keep on-prem (compliance, latency) or decommission — deciding NOT to migrate is a valid strategy",
          "Exam rule: 'minimal changes, fast' is rehost; 'move to managed/SaaS' is replatform/repurchase; 'rebuild for cloud' is refactor"],
         "# Strategy picker:\n# Need it moved in weeks, no changes?      -> Rehost\n# DB on EC2 pain? Move DB to RDS in flight? -> Replatform\n# Email/CRM commodity?                      -> Repurchase (SaaS)\n# App must auto-scale globally?              -> Refactor\n# Compliance keeps it on-prem?               -> Retain\n# Unused for 2 years?                        -> Retire\n# Portfolio rule: 70% rehost/replatform, 20% retain/retire, 10% refactor.",
         "The picker turns strategy into triage: most portfolios are mostly rehost/replatform (move fast, optimize later), a slice stays or dies, and a small slice earns the refactor investment. The exam tests the mapping — 'minimal changes' is always rehost, 'managed service in the move' is replatform, 'SaaS' is repurchase.",
         ["Rehosting everything by default — fast now, technical debt later; replatform the easy wins in flight",
          "Refactoring the whole portfolio — years of effort for apps that needed a truck, not a rebuild",
          "No retire decisions — migrating dead apps wastes the budget; decommission first"],
         "Classify 6 hypothetical apps into the Six R's and defend each choice."),
        ("Cloud Adoption Framework Perspectives",
         ["CAF: six perspectives for migration success — Business, People, Governance (business side); Platform, Security, Operations (technical side)",
          "Business: the value case — what outcomes justify the migration; People: roles, skills, training for the cloud operating model",
          "Governance: controls without bureaucracy — guardrails, budgets, compliance that scale",
          "Platform: the landing zone and architectures; Security: identity, detective controls, data protection from day one",
          "Operations: runbooks, monitoring, game days — operating in cloud, not just arriving there",
          "Exam anchor: 'which CAF perspective covers X' — skills/training is People, cost controls is Governance, architectures is Platform"],
         "# CAF cheat sheet:\n# Business    -> why migrate (outcomes, KPIs)\n# People      -> who does it (roles, training, change)\n# Governance  -> rules that scale (budgets, guardrails, risk)\n# Platform    -> where it runs (landing zone, architectures)\n# Security    -> how it stays safe (identity, detection, data)\n# Operations  -> how it runs day 2 (runbooks, monitoring, health)\n# Question pattern: 'team lacks cloud skills' -> People perspective.",
         "The cheat sheet is the memorization device: each perspective owns a question family. 'Skills gap' is always People; 'who approves spend' is Governance; 'reference architectures' is Platform. The exam rarely asks deep — it asks which bucket a concern belongs in.",
         ["Treating CAF as technical-only — half the perspectives are business; migrations fail on people, not packets",
          "Skipping the People perspective — the best landing zone fails with an untrained team",
          "Governance as paperwork — guardrails and budgets ARE the governance; make them automatic"],
         "Map 6 migration concerns (skills gap, budget overrun, no runbooks, weak IAM, no landing zone, unclear ROI) to CAF perspectives."),
        ("TCO and Cloud Economics",
         ["TCO compares fully loaded costs: on-prem (hardware, power, cooling, space, staff, refresh) vs cloud (compute, storage, transfer, support)",
          "The Pricing Calculator models the cloud side — but only with honest inputs: real utilization, real transfer, real support tier",
          "Hidden on-prem costs people forget: the refresh cycle (3-5 years), the 2 AM pager (staff), the half-empty racks (overprovisioning)",
          "Hidden cloud costs people forget: data transfer out, idle resources, and the migration itself — model all three",
          "The honest answer is a spreadsheet reviewed by finance — not a slogan; sometimes the answer is hybrid"],
         "# TCO worksheet (3 years):\n# ON-PREM: servers $400k + power/cooling $90k + rack space $60k\n#          + 2 FTE $450k + refresh reserve $150k = ~$1.15M\n# CLOUD:   50 m5.xlarge SP $380k + S3 20TB $55k + transfer $40k\n#          + Business support $30k + migration $120k = ~$625k\n# PLUS: agility value (features shipped faster) — quantify if you can.\n# Rule: fully loaded both sides, finance reviews, no slogans.",
         "The worksheet shows the shape: on-prem's big lines are people and refresh, cloud's are compute and the migration itself. The migration cost line is the one cloud pitches omit and the staff line is the one on-prem analyses omit. Finance reviewing both sides is what makes the number defensible.",
         ["Comparing hardware to cloud bills — people and power are half the on-prem cost",
          "Omitting migration cost — the move itself is a six-figure line item",
          "One-time analysis — recheck yearly; workload shapes change"],
         "Build a rough 3-year TCO for 20 VMs: fully loaded on-prem vs Savings-Plan cloud."),
        ("Landing Zones and Wave Planning",
         ["Landing zone first: the multi-account foundation (OUs, guardrails, logging, identity) exists BEFORE the first workload migrates",
          "Control Tower builds it: Account Factory for standardized accounts, guardrails that persist, Security OU with audit and log-archive accounts",
          "Wave planning: group applications by dependency (discovery data), business priority, and risk — migrate in waves, not all at once",
          "Wave 0 is the pilot: one low-risk app proving the runbook — then the factory scales proven patterns",
          "Each wave carries a rollback trigger decided in advance — the abort criteria are set calmly, not at 2 AM"],
         "# Migration program shape:\n# Phase 0: Landing zone (Control Tower) + discovery (ADS)\n# Phase 1: Wave 0 pilot — 1 app, prove runbook + rollback\n# Phase 2: Waves 1..N — independent apps first, tangled core last\n# Per wave: runbook, rollback trigger (e.g., errors >2% 15min -> flip back),\n#           owner, hypercare roster (2 weeks elevated monitoring)\n# Measure: cutover time, rollback count, MTTR — improve per wave.",
         "The program shape orders the work: foundation before workloads, pilot before factory, independent apps before the tangled core. The per-wave rollback trigger is the risk control — decided in advance, executed mechanically. Hypercare after each wave catches the Monday-morning surprises the cutover missed.",
         ["Migrating before the landing zone — workloads land in snowflake accounts with no guardrails",
          "Big-bang cutover — maximum blast radius; waves exist to avoid this",
          "No rollback triggers — 'we will know if it is bad' is not a trigger"],
         "Draft a 3-wave plan for 8 apps: assign waves, rollback triggers, hypercare owners."),
    ]
    for sp in specs:
        lessons.append(L(did, *sp))
    return lessons, scenarios
