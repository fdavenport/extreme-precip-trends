#!/bin/bash
#SBATCH --job-name=summary
#SBATCH --error=/davenport-scratch/fvdav22/job_output/summary.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/summary.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH -c 64
#SBATCH --time=10:00:00
#SBATCH -p dav_all

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

python -u ./summarize_results.py 
