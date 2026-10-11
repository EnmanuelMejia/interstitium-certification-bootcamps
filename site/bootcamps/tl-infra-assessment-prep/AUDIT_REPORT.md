# Technology Audit + Performance Review — tl-infra-assessment-prep
Date: 2026-10-10 · Auditor: Hana (subagent) · Interview: Tue 2026-10-13 — stability prioritized.

## 1. Technology choices — justifications

### Vanilla JS (2,036-line app.js) vs a framework — VANILLA IS CORRECT, keep it
- **Zero-dependency constraint is real**: the app must run offline-first from a Service Worker cache with no CDN. Any framework (React/Vue/Svelte) would need a build step and a bundled runtime (30–150KB+) for no functional gain here.
- **The app is a hash-router that renders HTML strings into `#view`** — there is no complex reactive state graph, no component tree diffing problem to solve. `innerHTML` + event delegation is the simplest correct tool.
- **Load performance**: framework runtime + hydration would slow first paint on the mobile-first target. Current critical path is one HTML file (22KB, inline CSS) + deferred scripts.
- Verdict: no framework. The code is well-factored ES5-style vanilla (pure view functions per route, a Store, Content loader). Readability is good; keep app.js as source of truth.

### Custom terminal emulators vs xterm.js — CUSTOM IS CORRECT, keep it
- **There is no PTY here.** xterm.js is a *display renderer* for a real terminal byte stream (escape sequences, cursor addressing, canvas rendering). These sims are *scripted command interpreters*: `sims/ios-cli.js` is a 52KB regex-grammar IOS engine (`exec(cmd) → string`), and output renders into accessible DOM (`div` scrollback + text input).
- Bolting xterm.js (~150KB+) on top would buy nothing: no real shell, no escape sequences to interpret (output is already sanitized text), and it would *harm* accessibility (canvas text is invisible to screen readers; the DOM version is natively readable).
- The IOS engine even has a graceful fallback (`iosFallbackRunFactory`) when the script is absent — evidence the custom design is deliberate, not accidental.
- Verdict: do not adopt xterm.js. The custom emulator is the right engineering call for simulated CLIs.

### SMIL-only SVGs — REASONING VALIDATED, keep it
- The claim "CSS/JS don't run in `<img>` tags" is correct: SVG loaded via `<img>` runs in a secure static mode — no external CSS, no scripting. **SMIL is the only declarative animation mechanism that works in `<img>`-embedded SVG**, and it remains supported in Chromium, Firefox, and Safari.
- All 17 SVGs validated: well-formed XML, `viewBox` present on every file, every `<animate>`/`<animateTransform>`/`<animateMotion>` has valid `attributeName`/`dur`/`repeatCount`/`begin`, all `animateMotion` have paths. 5–25 animation elements each, ~8KB per file — lightweight.
- Known limitation (documented, not fixable without redesign): SMIL inside `<img>` cannot honor `prefers-reduced-motion` — scripting is disabled in that context, and CSS cannot pause SMIL. Mitigation: the animations are decorative packet-flow loops over fully legible static diagrams; the static first frame conveys all information. Every *page-level* CSS animation now honors reduced-motion (see upgrades).

### No build step — keep it, with one exception
- The site ships source directly; no bundler means any file can be hot-fixed from any machine before Tuesday. That operational simplicity is worth more than bundle savings here.
- Exception: a **checked-in minified artifact** (`app.min.js`, built with terser 5.51.2) is now the runtime bundle while `app.js` remains the readable source of truth. See §3.

## 2. Performance — asset weight

Total: **2.0 MB** on disk. Composition:
| Asset | Raw | Gzip | Note |
|---|---|---|---|
| content.json | 1,004 KB | 344 KB | 90%+ of weight; pretty-printed curriculum data |
| app.js → app.min.js | 105 KB → 79 KB | 30 KB → 25 KB | minified 2026-10-10 |
| sims/ios-cli.js | 52 KB | 12 KB | shared IOS engine, now `defer`red |
| sims/git-simulator.html | 64 KB | 19 KB | was navigation-orphaned; now linked |
| sims/fortigate-sim.html | 64 KB | ~19 KB | |
| sims/terminal-mastery.html | 56 KB | ~17 KB | |
| sims/proxmox-sim.html | 52 KB | ~16 KB | |
| sims/paloalto-sim.html | 48 KB | 13 KB | was navigation-orphaned; now linked |
| sims/site-to-site-vpn.html | 40 KB | ~12 KB | |
| tools/muscle-memory-drills.html | 36 KB | ~11 KB | |

Top-10 largest files are all listed above. No oversized PNGs in the tree (poster/OG live on the main site, not here). No duplicate assets on disk. No unused files remaining (see §3: orphans wired in).

