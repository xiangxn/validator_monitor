. ./scripts/env.sh
$BINARY tx staking create-validator \
  --amount=1000000uatom \
  --pubkey=$($BINARY tendermint show-validator --home $NODE_HOME) \
  --moniker=$MONIKER \
  --chain-id=$CHAIN_ID \
  --commission-rate="1.00" \
  --commission-max-rate="1.00" \
  --commission-max-change-rate="1.00" \
  --min-self-delegation="1000000" \
  --gas="200000" \
  --gas-prices="0.0025uatom" \
  --from=$FROM_NAME \
  --home=$NODE_HOME \
  --node=$RPC_NODE
