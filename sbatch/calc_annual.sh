#!/bin/bash
#SBATCH --job-name=calc_annual
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_annual.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_annual.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=40:00:00
#SBATCH -p dav_all

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends

eval "$(conda shell.bash hook)"
conda activate ./envs

cd code

for start_year in {1930..1980..5}; do
python -u ./calc_annual.py --start=$start_year --end=$((start_year + 39))
python -u ./calc_annual.py --start=$start_year --end=2020
done

python -u ./calc_annual.py --start=1979 --end=2020
python -u ./calc_annual.py --start=1979 --end=2024