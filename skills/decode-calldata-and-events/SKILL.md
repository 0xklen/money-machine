---
name: decode-calldata-and-events
description: Use when you need to turn raw transaction input or log data into named function calls and arguments, including for unknown or unverified contracts.
---

# Decode calldata and events

Raw `input` bytes and log topics are opaque until decoded against an ABI. The first four bytes
of calldata are the function selector; the first topic of a log is the event selector. Decode
against the contract's real ABI, and only fall back to signature databases.

## Procedure

1. Pull the raw input and check it is not a plain value transfer.

       cast tx $HASH --rpc-url $RPC --json | jq -r '.to, .value, .input'
       # input == "0x" means a plain ETH transfer, no calldata to decode

2. Identify the selector and, if you have the ABI, decode directly. `cast` takes a human
   signature; argument order and types must match exactly.

       cast calldata-decode "transfer(address,uint256)" \
         0xa9059cbb000000000000000000000000d8da6bf26964af9d7eed9e03e53415d37aa96045000000000000000000000000000000000000000000000000000000000f4240

   With an artifact, use the compiled ABI instead of guessing the signature:

       cast calldata-decode "$(forge inspect Token methods | grep ...)" ...

3. For an unknown selector, look it up — a single DB result is not proof.

       cast 4byte 0x095ea7b3                     # -> approve(address,uint256)
       curl -s "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x095ea7b3" \
         | jq -r '.results[].text_signature'
       curl -s "https://api.openchain.xyz/signature-database/v1/lookup?function=0x095ea7b3" \
         | jq -r '.result.function."0x095ea7b3"[].name'

4. Decode logs. `topics[0]` selects the event; indexed args are in `topics[1..]`, dynamic args
   in `data`.

       cast logs --address $CONTRACT \
         "$(cast keccak 'Transfer(address,address,uint256)')" --rpc-url $RPC --json \
         | jq -r '.[] | [.topics[1], .topics[2], .data] | @tsv'

5. Decode a raw event with its signature and the non-indexed data:

       cast decode-event --sig "Transfer(address,address,uint256)" \
         0x00000000000000000000000000000000000000000000000000000000000f4240

6. Re-encode to confirm round-trip:

       cast calldata "transfer(address,uint256)" 0xd8dA...6045 1000000 | head -c 10

## Pitfalls

- Four-byte selectors collide (the space is only 2^32). A DB hit means "a function with this
  selector exists", not "this is the function called". Confirm against the contract's ABI or
  bytecode before relying on it.
- Signature databases are publicly writable and polluted with spam signatures that decode your
  calldata into plausible-looking garbage. Prefer the verified ABI.
- `delegatecall` and proxies: the calldata is decoded against the implementation's ABI even
  though the tx `to` is the proxy; using the proxy ABI yields wrong results.
- Tuples and arrays need the full type string, e.g.
  `foo((address,uint256)[],bytes32)`, not just the flattened inner types.
- Tokens that do not follow ERC-20 (missing return value, non-standard event) decode with the
  standard ABI but produce nonsense; check the actual emitted topic0.
- Address args are left-padded to 32 bytes in topics; take the last 20 bytes for the address.

## Verification

    cast 4byte 0x095ea7b3
    cast sig "approve(address,uint256)"        # must equal 0x095ea7b3

Decode the same transaction with two sources (the verified ABI and a signature database) and
report the function name, the top-level args, and any disagreement between the sources.
