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

AREAS = "\n".join(f"`{c}` {d}" for c, d in area_names)

README = f"""```
  ██  ██  █████  ██████  ██████        ██     ██  ██████  ███    ██
  ██  ██ ██   ██ ██   ██ ██   ██       ██     ██ ██    ██ ████   ██
  ██████ ███████ ██████  ██   ██ █████ ██  █  ██ ██    ██ ██ ██  ██
  ██  ██ ██   ██ ██   ██ ██   ██       ██ ███ ██ ██    ██ ██  ██ ██
  ██  ██ ██   ██ ██   ██ ██████         ███ ███   ██████  ██   ████
```

# hard-won

**A thousand skills for AI agents that do real work — each one earned from a failure first.**

Not tips. Not prompt tricks. Procedures with the commands, the thresholds, and the check that
proves it worked.

    {len(slugs)} skills   ·   {words:,} words   ·   {len(areas)} areas   ·   {verdict}

---

## Why this exists

Every skill here started as something that went wrong.

A database was deleted from `server/` while the writer was using the project root — the delete
succeeded and changed nothing. A stale `cache/` replayed deleted file paths into a fresh deploy
log, making a new run look like an old one. A site showed devnet numbers as if they were mainnet.
A transaction was about to be signed against the wrong chain. A test passed because `all()` over an
empty list is `True`.

None of those are exotic. They are the ordinary ways competent agents lose an afternoon, and none
of them are covered by "be careful".

So each one became a skill: the failure, the procedure that prevents it, and the check that proves
you actually ran the procedure.

## What a skill looks like

Every skill is one file, `skills/<slug>/SKILL.md`, with the same four parts:

```markdown
---
name: read-back-state-after-deploy
description: Use when you have just deployed or written to a remote system. Read the state
  back from the owning system instead of trusting the deploy output.
---

## Procedure      numbered steps with real commands
## Pitfalls       the specific ways this goes wrong
## Verification   the check, and the result that means it passed
```

The `description` is the trigger — it says *when* to use it, so an agent can find it without
reading the body. The `Verification` section is not optional: **a skill that cannot be checked is
a belief, not a skill.**

## The gate

`python3 tools/validate.py` fails the build on any of these, so the floor is enforced rather than
promised:

| rejected | why |
|---|---|
| missing `## Procedure` / `## Pitfalls` / `## Verification` | a skill you cannot follow or check is decoration |
| body under 200 words or 35 lines | that is a stub with a title |
| no command, code block or path | an abstraction nobody can execute |
| "in today's fast-paced world", "it's important to note" | filler that costs context and says nothing |
| two skills sharing 50%+ of their 5-gram shingles | the same skill written twice under two names |

Run it with `--only slug-a,slug-b` to check one batch, or bare to check all of them.

## Install

    git clone https://github.com/askexort/hard-won
    cp -r hard-won/skills/* ~/.hermes/skills/          # Hermes Agent
    cp -r hard-won/skills/* ~/.claude/skills/          # Claude Code
    cp -r hard-won/skills/* ~/.codex/skills/           # Codex

They are plain markdown with YAML frontmatter. Any agent that can read a directory can use them;
nothing here depends on a specific runtime.

## The areas

{AREAS}

## What this is not

- **Not a policy or a safety layer.** These are working procedures, not guardrails.
- **Not generated filler.** The validator rejects stubs and duplicates; a thin area gets fixed or
  cut, not padded to hit a number.
- **Not advice about your jurisdiction, your security model, or your money.** Several skills tell
  you to stop and ask a human. That is the point of them.
- **Not finished.** Skills are wrong the moment the world moves. `skill-hygiene` and
  `prune-stale-facts` exist because keeping this set honest is ongoing work.

## The parts worth reading first

If you read four, read these:

    reconcile-state-before-acting          what is actually running, cached and listening
    poison-a-fixture-to-prove-a-detector   prove your detector catches a planted fault
    simulate-a-transaction-before-broadcast  never discover a revert on mainnet
    read-back-state-after-deploy           a successful call is not a successful task
    design-an-eval-that-can-actually-fail  an eval that cannot fail measures nothing

## Contributing

Bring the failure, not the topic. A skill earns its place by describing something that actually
went wrong, the procedure that prevents it, and how to prove the procedure ran. Run
`python3 tools/build-readme.py` afterwards so the figures on this page stay true.

## License

MIT — see `LICENSE`.
"""
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(README)
print(f"  README.md regenerated: {len(slugs)} skills, {words:,} words, {len(areas)} areas, {verdict}")
