# -*- coding: utf-8 -*-
"""Original SVG diagram builders for the Enterprise CBT media worker (Worker 2).

All diagrams are generated programmatically, dark-theme, and original content.
No vendor diagrams are copied; labels use only well-established technical facts
(port numbers, protocol names, layer orders, real command names).

Each builder returns a complete SVG document string (viewBox 0 0 800 450).
"""

BG = '#0a0e14'
SUR = '#101722'
SUR2 = '#16202f'
INK = '#e9f1f4'
MUT = '#93a4b8'
LINE = '#223046'
ACC = '#3ddc97'
SIG = '#fbbf24'
DAN = '#f87171'
CODE = '#b9f5d8'
PURP = '#a78bfa'

SANS = "font-family='-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif'"
MONO = "font-family='ui-monospace,SF Mono,Menlo,Consolas,monospace'"


def esc(s):
    s = '' if s is None else str(s)
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def wrap(text, maxc):
    """Greedy word wrap -> list of lines."""
    words = str(text or '').split()
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= maxc:
            cur = (cur + ' ' + w).strip()
        else:
            if cur:
                lines.append(cur)
            if len(w) > maxc:  # hard-break very long tokens (commands, URLs)
                while len(w) > maxc:
                    lines.append(w[:maxc])
                    w = w[maxc:]
            cur = w
    if cur:
        lines.append(cur)
    return lines or ['']


def _defs():
    return ('<defs>'
            '<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>'
            '<marker id="ahm" viewBox="0 0 10 10" refX="8" refY="5" '
            'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>'
            '</defs>' % (ACC, MUT))


def doc(title, desc, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img">'
            '<title>%s</title><desc>%s</desc>'
            '<rect width="800" height="450" fill="%s" rx="12"/>'
            '%s</svg>' % (esc(title), esc(desc), BG, body))


def _header(title, caption):
    parts = []
    parts.append('<text x="36" y="44" %s font-size="23" font-weight="700" fill="%s">%s</text>'
                 % (SANS, INK, esc(title)))
    y = 68
    if caption:
        for ln in wrap(caption, 96)[:2]:
            parts.append('<text x="36" y="%d" %s font-size="13" fill="%s">%s</text>'
                         % (y, SANS, MUT, esc(ln)))
            y += 17
    parts.append('<rect x="36" y="%d" width="728" height="2" fill="%s" opacity="0.6"/>'
                 % (y + 2, LINE))
    return ''.join(parts), y + 22  # content top


