#!/usr/bin/env python2

import sys
import datetime
from optparse import OptionParser

from communityutils import *


##########################################
#
# COMMAND LINE INTERFACE

def commandline_interface():
    parser = OptionParser()
   
    parser.add_option("-g", dest="graph_file_input", type="string",
            help="Input: LFR benchmark graph file")
    parser.add_option("-G", dest="graph_file_output", type="string",
            help="Output: custom graph file")

    parser.add_option("-c", dest="community_file_input", type="string",
            help="Input: LFR benchmark community network")
    parser.add_option("-C", dest="community_file_output", type="string",
            help="Output: custom community file")

    parser.add_option("-S", dest="seed_nodes", type="string",
            help="Output: custom seed-node file")
    parser.add_option("-n", dest="seed_frac", type="float",
            help="fraction of seed nodes (in range 0.0 to 1.0)")

    parser.add_option("-s", dest="seed_strategy", type="string",default="uniform",
            help="strategy for picking seed nodes (uniform,degree)")
   
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

    graph = Graph()
    graph.readGraphLFR(options.graph_file_input)

    if not graph.isConnected():
        # fail if graph is not connected
        sys.stderr.write(datetime.datetime.now() + " - ERROR: Graph file is not one connected component.\n")
        sys.exit(1)
    else:
        # proceed if graph is connected

        #write the graph to file in our custom format
        graph.writeGraphCustom(options.graph_file_output)

        # read, process, and write community file
        communities = Communities()
        communities.readCommunitiesLFR(options.community_file_input)
        communities.writeCommunitesCustom(options.community_file_output)

        # pick seeds and write seed file
        if options.seed_strategy == "uniform":
            seeds = communities.generateSeeds(options.seed_frac)
        elif options.seed_strategy == "degree":
            seeds = communities.generateHighestDegreeSeeds(graph, options.seed_frac)
        else:
            raise Exception("unknown parameter {0} for strategy".format(options.seed_strategy))
        
        communities.writeSeedsCustom(seeds, options.seed_nodes)
