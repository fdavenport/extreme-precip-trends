#!/bin/bash
#SBATCH --job-name=calc_pos_trends
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_pos_trends.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_pos_trends.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH -c 64
#SBATCH --time=10:00:00
#SBATCH -p dav_all

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

python -u ./calc_pos_trends.py 
