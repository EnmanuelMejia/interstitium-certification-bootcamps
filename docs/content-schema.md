# Content Schema — cert-bootcamps

Each bootcamp is ONE JSON file: `~/workspace/cert-bootcamps/content/<slug>.json`.
Write valid JSON (UTF-8, no trailing commas). The platform generator builds the
bootcamp page + chat companion from this file. Follow this schema exactly.

## Top-level

```json
{
  "slug": "python",
  "title": "Python Programming",
  "tagline": "One-line hook shown on the hub card and bootcamp hero.",
  "vendor": {"name": "Python Institute", "certs": "PCEP, PCAP", "docs": "https://pythoninstitute.org"},
  "disclaimer": "Independent practice material by Interstitium Labs. Not affiliated with, endorsed by, or sponsored by <Vendor>. Confers no certificate. All scenarios are original; no exam content is reproduced.",
  "domains": [ ... ],
  "behavioral": [ ... ],
  "chat": { ... }
}
```

- `slug`, `title`, `tagline`, `vendor` come from `catalog.json` (copy exactly).
- `disclaimer`: always present; name the real vendor; never claim affiliation.

## Domains (4–6 per bootcamp; domain names come from catalog.json)

Each domain: 6–8 scenarios (aim ~32–40 total per bootcamp).

```json
{
  "id": "basics",
  "name": "Language Fundamentals",
  "scenarios": [
    {
      "id": "py-mutable-default",
      "title": "The shared-list surprise",
      "situation": "A teammate's function accumulates results across calls in a way nobody expected. You open the file.",
      "prompt": "What is the root cause, and what is the correct fix?",
      "evidence": [
        ["app.py", "def collect(items=[]):\n    items.append(1)\n    return items"]
      ],
      "choices": [
        "Default argument evaluated once at def time — use None and create inside",
        "List.append is not thread-safe — add a lock",
        "Python caches small lists — call list.clear() first",
        "The interpreter reuses the name — rename the parameter"
      ],
      "answer": 0,
      "why": "Default arguments are evaluated once when the function is defined, so the same list object is shared across calls. The standard fix is items=None with a fresh list created inside the body.",
      "hint": "When does Python evaluate a default argument value?",
      "objectives": ["Function semantics", "Mutable defaults"],
      "mins": 6
    }
  ]
}
```

Rules:
- `id`: unique within the bootcamp, kebab-case.
- `choices`: exactly 4, plausible distractors, one clearly best.
- `answer`: 0-based index of the correct choice.
- `evidence`: 0–4 [label, text] pairs (code, terminal output, config). Keep each under ~12 lines.
- `why`: teaches the concept (2–4 sentences). `hint`: Socratic nudge, never the answer.
- `mins`: estimated minutes (4–12).
- ORIGINAL CONTENT ONLY. Never reproduce real exam questions — no braindumps, for CompTIA/AWS/Microsoft/Oracle/Red Hat/HashiCorp/CNCF or any vendor. Write original scenario-style questions that teach the underlying concepts from the official exam OBJECTIVES (objectives are public; questions must be yours).
- No invented facts: commands, flags, API names, default ports, and limits must be real. If unsure, use only what you can verify from the vendor docs URL in catalog.json or write the scenario around concepts, not trivia.

## Behavioral (8 prompts)

```json
{
  "prompt": "Tell me about a time you debugged a production issue under pressure.",
  "framework": "STAR",
  "points": ["Set the scene in one sentence", "Your specific actions", "Measurable outcome"],
  "pitfalls": ["Blaming others", "No outcome stated"]
}
```

## Chat companion

```json
{
  "persona": "You are a friendly but rigorous Python interviewer running a mock assessment.",
  "topics": [
    {
      "id": "basics",
      "name": "Language Fundamentals",
      "key_points": ["mutable default args", "scope LEGB", "comprehensions", "generators vs lists"],
      "followups": ["Can you give an example?", "What would break if...?"]
    }
  ]
}
```

