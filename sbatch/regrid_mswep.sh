#!/bin/bash
#SBATCH --job-name=rg_mswep
#SBATCH --error=/davenport-scratch/fvdav22/job_output/regrid_mswep_%a.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/regrid_mswep_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --cpus-per-task=8
#SBATCH --array=0-45%5
#SBATCH --time=40:00:00
#SBATCH -p dav+coe


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends

pwd

eval "$(conda shell.bash hook)"
conda activate ./envs
conda env list

cd code

YEAR=$(($SLURM_ARRAY_TASK_ID+1979))

python -u ./regrid_mswep.py --freq="mon" --year=$YEAR --overwrite

python -u ./regrid_mswep.py --freq="day" --year=$YEAR --overwrite

