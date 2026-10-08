<div align="center">

<img src="assets/logo.svg" width="110" alt="money machine">

# MONEY MACHINE

**A thousand skills for AI agents that build money machines — pricing, payments, revenue ops, and
the crypto rails underneath.**

[![stars](https://img.shields.io/github/stars/0xklen/money-machine?style=flat-square&labelColor=000000&color=000000)](https://github.com/0xklen/money-machine/stargazers)
[![last commit](https://img.shields.io/github/last-commit/0xklen/money-machine?style=flat-square&labelColor=000000&color=000000)](https://github.com/0xklen/money-machine/commits/main)
[![license](https://img.shields.io/github/license/0xklen/money-machine?style=flat-square&labelColor=000000&color=000000)](LICENSE)
[![skills](https://img.shields.io/badge/skills-1040-000000?style=flat-square&labelColor=000000)](skills)

```
   █   █   ███   █   █  █████  █   █        █   █   ███   ████  █   █  █  █   █  █████
   ██ ██  █   █  ██  █  █      █   █        ██ ██  █   █  █     █   █  █  ██  █  █
   █   █   ███   █   █  █████   ███         █   █   ███   █     █████  █  █   █  █████
```

```
              .---------.
             /    $      \          +-----------------------+
            |      $      |  --->   |   [    C O I N    ]  |
             \    $      /          |                       |
              '---------'           |   $   $   $   $   $   |
                                    |   $   $   $   $   $   |
                                    +-----------------------+
     one coin goes in  ................  a machine, and a lot of coins come out
```

1040 skills · 444,073 words · 52 areas · 1040/1040 valid, 0 failing, 0 duplicate

</div>

---

## What this is

1040 files, each one a procedure an agent can follow without asking questions. Every skill
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
ls ~/.hermes/skills | wc -l          # expect 1040
python3 tools/validate.py            # expect 1040/1040 valid, 0 failing, 0 duplicate
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
├── skills/                  one directory per skill, 1040 of them
│   └── <slug>/
│       └── SKILL.md         the skill itself — Procedure, Pitfalls, Verification
├── tools/
│   ├── validate.py          the gate: structure, word floors, duplicates
│   ├── build-readme.py      fills this page's figures from disk
│   └── pixelart.py          generates the pixel art
├── assets/                  logo and generated art
├── TEMPLATE.md              the shape every skill must follow
├── BRIEF.md                 the 52 areas, and what belongs in each
├── LICENSE                  MIT
└── README.md                generated — edit the template, not this file
```

## The fifty-two areas

`agent-01` Agent self-management · `agent-02` Agent honesty and evidence · `software-01` Correctness under change · `software-02` Running systems · `software-03` Delivery and supply chain · `crypto-01` Keys and signing · `crypto-02` Contract safety · `crypto-03` DeFi and markets · `crypto-04` On-chain interaction · `judgment` Research and evaluation · `agent-03` Memory and knowledge · `agent-04` Multi-agent orchestration · `agent-05` Tool and API integration · `agent-06` Failure containment · `agent-07` Communication · `sec-01` Security review · `sec-02` Privacy and data · `sec-03` Adversarial robustness · `data-01` Pipelines · `data-02` Analytics · `infra-01` Containers · `infra-02` Networking · `infra-03` Storage · `infra-04` IaC and environments · `perf-01` Web performance · `perf-02` Backend performance · `prod-01` Product and requirements · `prod-02` Design engineering · `crypto-05` Wallets and custody · `crypto-06` MEV and orderflow · `crypto-07` Rollups and L2 ops · `crypto-08` Stablecoins and payments · `crypto-09` NFT and on-chain art · `crypto-10` Governance and DAOs · `crypto-11` Data and indexers · `crypto-12` Compliance-aware work · `ai-01` Model selection and prompting · `ai-02` Evaluation and red-teaming · `ai-03` RAG and knowledge · `ai-04` Agents and tool use · `craft-01` Docs and writing · `craft-02` Code review · `craft-03` Debugging method · `craft-04` Incident command · `craft-05` Estimation and planning · `craft-06` Negotiation and scope · `craft-07` Teaching and onboarding · `craft-08` Automation design · `craft-09` Time and calendar · `craft-10` Money and units · `money-01` Pricing and unit economics · `money-02` Revenue operations

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
