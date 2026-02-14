# ALPS-AI

This project implements a decentralized AI model training data attribution system using blockchain technology. 
The project is supported by the Ethereum Foundation Academic Grant titled *"A Fair and Trustworthy Remuneration Framework for AI Model Training using Ethereum"* (id: FY25-2125).

## Technologies used

The project uses the following languages and technologies:

- Python
- Solidity
- Bash
- geth
- solc
- ...

## AI model and attribution method

The project relies on the nanoGPT (https://github.com/karpathy/nanoGPT) model and utilizes dattri (https://github.com/trais-lab/dattri) as a library for data attribution methods. The model has been trained using (a subset of) the TinyStories (https://huggingface.co/datasets/roneneldan/TinyStories) dataset.

## Aggregator Contract

The Aggregator contract is a Solidity smart contract that manages requests for data attribution and stores the results submitted by attributors.

## Scripts

- `request_client.py`: A client script that allows users to interact with the model and create new requests to the Aggregator contract.

- `dummy_attributor.py`: A dummy attributor that listens for `RequestCreated` events from the Aggregator contract, performs a dummy attribution by generating random values, and submits the results back to the contract.

- `model/model_attributor.py`: This script can be used for computing the data attribution result for a given model output. The script takes a file containing the model output as input, and outputs a text file containing the data attribution scores.

- `model/model_service.py`: This script can be used for running the model as a service. It loads the model and provides a REST API for querying the model.