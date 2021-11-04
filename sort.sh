#!/bin/bash

#SBATCH -p bgmp

#SBATCH --cpus-per-task=8
#SBATCH --job-name=dedup_sort
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --account=bgmp
#SBATCH --time=0-24:00:00

samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam  -o sorted.sam