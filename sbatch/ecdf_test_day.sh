#!/bin/bash
#SBATCH --job-name=ecdf_test_day
#SBATCH --error=/davenport-scratch/fvdav22/job_output/ecdf_test_day_%a.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/ecdf_test_day_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=4
#SBATCH --time=3:00:00
#SBATCH --array=0-40
#SBATCH --partition=dav_all

cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

start_year=$((SLURM_ARRAY_TASK_ID+1950))

for end_year in $(seq $((start_year + 30)) 2020); do

    if [ "$end_year" -le 2016 ]; then
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="regen" --model="cmip-sub" --var="rx1day" --test
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="regen" --model="cmip-sub" --var="rx1day" --test --obsmask
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="regen" --model="spear" --var="rx1day" --test
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="regen" --model="spear" --var="rx1day" --test --obsmask
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="regen" --model="mesaclip" --var="rx1day" --test
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="regen" --model="mesaclip" --var="rx1day" --test --obsmask
    fi

    if [ "$start_year" -ge 1979 ]; then
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="cpc" --model="cmip-sub" --var="rx1day" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="cpc" --model="spear" --var="rx1day" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="cpc" --model="mesaclip" --var="rx1day" --test --obsmask
       
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="cmip-sub" --var="rx1day" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="spear" --var="rx1day" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="mesaclip" --var="rx1day" --test --obsmask

       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="cpc" --model="cmip-sub" --var="rx1day" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="cpc" --model="spear" --var="rx1day" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="cpc" --model="mesaclip" --var="rx1day" --test
       
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="cmip-sub" --var="rx1day" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="spear" --var="rx1day" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="mesaclip" --var="rx1day" --test
    fi

done



