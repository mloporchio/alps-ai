# ALPS-AI

This project implements a decentralized AI model training data attribution system using blockchain technology. 

## Technologies used

The project uses the following languages and technologies:

- Python
- Solidity
- Bash
- Web3.py
- geth
- solc
- ...

## Aggregator Contract

The Aggregator contract is a Solidity smart contract that manages requests for data attribution and stores the results submitted by attributors.

## Scripts

- `request_client.py`: A client script that allows users to interact with the model and create new requests to the Aggregator contract.

- `dummy_attributor.py`: A dummy attributor that listens for `RequestCreated` events from the Aggregator contract, performs a dummy attribution by generating random values, and submits the results back to the contract.

- ...