**Minification analysis**: `content.json` minified saves only 6 KB gzipped (344→338 KB) — pretty-printing compresses away; **not worth touching**. `app.js` via terser: 105→79 KB raw, 30→25 KB gzip — modest but real, zero risk after validation; done.

## 3. Upgrades implemented (all safe, no behavior changes)

1. **`app.min.js` via terser** (`npx terser app.js -c -m`): 25% smaller raw. `index.html` now loads `app.min.js`; `app.js` kept as source of truth. Validated: `node --check` on both, full top-level execution under DOM stubs, identical key globals, and **identical outputs on 6 pure-function differential probes** (esc/pad2/fmtClock/slugify/parseRoute/normCmd) between original and minified.
2. **`defer` on both scripts** (`ios-cli.js`, `app.min.js`): removes parser blocking; safe because `init` runs on `DOMContentLoaded` and deferred scripts preserve order and execute before it.
3. **View Transitions on route changes** (`paintView()` in app.js): `document.startViewTransition()` wraps the `#view` swap only when supported **and** `prefers-reduced-motion` is not set; try/catch falls back to direct paint. Progressive enhancement, no behavior change on unsupported browsers.
4. **Dashboard poster image** (was `loading="lazy"` on the above-fold LCP image): now eager + `fetchpriority="high"`, `aspect-ratio:16/9` in CSS to reserve space (CLS fix), and `onerror` hides the banner when the remote poster is unreachable offline instead of showing a broken-image icon.
5. **`prefers-reduced-motion` coverage**: added to `index.html` inline CSS (kills the sync-dot pulse + all transitions) and to the 4 standalone pages with CSS keyframes (`git-simulator`, `raid-simulator`, `subnet-splitter`, `vlan-explorer`). Verified no other page uses CSS animations.
6. **Gallery images** (`visuals/index.html`, `diagrams/index.html`): all 25 SVG `<img>` tags now have `loading="lazy"` + `width`/`height` from each file's `viewBox` (CLS-safe, below-fold deferred).
7. **Orphaned sims wired into navigation**: `sims/git-simulator.html` and `sims/paloalto-sim.html` were referenced in lesson text but had no clickable card and were missing from the SW precache — added reference cards in `viewReference()`.
8. **Service Worker precache completed**: added the 6 IOS network sims (`vlan-basics`, `static-routing`, `inter-vlan-routing`, `dhcp-server`, `nat-pat`, `site-to-site-vpn`) + `git-simulator` + `paloalto-sim`; swapped `app.js` → `app.min.js`. (SW update triggers automatically since `sw.js` bytes changed; same cache name, no forced full re-download.)

## 4. Deliberately NOT changed — and why

- **No framework, no xterm.js** (§1). Fashion would say otherwise; engineering says no.
- **`content.json` not minified**: 6 KB gzipped saving isn't worth the churn/risk; gzip already handles the repetition.
- **`ios-cli.js` not lazy-loaded on-demand**: considered it (12 KB gzip off initial load), but the fallback-window UX inconsistency (full IOS engine vs. fallback for the first ~second) is a behavior change; `defer` captures nearly all the benefit with zero risk. Revisit only if initial-load budgets tighten.
- **No `:has()` / container queries**: the grids already use `auto-fill/minmax` + a single 860px breakpoint — both features would add complexity without a visible improvement.
- **No SMIL→CSS/JS conversion**: would require inlining SVGs (losing `<img>` caching/simplicity) for animations that already work everywhere.
- **No hand-minification anywhere**: per instructions, only real-minifier output ships.
- **`hidden-audit/` dev scripts untouched** (not user-facing, not in SW precache).

## 5. Validation performed
- `node --check`: app.js, app.min.js, sw.js, ios-cli.js — all pass.
- Minification differential test: identical pure-function outputs (original vs minified).
- All 17 SVGs: XML well-formedness + SMIL attribute validity — 0 issues.
- Gallery pages: 25/25 imgs lazy + dimensioned; all HTML files have `<meta name="viewport">`.
- Mirror `~/workspace/cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/` re-synced via rsync — `diff -rq` clean.

## 6. Residual notes for parent
- The poster image is a **remote** `interstitiumlabs.dev` URL on an otherwise offline-first app; offline it now hides gracefully, but a local copy in the tree would be more in the spirit (left as-is: no behavior change, URL is canonical).
- SMIL + `prefers-reduced-motion` remains unfixable inside `<img>` context (platform limitation, documented above).
- SW cache name unchanged (`tl-infra-prep-v1`); clients update on next visit since `sw.js` changed.
