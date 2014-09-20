#!/usr/bin/env python2

import datetime
import sys
import os
import numpy as np
import subprocess as sp
import json
from optparse import OptionParser
from collections import defaultdict

from pprint import pprint


#path to the repositories root
ROOT = os.path.dirname(os.path.realpath(__file__)) + "/.."

#for logging purposes
LOGERROR = open("LOGERROR", 'w')
DEVNULL = open(os.devnull, 'w')

OUTPUTFOLDER = "./nmi_values_" + str(datetime.datetime.now()) + "/"

################################

class Benchmark:
    def __init__(self, numberOfNodes, communitySize, _seedPercentage, _iterations, _mixingRange):

        # LFR parameters
        self.k = 20
        self.maxk = 50
        self.t1 = 2
        self.t2 = 1
        self.N = numberOfNodes
        self.on = 0
        self.om = 0
        if communitySize == "small":
            self.minc = 10
            self.maxc = 50
        elif communitySize == "big":
            self.minc = 20 
            self.maxc = 100 
        else:
            raise Exception("wrong parameter for communitySize. it must either be small or big")

        #how many graphs with the same parameters
        if _iterations is None:
            self.iterations = 100
        else:
            self.iterations = _iterations

        #the values for the mixing parameter
        if _mixingRange is None:
            self.mixingRange = [x*0.01 for x in range(4, 96, 2)]
        else:
            self.mixingRange = [x*0.01 for x in _mixingRange]

        #the percentage of seed nodes
        self.seedPercentage = _seedPercentage

        #a list of nmi-values for each mixing parameter
        self.nmiValues = defaultdict(list)
        #the mean nmi-value for each mixing parameter
        self.nmiValuesMean = defaultdict()

        #the filename under which this object gets stored
        self.filename = ( str(self.N) + "N"
                      + "_" + communitySize + "Communities"
                      + "_" + str(self.on) + "on"
                      + "_" + str(self.om) + "om"
                      + "_" + ('{num:03d}'.format(num=self.seedPercentage)) + "pSeed"
                      + ".json" 
                      )
                        #('{num:02d}'.format(num=self.seedPercentage))
                        #"%02d" % (self.seedPercentage,)


    # fill in all data by running LFRtoNMI.sh a couple times
    def run(self):
        print ""
        print "====================================="
        print ""

        print "parameters for next benchmark:"
        print "seedPercentage =", self.seedPercentage 
        print "N =",    self.N
        print "minc =", self.minc
        print "maxc =", self.maxc
        print "k =",    self.k
        print "maxk =", self.maxk
        print "t1 =",   self.t1
        print "t2 =",   self.t2
        print "on =",   self.on
        print "om =",   self.om
        print "iterations =", self.iterations
        print "mixingRange =", self.mixingRange

        for mu in self.mixingRange:
            print ""
            print "mu = " + str(mu)
            print "---------"

            successful = 0
            errorsInARow = 0

            while successful < self.iterations:
                #delete last line of output
                
                #call graph generator and calculate nmi
                scriptName = ROOT + "/scripts/LFRtoNMI.sh"
                if not os.path.isfile(scriptName):
                        raise Exception("path to LFRtoNMI.sh is wrong")
                call = [ scriptName
                       , str(self.seedPercentage)
                       , "-k", str(self.k)
                       , "-maxk" ,str(self.maxk)
                       , "-t1", str(self.t1)
                       , "-t2", str(self.t2)
                       , "-minc",str(self.minc)
                       , "-maxc", str(self.maxc)
                       , "-mu", str(mu)
                       , "-N", str(self.N)
                       , "-on", str(self.on)
                       , "-om", str(self.om)
                       ]
                returnValue = sp.call(call, stdin=None , stderr=LOGERROR, stdout=DEVNULL, shell=False)

                if returnValue == 0:
                    #script was successful
                    successful = successful + 1
                    errorsInARow = 0
                    with open ("tmp_nmivalue", "r") as f:
                        nmi = float(f.read())
                        self.nmiValues[mu].append(nmi)
                        print "(" + str(successful) + "/" + str(self.iterations) + "): " + str(nmi)
                else:
                    errorsInARow = errorsInARow + 1
                    if errorsInARow > 100:
                        raise Exception("LFRtoNMI crashes a lot for these parameters")


            self.nmiValuesMean[mu] = np.mean(self.nmiValues[mu])



    # dump the object as json file
    def dump(self):
        obj = defaultdict()
        obj["_k"]    = self.k
        obj["_maxk"] = self.maxk
        obj["_t1"]   = self.t1
        obj["_t2"]   = self.t2
        obj["_N"]    = self.N
        obj["_on"]   = self.on
        obj["_om"]   = self.om
        obj["_minc"] = self.minc
        obj["_maxc"] = self.maxc
        obj["_iterations"] = self.iterations
        obj["_seedPercentage"] = self.seedPercentage
        obj["_mixingRange"] = self.mixingRange
        obj["nmiValues"] = self.nmiValues
        obj["nmiValuesMean"] = self.nmiValuesMean

        with open(OUTPUTFOLDER + self.filename, 'w') as outfile:
            json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))


def runBenchmark(*args):
    b = Benchmark(*args)
    b.run()
    b.dump()

################################



# interface
def commandline_interface():
    usage = "usage: %prog"
    parser = OptionParser()
    
    # command line options
    parser.add_option("-n", dest="numberOfNodes", type="string",
        help="whitespace separated list of graph sizes")

    parser.add_option("-c", dest="communitySizes", type="string",
        help="whitespace separated list of community sizes")

    parser.add_option("-s", dest="seedPercentages", type="string",
        help="whitespace separated list of seed percentages")

    parser.add_option("-i", dest="iterations", type="int",
        help="optional parameter. iterations per data point. default is 100")

    parser.add_option("-m", dest="mixingRange", type="str",
        help="optional parameter. start stop step separated by whitespaces in percentage. derault is range(4,96,2)")
    
    global options, args
    (options, args) = parser.parse_args()

    if not (options.numberOfNodes and 
            options.communitySizes): 
        parser.print_help()
        return False
    return True


options, args = 0, 0
if commandline_interface():

    numberOfNodes   = [int(N) for N in options.numberOfNodes.split()]
    communitySizes  = options.communitySizes.split()

    mixingRange = None
    if not options.mixingRange is None:
        tmp             = options.mixingRange.split()
        mixingRange     = range(int(tmp[0]), int(tmp[1]), int(tmp[2]))

    for c in communitySizes:
        if c != "big" and c != "small":
            raise Exception("wrong parameter for communitySize. it must either be small or big")

    seedPercentages = [5,10,15,20]
    if not options.seedPercentages is None:
        seedPercentages = [int(s) for s in options.seedPercentages.split()]

    print "will run the following benchmarks:"

    print "OUTPUTFOLDER = " + OUTPUTFOLDER
    if not os.path.exists(OUTPUTFOLDER):
        os.makedirs(OUTPUTFOLDER)

    for N in numberOfNodes:
        for size in communitySizes:
            for seed in seedPercentages:
                print "> runBenchmark(", N, size, seed, options.iterations, mixingRange, ")"

    for N in numberOfNodes:
        for size in communitySizes:
            for seed in seedPercentages:
                runBenchmark(N, size, seed, options.iterations, mixingRange)
