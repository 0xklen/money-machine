---
name: read-proxy-implementation-slot
description: Use when a contract is a proxy and you must find the real implementation address from storage, including EIP-1967, beacon, diamond and legacy slots.
---

# Read a proxy implementation slot

Behind a proxy, the address you call is not where the logic lives. Resolve the implementation
from the standard storage slot before reading any business getter, or you will be decoding
proxy admin functions against the wrong ABI.

## Procedure

1. Try the EIP-1967 slots directly. The implementation slot is
   `bytes32(uint256(keccak256("eip1967.proxy.implementation")) - 1)`:

       IMPL_SLOT=0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc
       cast storage $PROXY $IMPL_SLOT --rpc-url $RPC
       # strip leading zeros, last 20 bytes are the address
       cast to-address 0x000000000000000000000000$(cast storage $PROXY $IMPL_SLOT --rpc-url $RPC | tail -c 41)

2. Check the other standard slots:

       # admin:  0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103
       # beacon: 0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50
       cast storage $PROXY 0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103 --rpc-url $RPC
       cast storage $PROXY 0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50 --rpc-url $RPC

3. Try non-standard getters that many proxies still expose:

       cast call $PROXY "implementation()(address)" --rpc-url $RPC 2>/dev/null
       cast call $PROXY "admin()(address)"          --rpc-url $RPC 2>/dev/null
       cast call $PROXY "proxiableUUID()(bytes32)"  --rpc-url $RPC 2>/dev/null   # UUPS marker

4. For a beacon proxy, the beacon slot holds the beacon; read `implementation()` on the beacon:

       cast call $(cast to-address 0x...beaconSlotValue) "implementation()(address)" --rpc-url $RPC

5. For a diamond (EIP-2535), enumerate facets instead of a single slot:

       cast call $PROXY "facets()((address,bytes4[])[])" --rpc-url $RPC

6. Confirm the implementation itself is verified and matches the proxy's ABI expectations.

## Pitfalls

- The slot holds a left-zero-padded 32-byte word; passing the raw word to `cast call` fails.
  Take the last 20 bytes and checksum it with `cast to-address`.
- Old OpenZeppelin proxies (pre-1967) used `keccak256("org.zeppelinos.proxy.implementation")`
  and `keccak256("org.zeppelinos.proxy.admin")`; check both eras.
- A non-proxy contract reads `0x0` for every slot — a zero result means "not a proxy", not
  "implementation is address(0)".
- Beacon proxies have no implementation slot, only the beacon; skipping step 4 leaves the slot
  at zero and is misread as a plain contract.
- Diamonds have no single implementation; a `facets()`-less diamond (some custom) needs the
  `facetAddress(bytes4)` loupe function per selector.
- The implementation can be swapped after you read the slot; re-read it in the same block as any
  dependent call.

## Verification

    cast storage $PROXY 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc --rpc-url $RPC
    # non-zero -> implementation address; cross-check with the Upgraded event

Report the proxy address, the slot that yielded the implementation, the implementation address,
and whether it has verified source.
