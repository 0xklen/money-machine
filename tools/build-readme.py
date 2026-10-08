#!/usr/bin/env python3
"""Generate README.md from the real state of the repo. Every figure is read from disk.

Hard-coded numbers rot the moment someone adds a skill and lie until they notice.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "skills")

slugs = sorted(d for d in os.listdir(SK) if os.path.isdir(os.path.join(SK, d)))
words, lines, cats = 0, 0, {}
for s in slugs:
    p = os.path.join(SK, s, "SKILL.md")
    if not os.path.isfile(p):
        continue
    t = open(p, encoding="utf-8").read()
    words += len(t.split())
    lines += len(t.splitlines())

brief = open(os.path.join(ROOT, "BRIEF.md"), encoding="utf-8").read()
areas = re.findall(r"^\s*(\d+)[.\s]+([a-z0-9-]+)\s{2,}(.+?)$", brief, re.M)
area_names = []
for num, code, desc in areas:
    first = desc.strip().split(":")[0].split(",")[0]
    area_names.append((code, first[:58]))
area_names = [a for a in dict.fromkeys(area_names)]


def sh(cmd):
    import subprocess
    return subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True).stdout.strip()


verdict = sh("python3 tools/validate.py 2>&1 | tail -1").strip() or "not run"

AREAS = " · ".join(f"`{c}` {d}" for c, d in area_names)

tmpl = open(os.path.join(ROOT, "tools", "README.template.md"), encoding="utf-8").read()
README = (tmpl.replace("{{skills}}", f"{len(slugs)}")
              .replace("{{words}}", f"{words:,}")
              .replace("{{areas}}", str(len(areas)))
              .replace("{{verdict}}", verdict)
              .replace("{{arealist}}", AREAS))

open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(README)
print(f"  README.md regenerated: {len(slugs)} skills, {words:,} words, {len(areas)} areas, {verdict}")