- One topic per domain (same ids/names). 4–6 key_points each — these drive the keyword-heuristic feedback.
- Generic, any-candidate framing. No personal data.

## Volume targets

- 30–40 scenarios per bootcamp (6–8 per domain)
- 8 behavioral prompts
- chat topics covering every domain

## Optional platform fields (added by the platform team — all safe to omit)

These extend the schema without renaming or removing anything above.
Omit any of them and the engine uses the stated default.

```json
{
  "accent": "#3ddc97",
  "simulation": {"items": 12, "minutes": 180, "evidence_cost_mins": 0},
  "domains": [
    {"scenarios": [{"desc": "Short card blurb (fallback: first ~140 chars of situation)"}]}
  ],
  "chat": {
    "topics": [
      {
        "prompt": "Custom opening question for this topic (fallback: engine-generated)",
        "hint": "Custom hint-chip text (fallback: generic, never leaks key points)"
      }
    ]
  }
}
```

- `accent`: hex color theming this bootcamp (`--accent` / `--accent-soft` / `--accent-ink`). Default: platform green `#3ddc97`.
- `simulation.items` / `.minutes`: lineup size and clock (defaults 12 / 180). `.evidence_cost_mins`: minutes deducted per evidence source opened during the sim (default 0 = free; the reference design used 2).
- `desc`: one-line scenario blurb for library cards.
- `chat.topics[].prompt` / `[].hint`: per-topic overrides; the engine generates honest fallbacks when absent.

## Learn & Labs (optional top-level fields — safe to omit)

Two optional arrays that power the Learn and Labs views. Omit either (or
both) and the corresponding view renders the branded "content on the way"
empty state; nothing else changes.

```json
{
  "lessons": [
    {
      "domain_id": "basics",
      "title": "Reading the evidence first",
      "concepts": ["Defensive reading", "Hypothesis before verdict"],
      "example": {
        "lang": "python",
        "code": "def collect(items=[]):\n    items.append(1)\n    return items",
        "walkthrough": "Default arguments evaluate once at def time, so the same list is shared across calls."
      },
      "pitfalls": ["Skimming the prompt and jumping to the first plausible answer"],
      "try_it": "Open the evidence panel and trace what each line does before choosing."
    }
  ],
  "labs": [
    {
      "id": "lab-guided-scan",
      "title": "Guided service scan",
      "objective": "Identify open services on the target host.",
      "steps": ["Open the terminal view", "Run a service scan against the target"],
      "checks": [
        {"command_pattern": "nmap.*", "expect_contains": "open", "hint": "Try nmap -sV <target>"}
      ],
      "success_message": "Lab complete — you enumerated the open services."
    }
  ]
}
```

- `lessons[].domain_id` matches a `domains[].id` from the same file.
- `lessons[].concepts`: 3–6 short concept labels. `example`: one runnable
  snippet (`lang` = language or shell), `walkthrough` explains it in 2–4
  sentences. `pitfalls`: common mistakes to avoid. `try_it`: one hands-on
  prompt for the learner.
