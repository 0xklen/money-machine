---
name: identify-function-selectors
description: Use when you see a bare 4-byte selector or event topic and must work out which function or event it is, and whether the match is trustworthy.
---

# Identify function selectors

A selector is `bytes4(keccak256("name(type,type,...)"))` truncated to 4 bytes. Look it up, but
treat database hits as candidates: the selector space is small enough to collide, so confirm
against real bytecode or an ABI.

## Procedure

1. Compute the selector from a signature to build intuition and to round-trip later.

       cast sig "transfer(address,uint256)"      # 0xa9059cbb
       cast sig "approve(address,uint256)"       # 0x095ea7b3
       cast sig "setApprovalForAll(address,bool)"# 0xa22cb465

2. Look up the selector across independent databases:

       cast 4byte 0x095ea7b3
       curl -s "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x095ea7b3" \
         | jq -r '.results[] | "\(.id) \(.text_signature)"'
       curl -s "https://api.openchain.xyz/signature-database/v1/lookup?function=0x095ea7b3" \
         | jq -r '.result.function."0x095ea7b3"[] | "\(.name) \(.filtered)"'

3. For events, the topic0 is the keccak of the full signature (256-bit, collision-free in
   practice) — compute rather than look up:

       cast keccak "Transfer(address,address,uint256)"
       # 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
       cast keccak "Approval(address,address,uint256)"

4. Confirm a candidate against the actual contract: the selector should appear in the deployed
   runtime code, and the verified ABI should list the function.

       cast selectors $(cast code $IMPL --rpc-url $ETH_RPC) | grep -i 095ea7b3
       curl -s "https://api.etherscan.io/v2/api?chainid=1&module=contract&action=getabi\
&address=$ADDR&apikey=$ETHERSCAN_API_KEY" | jq -r '.result' | \
         jq -r '.[] | select(.type=="function") | "\(.name)"' | grep -i approve

5. If several candidates survive, disambiguate by decoding the args and checking they make
   sense for the contract type (e.g. an `address,uint256` argument pair is consistent with a
   transfer-like call, not a `bytes32` key).

## Pitfalls

- Selector collisions are real: two different signatures can share the same 4 bytes. A DB can
  return multiple rows; do not pick the first without checking the contract's ABI.
- Public databases are writable and full of junk signatures added by spammers to confuse
  decoders. A hit is a hypothesis, not a fact.
- A proxy's fallback may route unknown selectors and never revert, so "the call succeeded"
  does not mean the selector is a real function.
- `personal_sign`/`eth_sign` payloads are not selectors; do not run a 4-byte lookup on a 65-byte
  signature.
- Event topic0 is 32 bytes, not 4; a 4-byte lookup on a topic0 yields nothing meaningful.

## Verification

    cast sig "approve(address,uint256)" | grep -qi 095ea7b3 && echo round-trip-ok
    cast selectors $(cast code $IMPL --rpc-url $ETH_RPC) | grep -qi 095ea7b3 && echo on-chain-ok

Report every candidate signature, its source (4byte/OpenChain/ABI), and which one you confirmed
against the deployed code.
