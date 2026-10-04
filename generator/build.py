#!/usr/bin/env python3
"""Build the Interstitium Labs Certification Bootcamps static site.

Reads:
  catalog.json               — the 68-bootcamp catalog (slugs, titles, vendors,
                               domains, groups, maps_to)
  content/<slug>.json        — per-bootcamp training content (docs/content-schema.md)
  templates/{hub,bootcamp,chat}.html
  engine/*                   — shared JS/CSS (copied verbatim)

Writes the deployable tree under site/ (all paths nested under /bootcamps so
<host>/bootcamps/* routes map directly onto the asset tree — pure static
assets, no edge worker):
  site/bootcamps/index.html            — hub landing (static cards + hub.js filters)
  site/bootcamps/catalog-map.json      — machine-readable slug -> catalog node refs
  site/bootcamps/engine/*              — shared engine (style.css, bootcamp.js, chat.js, hub.js)
  site/bootcamps/<slug>/index.html     — thin shell (loads ../engine + ./content.json)
  site/bootcamps/<slug>/chat/index.html — thin shell for the chat companion
  site/bootcamps/<slug>/content.json   — copied content (when valid)

Usage:
  python3 generator/build.py [--clean]

Exit codes: 0 = ok (warnings allowed), 2 = one or more content files had hard
errors (their content.json was excluded; shells still generated).
"""
import datetime
import json
import os
import re
import shutil
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(BASE, "catalog.json")
CONTENT_DIR = os.path.join(BASE, "content")
TEMPLATE_DIR = os.path.join(BASE, "templates")
ENGINE_DIR = os.path.join(BASE, "engine")
SITE = os.path.join(BASE, "site")

GROUP_META = {
    "languages":  ("Programming Languages", "Syntax to systems: the languages exams are written in."),
    "comptia":    ("CompTIA", "Vendor-neutral fundamentals: A+, Network+, Security+, and beyond."),
    "aws":        ("Amazon Web Services", "Cloud Practitioner through Solutions Architect."),
    "microsoft":  ("Microsoft", "Azure, Microsoft 365, and role-based certifications."),
    "oracle":     ("Oracle", "Java and database certification paths."),
    "data":       ("Data & Analytics", "Databases, analytics, and data engineering."),
    "web":        ("Web Development", "Front-end to full-stack web paths."),
    "cloudnative":("Cloud-Native & DevOps", "Kubernetes, containers, and platform engineering."),
    "security":   ("Security", "Offensive, defensive, and governance security paths."),
    "linux":      ("Linux", "Linux Foundation and LPIC paths."),
    "gov":        ("Government & Compliance", "Public-sector and compliance frameworks."),
    "special":    ("Specialty Paths", "Niche and emerging certification tracks."),
}

