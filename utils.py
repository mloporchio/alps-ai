"""
Utility functions for loading contract ABIs and bytecodes.
Author: Matteo Loporchio
"""

import json
import config

# Load the ABI for a given contract
def load_abi(contract_name):
    if contract_name == "AGGREGATOR":
        contract_abi = None
        with open(config.AGGREGATOR_ABI, 'r') as abi_file:
            contract_abi = json.loads(abi_file.read())
        return contract_abi
    else:
        raise ValueError(f"Unknown contract name: {contract_name}")
    
# Load the bytecode for a given contract
def load_bytecode(contract_name):
    contract_bytecode = None
    if contract_name == "AGGREGATOR":
        with open(config.AGGREGATOR_BYTECODE, 'r') as bytecode_file:
            contract_bytecode = bytecode_file.read().strip()
        return contract_bytecode
    else:
        raise ValueError(f"Unknown contract name: {contract_name}")