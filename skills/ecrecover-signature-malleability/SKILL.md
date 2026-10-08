---
name: ecrecover-signature-malleability
description: Use when a contract verifies signatures with ecrecover for permits, meta-transactions or allowances. Checks s-range, v-value, nonce and domain binding to stop signature replay and malleability.
---

# ecrecover signature malleability and replay

`ecrecover` accepts a malleable `(v, r, s)` and will return a valid signer for more than one encoding of the same signature, so any signature-based path must normalise and bind it to a nonce and chain.

## Procedure

1. Find signature verification: `grep -nE 'ecrecover|ECDSA|isValidSignature|permit\(|DOMAIN_SEPARATOR|verify\(' -r src/`.
2. Replace raw `ecrecover` with OpenZeppelin `ECDSA.recover`, which rejects `s` in the upper half of the curve order and `v ∉ {27, 28}`:

```solidity
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
address signer = ECDSA.recover(digest, v, r, s);
```

3. If hand-rolling, enforce `require(uint256(s) <= 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0, "bad s")` and `require(v == 27 || v == 28)`.
4. Bind to a domain: include `block.chainid` and `address(this)` in the EIP-712 domain separator, and recompute it when `chainid` changes.
5. Bind to a nonce: increment the signer's nonce and `require(!usedNonces[nonce])`, so a signature cannot be replayed.
6. Check the deadline: `require(block.timestamp <= deadline, "expired")` — a missing deadline makes a signature valid forever.
7. Verify `ecrecover` returning `address(0)` for a malformed signature is rejected (`require(signer != address(0))`).
8. Confirm the signed digest covers all mutating fields (amount, spender, nonce, deadline, chainid); a missing field is a replay vector.
9. Test both malleability and replay:

```solidity
(uint8 v2, bytes32 r2, bytes32 s2) = flipS(v, r, s); // s' = n - s, v' = 28/27
vm.expectRevert(); token.permit(owner, spender, value, deadline, v2, r2, s2);
```

10. For ERC-1271 smart-contract wallets, call `isValidSignature` rather than `ecrecover`, which cannot verify them.

## Pitfalls

- Hand-rolled `ecrecover` without the `s`-range check lets an attacker flip `s` to get a second valid signature, breaking any "seen digest" replay map keyed on the signature bytes.
- Domain separator computed once in the constructor with `block.chainid` — on a fork or a chain-id change it is wrong; recompute per call or cache with an invalidation branch.
- Nonce not incremented, so the same meta-transaction executes repeatedly.
- Missing `address(0)` check: `ecrecover` returns `address(0)` on failure, and if `address(0)` is a valid spender in your mapping the check passes.
- Signing `keccak256(data)` without a prefix, allowing a signature to be reused as a different type of payload.

## Verification

    forge test --match-test "testMalleability|testReplay" -vvv

Pass: the flipped-`s` signature reverts and the replayed signature reverts with "nonce used"; `grep -c 'ecrecover' src/` returns 0 (all via ECDSA).

Report each signature site, whether `s` and `v` are checked, and the domain/nonce binding.
