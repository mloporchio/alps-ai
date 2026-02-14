"""
This script performs attribution on a nanoGPT model trained on the Tiny Stories dataset.
The input file is a contains the model output, and the script outputs a file containing the attribution scores.
Author: Matteo Loporchio
"""

import numpy as np
import os
import shutil
import sys
import time
import torch
import model_utils
from pathlib import Path
from torch.utils.data import  Dataset
from torch.utils.data import DataLoader
from dattri.algorithm.tracin import TracInAttributor
from dattri.benchmark.load import load_benchmark
from dattri.benchmark.models.nanoGPT.model import GPT, GPTConfig
from dattri.task import AttributionTask
from dattri.benchmark.datasets.shakespeare_char.data import CustomDataset

INPUT_FILE = sys.argv[1] # Contains the previously computed model output
OUTPUT_FILE = sys.argv[2] # Where the scores will be saved

TEMP_DIR = "./tmp"
META_PATH = "./nanoGPT/data/tinystories/meta.pkl"
data_path = Path("./nanoGPT/data/tinystories")
checkpoint_path = "./nanoGPT/out-tinystories/ckpt.pt" #"./nanoGPT/out-tinystories/ckpt_5750.pt"
device = "cpu"
block_size = 128
#checkpoint_list = [f"./nanoGPT/out-tinystories/ckpt_{i}.pt" for i in range(250, 5750+250, 250)]
ensemble = 1 #len(checkpoint_list)

# def checkpoints_load_func(model, checkpoint):
#     checkpoint = torch.load(checkpoint_path, map_location=device)
#     model_args = checkpoint["model_args"]
#     gptconf = GPTConfig(**model_args)
#     model = GPT(gptconf)
#     model.to(device)
#     model.eval()
#     return model

os.makedirs(TEMP_DIR, exist_ok=True)

print("Loading train and test datasets...")
start_time = time.time()
# Load training dataset.
train_data = np.memmap(os.path.join(data_path, 'train.bin'), dtype=np.uint16, mode='r')
train_dataset = CustomDataset(train_data, block_size)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=False)
# Load model output as test dataset.
encode, decode = model_utils.load_meta(META_PATH)
model_utils.convert(encode, INPUT_FILE, os.path.join(TEMP_DIR, 'val.bin'))
val_data = np.memmap(os.path.join(TEMP_DIR, 'val.bin'), dtype=np.uint16, mode='r')
val_dataset = CustomDataset(val_data, block_size)
val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

print(f"Train size: {len(train_data):,}\nTest size: {len(val_data):,}")
elapsed = time.time() - start_time
print(f"Done. Took {elapsed:.3f} seconds.")

print("Loading model...")
start_time = time.time()
checkpoint = torch.load(checkpoint_path, map_location=device)
model_args = checkpoint["model_args"]
print(model_args)
gptconf = GPTConfig(**model_args)
model = GPT(gptconf)
model.to(device)
model.eval()
elapsed = time.time() - start_time
print(f"Done. Took {elapsed:.3f} seconds.")

print("Performing training data attribution...")
start_time = time.time()

def loss_tracin(params, data_target_pair):
    x, y = data_target_pair
    x_t = x.unsqueeze(0)
    y_t = y.unsqueeze(0)
    _, loss = torch.func.functional_call(model, params, (x_t, y_t))
    return loss

task = AttributionTask(
    model=model,
    loss_func=loss_tracin,
    checkpoints=model.state_dict() #checkpoint_list
    #checkpoints_load_func=checkpoints_load_func,
)

attributor = TracInAttributor(
    task=task,
    weight_list=torch.ones(ensemble) * 1e-3,
    normalized_grad=False,
    device=device
)

with torch.no_grad():
    score = attributor.attribute(train_loader, val_loader)
    np.savetxt(OUTPUT_FILE, score.numpy())
elapsed = time.time() - start_time

print(f"Done. Took {elapsed:.3f} seconds.")
shutil.rmtree(TEMP_DIR)  # Remove temporary directory
