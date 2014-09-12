#!/usr/bin/python
import sys
from optparse import OptionParser
from collections import defaultdict
import re

# interface
def setup_commandline():
    usage = "usage: %prog"
    parser = OptionParser()
    parser.add_option("-a", dest="affinity_file", type="string",
        help="belonging vector output of the markov chain algorithm")
    global options, args
    (options, args) = parser.parse_args()

    if (len(args) == 0):
        parser.error("Incorrect number of arguments")
        parser.print_help()
        return True

    elif not options.affinity_file:
        parser.error("Affinity file not given")
        parser.print_help()
        return False

    return True

# read LFR network file
def read_affinity(file):
    with open (file, "r") as f:
        affinities = defaultdict(list)
        number = re.compile(r'([\d.]*\d+)')
        # store affinities
        next(f)
        for i, line in enumerate(f):
            max_affinity = 0
            min_affinity = 1
            match = number.findall(line.strip())
            for m in match[1:]:
                affinities[int(match[0])].append(float(m))
                # derive maximum and minimum for later classification
                if float(m) > max_affinity:
                    max_affinity = float(m)
                elif float(m) < min_affinity:
                    min_affinity = float(m)
            affinities[int(match[0])].append(float(min_affinity))
            affinities[int(match[0])].append(float(max_affinity))
    print affinities
    return affinities

# evaluate communities
def classify_communities(affinities):
    community_vertices = defaultdict(list)
    for vertex in affinities:
        # check max affinity for classification
        if affinities[vertex][-1] < 0.5:
            threshold = (affinities[vertex][-1] + affinities[vertex][-2]) /2
        else:
            threshold = 0.5
        affinities[vertex].append(threshold)
        for index, affinity in enumerate(affinities[vertex][:-3]):
            if affinity >= affinities[vertex][-1]:
                community_vertices[index].append(vertex)
    print community_vertices
    return community_vertices

#write output community file
def write_communites(community_vertices):
    with open ("classified_communities", "w") as file:
        for vertices in community_vertices:
            file.write("{0}".format(community_vertices[vertices][0]))
            for v in community_vertices[vertices][1:]:
               file.write(" {0}".format(v))
            file.write("\n")

# main program
options, args = 0, 0
#if setup_commandline():
affinities = read_affinity(sys.argv[1])
community_vertices = classify_communities(affinities)
write_communites(community_vertices)