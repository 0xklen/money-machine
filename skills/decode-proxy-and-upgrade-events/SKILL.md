---
name: decode-proxy-and-upgrade-events
description: Use when indexing events from upgradeable proxy contracts. Resolves the implementation active at the block of each log, because the ABI changes across upgrades and one ABI cannot decode the whole history.
---

# Decode proxy and upgrade events across versions

An upgradeable contract's ABI is a timeline, not a constant. Decoding a 2021 log with the 2024 ABI produces garbage fields that still look plausible.

## Procedure

1. Read the EIP-1967 implementation slot per block range, or capture `Upgraded(address)` events to build an implementation timeline:
   `cast storage $PROXY 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc --rpc-url $RPC`
2. Map each log's `block_number` to the implementation active then, then to that implementation's ABI.
3. Decode with the ABI pinned by block and record `decoder_abi_version` on the row:
   ```python
   abi = abi_for_impl(impl_at(block_number))
   ev = contract.decode_event("Transfer", log["topics"], log["data"], abi=abi)
   ```
4. Treat `Upgraded`/`AdminChanged` logs as first-class events; they explain downstream schema changes.
5. When an implementation's code is unverified, fetch its runtime bytecode and match selectors rather than guessing:
   `cast code $IMPL --rpc-url $RPC | cast 4byte-decode <selector>`
6. Re-decode history after a new implementation only for the ranges whose ABI changed.
7. Cache decoded ABI versions per implementation address so a repeated range does not re-read the slot each time.
8. Store the `Upgraded` event's block number and new implementation so the timeline is queryable without re-reading storage.

## Pitfalls

- Using the current implementation's ABI for all history silently mis-decodes pre-upgrade logs whose topic signatures match but whose data layout differs.
- Diamond (EIP-2535) proxies route per facet; one implementation slot does not describe the whole contract.
- A proxy upgraded before the first indexed block needs its historical implementation read, not the current one.
- Signature-compatible upgrades with changed semantics decode cleanly but mean something different; record the version.
- A proxy whose implementation was set in the constructor (no `Upgraded` event) has an empty timeline; read the slot at the deploy block.
- Beacon-proxy (EIP-1967 beacon slot) contracts resolve the implementation through the beacon, not the proxy's own slot; follow the beacon.

## Verification

    cast call $PROXY "implementation()(address)" --rpc-url $RPC
    # compare with the EIP-1967 slot value and with the implementation decoded against per block

Report the implementation timeline by block range and the ABI version used to decode each range.