def _badge(x, y, r, text, fill, fg=BG, size=13):
    return ('<circle cx="%d" cy="%d" r="%d" fill="%s"/>'
            '<text x="%d" y="%d" %s font-size="%d" font-weight="700" fill="%s" '
            'text-anchor="middle">%s</text>'
            % (x, y, r, fill, x, y + size // 2 - 1, SANS, size, fg, esc(text)))


# ---------------------------------------------------------------- keypoints
def keypoints(title, caption, items, desc=None):
    """Grid of concept cards. items: [(head, detail), ...], up to 6."""
    items = list(items)[:6]
    n = len(items)
    cols = 1 if n <= 2 else 2
    rows = (n + cols - 1) // cols
    cw = 728 if cols == 1 else 356
    ch = 118 if rows <= 2 else 108
    head, top = _header(title, caption)
    parts = [head]
    for i, (h, d) in enumerate(items):
        c, r = i % cols, i // cols
        x = 36 + c * (cw + 16)
        y = top + r * (ch + 12)
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="1"/>' % (x, y, cw, ch, SUR, LINE))
        parts.append('<rect x="%d" y="%d" width="4" height="%d" rx="2" fill="%s"/>'
                     % (x, y + 12, ch - 24, ACC))
        parts.append(_badge(x + 30, y + 26, 13, str(i + 1), ACC))
        ty = y + 30
        for ln in wrap(h, 34 if cols == 1 else 30)[:1]:
            parts.append('<text x="%d" y="%d" %s font-size="15" font-weight="700" fill="%s">%s</text>'
                         % (x + 50, ty, SANS, INK, esc(ln)))
            ty += 20
        for ln in wrap(d, 72 if cols == 1 else 44)[:3]:
            parts.append('<text x="%d" y="%d" %s font-size="12.5" fill="%s">%s</text>'
                         % (x + 50, ty, SANS, MUT, esc(ln)))
            ty += 16
    d = desc or ('Key ideas: ' + '; '.join(h for h, _ in items))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- layers
def layers(title, caption, layers, desc=None, top_label='top'):
    """Vertical numbered stack. layers: [(label, sub), ...] top -> bottom, up to 8."""
    layers = list(layers)[:8]
    n = len(layers)
    head, top = _header(title, caption)
    parts = [head, _defs()]
    avail = 430 - top
    lh = min(52, (avail - (n - 1) * 8) / n)
    w = 600
    x = (800 - w) / 2
    for i, (label, sub) in enumerate(layers):
        y = top + i * (lh + 8)
        parts.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="9" fill="%s" '
                     'stroke="%s" stroke-width="1"/>' % (x, y, w, lh, SUR, LINE))
        shade = 0.16 + 0.10 * (i / max(n - 1, 1))
        parts.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="9" fill="%s" opacity="%.2f"/>'
                     % (x, y, w, lh, ACC, shade * 0.35))
        parts.append(_badge(int(x) + 30, y + lh / 2, 14, str(n - i), ACC))
        label_lines = wrap(label, 40)
        sub_lines = wrap(sub, 46)
        if lh >= 48 and sub_lines:
            parts.append('<text x="%d" y="%.1f" %s font-size="15" font-weight="700" fill="%s">%s</text>'
                         % (int(x) + 54, y + lh / 2 - 4, SANS, INK, esc(label_lines[0])))
            parts.append('<text x="%d" y="%.1f" %s font-size="12" fill="%s">%s</text>'
                         % (int(x) + 54, y + lh / 2 + 14, SANS, MUT, esc(sub_lines[0])))
        else:
            parts.append('<text x="%d" y="%.1f" %s font-size="14" font-weight="700" fill="%s">%s</text>'
                         % (int(x) + 54, y + lh / 2 + 5, SANS, INK, esc(label_lines[0])))
        if i < n - 1:
            parts.append('<line x1="400" y1="%.1f" x2="400" y2="%.1f" stroke="%s" '
                         'stroke-width="2" marker-end="url(#ahm)"/>' % (y + lh, y + lh + 8, MUT))
    d = desc or ('Stacked layers, top to bottom: ' + ' > '.join(l for l, _ in layers))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- flow
def flow(title, caption, steps, desc=None, note=None):
    """Horizontal numbered boxes with arrows. steps: [(label, sub), ...], up to 6."""
    steps = list(steps)[:6]
    n = len(steps)
    head, top = _header(title, caption)
    parts = [head, _defs()]
    gap, aw = 14, 26
    bw = (728 - (n - 1) * (gap + aw)) / n
    bh = 190
    y = top + 30
    for i, (label, sub) in enumerate(steps):
        x = 36 + i * (bw + gap + aw)
        fill = SUR2 if i in (0, n - 1) else SUR
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="1.5"/>' % (x, y, bw, bh, fill, ACC if i == n - 1 else LINE))
        parts.append(_badge(int(x + bw / 2), int(y) - 2, 14, str(i + 1), ACC if i < n - 1 else SIG))
        ty = y + 40
        for ln in wrap(label, int(bw / 8.2))[:2]:
            parts.append('<text x="%.1f" y="%.1f" %s font-size="14.5" font-weight="700" '
                         'fill="%s" text-anchor="middle">%s</text>'
                         % (x + bw / 2, ty, SANS, INK, esc(ln)))
            ty += 19
        ty += 4
        for ln in wrap(sub, int(bw / 7.0))[:5]:
            parts.append('<text x="%.1f" y="%.1f" %s font-size="11.5" fill="%s" '
                         'text-anchor="middle">%s</text>'
                         % (x + bw / 2, ty, SANS, MUT, esc(ln)))
            ty += 15
        if i < n - 1:
            x2 = x + bw + gap
            parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                         'stroke-width="2.5" marker-end="url(#ah)"/>'
                         % (x2, y + bh / 2, x2 + aw, y + bh / 2, ACC))
    if note:
        parts.append('<text x="400" y="%d" %s font-size="12.5" fill="%s" text-anchor="middle">%s</text>'
                     % (y + bh + 34, SANS, SIG, esc(note)))
    d = desc or ('Sequence: ' + ' -> '.join(l for l, _ in steps))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- tiers
