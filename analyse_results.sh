#!/bin/bash

#SBATCH --job-name=analyse_albt

#SBATCH --partition=workq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=16GB
#SBATCH --time=01:00:00

echo 'running predictions'

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

python benchmark/analyse_results.py --pred_path=fn_1d_rounded/data/prd-test.txt --test_path=fn_1d_rounded/data/tgt-test.txt

echo "8 files results"
