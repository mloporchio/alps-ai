from web3 import Web3
from solcx import compile_standard # Compile the Solidity contract
from pathlib import Path
import json

# Connect to local Geth node
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Check connection
if not w3.is_connected():
    print("Failed to connect to the node.")
    exit()

# Unlock your account (use the appropriate account)
account = w3.eth.accounts[0]  # Using the first account for this example
w3.eth.defaultAccount = account

print(account)

# Solidity contract source code
contract_source_code = Path('Aggregator.sol').read_text()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "Aggregator.sol": {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["*"]
            }
        }
    }
})

# Get the contract interface
contract_interface = compiled_sol['contracts']['Aggregator.sol']['Aggregator']

# Deploy the contract
Aggregator = w3.eth.contract(
    abi=contract_interface['abi'],
    bytecode=contract_interface['evm']['bytecode']['object']
)

# Create a transaction to deploy the contract
tx_hash = Aggregator.constructor().transact({'from': account})

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Print the contract address
print(f'Contract deployed at address: {tx_receipt.contractAddress}')

# Print the transaction receipt
print(tx_receipt)
