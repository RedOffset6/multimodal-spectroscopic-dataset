#!/bin/bash

#SBATCH --job-name=imp_run
#SBATCH --account=CHEM014742
#SBATCH --partition=cpu
#SBATCH --ntasks=1               
#SBATCH --cpus-per-task=1          
#SBATCH --mem=32GB
#SBATCH --time=1-00:00:00
#SBATCH --array=000-244
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
mamba activate imp_env
echo "after activation: $(which python)"

python run_impression.py ${SLURM_ARRAY_TASK_ID}
