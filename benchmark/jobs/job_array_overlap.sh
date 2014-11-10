#!/usr/bin/env zsh

### Job name
#BSUB -J NONOVERLAPPING_ITERATIVE[1-16]

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o FOO%J.%I

### Request the time you need for execution in minutes
### The format for the parameter is: [hour:]minute,
### that means for 80 minutes you could also use this: 1:20
# BSUB -W 60:00

### Request memory you need for your job in TOTAL in MB
# BSUB -M 2024

#BSUB -B
#BSUB -N
#BSUB -u philipp.kuinke@rwth-aachen.de

##############################################

# fail fast
set -e

echo "begin benchmark, LSB_JOBINDEX=$LSB_JOBINDEX"

tmpdir=tmpdir_$LSB_JOBINDEX
rm -rf $tmpdir
mkdir $tmpdir
cd $tmpdir
mkdir -p ../../../../output

case $LSB_JOBINDEX in
1)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.05 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
2)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.10 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
3)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.15 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
4)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.20 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
5)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.05 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
6)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.10 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
7)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.15 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
8)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c small -s 0.20 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
9)  ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.05 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
10) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.10 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
11) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.15 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
12) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.20 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.1 --samples_per_datapoint 100 --classification_strategy gap
    ;;
13) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.05 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
14) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.10 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
15) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.15 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
16) ../../benchmark_overlap.py -o ../../../../output -n 1000 -c big -s 0.20 -i 1  -O "0.0 0.5 0.05" --om 3 -m 0.3 --samples_per_datapoint 100 --classification_strategy gap
    ;;
*)  echo "error"
    ;;
esac


echo "end benchmark"