- `labs[].id`: unique, kebab-case. `steps`: ordered instructions.
  `checks[]`: `command_pattern` (regex the learner's command must match),
  `expect_contains` (substring the command output must contain), `hint`
  (shown after a failed check). `success_message`: shown when all checks pass.
- The original-content rules above apply to both: no real exam questions,
  no invented facts — commands, flags, API names, and defaults must be real.

## Foundations, Math & Sections (optional top-level fields — safe to omit)

Every bootcamp assumes zero prior knowledge, so prerequisites are taught
inside the platform itself rather than assumed. Three optional fields power
this; omit any of them and the Learn view simply skips that block.

```json
{
  "foundations": [
    {
      "track": "linux-cli",
      "why_needed": "The CKA is a hands-on terminal exam on Linux. Command-line fluency is non-negotiable."
    }
  ],
  "math": ["binary", "subnetting"],
  "sections": [
    {
      "id": "sec-networking",
      "title": "Networking for this path",
      "kind": "foundation",
      "lectures": [],
      "lab_ids": ["lab-guided-scan"],
      "drill_domain_ids": ["networking"]
    }
  ]
}
```

- `foundations[]`: prerequisite tracks for this bootcamp (1–3 typical).
  `track` is an id from the shared `engine/foundations.json` asset;
  `why_needed` is 1–2 sentences explaining why *this* certification needs
  *this* prerequisite. The Learn view renders the track's lectures inline.
- `math[]`: ids of shared math modules from `engine/math.json` this
  bootcamp needs: `binary`, `subnetting`, `logic`, `stats`, `probability`,
  `linalg`. Empty list allowed (omit or `[]` when the path needs no math
  beyond its own content).
- `sections[]`: Learn-view groupings. `id` unique kebab-case; `title`
  display name; `kind` one of `foundation` (prerequisite material),
  `core` (the path's own domains), `math` (math modules); `lectures[]`
  slide-model lectures; `lab_ids[]` referencing `labs[].id` in the same
  file; `drill_domain_ids[]` referencing `domains[].id` in the same file.
- Omit `foundations`, `math`, or `sections` (or pass empty arrays) and the
  corresponding Learn block renders nothing; nothing else changes.

## Shared assets: engine/foundations.json + engine/math.json

Two JSON assets ship at the engine level and are copied verbatim into
`site/bootcamps/engine/` by `generator/build.py`. They are the single
source of truth for prerequisite teaching — no per-bootcamp duplication.

`engine/foundations.json` (source of truth:
`generator/foundation-tracks.json`):

```json
{
  "tracks": [
    {
      "id": "linux-cli",
      "title": "Linux Command Line",
      "audience": "Beginners comfortable opening a terminal who need real Linux skills.",
      "lectures": [
        {
          "id": "linux-files-folders",
          "title": "Files, folders, and where you are",
          "slides": [
            {"kind": "title", "heading": "...", "lede": "...", "narration": "..."},
            {"kind": "bullets", "heading": "...", "bullets": ["..."], "narration": "..."},
            {"kind": "diagram", "heading": "...",
             "diagram": {"type": "flow", "title": "...", "nodes": ["..."], "note": "..."},
             "narration": "..."},
            {"kind": "code", "heading": "...",
             "code": {"lang": "shell", "code": "..."},
             "walkthrough": "...", "narration": "..."},
            {"kind": "bullets", "heading": "Common pitfalls", "bullets": ["..."], "narration": "..."},
            {"kind": "tryit", "heading": "...", "text": "...", "narration": "..."}
          ]
        }
      ]
    }
  ]
}
```

`engine/math.json`:

```json
{
  "modules": [
    {
      "id": "binary",
      "title": "Binary & Number Bases",
      "why": "One or two sentences on why this math matters across the catalog.",
      "lectures": [ ... same slide model as above ... ]
    }
  ]
}
```

### Slide model (shared contract with the Learn renderer)

- Every lecture: 4–7 slides. Every slide carries a `narration` transcript
  (1–3 sentences; accessibility + SEO).
- Slide kinds: `title` (`heading`, `lede`, `narration`); `bullets`
  (`heading`, `bullets[]`, `narration`); `diagram` (`heading`,
  `diagram{type,title,nodes[],note}`, `narration`); `code` (`heading`,
  `code{lang,code}`, `walkthrough`, `narration`); `tryit` (`heading`,
  `text`, `narration`).
- Diagrams: at least 1 per lecture. `type` is one of
  `flow` | `layers` | `cycle` | `compare` | `hierarchy` | `timeline`;
  `nodes[]` are short labels (≤5 words); `note` is one clarifying sentence.
- Code examples are tiny and valid; arithmetic walkthroughs use
  `"lang": "text"` with step-by-step working.
- Content principles apply to all shared assets: original teaching prose
  only (never reproduce exam questions or vendor materials), honest
  framing (no affiliation claimed, confers no certificate), true-beginner
  level (assume the reader knows nothing), any-candidate product
  (no personal data).
