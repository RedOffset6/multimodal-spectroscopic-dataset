#!/bin/bash

#SBATCH --job-name=Alberts_test_BMORG
#SBATCH --partition=workq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64GB
#SBATCH --time=04:00:00
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

#onmt_translate -model=alberts_model/model_step_250000.pt -src=alberts_model/data/src-test.txt -output=alberts_model/data/prd-test.txt -beam_size=10 -n_best=10 -min_length=5 -gpu=0

onmt_translate -model=fn_1d_rounded/model_step_150000.pt -src=fn_1d_rounded/data/src-test.txt -output=fn_1d_rounded/data/prd-test.txt -beam_size=10 -n_best=10 -min_length=5 -gpu=0

echo "200 files"