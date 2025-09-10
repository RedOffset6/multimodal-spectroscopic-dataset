#!/bin/bash

#SBATCH --job-name=vanila_Train_BMORG
#SBATCH --account=CHEM014742
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64GB
#SBATCH --time=7-00:00:00
#SBATCH --gres=gpu:1
echo 'training the neural network'

#gpu_veryshort appears to no longer exist
#hostname
#previously the queue was gpu_veryshort
#account CHEM014742
#module load languages/miniconda
#module load libs/cuda/12.0.0-gcc-9.1.0
module load cuda/12.4.0-z7k5

echo "before activation: $(which python)"

source ~/initMamba.sh
mamba activate multispecdata
echo "after activation: $(which python)"

python benchmark/start_training.py --output_path=1d_only_no_formula
