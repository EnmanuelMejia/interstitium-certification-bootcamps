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
