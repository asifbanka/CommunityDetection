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

from lib.communityutils import *
from lib.communities import *


########################################################
#
# COMMAND LINE INTERFACE


# parse the parameters
parser = OptionParser()
parser.add_option("-g", "--graph",             dest="graph",                             help="input graph")
parser.add_option("-s", "--seed",              dest="seed",                              help="input seeds")
parser.add_option("-A", "--affinities",        dest="affinities",                        help="output affinities")
parser.add_option("-i", "--iterations",        dest="iterations",         type="int",    help="number of iterations")
parser.add_option("--iterative_strategy",      dest="iterative_strategy", type="string", help="")
parser.add_option("--iterative_factor",        dest="iterative_factor",   type="float" , help="")
parser.add_option("--classification_strategy", dest="classification_strategy",           help="")
options, args = parser.parse_args()

valid = True
if not (options.graph and 
        options.seed and 
        options.affinities and 
        options.iterations and
        options.iterative_strategy and
        options.iterative_factor and
        options.classification_strategy):
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


def pick_seeds_by_fraction(affinities, factor):
    number_of_communities = len(affinities.vertexToAffinities.itervalues().next())

    community_to_vertices = defaultdict(list)
    for vertex, affinities_of_vertex in affinities.vertexToAffinities.iteritems():
        community = np.argmax(affinities_of_vertex)
        community_to_vertices[community].append(vertex)

    seeds = set()
    for community, vertices in community_to_vertices.iteritems():
        number_of_seed_nodes = sum(1 for vertex in vertices if max(affinities.vertexToAffinities[vertex]) == 1)
        number_of_new_seed_nodes = int(math.ceil(number_of_seed_nodes * factor))

        sorted_items = sorted(vertices, key=lambda vertex: max(affinities.vertexToAffinities[vertex]), reverse=True)
        seeds = seeds.union(sorted_items[:number_of_new_seed_nodes])

    return seeds


#def pick_seeds_by_threshold(communities, affinities, factor):
    #communities.numberOfCommunities = len(affinities.vertexToAffinities.itervalues().next())

    #communities.vertexToCommunities = defaultdict(list)
    #for nodeId, affinitiesOfVertex in affinities.vertexToAffinities.iteritems():
        #maxIndex = np.argmax(affinitiesOfVertex)
        #if affinitiesOfVertex[maxIndex] >= factor:
            #communities.vertexToCommunities[nodeId] = [maxIndex]

    #communities.communityToVertices = communities.reverseMapping(communities.vertexToCommunities)


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

for i in range(options.iterations):

    print "------------"

    returnValue = sp.call([PATH_TO_ALGORITHM, options.graph , seedFileNo(i) , affinityFileNo(i)], shell=False)
    if returnValue != 0:
        print "error in subprocess"
        exit(1)

    print "read seed nodes from", affinityFileNo(i), ", modify them using the", options.classification_strategy ,"strategy, and write them to", seedFileNo(i+1)

    affinities = Affinities()
    affinities.readAffinitiesOurFormat(affinityFileNo(i))


    # generate a new set of seed nodes
    seeds = set()
    if options.iterative_strategy == "fraction":
        seeds = pick_seeds_by_fraction(affinities, options.iterative_factor)
    elif options.iterative_strategy == "threshold":
        raise Exception("sorry. i did not port this function")
    if len(seeds) == 0:
        raise Exception("got no new seeds for the next round. this is probably due to a bad parameter for -f")
    print "number of seeds ", len(seeds)


    # classify vertices with propper strategy and write some of them as seed nodes to file
    communities = Communities()
    if options.classification_strategy == "max":
        communities.classifyCommunities(affinities)
    elif options.classification_strategy == "gap":
        communities.classifyCommunitiesWithGaps(affinities)
    else:
        raise Exception("invalid classification_strategy")
    communities.writeSeedsOurFormat(seeds, seedFileNo(i+1))


#shutil.copy2(affinityFileNo(options.iterations-1), options.affinities)
