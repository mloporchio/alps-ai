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
user_account = '0x71562b71999873DB5b286dF957af199Ec94617F7'

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

# Create a new request
def create_request(message):
    # Call the newRequest function
    tx_hash = contract.functions.newRequest(message).transact({'from': user_account})

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Print the transaction receipt
    print(f'Transaction successful with hash: {tx_receipt.transactionHash.hex()}')

    # Extract and print the new request ID
    request_id = contract.events.RequestCreated().process_receipt(tx_receipt)[0]['args']['requestId']
    print(f'New Request ID assigned: {request_id}')

# Execute the function to create a request
num_requests = 60
for i in range(0, num_requests):
    message = f"Hello world! (seq: {i})"
    create_request(message)
    time.sleep(2) # wait for two seconds
