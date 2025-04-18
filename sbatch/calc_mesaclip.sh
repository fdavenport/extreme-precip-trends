#!/bin/bash
#SBATCH --job-name=calc_mesaclip
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_mesaclip.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_mesaclip.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=40:00:00
#SBATCH -p dav_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs_pyqreg
cd code

for start_year in {1930..1975..5}; do
    # calculate 30-year trends
    python -u ./calc_mesaclip_trends.py --start=$start_year --end=$((start_year + 41)) --q=0.95 --freq="mon"
    python -u ./calc_mesaclip_stats.py --start=$start_year --end=$((start_year + 41)) --freq="mon"

    # calculate trends through end date
    python -u ./calc_mesaclip_trends.py --start=$start_year --end=2020 --q=0.95 --freq="mon"
    python -u ./calc_mesaclip_stats.py --start=$start_year --end=2020 --freq="mon"

done


python -u ./calc_mesaclip_trends.py --start=1979 --end=2020 --q=0.95 --freq="mon"
python -u ./calc_mesaclip_stats.py --start=1979 --end=2020 --freq="mon"

python -u ./calc_mesaclip_trends.py --start=1979 --end=2024 --q=0.95 --freq="mon"
python -u ./calc_mesaclip_stats.py --start=1979 --end=2024 --freq="mon"