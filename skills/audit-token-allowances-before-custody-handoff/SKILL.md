---
name: audit-token-allowances-before-custody-handoff
description: Use when a wallet or treasury address is changing custodian or being retired. Enumerates every outstanding token and NFT approval, revokes the ones a third party can still pull, and proves none remain live.
---

# Audit token allowances before a custody handoff

An allowance is a standing permission that outlives the person who granted it; a wallet handed off with a forgotten unlimited approval is still drainable by the old spender. This skill enumerates every live approval and revokes those that no longer have a reason to exist.

## Procedure

1. Enumerate current approvals. For ERC-20, walk the spender set via a log-derived list or an indexer:
   `cast logs --address $TOKEN --topic0 0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925 --from-block 0 --to-block $LATEST --json`
   then read each current value:
   `cast call $TOKEN "allowance(address,address)(uint256)" $WALLET $SPENDER --rpc-url $RPC`
2. Flag every allowance equal to `uint256.max` (`115792089237316195423570985008687907853269984665640564039457584007913129639935`) — those are the ones an attacker can use without a further signal.
3. Revoke approvals the new custodian will not need by setting them to zero:
   `cast send $TOKEN "approve(address,uint256)" $SPENDER 0 --account $WALLET --rpc-url $RPC`
4. For ERC-721/1155, check operator approvals too:
   `cast call $NFT "isApprovedForAll(address,address)(bool)" $WALLET $OPERATOR --rpc-url $RPC`
   and clear with `setApprovalForAll($OPERATOR, false)`.
5. Confirm post-state: re-read every allowance you touched and confirm zero, and re-enumerate to catch approvals you missed.
6. Record the full before/after table with tx hashes so the handoff is provable.

## Pitfalls

- Revoking one spender while a router or aggregator holds the real allowance leaves the funds pullable through the router.
- A permit granted off-chain and not yet redeemed will not show as an allowance until it is redeemed; a compromised key's outstanding permits are a residual risk even after revoking on-chain approvals.
- Burning the wallet or transferring its key without revoking leaves the approvals live; approvals are per-spender and do not move with the key.
- Some tokens revert on `approve(0)` (e.g. USDT-style); use `approve(spender, 0)` directly rather than relying on decrease-allowance semantics that also revert.
- Never paste the retiring key or any seed into a chat or shell argument during the handoff; the hands-off wallet is drained from the environment or a restricted file only.

## Verification

    cast call $TOKEN "allowance(address,address)(uint256)" $WALLET $SPENDER --rpc-url $RPC
    # expect 0 for every spender you no longer intend to allow; any non-zero is a live risk

Report the approval table before and after, with the revoke tx hashes, quoting the reads.
