project(foo)

set(CMAKE_CXX_FLAGS "-Wall -std=c++0x ")

#include header-only Eigen library
include_directories(3rdparty)

#update this list whenever you add/remove/rename a file
set(SOURCES 
    src/graph.cpp
    src/graph.hpp
    src/main.cpp
    src/matrixBuilder.cpp
    src/matrixSolver.cpp
    src/seedNode.cpp
    src/seedNode.hpp
    src/communityClassifier.cpp
    src/communityClassifier.hpp
    src/communityProcessor.cpp
)

add_executable(foo ${SOURCES})
