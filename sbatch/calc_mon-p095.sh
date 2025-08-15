#!/bin/bash
#SBATCH --job-name=calc_mon-p095
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_mon-p095_%a.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_mon-p095_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=4
#SBATCH --time=24:00:00
#SBATCH --array=0-60
#SBATCH -p all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs_pyqreg
cd code

start_year=$((SLURM_ARRAY_TASK_ID+1930))

for end_year in $(seq $((start_year + 30)) 2020); do
    
    python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="gpcc" --q=0.95
    python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="cmip-sub" --q=0.95
    python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="mesaclip" --q=0.95
    python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="spear" --q=0.95

    if [ "$start_year" -ge 1979 ]; then
       python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="gpcp" --q=0.95
       python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="mswep" --q=0.95
    fi
        
done




