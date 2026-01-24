from web3 import Web3
import json
import time

# Connect to local Geth node
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Check connection
if not w3.is_connected():
    print("Failed to connect to the node.")
    exit()

# Specify the contract address (replace with your deployed contract address)
contract_address = '0xdB7d6AB1f17c6b31909aE466702703dAEf9269Cf'

# ABI for the deployed contract
contract_abi = json.loads('''[
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            }
        ],
        "name": "newRequest",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "requestId",
                "type": "uint256"
            }
        ],
        "name": "getRequestStatus",
        "outputs": [
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "requester",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "served",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "uint256",
                "name": "requestId",
                "type": "uint256"
            },
            {
                "indexed": true,
                "internalType": "string",
                "name": "message",
                "type": "string"
            }
        ],
        "name": "RequestCreated",
        "type": "event"
    }
]''')

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Event filter for RequestCreated Events
event_filter = contract.events.RequestCreated.create_filter(from_block='latest')

try:
    print("Listening for RequestCreated events...")
    while True:
        for event in event_filter.get_new_entries():
            request_id = event['args']['requestId']
            message = event['args']['message']
            print(f"New RequestCreated event: ID = {request_id}, Message = {message}")

        time.sleep(1)  # Delay to avoid overwhelming the node

except KeyboardInterrupt:
    print("Stopped listening.")
