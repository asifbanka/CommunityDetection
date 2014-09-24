#!/usr/bin/env python2

import matplotlib
matplotlib.use("pdf")

import matplotlib.pyplot as plt
import numpy as np
import json
from optparse import OptionParser
from pprint import pprint

# plot the json-file "filename"
# plot either the first (round="first") or the last (round="last") round of the iterative method
def plotFile(filename, round):
    xs = []
    ys = []
    label = ""
    with open(filename) as infile:
        data = json.load(infile)

        i = 0
        if round == "first":
            i = 0
        elif round == "last":
            i = int(data["_rounds"])-1
        else:
            raise Exception("pass either first or last as parameter")

        label += "N=" + str(data["_N"])
        label += ", seed=" + str(data["_seedFraction"])
        label += ", maxc=" + str(data["_maxc"])
        label += ", round=" + str(i)

        nmiValuesMean = data["nmiValuesMean"]
        for tup in nmiValuesMean:

            xs.append(float(tup["mu"]))
            ys.append(float(tup["value"][i]))
    return xs, ys, label

# interface
def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-f", dest="files", type="string",
        help="Whitespace-separated list json-files. This program plots NMI (y-axis) agains the mixing parameter (x-axis). Each json-file represents one plot-line.")

    parser.add_option("-o", dest="output", type="string",
        help="pdf output file")

    parser.add_option("-i", dest="iterative", action="store_true",
        help="flag without parameter. if set plot first and last value of iterative method")

    global options, args
    (options, args) = parser.parse_args()

    if not (options.files and options.output):
        parser.print_help()
        return False
    return True


options, args = 0, 0
if commandline_interface():

    filenames = options.files.split()
    graphs = []
    lines = []
    for f in filenames:
        xs, ys, label = plotFile(f, "first")
        line, = plt.plot(xs, ys, "-o", label=label)
        lines.append(line)

        if options.iterative:
            xs, ys, label = plotFile(f, "last")
            line, = plt.plot(xs, ys, "-o", label=label)
            lines.append(line)

    plt.legend(handles=lines)
    plt.legend(loc="best", fancybox=True, framealpha=0.5)
    plt.axis([0,1,0,1])
    plt.xlabel("mixing parameter")
    plt.ylabel("nmi")

    plt.savefig(options.output)
    #plt.show()

