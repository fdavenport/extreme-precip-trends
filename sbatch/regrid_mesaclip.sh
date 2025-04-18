#!/bin/bash
#SBATCH --job-name=rg_mesaclip
#SBATCH --error=/davenport-scratch/fvdav22/job_output/regrid_mesaclip.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/regrid_mesaclip.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=64
#SBATCH --time=40:00:00
#SBATCH -p dav+coe


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends

pwd

eval "$(conda shell.bash hook)"
conda activate ./envs
conda env list

cd code

python -u ./regrid_mesaclip.py

