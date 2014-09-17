#!/usr/bin/env sh

### Job name
#BSUB -J BENCHMARK_NONOVERLAPPING

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o BENCHMARK_NONOVERLAPPING.%J.%I

### Request the time you need for execution in minutes
### The format for the parameter is: [hour:]minute,
### that means for 80 minutes you could also use this: 1:20
### BSUB -W 1:23

### Request memory you need for your job in TOTAL in MB
### BSUB -M 1024

###################################################

# fail fast
set -e

# Execute the application
./calculateNMI_nonOverlapping.py
./calculateMean.py


