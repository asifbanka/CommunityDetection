#include <iostream>
#include <Eigen/Sparse>
#include <Eigen/Dense>
#include <vector>
#include "graph.hpp"
#include "seedNode.hpp"

typedef Eigen::SparseMatrix<double> SmatD;  // declares a column-major sparse matrix type of double
using Eigen::MatrixXd;

MatrixXd solve(Graph& g, SeedNode& seed, SmatD& A, SmatD& D, SmatD& R){
    SmatD D_A = D - A;
    const int numberOfCommunities = seed.num_communities();
    const int numberOfSeedNodes = seed.num_seed();
    const int numberOfNodes = g.num_vertices();
    const int numberOfNonSeedNodes = numberOfNodes - numberOfSeedNodes;
    MatrixXd affinities(numberOfNodes, numberOfCommunities);
    Eigen::SimplicialCholesky<SmatD> chol(D_A);  // performs a Cholesky factorization of (D-A)
    


    //for every community
    for(int l = 0; l < numberOfCommunities; ++l){
        Eigen::VectorXd sum(numberOfNonSeedNodes);
        Eigen::VectorXd b(numberOfNonSeedNodes);

        for(int j=0; j<numberOfSeedNodes; ++j){
            sum+= seed.get_affinity(seed.get_vertex_id(j),l)*R.col(l);
        }

        b = D * sum;

        Eigen::VectorXd x = chol.solve(b); // use the factorization to solve for the given right hand side


        //write the affinities for community l

        for(int i=0; i<numberOfNodes;++i){
            if(seed.is_seed(i)){
                affinities(i,l) = seed.get_affinity(i,l);
            } else {
                affinities(i,l) = x(seed.get_matrix_id(i));
            }
        }
    }

    return affinities;
}
