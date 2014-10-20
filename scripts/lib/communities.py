#!/usr/bin/env python2

import numpy.random as npr
from collections import defaultdict
from collections import deque
from random import sample
from math import ceil
import math_tools
import json

##########################################
#
# COMMUNITIES
#
# This class contains the community information of the network.
# This information can eithe be read from the LFR-output or 
# deduced from the affinity output of the c++ algorithm.
#
# Community information can be accessed in two different ways:
# * The dict "vertexToCommunities" maps each vertex to the communities it belongs to.
# * The dict "communityToVertices" maps each community to the vertices which are part of it.

class Communities(object):

    def __init__(self):
        self.vertexToCommunities = None
        self.communityToVertices = None
        self.numberOfCommunities = None


    def reverseMapping(self, inputDict):
        outputDict = defaultdict(list)
        # remap value list as keys, keys as values
        for key, listOfKey in inputDict.iteritems():
            for element in listOfKey:
                outputDict[element].append(key)
        return outputDict

    # input and output
    # ----------------

    # Read community information from the LFR community file.
    # The input is a file which where each line consists 
    # of a nodeid and then a list of communities this node belongs to
    # Ids of nodes and communities in the LFR file start at 1, 
    # we subtract 1 to let those ids start at 0.
    def readCommunitiesLFR(self, filename):
        self.vertexToCommunities = defaultdict(list)
        with open (filename, "r") as f:
            belongings = [[(int(x) - 1) for x in line.split()] for line in f.readlines()]
            for belonging in belongings:
                self.vertexToCommunities[belonging[0]] = belonging[1:]
        self.communityToVertices = self.reverseMapping(self.vertexToCommunities)
        self.numberOfCommunities = len(self.communityToVertices) 


    #the same as readCommunitiesLFR but reads our file format instead    
    #TODO: what format are you talking about?
    #TODO: this function seems buggy: vertices are not cast to int
    def readCommunitiesOurFormat(self, filename):
        self.communityToVertices = defaultdict(list)
        with open (filename, "r") as f:
            for community,line in enumerate(f):
                for vertex in line.split():
                    self.communityToVertices[community].append(vertex)
        self.vertexToCommunities = self.reverseMapping(self.communityToVertices)
        self.numberOfCommunities = len(self.communityToVertices)             


    # Write output community file.
    # Each line represents one community and lists all the vertices in this community.
    def writeCommunitesOurFormat(self, filename):
        with open (filename, "w") as f:
            for vertices in self.communityToVertices.values():
                f.write(" ".join([str(x) for x in vertices]) + "\n")


    # Write seed-information to file in affinity-fileformat.
    # seeds is a set of nodeids
    def writeSeedsOurFormat(self, seeds, filename):
        if seeds is None:
            raise Exception("seeds need to be generated first")
        with open (filename, "w") as f:
            
            f.write("{0} {1}".format(len(seeds), self.numberOfCommunities))
            for seed in seeds:
                tmp = [0] * self.numberOfCommunities
                for community in self.vertexToCommunities[seed]:
                    tmp[community] = 1
                f.write("\n" + str(seed) + " " + " ".join([str(x) for x in tmp]))


    # methods for generating seeds
    # ----------------------------

    # Generate seed nodes from a community object.
    # Pick a fraction of "seedFraction" nodes from each community.
    # The number of seeds per community is at least 1 and rounded to the next bigger integer
    def generateSeedsUniformly(self, seedFraction):
        seeds = set()
        for c in self.communityToVertices:
            if seedFraction == 0:
                seedCount = 1
            else:
                seedCount = int(ceil(seedFraction * len(self.communityToVertices[c])))
            seeds = seeds.union(sample(self.communityToVertices[c], seedCount))
        return seeds


    def generateSeedsDegreeBased(self, graph, seedFraction):
        seeds = set()

        for c, vertices in self.communityToVertices.iteritems():
            communityDegree = 0

            probabilities = list()
            for vertex in vertices:
                communityDegree += len(graph.vertexToNeighbours[vertex])

            for vertex in vertices:
                probabilities.append(len(graph.vertexToNeighbours[vertex]) / float(communityDegree))

            if seedFraction == 0:
                seedCount = 1
            else:
                seedCount = int(ceil(seedFraction * len(self.communityToVertices[c])))

            tmp = math_tools.choice(vertices, seedCount, replace=False, p=probabilities)
            seeds = seeds.union(tmp)
        return seeds

    # stuff
    # ----------------------------

    #Find position of biggest gap            
    def getGap(self,affinityVector):
        affinitytuple = list()

        #create new data structure with community id and correspodning affinity
        for i, affinity in enumerate(affinityVector):
            affinitytuple.append((i,affinity))

        affinitytuple = sorted(affinitytuple,key=lambda item: item[1], reverse=True)

        #Find position of maximum gap
        maxDiff = 0
        maxDiffPosition = -1
        for i in xrange(0,len(affinitytuple[:-1])):
            currentDiff = affinitytuple[i][1] - affinitytuple[i+1][1]
            if currentDiff > maxDiff:
                maxDiff = currentDiff
                maxDiffPosition = i

        first_half = affinitytuple[:maxDiffPosition+1]
        communities = list()
        for element in first_half:
            communities.append(element[0])
        return communities, maxDiffPosition, maxDiff       


    def getJSONOfVertex(self,affinities, groundTruth, vertex):
        affinity_vector = affinities.vertexToAffinities[vertex]
        deviation = math_tools.standartDeviation(affinity_vector)
        communities_according_to_gap,gap_position ,gap_size = self.getGap(affinity_vector)  

        actual_communities = groundTruth.vertexToCommunities[vertex]
        detected_communities = self.vertexToCommunities[vertex]

        return {
            "nodeid":vertex,
            "actual_communities":actual_communities,
            "actual_number_of_communities":len(actual_communities),
            "detected_communities":detected_communities,
            "detected_number_of_communities":len(detected_communities),

            "gap_position":gap_position,
            "standard_deviation":deviation,
            "affinities":affinity_vector,
            "gap_size":gap_size,
            "communities_according_to_gap":communities_according_to_gap}


    def writeJSONfile(self, filename, affinities, groundTruth):
        output = list()
        for vertex in self.vertexToCommunities:
            output.append(self.getJSONOfVertex(affinities, groundTruth, vertex))

        with open (filename, "w") as f:
            f.write(json.JSONEncoder(indent=4).encode({"body": output}))


    # classification
    # --------------

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


    # Classify communities from the affinity output of the c++ algorithm.
    # Assign communities according to "gap-strategy"
    def classifyCommunitiesWithGaps(self, affinities):
        self.vertexToCommunities = defaultdict(list)
        for vertex, affinities in affinities.vertexToAffinities.iteritems():
            communities,gapPosition,gapSize = self.getGap(affinities)
            self.vertexToCommunities[vertex] = communities
        self.communityToVertices = self.reverseMapping(self.vertexToCommunities)
        self.numberOfCommunities = len(self.communityToVertices)


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