def tiers(title, caption, tiers, desc=None):
    """Horizontal bands (e.g. 3-tier architecture). tiers: [(tier_label, [boxes]), ...]."""
    tiers = list(tiers)[:4]
    head, top = _header(title, caption)
    parts = [head, _defs()]
    avail = 428 - top
    th = (avail - (len(tiers) - 1) * 22) / len(tiers)
    for i, (tlabel, boxes) in enumerate(tiers):
        y = top + i * (th + 22)
        parts.append('<rect x="36" y="%.1f" width="728" height="%.1f" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="1"/>' % (y, th, SUR, LINE))
        parts.append('<text x="52" y="%.1f" %s font-size="13.5" font-weight="700" fill="%s">%s</text>'
                     % (y + th / 2 - 4, SANS, ACC, esc(tlabel)))
        parts.append('<text x="52" y="%.1f" %s font-size="11" fill="%s">tier %d</text>'
                     % (y + th / 2 + 14, SANS, MUT, i + 1))
        n = len(boxes)
        bw = min(200, (560 - (n - 1) * 12) / n)
        bx0 = 200 + (560 - (bw * n + 12 * (n - 1))) / 2
        bh = min(th - 24, 56)
        for j, b in enumerate(boxes):
            bx = bx0 + j * (bw + 12)
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" '
                         'fill="%s" stroke="%s" stroke-width="1.2"/>'
                         % (bx, y + (th - bh) / 2, bw, bh, SUR2, LINE))
            for k, ln in enumerate(wrap(b, int(bw / 7.6))[:2]):
                parts.append('<text x="%.1f" y="%.1f" %s font-size="13" font-weight="600" '
                             'fill="%s" text-anchor="middle">%s</text>'
                             % (bx + bw / 2, y + th / 2 - 4 + k * 16, SANS, INK, esc(ln)))
        if i < len(tiers) - 1:
            parts.append('<line x1="400" y1="%.1f" x2="400" y2="%.1f" stroke="%s" '
                         'stroke-width="2" marker-end="url(#ahm)"/>' % (y + th, y + th + 22, MUT))
    d = desc or ('Tiered architecture: ' + ' / '.join(t for t, _ in tiers))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- topology
def topology(title, caption, center, spokes, desc=None):
    """Center node with spokes. spokes: [label, ...], up to 8."""
    spokes = list(spokes)[:8]
    head, top = _header(title, caption)
    parts = [head]
    cx, cy, cw, chh = 400, (top + 430) / 2, 190, 74
    import math
    n = len(spokes)
    rx, ry = 250, 105
    for i, sp in enumerate(spokes):
        a = -math.pi / 2 + 2 * math.pi * i / n
        sx, sy = cx + rx * math.cos(a), cy + ry * math.sin(a)
        parts.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="1.5" opacity="0.7"/>' % (cx, cy, sx, sy, LINE))
        bw2, bh2 = 150, 46
        parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="8" fill="%s" '
                     'stroke="%s" stroke-width="1.2"/>' % (sx - bw2 / 2, sy - bh2 / 2, bw2, bh2, SUR, LINE))
        for k, ln in enumerate(wrap(sp, 20)[:2]):
            parts.append('<text x="%.1f" y="%.1f" %s font-size="12.5" font-weight="600" '
                         'fill="%s" text-anchor="middle">%s</text>'
                         % (sx, sy - 2 + k * 15, SANS, INK, esc(ln)))
    parts.append('<rect x="%d" y="%.1f" width="%d" height="%d" rx="10" fill="%s" '
                 'stroke="%s" stroke-width="2"/>' % (cx - cw / 2, cy - chh / 2, cw, chh, SUR2, ACC))
    for k, ln in enumerate(wrap(center, 24)[:2]):
        parts.append('<text x="%d" y="%.1f" %s font-size="15" font-weight="700" fill="%s" '
                     'text-anchor="middle">%s</text>' % (cx, cy - 2 + k * 18, SANS, INK, esc(ln)))
    d = desc or ('%s connected to: %s' % (center, ', '.join(spokes)))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- table
