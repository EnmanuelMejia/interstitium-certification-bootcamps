#!/usr/bin/env python3
"""Apply foundation tracks + math modules to every content/<slug>.json.

Reads catalog.json (bootcamp slugs) and generator/foundation-tracks.json
(valid track ids), then read-modify-writes each content file: sets the
top-level `foundations` and `math` keys while preserving every other key.

`foundations`: [{"track": <track_id>, "why_needed": <1-2 sentences>}]
`math`: [module ids from engine/math.json] (may be empty)

Prints a per-bootcamp foundations+math summary. Idempotent.
"""

import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(BASE, "catalog.json")
TRACKS_FILE = os.path.join(BASE, "generator", "foundation-tracks.json")
MATH_FILE = os.path.join(BASE, "engine", "math.json")
CONTENT_DIR = os.path.join(BASE, "content")

MATH_IDS = ["binary", "subnetting", "logic", "stats", "probability", "linalg"]

# slug -> [(track_id, why_needed)]
FOUNDATIONS = {
    "python": [
        ("programming-basics", "Python assumes you know what code is. This track teaches programs, variables, and how code runs, so the Python syntax lands on solid ground."),
    ],
    "c-lang": [
        ("programming-basics", "C is unforgiving to true beginners. Learn what code is and how programs run first, so pointers and memory have context."),
    ],
    "cpp": [
        ("programming-basics", "C++ builds on the same core ideas as every language. Learn what programs are and how they execute before tackling objects and memory."),
    ],
    "java": [
        ("programming-basics", "Java's verbosity overwhelms beginners who have never seen code. Learn what programs are first, so classes and types have meaning."),
    ],
    "dsa": [
        ("programming-basics", "Data structures are built from code. This track gives you the programming vocabulary — variables, functions, control flow — that every algorithm assumes."),
    ],
    "systems-cs": [
        ("programming-basics", "Systems topics assume you can read code. This track teaches what programs are and how they execute."),
        ("hardware", "Computer organization starts at the physical layer. Learn what the CPU, RAM, and storage do before studying how operating systems manage them."),
    ],
    "react-frontend": [
        ("programming-basics", "Components are code. Learn what programs are and how they run before JSX and state enter the picture."),
        ("http-web", "React apps live in the browser and talk to APIs. Learn how browsers load pages and what requests, URLs, and status codes mean."),
    ],
    "python-web": [
        ("programming-basics", "Web frameworks are code frameworks. Know what programs are before routing and templates."),
        ("http-web", "Django and Flask exist to answer HTTP requests. Learn requests, responses, and status codes before the framework magic."),
    ],
    "spring": [
        ("programming-basics", "Spring is Java at scale. The programming basics — code, execution, variables — come before dependency injection."),
        ("http-web", "Spring Boot serves HTTP. Learn requests, methods, and status codes before controllers and REST."),
    ],
    "dotnet": [
        ("programming-basics", "C# and ASP.NET assume programming literacy. Learn what code is before the framework."),
        ("http-web", ".NET web apps answer HTTP requests. Requests, URLs, and status codes come before middleware."),
    ],
    "fullstack": [
        ("programming-basics", "Full-stack means code on both ends. Learn what programs are before spanning front to back."),
        ("http-web", "The front end and back end communicate over HTTP. Learn the browser's journey and APIs before connecting the tiers."),
    ],
    "ides-tooling": [
        ("cli-basics", "Developer tools live half in the terminal. Learn what a command line is and how to get help before mastering IDEs."),
        ("programming-basics", "IDEs exist to write code. Know what code is first, so the tooling has something to serve."),
    ],
    "git-devops": [
        ("cli-basics", "Git and CI run in the terminal. Get comfortable with the command line before version control adds its own vocabulary."),
        ("programming-basics", "DevOps automates code workflows. Knowing what code and programs are makes pipelines meaningful."),
    ],
    "ai-product": [
        ("python", "AI features are built with Python: API calls, data handling, agent loops. Learn to read and write small scripts first."),
    ],
    "comptia-core": [
        ("hardware", "A+ is half hardware: CPUs, RAM, storage, troubleshooting. This track teaches the physical components before the exam objectives build on them."),
        ("networking", "Network+ is the other half of the trifecta. Learn IP addresses, DNS, ports, and HTTP before the objectives assume them."),
    ],
    "comptia-cyber": [
        ("networking", "Threat hunting and log analysis assume you read networks fluently: addresses, DNS, ports, and HTTP conversations."),
        ("linux-cli", "Security tooling lives on Linux. Learn to navigate files, search logs, and chain commands before the analyst workflows begin."),
    ],
    "comptia-infra": [
        ("networking", "Cloud+ and Server+ assume networking literacy: addresses, DNS, and ports appear in every infrastructure topic."),
        ("linux-cli", "Linux+ is hands-on Linux. Learn files, text tools, and pipes before administration topics assume them."),
    ],
    "cissp": [
        ("security-basics", "CISSP's eight domains assume the CIA triad, threat vocabulary, and defense-in-depth thinking. This track teaches that shared language from zero."),
        ("networking", "Four of the eight domains touch network security. Learn addresses, DNS, ports, and HTTP before the architecture discussions."),
    ],
    "cism": [
        ("security-basics", "CISM governs security programs. The CIA triad, risk vocabulary, and layered defense are the concepts every governance discussion assumes."),
        ("networking", "Incident management and network security topics assume you understand addresses, ports, and HTTP."),
    ],
    "aws-clf": [
        ("cloud-concepts", "Cloud Practitioner is the cloud mental model: regions, services, billing, shared responsibility. Learn it here before the exam vocabulary."),
        ("networking", "VPCs, DNS, and HTTP underpin every AWS architecture question. Get the fundamentals first."),
    ],
    "aws-saa": [
        ("networking", "Architecting on AWS means designing VPCs, subnets, DNS, and load balancing. This track teaches the networking those designs assume."),
        ("linux-cli", "EC2 administration and troubleshooting happen over SSH on Linux. Learn the command line before the ops scenarios."),
        ("iam-concepts", "Secure architectures are IAM architectures. Learn users, roles, and policies before designing access."),
    ],
    "aws-soa": [
        ("networking", "SysOps means operating VPCs: subnets, routing, and DNS come up in daily operations."),
        ("linux-cli", "Deploying and managing on AWS is terminal work over SSH. Command-line fluency comes first."),
        ("iam-concepts", "Operations on AWS are permission-gated. Learn users, roles, and policies before the runbooks."),
    ],
    "aws-dop": [
        ("linux-cli", "DevOps on AWS is terminal-driven: CLI commands, scripts, and pipelines. Get fluent before the automation topics."),
        ("iam-concepts", "Deployment pipelines assume roles constantly. Learn what roles and policies are before the SDLC automation."),
        ("cloud-concepts", "Multi-account strategy and billing topics assume the region, service, and billing mental model."),
    ],
    "aws-scs": [
        ("networking", "Securing AWS means securing VPCs, and VPCs are pure networking: addresses, subnets, ports."),
        ("iam-concepts", "The security specialty is an IAM exam in disguise. Master users, roles, and policies first."),
        ("security-basics", "Threat detection assumes the CIA triad and risk vocabulary. Learn the language of security from zero."),
    ],
    "aws-data": [
        ("python", "Data engineering on AWS is Python plus SQL: Glue jobs, Lambda transforms, and notebooks all assume scripting."),
        ("sql", "Lakes and warehouses are queried with SQL. Learn SELECT, filtering, and sorting before the analytics topics."),
        ("cloud-concepts", "S3, storage classes, and regions underpin every data architecture. Get the cloud model first."),
    ],
    "aws-ml": [
        ("python", "SageMaker, notebooks, and training scripts are Python. Learn to read and write scripts before the ML engineering."),
        ("cloud-concepts", "Training clusters, endpoints, and storage live in regions and AZs. Learn the cloud geography first."),
    ],
    "ms-fundamentals": [
        ("cloud-concepts", "The Microsoft fundamentals exams test the cloud model itself: concepts, pricing, and shared responsibility."),
        ("networking", "Azure networking basics and security fundamentals assume IP, DNS, and HTTP literacy."),
    ],
    "az-104": [
        ("cloud-concepts", "Azure administration assumes regions, resource groups, and the billing model. Learn the cloud concepts before the portal."),
        ("networking", "Virtual networking is the heart of AZ-104: VNets are subnets, DNS, and routing applied."),
    ],
    "az-305": [
        ("cloud-concepts", "Designing solutions assumes you already think in regions, zones, and services. This track builds that thinking."),
        ("networking", "Infrastructure design is network design: VNets, connectivity, and private access throughout."),
    ],
    "az-700": [
        ("networking", "This is the networking exam: design and operate Azure networks. Master IP, DNS, ports, and HTTP fundamentals first."),
        ("cloud-concepts", "Regions and VNets frame every design decision. Learn the geography before the architectures."),
    ],
    "azure-developer": [
        ("programming-basics", "AZ-204 assumes you write code. Learn what programs are and how they run before the SDKs and APIs."),
        ("cloud-concepts", "App Service, Functions, and managed identity live in the cloud model: regions, services, and billing."),
        ("http-web", "Every Azure API call is HTTP. Learn requests, status codes, and JSON-shaped thinking before the SDK topics."),
    ],
    "dp-203": [
        ("sql", "Data Factory and Synapse are SQL engines at heart. Learn to query before orchestrating pipelines."),
        ("python", "Databricks notebooks and data prep are Python. Scripting unlocks the data-engineering topics."),
        ("cloud-concepts", "Storage accounts, regions, and service tiers frame every design. Learn the cloud model first."),
    ],
    "sc-200": [
        ("security-basics", "SOC work is the CIA triad in action: detect threats, assess risk, respond in layers. Learn the vocabulary from zero."),
        ("networking", "Log analysis and hunting assume you read addresses, DNS, and HTTP fluently."),
    ],
    "sc-300": [
        ("iam-concepts", "Entra ID is identity and access management as a product. Learn users, groups, roles, and policies before the lifecycle topics."),
        ("security-basics", "Conditional Access and identity protection are risk decisions. The threat and risk vocabulary comes first."),
    ],
    "m365": [
        ("cloud-concepts", "The M365 tenant is a cloud service: regions, services, and the shared-responsibility line apply throughout."),
        ("networking", "Exchange, Teams, and hybrid identity all ride on DNS and HTTP. Learn the network basics first."),
    ],
    "oracle-oci": [
        ("cloud-concepts", "OCI mirrors the universal cloud model: regions, availability domains, services, billing. Learn it vendor-neutral first."),
        ("linux-cli", "OCI compute is Linux over SSH. Command-line fluency unlocks the hands-on topics."),
    ],
    "oracle-sql": [
        ("data-basics", "SQL starts with data thinking: tables, types, keys, and asking questions. This track teaches that before the first SELECT."),
    ],
    "oracle-db": [
        ("data-basics", "Database administration is data stewardship. Learn what data is, how it goes wrong, and how questions become queries."),
        ("linux-cli", "Oracle DBAs live on Linux: installs, logs, and scripts all run in the terminal."),
    ],
    "sql": [
        ("data-basics", "Queries start with data thinking: tables, types, keys, and turning questions into queries. Learn that before SELECT."),
    ],
    "mongodb": [
        ("data-basics", "Documents are still data: types, keys, and clean-versus-messy thinking apply before any CRUD."),
    ],
    "data-engineering": [
        ("python", "Pipelines are Python: ETL scripts, orchestration, and transforms all assume scripting fluency."),
        ("sql", "Warehouses and lakes answer in SQL. Query skills unlock the modeling and analytics topics."),
    ],
    "data-analyst": [
        ("sql", "Analysis is querying: SELECT, filter, sort, aggregate. Learn the query language before the BI tools."),
        ("python", "Spreadsheets end where Python begins. Scripting unlocks repeatable analysis."),
    ],
    "datascience-ml": [
        ("python", "ML is Python: notebooks, libraries, and model code all assume scripting fluency."),
        ("sql", "ML datasets live in databases and files. Query them with SQL, wrangle them with Python."),
    ],
    "llm-engineering": [
        ("python", "Agents, RAG pipelines, and evals are Python programs. Scripting fluency unlocks the engineering topics."),
        ("http-web", "LLM apps are API clients: prompts go out over HTTP, answers come back as JSON. Learn requests and APIs first."),
    ],
    "linux-essentials": [
        ("cli-basics", "Linux Essentials starts at the terminal. Learn what a command line is before Linux adds its own commands."),
    ],
    "rhcsa": [
        ("cli-basics", "System administration is terminal work. Command-line comfort comes before users, storage, and services."),
    ],
    "rhce": [
        ("cli-basics", "Ansible runs from the terminal over SSH. Command-line comfort comes before automation."),
        ("yaml", "Ansible playbooks are YAML documents. Learn to read and write YAML before the automation topics."),
    ],
    "k8s-associate": [
        ("linux-cli", "Kubernetes runs on Linux nodes and is operated from the terminal. Files, pipes, and text tools come first."),
        ("networking", "Services, DNS, and ingress are networking applied to clusters. Learn the fundamentals before the abstractions."),
        ("cloud-concepts", "Cloud-native assumes the cloud: regions, managed services, and billing shape every architecture."),
    ],
    "cka": [
        ("linux-cli", "The CKA is a hands-on terminal exam on Linux. Command-line fluency is non-negotiable."),
        ("yaml", "Every Kubernetes object is YAML. Read and write it confidently before the cluster topics."),
        ("networking", "Services, DNS, and CNI are networking inside the cluster. Fundamentals first."),
    ],
    "ckad": [
        ("linux-cli", "App developers debug pods from the terminal. Command-line fluency comes before deployment topics."),
        ("yaml", "Deployments, services, and config are all YAML manifests. Learn the format before the API objects."),
        ("networking", "Exposing apps means services, DNS, and ingress: networking fundamentals applied."),
    ],
    "docker": [
        ("cli-basics", "Docker is a terminal tool. Command-line comfort comes before images and containers."),
        ("linux-cli", "Containers are Linux: filesystems, processes, and pipes. Learn the Linux basics behind the abstraction."),
    ],
    "terraform": [
        ("cli-basics", "Terraform runs in the terminal: init, plan, apply. Get comfortable with the command line first."),
        ("cloud-concepts", "Infrastructure as code describes cloud infrastructure. Learn regions, services, and billing before codifying them."),
    ],
    "vault-consul": [
        ("cli-basics", "Vault's CLI is the primary interface. Terminal comfort comes before secrets engines."),
        ("cloud-concepts", "Service networking assumes the cloud service model: compute, network, and managed services."),
    ],
    "openshift": [
        ("linux-cli", "OpenShift is Kubernetes on Red Hat, operated from the terminal. Linux command-line skills come first."),
        ("yaml", "Projects, builds, and routes are YAML manifests. Learn the format before the platform."),
        ("networking", "Routes and networking are cluster networking: DNS, ports, and HTTP applied."),
    ],
    "sre-platform": [
        ("cli-basics", "SRE work is terminal work: incidents are debugged from the command line."),
        ("cloud-concepts", "Platforms are built on cloud primitives: regions, services, and the billing that constrains design."),
    ],
    "soc-analyst": [
        ("networking", "Detection is reading networks: addresses, DNS, ports, and HTTP in log form."),
        ("linux-cli", "Triage happens in the terminal: searching logs with grep and chaining pipes is the analyst's daily motion."),
    ],
    "pentest": [
        ("networking", "Recon and exploitation are applied networking: addresses, ports, DNS, and HTTP are the attack surface."),
        ("linux-cli", "Offensive tooling is Linux terminal tooling. Command-line fluency comes before methodology."),
    ],
    "hackers-arise": [
        ("networking", "Security starts with networks: addressing, DNS, and ports are the terrain."),
        ("linux-cli", "The Linux-first path assumes terminal fluency: files, text tools, and pipes throughout."),
    ],
    "zerotrust": [
        ("security-basics", "Zero trust is the CIA triad plus never-trust-always-verify. Learn the security vocabulary before the architecture."),
        ("networking", "Segmentation, the core zero-trust control, is pure networking: addresses, subnets, and ports."),
    ],
    "dod-8140": [
        ("security-basics", "The DoD workforce framework is built on security fundamentals: threats, risk, and layered defense. Learn the language first."),
        ("networking", "Work roles from IAT to CND all assume networking literacy: addresses, ports, and protocols."),
    ],
    "nsa-codebreaker": [
        ("programming-basics", "Crypto puzzles and reversing assume you read code. Learn what programs are before dissecting them."),
        ("linux-cli", "Forensics and network analysis happen in the terminal. Command-line skills unlock the challenge categories."),
        ("security-basics", "Web exploitation and crypto assume the threat vocabulary and CIA thinking."),
    ],
    "nice-framework": [
        ("security-basics", "The NICE specialty areas share one vocabulary: threats, risk, and layered defense. Learn it from zero."),
        ("networking", "Protect-and-defend and operate-and-maintain roles assume networking fundamentals."),
    ],
    "blockchain-dev": [
        ("programming-basics", "Smart contracts and protocols are code. Learn what programs are before studying consensus and cryptography."),
        ("networking", "Peer-to-peer networks are the substrate of every blockchain. Addresses and ports come before protocols."),
    ],
    # math-tech is the foundations-level path itself: no prerequisite tracks.
    "math-tech": [],
    "career-launch": [
        ("programming-basics", "Tech careers orbit code. Knowing what programs are helps every interview and role discussion land."),
    ],
    "nvidia-ai": [
        ("python", "CUDA workflows, notebooks, and inference scripts are Python. Scripting comes before GPU computing."),
        ("linux-cli", "GPU servers are Linux servers: the terminal is where the computing happens."),
    ],
    "creative-code": [
        ("programming-basics", "Generative art is code that draws. Learn what programs are before making them paint."),
    ],
    "hermetica": [
        ("programming-basics", "Esoteric programming is still programming. The basics of code ground the stranger systems that follow."),
    ],
}

