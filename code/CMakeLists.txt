cmake_minimum_required(VERSION 1.6)

project(community_detection)

set(CMAKE_CXX_FLAGS "-Wall -std=c++0x ")

# default set build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release")
endif(NOT CMAKE_BUILD_TYPE)

#include header-only Eigen and Catch libraries
include_directories(
    3rdparty/eigen
    3rdparty/catch
    src
)

#update this list whenever you add/remove/rename a file
set(SOURCES_community_detection
    src/graph.cpp
    src/graph.hpp
    src/matrixBuilder.cpp
    src/matrixBuilder.hpp
    src/matrixSolver.cpp
    src/matrixSolver.hpp
    src/communityClassifier.cpp
    src/communityClassifier.hpp
    src/communityProcessor.cpp
    src/main.cpp
)

#update this list whenever you add/remove/rename a file
#this list must not contain the main function from the community_detection executable
set(SOURCES_community_detection_test
    src/graph.cpp
    src/graph.hpp
    src/matrixBuilder.cpp
    src/matrixBuilder.hpp
    src/matrixSolver.cpp
    src/matrixSolver.hpp
    src/communityClassifier.cpp
    src/communityClassifier.hpp
    test/main.cpp
)

message (${CMAKE_BINARY_DIR}/test/data/)

#file( COPY
      #${CMAKE_CURRENT_SOURCE_DIR}/test/data/
      #DESTINATION ${CMAKE_BINARY_DIR}/test/data/
      ##FILES_MATCHING PATTERN "*"
#)

add_executable(community_detection ${SOURCES_community_detection})
add_executable(community_detection_test ${SOURCES_community_detection_test})
