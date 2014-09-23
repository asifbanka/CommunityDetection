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

# takes only those seed entries which have a maximum value of at least "threshold"
# the maximum values are set to 1, all other values are set to 0
def addSeedsByThreshold(seeds, threshold):
    newSeeds = defaultdict(list)
    for nodeId, affinities in seeds.iteritems():
        maxIndex = np.argmax(affinities)
        if(affinities[maxIndex]) >= threshold:
            newAffinities = ([0.0] * len(affinities))
            newAffinities[maxIndex] = 1.0
            newSeeds[nodeId] = newAffinities

            if affinities[maxIndex] != 1: 
                print "add seed with affinity", affinities[maxIndex]

    return newSeeds

# increase the number of seed nodes by a factor "factor". Add the nodes with the greatest max-affinity value
# the maximum values are set to 1, all other values are set to 0
def addSeedsByFactor(seeds, factor):
    numberOfSeedNodes = sum(1 for x in seeds.values() if max(x) == 1)
    numberOfNewSeedNodes = int(math.ceil(numberOfSeedNodes * factor))
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


########################################################

# parse the parameters
parser = OptionParser()
parser.add_option("-g", "--graph", dest="graph")
parser.add_option("-s", "--seed", dest="seed", help="")
parser.add_option("-a", "--affinities", dest="affinities")
parser.add_option("-i", "--iterations", dest="iterations", type="int")
parser.add_option("-t", "--iterations_threshold", dest="iterations_threshold", type="float" )
parser.add_option("-f", "--iterations_factor", dest="iterations_factor", type="float" )
(options, args) = parser.parse_args()

valid = True
if not (options.graph and 
        options.seed and 
        options.affinities and 
        options.iterations):
    print "ERROR: wrong parameters"
    print "usage: -g graph -s seed -a affinities -i iterations"
    valid = False

if (options.iterations_factor == None) == (options.iterations_threshold == None):
    print "the -t and the -f flag are mutually exclusive"
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
writeSeedFile(seeds, seedFileNo(0))

for i in range(options.iterations):

    print "------------"

    returnValue = sp.call([pathToAlgorithm , options.graph , seedFileNo(i) , affinityFileNo(i)], shell=False)
    if returnValue != 0:
        print "error in subprocess"
        exit(1)

    print "read seed nodes from", affinityFileNo(i), ", modify them, and write them to", seedFileNo(i+1)
    seeds = readSeedFile(affinityFileNo(i))

    newSeeds = 0
    if(options.iterations_factor):
        print "add seeds by factor"
        newSeeds = addSeedsByFactor(seeds, options.iterations_factor)
    else:
        print "add seeds by threshold"
        newSeeds = addSeedsByThreshold(seeds, options.iterations_threshold)

    if len(newSeeds) == 0:
        raise Exception("got no new seeds for the next round. this is probably due to bad parameters for -t and -f")

    print "number of seeds ", len(newSeeds)
    writeSeedFile(newSeeds, seedFileNo(i+1))

#shutil.copy2(affinityFileNo(options.iterations-1), options.affinities)
