#!/usr/bin/env python2

import matplotlib
matplotlib.use("pdf")

import matplotlib.pyplot as plt
import numpy as np
import json
from optparse import OptionParser
from pprint import pprint

##########################################
#
# COMMAND LINE INTERFACE

# interface
def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-f", dest="files", type="string",
        help="Whitespace-separated list of json-files. This program plots NMI (y-axis) against the mixing parameter (x-axis). \
        Each json-file represents one plot-line.")

    parser.add_option("-o", dest="output", type="string",
        help="pdf output file")

    parser.add_option("-i", dest="iterations", type="string",
        help="a list of iterations to display")

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

# plot the json-file "filename"
# plot either the first (round="first") or the last (round="last") round of the iterative method
def plotFileOld(filename, round):
    xs = []
    ys = []
    label = ""
    data = loadJson(filename)

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


# 
def getXsYs(data, iteration):
    xs = []
    ys = []

    nmiValuesMean = data["nmiValuesMean"]
    for tup in nmiValuesMean:
        xs.append(float(tup["mu"]))
        ys.append(float(tup["value"][iteration]))
    return xs, ys

##########################################
#
# LABELING

#if there we display just one file, put the seed percentage in the title and not the label
def getTitleAndLabel(dataList, iterations):


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


    #if we have just one seed percentage, put it in the title, otherwise in the label
    if(len(dataList) == 1):
        title += ", " + seedStrings[0]
    else:
        labels = seedStrings


    #if we have just one iteration, put it in the title, otherwise in the label
    if(len(iterations) == 1):
        if(iterations[0] == 0):
            title += ", " + "non-iterative"
        else:
            title += ", " + "iteration " + str(iterations[0])
    else:
        labels = seedStrings
        labels = ["iteration " + str(x) for x in iterations]


    return title, labels

##########################################
#
# MAIN 

options, args = 0, 0
if commandline_interface():

    filenames = options.files.split()
    iterations = [int(x) for x in options.iterations.split()]


    #pick title for plot
    dataList = [loadJson(x) for x in filenames]
    title, labels = getTitleAndLabel(dataList, iterations)

    graphs = []
    lines = []

    if(len(dataList) != 1 and len(iterations) != 1):
        raise Exception("right now we do not support plotting multiple files with multiple iterations")

    labelIdx = 0
    for data in dataList:
        for iteration in iterations:
            xs, ys = getXsYs(data, iteration)
            line, = plt.plot(xs, ys, "-o", label=labels[labelIdx])
            labelIdx = labelIdx + 1
            lines.append(line)

    plt.title(title)
    plt.legend(fancybox=True, shadow= True, loc=1)
    plt.axis([0,1,0,1])
    plt.xlabel("Mixing Parameter")
    plt.ylabel("Normalized Mutual Information")
    plt.savefig(options.output)
