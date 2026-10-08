<div align="center">

<img src="assets/logo.svg" width="110" alt="money machine">

# MONEY MACHINE

**A thousand skills for AI agents that build money machines — pricing, payments, revenue ops, and
the crypto rails underneath.**

[![stars](https://img.shields.io/github/stars/0xklen/money-machine?style=flat-square&labelColor=000000&color=000000)](https://github.com/0xklen/money-machine/stargazers)
[![last commit](https://img.shields.io/github/last-commit/0xklen/money-machine?style=flat-square&labelColor=000000&color=000000)](https://github.com/0xklen/money-machine/commits/main)
[![license](https://img.shields.io/github/license/0xklen/money-machine?style=flat-square&labelColor=000000&color=000000)](LICENSE)
[![skills](https://img.shields.io/badge/skills-{{skills}}-000000?style=flat-square&labelColor=000000)](skills)

<div align="center">
<pre>
{{art_wordmark}}
</pre>
</div>

<div align="center">
<pre>
{{art_machine}}
</pre>
</div>

{{skills}} skills · {{words}} words · {{areas}} areas · {{verdict}}

</div>

---

## What this is

{{skills}} files, each one a procedure an agent can follow without asking questions. Every skill
started as something that went wrong first: a database deleted from the wrong path, a stale cache
replaying deleted file paths, a test that passed because `all()` over an empty list is `True`.

Not tips. Not prompt tricks. Commands, thresholds, and the check that proves the work happened.

## How to run it

Nothing to build, no dependencies, no package manager. The skills are markdown; the tools are
plain Python 3 with no third-party imports.

**1. Get it**

```bash
git clone https://github.com/0xklen/money-machine
cd money-machine
```

**2. Install the skills into your agent**

```bash
cp -r skills/* ~/.hermes/skills/     # Hermes Agent
cp -r skills/* ~/.claude/skills/     # Claude Code
cp -r skills/* ~/.codex/skills/      # Codex

# or point any agent at the directory directly — it is just files
```

**3. Check it landed**

```bash
ls ~/.hermes/skills | wc -l          # expect {{skills}}
python3 tools/validate.py            # expect {{verdict}}
```

**4. Use one.** You do not read a skill to find it — the `description` is the trigger. When a task
matches, read the whole file and follow `## Procedure`, watch for `## Pitfalls`, then run
`## Verification` and report the result.

**5. Add one of your own**

```bash
mkdir -p skills/my-new-skill
cp TEMPLATE.md skills/my-new-skill/SKILL.md   # fill it in
python3 tools/validate.py --only my-new-skill # must pass, not "looks fine"
python3 tools/build-readme.py                 # refresh the figures above
```

**6. Regenerate the art** (optional — the pixel animations are generated, not drawn by hand)

```bash
python3 tools/pixelart.py
```

## What is in the box

```
money-machine/
├── skills/                  one directory per skill, {{skills}} of them
│   └── <slug>/
│       └── SKILL.md         the skill itself — Procedure, Pitfalls, Verification
├── tools/
│   ├── validate.py          the gate: structure, word floors, duplicates
│   ├── build-readme.py      fills this page's figures from disk
│   └── pixelart.py          generates the pixel art
├── assets/                  logo and generated art
├── TEMPLATE.md              the shape every skill must follow
├── BRIEF.md                 the {{areas}} areas, and what belongs in each
├── LICENSE                  MIT
└── README.md                generated — edit the template, not this file
```

## The fifty-two areas

{{arealist}}

## What this is not

- **Not policy or a safety layer.** These are working procedures, not guardrails.
- **Not filler.** The validator rejects stubs and duplicates, so a thin area gets fixed or cut
  rather than padded to hit a number.
- **Not advice about your jurisdiction, your security model, or your money.** Several skills
  instruct the reader to stop and ask a human. That is the point of them.
- **Not finished.** Skills go stale the moment the world moves; `skill-hygiene` and
  `prune-stale-facts` exist because keeping this honest is ongoing work.

## Four to read first

```
reconcile-state-before-acting             what is actually running, cached and listening
poison-a-fixture-to-prove-a-detector      prove the detector catches a planted fault
simulate-a-transaction-before-broadcast   never discover a revert on mainnet
read-back-state-after-deploy              a successful call is not a successful task
```

## Contributing

Bring the failure, not the topic. A skill earns its place by describing something that actually
went wrong, the procedure that prevents it, and how to prove the procedure ran. Then:

```bash
python3 tools/validate.py      # must print no failures
python3 tools/build-readme.py  # keeps the figures above true
```

## License

MIT — see [LICENSE](LICENSE). Use them, fork them, ship them in your own agent.

<div align="center">

```
   ██████  ██   ██  ██████  ████████  ██   ██     ██   ██  ███████  ██    ██
   ██      ██   ██  ██         ██    ██   ██     ██   ██  ██      ██    ██
   █████   ██   ██  █████      ██    ██   ██     ██   ██  ███████  ██    ██
```

*every skill in here was paid for by a mistake*

</div>
