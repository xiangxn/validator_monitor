. ./scripts/env.sh
$BINARY tx staking edit-validator \
  --moniker=$MONIKER \
  --website="https://nutbox.io/" \
  --identity=E711E530899015DC \
  --security-contact="contact@nutbox.io" \
  --details="A multi-chain staking protocol and staking-based DAO creation platform." \
  --chain-id=$CHAIN_ID \
  --gas="200000" \
  --gas-prices="0.0025uatom" \
  --from=$FROM_NAME \
  --home=$NODE_HOME \
  --node=$RPC_NODE
