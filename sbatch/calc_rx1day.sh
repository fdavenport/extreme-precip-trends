#!/bin/bash
#SBATCH --job-name=calc_rx1day
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_rx1day.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_rx1day.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=16
#SBATCH --time=40:00:00
#SBATCH -p dav+coe


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

for start_year in {1950..1975..5}; do

    # calculate trends through 2016 for all models and REGEN
    #python -u ./calc_rx1day.py --start=$start_year --end=2016 --dataset="regen"
    #python -u ./calc_rx1day.py --start=$start_year --end=2016 --dataset="cmip"
    #python -u ./calc_rx1day.py --start=$start_year --end=2016 --dataset="highres_cmip"
    #python -u ./calc_rx1day.py --start=$start_year --end=2016 --dataset="mesaclip"
    #python -u ./calc_rx1day.py --start=$start_year --end=2016 --dataset="spear"
    
    if [ "$start_year" -lt 1975 ]; then
        # calculate 45-year trends
        #python -u ./calc_rx1day.py --start=$start_year --end=$((start_year + 41)) --dataset="regen"
        #python -u ./calc_rx1day.py --start=$start_year --end=$((start_year + 41)) --dataset="cmip"
        #python -u ./calc_rx1day.py --start=$start_year --end=$((start_year + 41)) --dataset="highres_cmip"
        #python -u ./calc_rx1day.py --start=$start_year --end=$((start_year + 41)) --dataset="mesaclip"
        #python -u ./calc_rx1day.py --start=$start_year --end=$((start_year + 41)) --dataset="spear"
    fi

done

python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="regen"
python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="cpc"
python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="cpc_shift"
python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="mswep"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="highres_cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="mesaclip"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="spear"

python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="cpc"
python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="cpc_shift"
python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="mswep"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="highres_cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="mesaclip"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="spear"

python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="cpc"
python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="cpc_shift"
python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="mswep"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="highres_cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="mesaclip"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="spear"


