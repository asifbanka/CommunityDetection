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


########################################################

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

# for each community increase the number of seed nodes by a factor of "factor"
# the nodes with the greatest affinity value for each community are added to the seed nodes
def updateSeeds(seeds, factor):
    numberOfCommunities = len(seeds.itervalues().next())
    seedsOfCommunity = [defaultdict(list) for i in range(numberOfCommunities)]

    for nodeId, affinities in seeds.iteritems():
        maxIndex = np.argmax(affinities)
        seedsOfCommunity[maxIndex][nodeId] = affinities

    newSeeds = defaultdict(list)
    for i in range(numberOfCommunities):
        numberOfSeedNodes = sum(1 for x in seedsOfCommunity[i].values() if max(x) == 1)
        numberOfNewSeedNodes = int(math.ceil(numberOfSeedNodes * factor))


        sortedItems = sorted(seedsOfCommunity[i].items(), key=lambda tup: max(tup[1]))

        for (nodeId, affinities) in sortedItems[-numberOfNewSeedNodes:]:
            newAffinities = ([0.0] * len(affinities))
            newAffinities[i] = 1.0
            newSeeds[nodeId] = newAffinities

            #if affinities[i] != 1: 
                #print "add seed with affinity", affinities[i], "to community", i

    return newSeeds


########################################################

# parse the parameters
parser = OptionParser()
parser.add_option("-g", "--graph", dest="graph")
parser.add_option("-s", "--seed", dest="seed", help="")
parser.add_option("-a", "--affinities", dest="affinities")
parser.add_option("-r", "--rounds", dest="rounds", type="int")
parser.add_option("-f", "--factor", dest="factor", type="float" )
(options, args) = parser.parse_args()

valid = True
if not (options.graph and 
        options.seed and 
        options.affinities and 
        options.rounds and
        options.factor):
    print "ERROR: wrong parameters"
    print "usage: -g graph -s seed -a affinities -r rounds -f factor"
    valid = False

if valid == False:
    exit(1)


########################################################

# all the filenames


# the root of the c++ algorithm module
ROOT = os.path.dirname(os.path.realpath(__file__)) + "/../"

# the c++ algorithm
pathToAlgorithm = ROOT + "build/community_detection"


# the name of the temporary seed file for the ith iteration
def seedFileNo(i):
    return options.seed + "_" + str(i)

# the name of the affinity file for the ith iteration
def affinityFileNo(i):
    return options.affinities + "_" + str(i)

########################################################


print "copy", options.seed, "to", seedFileNo(0)
#shutil.copy2(options.seed, seedFileNo(0))
seeds = readSeedFile(options.seed)
print "initial number of seed nodes:", len(seeds)
writeSeedFile(seeds, seedFileNo(0))

for i in range(options.rounds):

    print "------------"

    returnValue = sp.call([pathToAlgorithm , options.graph , seedFileNo(i) , affinityFileNo(i)], shell=False)
    if returnValue != 0:
        print "error in subprocess"
        exit(1)

    print "read seed nodes from", affinityFileNo(i), ", modify them, and write them to", seedFileNo(i+1)
    seeds = readSeedFile(affinityFileNo(i))
    newSeeds = updateSeeds(seeds, options.factor)

    if len(newSeeds) == 0:
        raise Exception("got no new seeds for the next round. this is probably due to a bad parameter for -f")

    print "number of seeds ", len(newSeeds)
    writeSeedFile(newSeeds, seedFileNo(i+1))

#shutil.copy2(affinityFileNo(options.rounds-1), options.affinities)
