# Build brief: 200 agent skills

Every skill is a directory `skills/<slug>/SKILL.md` following `TEMPLATE.md` exactly.

Rules that the validator enforces, and that are not negotiable:

- frontmatter `name` equals the directory slug, lowercase, hyphenated.
- `description` starts with the literal words `Use when` and is under 500 characters.
- the body has the headings `## Procedure`, `## Pitfalls`, `## Verification`, in that order.
- at least 35 lines and 200 words of real content. A stub fails the build.
- at least one concrete artefact: a real command, a code block, or a path.
- no two skills may share their body. Near-duplicates (5-gram overlap >= 0.5) fail.
- no filler, no "in today's fast-paced world", no restating the title as the body.

## The ten builders and their areas

Each builder writes 20 skills, numbered 01-20, inside its own area. Slugs are invented by the
builder and must be specific and descriptive, not generic (`verify-a-broadcast-tx` not `tx-help`).

1. agent-01  Agent self-management: state reconciliation, resumable handoffs, rollback-first
   operations, ask-vs-act rubrics, absorbing course corrections, sunk-cost detection, failure
   archaeology, tool-selection economics, context budgeting, decomposition, retry-vs-switch,
   irreversible-action gates, dry runs, idempotency, silent-failure detection, timeouts.
2. agent-02  Agent honesty and evidence: claim auditing, honest uncertainty, error-message
   literalism, assumption logging, decision records, requirement freezing, scope-creep guards,
   progress reporting, budget tracking, verification of third parties, evidence tables,
   distinguishing correlation from causation, and reporting absence of evidence.
3. software-01  Correctness under change: refactor safety, test-fixture poisoning, mutation
   testing, property-based tests, flaky-test triage, cache invalidation, migration safety,
   schema evolution, API contract tests, backward compatibility, dead-code proof.
4. software-02  Running systems: observability, structured logging, error taxonomy, profiling,
   memory leaks, races, lock ordering, retry storms, circuit breaking, graceful degradation,
   blue-green cutover, canaries, rollback automation, incident timelines, postmortems.
5. software-03  Delivery and supply chain: reproducible builds, dependency audit, vendoring,
   offline builds, artifact provenance, supply-chain integrity, signing, release checklists,
   semver, changelogs, versioning, monorepo navigation, CI caching, cost profiling, capacity.
6. crypto-01  Keys and signing: key management, wallet hygiene, seed safety, signing-request
   review, transaction simulation, gas estimation, nonce management, replay protection,
   chain-id verification, EIP-712, permits, multisig operations, timelocks, approval revocation.
7. crypto-02  Contract safety: reentrancy, access control, oracle manipulation, flash loans,
   integer and rounding, ERC-20 quirks, ERC-721/1155 semantics, proxy upgrades, storage
   collisions, contract size, fuzzing, invariants, fork testing, static analysis, audit passes.
8. crypto-03  DeFi and markets: liquidity maths, impermanent loss, staking rewards, liquidation
   maths, stablecoin depegs, slippage and MEV, sandwich resistance, front-running, private
   mempools, bridges, L2 finality, tokenomics, vesting, treasury, airdrop and sybil resistance.
9. crypto-04  On-chain interaction: contract address verification, explorer verification, deploy
   verification, event reconstruction, indexing with reorgs, RPC redundancy and rate limits,
   archival access, calldata decoding, ABI drift, selectors, node health, testnet parity,
   mainnet deploy checklists, account abstraction, paymasters, scams and drainers.
10. judgment  Research and evaluation: source triangulation, primary sources, dataset provenance,
   sampling bias, statistical honesty, chart checks, reproducible analysis, scraping ethics,
   rate-limited crawls, record dedup, entity resolution, timelines, uncertainty ranges,
   forecasting calibration, benchmarks, eval design, LLM-judge pitfalls, red-teaming your own
   output, adversarial inputs, gap analysis.

---

# Campaign to 1000 skills

Fifty areas, twenty skills each. Areas 1-10 are above (wave 1). Areas 11-50 follow and are
dispatched in four further waves of ten.

11 agent-03    Memory and knowledge: memory vs session vs skill routing, pruning stale facts,
               resolving conflicting memories, retrieval quality, taxonomy design, skill versions.
12 agent-04    Multi-agent orchestration: briefs, verifying children, fan-out and fan-in, shared
               file conflicts, starvation, parallel cost, steering a child, stopping safely.
13 agent-05    Tool and API integration: docs reading, pagination, auth flows, backoff, response
               validation, schema drift, rate budgets, webhooks, idempotency keys, sandbox vs prod.
14 agent-06    Failure containment: blast radius, kill switches, safe defaults, fail-closed vs
               fail-open, degradation ladders, poison messages, quarantine, backpressure.
15 agent-07    Communication: terse reporting, status vs progress, bad news first, asking well,
               proposals vs questions, avoiding sycophancy, self-correction, docs for strangers.
16 sec-01      Security review: authn vs authz, IDOR, injection, SSRF, deserialization, secrets in
               code, dependency CVEs, sessions, CSRF, rate-limit abuse, security headers.
17 sec-02      Privacy and data: PII inventory, minimisation, retention, deletion vs anonymisation,
               consent, PII in logs, third-party flows, encryption at rest and in transit, breach.
18 sec-03      Adversarial robustness: prompt injection, tool poisoning, exfiltration channels,
               jailbreak resistance, prompt supply chain, canary tokens, sandboxing, egress watch.
