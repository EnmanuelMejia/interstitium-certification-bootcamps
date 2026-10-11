# FIX_REPORT3 — CBT Interactive Elements Root Cause

**Date:** 2026-10-10
**Issue:** Terminal, drills, quiz submit, and mock staging all non-functional in real browser, even after app.min.js was populated.

## Root Cause: Stale Service Worker Cache

The JavaScript code is **correct**. Verified via jsdom simulation:
- Terminal view renders (profile selector, prompt area)
- Drills view renders (question UI, start button)
- Mock view renders (stage button)
- Quiz submit logic correct
- Zero JS errors, zero broken references
- All bundles (source, mirror, live) identical and syntactically valid

The failure was **client-side**: the service worker (`sw.js`) uses cache-first strategy with a static cache name (`tl-infra-prep-v1`). Browsers that visited during the broken state (empty app.min.js) cached the broken bundle. Subsequent deploys updated the server files, but the SW kept serving the stale cached empty bundle.

This is the classic SW stale-cache trap: the server is correct, the code is correct, but the client never fetches the fix.

## Fix Applied

1. **Bumped SW cache version**: `tl-infra-prep-v1` → `tl-infra-prep-v2` in `sw.js`
   - The `activate` handler deletes all non-current caches, so v1 gets purged
   - `skipWaiting()` + `clients.claim()` ensure immediate takeover

2. **Added cache-busting query param**: `<script src="app.min.js?v=2">` in `index.html`
   - Defensive measure for HTTP-level browser cache (non-SW path)

3. **Deployed** via `deploy-worker-assets` to the `cert-bootcamps` worker
   - Config: `/tmp/cert-bootcamps-deploy.json`
   - Deployed at 2026-10-10T18:29:30Z

## Verification

| Check | Result |
|---|---|
| Live sw.js cache version | `tl-infra-prep-v2` ✓ |
| Live index.html script tag | `app.min.js?v=2` ✓ |
| Live app.min.js has terminal code | Yes (createTerminal present) ✓ |
| Live drill-data.json | 200 ✓ |
| jsdom full simulation | 0 errors, all views render ✓ |

## How the Fix Propagates

On next page visit, the browser will:
1. Detect sw.js byte-change → install new SW
2. New SW fetches fresh assets with `cache: 'reload'` (bypasses HTTP cache)
3. On activate: delete v1 cache, claim clients
4. Page serves fresh app.min.js → interactive elements work

## Remaining: Rendered Verification Needed

A live browser test should confirm the terminal renders a prompt, drills accept input, quiz submit enables, and mock staging works. The parent should delegate this to a browser task with a **fresh browser profile** (or hard refresh + SW unregister) to avoid the old cache.

## Files Changed

- `~/workspace/cbt-individual/tl-infra-assessment-prep/sw.js` (v1 → v2)
- `~/workspace/cbt-individual/tl-infra-assessment-prep/index.html` (app.min.js?v=2)
- Both synced to `~/workspace/cert-bootcamps/site/bootcamps/tl-infra-assessment-prep/`
- Deployed to `cert-bootcamps` worker
