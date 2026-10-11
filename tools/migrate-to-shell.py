#!/usr/bin/env python3
"""Migrate all CBT index.html files to the unified _shell/.

Reads each CBT's existing index.html, extracts per-CBT customizations,
and regenerates from _shell/index-template.html. Also copies _shell/sw.js
per-CBT with the correct cache name.

Usage: python3 migrate-to-shell.py [--dry-run] [--only slug1,slug2]
"""
import os, re, sys, json, shutil

BASE = os.path.expanduser('~/workspace/cert-bootcamps/site/bootcamps')
SHELL = os.path.join(BASE, '_shell')
TEMPLATE = os.path.join(SHELL, 'index-template.html')
SW_TEMPLATE = os.path.join(SHELL, 'sw.js')

SKIP = {'_engine', '_shell', 'engine', 'tl-infra-assessment-prep'}

def extract(path):
    """Extract per-CBT values from existing index.html."""
    with open(path, encoding='utf-8', errors='replace') as f:
        html = f.read()
    d = {}
    def grab(pat, default=''):
        m = re.search(pat, html, re.S)
        return m.group(1).strip() if m else default
    d['meta_description'] = grab(r'<meta name="description" content="([^"]*)"')
    d['page_title'] = grab(r'<title>(.*?)</title>')
    d['og_image'] = grab(r'<meta property="og:image" content="([^"]*)"')
    # accent colors
    m = re.search(r':root\{--accent:([^;]+);--accent-soft:([^;]+);--accent-ink:([^;]+);?\}', html)
    if m:
        d['accent'], d['accent_soft'], d['accent_ink'] = m.group(1), m.group(2), m.group(3)
    else:
        d['accent'], d['accent_soft'], d['accent_ink'] = '#2f81f7', 'rgba(47,129,247,.10)', '#0d1117'
    # BOOTCAMP_PAGE
    d['slug'] = grab(r'slug:\s*"([^"]+)"')
    d['hub_url'] = grab(r'hubUrl:\s*"([^"]+)"', 'https://interstitiumlabs.dev/bootcamps/')
    d['bootcamp_title'] = grab(r'window\.BOOTCAMP_PAGE\s*=\s*\{[^}]*title:\s*"([^"]+)"')
    # hero
    d['hero_vendor'] = grab(r'<span id="heroVendor">(.*?)</span>')
    d['hero_title'] = grab(r'<h1 id="heroTitle">(.*?)</h1>')
    d['hero_tagline'] = grab(r'<p class="lede" id="heroTagline">(.*?)</p>')
    d['hero_disclaimer'] = grab(r'<p class="disclaimer" id="heroDisclaimer">(.*?)</p>')
    # hero video block (preserve if present)
    m = re.search(r'(<div class="bootcamp-hero-video".*?</div>\s*</div>)', html, re.S)
    # simpler: capture the whole hero-video div
    m2 = re.search(r'(<div class="bootcamp-hero-video"[^>]*>.*?</video>\s*</div>)', html, re.S)
    d['hero_video'] = m2.group(1) if m2 else ''
    # footer nav links
    m = re.search(r'<footer class="footer">.*?<nav[^>]*>(.*?)</nav>', html, re.S)
    d['footer_nav'] = m.group(1).strip() if m else '<a href="https://interstitiumlabs.dev/bootcamps/">← All bootcamps</a>'
    return d

def build(slug, vals):
    with open(TEMPLATE, encoding='utf-8') as f:
        t = f.read()
    # HTML-escape values for safe injection
    def esc(s):
        return s.replace('&', '&amp;') if s else ''
    # Note: values come from existing HTML so they're already escaped; inject raw
    reps = {
        '__META_DESCRIPTION__': vals['meta_description'],
        '__PAGE_TITLE__': vals['page_title'],
        '__OG_IMAGE__': vals['og_image'],
        '__ACCENT__': vals['accent'],
        '__ACCENT_SOFT__': vals['accent_soft'],
        '__ACCENT_INK__': vals['accent_ink'],
        '__SLUG__': vals['slug'] or slug,
        '__HUB_URL__': vals['hub_url'],
        '__BOOTCAMP_TITLE__': vals['bootcamp_title'],
        '__HERO_VIDEO__': vals['hero_video'],
        '__HERO_VENDOR__': vals['hero_vendor'],
        '__HERO_TITLE__': vals['hero_title'],
        '__HERO_TAGLINE__': vals['hero_tagline'],
        '__HERO_DISCLAIMER__': vals['hero_disclaimer'],
        '__FOOTER_NAV__': vals['footer_nav'],
    }
    for k, v in reps.items():
        t = t.replace(k, v or '')
    return t

def main():
    dry = '--dry-run' in sys.argv
    only = None
    for a in sys.argv:
        if a.startswith('--only='):
            only = set(a.split('=', 1)[1].split(','))
    slugs = sorted(d for d in os.listdir(BASE)
                  if os.path.isdir(os.path.join(BASE, d))
                  and d not in SKIP
                  and os.path.isfile(os.path.join(BASE, d, 'index.html'))
                  and os.path.isfile(os.path.join(BASE, d, 'content.json')))
    if only:
        slugs = [s for s in slugs if s in only]
    print(f"Migrating {len(slugs)} CBTs to _shell/")
    ok, fail = [], []
    for slug in slugs:
        idx = os.path.join(BASE, slug, 'index.html')
        try:
            vals = extract(idx)
            if not vals['slug']:
                vals['slug'] = slug
            new_html = build(slug, vals)
            # sanity: no unreplaced placeholders
            leftovers = re.findall(r'__[A-Z_]+__', new_html)
            if leftovers:
                fail.append((slug, f"unreplaced placeholders: {leftovers}"))
                continue
            if not dry:
                # backup original
                bak = idx + '.pre-shell-bak'
                if not os.path.exists(bak):
                    shutil.copy2(idx, bak)
                with open(idx, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                # per-CBT service worker with cache name
                with open(SW_TEMPLATE, encoding='utf-8') as f:
                    sw = f.read()
                sw = sw.replace('CBT_CACHE_NAME', f'cbt-{slug}-v1')
                with open(os.path.join(BASE, slug, 'sw.js'), 'w', encoding='utf-8') as f:
                    f.write(sw)
            ok.append(slug)
        except Exception as e:
            fail.append((slug, str(e)))
    print(f"\nOK: {len(ok)}")
    if fail:
        print(f"FAILED: {len(fail)}")
        for s, e in fail:
            print(f"  {s}: {e}")
    else:
        print("No failures.")

if __name__ == '__main__':
    main()
