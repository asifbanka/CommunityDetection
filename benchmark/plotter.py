#!/usr/bin/env python2

import matplotlib
matplotlib.use("pdf")

import matplotlib.pyplot as plt
import numpy as np
import json
from optparse import OptionParser
import textwrap

##########################################
#
# COMMAND LINE INTERFACE

# interface
def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-f", dest="files", type="string",
        help="Whitespace-separated list of json-files. This program plots NMI (y-axis) against the mixing parameter or overlap (x-axis). \
        Each json-file represents one plot-line.")

    parser.add_option("-o", dest="output", type="string",
        help="pdf output file")

    parser.add_option("-i", dest="iterations", type="string",
        help="a list of iterations to display")

    parser.add_option("-m", dest="mode", type="string",
        help="either overlap or nonoverlap")

    global options, args
    (options, args) = parser.parse_args()

    if not (options.files and options.output):
        parser.print_help()
        return False
    return True


##########################################
#
# JSON HANDLING

def loadJson(filename):
    with open(filename) as infile:
        return json.load(infile)

##########################################
#
# PLOTTING 

def getXsYs(data, iteration, mode):
    xs = []
    ys = []

    nmiValuesMean = data["nmiValuesMean"]
    for tup in nmiValuesMean:
        if options.mode == "overlap":
            xs.append(float(tup["on"]))
        elif options.mode == "nonoverlap":
            xs.append(float(tup["mu"]))
        else:
            raise Exception()
        ys.append(float(tup["value"][iteration]))
    return xs, ys

##########################################
#
# LABELING

#generates the cuve's labels and the title for the plot
def getTitleAndLabel(dataList, iterations, mode):

    #number of nodes for each file
    N = [int(x["_N"]) for x in dataList]


    #each file has either big or small communities
    communitysizes = []
    for x in dataList:
        if int(x["_minc"]) == 10:
            communitysizes.append("small")
        elif int(x["_minc"]) == 20:
            communitysizes.append("big")
        else:
            raise Exception()

    #a string containing the seed percentage for each file
    seedStrings = [str(int(x["_seedFraction"] * 100))+ "% seeds" for x in dataList]

    #-------

    if(len(dataList) != 1 and len(iterations) != 1):
        raise Exception("right now we do not support plotting multiple files with multiple iterations")

    if(len(set(N)) != 1 or len(set(communitysizes)) != 1):
        raise Exception("tries to plot files with different number of nodes or communitysizes")


    #title must contain community sizes and number of nodes
    title = str(N[0]) + " nodes, " + communitysizes[0] + " communities"
    labels = ["" for x in dataList]


    #if we have just one seed percentage, put it in the title, otherwise in the label
    if(len(dataList) == 1):
        title += ", " + seedStrings[0]
    else:
        labels = seedStrings

    titleSecondLine = ""


    #if we have just one iteration, put it in the title, otherwise in the label
    if(len(iterations) == 1):
        if(iterations[0] == 0):
            titleSecondLine += "non-iterative"
        else:
            titleSecondLine += "iteration " + str(iterations[0]+1)
    else:
        labels = seedStrings
        labels = ["iteration " + str(x+1) for x in iterations]


    #add the mixing parameter to the title if in overlap mode
    if mode == "overlap":
        mus = [(x["_mu"]) for x in dataList]
        if len(set(mus)) != 1:
            raise Exception("there different mu values in these files")
        if titleSecondLine != "":
            titleSecondLine += ", "
        titleSecondLine += str(mus[0]) + " mixing parameter"

    if titleSecondLine != "":
        title += ",\n" + titleSecondLine


    #add some space below the title
    title += "\n"


    return title, labels

##########################################
#
# MAIN 

options, args = 0, 0
if commandline_interface():

    if(options.mode != "overlap" and options.mode != "nonoverlap"):
        raise Exception("mode must be either overlap or nonoverlap")

    filenames = options.files.split()
    iterations = [int(x) for x in options.iterations.split()]
    if(len(filenames) != 1 and len(iterations) != 1):
        raise Exception("right now we do not support plotting multiple files with multiple iterations")


    dataList = [loadJson(x) for x in filenames]
    dataList = sorted(dataList, key=lambda x: x["_seedFraction"])

    #pick title for plot
    title, labels = getTitleAndLabel(dataList, iterations, options.mode)
    #title = textwrap.fill(title, 55);

    lines = []
    i = 0
    for data in dataList:
        for iteration in iterations:
            xs, ys = getXsYs(data, iteration, options.mode)
            markers = ["o", "v", "^", "s", "d"]
            colors = ["b", "g", "r", "c", "m"]
            fillstyles = [ u'full', u'none' ] * 5
            #mews = [ 0, 3 ] * 5
            line, = plt.plot(xs, ys, "-o",
                    label=labels[i],
                    marker=markers[i],
                    fillstyle=fillstyles[i],
                    color=colors[i],
                    markeredgecolor=colors[i],
                    markersize=9,
                    mew=2) #thickness of marker borders
            i = i + 1
            lines.append(line)

    plt.title(title)
    plt.legend(fancybox=True, shadow=False, loc=3)
    if options.mode == "overlap":
        plt.axis([0,0.6,0,1])
        plt.xlabel("Fraction of overlapping vertices")
        plt.ylabel("Normalized Mutual Information")
    else:
        plt.axis([0,0.8,0,1])
        plt.xlabel("Mixing Parameter")
        plt.ylabel("Normalized Mutual Information")
    plt.grid(True)

    font = {'family' : 'normal',
            #'weight' : 'bold',
            'size'   : 16}
    matplotlib.rc('font', **font)

    #plt.tight_layout()
    plt.savefig(options.output, bbox_inches='tight')
