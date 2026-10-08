#!/usr/bin/env python3
"""Gate the skill set: structure, substance, and no duplicates. Exits 1 on any failure."""
import argparse, json, os, re, sys
from collections import Counter

RUN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(RUN)
SK = os.path.join(ROOT, "skills")


def parse(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    fm = text[3:end]
    d = {}
    for line in fm.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip()
    return d, text[end + 4:]


def shingles(text, n=5):
    w = re.findall(r"[a-z0-9]+", text.lower())
    return set(tuple(w[i:i + n]) for i in range(max(0, len(w) - n + 1)))


def check(slug):
    d = os.path.join(SK, slug)
    f = os.path.join(d, "SKILL.md")
    errs = []
    if not os.path.isfile(f):
        return ["no SKILL.md"], ""
    fm, body = parse(f)
    if fm is None:
        return ["no frontmatter"], ""
    if fm.get("name") != slug:
        errs.append(f"name '{fm.get('name')}' != directory '{slug}'")
    desc = fm.get("description", "")
    if not desc.lower().startswith("use when"):
        errs.append("description must start with 'Use when'")
    if len(desc) > 500:
        errs.append(f"description {len(desc)} chars > 500")
    for h in ("## Procedure", "## Pitfalls", "## Verification"):
        if h not in body:
            errs.append(f"missing {h}")
    if body.index("## Procedure") > body.index("## Pitfalls") if "## Procedure" in body and "## Pitfalls" in body else False:
        errs.append("sections out of order")
    if len(body.splitlines()) < 35:
        errs.append(f"body only {len(body.splitlines())} lines")
    if len(body.split()) < 200:
        errs.append(f"body only {len(body.split())} words")
    if "```" not in body and "`" not in body:
        errs.append("no concrete artefact (no code/command)")
    if re.search(r"(in today'?s fast-paced|as an AI|delve into|it is important to note)", body, re.I):
        errs.append("filler language")
    return errs, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    slugs = [s.strip() for s in a.only.split(",") if s.strip()] or sorted(
        d for d in os.listdir(SK) if os.path.isdir(os.path.join(SK, d)))
    bad, bodies, probs = {}, {}, {}
    for s in slugs:
        e, b = check(s)
        if e:
            bad[s] = e
        if b:
            bodies[s] = shingles(b)
    # near-duplicate bodies: copy-paste with the title changed is the failure mode
    keys = list(bodies)
    for i, x in enumerate(keys):
        for y in keys[i + 1:]:
            a_, b_ = bodies[x], bodies[y]
            if not a_ or not b_:
                continue
            ov = len(a_ & b_) / min(len(a_), len(b_))
            if ov >= 0.5:
                probs.setdefault(x, []).append(f"{ov:.0%} overlap with {y}")
    for s in sorted(bad):
        print(f"  FAIL {s}")
        for e in bad[s]:
            print(f"         {e}")
    for s in sorted(probs):
        print(f"  DUPE {s}: {'; '.join(probs[s])}")
    ok = len(slugs) - len(bad)
    print(f"\n  {ok}/{len(slugs)} valid, {len(bad)} failing, {len(probs)} duplicate")
    return 1 if (bad or probs) else 0


if __name__ == "__main__":
    sys.exit(main())
