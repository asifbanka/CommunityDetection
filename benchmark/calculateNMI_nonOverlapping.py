#!/usr/bin/env python2

import sys
import os
import numpy as np
import subprocess as sp
from optparse import OptionParser

#this script will create the graphs for the non overlapping test

smallN = 1000
bigN = 5000
k = 20
maxk = 50
t1 = 2
t2 = 1
#how many graphs with the same parameters#how many graphs with the same parameters
repetitions = 100 

minc = 0
maxc = 0
_size = ""

on = 0
om = 0

#path to the repositories root
ROOT = os.path.dirname(os.path.realpath(__file__)) + "/.."

#for logging purposes
LOGFILE = open("logfile", 'w')
DEVNULL = open(os.devnull, 'w')
OUTPUTFOLDER = "./nmi_values/non_overlapping/"

def setCommunitySize(size):
        global minc
        global maxc
        global _size 
        _size = size
        if size == "small":
                minc = 10
                maxc = 50
        elif size == "big":
                minc = 20
                maxc = 100
        else:
                raise Exception("wrong parameter in setCommunitySize. it must either be small or big")

def runBenchmark(n, size):

        print "N = " + str(n)
        print "community size = " + size
        setCommunitySize(size)

        for seed in xrange(5,21,5):
                print "seed nodes: " + str(seed) + "%"
                print ""
                for mu in np.arange(0.04, 0.96, 0.02):
                        print "mu = " + str(mu)
                        print ""
                        if not os.path.exists(OUTPUTFOLDER):
                                os.makedirs(OUTPUTFOLDER)

                        filename = ( str(n) + "N"
                                   + "_" + _size + "C"
                                   + "_" + str(on) + "on"
                                   + "_" + str(om) + "om"
                                   + "_" + str(seed) + "pSeed"
                                   + "_" + str(mu) + "mu"
                                   + ".dat" 
                                   )
                        nmiValues = open(OUTPUTFOLDER+filename, 'w')

			i = 0
			while i < repetitions:
                                #delete last line of output
                                print "graph " + str(i+1) + "/" + str(repetitions)
                                
                                #call graph generator and calculate nmi
                                lfrtonmi = ROOT + "/scripts/LFRtoNMI.sh"
                                if not os.path.isfile(lfrtonmi):
                                        raise Exception("path to LFRtoNMI.sh is wrong")
                                call = [ lfrtonmi
                                       , str(seed)
                                       , "-k", str(k)
                                       , "-maxk" ,str(maxk)
                                       , "-t1", str(t1)
                                       , "-t2", str(t2)
                                       , "-minc",str(minc)
                                       , "-maxc", str(maxc)
                                       , "-mu", str(mu)
                                       , "-N", str(n)
                                       , "-on", str(on)
                                       , "-om", str(om)
                                       ]
                                returnValue = sp.call(call, stdin=None , stderr=LOGFILE, stdout=DEVNULL, shell=False)

                                if returnValue == 0:
                                        #if no error occured
                                        tmp = open("tmp_nmivalue", "r")
		                        nmiValues.write(str(float(tmp.read()))+"\n")
                                        tmp.close()
					i = i + 1 #only increase if file was created
					
                        nmiValues.close()        


# interface
def commandline_interface():
    usage = "usage: %prog"
    parser = OptionParser()
    
    # command line options
    parser.add_option("-n", dest="numberOfNodes", type="int",
        help="number of nodes for the graph")

    parser.add_option("-s", dest="communitySize", type="string",
        help="community size, either small or big")
    
    global options, args
    (options, args) = parser.parse_args()

    if not options.numberOfNodes:
        parser.error("number of nodes not given")
        parser.print_help()
        return False
    elif not options.communitySize:
        parser.error("community size not given")
        parser.print_help()
        return False
    return True

options, args = 0, 0
if commandline_interface():
    runBenchmark(options.numberOfNodes, options.communitySize)
