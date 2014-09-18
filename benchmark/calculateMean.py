#!/usr/bin/env python2

import os
import numpy as np
import subprocess as sp

OUTPUTFOLDER = "./values/nonOverlapping/"

meanFile = open("mean", 'w')

for root, dirs, files in os.walk(OUTPUTFOLDER):
    for name in files:
        path = os.path.join(root, name)
        print path
        with open(path, "r") as handle:
            values = [float(x) for x in handle]
            print values
            line = ( path 
                   + "\t" 
                   + str(len(values)) + "_entries" 
                   + "\t"
                   + str(np.mean(values)) 
                   + "\n"
                   )
            meanFile.write(line)
