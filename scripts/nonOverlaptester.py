#!/usr/bin/env python2

import subprocess,os
#this script will create the graphs for the non overlapping test

smallN = 1000
bigN = 5000
k = 20
maxk = 50
t1 = 2
t2 = 1
repetitions = 100 #how many graphs with the same parameters
outputFolder = "./values/nonOverlapping/"

minc = 0
maxc = 0
_size = ""

on = 0
om = 0

pathLFRtoNMI = "./LFRtoNMI_alg.sh"



def remove(file):
	try:
		os.remove(file)
	except OSError:
	    	pass


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
                minc = 0
                maxc = 0
                print "Error: set correct community size"

def createGraphs(n):
        for j in range(5,96):
                mu = j * 0.01
                print "mu = " + str(mu)
                print ""
                for seed in xrange(5,31,5):
                        print "seed nodes: " + str(seed) + " %"
                        print ""
                        if not os.path.exists(outputFolder):
                                os.makedirs(outputFolder)

                        filename = str(n)+"N_"+_size+"C_"+str(mu)+"mu_"+str(on)+"on_"+str(om)+"om"+str(seed)+"p_seed"+".dat"
                        file = open(outputFolder+filename, 'w')
			i = 0
			while i < repetitions:
                                print "\033[A                             \033[A" #delete last line of output
                                print "graph " + str(i+1) + "/" + str(repetitions)
                                
                             
                                
                                remove("output.dat") #remove file from previous executions
                                #call graph generator and calculate nmi
                                subprocess.call([pathLFRtoNMI,str(seed),"-k",str(k), "-maxk",str(maxk),"-t1",str(t1),"-t2",str(t2),
                                        "-minc",str(minc),"-maxc",str(maxc),"-mu",str(mu),"-N",str(n),
                                        "-on", str(on), "-om", str(om)])
                                
				if os.path.isfile("output.dat"):        #the file does not exists if above script yields error
					outputFile = open("output.dat","r")
					outputText = outputFile.readline()
					nmiValue = 0
					for t in outputText.split():
	    					try:
	       						nmiValue = float(t)
	    					except ValueError:
							pass
		                        
					outputFile.close()
					
		                        #print str(nmiValue)
		                        file.write(str(nmiValue)+"\n")
					i = i + 1 #only increase if file was created
					
                        file.close()        
                        



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
