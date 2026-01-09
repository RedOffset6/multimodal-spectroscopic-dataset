#!/bin/bash

#SBATCH --job-name=imp_run
#SBATCH --partition=workq
#SBATCH --ntasks=1               
#SBATCH --cpus-per-task=1          
#SBATCH --mem=400GB
#SBATCH --time=0-24:00:00
echo 'training the neural network'

#SUBMIT FOR FOUR HOURS TO COMPLETELY COMPUTE THE DATA

#gpu_veryshort appears to no longer exist
#hostname
#previously the queue was gpu_veryshort
#account CHEM014742
#module load languages/miniconda
#module load libs/cuda/12.0.0-gcc-9.1.0
#module load cuda/12.4.0-z7k5

# Load Cray programming environment and MPI
module load PrgEnv-cray/8.6.0
module load craype-network-ofi
module load cray-mpich

# Activate your conda environmentß
source ~/miniforge3/bin/activate
conda activate mpi_env

# Reinstall mpi4py from source to link to Cray MPI
pip uninstall -y mpi4py
MPICC=cc pip install --no-binary=mpi4py mpi4py

echo "after activation: $(which python)"



# Run MPI script on 72 processes
srun -n 1 python generate_2d_expts.py