19 data-01     Pipelines: idempotent ETL, incremental loads, watermarks, late data, schema drift,
               backfills, dead-letter queues, exactly-once myths, lineage, data contracts.
20 data-02     Analytics: metric definitions, denominators, cohorts, seasonality, Simpson's
               paradox, survivorship bias, A/B validity, contamination, significance vs relevance.
21 infra-01    Containers: image pinning, layer caching, non-root, health/readiness, limits,
               config vs secrets, multi-arch, graceful shutdown, log routing, stateful pitfalls.
22 infra-02    Networking: DNS, TLS renewal, load balancing, timeout vs retry, proxies, CORS,
               private routing, firewall rules, debugging with curl and packet capture.
23 infra-03    Storage: choosing a store, backup vs snapshot, restore drills, retention,
               durability tradeoffs, object permissions, capacity alarms, corruption detection.
24 infra-04    IaC and environments: drift detection, state locking, plan review, secrets in state,
               environment parity, tagging, teardown, idle cost, destructive plans.
25 perf-01     Web performance: Core Web Vitals, bundle analysis, cache headers, image formats,
               layout shift, blocking scripts, perceived speed, mobile throttling, budgets.
26 perf-02     Backend performance: query plans, N+1, indexes, pooling, cache layers, stampedes,
               batch vs loop, backpressure, profiling in prod, headroom.
27 prod-01     Product and requirements: problem vs solution, acceptance criteria, smallest
               shippable slice, spec drift, user-visible states, error copy, telemetry, kill criteria.
28 prod-02     Design engineering: type scale, spacing, contrast, motion rules, focus states,
               dark mode, breakpoints, empty/loading/error states, terse vs verbose copy.
29 crypto-05   Wallets and custody: MPC vs multisig, hardware, hot-wallet limits, address
               whitelists, withdrawal limits, key ceremony, recovery drills, signer rotation.
30 crypto-06   MEV and orderflow: searcher vs builder, private orderflow, bundles, reverting tx
               cost, latency games, censorship resistance, tips vs fees, MEV accounting.
31 crypto-07   Rollups and L2 ops: sequencer trust, forced inclusion, escape hatches, withdrawal
               delays, proving windows, calldata vs blobs, L2 fee markets, cross-domain messages.
32 crypto-08   Stablecoins and payments: peg mechanisms, attestation, redemption, depeg drills,
               payment finality, invoicing, refunds, tax events, chargeback-free assumptions.
33 crypto-09   NFT and on-chain art: metadata permanence, pinning, on-chain SVG gas, royalties,
               mint mechanics, allowlists, reveal fairness, rarity verification, approvals.
34 crypto-10   Governance and DAOs: proposal lifecycle, quorum maths, delegation, timelocks,
               treasury controls, vote buying, emergency councils, execution review, transparency.
35 crypto-11   Data and indexers: reorg handling, backfill, entity modelling, query performance,
               on-chain to off-chain joins, event decoding, RPC budgets, indexing correctness.
36 crypto-12   Compliance-aware work: sanctions screening basics, travel rule, KYC/AML boundaries,
               privacy vs compliance, analytics pitfalls, jurisdiction, records, not legal advice.
37 ai-01       Model selection and prompting: model for the job, context vs cost, prompt structure,
               few-shot, tool schemas, output parsing, determinism, fallbacks, degraded providers.
38 ai-02       Evaluation and red-teaming: evals that can fail, judge bias, contamination,
               adversarial cases, regression suites, human sampling, thresholds, ship criteria.
39 ai-03       RAG and knowledge: chunking, embeddings vs keyword, recall vs precision, citations,
               freshness, poisoning, retrieval eval, hybrid search, per-chunk access control.
40 ai-04       Agents and tool use: tool selection, plan vs react, loop detection, budget limits,
               human-in-the-loop gates, per-tool permissions, sandboxed exec, action logs, replay.
41 craft-01    Docs and writing: READMEs that work, changelogs, API docs, runbooks, decisions,
               editing your own slop, plain language, example-first, doc drift detection.
42 craft-02    Code review: correctness, intent vs implementation, small diffs, comments that
               teach, security in review, coverage of the diff, approval criteria, blocking vs nit.
43 craft-03    Debugging method: reproduce first, bisect, hypothesis log, one variable, instrument
               before guessing, heisenbugs, reset to known good, documenting the fix.
44 craft-04    Incident command: roles, comms cadence, stakeholder updates, mitigate vs root cause,
               decision logs, blameless handoff, customer language, followups.
45 craft-05    Estimation and planning: ranges not points, reference classes, uncertainty budgets,
               dependency risk, buffers, milestone vs deadline, re-estimating, saying no.
46 craft-06    Negotiation and scope: reading the real ask, tradeoffs with costs, refusing unsafe
               work, re-negotiating when facts change, written agreement, escalation.
47 craft-07    Teaching and onboarding: explaining by example, choosing abstractions, exercises,
               feedback that lands, checking understanding, curated reading, first-week wins.
48 craft-08    Automation design: what to automate, cron vs event, idempotent jobs, alert only on
               action, failure visibility, runbook links, cost of automation, retiring automation.
49 craft-09    Time and calendar: timezone correctness, DST bugs, cron in UTC, duration vs deadline,
               timezone-aware logs, batch windows, retry timing.
50 craft-10    Money and units: currency units, rounding, fee arithmetic, basis points, precision
               loss, aggregation vs multiplication, reconciliation, audit trails, never float money.
