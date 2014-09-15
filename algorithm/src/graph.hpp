#ifndef GUARD_graphReader_h
#define GUARD_graphReader_h

#include <string>
#include <vector>
#include <iostream>
#include <stdexcept>

struct NodeAttribute {
    // neighbors of this vertex
    std::vector<int> neighbors;
    // affinity vector of this vertex
    std::vector<double> affinities;
    // the matrix index in the R matrix (if the node is a seed node) 
    // or the matrix index in the A and D matrix (if the node is a non-seed node) 
    int matrixIndex;
    // true if node is a seed node
    bool isSeed;

    // initialize as non-seed node
    NodeAttribute() : matrixIndex(-1), isSeed(false) {};
};

class Graph{
private:
    int mNumVertices;
    int mNumEdges;
    int mNumCommunities;
    int mNumSeed;
    std::vector<NodeAttribute> mNodeAttributes;
    std::vector<int> mSeedNodes;

public:
    /*
     * Structure of the graph File:
     * ----------------------------
     *
     * The first line contains the number of nodes and edges in the graph
     * The following lines represent one directed edge each.
     * "from" and "to" are nodeIds in the range [0, numberOfNodes-1]
     * The graph needs to be undirected.
     * If there is an edge from node a to node b, there also needs to be
     * an edge from node b to node a.
     *
     * numberOfNodes numberOfEdges
     * from to
     * from to
     * from to
     * ...
     *
     * Structure of the seed File:
     * ---------------------------
     *
     *  seedNodeId needs to be in range [0, numberOfNodes-1]
     *
     *  numberOfSeedNodes numberOfCommunities
     *  seedNodeId affinitytoCommunity1 affinitytoCommunity2 ... affinityToCommunity$(numberOfCommunities)
     *  seedNodeId affinitytoCommunity1 affinitytoCommunity2 ... affinityToCommunity$(numberOfCommunities)
     *  seedNodeId affinitytoCommunity1 affinitytoCommunity2 ... affinityToCommunity$(numberOfCommunities)
     *
     */
    void readGraph(const std::string &filenameGraph, const std::string filenameSeed);
    void readGraph(std::istream &isGraph, std::istream &isSeed);

    void writeCommunities(std::string filenameCommunities);
    void writeCommunities(std::ostream &osCommunities);

    int numCommunities() const {return mNumCommunities;}
    int numVertices() const { return mNumVertices; }
    int numEdges() const { return mNumEdges; }
    int numSeed() const {return mNumSeed ;}

    int getDegree(int id) const {
        return mNodeAttributes.at(id).neighbors.size();
    }
    const std::vector<int> &getNeighbors(int id) const {
        return mNodeAttributes.at(id).neighbors;
    }
    bool isSeed(int id) const { 
        return mNodeAttributes.at(id).isSeed;
    }
    const std::vector<double> &getAffinities(int id) const {
        return mNodeAttributes.at(id).affinities;
    }
    std::vector<double> &getAffinities(int id) {
        return mNodeAttributes.at(id).affinities;
    }
    int getMatrixIndex(int id) const {
        return mNodeAttributes.at(id).matrixIndex;
    }
    int getVertexId(int matrixIndex) const {
        return mSeedNodes.at(matrixIndex);
    }
};


#endif
