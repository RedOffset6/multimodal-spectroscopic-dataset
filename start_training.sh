#!/bin/bash

#SBATCH --job-name=vanila_Train_BMORG
#SBATCH --partition=workq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64GB
#SBATCH --time=1-00:00:00
#SBATCH --gres=gpu:1
echo 'training the neural network'

#gpu_veryshort appears to no longer exist
#hostname
#previously the queue was gpu_veryshort
#account CHEM014742
#module load languages/miniconda
#module load libs/cuda/12.0.0-gcc-9.1.0
module load cuda/12.6

echo "before activation: $(which python)"

source ~/miniforge3/bin/activate
conda activate multispecdata
echo "after activation: $(which python)"

python benchmark/start_training.py --output_path=test
