#!/usr/bin/env python2

import numpy.random as npr
from collections import defaultdict
from collections import deque
from random import sample
from math import ceil
import math_tools
#import statistics   only in 3.2 so sad
import json

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


    def readGraphOurFormat(self,filename):
        with open (filename, "r") as f:     
            edges = [[(int(vertex)) for vertex in line.split()] for line in f.readlines()[1:]]

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
    def writeGraphOurFormat(self, filename):
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

    def isSymmetric(self):
        for node, neighbours in self.vertexToNeighbours.iteritems():
            for neighbour in neighbours:
                if not node in self.vertexToNeighbours[neighbour]:
                    return False
        return True



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
    def readAffinitiesOurFormat(self, filename):

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