def table_svg(title, caption, headers, rows, desc=None):
    """Comparison table. headers: [..], rows: [[..], ...], up to 7 rows x 4 cols."""
    headers = list(headers)[:4]
    rows = [list(r)[:4] for r in rows][:7]
    ncol = len(headers)
    head, top = _header(title, caption)
    parts = [head]
    cw = 728 / ncol
    rh = 40
    hh = 44
    y = top + 6
    for j, htxt in enumerate(headers):
        x = 36 + j * cw
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="6" fill="%s"/>'
                     % (x, y, cw - 6, hh, SUR2))
        parts.append('<text x="%.1f" y="%.1f" %s font-size="14" font-weight="700" fill="%s">%s</text>'
                     % (x + 12, y + 28, SANS, ACC, esc(htxt)))
    y += hh + 6
    for i, row in enumerate(rows):
        for j in range(ncol):
            x = 36 + j * cw
            cell = row[j] if j < len(row) else ''
            bg = SUR if i % 2 == 0 else BG
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="6" fill="%s" '
                         'stroke="%s" stroke-width="0.7"/>' % (x, y, cw - 6, rh, bg, LINE))
            lines = wrap(cell, int(cw / 7.6))[:2]
            ty = y + (20 if len(lines) == 1 else 15)
            for ln in lines:
                parts.append('<text x="%.1f" y="%.1f" %s font-size="12.5" fill="%s">%s</text>'
                             % (x + 12, ty, SANS, INK if j == 0 else MUT, esc(ln)))
                ty += 15
        y += rh + 5
    d = desc or ('Table comparing %s across %s' % (headers[0], ', '.join(headers[1:])))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- commands
def commands(title, caption, cmds, desc=None, note=None):
    """Monospace command cards. cmds: [(cmd, desc), ...], up to 10."""
    cmds = list(cmds)[:10]
    head, top = _header(title, caption)
    parts = [head]
    cols = 2
    cw = 356
    rows = (len(cmds) + 1) // 2
    ch = min(66, (424 - top - (rows - 1) * 10) / rows)
    for i, (cmd, cdesc) in enumerate(cmds):
        c, r = i % cols, i // cols
        x = 36 + c * (cw + 16)
        y = top + r * (ch + 10)
        parts.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" rx="8" fill="%s" '
                     'stroke="%s" stroke-width="1"/>' % (x, y, cw, ch, '#060b11', LINE))
        cl = wrap(cmd, 40)[0]
        parts.append('<text x="%d" y="%.1f" %s font-size="13.5" font-weight="700" fill="%s">%s</text>'
                     % (x + 14, y + 24, MONO, CODE, esc(cl)))
        dl = wrap(cdesc, 46)[:1]
        if dl and ch > 44:
            parts.append('<text x="%d" y="%.1f" %s font-size="11.5" fill="%s">%s</text>'
                         % (x + 14, y + 44, SANS, MUT, esc(dl[0])))
    if note:
        parts.append('<text x="36" y="430" %s font-size="12" fill="%s">%s</text>'
                     % (SANS, SIG, esc(note)))
    d = desc or ('Command reference: ' + ', '.join(c for c, _ in cmds[:6]))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- git branch
