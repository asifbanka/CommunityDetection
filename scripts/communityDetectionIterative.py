#!/usr/bin/env python2

import os
import shutil
import operator
import math
import numpy as np
import subprocess as sp
from collections import defaultdict
from optparse import OptionParser
from pprint import pprint

from communityutils import *


########################################################


# parse the parameters
parser = OptionParser()
parser.add_option("-g", "--graph", dest="graph")
parser.add_option("-s", "--seed", dest="seed", help="")
parser.add_option("-A", "--affinities", dest="affinities")
parser.add_option("-i", "--iterations", dest="iterations", type="int")
parser.add_option("-m", "--method", dest="method", type="string")
parser.add_option("-f", "--factor", dest="factor", type="float" )
(options, args) = parser.parse_args()

valid = True
if not (options.graph and 
        options.seed and 
        options.affinities and 
        options.iterations and
        options.method and
        options.factor):
    print "ERROR: wrong parameters"
    print "usage: -g graph -s seed -a affinities -i iterations -m method -f factor"
    valid = False

if valid == False:
    exit(1)


########################################################


# all the filenames


# the root of the repository
ROOT = os.path.dirname(os.path.realpath(__file__)) + "/../"

# the c++ algorithm
PATH_TO_ALGORITHM = ROOT + "algorithm/build/community_detection"


# the name of the temporary seed file for the ith iteration
def seedFileNo(i):
    return options.seed + "_" + str(i)

# the name of the affinity file for the ith iteration
def affinityFileNo(i):
    return options.affinities + "_" + str(i)


########################################################


def pickSeedsNonoverlappingFraction(communities, affinities, factor):
    communities.numberOfCommunities = len(affinities.vertexToAffinities.itervalues().next())

    seedsOfCommunity = [defaultdict(list) for i in range(communities.numberOfCommunities)]
    for nodeId, affinitiesOfVertex in affinities.vertexToAffinities.iteritems():
        maxIndex = np.argmax(affinitiesOfVertex)
        seedsOfCommunity[maxIndex][nodeId] = affinitiesOfVertex

    communities.vertexToCommunities = defaultdict(list)
    for i in range(communities.numberOfCommunities):

        numberOfSeedNodes = sum(1 for x in seedsOfCommunity[i].values() if max(x) == 1)
        numberOfNewSeedNodes = int(math.ceil(numberOfSeedNodes * factor))

        sortedItems = sorted(seedsOfCommunity[i].items(), key=lambda tup: max(tup[1]))
        for (nodeId, affinity) in sortedItems[-numberOfNewSeedNodes:]:
            communities.vertexToCommunities[nodeId] = [i]

    communities.communityToVertices = communities.reverseMapping(communities.vertexToCommunities)


def pickSeedsNonoverlappingThreshold(communities, affinities, factor):
    communities.numberOfCommunities = len(affinities.vertexToAffinities.itervalues().next())

    communities.vertexToCommunities = defaultdict(list)
    for nodeId, affinitiesOfVertex in affinities.vertexToAffinities.iteritems():
        maxIndex = np.argmax(affinitiesOfVertex)
        if affinitiesOfVertex[maxIndex] >= factor:
            communities.vertexToCommunities[nodeId] = [maxIndex]

    communities.communityToVertices = communities.reverseMapping(communities.vertexToCommunities)


########################################################


print "copy", options.seed, "to", seedFileNo(0)
shutil.copy2(options.seed, seedFileNo(0))
#seeds = readSeedFile(options.seed)
#print "initial number of seed nodes:", len(seeds)
#writeSeedFile(seeds, seedFileNo(0))

for i in range(options.iterations):

    print "------------"

    returnValue = sp.call([PATH_TO_ALGORITHM, options.graph , seedFileNo(i) , affinityFileNo(i)], shell=False)
    if returnValue != 0:
        print "error in subprocess"
        exit(1)

    print "read seed nodes from", affinityFileNo(i), ", modify them, and write them to", seedFileNo(i+1)

    affinities = Affinities()
    affinities.readAffinitiesCustom(affinityFileNo(i))

    communities = Communities()

    if options.method == "fraction":
        pickSeedsNonoverlappingFraction(communities, affinities, options.factor)
    elif options.method == "threshold":
        pickSeedsNonoverlappingThreshold(communities, affinities, options.factor)
    else:
        raise Exception("invalid method")


    if len(communities.vertexToCommunities) == 0:
        raise Exception("got no new seeds for the next round. this is probably due to a bad parameter for -f")

    print "number of seeds ", len(communities.vertexToCommunities)
    communities.writeSeedsCustom(communities.vertexToCommunities.keys(), seedFileNo(i+1))


#shutil.copy2(affinityFileNo(options.iterations-1), options.affinities)
