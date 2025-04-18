#!/bin/bash
#SBATCH --job-name=obs_trends
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_obs_trends.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_obs_trends.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=40:00:00
#SBATCH -p dav+coe

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs_pyqreg
cd code


for start_year in {1930..1975..5}; do
   
    ## TRENDS FOR GPCC
    python -u ./calc_obs_trends.py --start=$start_year --end=$((start_year + 41)) --q=0.95 --dataset="gpcc" --freq="mon"
    python -u ./calc_obs_stats.py --start=$start_year --end=$((start_year + 41)) --dataset="gpcc" --freq="mon"

    # calculate trends through end date
    python -u ./calc_obs_trends.py --start=$start_year --end=2020 --q=0.95 --dataset="gpcc" --freq="mon"
    python -u ./calc_obs_stats.py --start=$start_year --end=2020 --dataset="gpcc" --freq="mon"
    
done

python -u ./calc_obs_trends.py --start=1979 --end=2020 --q=0.95 --dataset="gpcc" --freq="mon"
python -u ./calc_obs_stats.py --start=1979 --end=2020 --dataset="gpcc" --freq="mon"
#python -u ./calc_obs_trends.py --start=1979 --end=2020 --q=0.95 --dataset="gpcc_shift" --freq="mon"
#python -u ./calc_obs_stats.py --start=1979 --end=2020 --dataset="gpcc_shift" --freq="mon"

#python -u ./calc_obs_trends.py --start=1979 --end=2020 --q=0.95 --dataset="gpcp" --freq="mon"
#python -u ./calc_obs_stats.py --start=1979 --end=2020 --dataset="gpcp" --freq="mon"
#python -u ./calc_obs_trends.py --start=1979 --end=2020 --q=0.95 --dataset="mswep" --freq="mon"
#python -u ./calc_obs_stats.py --start=1979 --end=2020 --dataset="mswep" --freq="mon"

#python -u ./calc_obs_trends.py --start=1979 --end=2024 --q=0.95 --dataset="gpcp" --freq="mon"
#python -u ./calc_obs_stats.py --start=1979 --end=2024 --dataset="gpcp" --freq="mon"
#python -u ./calc_obs_trends.py --start=1979 --end=2024 --q=0.95 --dataset="mswep" --freq="mon"
#python -u ./calc_obs_stats.py --start=1979 --end=2024 --dataset="mswep" --freq="mon"

