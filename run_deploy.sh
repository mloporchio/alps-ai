#!/bin/bash

OUTPUT_FILE="aggregator_address"

# First, compile the contract.
./aggregator_compile.sh

# Then deploy it and save the address to file.
python3 aggregator_deploy.py | cut -d':' -f2 | cut -d' ' -f2 > ${OUTPUT_FILE}