#!/bin/sh

rm -rf build
mkdir -p build
cd build
cmake ..
make
./community_detection_test
