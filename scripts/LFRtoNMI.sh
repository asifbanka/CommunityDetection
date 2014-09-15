#!/bin/sh

#TODO change this to your location
ROOT=~/community-detection

communityDetection=$ROOT/algorithm/build/community_detection
communityClassifier=$ROOT/scripts/communityClassifier.py
graphParser=$ROOT/scripts/graphParser.py
NMI=$ROOT/code/coverComparision/mutual

# the graph output of the lfr
graphLFR=$1
# the community output of the lfr
communitiesLFR=$2
# the percentage of seed nodes
percentage=$3

# temporary files
graph="/tmp/tmp_graph"
communities="/tmp/tmp_communities"
seedNodes="/tmp/tmp_seedNodes"
affinities="/tmp/tmp_affinies"
detectedCommunities="/tmp/tmp_detectedCommunities"

echo "=> convert the LFR files to our file format and get the seed nodes"
python2 $graphParser -g $graphLFR -G $graph -c $communitiesLFR -C $communities -s $seedNodes -n $percentage

echo "=> perform community detection"
$communityDetection $graph $seedNodes $affinities

echo "=> classify communities"
python2 $communityClassifier -a $affinities -o 0 -c $detectedCommunities

echo "=> calculate NMI"
$NMI $communities $detectedCommunities
