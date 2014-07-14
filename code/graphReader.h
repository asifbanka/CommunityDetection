#ifndef GUARD_graphReader_h
#define GUARD_graphReader_h
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
	
		// Copy construtor
		Graph(const Graph& rhs){
				numV = rhs.numV;
				numE = rhs.numE;
				adjList = rhs.adjList;
		}

		// Assignment operator
		Graph& operator= (const Graph& rhs){
			if ( this == &rhs )
				return *this;
				
			numV = rhs.numV;
			numE = rhs.numE;
			adjList = rhs.adjList;
			
			return *this;
		}

		void read(const char* file_name);
    	int num_vertices() const { return numV; }
    	int num_edges() const { return numE; }
    	int get_degree(int id) const;
    	std::list<int> get_neighbors(int id);

    	// For now, this is a test function
    	void display_graph();
};
#endif
