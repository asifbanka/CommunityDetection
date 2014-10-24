#!/usr/bin/env sh

### Job name
#BSUB -J BENCHMARK_NONOVERLAPPING

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o BENCHMARK_NONOVERLAPPING.%J.%I

### Request the time you need for execution in minutes
### The format for the parameter is: [hour:]minute,
### that means for 80 minutes you could also use this: 1:20
# BSUB -W 60:00

### Request memory you need for your job in TOTAL in MB
# BSUB -M 1024

#BSUB -B
#BSUB -N
#BSUB -u jan.dreier@rwth-aachen.de

##############################################




echo begin benchmark, LSB_JOBINDEX: $LSB_JOBINDEX
LSB_JOBINDEX=1

tmpdir=tmpdir_$LSB_JOBINDEX
rm -f $tmpdir
mkdir $tmpdir
cd $tmpdir
../benchmark_nonOverlapping.py -n 1000 -c 100-200 -s 0.0$LSB_JOBINDEX -o ../nmivalues --samples_per_datapoint 20 -m "0.08 0.61 0.04" -i 50


echo "end benchmark"
