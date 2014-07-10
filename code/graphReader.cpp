#include <iostream>
#include <vector>
#include <list>
#include <fstream>

class Graph{
	friend class SeedNode;
	private:
		int numV;
		int numE;
		// note that the first entry of the list is the 
		// degree of the vertex; the next entries 
		// are the neighbors.
		std::vector< std::list<int> > adjList;
	
	public:
		// Constructors: the second constructor 
   		// creates a graph by reading it from a file
    	Graph() : numV(0), numE(0) {}
		Graph(const char* file_name){read(file_name);}

		void read(const char* file_name);
    	int num_vertices() {return numV;}
    	int num_edges() {return numE;}
    	int get_degree(int id);
    	std::list<int> get_neighbors(int id);

    	// For now, this is a test function
    	void display_graph();
};

void Graph::read(const char* file_name){
	std::ifstream graph_data(file_name);
	if ( !graph_data.is_open() ){
		std::cout << "Cannot open file" << std::endl;
		return;
	}	

  	// first clear old data
  	adjList.clear();

	// then, read numV and numE
	int dat1, dat2;
	graph_data >> dat1 >> dat2;
	numV = dat1;
	numE = dat2;

	// allocate enough space for a vector of size numV
  	for (int i = 0; i != numV; ++i){
  		std::list<int> temp_list;
		// create the counter to keep track of the degree
		int counter = 0;
		temp_list.push_back(counter);
    	adjList.push_back( temp_list );
	}
	
  // finally, read the data into the vector
  while ( graph_data >> dat1 >> dat2 ){
		// push the next neighbor
		adjList[dat1].push_back(dat2);
		++adjList[dat1].front();
		
		// do this again for the symmetric case
    adjList[dat2].push_back(dat1);
		++adjList[dat2].front();
  }

  graph_data.close();
  
  return;
}


void Graph::display_graph(){
	if ( adjList.size() == 0 ){
  	std::cout << "Graph empty." << std::endl;
    return;
  }

	int sz = num_vertices();
  	for ( int i = 0; i != sz; ++i ){
		std::cout << "vertex " << i << " has degree: " << 
			adjList[i].front() << std::endl;

  	std::cout << "vertex " << i << " is adjacent to: " << std::endl;
	typedef std::list<int>::const_iterator iter;
	// the iterator points beyond the counter!
    iter it = adjList[i].begin();
	++it; // the first location of the list contains the degree
    for ( ; it != adjList[i].end(); ++it )
    	std::cout << *it << ", ";
    std::cout << std::endl;
 	}
}

int Graph::get_degree(int id){
	return Graph::adjList[id].front();	
}

std::list<int> Graph::get_neighbors(int vert_id){
	std::list<int> neighbors;
  	typedef std::list<int>::const_iterator iter;
	iter it = adjList[vert_id].begin(); 
	++it; // the first location contains the degree info
	for ( ; it != adjList[vert_id].end(); ++it)
		neighbors.push_back(*it);
	
	return neighbors;
}


//int main(){
//    Graph graph("test_for_graph_reader.txt");
//    graph.display_graph();
//	for (int i = 0; i != graph.num_vertices(); ++i){
//		std::list<int> neighbors = graph.get_neighbors(i);
//		std::cout << "The neighbors of vertex " << i << " are: " << std::endl;
//		for (std::list<int>::const_iterator it = neighbors.begin(); 
//				it != neighbors.end(); ++it)
//
//			std::cout << *it << ", "; 
//	}
//
//    return 0;
//}
