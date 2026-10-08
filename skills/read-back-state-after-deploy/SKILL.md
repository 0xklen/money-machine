---
name: read-back-state-after-deploy
description: Use when you just broadcast a contract deploy or upgrade and must prove on-chain that it actually landed and is initialised correctly.
---

# Read back state after a deploy

A broadcast is a request, not a result. Confirm the receipt succeeded, the code is present,
the constructor ran with the values you sent, and record the block you can reproduce from.

## Procedure

1. Capture the tx hash from the broadcast artifact (Foundry writes it).

       TX=$(jq -r '.transactions[0].hash' \
             broadcast/Deploy.s.sol/1/run-latest.json)
       ADDR=$(jq -r '.transactions[0].contractAddress' \
             broadcast/Deploy.s.sol/1/run-latest.json)

2. Check the receipt status and that it was mined. `status` is `0x1` on success, `0x0` on
   revert (gas still spent).

       cast receipt $TX --rpc-url $ETH_RPC --json \
         | jq -r '{status, blockNumber, contractAddress, gasUsed}'
       cast receipt $TX --rpc-url $ETH_RPC | grep -i 'status'

3. Confirm code exists at the address (a self-destructed or mis-deployed contract reads `0x`).

       cast code $ADDR --rpc-url $ETH_RPC | wc -c        # must be > 2
       cast codesize $ADDR --rpc-url $ETH_RPC            # runtime size in bytes

4. Re-read every value the constructor set and compare against the deployment inputs.

       cast call $ADDR "owner()(address)"   --rpc-url $ETH_RPC
       cast call $ADDR "paused()(bool)"     --rpc-url $ETH_RPC
       # for a token: name/symbol/decimals/totalSupply

5. For a proxy deploy, verify the implementation slot and that `initialize()` ran exactly
   once (a second call must revert).

       cast call $ADDR "implementation()(address)" --rpc-url $ETH_RPC 2>/dev/null \
         || cast storage $ADDR \
            0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc \
            --rpc-url $ETH_RPC

6. Pin the block number in your records so later checks read the same state:

       cast block-number --rpc-url $ETH_RPC

## Pitfalls

- `status == 0x1` does not mean your logic succeeded: a proxy `delegatecall` inside a
  `try/catch`, or an ignored low-level call, can revert without failing the outer tx.
- `--rpc-url` defaults are easy to get wrong; an env var left unset can broadcast to the
  wrong chain. Re-check `cast chain-id --rpc-url $ETH_RPC` before and after.
- One confirmation is not finality. On mainnet wait ~12 blocks; on L2s wait for the
  `safe`/`finalized` head, not `latest`.
- The `contractAddress` in `run-latest.json` for a CREATE2 deploy is the *predicted* address;
  if the salt was reused the actual address differs — trust `receipt.contractAddress`.
- Skipping the initialize check leaves a proxy pointing at an uninitialised implementation,
  which anyone can then initialise and take over.

## Verification

    cast receipt $TX --rpc-url $ETH_RPC --json | jq -r .status     # 0x1
    cast code $ADDR --rpc-url $ETH_RPC | wc -c                     # > 2
    cast call $ADDR "owner()(address)" --rpc-url $ETH_RPC          # == deployer

Report the tx hash, block number, runtime code size, and the read-back values that match the
deployment inputs.
