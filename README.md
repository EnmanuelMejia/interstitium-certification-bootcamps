# Interstitium Labs — Certification Bootcamp Catalog

An enterprise-grade platform of **75 interactive, adaptive certification-prep bootcamps** covering the full Interstitium Labs catalog: programming languages, web frameworks, developer tooling, CompTIA, AWS, Microsoft/Azure, Oracle, databases, Linux, cloud-native, security, government/NSA programs, data/AI, and career tracks.

**Live hub:** https://enmanueldmejia.com/bootcamps/

## Architecture

One shared platform, zero per-path duplication:

```
content/<slug>.json      # per-bootcamp practice content (schema: docs/content-schema.md)
catalog.json             # definitive catalog: 75 bootcamps, groups, vendor info, catalog-node mappings
engine/
  bootcamp.js            # shared engine: scenarios, adaptive drill queue, mastery (localStorage), timed simulation
  chat.js                # shared AI-practice-companion engine (keyword-heuristic feedback)
  style.css              # shared theme (per-path accent via CSS variables)
  hub.js                 # hub search/filter enhancement
  learn.js               # Learn view: domain lessons (concepts, worked examples, pitfalls)
  terminal.js            # Terminal view: interactive command-practice emulator
  labs.js                # Labs view: guided multi-step labs with command checks
templates/               # hub.html, bootcamp.html, chat.html shells
generator/build.py       # builds site/ from catalog.json + content/
site/                    # deployable static output (generated, not hand-edited)
  index.html             # unified catalog hub
  catalog-map.json       # machine-readable bootcamp → catalog-node map
  bootcamps/<slug>/      # index.html + chat/ + content.json per bootcamp
  engine/                # shared assets
  worker.js              # edge router (/bootcamps/* → assets)
deploy/
  worker-config.json     # deploy-worker-assets config (worker: cert-bootcamps)
  create-routes.py       # creates /bootcamps/* routes on the three domains
```

## Build

```bash
python3 generator/build.py [--clean]
```

Validates every content file against the schema (hard errors exclude that path's
`content.json` but still emit its shells; exit 2), then writes `site/`.

## Deploy

Production deploy uses the Cloudflare `deploy-worker-assets` flow (Static Assets —
see `~/workspace/skills/cloudflare/SKILL.md`):

```bash
# from the repo root, with the custom.cloudflare credential available
deploy-worker-assets deploy/worker-config.json
python3 deploy/create-routes.py
```

Routes: `enmanueldmejia.com/bootcamps/*`, `interstitiumlabs.dev/bootcamps/*`,
`learn.interstitiumlabs.dev/bootcamps/*` → worker `cert-bootcamps`.

## Content principles

- **Original practice content only.** No real exam questions are reproduced for any
  vendor (CompTIA, AWS, Microsoft, Oracle, Red Hat, HashiCorp, CNCF, ISC2, ISACA…).
  Scenarios teach underlying concepts from public exam objectives.
- **Honest framing.** Every bootcamp names its vendor, states no affiliation or
  endorsement, and confers no certificate. Government paths (DoD 8140, NSA
  Codebreaker Challenge, NICE Framework) are verified against public .gov/.mil
  sources; nothing is invented.
- **Any-candidate product.** No personal data in any bootcamp.

## Catalog map

`site/catalog-map.json` links every bootcamp URL to its catalog nodes on
`interstitiumlabs.dev` and `learn.interstitiumlabs.dev` (paths, sequences,
academies). The hub UI surfaces the same mapping per card.

Built by [Interstitium Labs](https://interstitiumlabs.dev) — Enmanuel D. Mejia, Founder.
