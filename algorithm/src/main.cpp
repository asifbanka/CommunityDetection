#include <iostream>
#include <stdexcept>

#include <Eigen/Sparse>

#include "graph.hpp"
#include "matrixBuilder.hpp"
#include "matrixSolver.hpp"


using namespace std;

int main( int argc, const char* argv[] )
{
    if(argc < 3) {
        cout << "usage: " << argv[0] << " $graph $seed $affinities" << endl;
        cout << "where $graph and $seed are the input files and $affinities is the output file." << endl;
        return 1;
    }

    string filenameGraph = argv[1];
    string filenameSeed = argv[2];
    string filenameCommunities = argv[3];

    Graph g;
    g.readGraph(filenameGraph, filenameSeed);

    Eigen::SparseMatrix<double> D;
    Eigen::SparseMatrix<double> A;
    Eigen::SparseMatrix<double> R;
    buildMatrices(g, D, A, R); 

    cout << "perform community detection" << endl;
    solveMatrices(g, D, A, R);

    g.writeCommunities(filenameCommunities);

    return 0;
} 
