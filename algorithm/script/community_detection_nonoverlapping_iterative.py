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

# the root of the c++ algorithm module
ROOT = os.path.dirname(os.path.realpath(__file__)) + "/../"

# the c++ algorithm
pathToAlgorithm = ROOT + "build/community_detection"

# parse the parameters
parser = OptionParser()
parser.add_option("-g", dest="graph")
parser.add_option("-s", dest="seed", help="")
parser.add_option("-a", dest="affinities")
parser.add_option("-i", dest="iterations", type="int", default=1)
#parser.add_option("-t", dest="threshold", type="float", default=1.0)
(options, args) = parser.parse_args()
if not (options.graph and 
        options.seed and
        options.affinities):
    print "ERROR: wrong parameters"
    print "usage: -g graph -s seed -a affinities [-i iterations (default=1)]"
    exit(1)


# seed information is stored as a dict, which maps the seed node id to a list of affinities

# read seed nodes from file and return seed dict
def readSeedFile(filename):
    infile = open(filename, "r")

    s = infile.readline().split()
    if len(s) != 2:
        raise Exception("first line should have exactly two entries")
    numberOfSeedNodes = int(s[0])
    numberOfCommunities = int(s[1])

    # contain seed nodes with their affinties
    seeds = defaultdict(list)
    for l in infile.readlines():
        split = l.split()
        nodeId = int(split[0])
        affinities = [float(a) for a in split[1:]]
        seeds[nodeId] = affinities
        if len(seeds[nodeId]) != numberOfCommunities:
            raise Exception("wrong number of communities")
    return seeds

# write seed dict to file
def writeSeedFile(seeds, filename):
    outfile = open(filename, "w")
    numberOfNodes = len(seeds)
    numberOfCommunities = len(seeds.itervalues().next())
    outfile.write(str(numberOfNodes) + " " + str(numberOfCommunities) + "\n")

    for nodeId, affinities in sorted(seeds.iteritems()):
    #for nodeId, affinities in seeds.iteritems():
        outfile.write(str(nodeId) + " " + " ".join([str(x) for x in affinities]) + "\n")

# takes keeps only those seed entries which have a maximum value of at least $threshold
# the maximum values are set to 1, all other values are set to 0
def updateSeeds(seeds, threshold):

    numberOfSeedNodes = sum(1 for x in seeds.values() if max(x) == 1)
    numberOfNewSeedNodes = int(math.ceil(numberOfSeedNodes * 1.1))
    #numberOfNewSeedNodes = numberOfSeedNodes + 1

    sortedItems = sorted(seeds.items(), key=lambda tup: max(tup[1]))


    newSeeds = defaultdict(list)
    for (nodeId, affinities) in sortedItems[-numberOfNewSeedNodes:]:
        maxIndex = np.argmax(affinities)
        newAffinities = ([0.0] * len(affinities))
        newAffinities[maxIndex] = 1.0
        newSeeds[nodeId] = newAffinities

        if affinities[maxIndex] != 1: 
            print "add seed with affinity", affinities[maxIndex]
    return newSeeds


    #for nodeId, affinities in seeds.iteritems():
        #maxIndex = np.argmax(affinities)
        #if(affinities[maxIndex]) >= threshold:
            #print affinities[maxIndex]
            ## if we strongly believe that a certain node belongs to a community
            #newAffinities = ([0] * len(affinities))
            ##newAffinities[0] = 1
            #newAffinities[maxIndex] = 1
            #newSeeds[nodeId] = newAffinities
    #return newSeeds


########################################################

# the name of the temporary seed file for the ith iteration
def seedFileNo(i):
    return options.seed + "_" + str(i)

# the name of the affinity file for the ith iteration
def affinityFileNo(i):
    return options.affinities + "_" + str(i)


print "copy", options.seed, "to", seedFileNo(0)
#shutil.copy2(options.seed, seedFileNo(0))
seeds = readSeedFile(options.seed)
writeSeedFile(seeds, seedFileNo(0))

for i in range(options.iterations):

    print "------------"

    returnValue = sp.call([pathToAlgorithm , options.graph , seedFileNo(i) , affinityFileNo(i)], shell=False)
    if returnValue != 0:
        print "error in subprocess"
        exit(1)

    print "read seed nodes from", affinityFileNo(i), ", modify them, and write them to", seedFileNo(i+1)
    seeds = readSeedFile(affinityFileNo(i))
    newSeeds = updateSeeds(seeds, 0.2)
    print "number of seeds ", len(newSeeds)
    writeSeedFile(newSeeds, seedFileNo(i+1))

#shutil.copy2(affinityFileNo(options.iterations-1), options.affinities)
