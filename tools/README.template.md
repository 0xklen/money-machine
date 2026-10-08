<img src="assets/logo.svg" width="96" alt="money machine">

![MONEY MACHINE typing itself in, letter by letter](assets/banner.gif)

# money machine

**A thousand skills for AI agents that build money machines — pricing, payments, revenue ops, and
the crypto rails underneath. Every one earned from something that went wrong first.**

Not tips. Not prompt tricks. Procedures with the commands, the thresholds, and the check that
proves it worked.

    {{skills}} skills   ·   {{words}} words   ·   {{areas}} areas   ·   {{verdict}}

---

## Why this exists

Every skill here started as something that went wrong.

A database was deleted from `server/` while the writer was using the project root — the delete
succeeded and changed nothing. A stale `cache/` replayed deleted file paths into a fresh deploy
log, making a new run look like an old one. A site displayed devnet numbers as if they were mainnet.
A test passed because `all()` over an empty list is `True`.

![A coin drops into the machine and the stack grows: money making money](assets/money.gif)

![A terminal running the validator: lines appear, one turns red, the run ends green](assets/terminal.gif)

None of that is exotic. It is the ordinary way a competent agent loses an afternoon, and none of it
is covered by "be careful". So each one became a skill: the failure, the procedure that prevents it,
and the check that proves you actually ran the procedure.

## What a skill looks like

One file, `skills/<slug>/SKILL.md`, always the same four parts:

```markdown
---
name: read-back-state-after-deploy
description: Use when you have just deployed or written to a remote system. Read the state
  back from the owning system instead of trusting the deploy output.
---

## Procedure      numbered steps, real commands
## Pitfalls       the specific ways this goes wrong
## Verification   the check, and the result that means it passed
```

The `description` is the trigger — it says *when* to use the skill, so an agent can find it without
reading the body. The `Verification` section is not optional. **A skill you cannot check is a
belief, not a skill.**

## The gate

![A progress bar filling to one thousand](assets/bar.gif)

`python3 tools/validate.py` fails the build on any of these, so the floor is enforced rather than
promised:

| rejected | why |
|---|---|
| missing `## Procedure` / `## Pitfalls` / `## Verification` | a skill you cannot follow or check is decoration |
| under 200 words or 35 lines | that is a stub with a title |
| no command, code block or path | an abstraction nobody can execute |
| "in today's fast-paced world", "it's important to note" | filler that costs context and says nothing |
| two skills sharing 50%+ of their 5-gram shingles | the same skill written twice under two names |

Run it bare to check everything, or `--only slug-a,slug-b` for one batch.

## Install

    git clone https://github.com/askexort/money-machine
    cp -r money-machine/skills/* ~/.hermes/skills/     # Hermes Agent
    cp -r money-machine/skills/* ~/.claude/skills/     # Claude Code
    cp -r money-machine/skills/* ~/.codex/skills/      # Codex

Plain markdown with YAML frontmatter. Any agent that can read a directory can use them; nothing
here depends on a particular runtime.

## What's in the machine

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

    reconcile-state-before-acting          what is actually running, cached and listening
    poison-a-fixture-to-prove-a-detector   prove the detector catches a planted fault
    simulate-a-transaction-before-broadcast  never discover a revert on mainnet
    read-back-state-after-deploy           a successful call is not a successful task

## Contributing

Bring the failure, not the topic. A skill earns its place by describing something that actually
went wrong, the procedure that prevents it, and how to prove the procedure ran. Afterwards run
`python3 tools/build-readme.py` so the figures above stay true, and `python3 tools/pixelart.py`
if you changed the art.

## License

MIT — see `LICENSE`.