# slug -> [math module ids]
MATH = {
    "python": [],
    "c-lang": ["binary"],
    "cpp": ["binary"],
    "java": [],
    "dsa": ["logic", "stats"],
    "systems-cs": ["binary", "logic"],
    "react-frontend": [],
    "python-web": [],
    "spring": [],
    "dotnet": [],
    "fullstack": [],
    "ides-tooling": [],
    "git-devops": [],
    "ai-product": ["stats", "probability"],
    "comptia-core": ["binary"],
    "comptia-cyber": ["binary", "logic"],
    "comptia-infra": ["binary", "subnetting"],
    "cissp": ["binary", "logic"],
    "cism": ["logic"],
    "aws-clf": ["binary"],
    "aws-saa": ["binary", "subnetting"],
    "aws-soa": ["binary", "subnetting"],
    "aws-dop": ["binary", "subnetting"],
    "aws-scs": ["binary", "subnetting"],
    "aws-data": ["stats", "probability"],
    "aws-ml": ["stats", "probability", "linalg"],
    "ms-fundamentals": [],
    "az-104": [],
    "az-305": [],
    "az-700": ["binary", "subnetting"],
    "azure-developer": [],
    "dp-203": ["stats", "probability"],
    "sc-200": ["logic"],
    "sc-300": [],
    "m365": [],
    "oracle-oci": ["subnetting"],
    "oracle-sql": [],
    "oracle-db": [],
    "sql": [],
    "mongodb": [],
    "data-engineering": ["stats", "probability"],
    "data-analyst": ["stats", "probability"],
    "datascience-ml": ["stats", "probability", "linalg"],
    "llm-engineering": ["stats", "probability", "linalg"],
    "linux-essentials": [],
    "rhcsa": [],
    "rhce": [],
    "k8s-associate": ["binary", "subnetting"],
    "cka": ["binary", "subnetting"],
    "ckad": ["binary", "subnetting"],
    "docker": ["binary"],
    "terraform": [],
    "vault-consul": [],
    "openshift": ["binary", "subnetting"],
    "sre-platform": ["stats"],
    "soc-analyst": ["logic"],
    "pentest": ["binary", "subnetting"],
    "hackers-arise": ["binary", "subnetting"],
    "zerotrust": ["binary", "subnetting"],
    "dod-8140": [],
    "nsa-codebreaker": ["binary", "logic"],
    "nice-framework": [],
    "blockchain-dev": ["binary"],
    "math-tech": [],
    "career-launch": [],
    "nvidia-ai": ["stats", "probability", "linalg"],
    "creative-code": [],
    "hermetica": [],
}


