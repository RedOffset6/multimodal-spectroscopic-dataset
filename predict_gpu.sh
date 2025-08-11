#!/bin/bash

#SBATCH --job-name=Alberts_test_BMORG
#SBATCH --account=CHEM014742
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64GB
#SBATCH --time=01:00:00
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

onmt_translate -model=alberts_model/model_step_250000.pt -src=alberts_model/data/src-test.txt -output=alberts_model/data/prd-test.txt -beam_size=10 -n_best=10 -min_length=5 -gpu=0