def git_branch(title, caption, main='main', feature='feature/login', desc=None):
    """Simplified git branching diagram: main line, feature branch off and merge back."""
    head, top = _header(title, caption)
    parts = [head, _defs()]
    cy_main, cy_feat = top + 150, top + 60
    x0, x1 = 80, 720
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>'
                 % (x0, cy_main, x1, cy_main, ACC))
    parts.append('<text x="%d" y="%d" %s font-size="13" font-weight="700" fill="%s">%s</text>'
                 % (x0, cy_main + 34, MONO, ACC, esc(main)))
    for i, x in enumerate([140, 260, 380, 500, 640]):
        parts.append('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>'
                     % (x, cy_main, BG, ACC))
    bx0, bx1 = 200, 560
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>'
                 % (bx0, cy_feat, bx1, cy_feat, PURP))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" '
                 'marker-end="url(#ah)"/>' % (bx0, cy_feat, bx0, cy_main - 12, PURP))
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" '
                 'stroke-dasharray="7,5" marker-end="url(#ah)"/>' % (bx1, cy_feat, bx1, cy_main - 12, SIG))
    for x in [290, 410, 530]:
        parts.append('<circle cx="%d" cy="%d" r="9" fill="%s" stroke="%s" stroke-width="2"/>'
                     % (x, cy_feat, BG, PURP))
    parts.append('<text x="%d" y="%d" %s font-size="13" font-weight="700" fill="%s">%s</text>'
                 % (bx0, cy_feat - 24, MONO, PURP, esc(feature)))
    parts.append('<text x="%d" y="%d" %s font-size="12" fill="%s">git checkout -b %s</text>'
                 % (bx0 - 150, cy_feat + 6, MONO, MUT, esc(feature)))
    parts.append('<text x="%d" y="%d" %s font-size="12" fill="%s">git merge %s</text>'
                 % (bx1 + 16, cy_feat + 6, MONO, MUT, esc(feature)))
    parts.append('<text x="36" y="%d" %s font-size="12.5" fill="%s">Each circle is a commit. '
                 'Feature work stays isolated until the merge commit joins it back to %s.</text>'
                 % (cy_main + 62, SANS, MUT, esc(main)))
    d = desc or ('Git branching: %s branches from %s and merges back' % (feature, main))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- quadrants
def quadrants(title, caption, quads, desc=None):
    """2x2 grid. quads: [(label, [items]), ...] exactly 4."""
    quads = list(quads)[:4]
    head, top = _header(title, caption)
    parts = [head]
    qw, qh = 356, 148
    colors = [ACC, SIG, PURP, CODE]
    for i, (label, items) in enumerate(quads):
        c, r = i % 2, i // 2
        x = 36 + c * (qw + 16)
        y = top + r * (qh + 12)
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="1"/>' % (x, y, qw, qh, SUR, LINE))
        parts.append('<rect x="%d" y="%d" width="%d" height="30" rx="10" fill="%s" opacity="0.16"/>'
                     % (x, y, qw, colors[i]))
        parts.append('<text x="%d" y="%d" %s font-size="14.5" font-weight="700" fill="%s">%s</text>'
                     % (x + 16, y + 21, SANS, colors[i], esc(label)))
        ty = y + 52
        for it in items[:4]:
            parts.append('<circle cx="%d" cy="%d" r="3.5" fill="%s"/>' % (x + 20, ty - 4, colors[i]))
            for ln in wrap(it, 40)[:1]:
                parts.append('<text x="%d" y="%d" %s font-size="12.5" fill="%s">%s</text>'
                             % (x + 32, ty, SANS, MUT, esc(ln)))
                ty += 19
    d = desc or ('Four quadrants: ' + ', '.join(l for l, _ in quads))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- schema
