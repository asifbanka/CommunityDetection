#!/usr/bin/python

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

        i=0
        if round == -1:
            label = str(int(data["_seedFraction"]*100))+"% Seeds"
        else:
            i=round
            if round > int(data["_iterations"])-1:
                i=int(data["_iterations"])-1

            label = "Iteration "+str(i)    

        #label += "N=" + str(data["_N"])
        #label = str(int(data["_seedFraction"]*100))+"% seeds"
        #label += ," maxc=" + str(data["_maxc"])
        #label += ", round=" + str(i)

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
        help="Whitespace-separated list of json-files. This program plots NMI (y-axis) against the mixing parameter (x-axis). \
        Each json-file represents one plot-line.")

    parser.add_option("-o", dest="output", type="string",
        help="pdf output file")

    parser.add_option("-i", dest="iterations", type="int",
        help="flag for setting the number iteration for the second line in iterative method. -1 if non iterativ plot")

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
        if(options.iterations == -1):
            xs, ys, label = plotFile(f, -1)
            line, = plt.plot(xs, ys, "-o", label=label)
            lines.append(line)

        else:
            xs, ys, label = plotFile(f, 0)
            line, = plt.plot(xs, ys, "-o", label=label)
            lines.append(line)

            xs, ys, label = plotFile(f, options.iterations)
            line, = plt.plot(xs, ys, "-o", label=label)
            lines.append(line)

    plt.legend(fancybox=True, shadow= True, loc=1)
    plt.axis([0,1,0,1])
    plt.xlabel("Mixing Parameter")
    plt.ylabel("Normalized Mutual Information")
    plt.title("")
    plt.savefig(options.output)
    #plt.show()
