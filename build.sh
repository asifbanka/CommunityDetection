#!/bin/sh

# build the c++ implementation
(cd algorithm && ./build.sh)

# build external programs
(cd external && ./build.sh)