def schema(title, caption, tables, desc=None, note=None):
    """DB schema: tables with columns and PK/FK badges. tables: [(name, [(col, key)]), ...]."""
    tables = list(tables)[:4]
    head, top = _header(title, caption)
    parts = [head]
    n = len(tables)
    tw = min(230, (728 - (n - 1) * 18) / n)
    x0 = 36 + (728 - (tw * n + 18 * (n - 1))) / 2
    for i, (tname, cols) in enumerate(tables):
        x = x0 + i * (tw + 18)
        y = top + 8
        rh = 30
        hh = 40
        parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="8" fill="%s" '
                     'stroke="%s" stroke-width="1.4"/>'
                     % (x, y, tw, hh, SUR2, ACC))
        parts.append('<text x="%.1f" y="%.1f" %s font-size="14" font-weight="700" fill="%s" '
                     'text-anchor="middle">%s</text>' % (x + tw / 2, y + 26, MONO, INK, esc(tname)))
        y += hh
        for col, key in cols[:8]:
            parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" fill="%s" '
                         'stroke="%s" stroke-width="0.7"/>' % (x, y, tw, rh, SUR, LINE))
            badge = ''
            if key == 'PK':
                badge = '<rect x="%.1f" y="%.1f" width="30" height="18" rx="4" fill="%s"/>' % (x + 8, y + 6, SIG)
                badge += '<text x="%.1f" y="%.1f" %s font-size="10.5" font-weight="700" fill="%s">PK</text>' % (x + 23, y + 19, SANS, BG)
            elif key == 'FK':
                badge = '<rect x="%.1f" y="%.1f" width="30" height="18" rx="4" fill="%s"/>' % (x + 8, y + 6, ACC)
                badge += '<text x="%.1f" y="%.1f" %s font-size="10.5" font-weight="700" fill="%s">FK</text>' % (x + 23, y + 19, SANS, BG)
            parts.append(badge)
            for ln in wrap(col, int(tw / 8.4))[:1]:
                parts.append('<text x="%.1f" y="%.1f" %s font-size="12.5" fill="%s">%s</text>'
                             % (x + 46, y + 20, MONO, MUT, esc(ln)))
            y += rh
        if i < n - 1:
            parts.append('<text x="%.1f" y="%.1f" %s font-size="20" fill="%s" text-anchor="middle">\u27f6</text>'
                         % (x + tw + 9, top + 60, SANS, MUT))
    if note:
        parts.append('<text x="36" y="430" %s font-size="12" fill="%s">%s</text>'
                     % (SANS, SIG, esc(note)))
    d = desc or ('Database schema: ' + ', '.join(t for t, _ in tables))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- timeline
def timeline(title, caption, events, desc=None):
    """Horizontal timeline. events: [(label, sub), ...], up to 6."""
    events = list(events)[:6]
    head, top = _header(title, caption)
    parts = [head]
    n = len(events)
    y = top + 110
    x0, x1 = 70, 730
    parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>'
                 % (x0, y, x1, y, LINE))
    for i, (label, sub) in enumerate(events):
        x = x0 + (x1 - x0) * i / max(n - 1, 1)
        parts.append('<circle cx="%.1f" cy="%d" r="10" fill="%s" stroke="%s" stroke-width="3"/>'
                     % (x, y, BG, ACC))
        parts.append('<text x="%.1f" y="%d" %s font-size="11" font-weight="700" fill="%s" '
                     'text-anchor="middle">%d</text>' % (x, y + 4, SANS, ACC, i + 1))
        ty = y - 24
        for ln in wrap(label, 18)[:2]:
            parts.append('<text x="%.1f" y="%d" %s font-size="13" font-weight="700" fill="%s" '
                         'text-anchor="middle">%s</text>' % (x, ty, SANS, INK, esc(ln)))
            ty -= 17
        ty = y + 34
        for ln in wrap(sub, 20)[:3]:
            parts.append('<text x="%.1f" y="%d" %s font-size="11.5" fill="%s" '
                         'text-anchor="middle">%s</text>' % (x, ty, SANS, MUT, esc(ln)))
            ty += 15
    d = desc or ('Timeline: ' + ' -> '.join(l for l, _ in events))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- cycle
