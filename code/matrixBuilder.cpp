#include <iostream>
#include <Eigen/Sparse>

typedef Eigen::SparseMatrix<double> SMatD;  // declares a column-major sparse matrix type of double
typedef Eigen::Triplet<double> Td; // A triplet is a simple object representing a non-zero entry as 
																	 // the triplet: row index, column index, value.


//param: graph and seed node class
//return: matrices D, A and R
void initMatrices(Graph* g,SeedNode* seed,SmatD* D_pointer,SmatD* A_pointer, SmatD* R_pointer){

    const int numberOfVertices = g->num_vertices();
    const int numberOfseedVertices = seed->num_seed();
    const int numberOfNonSeedVertices = numberOfVertices - numberOfseedVertices;

   


    
    // generate the matrices
    SmatD A(numberOfNonSeedVertices,numberOfNonSeedVertices);
    SmatD D(numberOfNonSeedVertices,numberOfNonSeedVertices)
    SmatD R(numberOfNonSeedVertices, numberOfseedVertices);

    std::vector<T> tripletListA,tripletListD,tripletListR;
    const int numberOfNonZeroesA = g->num_edges();
    const int numberOfNonZeroesD = numberOfNonSeedVertices;
    const int numberOfNonZeroesR = numberOfNonZeroesA;      //maybe get a bestter estimate here

    tripletListA.reserve(numberOfNonZeroesA);
    tripletListD.reserve(numberOfNonZeroesD);
    tripletListR.reserve(numberOfNonZeroesR);
    
    //filling A, D and R
    for(int i=0;i<numberOfVertices;++i){ //going over all vertices
        if(!seed->is_seed(i)){ //if the current vertex is not a seed node
            tripletListD.push_back(T(g->get_matrix_id(i),g->get_matrix_id(i),g->get_degree(i)); 

            //going over all neighbors of i and adding entries to A and R depending on the neighbor beeing a seed node
            for (std::list<int>::const_iterator neighbor = g->get_neighbors(i).begin(); neighbor != g->get_neighbors(i).end; ++neighbor) {
                    if(!seed->is_seed(*neighbor)){           
                        tripletListA.push_back(T(g->get_matrix_id(i),g->get_matrix_id(*neighbor),1); 
                    } else {
                        tripletListR.push_back(T(g->get_matrix_id(i),g->get_matrix_id(*neighbor),1)); 
                    }
            }
        }
    }

    //building A, D and R
    A.setFromTriplets(tripletListA.begin(), tripletListA.end());
    D.setFromTriplets(tripletListD.begin(), tripletListD.end());
    R.setFromTriplets(tripletListR.begin(), tripletListR.end());


    A_pointer = &A;
    D_pointer = &D;
    R_pointer = &R;

}


