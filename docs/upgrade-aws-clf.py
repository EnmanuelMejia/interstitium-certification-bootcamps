"""AWS CLF upgrade (CBT-8 section 7): additive-only upgrade of aws-clf.json.

- Sets accent "#ff9900" and simulation {"items":30,"minutes":45}
- Fixes clf-cc-06 (answer pointed at "AWS Region"; the fault domain within a region is the AZ)
- Adds 2 exam-focused labs: pricing-calculator reasoning + support-plan selection
- Adds a foundations entry: CLF-C02 exam-strategy refresher
- Registers new labs in the "advanced" section lab_ids
- Never deletes or rewrites existing scenarios/lessons/labs/missions/simulations.

Run: python3 docs/upgrade-aws-clf.py
"""
import copy
import json
import os

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")
PATH = os.path.join(CONTENT_DIR, "aws-clf.json")
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups", "aws-clf.json.2026-10-06.bak")

NEW_LABS_JSON = '''
[
  {
    "id": "aws-clf-lab-pricing-calc",
    "title": "Pricing Calculator \u2014 reason before you spend",
    "objective": "Practice the Cloud Practitioner pricing habit: pull the live price list for EC2, then reason through a monthly estimate the way the AWS Pricing Calculator does.",
    "difficulty": 2,
    "steps": [
      "Open the Terminal tab for this bootcamp.",
      "Type exactly: aws pricing describe-services --service-code AmazonEC2 \\u2014 confirm the Price List API knows this service",
      "Type exactly: aws ec2 describe-instance-types --instance-types t3.micro \\u2014 read the vCPU and memory of a Free Tier eligible type",
      "In your own words, build a monthly estimate: hourly price \\u00d7 hours in a month \\u00d7 instance count, then say which Pricing Calculator inputs (region, instance type, utilization) would change your answer."
    ],
    "checks": [
      {
        "command_pattern": "^aws pricing describe-services --service-code AmazonEC2$",
        "expect_contains": "AmazonEC2",
        "hint": "In the Terminal tab, run `aws pricing describe-services --service-code AmazonEC2`. If the check fails, confirm you typed it exactly and that the output contains \\"AmazonEC2\\"."
      },
      {
        "command_pattern": "^aws ec2 describe-instance-types --instance-types t3.micro$",
        "expect_contains": "t3.micro",
        "hint": "In the Terminal tab, run `aws ec2 describe-instance-types --instance-types t3.micro`. If the check fails, confirm you typed it exactly and that the output contains \\"t3.micro\\"."
      }
    ],
    "success_message": "Lab complete \\u2014 you estimated cost from the price list before deploying anything, which is the whole point of the Pricing Calculator."
  },
  {
    "id": "aws-clf-lab-support-plans",
    "title": "Support plan selection \\u2014 match the response to the risk",
    "objective": "Learn to match a support plan to a real incident: inspect severity levels via the Support API, then pick the plan whose response target fits the scenario.",
    "difficulty": 2,
    "steps": [
      "Open the Terminal tab for this bootcamp.",
      "Type exactly: aws support describe-severity-levels \\u2014 read the five severity levels from low to urgent",
      "Type exactly: aws support describe-services \\u2014 confirm which services the Support API covers",
      "In your own words, answer: a production checkout is down and the team needs AWS responding in under 15 minutes with a named TAM \\u2014 which plan, and why do Business and Developer fall short?"
    ],
    "checks": [
      {
        "command_pattern": "^aws support describe-severity-levels$",
        "expect_contains": "urgent",
        "hint": "In the Terminal tab, run `aws support describe-severity-levels`. If the check fails, confirm you typed it exactly and that the output contains \\"urgent\\"."
      },
      {
        "command_pattern": "^aws support describe-services$",
        "expect_contains": "Amazon Elastic Compute Cloud",
        "hint": "In the Terminal tab, run `aws support describe-services`. If the check fails, confirm you typed it exactly and that the output contains \\"Amazon Elastic Compute Cloud\\"."
      }
    ],
    "success_message": "Lab complete \\u2014 you matched severity to plan: only Enterprise answers an urgent production event in under 15 minutes with a TAM."
  }
]
'''

