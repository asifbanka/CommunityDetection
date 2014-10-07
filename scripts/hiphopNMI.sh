#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT=$DIR/..

LFR=$ROOT/external/binary_networks/benchmark
communityDetection=$ROOT/scripts/communityDetectionIterative.py
communityClassifier=$ROOT/scripts/communityClassifier.py
graphParser=$ROOT/scripts/graphParser.py
NMI=$ROOT/external/NMI/mutual

hiphopGraph=$ROOT/data/hiphop/hiphop.edges
hiphopCommunities=$ROOT/data/hiphop/hiphop.communities

seed1=$ROOT/data/hiphop/hiphop_0.05.seed

# the affinity output from the c++ algorithm
affinities="tmp_affinies"
# the output from the community classifier
detectedCommunities="tmp_detectedCommunities"

# write the nmi value to this file
nmiValue=$1

# the multiplication factor for the iterative method
factor=1.1

# the number of rounds for the iterative method
rounds=1

# fail fast
set -e

echo "=> perform community detection"
$communityDetection -g $hiphopGraph -s $seed1 -A $affinities -r $rounds -f $factor

rm -f $nmiValue
echo "=> classify communities and calculate NMI"
for i in $(seq 0 $(($rounds-1))); do 
    #echo "($(($i+1))/$rounds)"
    $communityClassifier -a ${affinities}_$i -c $hiphopCommunities -C ${detectedCommunities}_$i
    $NMI $hiphopCommunities ${detectedCommunities}_$i | awk '{print $2 }' >> $nmiValue
done

echo "=> delete files except for $nmiValue"
rm ${seedNodes}_$rounds
for i in $(seq 0 $(($rounds-1))); do 
    rm ${seedNodes}_$i
    rm ${affinities}_$i
    rm ${detectedCommunities}_$i
done

echo ""
echo "======================="
echo ""
echo ""
echo "NMI:" 
echo "----"
cat $nmiValue