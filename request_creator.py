"""
Req
Author: Matteo Loporchio
"""

from web3 import Web3
import config
import json
import sys
import utils

# Function for creating and submitting a new request.
def create_request(contract_instance, user_account, message):
    tx_hash = contract_instance.functions.newRequest(message).transact({'from': user_account})
    return w3.eth.wait_for_transaction_receipt(tx_hash)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python request_creator.py <message>")
        sys.exit(1)

    # Read the command line arguments
    user_message = sys.argv[1]
    print(f"Creating request with message: {user_message}")

    # Read the aggregator contract address
    aggregator_address = Web3.to_checksum_address(utils.read_aggregator_address())

    # Connect to local Geth node
    w3 = Web3(Web3.HTTPProvider(config.GETH_PROVIDER))
    if not w3.is_connected():
        print("Error: failed to connect to the node.")
        sys.exit(1)

    # Create a contract instance
    contract_instance = w3.eth.contract(
        address = aggregator_address,
        abi = utils.load_abi("AGGREGATOR")
    )

    # Create a new request and submit it.
    tx_receipt = create_request(contract_instance, Web3.to_checksum_address(config.USER_ACCOUNT), user_message)
    print(f'Request created in transaction: {tx_receipt.transactionHash.hex()}')

    # Extract and print the new request ID
    count = contract_instance.functions.getRequestCount().call()
    print(f"There are currently {count} requests.")