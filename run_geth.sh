#!/bin/bash

GETH_PATH="./geth/geth"
HTTP_ADDR="127.0.0.1"
HTTP_PORT="8545"

if [ ! -f "$GETH_PATH" ]; then
    echo "Error: geth binary not found at $GETH_PATH."
    exit 1
fi

# Start geth with specified options
${GETH_PATH} --dev --http --http.api eth,net,web3,personal --http.addr ${HTTP_ADDR} --http.port ${HTTP_PORT} console