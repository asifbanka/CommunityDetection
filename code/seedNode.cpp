#include <iostream>
#include <string>
#include <fstream>
#include <Eigen/Core>
#include <stdexcept>
#include <utility>


class SeedNode{
	private:
		// The seed nodes along with their affinities are stored
		// in a matrix of doubles. For s seed nodes and k communities
		// this matrix has dimension s * (k + 1). The additional 
		// column is for storing the vertex ids of the respective 
		// seed nodes.
		Eigen::Matrix<double, Dynamic, Dynamic, RowMajor> seedNodes;
		
		// The matrix id of each node, along with the fact whether 
		// it is a seed node or not is stored in this vector.
		// If the node is a seed node, then the id is an integer
		// between 0 and s - 1. For non-seed nodes, the id
		// is an integer between 0 and n - s - 1.
		std::vector< std::pair<bool, int> > matrixIds;
		
		int numSeed;
		int numCommunities;
		void read(const char* file_name);
		
	public:
		SeedNode() :
					numSeed(0), 
			  		numCommunities(0), 
			  		{}

		SeedNode(const char* file_name){ read(file_name);}
		bool is_seed(int vert_id);
		int num_seed() {return numSeed;}
		int num_communities() {return numCommunities;}
		int get_matrix_id(int vert_id); // vertex id to matrix id
		int get_affinity(int seed_node_id, int community);
		int get_vertex_id(int matrix_id); // matrix id to vertex id (reqd only for seed nodes)
};

void SeedNode::read(const char* file_name){
	std::ifstream seed_data(file_name);
	if ( !seed_data.is_open() ){
		std::cout << "Cannot open file" << std::endl;
		return;
	}

	// read numSeed, numCommunities
	seed_data >> numSeed >> numCommunities;

	// allocate enough memory
	seedNodes(numSeed, numCommunities + 1);
	
	// first clear, then allocate memory, and initialize 
	matrixIds.clear();
	matrixIds( Graph::num_vertices(), std::make_pair(false, -1) );
	
	// read the data into the matrices seedNode 
	// and matrixIds
	for (int num_s = 0; num_s != numSeed; ++num_s){
		int num_c = 0; 
		seed_data >> seedNodes(num_s, num_c); // this is node_id
		int node_id = (int) seedNode(num_s, num_c);
		matrixIds[node_id].first = true; 	// node_id is a seed node
		matrixIds[node_id].second = num_s; 	// node_id has num_s as matrix id
		for ( ; num_c != numCommunities + 1; ++num_c)
			seed_data >> seedNodes(num_s, num_c);
	}
	
	// assign values to the non-seed node entries of matrixIds
    int counter = 0;
	for (int i = 0; i != Graph::num_vertices(); ++i){
		if ( matrixIds[i].first == false )   // if it is not a seed node
			matrixIds[i].second = counter++; // then set its matrix id
	}

	seed_data.close();

	return;
}

bool SeedNode::is_seed(int vert_id){
	if ( num_seed() == 0 || vert_id >= Graph::num_vertices() )
		throw std::out_of_range ("either no. of seed nodes = 0 or vertex id out of range");

	return matrixIds[vert_id].first;
}

int SeedNode::get_matrix_id(int vert_id){
	if ( vert_id < 0 || vert_id >= Graph::num_vertices )
		throw std::out_of_range("vertex id out of range");
	
	return matrixIds[vert_id].second;
}

int SeedNode::get_vertex_id(int matrix_id){
	if ( matrix_id < 0 || matrix_id >= num_seed() )
		throw std::out_of_range("matrix id does not belong to any seed node");
	
	return seedNode(matrix_id, 0); // the first entry on row matrix_id is the node id 
}

int SeedNode::get_affinity(int seed_node_id, int community){
	if (seed_node_id < 0 || seed_node_id >= num_seed() || community < 0 || community >= num_communities())
		throw std::out_of_range("either seed node id or community id is out of range");

	return seedNode(seed_node_id, community + 1); // one has to add a 1, to get to the correct column 
}

