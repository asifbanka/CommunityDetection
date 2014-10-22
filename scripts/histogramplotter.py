#!/usr/bin/env python2

import sys
import json
from collections import defaultdict
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint

##########################################
#
# COMMAND LINE INTERFACE

def commandline_interface():
    parser = OptionParser()

    parser.add_option("-i", dest="input_file", type="string",
            help="input file in json format")
   
    parser.add_option("-o", dest="output_file", type="string",
            help="deduces fileformat automatically. *.pdf or *.png works")

    parser.add_option("-f", dest="json_fields", type="string",
            help="whitespace separated list of fields to plot")
   
    global options, args
    (options, args) = parser.parse_args()

    if not (options.output_file and
            options.input_file and
            options.json_fields):
        parser.print_help()
        return False

    return True


##########################################
#
# PARSING


# Returns the json-file contend grouped by number_of_communities.
#
# The return-value can be accessed like this:
#
# aggregated[2]["gap_position"] returns the list of all 
# gap-positions of vertices # which belong to 2 communities.

def aggregatedata(filename, jsonkeys):
    with open(filename) as f:
        data = json.load(f)
    aggregated = defaultdict(lambda : defaultdict(list))
    for jsonkey in jsonkeys:
        for entry in data["body"]:
            k = entry["actual_number_of_communities"]
            aggregated[k][jsonkey].append(entry[jsonkey])
    return aggregated


##########################################
#
# PLOTTING

colors = ['b', 'y', 'r', 'g']
colorindex = -1
def getCycledColor():
    global colorindex
    if colorindex < len(colors) - 1:
        colorindex = colorindex + 1
        return colors[colorindex]
    else:
        colorindex = -1

def addhistbar(ax, values):

    #for integers each int should be an individual bin
    #floats shall be placed in a fixed number of bins
    if all(isinstance(item, int) for item in values):
        hist, bins = np.histogram(values, bins=range(min(values)-1, max(values)+1))
    else:
        hist, bins = np.histogram(values, bins=50)

    center = (bins[:-1] + bins[1:]) / 2
    width = 1.0 * (bins[1] - bins[0])

    return ax.bar(center, hist, align='center', width=width, linewidth=0, alpha=0.5, facecolor=getCycledColor())


##########################################
#
# MAIN

#parse parameters
options, args = 0, 0
if not commandline_interface():
    sys.exit(1)

#parse data
jsonkeys = options.json_fields.split()
aggregated = aggregatedata(options.input_file, jsonkeys)

#plot data
fig, ax = plt.subplots()
legends = []
for jsonkey in jsonkeys:
    for k in aggregated.keys():
        rect = addhistbar(ax, aggregated[k][jsonkey])
        label = jsonkey + ", k=" + str(k)
        legends.append((rect, label))
ax.legend(zip(*legends)[0], zip(*legends)[1])
fig.savefig(options.output_file)
