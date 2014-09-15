#include "matrixBuilder.hpp"

#include <iostream>
#include <Eigen/Sparse>
#include "graph.hpp"

using namespace std;

// declares a column-major sparse matrix type of double
typedef Eigen::SparseMatrix<double> SMatD;
// A triplet is a simple object representing a non-zero entry as 
// the triplet: row index, column index, value.
typedef Eigen::Triplet<double> TripletD; 

//param: graph and seed node class
//return: matrices D, A and R
void buildMatrices(const Graph& g, SMatD& D, SMatD& A, SMatD& R){

    int numberOfVertices = g.numVertices();
    int numberOfseedVertices = g.numSeed();
    int numberOfNonSeedVertices = numberOfVertices - numberOfseedVertices;

    // generate the matrices
    A.resize(numberOfNonSeedVertices, numberOfNonSeedVertices);
    D.resize(numberOfNonSeedVertices, numberOfNonSeedVertices);
    R.resize(numberOfNonSeedVertices, numberOfseedVertices);

    std::vector<TripletD> tripletListA,tripletListD,tripletListR;
    
    //filling A, D and R
    for (int i = 0; i < numberOfVertices; ++i) { // going over all vertices
        if(!g.isSeed(i)){ //if the current vertex is not a seed node
            tripletListD.push_back(TripletD(g.getMatrixIndex(i), g.getMatrixIndex(i),g.getDegree(i))); 
            //going over all neighbors of i and adding entries to A and R depending on the neighbor beeing a seed node
            for(auto neighbor = g.getNeighbors(i).begin(); neighbor != g.getNeighbors(i).end(); neighbor++) {
                if(g.isSeed(*neighbor)){           
                    tripletListR.push_back(TripletD(g.getMatrixIndex(i),g.getMatrixIndex(*neighbor), 1)); 
                } else {
                    tripletListA.push_back(TripletD(g.getMatrixIndex(i),g.getMatrixIndex(*neighbor), 1)); 
                }
            }
        }
    }

    //building A, D and R
    A.setFromTriplets(tripletListA.begin(), tripletListA.end());
    D.setFromTriplets(tripletListD.begin(), tripletListD.end());
    R.setFromTriplets(tripletListR.begin(), tripletListR.end());
}


