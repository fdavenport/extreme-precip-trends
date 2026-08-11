#!/bin/bash
#SBATCH --job-name=ecdf_test_mon
#SBATCH --error=/davenport-scratch/fvdav22/job_output/ecdf_test_mon_%a.err
#SBATCH --output=/davenport-scratch/fvdav22/job_output/ecdf_test_mon_%a.out
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=f.davenport@colostate.edu
#SBATCH --ntasks=4
#SBATCH --time=3:00:00
#SBATCH --array=0-60%16
#SBATCH --partition=dav_all


cd /davenport-scratch/fvdav22/projects/extreme-precip-trends
eval "$(conda shell.bash hook)"
conda activate ./envs
cd code

start_year=$((SLURM_ARRAY_TASK_ID+1930))

for end_year in $(seq $((start_year + 30)) 2020); do
    
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcc" --model="cmip-sub" --var="mon-p095" --test
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcc" --model="cmip-sub" --var="mon-p095" --test --obsmask
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcc" --model="spear" --var="mon-p095" --test 
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcc" --model="spear" --var="mon-p095" --test --obsmask
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcc" --model="mesaclip" --var="mon-p095" --test
    python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcc" --model="mesaclip" --var="mon-p095" --test --obsmask

    if [ "$start_year" -ge 1979 ]; then
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcp" --model="cmip-sub" --var="mon-p095" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcp" --model="spear" --var="mon-p095" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcp" --model="mesaclip" --var="mon-p095" --test --obsmask
       
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="cmip-sub" --var="mon-p095" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="spear" --var="mon-p095" --test --obsmask
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="mesaclip" --var="mon-p095" --test --obsmask

       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcp" --model="cmip-sub" --var="mon-p095" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcp" --model="spear" --var="mon-p095" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="gpcp" --model="mesaclip" --var="mon-p095" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="cmip-sub" --var="mon-p095" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="spear" --var="mon-p095" --test
       python -u ./calc_ecdf.py --start=$start_year --end=$end_year --obs="mswep" --model="mesaclip" --var="mon-p095" --test 
       
    fi
    
done



