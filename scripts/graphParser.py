#!/usr/bin/env python2

import sys
import datetime
from optparse import OptionParser
from collections import defaultdict
from collections import deque
from random import sample
from math import ceil

##########################################
#
# GRAPH
#
# Internally, the graph is represented as a dictionary. 
# This dictionary maps the ids of each node (starting at 0) to its neighbours


# Read LFR network file.
# In the LFR file the ids start at one. we subtract 1 to let the ids start at 0.
def readGraph(filename):
    with open (filename, "r") as f:

        # split strings into ints on whitespaces and subtract 1 from each value
        edges = [[(int(vertex)-1) for vertex in line.split()] for line in f.readlines()]

        graph = defaultdict(list)
        for edge in edges:
            if len(edge) != 2:
                raise Exception("there must be exactly two entries in each line of the input graph")
            graph[edge[0]].append(edge[1])
    return graph


# Write output graph in our custom format
# The number and nodes and edges are written in the first line, then a list of edges follow.
def writeGraph(graph, filename):
    numVertices = len(graph)
    numEdges = 0
    for neighbours in graph.values():
        numEdges += len(neighbours)
    with open (filename, "w") as f:
        f.write("{0} {1}".format(numVertices, numEdges))
        for v, neighbours in graph.iteritems():
            for n in neighbours:
                f.write("\n{0} {1}".format(v, n))


# Check connectivity by performing a dfs search.
def isConnected(graph):
    visited = set() 
    # start at node 0
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            for neighbour in graph[vertex]:
                if neighbour not in visited:
                    queue.append(neighbour)
    return len(visited) == len(graph)


##########################################
#
# COMMUNIY INFORMATION
#
# Community information is stored internally in two different ways:
# 
# The first is a map which maps each vertex to the communities it belongs to.
# This structure will be called "vertexToCommunities"
# 
# The second one maps each community to the vertices which are part of it
# this structure is called "communityToVertices".


# Read LFR community file.
# The input is a file which where each line consists 
# of a nodeid and then a list of communities this node belongs to
# Ids of nodes and communities in the LFR file start at 1, we subtract 1 to let those ids start at 0.
# Returns vertexToCommunities and communityToVertices, as decribed above.
def readCommunities(filename):
    vertexToCommunities = defaultdict(list)
    with open (filename, "r") as f:
        belongings = [[(int(x) - 1) for x in line.split()] for line in f.readlines()]
        for belonging in belongings:
            vertexToCommunities[belonging[0]] = belonging[1:]

    # remap value list as keys, keys as values
    communityToVertices = defaultdict(list)
    for vertex, communities in vertexToCommunities.iteritems():
        for c in communities:
            communityToVertices[c].append(vertex)

    return vertexToCommunities, communityToVertices

# Write output community file.
# Each line represents one community and lists all the vertices in this community.
def writeCommunites(communityToVertices, filename):
    with open (filename, "w") as f:
        for vertices in communityToVertices.values():
            f.write(" ".join([str(x) for x in vertices]) + "\n")


##########################################
#
# SEEDS
#
# seeds are stored in a set


# Generate seed nodes.
# Pick a fraction of "seedFraction" nodes from each community.
# The number of seeds per community is at least 1 and rounded to the next bigger integer
def generateSeeds(communityToVertices, seedFraction):
    seeds = set()
    for c in communityToVertices:
        if seedFraction == 0:
            seedCount = 1
        else:
            seedCount = int(ceil(seedFraction * len(communityToVertices[c])))
        seeds = seeds.union(sample(communityToVertices[c], seedCount))
    return seeds


# Write seed-information to file.
def writeSeeds(seeds, communityToVertices, vertexToCommunities, filename):
    with open (filename, "w") as f:
        numberOfCommunities = len(communityToVertices)
        f.write("{0} {1}".format(len(seeds), numberOfCommunities))
        for seed in seeds:
            tmp = [0] * numberOfCommunities
            for community in vertexToCommunities[seed]:
                tmp[community] = 1
            f.write("\n" + str(seed) + " " + " ".join([str(x) for x in tmp]))


##########################################
#
# COMMAND LINE INTERFACE


def commandline_interface():
    usage = "usage: %prog"
    parser = OptionParser()
   
    parser.add_option("-g", dest="graph_file_input", type="string",
            help="Input: LFR benchmark graph file")
    parser.add_option("-G", dest="graph_file_output", type="string",
            help="Output: custom graph file")

    parser.add_option("-c", dest="community_file_input", type="string",
            help="Input: LFR benchmark community network")
    parser.add_option("-C", dest="community_file_output", type="string",
            help="Output: custom community file")

    parser.add_option("-s", dest="seed_nodes", type="string",
            help="Output: custom seed-node file")
    parser.add_option("-n", dest="seed_frac", type="float",
            help="fraction of seed nodes (in range 0.0 to 1.0)")
   
    global options, args
    (options, args) = parser.parse_args()

    if not options.graph_file_input:
        parser.error("input graph file not given")
        parser.print_help()
        return False

    elif not options.graph_file_output:
        parser.error("output graph file not given")
        parser.print_help()
        return False

    elif not options.community_file_input:
        parser.error("input community file not given")
        parser.print_help()
        return False

    elif not options.community_file_output:
        parser.error("output community file not given")
        parser.print_help()
        return False

    elif not options.seed_nodes:
        parser.error("output seed-node file not given")
        parser.print_help()
        return False

    elif not hasattr(options, "seed_frac"):
        parser.error("seed-node fraction not given")
        parser.print_help()
        return False

    return True


##########################################
#
# MAIN PROGRAM

options, args = 0, 0
if commandline_interface():

    graph = readGraph(options.graph_file_input)

    if not isConnected(graph):
        # fail if graph is not connected
        sys.stderr.write(datetime.datetime.now() + " - ERROR: Graph file is not one connected component.\n")
        sys.exit(1)
    else:
        # proceed if graph is connected

        #write the graph to file in our custom format
        writeGraph(graph, options.graph_file_output)

        # read, process, and write community file
        vertexToCommunities, communityToVertices = readCommunities(options.community_file_input)
        writeCommunites(communityToVertices, options.community_file_output)

        # pick seeds and write seed file
        seeds = generateSeeds(communityToVertices, options.seed_frac)
        writeSeeds(seeds, communityToVertices, vertexToCommunities, options.seed_nodes)
