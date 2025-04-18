#!/bin/bash
#SBATCH --job-name=rg_spear
#SBATCH --error=/davenport-scratch/fvdav22/job_output/regrid_spear.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/regrid_spear.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=40:00:00
#SBATCH -p dav_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends

pwd

eval "$(conda shell.bash hook)"
conda activate ./envs
conda env list

cd code

python -u ./regrid_spear.py 

