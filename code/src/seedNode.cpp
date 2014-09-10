#include "seedNode.hpp"
#include "graph.hpp"


void SeedNode::read(const char* file_name, Graph& g){
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
	for (int i = 0; i != g.num_vertices(); ++i)
		matrixIds.push_back(std::make_pair(false, -1));
		
	
	// read the data into the matrices seedNode 
	// and matrixIds
	for (int num_s = 0; num_s != numSeed; ++num_s){
		int num_c = 0; 
		seed_data >> seedNodes(num_s, num_c); // this is node_id
		int node_id = (int) seedNodes(num_s, num_c);
		matrixIds[node_id].first = true; 	// node_id is a seed node
		matrixIds[node_id].second = num_s; 	// node_id has num_s as matrix id
		for ( ; num_c != numCommunities + 1; ++num_c)
			seed_data >> seedNodes(num_s, num_c);
	}
	
	// assign values to the non-seed node entries of matrixIds
    int counter = 0;
	for (int i = 0; i != g.num_vertices(); ++i){
		if ( matrixIds[i].first == false )   // if it is not a seed node
			matrixIds[i].second = counter++; // then set its matrix id
	}

	seed_data.close();

	return;
}

bool SeedNode::is_seed(int vert_id){
	int sz = matrixIds.size();
	if ( num_seed() == 0 || sz == 0 || vert_id >= sz )
		throw std::out_of_range ("either no. of seed nodes = 0 or vertex id out of range");

	return matrixIds[vert_id].first;
}

int SeedNode::get_matrix_id(int vert_id){
	int sz = matrixIds.size();
	if ( vert_id < 0 || sz == 0 || vert_id >= sz )
		throw std::out_of_range("vertex id out of range");
	
	return matrixIds[vert_id].second;
}

int SeedNode::get_vertex_id(int matrix_id){
	if ( matrix_id < 0 || matrix_id >= num_seed() )
		throw std::out_of_range("matrix id does not belong to any seed node");
	
	return seedNodes(matrix_id, 0); // the first entry on row matrix_id is the node id 
}

int SeedNode::get_affinity(int seed_node_id, int community){
	if ( seed_node_id < 0 			|| 
		 seed_node_id >= num_seed() || 
		 community < 0 				|| 
		 community >= num_communities()	)
		throw std::out_of_range("either seed node id or community id is out of range");
	return seedNodes(get_matrix_id(seed_node_id), community + 1); 
	// one has to add a 1, to get to the correct column 
}

