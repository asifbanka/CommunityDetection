// This file takes a graph file and computes the comunities

#include <iostream>
#include "graphReader.h"
#include "seedNode.h"


int main(int argc, char* argv[]){
 // Check the number of parameters
    if (argc < 3) {
        // Tell the user how to run the program
        std::cerr << "Please give a graph file and a seedNode file" << std::endl;
        return 1;
    }

    const char* graph_file = argv[1];
    const char* seedNode_file = argv[2];
    //std::cout << graph_file << std::endl;

    Graph g(graph_file);
    SeedNode seed(seedNode_file,g);
    g.display_graph();
   // std::cout << "num seed: " << seed.num_seed() << " num communities: " << seed.num_communities() << std::endl;


    return 1;
}
