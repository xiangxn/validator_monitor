. ./scripts/env.sh
# $BINARY query distribution commission $VALIDATOR -o json --node $RPC_NODE
$BINARY query distribution validator-outstanding-rewards $VALIDATOR -o json --node $RPC_NODE
# $BINARY query distribution rewards $VALIDATOR -o json --node $RPC_NODE