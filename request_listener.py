"""
Docstring per request_listener
Author: Matteo Loporchio
"""

from web3 import Web3
import config
import sys
import time
import utils

if __name__ == "__main__":

    # Read the aggregator contract address
    aggregator_address = Web3.to_checksum_address(utils.read_aggregator_address())

    # Connect to local Geth node
    w3 = Web3(Web3.HTTPProvider(config.GETH_PROVIDER))
    if not w3.is_connected():
        print("Error: failed to connect to the node.")
        sys.exit(1)

    # Load the contract ABI
    contract_abi = utils.load_abi("AGGREGATOR")

    # Create a contract instance
    contract_instance = w3.eth.contract(
        address=aggregator_address, 
        abi=contract_abi
    )

    # Event filter for RequestCreated Events
    event_filter = contract_instance.events.RequestCreated.create_filter(from_block='latest')

    # Listen for events indefinitely
    try:
        print("Listening for RequestCreated events...")
        while True:
            for event in event_filter.get_new_entries():
                request_id = event['args']['requestId']
                requester = event['args']['requester']
                messageHash = event['args']['messageHash']
                print(f"New RequestCreated event: ID = {request_id}, Requester = {requester}, MessageHash = {messageHash.hex()}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("CTRL+C pressed: stopped listening.")
