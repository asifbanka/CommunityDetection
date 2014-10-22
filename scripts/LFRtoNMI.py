#!/usr/bin/env python2

import subprocess as sp
import os
import sys
import datetime
from optparse import OptionParser

##########################################
#
# COMMAND LINE INTERFACE


#TODO: add option to use config files like this:
#http://stackoverflow.com/questions/1880404/using-a-file-to-store-optparse-arguments

parser = OptionParser()

# parameters for the LFR benchmark
parser.add_option("-N", "--N",                 dest="lfr_N",                   help="number of nodes")
parser.add_option("-k", "--k",                 dest="lfr_k",                   help="average degree")
parser.add_option("--maxk",                    dest="lfr_maxk",                help="maximum degree")
parser.add_option("--mu",                      dest="lfr_mu",                  help="mixing parameter")
parser.add_option("--t1",                      dest="lfr_t1",                  help="minus exponent for the degree sequence")
parser.add_option("--t2",                      dest="lfr_t2",                  help="minus exponent for the community size distribution")
parser.add_option("--minc",                    dest="lfr_minc",                help="minimum for the community sizes")
parser.add_option("--maxc",                    dest="lfr_maxc",                help="maximum for the community sizes")
parser.add_option("--on",                      dest="lfr_on",                  help="number of overlapping nodes")
parser.add_option("--om",                      dest="lfr_om",                  help="number of memberships of the overlapping nodes")
parser.add_option("-C", "--C",                 dest="lfr_C",                   help="[average clustering coefficient]")

# parameters for our scripts
parser.add_option("-o",                        dest="output_file",             help="write the nmi value to this file")
parser.add_option("-s",                        dest="seed_frac",               help="the percentage of seed nodes")
parser.add_option("-i",                        dest="iterations", type="int",  help="the number of iterations for the iterative method")
parser.add_option("--seed_strategy",           dest="seed_strategy",           help="strategy for picking seed nodes")
parser.add_option("--classification_strategy", dest="classification_strategy", help="strategy for the classifier")

options, args = parser.parse_args()

valid = True
if not (options.output_file and
        options.seed_frac and
        options.iterations and
        options.seed_strategy and
        options.classification_strategy):
    valid = False

if valid == False:
    parser.print_help()
    exit(1)


##########################################
# 
# SETTINGS

iterative_strategy="fraction"
iterative_factor=1.1


##########################################
# 
# EXECUATBLES

ROOT = os.path.dirname(os.path.realpath(__file__)) + "/.."
LFR = ROOT + "/external/binary_networks/benchmark"
communityDetectionIterative = ROOT + "/scripts/communityDetectionIterative.py"
communityClassifier = ROOT + "/scripts/communityClassifier.py"
graphParser = ROOT + "/scripts/graphParser.py"
NMI = ROOT + "/external/NMI/mutual"


##########################################
# 
# TEMPORARY FILES

# the graph output of the lfr
graphLFR = "network.dat"
# the community output of the lfr
communitiesLFR = "community.dat"
# the graph generated by the graph parser
graph = "tmp_graph"
# the community file generated by the graph parser
communities = "tmp_communities"
# the seed-node file generated by the graph parser
seedNodes = "tmp_seedNodes"
# the affinity output from the c++ algorithm
affinities = "tmp_affinies"
# the output from the community classifier
detectedCommunities = "tmp_detectedCommunities"


######################################
#
# MAIN

try:
    print "=> run LFR"
    call = [LFR]
    if options.lfr_N: call.extend(["-N", options.lfr_N])
    if options.lfr_k: call.extend(["-k", options.lfr_k])
    if options.lfr_maxk: call.extend(["-maxk", options.lfr_maxk])
    if options.lfr_mu: call.extend(["-mu", options.lfr_mu])
    if options.lfr_t1: call.extend(["-t1", options.lfr_t1])
    if options.lfr_t2: call.extend(["-t2", options.lfr_t2])
    if options.lfr_minc: call.extend(["-minc", options.lfr_minc])
    if options.lfr_maxc: call.extend(["-maxc", options.lfr_maxc])
    if options.lfr_on: call.extend(["-on", options.lfr_on])
    if options.lfr_om: call.extend(["-om", options.lfr_om])
    if options.lfr_C: call.extend(["-C", options.lfr_C])
    sp.check_call(call)

    print "=> convert the LFR files to our file format and get the seed nodes"
    sp.check_call([graphParser,
        "-g", graphLFR,
        "-G", graph,
        "-c", communitiesLFR,
        "-C", communities,
        "-S", seedNodes,
        "-n", options.seed_frac,
        "--seed_strategy", options.seed_strategy])

    print "=> perform community detection"
    sp.check_call([communityDetectionIterative,
        "-g", graph,
        "-s", seedNodes,
        "-A", affinities,
        "-i", str(options.iterations),
        "--iterative_strategy", iterative_strategy,
        "--iterative_factor", str(iterative_factor),
        "--classification_strategy", options.classification_strategy])


    print "=> classify communities and calculate NMI"
    nmis = []
    for i in range(options.iterations):

        affinities_i = affinities + "_" + str(i)
        detectedCommunities_i = detectedCommunities + "_" + str(i)

        sp.check_call([communityClassifier,
            "-a", affinities_i,
            "-c", communitiesLFR,
            "--classification_strategy", options.classification_strategy,
            "-C", detectedCommunities_i])

        output = sp.Popen([NMI, communities, detectedCommunities_i], stdout=sp.PIPE).communicate()[0]
        nmis.append(output.split()[1])

    with open (options.output_file, "w") as f:
        f.writelines("\n".join(nmis))

    os.remove(graphLFR)
    os.remove(communitiesLFR)
    os.remove(graph)
    os.remove(communities)
    os.remove(seedNodes)
    for i in range(options.iterations):
        os.remove(seedNodes + "_" + str(i))
        os.remove(affinities + "_" + str(i))
        os.remove(detectedCommunities + "_" + str(i))
    os.remove(seedNodes + "_" + str(options.iterations))

    print ""
    print "======================="
    print ""
    print ""
    print "NMI:" 
    print "----"
    with open (options.output_file, "r") as f: print f.read()


# in case one of the scripts fail
except sp.CalledProcessError:
    sys.stderr.write(str(datetime.datetime.now()) + " - ERROR in subprocess.\n")
    sys.exit(1)
