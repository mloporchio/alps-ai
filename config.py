#
#   Configuration file for Ethereum connection and contract details.
#   Author: Matteo Loporchio
#

GETH_HOST = 'localhost'
GETH_PORT = 8545
GETH_PROVIDER = f'http://{GETH_HOST}:{GETH_PORT}'

USER_ACCOUNT = '0x71562b71999873db5b286df957af199ec94617f7'
ATTRIBUTOR_ACCOUNT = '0x71562b71999873db5b286df957af199ec94617f7'

CONTRACT_OUTPUT_DIR = 'output'
AGGREGATOR_ABI = f'{CONTRACT_OUTPUT_DIR}/Aggregator.abi'
AGGREGATOR_BYTECODE = f'{CONTRACT_OUTPUT_DIR}/Aggregator.bin'
AGGREGATOR_ACCOUNT_FILE = "aggregator_address"

MODEL_HOST = 'localhost'
MODEL_PORT = 50100
MODEL_ENDPOINT = f'http://{MODEL_HOST}:{MODEL_PORT}/query'