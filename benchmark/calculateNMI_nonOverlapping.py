#!/usr/bin/env python2

import os
import numpy as np
import subprocess as sp

#this script will create the graphs for the non overlapping test

smallN = 1000
bigN = 5000
k = 20
maxk = 50
t1 = 2
t2 = 1
repetitions = 100 #how many graphs with the same parameters

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
OUTPUTFOLDER = "./values/nonOverlapping/"

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
                raise Exception("set correct community size")

def createGraphs(n):
        for mu in np.arange(0.05, 0.96, 0.01):
                print "mu = " + str(mu)
                print ""
                for seed in xrange(5,31,5):
                        print "seed nodes: " + str(seed) + " %"
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
                                print "\033[A                             \033[A"
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
                        
print "Beginning test:"
print "N = " + str(smallN)

print "community size = small"
setCommunitySize("small")
createGraphs(smallN)

print "community size = big"
setCommunitySize("big")
createGraphs(smallN)


print "N = " + str(bigN)
print "community size = small"
setCommunitySize("small")
createGraphs(bigN)

print "community size = big"
setCommunitySize("big")
createGraphs(bigN)

print "testing finished"
