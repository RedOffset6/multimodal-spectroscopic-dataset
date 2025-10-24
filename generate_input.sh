#!/bin/bash

#SBATCH --job-name=Generate_Input
#SBATCH --partition=workq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64GB
#SBATCH --time=03:00:00

echo 'training the neural network'

#gpu_veryshort appears to no longer exist
#hostname
#previously the queue was gpu_veryshort
#account CHEM014742
#module load languages/miniconda
#module load libs/cuda/12.0.0-gcc-9.1.0
#module load cuda/12.4.0-z7k5

echo "before activation: $(which python)"

source ~/miniforge3/bin/activate
conda activate multispecdata
echo "after activation: $(which python)"

python benchmark/generate_input.py --analytical_data=data_imp_2d --out_path=test --formula --c_nmr --h_nmr --cosy --hsqc --hmbc