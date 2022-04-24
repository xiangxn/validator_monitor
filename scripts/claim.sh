. ./scripts/env.sh
$BINARY tx distribution withdraw-all-rewards --from testmain --home $NODE_HOME --node $NODE_TCP --yes --fees "500uatom" && \
$BINARY tx distribution withdraw-rewards $VALIDATOR --from testmain --home $NODE_HOME --node $NODE_TCP --yes --fees "500uatom" --commission
