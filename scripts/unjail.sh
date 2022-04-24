. ./scripts/env.sh
$BINARY tx slashing unjail \
    --from=$FROM_NAME \
    --chain-id=$CHAIN_ID \
    --node=$RPC_NODE \
    --home=$NODE_HOME \
    --fees=500uatom

