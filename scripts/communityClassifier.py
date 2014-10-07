#!/usr/bin/env python2

import sys
from optparse import OptionParser
from collections import defaultdict

from communityutils import *


##########################################
#
# COMMAND LINE INTERFACE

def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-a", dest="affinity_file", type="string",
        help="Input: affinity vectors, as given by the c++ algorithm")

    parser.add_option("-c", dest="actual_communities_file", type="string",
            help="Output: classified communities")

    parser.add_option("-C", dest="classified_communities_file", type="string",
            help="Output: classified communities")
    
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

    return True


##########################################
#
# MAIN PROGRAM

options, args = 0, 0
if commandline_interface():

    affinities = Affinities()
    affinities.readAffinitiesCustom(options.affinity_file)

    actualCommunities = Communities()
    actualCommunities.readCommunitiesLFR(options.actual_communities_file)

    communities = Communities()
    #communities.classifyCommunities(affinities)
    communities.classifyCommunitiesOverlapping(affinities, actualCommunities)
    communities.writeCommunitesCustom(options.classified_communities_file)
