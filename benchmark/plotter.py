#!/usr/bin/env python2

import matplotlib.pyplot as plt
import numpy as np
import json
from optparse import OptionParser
from pprint import pprint

def plotFile(filename):
    xs = []
    ys = []
    label = ""
    with open(filename) as infile:
        data = json.load(infile)
        label += "N = " + str(data["_N"])
        label += ", seed = " + str(data["_seedPercentage"])
        label += ", maxc = " + str(data["_maxc"])

        nmiValuesMean = data["nmiValuesMean"]
        for tup in nmiValuesMean:
            xs.append(float(tup["mu"]))
            ys.append(float(tup["value"]))
    return xs, ys, label

# interface
def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-f", dest="files", type="string",
        help="Whitespace-separated list json-files. This program plots NMI (y-axis) agains the mixing parameter (x-axis). Each json-file represents one plot-line.")

    global options, args
    (options, args) = parser.parse_args()

    if not options.files:
        parser.print_help()
        return False
    return True


options, args = 0, 0
if commandline_interface():

    filenames = options.files.split()
    graphs = []
    lines = []
    for f in filenames:
        xs, ys, label = plotFile(f)
        line, = plt.plot(xs, ys, "-o", label=label)
        lines.append(line)

    plt.legend(handles=lines)
    plt.legend(loc="best", fancybox=True, framealpha=0.5)
    plt.axis([0,1,0,1])
    plt.xlabel("mixing parameter")
    plt.ylabel("nmi")
    plt.show()

