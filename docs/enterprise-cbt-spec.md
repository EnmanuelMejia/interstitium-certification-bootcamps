# Enterprise CBT Upgrade — Spec & Schema (Phase 1)

Date: 2026-10-04. Coordinator spec for the "full enterprise-level computer-based
adaptive training" upgrade across all 68 bootcamps in `~/workspace/cert-bootcamps`.

Source of truth for content: `content/<slug>.json` (generator copies to
`site/bootcamps/<slug>/content.json` via `generator/build.py`).
New SVG media assets: `content/<slug>/assets/diagrams/*.svg` (generator must
copy `content/<slug>/assets/` → `site/bootcamps/<slug>/assets/` — Phase 3 task).

## 0. Standing rules (non-negotiable, all workers)

- Original practice content ONLY. Never reproduce real exam questions (no braindumps),
  no vendor affiliation claimed, confers no certificate. Every bootcamp keeps its disclaimer.
- Simulated terminals/consoles are sandboxes — never real shells, never real cloud accounts.
- Technical accuracy over volume: a wrong diagram/lab is worse than a missing one. Self-review domain facts.
- Vanilla JS, ES5-compatible, zero dependencies, offline-capable (no network calls in engines).
- Backward compatible: every new content.json key is OPTIONAL; engines must degrade gracefully when absent.
- Concurrency: workers NEVER edit `content/<slug>.json` directly. Each worker writes
  FRAGMENT files (below); the coordinator merges in Phase 3. Only Worker 1 touches
  `engine/` and `templates/`.

## 1. Extended content.json schema (all new keys optional)

### 1.1 `simulations[]` — consumed by engine/simulations.js
```json
{
  "id": "py-sim-debug-1", "title": "…", "kind": "troubleshoot|branching|ordering|config-check",
  "domain_id": "fundamentals", "difficulty": 1,
  "brief": "2–4 sentence scenario setup",
  "steps": [ /* kind-specific, see below */ ],
  "debrief": "what the exercise taught (2–4 sentences)",
  "points": 10
}
```
Kind-specific `steps`:
- `troubleshoot`: `[{"symptom":"…","evidence":[["file","text"],…],"options":["…","…","…","…"],"correct":0,"explain":"…"}]` — 2–4 sequential diagnostic steps; each step picks the right next action.
- `branching`: `[{"id":"s1","text":"…","choices":[{"label":"…","next":"s2|END","points":2,"feedback":"…"}]}]` — decision tree; `next:"END"` ends the run; terminal nodes may carry `"outcome":"good|bad"`.
- `ordering`: `{"context":"…","items":["step A","step B",…], "correct_order":[2,0,1,…]}` — items shown shuffled; candidate drag/click-orders them; correct_order lists item indices in right sequence.
- `config-check`: `{"config":"line1\nline2\n…","find":2,"issues":[{"line":3,"description":"…","fix":"…"}]}` — candidate clicks the misconfigured lines (max ~12 lines of config).

### 1.2 `media[]` — consumed by learn.js (embedded) + Media section
```json
{"id":"py-closures-diagram","kind":"diagram","title":"…",
 "svg":"assets/diagrams/py-closures.svg","lesson_ref":"c-fundamentals",
 "caption":"…","alt":"plain-text description of the diagram"}
```
- `svg` path is relative to the bootcamp dir (`site/bootcamps/<slug>/assets/diagrams/…`).
- `lesson_ref` = lesson card id (`c-<domain_id>` per learn.js convention) OR `"resources"` to show only in Resources/Media view.
- Worker 2 target: ≥1 diagram per lesson section in every bootcamp (i.e. every `lessons[]` entry gets ≥1 media item with matching `lesson_ref`).

### 1.3 `resources{}` — consumed by learn.js Resources view
```json
{"cheatsheet":{"title":"…","sections":[{"heading":"…","items":["term — definition",…]}]},
 "glossary":[{"term":"…","def":"…"}],
 "links":[{"label":"…","url":"https://…","note":"…"}],
 "checklist":["…"]}
```
- `links`: REAL URLs only; Worker 3 must curl-verify each returns HTTP 200 before including. Prefer official vendor docs, RFCs, NIST pubs.
- `cheatsheet`/`glossary` generated FROM the bootcamp's own lessons (key terms, commands, ports, defaults).

### 1.4 `consoleSims[]` — consumed by engine/consoles.js
```json
{"id":"aws-sim-vpc-1","title":"…","console":"aws-vpc","domain_id":"…","difficulty":1,
 "brief":"…",
 "tasks":[{"id":"t1","instruction":"…","validate":{"action":"create-subnet","params":{"cidr":"10.0.1.0/24"}},"hint":"…"}],
 "debrief":"…"}
```
- `console` selects the simulated console UI. Supported console types (Worker 1 defines; content workers use only these):
  `aws-vpc`, `aws-iam`, `azure-portal`, `gcp-console`(generic cloud), `k8s-dashboard`,
  `firewall`, `switch-cli`, `linux-desktop`(file manager/permissions), `sql-studio`,
  `git-host`(PR review UI), `cicd-pipeline`, `siem-dashboard`, `ticketing`(incident queue),
  `code-editor`(IDE w/ debugger), `db-admin`, `generic-web`(fallback form-based console).
