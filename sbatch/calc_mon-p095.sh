#!/bin/bash
#SBATCH --job-name=calc_mon-p095
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_mon-p095.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_mon-p095.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=40:00:00
#SBATCH -p dav+coe


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

python -u ./calc_mon-p095.py --start=1979 --end=2020 --dataset="gpcc" -q=0.95




