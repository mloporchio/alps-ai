"""
Request Client Script
This script allows users to interact with the model and 
create new requests to the Aggregator contract

Author: Matteo Loporchio
"""

from web3 import Web3
import config
import requests
import sys
import utils

# Function for creating and submitting a new request.
def create_request(contract_instance, user_account, message):
    tx_hash = contract_instance.functions.newRequest(message).transact({'from': user_account})
    return w3.eth.wait_for_transaction_receipt(tx_hash)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python request_creator.py <aggregator_address>")
        sys.exit(1)
    aggregator_address = sys.argv[1]

    # Read the command line arguments
    aggregator_address = Web3.to_checksum_address(sys.argv[1])

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
    
    # Loop for sending requests to the model endpoint.
    while True:
        try:
            # Get user input
            print("Enter your message (or Ctrl+C to exit):")
            user_input = input("> ")
            if not user_input:
                continue

            # Send request to the model endpoint
            response = requests.post(
                config.MODEL_ENDPOINT,
                json={"text": user_input},
                timeout=10
            )

            # Read response and check for HTTP errors
            response.raise_for_status()
            if response.status_code != 200:
                print(f"Error: received status code {response.status_code}")
                continue

            # Print the model response to stdout.
            print(response.text)
            print("")

            # Create a new request and submit it.
            tx_receipt = create_request(contract_instance, Web3.to_checksum_address(config.USER_ACCOUNT), user_input)
            print(f'Request created in transaction: {tx_receipt.transactionHash.hex()}')

            # Extract and print the new request ID
            count = contract_instance.functions.getRequestCount().call()
            print(f"There are currently {count} requests.")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except requests.RequestException as e:
            print(f"Request error: {e}")
