---
name: budget-eth-getlogs-block-ranges
description: Use when querying eth_getLogs over a large block range. Shrinks the window until the provider returns, respects result caps, and catches the silent truncation a capped provider applies.
---

# Budget eth_getLogs block ranges

Providers silently cap `eth_getLogs` by result count. A request that succeeds with a truncated list looks like a quiet chain, not a rate error.

## Procedure

1. Never request an unbounded range. Start with a fixed window and a topic filter:
   ```bash
   curl -s $RPC -H 'content-type: application/json' -d '{
     "jsonrpc":"2.0","id":1,"method":"eth_getLogs","params":[{
       "fromBlock":"0x1036640","toBlock":"0x1036664",
       "address":"0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
       "topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]
     }]}
   ' | jq '.result | length'
   ```
2. Treat a count near a round cap (1000, 10000) as a truncation signal, not a finish line. Halve the window and re-query.
3. Implement adaptive halving: a 1000-block window at or above the cap retries at 500, then 250, until the count sits well under it.
4. Bisect the range deterministically so parallel workers cover disjoint blocks and never overlap:
   `ranges = [(start + i*W, min(start + (i+1)*W - 1, end)) for i in range(n)]`
5. Persist the last completed range so a crash resumes rather than re-scans.
6. For very active contracts, add a second indexed topic (e.g. a `from` address) to cut the result set instead of only shrinking blocks.

## Pitfalls

- A provider returning exactly its cap for a wide range may have stopped at block 3; the count, not the span, is the tell.
- Caps differ by provider and can change silently; assume each node has its own.
- Overlapping parallel ranges double-count unless you dedupe on `(tx_hash, log_index)`.
- An archive-limited paid node rejects old ranges; that is a plan limit, not a reorg.

## Verification

    curl -s $RPC -H 'content-type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"eth_getLogs","params":[{"fromBlock":"0x1036640","toBlock":"0x1036640","address":"0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"}]}' | jq '.result | length'
    # one block, count well under the cap, confirms sizing before the wide scan

Report the window width chosen, the observed per-window counts, and the cap you stayed under.
