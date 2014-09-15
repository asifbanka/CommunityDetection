#!/bin/sh

#TODO change this to your location
ROOT=~/community-detection

communityDetection=$ROOT/algorithm/build/community_detection
NMI=$ROOT/code/coverComparision/mutual
communityClassifier=$ROOT/scripts/communityClassifier.py

# the graph input to the c++ algorithm
graph=$1
# the seed input to the c++ algorithm
seedNodes=$2
# the original communities
communities=$3

# temporary affinity file
affinity=/tmp/affinityFile
# temporary community file
detectedCommunities=/tmp/communityFile

$communityDetection $graph $seedNodes $affinity
python2 $communityClassifier -a $affinity -o 0 -c $detectedCommunities
$NMI $communities $detectedCommunities
