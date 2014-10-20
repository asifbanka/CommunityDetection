#!/usr/bin/env python2

import sys
from optparse import OptionParser
from collections import defaultdict

from lib.communityutils import *
from lib.communities import *


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
        help="Output: heuristic for community classification (max | gap)")

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
# MAIN PROGRAM

affinities = Affinities()
affinities.readAffinitiesOurFormat(options.affinity_file)

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


classifiedCommunities.writeCommunitesOurFormat(options.classified_communities_file)
classifiedCommunities.writeJSONfile("statistics.json", affinities, groundTruth)
