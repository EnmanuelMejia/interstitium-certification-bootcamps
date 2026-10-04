#!/usr/bin/env python3
"""Generate one lesson per domain for every content/<slug>.json.

Writes a new top-level "lessons" array into each file, in place, preserving
all other content. Lessons teach underlying concepts distilled from scenario
objectives and why-explanations; they NEVER copy situation/prompt/choices
text. Example code may reuse short evidence snippets (already original
platform content) or, for evidence-free domains, a worked reasoning example.

Usage:
    python3 generator/gen_lessons.py [--limit N]
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

STOP = set(
    """a an the and or but if then else when while of at by for with about into
    through during before after above below to from up down in out on off over
    under again further once here there all any both each few more most other
    some such no nor not only own same so than too very can will just don should
    now is are was were be been being has have had having does did doing would
    could ought its this that these those their them they you your yours we our
    ours us what which who whom whose how why where whether because until as per
    via within without between also often usually always never much many""".split()
)

CODE_LANG = {
    "py": "python", "js": "javascript", "jsx": "javascript", "mjs": "javascript",
    "ts": "typescript", "tsx": "typescript", "java": "java", "c": "c", "h": "c",
    "cpp": "cpp", "cc": "cpp", "cxx": "cpp", "cs": "csharp", "go": "go",
    "rs": "rust", "rb": "ruby", "php": "php", "sql": "sql", "sh": "bash",
    "bash": "bash", "zsh": "bash", "ps1": "powershell", "tf": "terraform",
    "hcl": "terraform", "yml": "yaml", "yaml": "yaml", "json": "json",
    "jsonl": "json", "html": "html", "htm": "html", "css": "css", "xml": "xml",
    "r": "r", "swift": "swift", "kt": "kotlin", "kts": "kotlin",
    "scala": "scala", "lua": "lua", "pl": "perl", "ex": "elixir",
    "erl": "erlang", "hs": "haskell", "dart": "dart", "vue": "vue",
    "dockerfile": "dockerfile",
}

# Lead-in rewordings: turn why-style sentences into lesson-voice teaching prose.
REWORDS = [
    (r"^Remember that\s+", ""),
    (r"^Note that\s+", ""),
    (r"^In short,?\s+", ""),
    (r"^This means\s+", "In practice, "),
    (r"^That means\s+", "In practice, "),
    (r"^The key insight is (that\s+)?", "Key insight: "),
    (r"^The standard fix is\s+", "Fix it by "),
    (r"^The fix is\s+", "Fix it by "),
    (r"^The rule of thumb is (that\s+)?", "Rule of thumb: "),
    (r"^The rule is (that\s+)?", "Rule: "),
    (r"^The takeaway is (that\s+)?", "Takeaway: "),
    (r"^The pattern is\s+", "The pattern: "),
    (r"^In other words,?\s+", ""),
]


def sentences(text):
    """Split text into sentences, keeping punctuation."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'\(\u201c])", text.strip())
    return [p.strip() for p in parts if p.strip()]


def tokens(s):
    return [
        t for t in re.findall(r"[A-Za-z][A-Za-z0-9+#_.\-/]*", s.lower())
        if len(t) > 2 and t not in STOP
    ]


def tokset(s):
    return set(tokens(s))


def reword(s):
    """Light paraphrase: normalize lead-ins, trim, ensure terminal punctuation."""
    s = s.strip()
    for pat, rep in REWORDS:
        ns, n = re.subn(pat, rep, s, count=1)
        if n:
            s = ns
            break
    s = re.sub(r"\s+", " ", s).strip()
    if s and s[-1] not in ".!?:":
        s += "."
    return s


def flow_start(s):
    """Lowercase a sentence start for flow after an 'Objective: ' lead-in,
    but leave acronyms (NIST, SQS, ALE) and single letters intact."""
    if not s:
        return s
    w = s.split(" ", 1)[0].rstrip(".,;:")
    if len(w) > 1 and w.isupper():
        return s
    return s[0].lower() + s[1:] if s[0].isupper() else s


def lead_bullet(obj, s):
    """'Objective: sentence' without echoing the objective twice."""
    obj = obj.rstrip(".")
    low, olow = s.lower(), obj.lower()
    first = obj.split()[0] if obj.split() else ""
    if low.startswith(olow) or (first and low.startswith(first.lower())):
        # sentence already opens with (the start of) the objective — stand alone
        return s[0].upper() + s[1:] if s and s[0].islower() else s
    return obj + ": " + flow_start(s)


