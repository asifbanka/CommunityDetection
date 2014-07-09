#include <iostream>
#include <Eigen/Sparse>
#include <Eigen/Dense>
#include <vector>

typedef Eigen::SparseMatrix<double> SMatD;  // declares a column-major sparse matrix type of double
using Eigen::MatrixXd;

MatrixXd solve (graph* g, seedNode* seed, SMatD& A, SMatD& D, SMatD& R){
    SMatD D_A = D - A;
    const int numberOfCommunities = seed->num_communities();
    const int numberOfNonSeedNodes = NON_SEED;
    const int numberOfSeedNodes = SEED;
    const int numberOfNodes = NUM_NODES;
    MatrixXd affinities(numberOfNodes,numberOfCommunities);
    Eigen::SimplicialCholesky<SpMat> chol(D_A);  // performs a Cholesky factorization of (D-A)
    


    //for every community
    for(int l = 0; l < numberOfCommunities, ++l){
        Eigen::VectorXd sum(numberOfNonSeedNodes);
        Eigen::VectorXd b(numberOfNonSeedNodes);

        for(int j=0; j<numberOfSeedNodes; ++j){
            sum+= seed->get_affinity(seed->get_vertexId(j),l)*R.col(l);
        }

        b = D * sum;

        Eigen::VectorXd x = chol.solve(b); // use the factorization to solve for the given right hand side


        //write the affinities for community i

        for(int i=0; i<numberOfNodes;++i){
            if(seed->is_seed(j)){
                affinities(i,l) = seed->get_affinity(i,l);
            } else {
                affinities(i,l) = x(seed->get_matrix_id(i));
            }
        }
    }

    return affinities;



}