EXAM_STRATEGY_FOUNDATION = {
    "track": "exam-strategy",
    "why_needed": (
        "CLF-C02 is 65 multiple-choice and multiple-response questions in 90 minutes "
        "(roughly 80 seconds per question, passing score 700/1000). Answer what you know "
        "first and flag the rest: two choices are usually obviously wrong, leaving a "
        "50/50 between concepts you can reason about. Beware absolutes like 'always', "
        "'never', and 'zero downtime' — they are almost always the distractor. When "
        "two answers both sound right, pick the one that matches the shared responsibility "
        "model or the cheapest managed option; the exam rewards cloud-native thinking, not trivia."
    ),
}


def main():
    os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
    with open(PATH, encoding="utf-8") as f:
        original = f.read()
    d = json.loads(original)

    before_labs = len(d["labs"])
    before_foundations = len(d["foundations"])
    scenario_counts_before = {dom["id"]: len(dom["scenarios"]) for dom in d["domains"]}

    # (a) accent + simulation
    d["accent"] = "#ff9900"
    d["simulation"] = {"items": 30, "minutes": 45}

    # (e) accuracy fix: clf-cc-06 answer pointed at "AWS Region"; the fault domain
    # within a region is the Availability Zone (matches the why text).
    fixed = 0
    for dom in d["domains"]:
        for s in dom["scenarios"]:
            if s["id"] == "clf-cc-06":
                assert s["answer"] == 2, "clf-cc-06 answer drifted; inspect manually"
                s["answer"] = 0
                fixed += 1
    assert fixed == 1

    # (b) top up domains below 6 scenarios (none currently, but enforce the rule)
    topped = []
    for dom in d["domains"]:
        if len(dom["scenarios"]) < 6:
            topped.append(dom["id"])
    assert not topped, f"domains below 6 scenarios need new content: {topped}"

    # (c) add exam-focused labs (shared-responsibility drill already exists)
    existing_lab_ids = {lab["id"] for lab in d["labs"]}
    new_labs = json.loads(NEW_LABS_JSON)
    for lab in new_labs:
        if lab["id"] not in existing_lab_ids:
            d["labs"].append(lab)

    # (d) add exam-strategy foundations entry
    existing_tracks = {f["track"] for f in d["foundations"]}
    if "exam-strategy" not in existing_tracks:
        d["foundations"].append(EXAM_STRATEGY_FOUNDATION)

    # register new labs in the advanced section
    for sec in d.get("sections", []):
        if sec.get("id") == "advanced":
            for lab in new_labs:
                if lab["id"] not in sec.get("lab_ids", []):
                    sec["lab_ids"].append(lab["id"])

    # sanity: nothing existing was removed or rewritten
    d_before = json.loads(original)
    assert len(d["domains"]) == len(d_before["domains"])
    for dom_new, dom_old in zip(d["domains"], d_before["domains"]):
        assert dom_new["id"] == dom_old["id"]
        old_scen = {s["id"]: s for s in dom_old["scenarios"]}
        for s in dom_new["scenarios"]:
            if s["id"] in old_scen:
                old = dict(old_scen[s["id"]])
                new = dict(s)
                if s["id"] == "clf-cc-06":
                    old["answer"] = 0  # the one intentional fix
                assert new == old, f"scenario {s['id']} was altered unintentionally"

    with open(BACKUP, "w", encoding="utf-8") as f:
        f.write(original)

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=True)
        f.write("\n")

    # verify
    with open(PATH, encoding="utf-8") as f:
        v = json.load(f)
    print("OK - parses")
    print("accent:", v["accent"], "| simulation:", v["simulation"])
    print("domains:", [(dom["id"], len(dom["scenarios"])) for dom in v["domains"]])
    print("labs:", before_labs, "->", len(v["labs"]))
    print("foundations:", before_foundations, "->", len(v["foundations"]),
          [f["track"] for f in v["foundations"]])
    print("behavioral:", len(v["behavioral"]), "| terminalMissions:", len(v["terminalMissions"]),
          "| simulations:", len(v["simulations"]), "| lessons:", len(v["lessons"]))
    print("file size:", os.path.getsize(PATH), "bytes")
    print("backup:", BACKUP)


if __name__ == "__main__":
    main()
