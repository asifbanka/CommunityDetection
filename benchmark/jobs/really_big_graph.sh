#!/usr/bin/env zsh

### Job name
#BSUB -J REALLY_BIG_GRAPH[1-9]

### File / path where STDOUT & STDERR will be written
###    %J is the job ID, %I is the array ID
#BSUB -o REALLY_BIG_GRAPH%J.%I

### Request the time you need for execution in minutes
### The format for the parameter is: [hour:]minute,
### that means for 80 minutes you could also use this: 1:20
# BSUB -W 120:00

### Request memory you need for your job in TOTAL in MB
# BSUB -M 10000 

#BSUB -B
#BSUB -N
#BSUB -u jan.dreier@rwth-aachen.de

##############################################



set -e #fail fast
echo "begin benchmark, LSB_JOBINDEX=$LSB_JOBINDEX"


#each job needs to be run in its own subdir
tmpdir=tmpdir_really_big_$LSB_JOBINDEX
rm -rf $tmpdir
mkdir $tmpdir


#go to subfolder
cd $tmpdir


#create output directories
outdir=../../../../really_big_graph
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
nodes=( 50000 )
#run the benchmark with these community sizes
communitysizes=( diverse )
#use these seed fractions when not doing iteration
seedsNonIterative=( 0.02 0.05 )
samples=1
muRange=( 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 )


#non-overlapping, non-iterative
for n in $nodes
do
    for c in $communitysizes
    do
        for s in $seedsNonIterative
        do
	    for mu in $muRange
            do
                job=$((job+1))
                if [ "$job" -eq "$LSB_JOBINDEX" ]
                then

	            mkdir -p $outdir/job$job
                    $benchmark_nonoverlap \
                        -o $outdir/job$job \
                        -n $n -c $c -s $s -i 1 \
                        -m $mu
                        --samples_per_datapoint $samples \
                        --classification_strategy max \
                        --overwrite_file 1
                fi
            done
        done
    done
done

echo "end benchmark"
