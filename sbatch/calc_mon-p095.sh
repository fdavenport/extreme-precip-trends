#!/bin/bash
#SBATCH --job-name=calc_mon-p095
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_mon-p095.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_mon-p095.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=32
#SBATCH --time=40:00:00
#SBATCH -p dav_all,coe_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs_pyqreg
cd code

for start_year in $(seq 1930 1990); do
    for end_year in $(seq $((start_year + 30)) 2020); do
    
        python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="gpcc" --q=0.95
        python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="cmip" --q=0.95
        python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="mesaclip" --q=0.95
        python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="spear" --q=0.95

        if [ "$start_year" -ge 1979]; then
           python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="gpcp"
           python -u ./calc_mon-p095.py --start=$start_year --end=$end_year --dataset="mswep"
        fi
        
    done
done