- `validate.action` is a string the console type understands; `params` the expected state.
  Worker 1 documents the action vocabulary per console type in engine/consoles.js header.

### 1.5 `terminalMissions[]` — consumed by engine/missions.js
```json
{"id":"py-mission-1","title":"…","domain_id":"…","difficulty":1,
 "brief":"…","objectives":["…"],
 "checks":[{"command_pattern":"^python3?\\s+app\\.py","expect_contains":"Result: 42","hint":"…"}],
 "success_message":"…"}
```
- Same check contract as labs.js: regex on the typed command AND substring in the
  terminal output. Missions MUST use commands/outputs that actually exist in the
  bootcamp's terminal profile (read `engine/terminal.js` profiles). If a mission needs
  a command the profile lacks, DO NOT invent output — note it in your report as
  `NEEDS-COMMAND: <slug> <profile> <command>`; the coordinator adds profile commands in Phase 3.

## 2. Engine contracts (Worker 1)

New files (vanilla JS, ES5, zero deps, IIFE modules like existing engines):
- `engine/simulations.js` — listens `ilb:view` detail `'exercises'`; renders sim cards + runner for all 4 kinds; validation + scoring; LS key `ilb-bootcamp-<slug>-sims-v1`; exposes `window.SimsView = {render}`; testing seam `window.ENGINE_TEST → window.__simsEngine` (pure validators).
- `engine/consoles.js` — listens `ilb:view` detail `'console'`; renders console-type UIs with task list + validation; LS key `ilb-bootcamp-<slug>-console-v1`; exposes `window.ConsoleView`; documents action vocabulary in header comment.
- `engine/missions.js` — listens `ilb:view` detail `'missions'`; card UI like labs.js; hooks `window.ILBTerminal.onCommand`; LS key `ilb-bootcamp-<slug>-missions-v1`; exposes `window.MissionsView`.
- learn.js extension (edit in place): embed `media[]` diagrams inside lesson decks (after the example slide) + new Resources view rendered on `ilb:view` detail `'resources'` (cheatsheet, glossary, links, checklist). Keep existing lecture ids working.
- bootcamp.js extension (edit in place): add `window.ILBProgress = { domainMastery(), nextRecommendations() }`; the dashboard "next up" panel recommends next labs/simulations/missions in the weakest domain (reads the other LS keys; tolerates missing engines).
- `templates/bootcamp.html`: add nav buttons + `<section class="view">` blocks for `exercises`, `console`, `missions`, `resources`; add `<script>` tags for the 3 new engines (defer, after labs.js). New view ids: `view-exercises`/`exercisesBody`, `view-console`/`consoleBody`, `view-missions`/`missionsBody`, `view-resources`/`resourcesBody`.
- `generator/build.py`: copy `content/<slug>/assets/` → `site/bootcamps/<slug>/assets/` when present; new engine files are copied verbatim by the existing engine-copy loop (verify `simulations.js`, `consoles.js`, `missions.js` land in `site/bootcamps/engine/`).
- `test/smoke.js`: extend with pure-logic tests for the new engines' validators (optional but preferred).

## 3. Fragment files (concurrency protocol)

- Worker 2 writes per bootcamp: `content/<slug>/assets/diagrams/*.svg` + `content/<slug>/fragments/media.json` → `{"media":[…]}`.
- Worker 3 writes per bootcamp: `content/<slug>/fragments/resources.json` → `{"resources":{…}}`.
- Workers 4–7 write per bootcamp: `content/<slug>/fragments/extended.json` → `{"labs_add":[…],"simulations":[…],"consoleSims":[…],"terminalMissions":[…]}`.
- Phase 3 merge: `labs = labs + labs_add`; others assigned directly. Fragments are then deleted from `content/` (they do not ship).

## 4. Per-bootcamp volume targets

- Labs: 8 total (4 existing + 4 new), difficulty progression 1→3.
- Simulations: ≥4 (mix of kinds; ≥2 kinds per bootcamp).
- Console sims: ≥2 (console type must fit the domain — e.g. aws-* → aws-vpc/aws-iam; k8s → k8s-dashboard; pentest → siem-dashboard or switch-cli; sql → sql-studio).
- Terminal missions: ≥6 (difficulty 1→3; wired to the slug's real terminal profile commands).
- Media: ≥1 diagram per lesson (Worker 2).
- Resources: full pack (Worker 3).

## 5. Terminal profile map (for mission authors — read the profile before writing checks)

aws→aws-profile · azure/ms→az · k8s/cka/ckad/openshift→kubectl · terraform→terraform ·
docker→docker · git-devops→git · vault-consul→vault · mongodb→mongosh · oracle-oci/db→oci ·
sql/oracle-sql/dp-203/data-engineering/data-analyst→sql · linux/rhcsa/rhce/sre/comptia*/cissp/cism/pentest/soc/zerotrust/dod-8140/nice/hackers-arise/nsa-codebreaker/systems-cs→bash ·
python/datascience/llm/nvidia-ai/dsa/ml→python · everything else→bash-lite (+flavor extras).
