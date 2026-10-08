---
name: audit-bridge-trust-assumptions
description: Use when evaluating a bridge before moving funds: classifying the trust model (lock-mint multisig, optimistic, light client, zk), counting validators, and checking upgrade and delay controls.
---

# Audit bridge trust assumptions

A bridge is only as strong as its weakest trust anchor: most bridge losses came from a validator multisig or an upgradeable contract, not the cryptography, so the audit is about who can move the locked funds and how easily.

## Procedure

1. Classify the model by reading the vault: lock-and-mint (wrapped asset), liquidity network (native both sides), optimistic (fraud window), or light-client/zk (on-chain proof). Record which.

2. For lock-mint and validator bridges, read the quorum:

   cast call $VAULT "getThreshold()(uint256)" --rpc-url $RPC
   cast call $VAULT "getOwners()(address[])" --rpc-url $RPC

   A 2-of-3 or a single EOA owner is a soft target; require >= 5-of-9 with independent operators.

3. Check upgradeability and delay: is the implementation behind a proxy, is there a timelock, and how long?

   cast storage $PROXY 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc --rpc-url $RPC

   A `None` delay on an upgradeable vault means the team can drain instantly.

4. Read TVL as a risk scalar — a $50M bridge protecting $2B TVL is a disproportionate honeypot:

   curl -s https://api.llama.fi/tvl/$BRIDGE

5. For optimistic bridges, verify the challenge window (typically 7 days) and whether a "fast" liquidity path bypasses it — the fast path usually reintroduces a trusted party.

6. Require: threshold >= 2/3 of validators, upgrade delay >= 48h, a documented pause/slashing mechanism, and two independent RPCs for monitoring. Fail the bridge if any is missing and the intended amount exceeds what you can afford to lose.

## Pitfalls

- Reading only the token contract; the trust lives in the vault/bridge contract, not the ERC-20 wrapper.
- A "decentralized" label sitting on a 3-of-5 multisig with a team-held key is one compromise from loss.
- Bridge TVL is frequently double-counted; a "$2B" label often nets to far less locked value on the destination chain.

## Verification

    cast call $VAULT "getOwners()(address[])" --rpc-url $RPC

Count owners and compare to `getThreshold()`; fewer than 5 owners or a threshold below 2/3 fails the review.

Report model, threshold, upgrade delay, TVL, and the disqualifying finding.
