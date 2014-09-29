#!/usr/bin/env python2

from collections import defaultdict
from collections import deque
from random import sample
from math import ceil

##########################################
#
# GRAPH
# 
# This class stores parses the graph from the LFR-fileformat to our 
# custom-fileformat and checks if the graph is connected.
#
# Internally, the graph is represented as a dictionary called "vertexToNeighbours". 
# This dictionary maps the ids of each node (starting at 0) to its neighbours

class Graph(object):
    def __init__(self):
        self.vertexToNeighbours = None
        self.numEdges = None
        self.numVertices = None


    # Read LFR network file.
    # In the LFR file the ids start at 1. we subtract 1 to let the ids start at 0.
    def readGraphLFR(self,filename):
        with open (filename, "r") as f:

            # split strings into ints on whitespaces and subtract 1 from each value
            edges = [[(int(vertex)-1) for vertex in line.split()] for line in f.readlines()]

            self.vertexToNeighbours = defaultdict(list)
            for edge in edges:
                if len(edge) != 2:
                    raise Exception("there must be exactly two entries in each line of the input graph")
                self.vertexToNeighbours[edge[0]].append(edge[1])
        self.numVertices = len(self.vertexToNeighbours)
        self.numEdges = 0
        for neighbours in self.vertexToNeighbours.values():
            self.numEdges += len(neighbours)


    # Write output graph in our custom format
    # The number and nodes and edges are written in the first line, then a list of edges follow.
    def writeGraphCustom(self, filename):
        with open (filename, "w") as f:
            f.write("{0} {1}".format(self.numVertices, self.numEdges))
            for v, neighbours in self.vertexToNeighbours.iteritems():
                for n in neighbours:
                    f.write("\n{0} {1}".format(v, n))


    # Check connectivity by performing a dfs search.
    def isConnected(self):
        visited = set() 
        # start at node 0
        queue = deque([0])
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                for neighbour in self.vertexToNeighbours[vertex]:
                    if neighbour not in visited:
                        queue.append(neighbour)
        return len(visited) == len(self.vertexToNeighbours)



##########################################
#
# AFFINITIES
#
# This class deals with the affinity output from the c++ algorithm.
# 
# Affinities are stored as a dict which maps the nodeid to an affinity-vector.
# The i-th index in this vector represents the affinity to the i-th community
# This strucure is called vertexToAffinities

class Affinities(object):
    def __init__(self):
        self.vertexToAffinities  = None

    # Read output from c++ algorithm to affinity-dict.
    def readAffinitiesCustom(self, filename):

        self.vertexToAffinities = defaultdict(list)
        with open (filename, "r") as f:

            firstRow = f.readline().split()
            if len(firstRow) != 2:
                raise Exception("first line should have exactly two entries")
            numberOfNodes = int(firstRow[0])
            numberOfCommunities = int(firstRow[1])

            for line in f.readlines():
                split = line.split()
                nodeId = int(split[0])
                self.vertexToAffinities[nodeId] = [float(a) for a in split[1:]]

                if len(self.vertexToAffinities[nodeId]) != numberOfCommunities:
                    raise Exception("wrong number of communities")

                #communitiesPerVertex = 1
                #s = sum(self.vertexToAffinities[nodeId])
                #if not ( communitiesPerVertex - 0.01 < s and s < communitiesPerVertex + 0.01):
                    #raise Exception("rows dont sum up")

            if len(self.vertexToAffinities) != numberOfNodes:
                raise Exception("wrong number of nodes")


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


    # A helper function which calculates "communityToVerties" and 
    # "numberOfCommunities" from "vertexToCommunities".
    def _reverseMapping(self):
        # remap value list as keys, keys as values
        self.communityToVertices = defaultdict(list)
        for vertex, communities in self.vertexToCommunities.iteritems():
            for c in communities:
                self.communityToVertices[c].append(vertex)
        self.numberOfCommunities = len(self.communityToVertices)            


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
        self._reverseMapping()


    # Classify communities from the affinity output of the c++ algorithm.
    # Simply assign the vertex the the community with the maximum affinity-value.
    def classifyCommunities(self, affinities):
        communitiesPerVertex = 1
        self.vertexToCommunities = defaultdict(list)
        for vertex, affinities in affinities.vertexToAffinities.iteritems():
            # Put affinities with their index (the corresponding community) in tuple 
            # and sort them by first entry (affinity). 
            # Then extract the second entry (the community) from each tuple.
            sortedTuples = sorted([(v,i) for i,v in enumerate(affinities)])
            # The list was sorted ascending, so take communities from the end.
            communities = [i for (v,i) in sortedTuples][-communitiesPerVertex:]
            self.vertexToCommunities[vertex] = communities
        self._reverseMapping()


    # Write output community file.
    # Each line represents one community and lists all the vertices in this community.
    def writeCommunitesCustom(self, filename):
        with open (filename, "w") as f:
            for vertices in self.communityToVertices.values():
                f.write(" ".join([str(x) for x in vertices]) + "\n")


##########################################
#
# SEEDS
#
# Seeds are picked from the communities-object and stored as a set of vertex ids

class Seeds(object):
    def __init__(self, communities):
        self.seeds = None
        self.communities = communities

    # Generate seed nodes from a community object.
    # Pick a fraction of "seedFraction" nodes from each community.
    # The number of seeds per community is at least 1 and rounded to the next bigger integer
    def generateSeeds(self, seedFraction):
        self.seeds = set()
        for c in self.communities.communityToVertices:
            if seedFraction == 0:
                seedCount = 1
            else:
                seedCount = int(ceil(seedFraction * len(self.communities.communityToVertices[c])))
            self.seeds = self.seeds.union(sample(self.communities.communityToVertices[c], seedCount))
        

    # Write seed-information to file in affinity-fileformat.
    def writeSeedsCustom(self, filename):
        if self.seeds is None:
            raise Exception("seeds need to be generated first")
        with open (filename, "w") as f:
            
            f.write("{0} {1}".format(len(self.seeds), self.communities.numberOfCommunities))
            for seed in self.seeds:
                tmp = [0] * self.communities.numberOfCommunities
                for community in self.communities.vertexToCommunities[seed]:
                    tmp[community] = 1
                f.write("\n" + str(seed) + " " + " ".join([str(x) for x in tmp]))
