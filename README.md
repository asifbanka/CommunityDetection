This is code for testing a new community detection algorithm.

This repository contains everything which is relevant to our 
community-detection method. Each module shall be in its own 
subfolder together with a README which describes the module 
and a build.sh file which builds executables (if needed). 
All executables shall be .gitignored. The executables of all 
modules shall be build by calling the build.sh script in this 
directory.


The subfolders include:

paper       the paper we later want to publish

algorithm   a C++ implementation of the community-detection algorithm

data        test-data or scripts which generate test-data

scripts     scripts to modify and parse the input and output of 
						various programs, so that they seamlessly work together

external    contains all programs we did not write ourselves, like 
						the LFR-benchmark

code        a folder which still needs to be cleaned up
