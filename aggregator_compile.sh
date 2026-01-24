#!/bin/bash
#
# This script compiles the Aggregator smart contract using solc.
# Author: Matteo Loporchio
#

SOLC_PATH="./solc/solc-static-linux"
AGGREGATOR_CONTRACT="Aggregator.sol"
OUTPUT_DIR="./output"

# First, we check if compiler and contract files exist
if [ ! -f "$SOLC_PATH" ]; then
    echo "Error: solc binary not found at $SOLC_PATH."
    exit 1
fi

if [ ! -f "$AGGREGATOR_CONTRACT" ]; then
    echo "Error: Aggregator contract file not found at $AGGREGATOR_CONTRACT."
    exit 1
fi

# Then we compile the Aggregator contract
mkdir -p $OUTPUT_DIR
${SOLC_PATH} -o $OUTPUT_DIR --overwrite --bin --abi $AGGREGATOR_CONTRACT