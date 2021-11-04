#!/bin/bash

#SBATCH -p bgmp

#SBATCH --cpus-per-task=24
#SBATCH --job-name=deduper
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --account=bgmp
#SBATCH --time=0-24:00:00


python Trial_2.py -fh_input sorted.sam -fh_umi STL96.txt -fh_o deduplicated.sam

#python Trial.py -fh_input DataFile -fh_umi STL96.txt -fh_o my.o 