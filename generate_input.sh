#!/bin/bash

#SBATCH --job-name=ALBERTS_BMORG
#SBATCH --account=CHEM014742
#SBATCH --partition=veryshort
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16GB
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

source ~/initMamba.sh
mamba activate multispecdata
echo "after activation: $(which python)"

python benchmark/generate_input.py --analytical_data=data --out_path=model_inputs --h_nmr --c_nmr
