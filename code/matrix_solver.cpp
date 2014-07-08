#include <iostream>
#include <Eigen/Sparse>

typedef Eigen::SparseMatrix<double> SMatD;  // declares a column-major sparse matrix type of double
typedef Eigen::Triplet<double> Td; // A triplet is a simple object representing a non-zero entry as 
																	 // the triplet: row index, column index, value.


//param: adjacency lists and set of seed nodes
//return: matrices Q and R
void initMatrices(std::vector<std::list<int>> adjacencyLists,std::set<int> seedNodes,SmatD* Q_pointer,SmatD* R_pointer){

    int numberOfVertices = adjacencyLists.size();
    int numberOfseedVertices = seedNodes.size();
    int numberOfNonSeedVertices = numberOfVertices - numberOfseedVertices;

    //for the translation of indices
    int Q_position = 0;
    int R_position=0;


    /*
    Regarding the translation of vertex name -> matrix index:
    The problem is if you find a vertex in the adjaceny list that was not yet processed you have no way of knowing it's future matrix index.
    So I think there is no way around of parsing the complete list of vertices beforehand to create a translation table

    One possibillity would be to implement the following function f(n) = [number of seed nodes < n]
    Then the index of n for the matrix Q would be n- f(n). 
    For R then we would have to count the 'gaps' between the seed vertices. not really sure if this overhead is worth it to get around traversing
    the whole vertex space
    

    */

    SmatD Q(numberOfNonSeedVertices,numberOfNonSeedVertices);
    SmatD R(numberOfNonSeedVertices, numberOfseedVertices);

    std::vector<T> tripletListQ,tripletListR;
    int numberOfNonZeroesQ = CountNonZeroesQ(adjacencyLists, seedNodes);
    int numberOfNonZeroesR = CountNonZeroesR(adjacencyLists, seedNodes);

    //missing: get number of entries
    tripletListQ.reserve(numberOfNonZeroesQ);
    tripletListR.reserve(numberOfNonZeroesR);
    
    //filling Q and R
    for(int i=0;i<numberOfVertices;++i){
        
        //if the current vertex is not a seed node
        if(seedNodes.find(i) = seedNodes.end()){
        
            for (std::list<int>::const_iterator iterator = adjacencyLists[i].begin(); iterator != adjacencyLists[i].end;++iterator) {
                if(iterator != adjacencyLists[i].begin()){ //assume the first index of the list is the number of neighbours
                    if(seedNodes.find(*iterator) = seedNodes.end()){           
                        tripletListQ.push_back(T(i,*iterator,1/adjacencyLists[i].front())); //dis is wrong (translation from vertex id to matrix id missing)
                        ++Q_position;
                    } else {
                        tripletListR.push_back(T(i,*iterator,1)); // dis is also wrong
                        ++R_position;
                    }
                }
            }
        
        

        
        
        }
    }

    //building Q and R
    Q.setFromTriplets(tripletListQ.begin(), tripletListQ.end());
    R.setFromTriplets(tripletListR.begin(), tripletListR.end());


    Q_pointer = &Q;
    R_pointer = &R;

}


int CountNonZeroesR(std::vector<std::list<int>> adjacencyLists,std::set<int> seedNodes){
    int result = 0;
    for(std::set<int>::const_iterator seeds=seedNodes.begin();seeds !=seedNodes.end;++seeds){
        for (std::list<int>::const_iterator iterator = adjacencyLists[*seeds].begin(); iterator != adjacencyLists[*seeds].end;++iterator) {
                if(seedNodes.find(*iterator) != seedNodes.end()){ 
                    result++; //count all edges of the form (seed node) -> (non seed node)
                }
        }
    }

    return result;
}

//probably possible to be more efficient
int CountNonZeroesQ(std::vector<std::list<int>> adjacencyLists,std::set<int> seedNodes){
    int result = 0;
    for(int i=0;i<adjacencyLists.size();++i){
         //if the current vertex is not a seed node
        if(seedNodes.find(i) = seedNodes.end()){
            for (std::list<int>::const_iterator iterator = adjacencyLists[i].begin(); iterator != adjacencyLists[i].end;++iterator) {
                if(seedNodes.find(*iterator) = seedNodes.end()){ 
                    result++; //count all edges of the form (non seed node) -> (non seed node)
                }
            }    
        }
    }

    return result;
}
