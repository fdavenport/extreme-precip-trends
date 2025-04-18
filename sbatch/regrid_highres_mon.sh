#!/bin/bash
#SBATCH --job-name=rg_highres_mon
#SBATCH --error=/davenport-scratch/fvdav22/job_output/regrid_highres_mon_%a.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/regrid_highres_mon_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --cpus-per-task=4
#SBATCH --time=10:00:00
#SBATCH --array=1-20%10
#SBATCH -p dav_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends

pwd

eval "$(conda shell.bash hook)"
conda activate ./envs
conda env list

histpath="/davenport-scratch/DATA/CMIP6/raw_data/hist-1950/mon/pr"

cd $histpath
## read in list of model names and select current model based on Task ID
modelname=$(ls pr_* | cut -d"_" -f3 | uniq | head -n $SLURM_ARRAY_TASK_ID | tail -n1)
## read in list of files for current model

echo $modelname 

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends/code

python -u ./regrid_highres_cmip.py --freq="mon" --var="pr" --model=$modelname --overwrite


