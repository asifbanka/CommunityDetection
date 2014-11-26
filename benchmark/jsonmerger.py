#!/usr/bin/env python2


import matplotlib.pyplot as plt
import numpy as np
import json
from optparse import OptionParser

##########################################
#
# COMMAND LINE INTERFACE

# interface
def commandline_interface():
    parser = OptionParser()
    
    # command line options
    parser.add_option("-i", dest="files", type="string",
        help="whitespace separated json files which shall be merged")

    parser.add_option("-o", dest="output", type="string",
        help="json outputfile")

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


def mergeJson(dataList):
    newData = dataList[0]
    newData["nmiValues"] = []
    newData["nmiValuesMean"] = []

    for data in dataList:
        newData["nmiValues"]     += data["nmiValues"]
        newData["nmiValuesMean"] += data["nmiValuesMean"]

    newData["nmiValues"]     = sorted(newData["nmiValues"], key=lambda x: x["mu"]) 
    newData["nmiValuesMean"] = sorted(newData["nmiValuesMean"], key=lambda x: x["mu"]) 

    return newData

##########################################
#
# MAIN 

options, args = 0, 0
if commandline_interface():

    dataList = [loadJson(x) for x in options.files.split()]
    newData = mergeJson(dataList)

    with open(options.output, 'w') as outfile:
        json.dump(newData, outfile, sort_keys=True, indent=4, separators=(',', ': '))

