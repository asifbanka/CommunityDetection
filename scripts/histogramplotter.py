#!/usr/bin/env python2

import sys
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np

##########################################
#
# COMMAND LINE INTERFACE

def commandline_interface():
    parser = OptionParser()
   
    parser.add_option("-o", dest="output_file", type="string",
            help="deduces fileformat automatically. *.pdf or *.png works")
   
    global options, args
    (options, args) = parser.parse_args()

    if not options.output_file:
        parser.print_help()
        return False

    return True

##########################################
#
# PLOTTING

options, args = 0, 0
if not commandline_interface():
    sys.exit(1)

colors = ['b', 'y', 'r', 'g']
colorindex = -1
def getCycledColor():
    global colorindex
    if colorindex < len(colors) - 1:
        colorindex = colorindex + 1
        return colors[colorindex]
    else:
        colorindex = -1

def addhistbar(ax, values):
    hist, bins = np.histogram(values, bins=50)
    freq = [float(x)/len(values) for x in hist]
    center = (bins[:-1] + bins[1:]) / 2
    width = 1.0 * (bins[1] - bins[0])
    ax.bar(center, freq, align='center', width=width, linewidth=0, alpha=0.5, facecolor=getCycledColor())


fig, ax = plt.subplots()

addhistbar(ax, np.random.randn(10000) + 2)
addhistbar(ax, np.random.randn(10000) + 4)
addhistbar(ax, np.random.randn(10000))

fig.savefig(options.output_file)
