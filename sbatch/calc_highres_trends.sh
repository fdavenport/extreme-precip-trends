#!/bin/bash
#SBATCH --job-name=highres_trends
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_highres_trends.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_highres_trends.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=20:00:00
#SBATCH -p dav_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs_pyqreg
cd code

for start_year in {1950..1975..5}; do
   
    python -u ./calc_cmip_trends.py --start=$start_year --end=$((start_year + 41)) --q=0.95 --freq="mon" --res="highres"
    python -u ./calc_cmip_stats.py --start=$start_year --end=$((start_year + 41)) --freq="mon" --res="highres"
    
    # calculate trends through end date
    python -u ./calc_cmip_trends.py --start=$start_year --end=2020 --q=0.95 --freq="mon" --res="highres"
    python -u ./calc_cmip_stats.py --start=$start_year --end=2020 --freq="mon" --res="highres"

done


python -u ./calc_cmip_trends.py --start=1979 --end=2020 --q=0.95 --freq="mon" --res="highres"
python -u ./calc_cmip_stats.py --start=1979 --end=2020 --freq="mon" --res="highres"

python -u ./calc_cmip_trends.py --start=1979 --end=2024 --q=0.95 --freq="mon" --res="highres"
python -u ./calc_cmip_stats.py --start=1979 --end=2024 --freq="mon" --res="highres"