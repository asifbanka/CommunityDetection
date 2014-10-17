#!/usr/bin/env python2

import sys
from optparse import OptionParser
from collections import defaultdict

from communityutils import *


##########################################
#
# COMMAND LINE INTERFACE


parser = OptionParser()

# command line options
parser.add_option("-a", dest="affinity_file", type="string",
    help="Input: affinity vectors, as given by the c++ algorithm")

parser.add_option("-c", dest="actual_communities_file", type="string",
        help="Output: classified communities")

parser.add_option("--classification_strategy", dest="classification_strategy", type="string",
        help="Output: heuristic for community classification (max (default)| gap)")

parser.add_option("-C", dest="classified_communities_file", type="string",
        help="Output: classified communities")

options, args = parser.parse_args()

valid = True
if not (options.affinity_file
        and options.classification_strategy
        and options.classified_communities_file):
    valid = False

if valid == False:
    parser.print_help()
    exit(1)


##########################################
#
# CLASSIFICATION

# Classify communities from the affinity output of the c++ algorithm.
# Simply assign the vertex the the community with the maximum affinity-value.
def classifyCommunities(self, affinities):
    communitiesPerVertex = 1
    self.vertexToCommunities = defaultdict(list)
    for vertex, affinities in affinities.vertexToAffinities.iteritems():
        maxIndex = max([(v,i) for i,v in enumerate(affinities)])[1]
        self.vertexToCommunities[vertex] = [maxIndex]
    self.communityToVertices = self.reverseMapping(self.vertexToCommunities)
    self.numberOfCommunities = len(self.communityToVertices)
setattr(Communities, 'classifyCommunities', classifyCommunities)

# Classify communities from the affinity output of the c++ algorithm.
# Assign communities according to "gap-strategy"
def classifyCommunitiesWithGaps(self, affinities):
    self.vertexToCommunities = defaultdict(list)
    for vertex, affinities in affinities.vertexToAffinities.iteritems():
        communities,gapPosition,gapSize = self.getGap(affinities)
        self.vertexToCommunities[vertex] = communities
    self.communityToVertices = self.reverseMapping(self.vertexToCommunities)
    self.numberOfCommunities = len(self.communityToVertices)
setattr(Communities, 'classifyCommunitiesWithGaps', classifyCommunitiesWithGaps)

def classifyCommunitiesGroundTruth(self, affinities, groundTruth):
    self.vertexToCommunities = defaultdict(list)
    for vertex, affinities in affinities.vertexToAffinities.iteritems():
        # Put affinities with their index (the corresponding community) in tuple 
        # and sort them by first entry (affinity). 
        # Then extract the second entry (the community) from each tuple.
        sortedTuples = sorted([(v,i) for i,v in enumerate(affinities)])
        sortedTuples.reverse()

        foo = groundTruth.vertexToCommunities[vertex]
        numberOfCommunities = len(foo)

        communities = [i for (v,i) in sortedTuples][:numberOfCommunities]
        self.vertexToCommunities[vertex] = communities

    self.communityToVertices = self.reverseMapping(self.vertexToCommunities)
    self.numberOfCommunities = len(self.communityToVertices)
setattr(Communities, 'classifyCommunitiesGroundTruth', classifyCommunitiesGroundTruth)


##########################################
#
# MAIN PROGRAM

affinities = Affinities()
affinities.readAffinitiesCustom(options.affinity_file)

classifiedCommunities = Communities()

#read Ground Truth
groundTruth = Communities()
groundTruth.readCommunitiesLFR(options.actual_communities_file)

print "use classification stragegy", options.classification_strategy
if options.classification_strategy == "max":
    classifiedCommunities.classifyCommunities(affinities)
elif options.classification_strategy == "gap":
    classifiedCommunities.classifyCommunitiesWithGaps(affinities)
elif options.classification_strategy == "ground_truth":
    classifiedCommunities.classifyCommunitiesGroundTruth(affinities, groundTruth)
else:
    raise Exception("invalid classification_strategy")


classifiedCommunities.writeCommunitesCustom(options.classified_communities_file)
classifiedCommunities.writeJSONfile("statistics.json", affinities, groundTruth)