def novelty(s, seen_toks):
    """Fraction of this sentence's tokens not already used."""
    ts = tokset(s)
    if not ts:
        return 0.0
    return len(ts - seen_toks) / len(ts)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def trim(s, limit):
    s = s.strip()
    if len(s) <= limit:
        return s
    cut = s.rfind(" ", 0, limit)
    return (s[:cut] if cut > 40 else s[:limit]).rstrip(" ,;:") + "\u2026"


# ---------------------------------------------------------------- domain model

class DomainModel:
    def __init__(self, domain):
        self.domain = domain
        self.scenarios = domain.get("scenarios", []) or []
        # objective frequency + first-appearance order
        self.obj_count = {}
        self.obj_order = {}
        for sc in self.scenarios:
            for o in sc.get("objectives", []) or []:
                o = o.strip()
                if not o:
                    continue
                self.obj_count[o] = self.obj_count.get(o, 0) + 1
                if o not in self.obj_order:
                    self.obj_order[o] = len(self.obj_order)
        self.objectives = sorted(
            self.obj_count, key=lambda o: (-self.obj_count[o], self.obj_order[o])
        )
        # sentence pool from why-explanations: (scenario_idx, sent_idx, text, toks)
        self.pool = []
        for si, sc in enumerate(self.scenarios):
            why = sc.get("why") or ""
            for ji, s in enumerate(sentences(why)):
                if len(s) < 25:
                    continue
                self.pool.append((si, ji, s, tokset(s)))
        self.dom_toks = tokset(" ".join(self.objectives) + " " + domain.get("name", ""))

    def support_sentences(self, objective, used, n=2):
        """Best why-sentences backing an objective, from distinct scenarios.

        A sentence only qualifies if it shares at least one content token with
        the objective or names the objective phrase outright — this keeps each
        concept bullet anchored to its objective instead of drifting.
        """
        key = tokset(objective)
        scored = []
        for si, ji, s, ts in self.pool:
            if s in used:
                continue
            overlap = len(ts & key)
            names_it = objective.lower() in s.lower()
            if overlap < 1 and not names_it:
                continue
            score = overlap * 2 + (3 if names_it else 0)
            score += len(ts & self.dom_toks) * 0.2
            scored.append((score, si, ji, s))
        scored.sort(key=lambda x: (-x[0], x[1], x[2]))
        out, seen_si = [], set()
        for score, si, ji, s in scored:
            if si in seen_si:
                continue
            seen_si.add(si)
            out.append(s)
            if len(out) >= n:
                break
        return out


# ---------------------------------------------------------------- concepts

def build_concepts(dm):
    concepts, used = [], set()
    seen_toks = set()
    for obj in dm.objectives[:6]:
        cands = dm.support_sentences(obj, used, n=2)
        if not cands:
            continue
        s1 = reword(cands[0])
        bullet = lead_bullet(obj, s1)
        seen_toks |= tokset(bullet)
        if len(cands) > 1 and len(bullet) < 200:
            s2 = reword(cands[1])
            if novelty(s2, seen_toks) >= 0.4 and len(bullet) + len(s2) < 340:
                bullet += " " + s2
                seen_toks |= tokset(s2)
        concepts.append(bullet)
        used.update(cands)
        if len(concepts) >= 6:
            break
    # pad to at least 3 with domain-level principles if objectives were thin
    if len(concepts) < 3:
        for si, ji, s, ts in dm.pool:
            if s in used:
                continue
            s = reword(s)
            if novelty(s, seen_toks) >= 0.45:
                concepts.append("Principle: " + flow_start(s))
                seen_toks |= tokset(s)
                used.add(s)
            if len(concepts) >= 3:
                break
    return concepts[:6]


# ---------------------------------------------------------------- pitfalls

def distractor_claim(choice):
    """Extract the misconception claim from a wrong choice (paraphrase-safe)."""
    c = (choice or "").strip()
    parts = re.split(r"\s+[—–]\s+", c, maxsplit=1)
    if len(parts) == 2:
        head, tail = parts[0].strip(), parts[1].strip()
        # short label heads ("Avoid", "Script A", "Mitigate") -> claim is the tail
        if len(head.split()) <= 4 and head[:1].isupper():
            return tail
        return head
    c = re.sub(r"^(Option|Choice)\s+[A-D\d]\s*[:.)]\s*", "", c, flags=re.I)
    return c.strip()


