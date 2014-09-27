#!/usr/bin/env python2

import sys
from optparse import OptionParser
from collections import defaultdict
import re

##########################################
#
# COMMAND LINE INTERFACE

def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-a", dest="affinity_file", type="string",
        help="Input: affinity vectors, as given by the c++ algorithm")

    parser.add_option("-c", dest="classified_communities_file", type="string",
            help="Output: classified communities")
    
    #parser.add_option("-o", dest="overlapping", type="int",
        #help="if communities are overlapping set to 1, otherwise to 0")
    
    global options, args
    (options, args) = parser.parse_args()

    if not options.affinity_file:
        parser.error("Affinity file not given")
        parser.print_help()
        return False

    elif not options.classified_communities_file:
        parser.error("Output file not given")
        parser.print_help()
        return False

    #elif not hasattr(options, "overlapping"):
        #parser.error("Specify if using overlapping or non-overlapping mode")
        #parser.print_help()
        #return False

    return True


##########################################
#
# AFFINITIES
# 
# Affinities are stored as a dict, which maps the nodeid to an affinity-vector.
# The i-th index in this vector represents the affinity to the i-th community
# This strucure is called vertexToAffinities


# Read output from c++ algorithm to affinity-dict.
# "overlapping" should be true if we are doing overlapping community-detection.
def readAffinities(filename, communitiesPerVertex):
    vertexToAffinities = defaultdict(list)
    with open (filename, "r") as f:

        firstRow = f.readline().split()
        if len(firstRow) != 2:
            raise Exception("first line should have exactly two entries")
        numberOfNodes = int(firstRow[0])
        numberOfCommunities = int(firstRow[1])

        for line in f.readlines():
            split = line.split()
            nodeId = int(split[0])
            vertexToAffinities[nodeId] = [float(a) for a in split[1:]]

            if len(vertexToAffinities[nodeId]) != numberOfCommunities:
                raise Exception("wrong number of communities")

            s = sum(vertexToAffinities[nodeId])
            if not ( communitiesPerVertex - 0.01 < s and s < communitiesPerVertex + 0.01):
                raise Exception("rows dont sum up")

        if len(vertexToAffinities) != numberOfNodes:
            raise Exception("wrong number of nodes")

    return vertexToAffinities


##########################################
#
# COMMUNITIES
# 
# Communities are stored as a dict, which maps the vertex # to the list of communities it belongs to.
# This strucure is called vertexToCommunities.


# simply assign the vertex the the community with the maximum affinity-value
def classifyCommunities(vertexToAffinities, communitiesPerVertex):
    vertexToCommunities = defaultdict(list)
    for vertex, affinities in vertexToAffinities.iteritems():
        # Put affinities with their index (the corresponding community) in tuple 
        # and sort them by first entry (affinity). 
        # Then extract the second entry (the community) from each tuple.
        sortedTuples = sorted([(v,i) for i,v in enumerate(affinities)])
        # The list was sorted ascending, so take communities from the end.
        communities = [i for (v,i) in sortedTuples][-communitiesPerVertex:]
        vertexToCommunities[vertex] = communities


    return vertexToCommunities


#write output community file
def writeCommunites(vertexToCommunities, filename):

    # remap value list as keys, keys as values
    communityToVertices = defaultdict(list)
    for vertex, communities in vertexToCommunities.iteritems():
        for c in communities:
            communityToVertices[c].append(vertex)

    with open (filename, "w") as f:
        for vertices in communityToVertices.values():
            f.write(" ".join([str(x) for x in vertices]) + "\n")


##########################################
#
# MAIN PROGRAM

options, args = 0, 0
if commandline_interface():

    # set this to 1 for non-overlapping detection
    communitiesPerVertex = 1

    vertexToAffinities = readAffinities(options.affinity_file, communitiesPerVertex)
    vertexToCommunities = classifyCommunities(vertexToAffinities, communitiesPerVertex)
    writeCommunites(vertexToCommunities, options.classified_communities_file)
