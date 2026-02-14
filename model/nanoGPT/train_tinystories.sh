#!/bin/bash
#
#   This script trains a nanoGPT model on the custom Tiny Stories dataset.
#   Author: Matteo Loporchio
#

#python3 train.py config/train_tinystories.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=6000 --lr_decay_iters=6000 --dropout=0.0
python3 train.py config/train_tinystories.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=128 --batch_size=64 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=8000 --lr_decay_iters=8000 --dropout=0.0
#python3 train.py config/train_tinystories.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=128 --batch_size=64 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=6000 --lr_decay_iters=6000 --dropout=0.0