def cycle(title, caption, steps, desc=None):
    """Circular loop. steps: [(label, sub), ...], 3-6."""
    import math
    steps = list(steps)[:6]
    head, top = _header(title, caption)
    parts = [head, _defs()]
    cx, cy, R = 400, (top + 430) / 2 + 10, 118
    n = len(steps)
    pts = []
    for i, (label, sub) in enumerate(steps):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pts.append((x, y))
        bw2, bh2 = 168, 64
        parts.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="1.5"/>' % (x - bw2 / 2, y - bh2 / 2, bw2, bh2, SUR, ACC))
        parts.append('<text x="%.1f" y="%.1f" %s font-size="13.5" font-weight="700" fill="%s" '
                     'text-anchor="middle">%s</text>' % (x, y - 4, SANS, INK, esc(wrap(label, 20)[0])))
        sl = wrap(sub, 22)[:1]
        if sl:
            parts.append('<text x="%.1f" y="%.1f" %s font-size="11" fill="%s" '
                         'text-anchor="middle">%s</text>' % (x, y + 16, SANS, MUT, esc(sl[0])))
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # push midpoint outward so arrows arc around the circle
        import math as m
        dx, dy = mx - cx, my - cy
        dist = m.hypot(dx, dy) or 1
        ox, oy = mx + dx / dist * 34, my + dy / dist * 34
        parts.append('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" '
                     'stroke-width="2" marker-end="url(#ah)"/>' % (x1, y1, ox, oy, x2, y2, ACC))
    parts.append('<circle cx="%d" cy="%d" r="34" fill="%s" stroke="%s" stroke-width="1.5"/>'
                 % (cx, cy, SUR2, LINE))
    parts.append('<text x="%d" y="%d" %s font-size="12" font-weight="700" fill="%s" '
                 'text-anchor="middle">repeats</text>' % (cx, cy + 4, SANS, MUT))
    d = desc or ('Continuous loop: ' + ' -> '.join(l for l, _ in steps))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- crypto
def crypto(title, caption, left, key_label, right, left_sub='', key_sub='', right_sub='', desc=None):
    """Three-stage transform: input -> key/material -> output."""
    head, top = _header(title, caption)
    parts = [head, _defs()]
    y = top + 60
    bw, bh = 190, 130
    xs = [70, 305, 540]
    fills = [SUR, SUR2, SUR]
    strokes = [ACC, SIG, PURP]
    labels = [(left, left_sub), (key_label, key_sub), (right, right_sub)]
    for x, (lab, sub), f, s in zip(xs, labels, fills, strokes):
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" '
                     'stroke="%s" stroke-width="2"/>' % (x, y, bw, bh, f, s))
        ty = y + 44
        for ln in wrap(lab, 20)[:2]:
            parts.append('<text x="%d" y="%d" %s font-size="15" font-weight="700" fill="%s" '
                         'text-anchor="middle">%s</text>' % (x + bw // 2, ty, SANS, INK, esc(ln)))
            ty += 20
        for ln in wrap(sub, 24)[:2]:
            parts.append('<text x="%d" y="%d" %s font-size="11.5" fill="%s" '
                         'text-anchor="middle">%s</text>' % (x + bw // 2, ty, SANS, MUT, esc(ln)))
            ty += 15
    for xa, xb in [(260, 305), (495, 540)]:
        parts.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.5" '
                     'marker-end="url(#ah)"/>' % (xa, y + bh / 2, xb, y + bh / 2, ACC))
    d = desc or ('%s combined with %s produces %s' % (left, key_label, right))
    return doc(title, d, ''.join(parts))


# ---------------------------------------------------------------- dispatch
BUILDERS = {
    'keypoints': keypoints,
    'layers': layers,
    'flow': flow,
    'tiers': tiers,
    'topology': topology,
    'table': table_svg,
    'commands': commands,
    'git_branch': git_branch,
    'quadrants': quadrants,
    'schema': schema,
    'timeline': timeline,
    'cycle': cycle,
    'crypto': crypto,
}


def build(kind, **kwargs):
    if kind not in BUILDERS:
        raise ValueError('unknown diagram kind: %r' % kind)
    return BUILDERS[kind](**kwargs)