def main():
    catalog = json.load(open(CATALOG, encoding="utf-8"))
    slugs = [e["slug"] for e in catalog["bootcamps"]]

    track_ids = {t["id"] for t in json.load(open(TRACKS_FILE, encoding="utf-8"))["tracks"]}
    math_ids = {m["id"] for m in json.load(open(MATH_FILE, encoding="utf-8"))["modules"]}
    assert math_ids == set(MATH_IDS), "math.json module ids drifted: %s" % (math_ids ^ set(MATH_IDS))

    missing_f = [s for s in slugs if s not in FOUNDATIONS]
    missing_m = [s for s in slugs if s not in MATH]
    if missing_f or missing_m:
        print("MISSING MAP ENTRIES — foundations: %s math: %s" % (missing_f, missing_m))
        sys.exit(1)

    extra_f = [s for s in FOUNDATIONS if s not in slugs]
    extra_m = [s for s in MATH if s not in slugs]
    if extra_f or extra_m:
        print("STALE MAP ENTRIES — foundations: %s math: %s" % (extra_f, extra_m))
        sys.exit(1)

    for slug in slugs:
        for track_id, _why in FOUNDATIONS[slug]:
            assert track_id in track_ids, "%s: unknown track %s" % (slug, track_id)
        for mid in MATH[slug]:
            assert mid in math_ids, "%s: unknown math module %s" % (slug, mid)

    print("%-18s | %-42s | %s" % ("bootcamp", "foundations", "math"))
    print("-" * 18 + "-+-" + "-" * 42 + "-+-" + "-" * 30)
    n_found = 0
    for slug in slugs:
        path = os.path.join(CONTENT_DIR, slug + ".json")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("slug") != slug:
            print("SKIP %s: slug mismatch in file" % slug)
            continue
        data["foundations"] = [
            {"track": tid, "why_needed": why} for tid, why in FOUNDATIONS[slug]
        ]
        data["math"] = list(MATH[slug])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        n_found += len(FOUNDATIONS[slug])
        print("%-18s | %-42s | %s" % (
            slug,
            ", ".join(t for t, _ in FOUNDATIONS[slug]) or "(none)",
            ", ".join(MATH[slug]) or "(none)",
        ))

    print()
    print("wrote foundations+math for %d bootcamps (%d foundation assignments)" % (len(slugs), n_found))


if __name__ == "__main__":
    main()
