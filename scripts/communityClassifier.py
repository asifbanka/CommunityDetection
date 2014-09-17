#!/usr/bin/env python2

import sys
from optparse import OptionParser
from collections import defaultdict
import re

# interface
def commandline_interface():
    usage = "usage: %prog"
    parser = OptionParser()
    
    # command line options
    parser.add_option("-a", dest="affinity_file", type="string",
        help="belonging vector output of the markov chain algorithm")

    parser.add_option("-c", dest="classified_communities", type="string",
        help="classified communities, the output of this script")
    
    parser.add_option("-o", dest="overlapping", type="int", default=0,
        help="if communities are overlapping set to 1, otherwise to 0 (default)")
    
    global options, args
    (options, args) = parser.parse_args()

    if not options.affinity_file:
        parser.error("Affinity file not given")
        parser.print_help()
        return False

    elif options.overlapping != 1 and options.overlapping != 0:
        parser.error("Invalid overlap parameter")
        parser.print_help()
        return False

    elif not options.classified_communities:
        parser.error("Output file not given")
        parser.print_help()
        return False

    return True

# read LFR network file
def read_affinity(file):
    with open (file, "r") as f:
        affinities = defaultdict(list)
        next(f) # overread first line 
        for i, line in enumerate(f):
            # affinity value range is [0, 1]
            max_affinity = 0
            min_affinity = 1
            numbers = line.split()
            # iterate over affinity values of vertex
            for m in numbers[1:]:
                affinities[int(numbers[0])].append(float(m))

                # derive maximum and minimum for later classification
                if float(m) > max_affinity:
                    max_affinity = float(m)
                elif float(m) < min_affinity:
                    min_affinity = float(m)
            # append max and min at the end for easy access later on
            affinities[int(numbers[0])].append(float(min_affinity))
            affinities[int(numbers[0])].append(float(max_affinity))
    return affinities

# evaluate communities
def classify_communities(affinities):
    community_vertices = defaultdict(list)
    for vertex in affinities:
        # determine classification threshold
        max_affinity = affinities[vertex][-1]
        min_affinity = affinities[vertex][-2]
        # if non overlapping just set threshold as maximum affinity
        if options.overlapping == 0:
            threshold = max_affinity 
        # overlapping
        else: 
            # if the max affinity is smaller 0.5 pick the mid range value 
            if affinities[vertex][-1] < 0.5:
                threshold = (max_affinity  + min_affinity) / 2
            else:
                threshold = 0.5

        # construct communities
        for index, affinity in enumerate(affinities[vertex][:-2]):
            if affinity >= threshold:
                community_vertices[index].append(vertex)

    return community_vertices

#write output community file
def write_communites(community_vertices):
    with open (options.classified_communities, "w") as file:
        for community in community_vertices:
            file.write("{0}".format(community_vertices[community][0]))
            
            for v in community_vertices[community][1:]:
                file.write(" {0}".format(v))
            file.write("\n")


# main program
options, args = 0, 0
if commandline_interface():
    affinities = read_affinity(options.affinity_file)
    community_vertices = classify_communities(affinities)
    write_communites(community_vertices)
