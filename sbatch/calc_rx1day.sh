#!/bin/bash
#SBATCH --job-name=calc_rx1day
#SBATCH --error=/davenport-scratch/fvdav22/job_output/calc_rx1day.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/calc_rx1day.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=32
#SBATCH --time=40:00:00
#SBATCH -p dav_all,coe_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

#for start_year in {1950..1975..5}; do

for start_year in $(seq 1950 1990); do
    for end_year in $(seq $((start_year + 30)) 2020); do
    
        # calculate trends through 2016 for all models and REGEN
        python -u ./calc_rx1day.py --start=$start_year --end=$end_year --dataset="cmip"
        python -u ./calc_rx1day.py --start=$start_year --end=$end_year --dataset="mesaclip"
        python -u ./calc_rx1day.py --start=$start_year --end=$end_year --dataset="spear"
    
    if [ "$end_year" -le 2016]; then
       python -u ./calc_rx1day.py --start=$start_year --end=$end_year --dataset="regen"
    fi
    
    if [ "$start_year" -ge 1979]; then
       python -u ./calc_rx1day.py --start=$start_year --end=$end_year --dataset="cpc"
       python -u ./calc_rx1day.py --start=$start_year --end=$end_year --dataset="mswep"
    fi

    done
done

#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="regen"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="cpc"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="cpc_shift"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="mswep"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="highres_cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="mesaclip"
#python -u ./calc_rx1day.py --start=1979 --end=2016 --dataset="spear"

#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="cpc"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="cpc_shift"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="mswep"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="highres_cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="mesaclip"
#python -u ./calc_rx1day.py --start=1979 --end=2020 --dataset="spear"

#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="cpc"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="cpc_shift"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="mswep"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="highres_cmip"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="mesaclip"
#python -u ./calc_rx1day.py --start=1979 --end=2024 --dataset="spear"


