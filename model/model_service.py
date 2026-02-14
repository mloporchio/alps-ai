"""
This script is the main entry point for the nanoGPT model service.
It loads the model and provides a REST API for querying the model.

You can run it as:

$ python model_service.py

To send queries, you can use curl from the command line as follows:

curl -X POST "http://<hostname>:<port>/query" -d "text=Once%20upon%20a%20time" 

or 

curl -X GET "http://<hostname>:<port>/query?text=Once%20upon%20a%20time"

where <hostname> and <port> are the host and port of the model service.

Author: Matteo Loporchio
"""

from contextlib import nullcontext
from dattri.benchmark.models.nanoGPT.model import GPT, GPTConfig
from flask import Flask, request, Response
import configparser
import torch
import model_utils

CONFIG_FILE = 'model_service_config.ini'

# Read and parse the configuration file.
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
app_port = config['APPLICATION']['port']
app_host = config['APPLICATION']['host']
meta_path = config['MODEL']['meta_path']
checkpoint_path = config['MODEL']['checkpoint_path']
device = config['MODEL']['device']
block_size = int(config['MODEL']['block_size'])
seed = int(config['MODEL']['seed'])
num_samples = int(config['MODEL']['num_samples'])
max_new_tokens = int(config['MODEL']['max_new_tokens'])
temperature = float(config['MODEL']['temperature'])
top_k = int(config['MODEL']['top_k'])
#geth_port = int(config['DEFAULT']['geth_port'])
#aggregator_abi = config['DEFAULT']['aggregator_abi']
#aggregator_address = config['DEFAULT']['aggregator_address']
#bot_token = config['DEFAULT']['bot_token']
#provider = f'http://{geth_host}:{geth_port}'
ctx = nullcontext()
torch.manual_seed(seed)

# Initialize Flask app
app = Flask(__name__)
encode = None
decode = None
model = None
tasks = {}

# Load model once at startup
def load_model():
    global encode, decode, model
    encode_f, decode_f = model_utils.load_meta(meta_path)
    encode = encode_f
    decode = decode_f
    checkpoint = torch.load(checkpoint_path, map_location=device)
    gptconf = GPTConfig(**checkpoint['model_args'])
    model = GPT(gptconf)
    state_dict = checkpoint['model']
    unwanted_prefix = '_orig_mod.'
    for k,v in list(state_dict.items()):
        if k.startswith(unwanted_prefix):
            state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(device)

# Query the model
def query_model(query):
    start_ids = encode(query + " ")
    x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])
    with torch.no_grad():
        with ctx:
            y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
            return decode(y[0].tolist())

@app.route('/query', methods=['GET', 'POST'])
def query():
    # Get the string from query params (GET) or form data (POST)
    text = request.values.get('text', '')
    print(f"Received query: {text}")
    response = query_model(text)
    return response

if __name__ == '__main__':
    load_model()
    print("Model loaded and ready to serve requests.")
    app.run(debug=True, host=app_host, port=app_port)
