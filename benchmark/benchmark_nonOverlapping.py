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

OUTPUTFOLDER = "./nmi_values_" + str(datetime.datetime.now()).replace(" ", "_") + "/"

################################

class Benchmark:
    def __init__( self
                , numberOfNodes
                , communitySize
                , _seedFraction
                , _iterations
                , _mixingRange
                , _rounds):


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
        self.iterations = _iterations

        #the values for the mixing parameter
        self.mixingRange = _mixingRange

        #the fraction of seed nodes
        self.seedFraction = _seedFraction

        #the number of rounds for the iterative method
        self.rounds = _rounds

        #a list of nmi-values for each mixing parameter and round for the iterative method
        #self.nmiValues[mu][round][i] will give the nmi for mixingParam mu after the "round"th iterative round and the ith iteration
        self.nmiValues = []

        #the mean nmi-value for each mixing parameter
        #self.nmiValues[mu][round] will give the mean-nmi for mixingParam mu after the "round"th iterative round
        self.nmiValuesMean = []

        #the filename under which this object gets stored
        self.filename = ( str(self.N) + "N"
                      + "_" + communitySize + "Communities"
                      + "_" + str(self.on) + "on"
                      + "_" + str(self.om) + "om"
                      + "_" + str(self.seedFraction) + "seed"
                      + ".json" 
                      )


    # fill in all data by running LFRtoNMI.sh a couple times
    def run(self):
        print ""
        print "====================================="
        print ""
        print "parameters for next benchmark:"
        print "seedFraction =", self.seedFraction 
        print "N =",            self.N
        print "minc =",         self.minc
        print "maxc =",         self.maxc
        print "k =",            self.k
        print "maxk =",         self.maxk
        print "t1 =",           self.t1
        print "t2 =",           self.t2
        print "on =",           self.on
        print "om =",           self.om
        print "rounds =",       self.rounds
        print "iterations =",   self.iterations
        print "mixingRange =",  self.mixingRange

        for mu in self.mixingRange:
            print ""
            print "mu = " + str(mu)
            print "---------"

            successful = 0
            successiveErrors = 0

            
            #nmis[round][i] contains the nmi for a fixed mixingParam mu after the "round"th iterative round and the ith iteration
            nmiValuesFixedMu = [ [] for x in range(self.rounds) ]

            while successful < self.iterations:
                #call graph generator and calculate nmi

                # this scripts generates a graph, runs the algorithm and calculates the nmi
                scriptName = ROOT + "/scripts/LFRtoNMI.sh"
                # the file the script stores the nmi values in
                nmiFileName = "tmp_nmivalues"

                if not os.path.isfile(scriptName):
                        raise Exception("path to LFRtoNMI.sh is wrong")
                call = [ scriptName
                       , nmiFileName
                       , str(self.seedFraction)
                       , str(self.rounds)
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
                    successiveErrors = 0

                    nmisOfIteration = []
                    with open (nmiFileName, "r") as f:
                        for line in f:
                            nmisOfIteration.append(float(line))

                    if len(nmisOfIteration) != self.rounds:
                        raise Exception("wrong number of lines in nmi-file")

                    for r in range(self.rounds):
                        nmiValuesFixedMu[r].append(nmisOfIteration[r])

                    print "(" + str(successful) + "/" + str(self.iterations) + "): " + str(nmisOfIteration)
                else:
                    successiveErrors = successiveErrors + 1
                    if successiveErrors > 100:
                        raise Exception("LFRtoNMI crashes a lot for these parameters")

            tmp = defaultdict()
            tmp["mu"] = mu
            tmp["value"] = nmiValuesFixedMu
            self.nmiValues.append(tmp)

            tmpMean = defaultdict()
            tmpMean["mu"] = mu
            tmpMean["value"] = [[] for x in range(self.rounds) ]
            for r in range(self.rounds):
                tmpMean["value"][r] = np.mean(nmiValuesFixedMu[r])
            self.nmiValuesMean.append(tmpMean)




    # dump the object as json file
    def dump(self):
        obj = defaultdict()
        obj["_k"]            = self.k
        obj["_maxk"]         = self.maxk
        obj["_t1"]           = self.t1
        obj["_t2"]           = self.t2
        obj["_N"]            = self.N
        obj["_on"]           = self.on
        obj["_om"]           = self.om
        obj["_minc"]         = self.minc
        obj["_maxc"]         = self.maxc
        obj["_rounds"]       = self.rounds
        obj["_iterations"]   = self.iterations
        obj["_seedFraction"] = self.seedFraction
        obj["nmiValues"]     = self.nmiValues
        obj["nmiValuesMean"] = self.nmiValuesMean

        #print (options.outputfolder + "/" + self.filename, 'w')
        with open(options.outputfolder + "/" + self.filename, 'w') as outfile:
            json.dump(obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))

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

    parser.add_option("-s", dest="seedFractions", type="string",
        help="whitespace separated list of seed percentages")

    parser.add_option("-o", dest="outputfolder", type="str",
        help="the folder the json files will be written to")

    parser.add_option("-i", dest="iterations", type="int",
        help="iterations per data point")

    parser.add_option("-m", dest="mixingRange", type="str",
        help="start stop step, separated by whitespaces")

    parser.add_option("-r", dest="rounds", type="int",
        help="number of rounds for the iterative method")

    
    global options, args
    (options, args) = parser.parse_args()

    if not (options.numberOfNodes and 
            options.communitySizes and
            options.seedFractions and
            options.outputfolder and
            options.iterations and
            options.mixingRange and
            options.rounds): 
        parser.print_help()
        return False
    return True


options, args = 0, 0
if commandline_interface():

    numberOfNodes   = [int(N) for N in options.numberOfNodes.split()]
    communitySizes  = options.communitySizes.split()
    seedFractions   = [float(s) for s in options.seedFractions.split()]
    iterations      = options.iterations

    tmp = [float(x) for x in options.mixingRange.split()]
    print tmp
    mixingRange     = [x for x in np.arange(tmp[0], tmp[1], tmp[2])]
    print mixingRange


    for c in communitySizes:
        if c != "big" and c != "small":
            raise Exception("wrong parameter for communitySize. it must either be small or big")


    print "will run the following benchmarks:"

    print "outputfolder =", options.outputfolder
    if not os.path.exists(options.outputfolder):
        os.makedirs(options.outputfolder)

    benchmarks = []
    for N in numberOfNodes:
        for size in communitySizes:
            for seed in seedFractions:
                print "> create Benchmark(", N, size, seed, iterations, mixingRange, options.rounds, ")"
                benchmarks.append(Benchmark(N, size, seed, iterations, mixingRange, options.rounds))

    for benchmark in benchmarks:
        benchmark.run()
        benchmark.dump()
