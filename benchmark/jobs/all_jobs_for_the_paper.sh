#!/usr/bin/env zsh

### Job name
#BSUB -J ALL_JOBS_FOR_THE_PAPER[1-96]

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o FOO%J.%I

### Request the time you need for execution in minutes
### The format for the parameter is: [hour:]minute,
### that means for 80 minutes you could also use this: 1:20
# BSUB -W 120:00

### Request memory you need for your job in TOTAL in MB
# BSUB -M 2024

#BSUB -B
#BSUB -N
#BSUB -u jan.dreier@rwth-aachen.de

##############################################


# THIS SCRIPT SHALL GENERATE ALL THE RESULTS PLOTTED IN THE PAPER



set -e #fail fast
echo "begin benchmark, LSB_JOBINDEX=$LSB_JOBINDEX"


#each job needs to be run in its own subdir
tmpdir=tmpdir_$LSB_JOBINDEX
rm -rf $tmpdir
mkdir $tmpdir


#go to subfolder
cd $tmpdir


#create output directories
outdir=../../../../benchmarkoutput
mkdir -p $outdir
mkdir -p $outdir/nonoverlap_noniter
mkdir -p $outdir/nonoverlap_iter
mkdir -p $outdir/overlap_noniter
mkdir -p $outdir/overlap_iter


#aliases for the two benchmark scripts
benchmark_nonoverlap=../../benchmark.py
benchmark_overlap=../../benchmark_overlap.py


#this counter is incremented while iterating over all possible jobs.
#once the counter hits LSB_JOBINDEX the job is executed
job=0

#run the benchmark with these numbers of nodes
nodes=( 1000 5000 )
#run the benchmark with these community sizes
communitysizes=(big small)
#use these seed fractions when not doing iteration
seedsNonIterative=( 0.05 0.10 0.15 0.20 )
#use these seed fractions when doing iteration
seedsIterative=( 0.02 0.3 0.5 0.10 )
#use these mixing parameter when doing overlapping detection
overlapMixing=( 0.1 0.3 )
#number of iterations for the iterative method
iterations=10
#samples per datapoint
samples=100


#non-overlapping, non-iterative
for n in $nodes
do
    for c in $communitysizes
    do
        for s in $seedsNonIterative
        do
            job=$((job+1))
            if [ "$job" -eq "$LSB_JOBINDEX" ]
            then
                $benchmark_nonoverlap -o $outdir/nonoverlap_noniter -n $n -c $c -s $s -i 1 -m "0.05 0.8 0.05" --samples_per_datapoint $samples --classification_strategy max
            fi
        done
    done
done

#non-overlapping, iterative
for n in $nodes
do
    for c in $communitysizes
    do
        for s in $seedsIterative
        do
            job=$((job+1))
            if [ "$job" -eq "$LSB_JOBINDEX" ]
            then
                $benchmark_nonoverlap -o $outdir/nonoverlap_iter -n $n -c $c -s $s -i $iterations -m "0.05 0.8 0.05" --samples_per_datapoint $samples --classification_strategy max
            fi
        done
    done
done

#overlapping, non-iterative
for n in $nodes
do
    for c in $communitysizes
    do
        for s in $seedsNonIterative
        do
            for m in $overlapMixing
            do
                job=$((job+1))
                if [ "$job" -eq "$LSB_JOBINDEX" ]
                then
                    $benchmark_overlap -o $outdir/overlap_noniter -n $n -c $c -s $s -i 1 -O "0.0 0.5 0.05" --om 3 -m $m --samples_per_datapoint $samples --classification_strategy gap
                fi
            done
        done
    done
done

#overlapping, iterative
for n in $nodes
do
    for c in $communitysizes
    do
        for s in $seedsIterative
        do
            for m in $overlapMixing
            do
                job=$((job+1))
                if [ "$job" -eq "$LSB_JOBINDEX" ]
                then
                    $benchmark_overlap -o $outdir/overlap_iter -n $n -c $c -s $s -i $iterations -O "0.0 0.5 0.05" --om 3 -m $m --samples_per_datapoint $samples --classification_strategy gap
                fi
            done
        done
    done
done

echo "end benchmark"
