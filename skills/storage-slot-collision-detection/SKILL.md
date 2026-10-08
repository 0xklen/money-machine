---
name: storage-slot-collision-detection
description: Use when two contracts share a storage layout (inheritance, proxy, assembly, or appended modules) and a variable could occupy another's slot. Computes slots and proves no aliasing.
---

# Storage slot collision detection

Two variables colliding in the same slot is invisible until one write silently overwrites the other — the review is slot arithmetic done by hand and cross-checked against the compiler.

## Procedure

1. Dump the layout: `forge inspect MyContract storage-layout --pretty`.
2. Read the raw slot to confirm the compiler's answer: `cast storage $ADDR 0x0 --rpc-url $RPC`.
3. For inherited contracts, verify each base's variables land at the documented offset; C3 linearisation order decides slot order.
4. Check assembly that writes storage directly: `grep -nE 'sstore\(|sload\(|\.slot|keccak256\(.*slot' -r src/` — hand-computed slots must not overlap compiler-assigned ones.
5. For unstructured storage (proxy admin slot `0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103`), confirm it is `bytes32(uint256(keccak256("eip1967.proxy.admin")) - 1)`, not a low slot.
6. For mapping keys, recompute: `keccak256(abi.encode(key, slot))`; verify `cast index uint256 <key> <slot>` matches.
7. Check dynamic array element slots: `keccak256(slot)` is the first element; index i is at `keccak256(slot) + i`.
8. Diff layouts across versions with `diff <(forge inspect A storage-layout) <(forge inspect B storage-layout)`.
9. For Diamond/modular designs, verify each facet's storage namespace is unique (`keccak256("myapp.storage.v1")`).
10. Write an invariant test that writes each variable and asserts no other changed:

```solidity
function invariant_noAlias() public {
    assertEq(readVarA(), varAValue);
    assertEq(readVarB(), varBValue);
}
```

## Pitfalls

- Inheriting two bases that each declare a variable of the same name; Solidity allows it, both get distinct slots, but reads resolve to the most-derived one — a logic bug.
- Assembly computing a slot by hard-coding a number that the compiler later shifts when a new base is added above.
- `uint128` packing: two 128-bit vars share slot N; a partial write via assembly overflows into the sibling.
- Diamond facets reusing `keccak256("diamond.storage")` from the library while the lib table also uses it.
- Mapping over a string key: `keccak256(bytes(key))` vs `keccak256(abi.encodePacked(key))` produce different slots; pick one and stay consistent.

## Verification

    forge inspect MyContract storage-layout --pretty | grep -E 'Name|slot'

Pass: each meaningful variable has a distinct (slot, offset) and the invariant test passes after writing every variable.

Report the layout, any overlaps found, and the invariant test result.
