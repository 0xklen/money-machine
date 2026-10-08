---
name: detect-abi-drift
description: Use when a contract you integrate with may have been upgraded or redeployed, and your stored ABI may no longer match the deployed bytecode.
---

# Detect ABI drift

Function selectors live in the deployed bytecode, so you can diff the on-chain selector set
against your stored ABI without trusting a changelog. Run this after any upgrade, before
every integration release, and when a call starts reverting unexpectedly.

## Procedure

1. Extract the function selectors actually present in the deployed runtime bytecode.

       cast selectors $(cast code $PROXY --rpc-url $ETH_RPC) | sort -u > deployed.sel
       wc -l deployed.sel

   Note: on a proxy, `cast code` returns the *proxy's* bytecode (fallback + admin), not the
   implementation's. Resolve the implementation first (see `read-proxy-implementation-slot`)
   and run `cast selectors` on the implementation code.

2. Extract the selectors your stored ABI implies.

       forge inspect src/Vault.sol:Vault methods | awk '{print $1}' | sort -u > local.sel

   Or from a JSON ABI:

       jq -r '.[] | select(.type=="function") | "\(.name)(\(.inputs|map(.type)|join(",")))"' \
         abi.json | xargs -I{} cast sig "{}" | sort -u > local.sel

3. Diff both directions — added *and* removed functions both matter.

       comm -23 deployed.sel local.sel   # on-chain functions missing from your ABI
       comm -13 deployed.sel local.sel   # your ABI has functions not on-chain

4. Compare event signatures too, by recomputing topic0 for each event in the ABI and checking
   the contract still emits them:

       cast keccak "Transfer(address,address,uint256)"
       # 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef

5. Check whether the implementation address itself changed since your last snapshot.

       cast storage $PROXY \
         0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc \
         --rpc-url $ETH_RPC

## Pitfalls

- A proxy with a `fallback` that returns empty calldata for unknown selectors makes an unknown
  function *look* like it succeeded (returning `0x`), hiding drift. Compare selector sets, do
  not probe function-by-function.
- Etherscan verification lags an upgrade by minutes; re-pull the ABI from `getsourcecode`
  rather than trusting a cached copy.
- Storage layout can also drift even when selectors match — a new variable inserted in the
  middle corrupts reads. Re-run an upgrade-safety check, not just the selector diff.
- Diamonds (EIP-2535) route selectors from a `facetAddress` map in storage; `cast selectors` on
  the diamond shows only the diamondCut selectors, so compare against `facets()` output.

## Verification

    comm -23 deployed.sel local.sel | head
    # empty output means every on-chain function is in your ABI

Report the implementation address, the count of selectors on-chain vs in your ABI, and any
functions present in only one set.
