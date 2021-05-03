# Step 3.
# Matrix Reordering using CPU
# push high values to the diagonal line
"""
while True:
    random i and j
    if swap i and j is good:
        swap
"""

import os, argparse
import numpy as np
from tools.core import loss_cpu, loss_gradient_if_swap
from tools.images import save_pic
import wandb

def search(matrix, indices, seed=0, total_steps=100, num_save=10):
    l = matrix.shape[0]
    np.random.seed(seed)
    for step in range(total_steps):
        i,j = int(np.random.random() * l), int(np.random.random() * l)
        if i==j:
            continue
        if loss_gradient_if_swap(matrix, i, j)>0:
            # swap
            _tmp = matrix[i,:].copy()
            matrix[i,:] = matrix[j,:]
            matrix[j,:] = _tmp
            
            _tmp = matrix[:,i].copy()
            matrix[:,i] = matrix[:,j]
            matrix[:,j] = _tmp

            _tmp = indices[i]
            indices[i] = indices[j]
            indices[j] = _tmp
        
        if (step-1)%(total_steps//num_save)==0:
            loss_LA = loss_cpu(matrix)
            record= {"step": step, "loss": loss_LA}
            wandb.log(record)
            print(record)
            save_pic(matrix, indices, f"tmp/minLA_cpu/seed_{args.seed}_step_{step:06}")

    return matrix, indices

def step3(args):
    os.makedirs("tmp/minLA_cpu", exist_ok=True)

    matrix = np.load("data/matrix.npy")
    np.random.seed(args.seed)
    indices = np.arange(matrix.shape[0])
    # random initial state
    np.random.shuffle(indices)
    matrix = matrix[indices, :]
    matrix = matrix[:, indices]
    save_pic(matrix, indices, f"tmp/minLA_cpu/seed_{args.seed}_start")
    # record loss for initial state
    loss_LA = loss_cpu(matrix)
    print(f"After initialization, loss LA = {loss_LA}")

    # Optimization will take about 2 mins
    print(f"Optimization start.")
    matrix, indices = search(matrix, indices, seed=args.seed, total_steps=args.num_steps)

    loss_LA = loss_cpu(matrix)
    print(f"After optimization, loss LA = {loss_LA}")
    save_pic(matrix, indices, f"tmp/minLA_cpu/seed_{args.seed}_end")


if __name__=="__main__":

    wandb.init(project="arxiv_4422")

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_steps", type=float, default=5e5, help="")
    parser.add_argument("--seed", type=int, default=0, help="random seed")
    parser.add_argument("--tag", type=str, default="cpu")
    parser.add_argument("--exp_name", type=str)
    args = parser.parse_args()
    args.num_steps = int(args.num_steps)
    wandb.config.update(args)

    step3(args)