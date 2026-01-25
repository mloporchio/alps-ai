"""
Dummy Attributor Script
This script listens for RequestCreated events from an Aggregator contract,
performs a dummy attribution by generating random values, and submits the
results back to the contract.

Author: Matteo Loporchio
"""

from web3 import Web3
import config
import sys
import time
import utils
import numpy as np

def attribute():
    size = 1000
    top_n = 10
    mu, sigma = 3., 1.  # mean and standard deviation
    values = np.random.lognormal(mu, sigma, size).tolist() # Generate dummy attribution values
    attribution = list(zip(range(0, size), values))
    attribution_s = sorted(attribution, key=lambda x: x[1], reverse=True) # Sort by balance descending
    attribution_t = list(map(lambda z: (z[0], round(z[1])), attribution_s[:top_n])) # Take top n and round balances
    return attribution_t

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dummy_attributor.py <aggregator_address>")
        sys.exit(1)

    # Read the command line arguments
    aggregator_address = Web3.to_checksum_address(sys.argv[1])

    # Connect to local Geth node
    w3 = Web3(Web3.HTTPProvider(config.GETH_PROVIDER))
    if not w3.is_connected():
        print("Error: failed to connect to the node.")
        sys.exit(1)
    print("Connected to the node.")

    # Get gas price and limit
    gas_price = w3.eth.gas_price
    latest_block = w3.eth.get_block("latest")
    gas_limit = latest_block["gasLimit"]
    print(f"Using gas price: {w3.from_wei(gas_price, 'gwei')} gwei, gas limit: {gas_limit}")

    # Load the contract ABI
    contract_abi = utils.load_abi("AGGREGATOR")

    # Create a contract instance
    contract_instance = w3.eth.contract(
        address=aggregator_address, 
        abi=contract_abi
    )

    # Event filter for RequestCreated and RequestServed events
    request_created_filter = contract_instance.events.RequestCreated.create_filter(from_block='latest')
    request_served_filter = contract_instance.events.RequestServed.create_filter(from_block='latest')

    # Listen for events indefinitely
    try:
        print("Listening for RequestCreated events...")
        while True:
            for event in request_created_filter.get_new_entries():
                request_id = event['args']['requestId']
                requester = event['args']['requester']
                messageHash = event['args']['messageHash']
                print(f"New RequestCreated event: ID = {request_id}, Requester = {requester}, MessageHash = {messageHash.hex()}")
                # Perform attribution
                attribution_result = attribute()
                # Submit the attribution result
                tx_hash = contract_instance.functions.serveRequest(request_id, attribution_result).transact({
                    'from': Web3.to_checksum_address(config.ATTRIBUTOR_ACCOUNT)
                    #'gas': gas_limit,
                    #'gasPrice': w3.to_wei(gas_price, 'gwei')
                })
                print(f"Submitted attribution for Request ID {request_id}, Transaction Hash: {tx_hash.hex()}")
            
            for event in request_served_filter.get_new_entries():
                request_id = event['args']['requestId']
                print(f"New RequestServed event: {request_id}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("CTRL+C pressed: stopped listening.")
