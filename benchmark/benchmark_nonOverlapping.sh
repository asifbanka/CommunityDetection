#!/usr/bin/env sh

### Job name
#BSUB -J BENCHMARK_NONOVERLAPPING

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o BENCHMARK_NONOVERLAPPING.%J.%I

### Request the time you need for execution in minutes
### The format for the parameter is: [hour:]minute,
### that means for 80 minutes you could also use this: 1:20
### BSUB -W 48:00

### Request memory you need for your job in TOTAL in MB
### BSUB -M 5000

#BSUB -B
#BSUB -N
#BSUB -u jan.dreier@rwth-aachen.de

##############################################

# fail fast
set -e

echo "begin benchmark"

echo "=> calculate NMI"
./calculateNMI_nonOverlapping.py
echo "=> calculate mean"
./calculateMean.py

echo "end benchmark"
