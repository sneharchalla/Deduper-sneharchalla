#!/bin/bash

#SBATCH -p bgmp

#SBATCH --cpus-per-task=8
#SBATCH --job-name=deduper_stats
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --account=bgmp
#SBATCH --time=0-24:00:00


awk '$3 !- /@/ {print $3}' deduplicated.sam | uniq -c