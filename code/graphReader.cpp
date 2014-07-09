#include <iostream>
#include <vector>
#include <list>
#include <fstream>

class Graph{
	private:
    typedef std::size_t size_type;
		size_type numV;
		size_type numE;
		// note that the first entry of the list is the 
		// degree of the vertex; the next entries 
		// are the neighbors.
		std::vector< std::list<size_type> > adjList;
	
	public:
		// Constructors: the second constructor 
   	// creates a graph by reading it from a file
    Graph() : numV(0), numE(0) {}
		Graph(const char* file_name){read(file_name);}

		void read(const char* file_name);
    size_type num_vertices() {return numV;}
    size_type num_edges() {return numE;}
    size_type get_degree(size_type id);
    std::list<size_type> get_neighbors(size_type id);

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
	Graph::size_type dat1, dat2;
	graph_data >> dat1 >> dat2;
	numV = dat1;
	numE = dat2;

	// allocate enough space for a vector of size numV
  for (Graph::size_type i = 0; i != numV; ++i){
  	std::list< Graph::size_type > temp_list;
		// create the counter to keep track of the degree
		Graph::size_type counter = 0;
		temp_list.pushback(counter);
    adjList.push_back( temp_list );
	}
	
  // finally, read the data into the vector
  while ( graph_data >> dat1 >> dat2 ){
		std::list< Graph::size_type >::
					iterator it1 = adjList[dat1].begin(),
									 it2 = adjList[dat2].begin();																					
  	
		// push the next neighbor
		adjList[dat1].push_back(dat2);
		++(*it1); // and increment counter
		
		// do this again for the symmetric case
    adjList[dat2].push_back(dat1);
		++(*it2);
  }
  return;
}


void Graph::display_graph(){
	if ( adjList.size() == 0 ){
  	std::cout << "Graph empty." << std::endl;
    return;
  }

  for ( Graph::size_type i = 0; i != adjList.size(); ++i ){
  	std::cout << "vertex " << i << " is adjacent to: " << std::endl;
    std::list<Graph::size_type>::const_iterator it;
    for ( it = adjList[i].begin(); it != adjList[i].end(); ++it )
    	std::cout << *it << ", ";
     	std::cout << std::endl;
 	}
}

int main(){
    Graph graph("test.txt");
    graph.print();
    std::cout << graph.getNumV() << " " << graph.getNumE() << std::endl;

    return 0;
}
