#ifndef GUARD_seedNode_h
#define GUARD_seedNode_h

#include <iostream>
#include <fstream>
#include <vector> 
#include <Eigen/Core>
#include <stdexcept>
#include <utility>
#include "graphReader.h"

class SeedNode{
	private:
		// The seed nodes along with their affinities are stored
		// in a matrix of doubles. For s seed nodes and k communities
		// this matrix has dimension s * (k + 1). The additional 
		// column is for storing the vertex ids of the respective 
		// seed nodes.
		Eigen::MatrixXd seedNodes;
		
		// The matrix id of each node, along with the fact whether 
		// it is a seed node or not is stored in this vector.
		// If the node is a seed node (TRUE), then the id is an integer
		// between 0 and s - 1. For non-seed nodes (FALSE), the id
		// is an integer between 0 and n - s - 1.
		std::vector< std::pair<bool, int> > matrixIds;
		
		int numSeed;
		int numCommunities;
		void read(const char* file_name, Graph& g);
		
	public:
		SeedNode() :
					numSeed(0), 
			  		numCommunities(0) 
			  		{}

		SeedNode(const char* file_name, Graph& g){ read(file_name, g); }
		bool is_seed(int vert_id);
		int num_seed() {return numSeed;}
		int num_communities() {return numCommunities;}
		int get_matrix_id(int vert_id); // vertex id to matrix id
		int get_affinity(int seed_node_id, int community);
		int get_vertex_id(int matrix_id); // matrix id to vertex id (reqd only for seed nodes)
};
#endif
