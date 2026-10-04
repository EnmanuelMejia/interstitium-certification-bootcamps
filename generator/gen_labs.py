#!/usr/bin/env python3
"""Generate guided hands-on labs for every cert-bootcamp content file.

Reads content/<slug>.json (68 files), derives 4 guided labs per bootcamp from
scenario titles/objectives/domains, and writes a new top-level "labs" array
into each file in place (everything else preserved, valid JSON, UTF-8).

Lab checks reference ONLY the guaranteed terminal command sets per profile
family (see FAMILY_COMMANDS). A verification pass re-reads every file and
asserts: valid JSON, lab schema present, each check's regex compiles and
matches at least one canonical command of the bootcamp's family.

Content rules: original practice content only (titles/objectives paraphrased,
never scenario prompts/choices copied); honest framing; no personal data.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")
LABS_PER_BOOTCAMP = 4

# ---------------------------------------------------------------------------
# Terminal profile families (slugs) -> canonical command pool.
# Each entry: (command_to_type, regex_pattern, expect_contains, observe_note)
# expect_contains values are single distinctive tokens the simulated terminal
# is guaranteed to emit for that command.
# ---------------------------------------------------------------------------

FAMILY_COMMANDS = {
    "python": [
        ('print("{tok} ready")', r"print\(", "{tok}",
         "the REPL echoes your concept token back on the next line"),
        ('len("bootcamp")', r"len\(", "8",
         "the REPL counts the characters and reports 8"),
        ("type(42)", r"type\(", "int",
         "the REPL names the int type for 42"),
        ("for i in range(3): print(i)", r"range\(", "2",
         "the loop prints 0, 1, then 2"),
        ("math.pi", r"math\.pi", "3.14",
         "the math module reports pi (run import math first if needed)"),
    ],
    "bash": [
        ("whoami", r"whoami", "candidate",
         "the shell reports the lab identity 'candidate'"),
        ("pwd", r"pwd", "/",
         "the output is an absolute path starting with /"),
        ("uname", r"uname", "Linux",
         "the kernel name reported is Linux"),
        ("echo {tok} ready", r"echo", "{tok}",
         "echo prints your concept token back verbatim"),
        ("ls", r"^ls$|^ls\s", "lab-notes",
         "the listing shows lab-notes (run 'mkdir lab-notes' first if it is missing)"),
        ("ps", r"^ps$|^ps\s", "PID",
         "the process table header names the PID column"),
        ("echo hello world | grep hello", r"grep", "hello",
         "grep passes through the line containing hello"),
    ],
    "kubectl": [
        ("kubectl get pods", r"kubectl get pods", "Running",
         "the pod list shows pods in the Running phase"),
        ("kubectl get nodes", r"kubectl get nodes", "Ready",
         "the node list reports Ready status"),
        ("kubectl get deployments", r"kubectl get deployments", "Available",
         "the deployment list shows available replicas"),
        ("kubectl describe pod/web", r"kubectl describe pod", "web",
         "the describe output names the pod web"),
    ],
    "aws": [
        ("aws s3 ls", r"aws s3 ls", "bucket",
         "the listing names your lab buckets"),
        ("aws sts get-caller-identity", r"aws sts get-caller-identity", "Account",
         "the identity document includes your Account id"),
        ("aws iam list-users", r"aws iam list-users", "UserName",
         "the user list carries the UserName field"),
        ("aws ec2 describe-instances", r"aws ec2 describe-instances", "Instances",
         "the reservation output includes the Instances block"),
    ],
    "sql": [
        (".tables", r"\.tables", "employees",
         "the schema listing includes the employees table"),
        ("SELECT * FROM employees;", r"SELECT \* FROM", "name",
         "the result set shows the name column"),
        (".tables", r"\.tables", "lab_notes",
         "run CREATE TABLE lab_notes (id INTEGER, note TEXT); first, then .tables lists it"),
        ("SELECT name FROM employees WHERE name = 'Ada';", r"SELECT name FROM", "Ada",
         "run INSERT INTO employees (name, role) VALUES ('Ada', 'engineer'); first, then this SELECT shows Ada"),
    ],
    "mongosh": [
        ("show dbs", r"show dbs", "admin",
         "the database list includes admin"),
        ("db.users.find()", r"db\.users\.find", "name",
         "the documents carry the name field"),
        ('db.users.insertOne({name: "lab"})', r"insertOne", "acknowledged",
         "the write result is acknowledged"),
    ],
    "terraform": [
        ("terraform init", r"terraform init", "initialized",
         "the backend initializes successfully"),
        ("terraform plan", r"terraform plan", "Plan",
         "the plan summary shows what would change"),
        ("terraform apply", r"terraform apply", "Apply complete",
         "the apply finishes with the completion message"),
    ],
    "docker": [
        ("docker ps", r"docker ps", "CONTAINER",
         "the container list header shows CONTAINER ID"),
        ("docker images", r"docker images", "REPOSITORY",
         "the image list header shows REPOSITORY"),
        ("docker pull hello-world", r"docker pull", "hello-world",
         "the pull output names the hello-world image"),
        ("docker run hello-world", r"docker run", "Hello from Docker",
         "the container prints its greeting"),
    ],
    "git": [
        ("git status", r"git status", "branch",
         "the status names your current branch"),
        ("git log", r"git log", "commit",
         "the history shows commit entries"),
        ("git branch", r"git branch", "main",
         "the branch list includes main"),
        ("git status", r"git status", "notes.txt",
         "run touch notes.txt first, then git status lists it"),
    ],
    "az": [
        ("az account show", r"az account show", "name",
         "the account document includes the subscription name"),
        ("az group list", r"az group list", "name",
         "each resource group entry carries a name"),
        ("az vm list", r"az vm list", "name",
         "each VM entry carries a name"),
    ],
    "vault": [
        ("vault status", r"vault status", "Sealed",
         "the status output reports the Sealed state"),
        ("vault kv put secret/lab owner=interstitium", r"vault kv put", "Success",
         "the write reports Success"),
        ("vault kv get secret/lab", r"vault kv get", "owner",
         "the read returns the owner field"),
        ("vault kv list secret/", r"vault kv list", "lab",
         "the listing includes the lab secret"),
    ],
    "oci": [
        ("oci iam user list", r"oci iam user list", "data",
         "the JSON envelope carries the data key"),
        ("oci compute instance list", r"oci compute instance list", "data",
         "the JSON envelope carries the data key"),
    ],
    "bashlite": [
        ("echo {tok} ready", r"echo", "{tok}",
         "echo prints your concept token back verbatim"),
        ("whoami", r"whoami", "candidate",
         "the shell reports the lab identity 'candidate'"),
        ("date", r"date", "2026",
         "the date output includes the year 2026"),
        ("uname", r"uname", "Linux",
         "the kernel name reported is Linux"),
    ],
}

FAMILY_TERMINAL = {
    "python": "Python REPL", "bash": "lab shell", "kubectl": "kubectl",
    "aws": "AWS CLI", "sql": "SQL shell", "mongosh": "mongosh",
    "terraform": "Terraform CLI", "docker": "Docker CLI", "git": "Git",
    "az": "Azure CLI", "vault": "Vault CLI", "oci": "OCI CLI",
    "bashlite": "terminal",
}

FAMILY_DRILL = {
    "python": "REPL drill", "bash": "shell drill", "kubectl": "kubectl drill",
    "aws": "AWS CLI drill", "sql": "SQL drill", "mongosh": "mongosh drill",
    "terraform": "Terraform drill", "docker": "Docker drill", "git": "Git drill",
    "az": "Azure CLI drill", "vault": "Vault drill", "oci": "OCI CLI drill",
    "bashlite": "terminal drill",
}

SLUG_TO_FAMILY = {
    # python REPL
    "python": "python", "python-web": "python", "datascience-ml": "python",
    "llm-engineering": "python", "nvidia-ai": "python", "dsa": "python",
    # bash
    "linux-essentials": "bash", "rhcsa": "bash", "rhce": "bash",
    "sre-platform": "bash", "comptia-core": "bash", "comptia-cyber": "bash",
    "comptia-infra": "bash", "cissp": "bash", "cism": "bash",
    "pentest": "bash", "soc-analyst": "bash", "zerotrust": "bash",
    "dod-8140": "bash", "nice-framework": "bash", "hackers-arise": "bash",
    "nsa-codebreaker": "bash", "systems-cs": "bash",
    # kubectl
    "k8s-associate": "kubectl", "cka": "kubectl", "ckad": "kubectl",
    "openshift": "kubectl",
    # aws
    "aws-clf": "aws", "aws-saa": "aws", "aws-soa": "aws", "aws-dop": "aws",
    "aws-data": "aws", "aws-ml": "aws", "aws-scs": "aws",
    # sql
    "sql": "sql", "oracle-sql": "sql", "dp-203": "sql",
    "data-engineering": "sql", "data-analyst": "sql",
    # mongosh / terraform / docker / git
    "mongodb": "mongosh", "terraform": "terraform", "docker": "docker",
    "git-devops": "git",
    # az
    "az-104": "az", "az-305": "az", "az-700": "az",
    "azure-developer": "az", "sc-200": "az", "sc-300": "az",
    "m365": "az", "ms-fundamentals": "az",
    # vault / oci
    "vault-consul": "vault", "oracle-oci": "oci", "oracle-db": "oci",
    # default bash-lite
    "java": "bashlite", "c-lang": "bashlite", "cpp": "bashlite",
    "dotnet": "bashlite", "spring": "bashlite", "fullstack": "bashlite",
    "react-frontend": "bashlite", "blockchain-dev": "bashlite",
    "career-launch": "bashlite", "creative-code": "bashlite",
    "hermetica": "bashlite", "math-tech": "bashlite",
    "ides-tooling": "bashlite", "ai-product": "bashlite",
}

OBJECTIVE_TEMPLATES = [
    "Run a short sequence of {term} commands that demonstrates {obj}, then verify each result against the expected output.",
    "Use the {term} to explore {obj} hands-on: type each command, read what comes back, and connect the output to the concept.",
    "Prove you can apply {obj} in the {term} — follow the steps, watch the output, and confirm every check passes.",
]

CONTEXT_TEMPLATES = [
    "This lab reworks the {domain} practice scenario \"{title}\" into commands you run yourself — same concept, hands-on instead of multiple choice.",
    "Inspired by the {domain} scenario \"{title}\": take its core idea and prove it live in the terminal instead of answering on paper.",
    "The {domain} scenario \"{title}\" tests this concept as a question. This lab makes you demonstrate it with real commands.",
]


def decap(s):
    """Lowercase first letter unless it starts an acronym (STAR, SQL, AWS)."""
    if not s:
        return s
    if len(s) > 1 and s[1].isupper():
        return s
    return s[0].lower() + s[1:]


def concept_token(obj):
    tok = re.sub(r"[^a-z0-9]+", "-", obj.lower()).strip("-")[:24]
    return tok or "lab"


def family_for(slug):
    return SLUG_TO_FAMILY.get(slug, "bashlite")


def pick_scenarios(data, n):
    """Round-robin across domains, unique scenario ids."""
    domains = data.get("domains", []) or []
    picks, seen, round_no = [], set(), 0
    while len(picks) < n and round_no < 60:
        progressed = False
        for d in domains:
            if len(picks) >= n:
                break
            pool = d.get("scenarios", []) or []
            if not pool:
                continue
            s = pool[round_no % len(pool)]
            if s.get("id") not in seen:
                seen.add(s["id"])
                picks.append((d.get("name", "General"), s))
                progressed = True
        round_no += 1
        if not progressed:
            break
    return picks


def build_lab(slug, family, domain_name, scenario, lab_no, check_offset):
    term = FAMILY_TERMINAL[family]
    drill = FAMILY_DRILL[family]
    pool = FAMILY_COMMANDS[family]

    objectives = scenario.get("objectives") or [domain_name]
    obj = str(objectives[0]).strip() or domain_name
    obj_low = decap(obj)
    tok = concept_token(obj)
    title_in = str(scenario.get("title", "practice scenario")).strip()

    title = "{} — {}".format(obj, drill)
    objective = OBJECTIVE_TEMPLATES[(lab_no - 1) % len(OBJECTIVE_TEMPLATES)].format(
        term=term, obj=obj_low)

    # Rotate through the command pool so labs differ; 3 checks per lab.
    n_checks = min(3, len(pool))
    chosen = [pool[(check_offset + i) % len(pool)] for i in range(n_checks)]

    steps = [
        CONTEXT_TEMPLATES[(lab_no - 1) % len(CONTEXT_TEMPLATES)].format(
            domain=domain_name, title=title_in),
        "Open the Terminal tab for this bootcamp — every command below runs there.",
    ]
    for cmd, _pat, expect, observe in chosen:
        cmd, expect, observe = (s.replace("{tok}", tok) for s in (cmd, expect, observe))
        steps.append(
            "Type exactly: {} — {}".format(cmd, observe))
    steps.append(
        "In your own words, say what each command's output taught you about {}.".format(obj_low))

    checks = []
    for cmd, pattern, expect, _observe in chosen:
        cmd, expect = (s.replace("{tok}", tok) for s in (cmd, expect))
        checks.append({
            "command_pattern": pattern,
            "expect_contains": expect,
            "hint": "In the Terminal tab, run `{}`. If the check fails, confirm you typed it exactly and that the output contains \"{}\".".format(cmd, expect),
        })

    return {
        "id": "{}-lab-{}".format(slug, lab_no),
        "title": title,
        "objective": objective,
        "steps": steps,
        "checks": checks,
        "success_message": (
            "Lab complete — {} practiced hands-on. That's the Interstitium Labs "
            "way: run it, see it, own it.".format(obj_low)),
    }


def generate_for_file(path, slug):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    family = family_for(slug)
    picks = pick_scenarios(data, LABS_PER_BOOTCAMP)
    labs = []
    for i, (domain_name, scenario) in enumerate(picks, start=1):
        labs.append(build_lab(slug, family, domain_name, scenario, i, (i - 1) * 2))
    data["labs"] = labs
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return len(labs), family


def verify_file(path, slug):
    """Verification pass: valid JSON, schema, checks match guaranteed commands."""
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # noqa: BLE001
        return ["invalid JSON: {}".format(e)]
    labs = data.get("labs")
    if not isinstance(labs, list) or not labs:
        return ["missing or empty 'labs' array"]
    family = family_for(slug)
    canonical = [c[0] for c in FAMILY_COMMANDS[family]]
    for lab in labs:
        for key in ("id", "title", "objective", "steps", "checks", "success_message"):
            if key not in lab:
                errors.append("{}: missing key '{}'".format(lab.get("id", "?"), key))
        steps = lab.get("steps", [])
        if not (3 <= len(steps) <= 8):
            errors.append("{}: steps count {} outside 3-8".format(lab.get("id"), len(steps)))
        checks = lab.get("checks", [])
        if not (2 <= len(checks) <= 5):
            errors.append("{}: checks count {} outside 2-5".format(lab.get("id"), len(checks)))
        for ch in checks:
            pat = ch.get("command_pattern", "")
            exp = ch.get("expect_contains", "")
            try:
                rx = re.compile(pat)
            except re.error as e:
                errors.append("{}: bad regex {!r}: {}".format(lab.get("id"), pat, e))
                continue
            if not any(rx.search(c) for c in canonical):
                errors.append("{}: pattern {!r} matches no {} command".format(
                    lab.get("id"), pat, family))
            if not exp or not isinstance(exp, str):
                errors.append("{}: empty expect_contains".format(lab.get("id")))
            if not ch.get("hint"):
                errors.append("{}: empty hint".format(lab.get("id")))
    return errors


def main():
    files = sorted(f for f in os.listdir(CONTENT_DIR) if f.endswith(".json"))
    if len(files) != 68:
        print("WARNING: expected 68 content files, found {}".format(len(files)))
    mapped = set(SLUG_TO_FAMILY)
    on_disk = {f[:-5] for f in files}
    for s in sorted(mapped - on_disk):
        print("WARNING: mapped slug '{}' has no content file (falls back to bashlite only if on disk)".format(s))

    counts, fams = {}, {}
    for fname in files:
        slug = fname[:-5]
        n, family = generate_for_file(os.path.join(CONTENT_DIR, fname), slug)
        counts[slug] = n
        fams[slug] = family
        print("  {:<18} family={:<9} labs={}".format(slug, family, n))

    total = sum(counts.values())
    print("\nGenerated {} labs across {} bootcamps.".format(total, len(counts)))

    # ---- verification pass ----
    print("\nVerification pass:")
    bad = 0
    for fname in files:
        slug = fname[:-5]
        errs = verify_file(os.path.join(CONTENT_DIR, fname), slug)
        if errs:
            bad += 1
            print("  FAIL {}:".format(slug))
            for e in errs:
                print("    - {}".format(e))
    if bad == 0:
        print("  OK: all {} files valid JSON; every check's pattern matches a guaranteed {} command and has a non-empty expect_contains.".format(len(files), "family"))
    else:
        print("  {} file(s) with problems.".format(bad))
        sys.exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
