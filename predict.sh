#!/bin/bash

#SBATCH --job-name=ALBERTS_BMORG
#SBATCH --account=CHEM014742
#SBATCH --partition=veryshort
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

source ~/initMamba.sh
mamba activate multispecdata
echo "after activation: $(which python)"

#python benchmark/generate_input.py --analytical_data=data --out_path=alberts_model --h_nmr --c_nmr --formula

onmt_translate -model=model_inputs/model_step_20000.pt -src=model_inputs/data/src-test.txt -output=model_inputs/data/prd-test.txt -beam_size=10 -n_best=10 -min_length=5 -gpu=0
