#!/bin/bash
#SBATCH --job-name=rg_cmip_day
#SBATCH --error=/davenport-scratch/fvdav22/job_output/regrid_cmip_day_%a.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/regrid_cmip_day_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --cpus-per-task=4
#SBATCH --time=20:00:00
#SBATCH --array=1-54%10
#SBATCH -p dav+coe


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends

pwd

eval "$(conda shell.bash hook)"
conda activate ./envs
conda env list

histpath="/davenport-scratch/DATA/CMIP6/raw_data/historical/day/pr"

cd $histpath
## read in list of model names and select current model based on Task ID
modelname=$(ls pr_* | cut -d"_" -f3 | uniq | head -n $SLURM_ARRAY_TASK_ID | tail -n1)
## read in list of files for current model

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends/code

python -u ./regrid_cmip.py --freq="day" --var="pr" --model=$modelname