WORKER_JS = """/* Cert-Bootcamps edge router (main_module).
   Routes: <host>/bootcamps/* -> this worker. Static assets live at the site
   root, so strip the /bootcamps prefix and delegate to the asset manifest. */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/bootcamps" || url.pathname.startsWith("/bootcamps/")) {
      const rest = url.pathname.slice("/bootcamps".length) || "/";
      url.pathname = rest;
      return env.ASSETS.fetch(new Request(url.toString(), request));
    }
    return env.ASSETS.fetch(request);
  }
};
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def accent_style(accent):
    """Build the :root accent override block, or '' when no accent given."""
    if not accent or not re.fullmatch(r"#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?", str(accent).strip()):
        return ""
    a = "#" + str(accent).strip().lstrip("#")
    r, g, b = hex_to_rgb(a)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    ink = "#052e1e" if lum > 0.45 else "#ffffff"
    return ("<style>:root{--accent:%s;--accent-soft:rgba(%d,%d,%d,.10);"
            "--accent-ink:%s;}</style>" % (a, r, g, b, ink))


# ---------------------------------------------------------------- validation
REQUIRED_SCEN = ["id", "title", "situation", "prompt", "choices", "answer",
                 "why", "objectives", "mins"]


def validate_content(slug, data, catalog_entry):
    """Return (errors, warnings, stats). Errors exclude the content file."""
    errors, warnings = [], []
    stats = {"scenarios": 0, "domains": 0, "behavioral": 0, "topics": 0}

    for key in ["slug", "title", "tagline", "vendor", "domains", "behavioral", "chat"]:
        if key not in data:
            errors.append("missing top-level key '%s'" % key)
    if errors:
        return errors, warnings, stats
    if data["slug"] != slug:
        errors.append("slug mismatch: file=%s content=%s" % (slug, data["slug"]))
    if not isinstance(data.get("vendor"), dict) or not data["vendor"].get("name"):
        errors.append("vendor must be an object with a name")

    catalog_domains = set(catalog_entry.get("domains", []))
    seen_ids = set()
    n_scen = 0
    for di, d in enumerate(data["domains"]):
        for key in ["id", "name", "scenarios"]:
            if key not in d:
                errors.append("domain[%d] missing '%s'" % (di, key))
        if d.get("name") not in catalog_domains:
            warnings.append("domain name '%s' not in catalog.json domains" % d.get("name"))
        n = len(d.get("scenarios", []))
        if n < 6 or n > 8:
            warnings.append("domain '%s' has %d scenarios (target 6-8)" % (d.get("name"), n))
        for si, s in enumerate(d.get("scenarios", [])):
            where = "domain '%s' scenario[%d]" % (d.get("name"), si)
            for key in REQUIRED_SCEN:
                if key not in s:
                    errors.append("%s missing '%s'" % (where, key))
            sid = "%s:%s" % (d.get("id"), s.get("id"))
            if sid in seen_ids:
                errors.append("duplicate scenario id '%s'" % sid)
            seen_ids.add(sid)
            ch = s.get("choices")
            if not isinstance(ch, list) or len(ch) != 4:
                errors.append("%s: choices must be exactly 4" % where)
            ans = s.get("answer")
            if not isinstance(ans, int) or not (0 <= ans <= 3):
                errors.append("%s: answer must be an int 0-3" % where)
            if "hint" not in s:
                warnings.append("%s has no hint" % where)
            n_scen += 1
    stats["scenarios"] = n_scen
    stats["domains"] = len(data["domains"])

    beh = data["behavioral"]
    stats["behavioral"] = len(beh) if isinstance(beh, list) else 0
    if stats["behavioral"] != 8:
        warnings.append("behavioral has %d prompts (target 8)" % stats["behavioral"])
    for bi, b in enumerate(beh if isinstance(beh, list) else []):
        for key in ["prompt", "framework", "points", "pitfalls"]:
            if key not in b:
                warnings.append("behavioral[%d] missing '%s'" % (bi, key))

    chat = data["chat"]
    topics = chat.get("topics", []) if isinstance(chat, dict) else []
    stats["topics"] = len(topics)
    domain_ids = {d.get("id") for d in data["domains"]}
    for t in topics:
        if t.get("id") not in domain_ids:
            warnings.append("chat topic '%s' has no matching domain id" % t.get("id"))
        kp = t.get("key_points", [])
        if not (4 <= len(kp) <= 6):
            warnings.append("chat topic '%s' has %d key_points (target 4-6)"
                            % (t.get("id"), len(kp)))
    if not chat.get("persona"):
        warnings.append("chat.persona missing; engine will use a generic fallback")
    return errors, warnings, stats


# ---------------------------------------------------------------- rendering
def render_bootcamp(entry, tpl, content, stats, prev_entry, next_entry, build_date):
    slug = entry["slug"]
    vendor = entry["vendor"]
    vendor_line = vendor["name"] + (" · " + vendor["certs"] if vendor.get("certs") else "")
    sim = (content or {}).get("simulation", {}) if content else {}
    sim_minutes = sim.get("minutes", 180)
    disclaimer = (content.get("disclaimer") if content
                  else "Independent practice material by Interstitium Labs. "
                         "Not affiliated with, endorsed by, or sponsored by %s. "
                         "Confers no certificate." % vendor["name"])

    def nav_link(e, arrow):
        if not e:
            return ""
        return ('<a href="../%s/">%s %s</a>'
                % (e["slug"], arrow, esc(e["title"])))

    html = tpl
    subs = {
        "{{SLUG}}": esc(slug),
        "{{TITLE}}": esc(entry["title"]),
        "{{TAGLINE}}": esc(entry["tagline"]),
        "{{VENDOR_LINE}}": esc(vendor_line),
        "{{DISCLAIMER}}": esc(disclaimer),
        "{{SCENARIO_COUNT}}": str(stats["scenarios"]) if content else "—",
        "{{DOMAIN_COUNT}}": str(len(entry["domains"])),
        "{{SIM_MINUTES}}": str(sim_minutes),
        "{{ACCENT_STYLE}}": accent_style((content or {}).get("accent")),
        "{{HUB_URL}}": "../index.html",
        "{{CHAT_URL}}": "./chat/",
        "{{BOOTCAMP_URL}}": "./",
        "{{PREV_LINK}}": nav_link(prev_entry, "←"),
        "{{NEXT_LINK}}": nav_link(next_entry, "→"),
        "{{BUILD_DATE}}": build_date,
    }
    for k, v in subs.items():
        html = html.replace(k, v)
    return html


def render_chat(entry, tpl, content, build_date):
    html = tpl
    subs = {
        "{{SLUG}}": esc(entry["slug"]),
        "{{TITLE}}": esc(entry["title"]),
        "{{ACCENT_STYLE}}": accent_style((content or {}).get("accent")),
        "{{HUB_URL}}": "../../index.html",
        "{{BOOTCAMP_URL}}": "../index.html",
        "{{BUILD_DATE}}": build_date,
    }
    for k, v in subs.items():
        html = html.replace(k, v)
    return html


def hub_card(entry, stats, has_content):
    slug = entry["slug"]
    vendor = entry["vendor"]
    vendor_line = vendor["name"] + (" · " + vendor["certs"] if vendor.get("certs") else "")
    search = " ".join([entry["title"], entry["tagline"], vendor["name"],
                       vendor.get("certs", ""), " ".join(entry["domains"])]).lower()
    count_tag = ('<span class="tag accent">%d scenarios</span>' % stats["scenarios"]
                 if has_content else '<span class="badge-soon">IN BUILD</span>')
    return (
        '<a class="hub-card" href="%s/" data-group="%s" data-vendor="%s" data-search="%s">'
        '<p class="vendor">%s</p><h3>%s</h3><p>%s</p>'
        '<div class="hub-meta">%s<span class="tag">%d domains</span>'
        '<span class="go">Open →</span></div></a>'
    ) % (esc(slug), esc(entry["group"]), esc(vendor["name"]), esc(search),
         esc(vendor_line), esc(entry["title"]), esc(entry["tagline"]),
         count_tag, len(entry["domains"]))


def render_hub(entries, contents, stats_map, tpl, build_date, version):
    groups_in_order = []
    for e in entries:
        if e["group"] not in groups_in_order:
            groups_in_order.append(e["group"])

    sections = []
    for g in groups_in_order:
        gname, gdesc = GROUP_META.get(g, (g.title(), ""))
        cards = "".join(
            hub_card(e, stats_map[e["slug"]], contents[e["slug"]] is not None)
            for e in entries if e["group"] == g)
        sections.append(
            '<section class="group-section" data-group-section="%s">'
            '<h2>%s</h2><p>%s</p><div class="hub-grid">%s</div></section>'
            % (esc(g), esc(gname), esc(gdesc), cards))

    group_opts = ('<option value="">All tracks</option>' + "".join(
        '<option value="%s">%s</option>' % (esc(g), esc(GROUP_META.get(g, (g.title(), ""))[0]))
        for g in groups_in_order))
    vendors = sorted({e["vendor"]["name"] for e in entries})
    vendor_opts = ('<option value="">All vendors</option>' + "".join(
        '<option value="%s">%s</option>' % (esc(v), esc(v)) for v in vendors))

    map_nodes = []
    for e in entries:
        links = ", ".join(
            '<a href="https://%s/%s">%s/%s</a>'
            % (esc(m["site"]), esc(m["node"]), esc(m["site"]), esc(m["node"]))
            for m in e.get("maps_to", []))
        map_nodes.append(
            '<div class="map-node"><code>%s</code> — %s<br />'
            '<span class="map-links">Maps to: %s</span></div>'
            % (esc(e["slug"]), esc(e["title"]), links or "—"))

    total_scen = sum(s["scenarios"] for s in stats_map.values())
    html = tpl
    for k, v in {
        "{{VERSION}}": esc(version),
        "{{BOOTCAMP_COUNT}}": str(len(entries)),
        "{{SCENARIO_TOTAL}}": str(total_scen),
        "{{GROUP_COUNT}}": str(len(groups_in_order)),
        "{{VENDOR_COUNT}}": str(len(vendors)),
        "{{GROUP_OPTIONS}}": group_opts,
        "{{VENDOR_OPTIONS}}": vendor_opts,
        "{{GROUP_SECTIONS}}": "\n".join(sections),
        "{{MAP_SECTION}}": "\n".join(map_nodes),
        "{{BUILD_DATE}}": build_date,
    }.items():
        html = html.replace(k, v)
    return html


# ---------------------------------------------------------------- main
def main():
    clean = "--clean" in sys.argv
    if clean and os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE, exist_ok=True)

    catalog = json.load(open(CATALOG, encoding="utf-8"))
    entries = catalog["bootcamps"]
    deploy_base = catalog.get("deploy_base", "/bootcamps")
    version = catalog.get("version", "1.0.0")
    build_date = datetime.date.today().isoformat()

    tpl_bootcamp = open(os.path.join(TEMPLATE_DIR, "bootcamp.html"), encoding="utf-8").read()
    tpl_chat = open(os.path.join(TEMPLATE_DIR, "chat.html"), encoding="utf-8").read()
    tpl_hub = open(os.path.join(TEMPLATE_DIR, "hub.html"), encoding="utf-8").read()

    # Load + validate content
    contents, stats_map = {}, {}
    hard_errors, warnings = [], []
    for e in entries:
        slug = e["slug"]
        path = os.path.join(CONTENT_DIR, slug + ".json")
        if not os.path.isfile(path):
            contents[slug] = None
            stats_map[slug] = {"scenarios": 0, "domains": len(e["domains"]),
                               "behavioral": 0, "topics": 0}
            continue
        try:
            data = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError as ex:
            hard_errors.append("%s: invalid JSON (%s)" % (slug, ex))
            contents[slug] = None
            stats_map[slug] = {"scenarios": 0, "domains": len(e["domains"]),
                               "behavioral": 0, "topics": 0}
            continue
        errs, warns, stats = validate_content(slug, data, e)
        stats_map[slug] = stats
        if errs:
            hard_errors.append("%s: %s" % (slug, "; ".join(errs)))
            contents[slug] = None  # excluded; shell shows "content on the way"
        else:
            contents[slug] = data
        for w in warns:
            warnings.append("%s: %s" % (slug, w))

    # Engine (copied verbatim) — lives under /bootcamps/engine/ so all
    # route-relative references resolve on every domain.
    eng_out = os.path.join(SITE, "bootcamps", "engine")
    os.makedirs(eng_out, exist_ok=True)
    for f in ["style.css", "bootcamp.js", "terminal.js", "learn.js", "labs.js",
              "simulations.js", "consoles.js", "missions.js",
              "chat.js", "hub.js"]:
        src = os.path.join(ENGINE_DIR, f)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(eng_out, f))
        else:
            warnings.append("engine/%s not present — skipped (workstream pending)" % f)
    # Optional shared assets (present once workstreams land; skipped if absent).
    for f in ["math.json"]:
        src = os.path.join(ENGINE_DIR, f)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(eng_out, f))
    # Shared foundation tracks ship as an engine-level asset (source of truth:
    # generator/foundation-tracks.json).
    ft_src = os.path.join(BASE, "generator", "foundation-tracks.json")
    if os.path.isfile(ft_src):
        shutil.copy2(ft_src, os.path.join(eng_out, "foundations.json"))
        shutil.copy2(os.path.join(ENGINE_DIR, f), os.path.join(eng_out, f))
    # NOTE: pure static-assets deploy — no edge worker. The asset tree already
    # carries the /bootcamps prefix, so <host>/bootcamps/* routes map directly.

    # Bootcamp pages
    for i, e in enumerate(entries):
        slug = e["slug"]
        content = contents[slug]
        prev_e = entries[i - 1] if i > 0 else None
        next_e = entries[i + 1] if i < len(entries) - 1 else None
        bdir = os.path.join(SITE, "bootcamps", slug)
        cdir = os.path.join(bdir, "chat")
        os.makedirs(cdir, exist_ok=True)
        with open(os.path.join(bdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_bootcamp(e, tpl_bootcamp, content, stats_map[slug],
                                    prev_e, next_e, build_date))
        with open(os.path.join(cdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_chat(e, tpl_chat, content, build_date))
        if content is not None:
            with open(os.path.join(bdir, "content.json"), "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False)
            # Enterprise CBT media assets (Worker 2 diagrams): content/<slug>/assets/
            # -> site/bootcamps/<slug>/assets/ when the source dir exists.
            assets_src = os.path.join(CONTENT_DIR, slug, "assets")
            if os.path.isdir(assets_src):
                shutil.copytree(assets_src, os.path.join(bdir, "assets"),
                                dirs_exist_ok=True)

    # Hub + catalog map (both live under /bootcamps/ to match the routes)
    with open(os.path.join(SITE, "bootcamps", "index.html"), "w", encoding="utf-8") as f:
        f.write(render_hub(entries, contents, stats_map, tpl_hub, build_date, version))

    catalog_map = {
        "generated": build_date,
        "platform": catalog.get("platform", ""),
        "version": version,
        "deploy_base": deploy_base,
        "bootcamps": {
            e["slug"]: {
                "title": e["title"],
                "tagline": e["tagline"],
                "vendor": e["vendor"],
                "group": e["group"],
                "url": "%s/%s/" % (deploy_base, e["slug"]),
                "chat_url": "%s/%s/chat/" % (deploy_base, e["slug"]),
                "content_ready": contents[e["slug"]] is not None,
                "scenario_count": stats_map[e["slug"]]["scenarios"],
                "maps_to": e.get("maps_to", []),
            } for e in entries
        },
    }
    with open(os.path.join(SITE, "bootcamps", "catalog-map.json"), "w", encoding="utf-8") as f:
        json.dump(catalog_map, f, ensure_ascii=False, indent=1)

    # Report
    ready = sum(1 for e in entries if contents[e["slug"]] is not None)
    total_scen = sum(s["scenarios"] for s in stats_map.values())
    print("bootcamps: %d | content ready: %d | scenarios: %d"
          % (len(entries), ready, total_scen))
    for w in warnings:
        print("WARN  %s" % w)
    for er in hard_errors:
        print("ERROR %s" % er)
    print("site written to %s" % SITE)
    return 2 if hard_errors else 0


if __name__ == "__main__":
    sys.exit(main())
