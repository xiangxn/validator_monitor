. ./scripts/env.sh
if [ -z "$SHOW_ADDRESS" ]; then
    $BINARY query tendermint-validator-set --node=$RPC_NODE --home $NODE_HOME | grep "$($BINARY tendermint show-address --home $NODE_HOME)"
else
    $BINARY query tendermint-validator-set --node=$RPC_NODE --home $NODE_HOME | grep "$SHOW_ADDRESS"
fi