def build_pitfalls(dm):
    claims = []  # (scenario_idx, claim, toks)
    for si, sc in enumerate(dm.scenarios):
        choices = sc.get("choices") or []
        answer = sc.get("answer")
        for i, ch in enumerate(choices):
            if i == answer:
                continue
            claim = distractor_claim(ch)
            ts = tokset(claim)
            if len(ts) < 4:
                continue
            if re.fullmatch(r"[\d$€£.,%\s+x×*/=()\-]+", claim):
                continue  # pure numeric distractors carry no theme
            claims.append((si, claim, ts))
    # rank: domain-relevant, then longer; dedupe near-duplicates
    claims.sort(key=lambda x: (-len(x[2] & dm.dom_toks), -len(x[2])))
    pitfalls, kept = [], []
    for si, claim, ts in claims:
        if any(jaccard(ts, k) >= 0.5 for k in kept):
            continue
        kept.append(ts)
        text = flow_start(claim.rstrip("."))
        pitfalls.append("Common trap: " + text + ".")
        if len(pitfalls) >= 4:
            break
    # fallback: Socratic hints reworded as pitfalls
    if len(pitfalls) < 2:
        for sc in dm.scenarios:
            hint = (sc.get("hint") or "").strip().rstrip("?")
            if len(hint) < 15:
                continue
            if hint[:1].isupper() and not hint.isupper():
                hint = hint[0].lower() + hint[1:]
            cand = "Skipping the key question: " + hint + "."
            cts = tokset(cand)
            if any(jaccard(cts, k) >= 0.5 for k in kept):
                continue
            kept.append(cts)
            pitfalls.append(cand)
            if len(pitfalls) >= 3:
                break
    # last resort: one objective-derived generic (max 1)
    if len(pitfalls) < 2 and len(dm.objectives) >= 2:
        pitfalls.append(
            "Confusing %s with %s \u2014 nail the distinction before you drill."
            % (dm.objectives[0].lower(), dm.objectives[1].lower())
        )
    return pitfalls[:4]


# ---------------------------------------------------------------- example

def lang_for(label):
    base = re.sub(r"\s*\(.*\)\s*$", "", label or "").strip()
    ext = base.rsplit(".", 1)[-1].lower() if "." in base else ""
    return CODE_LANG.get(ext, "text")


def pick_evidence(dm):
    """Pick the best (label, text, scenario_idx): short code sample preferred."""
    items = []
    for si, sc in enumerate(dm.scenarios):
        for ev in sc.get("evidence", []) or []:
            if not ev or len(ev) < 2:
                continue
            label, text = ev[0], ev[1]
            if not text or not text.strip():
                continue
            items.append((label, text, si))
    if not items:
        return None
    code_items = [it for it in items if lang_for(it[0]) != "text"]
    cands = code_items or items

    def score(it):
        label, text, si = it
        lines = [ln for ln in text.splitlines()]
        n = len(lines)
        # prefer 2..10 lines; penalize very long
        pen = 0 if 2 <= n <= 10 else (5 if n == 1 else 20)
        overlap = len(tokset(label + " " + lines[0] if lines else label) & dm.dom_toks)
        return (pen, n, -overlap)

    return min(cands, key=score)


def build_example(dm, used_sents):
    pick = pick_evidence(dm)
    if pick is None:
        return worked_text_example(dm)
    label, text, si = pick
    lang = lang_for(label)
    lines = [ln.rstrip() for ln in text.splitlines()]
    while lines and not lines[-1].strip():
        lines.pop()
    code = "\n".join(lines[:11]).strip("\n")
    sc = dm.scenarios[si]
    why_sents = [s for s in sentences(sc.get("why") or "") if len(s) >= 25]
    walk = []
    seen = set(tokset(" ".join(used_sents))) if used_sents else set()
    # pass 1: prefer sentences not already used in the concepts
    for s in why_sents:
        r = reword(s)
        if r in walk:
            continue
        if not walk or (novelty(r, seen) >= 0.3 and len(" ".join(walk)) + len(r) < 480):
            walk.append(r)
            seen |= tokset(r)
        if len(walk) >= 3:
            break
    # pass 2: still fewer than 2 sentences? reuse is better than thin.
    if len(walk) < 2:
        for s in why_sents:
            r = reword(s)
            if r not in walk:
                walk.append(r)
            if len(walk) >= 2:
                break
    if not walk:
        walk = ["Study the sample line by line, then map each line back to the concepts above."]
    return {"lang": lang, "code": code, "walkthrough": " ".join(walk[:3])}


