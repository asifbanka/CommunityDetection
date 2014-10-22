#!/usr/bin/env zsh

### Job name
#BSUB -J NONOVERLAPPING_ITERATIVE[1-8]

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o FOO%J.%I

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

# fail fast
set -e

echo "begin benchmark, LSB_JOBINDEX=$LSB_JOBINDEX"

tmpdir=tmpdir_$LSB_JOBINDEX
rm -rf $tmpdir
mkdir $tmpdir
cd $tmpdir
mkdir -p ../../../output

case $LSB_JOBINDEX in
1)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.05 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
2)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.10 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
3)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.15 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
4)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.01 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
5)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.02 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
6)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.03 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
7)  ../benchmark.py -o ../../../output -n 1000 -c nonoverlap -s 0.04 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy max
    ;;
8)  ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.05 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
9)  ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.10 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
10) ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.15 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
11) ../benchmark.py -o ../../../output -n 1000 -c overlap30  -s 0.05 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
12) ../benchmark.py -o ../../../output -n 1000 -c overlap30  -s 0.10 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
13) ../benchmark.py -o ../../../output -n 1000 -c overlap30  -s 0.15 -i 1  -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
14) ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.01 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
15) ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.02 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
16) ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.03 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
17) ../benchmark.py -o ../../../output -n 1000 -c overlap15  -s 0.04 -i 20 -m "0.05 0.7 0.05" --samples_per_datapoint 100 --classification_strategy gap
    ;;
*)  echo "error"
    ;;
esac


echo "end benchmark"
