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
#
# COMMAND LINE INTERFACE


# parse the parameters
parser = OptionParser()
parser.add_option("-g", "--graph",          dest="graph",                             help="input graph")
parser.add_option("-s", "--seed",           dest="seed",                              help="input seeds")
parser.add_option("-A", "--affinities",     dest="affinities",                        help="output affinities")
parser.add_option("-i", "--iterations",     dest="iterations",         type="int",    help="number of iterations")
parser.add_option("--iterative_strategy",   dest="iterative_strategy", type="string", help="")
parser.add_option("--iterative_factor",     dest="iterative_factor",   type="float" , help="")
options, args = parser.parse_args()

valid = True
if not (options.graph and 
        options.seed and 
        options.affinities and 
        options.iterations and
        options.iterative_strategy and
        options.iterative_factor):
    valid = False

if valid == False:
    parser.print_help()
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

# check if the input graph is valid
graph = Graph()
graph.readGraphOurFormat(options.graph)
if not graph.isSymmetric():
    raise Exception("graph is not symmetric!")
if not graph.isConnected():
    raise Exception("graph is not connected!")


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
    affinities.readAffinitiesOurFormat(affinityFileNo(i))

    communities = Communities()

    if options.iterative_strategy == "fraction":
        pickSeedsNonoverlappingFraction(communities, affinities, options.iterative_factor)
    elif options.iterative_strategy == "threshold":
        pickSeedsNonoverlappingThreshold(communities, affinities, options.iterative_factor)
    else:
        raise Exception("invalid method")


    if len(communities.vertexToCommunities) == 0:
        raise Exception("got no new seeds for the next round. this is probably due to a bad parameter for -f")

    print "number of seeds ", len(communities.vertexToCommunities)
    communities.writeSeedsOurFormat(communities.vertexToCommunities.keys(), seedFileNo(i+1))


#shutil.copy2(affinityFileNo(options.iterations-1), options.affinities)