def worked_text_example(dm):
    """Evidence-free domains: a worked reasoning example in plain text."""
    theme = dm.objectives[0] if dm.objectives else dm.domain.get("name", "this domain")
    # best explanatory sentences across the domain
    scored = []
    for si, ji, s, ts in dm.pool:
        score = len(ts & dm.dom_toks)
        if re.search(r"\b(rule|key|means|because|always|never|best|correct|principle)\b", s, re.I):
            score += 2
        scored.append((score, si, ji, s))
    scored.sort(key=lambda x: (-x[0], x[1], x[2]))
    picked, seen = [], set()
    for score, si, ji, s in scored:
        r = reword(s)
        if novelty(r, seen) >= 0.35:
            picked.append(r)
            seen |= tokset(r)
        if len(picked) >= 3:
            break
    while len(picked) < 3:
        picked.append("Apply the domain principles step by step, and check each claim against the objectives above.")
    lines = [
        "Worked example \u2014 " + theme.lower(),
        "Setup: " + trim(picked[0], 150),
        "Reasoning: " + trim(picked[1], 150),
        "Takeaway: " + trim(picked[2], 150),
    ]
    walkthrough = (
        "Read the setup and name the principle at play before looking at the reasoning. "
        "Then compare your answer with the takeaway \u2014 if they differ, re-read the "
        "concepts above and try the drill scenarios for this domain."
    )
    return {"lang": "text", "code": "\n".join(lines), "walkthrough": walkthrough}


# ---------------------------------------------------------------- lesson

def build_lesson(domain):
    dm = DomainModel(domain)
    if not dm.scenarios:
        return None
    concepts = build_concepts(dm)
    used_sents = set()
    for c in concepts:
        used_sents.add(c)
    example = build_example(dm, used_sents)
    pitfalls = build_pitfalls(dm)
    try_it = (
        "Try it now in the Terminal tab \u2192"
        if example["lang"] != "text"
        else "Work through this in the Terminal tab \u2192"
    )
    return {
        "domain_id": domain.get("id"),
        "title": domain.get("name", "").strip() + " \u2014 Core concepts",
        "concepts": concepts,
        "example": example,
        "pitfalls": pitfalls,
        "try_it": try_it,
    }


def process_file(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    domains = data.get("domains") or []
    lessons = []
    skipped = []
    for dom in domains:
        lesson = build_lesson(dom)
        if lesson is None:
            skipped.append(dom.get("id"))
        else:
            lessons.append(lesson)
    # insert "lessons" right after "domains", preserving everything else
    out = {}
    for k, v in data.items():
        out[k] = v
        if k == "domains":
            out["lessons"] = lessons
    if "lessons" not in out:
        out["lessons"] = lessons
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(lessons), skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="process only first N files (testing)")
    ap.add_argument("--content-dir", default=None, help="override content dir (testing)")
    args = ap.parse_args()
    content_dir = Path(args.content_dir) if args.content_dir else CONTENT_DIR
    files = sorted(content_dir.glob("*.json"))
    if args.limit:
        files = files[: args.limit]
    total, total_skipped = 0, []
    for path in files:
        try:
            n, skipped = process_file(path)
        except Exception as e:  # never silently corrupt a content file
            print(f"{path.stem}: ERROR {e}", file=sys.stderr)
            continue
        total += n
        flag = f"  skipped domains: {','.join(skipped)}" if skipped else ""
        print(f"{path.stem}: {n} lessons{flag}")
        total_skipped.extend((path.stem, d) for d in skipped)
    print(f"TOTAL: {total} lessons across {len(files)} files")
    if total_skipped:
        print(f"SKIPPED DOMAINS: {total_skipped}")


if __name__ == "__main__":
    main()
