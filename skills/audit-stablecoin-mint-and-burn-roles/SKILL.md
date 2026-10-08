---
name: audit-stablecoin-mint-and-burn-roles
description: Use when a token claims to be backed but you have not checked who can create supply. Enumerates mint, burn, and upgrade privileges on-chain and flags any issuance path not tied to a deposit.
---

# Audit stablecoin mint and burn roles

Reserve backing means nothing if an admin key can mint supply without a matching deposit. Enumerate every path that creates or destroys the token, and confirm each is tied to a deposit or a documented process.

## Procedure

1. Dump the ABI and search for privileged selectors:
   `cast interface $TOKEN | grep -iE "mint|burn|owner|role|upgrade"`
2. Read the owner and any role registry:
   `cast call $TOKEN "owner()(address)" --rpc-url $RPC`
   `cast call $TOKEN "getRoleMember(bytes32,uint256)(address)" $MINTER_ROLE 0 --rpc-url $RPC`
3. For each minter, classify: is it a deposit contract that mints only against a verified deposit, or an EOA/multisig that can mint on demand?
4. Verify the burn path ties to redemption: pull burn events and confirm each follows a redemption:
   `cast logs --from-block $START --address $TOKEN "$BURN_TOPIC" | jq length`
5. Check upgradeability: read the EIP-1967 implementation slot — an upgradeable token can gain a mint function after your review.
   `cast storage $TOKEN 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc --rpc-url $RPC`
6. Enumerate pause privileges: does the token expose `pause()`/`whenNotPaused` on transfers?

## Pitfalls

- A renounced `owner` while a separate `MINTER_ROLE` persists: renouncement is not a privilege audit.
- Minting via `transferFrom` out of a "bridge" reserve pool that is really the issuer's own float.
- A proxy admin that can upgrade to a new mint implementation after your audit window closes.
- Assuming a burn event means fewer liabilities when the same tx can re-mint.
- Reading only the EOAs and missing minters held by contracts that themselves have an admin.
- A timelock on the minter role that is shorter than your response time is effectively no timelock.

## Verification

    cast interface $TOKEN | grep -iE "mint|burn|pause|owner|role" | sort -u
    # every privileged selector mapped to an address and a rationale; none unaccounted for

Report the minter addresses, whether mint is deposit-linked, and the upgrade and pause status.
