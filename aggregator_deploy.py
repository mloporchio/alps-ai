"""
Docstring per aggregator_deploy
Author: Matteo Loporchio
"""

from web3 import Web3
from pathlib import Path
import config
import sys
import utils

if __name__ == "__main__":
    # Connect to local Geth node
    w3 = Web3(Web3.HTTPProvider(config.GETH_PROVIDER))
    if not w3.is_connected():
        print("Error: failed to connect to the node.")
        sys.exit(1)

    # Set account
    account = w3.eth.accounts[0] #config.USER_ACCOUNT 
    w3.eth.defaultAccount = account

    # Deploy the Aggregator contract
    Aggregator = w3.eth.contract(
        abi = utils.load_abi("AGGREGATOR"),
        bytecode = utils.load_bytecode("AGGREGATOR")
    )
    tx_hash = Aggregator.constructor().transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Contract deployed at address: {tx_receipt.contractAddress}') # Print the contract address