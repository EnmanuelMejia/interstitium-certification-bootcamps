# Architecture — Interstitium Labs Certification Bootcamps

One shared platform, 75 bootcamps, zero per-path code. Content builders write
**JSON only** (`docs/content-schema.md`); everything else is generated.

## Layout

```
cert-bootcamps/
├── catalog.json            # 75 bootcamps: slug/title/tagline/vendor/domains/group/maps_to
├── content/<slug>.json     # per-bootcamp training content (written by content builders)
├── docs/
│   ├── content-schema.md   # the content contract (fixed; platform may ADD optional fields)
│   └── ARCHITECTURE.md     # this file
├── engine/                 # shared runtime, copied verbatim into site/
│   ├── style.css           # dark theme; --accent/--accent-soft/--accent-ink overridable
│   ├── bootcamp.js         # scenario engine (dashboard/drill/simulation/behavioral)
│   ├── chat.js             # chat-companion engine (keyword-heuristic coaching)
│   └── hub.js              # hub search/filter enhancement
├── templates/              # thin HTML shells with {{TOKENS}}
│   ├── hub.html  bootcamp.html  chat.html
├── generator/build.py      # catalog.json + content/*.json -> site/
├── deploy/
│   ├── worker-config.json  # deploy-worker-assets config (worker: cert-bootcamps)
│   └── create-routes.py    # creates the three /bootcamps/* routes (parent runs)
└── site/                   # GENERATED — never edit by hand; rebuild instead
    ├── index.html                # hub
    ├── catalog-map.json          # machine-readable slug -> catalog node refs
    ├── worker.js                 # main_module: strips /bootcamps, serves assets
    ├── engine/*                  # copied from engine/
    └── bootcamps/<slug>/
        ├── index.html            # thin shell
        ├── content.json          # copied content (only when valid)
        └── chat/index.html       # thin shell
```

## Runtime contract

Each bootcamp shell declares a page contract **before** loading the engine:

```html
<script>window.BOOTCAMP_PAGE = { slug, hubUrl, title };</script>
<script src="../../engine/bootcamp.js" defer></script>
```

`bootcamp.js` then `fetch('./content.json')` and renders the whole app.
The chat shell declares `window.CHAT_PAGE = { slug, bootcampUrl, hubUrl, title }`
and `chat.js` fetches `../content.json`. If content is missing or invalid, both
engines render an honest "content on the way" state with a link back to the hub —
they never throw, never show a blank page.

The hub is different: the generator renders all cards **statically**, and
`hub.js` only adds client-side search/group/vendor filtering over
`data-*` attributes. The hub works with JS disabled.

## Engine design (ported from the proven full-spectrum bootcamp)

**Progress** — `localStorage["ilb-bootcamp-<slug>-v1"] = { scenarioId: {a, c} }`
(`a` attempts, `c` correct). Namespaced per slug so 75 bootcamps never collide.
A scenario is *cleared* once answered correctly; mastery per domain =
cleared / total. Double-click-to-confirm reset.

**Adaptive drill queue** — domains sorted weakest-first (mastery, then
answered-count, then name). Within each domain: uncleared scenarios shuffled
first, cleared shuffled after (keeps wins warm). Queue rebuilds around new
weaknesses when exhausted.

**Simulation** — lineup round-robins weakest-first domains until
`simulation.items` (default 12) is reached, preferring uncleared scenarios.
Countdown clock (`simulation.minutes`, default 180), hints disabled, each
decision final, optional per-evidence time cost (`evidence_cost_mins`,
default 0). Results feed mastery (`recordResult`) and produce a readiness
verdict: ≥85 ASSESSMENT-READY · ≥70 NEARLY READY · ≥50 DEVELOPING · else
FOUNDATIONS FIRST, plus a per-domain breakdown.

**Chat companion** — schema `key_points` are plain strings; the engine derives
matchable cues per point (significant words len≥4 minus stopwords, plus the
full phrase). Verdict per point: ≥60% of cues → strong, some → partial, none
→ missed. Chips: Hint (never leaks key points), Model points, Skip. Debrief:
per-topic strong/points table + improvement themes (points flagged missed or
partial). All local; the disclaimer says so on the page.

## Generator

`python3 generator/build.py [--clean]`

- Validates every `content/<slug>.json` against the schema. **Hard errors**
  (invalid JSON, missing required keys, slug mismatch, bad choices/answer)
  exclude that bootcamp's `content.json` from the build — its shells still
  generate and show the "content on the way" state — and the build exits 2.
  Warnings (scenario count off-target, missing hint, topic/domain drift) print
  but don't fail.
- Copies `engine/*` verbatim, writes `site/worker.js` (edge router),
  renders hub/bootcamp/chat shells, writes `catalog-map.json`.
- Prev/next footer nav follows catalog order.
- Per-bootcamp `accent` (optional content field) is compiled to a `:root`
  override block at build time (accent + 10% soft tint + readable ink).

## Deploy (parent runs — do NOT deploy from platform work)

1. `deploy-worker-assets deploy/worker-config.json` — uploads `site/` as
   static assets to worker `cert-bootcamps` (`main_module: worker.js`,
   `run_worker_first: ["/bootcamps", "/bootcamps/*"]`).
2. `python3 deploy/create-routes.py` — or manually create in the dashboard:
   `enmanueldmejia.com/bootcamps/*`, `interstitiumlabs.dev/bootcamps/*`,
   `learn.interstitiumlabs.dev/bootcamps/*` → worker `cert-bootcamps`.

`site/worker.js` strips the `/bootcamps` prefix and delegates to
`env.ASSETS`, so one asset tree serves all three domains.

## Adding a bootcamp

1. Add the entry to `catalog.json` (copy `slug/title/tagline/vendor/domains/group/maps_to` exactly into the content file).
2. Write `content/<slug>.json` per `docs/content-schema.md`.
3. Run `python3 generator/build.py` — fix any ERROR lines, heed WARN lines.

## Testing

- `node test/smoke.js` — headless engine tests. Loads the real
  `engine/bootcamp.js` / `engine/chat.js` in Node with stub DOM/storage/fetch
  and exercises logic through the `window.ENGINE_TEST` seam (queue building,
  mastery math, sim lineup, verdict thresholds, keyword-heuristic grading).
  The seam is inert in production — generator shells never set the flag.
- `python3 test/id-check.py` — verifies every DOM id referenced by the engines
  exists in its template, and every `BOOTCAMP_PAGE`/`CHAT_PAGE` field an engine
  reads is set by its shell.
- `python3 generator/build.py` — validates all content files; exits 2 on hard
  errors (still writes the rest of the site).

## Conventions

- Zero runtime dependencies: vanilla JS/CSS only. No frameworks, no CDNs.
- Accessible markup: skip link, landmarks, `aria-label`s, focus-visible rings,
  `role="status"` on feedback, `prefers-reduced-motion` respected.
- Honest framing everywhere: disclaimers name the real vendor and deny
  affiliation; original practice content only — never reproduced exam items.
- `site/` is a build artifact. Fix the source (engine/template/content), rebuild.
