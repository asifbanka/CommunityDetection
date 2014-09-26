#include "graph.hpp"

#include <fstream>
#include <iostream>
#include <stdexcept>

using namespace std;

void Graph::readGraph(const std::string &filenameGraph, const std::string filenameSeed) {
    cout << "read graph from txt-file: " << filenameGraph << endl;
    ifstream ifsGraph (filenameGraph.c_str());
    if (!ifsGraph.is_open())
        throw std::invalid_argument("Cannot open graph file");

    cout << "read seeds from txt-file: " << filenameSeed << endl;
    ifstream ifsSeed (filenameSeed.c_str());
    if (!ifsSeed.is_open())
        throw std::invalid_argument("Cannot open seed file");

    readGraph(ifsGraph, ifsSeed);
}

void Graph::readGraph(std::istream &isGraph, std::istream &isSeed) {

    // Fill graph
    // ----------

    isGraph >> mNumVertices >> mNumEdges;

    mNodeAttributes.resize(mNumVertices);

    int from, to;
    while(isGraph >> from >> to) {
        mNodeAttributes.at(from).neighbors.push_back(to);
    }

    int tmp = 0;
    for(auto node = mNodeAttributes.begin(); node != mNodeAttributes.end(); node++) {
        tmp += node->neighbors.size();
    }
    if(tmp != mNumEdges)
        throw std::invalid_argument("wrong number of edges");

    // Fill seed nodes
    // ---------------

    // use this:
    // http://stackoverflow.com/questions/236129/how-to-split-a-string-in-c

    isSeed >> mNumSeed >> mNumCommunities;

    for (int matrixId = 0; matrixId < mNumSeed; matrixId++) {
        int nodeId;
        isSeed >> nodeId;
        mNodeAttributes.at(nodeId).isSeed = true;
        for(int j = 0; j < mNumCommunities; j++) {
            double tmp;
            isSeed >> tmp;
            mNodeAttributes.at(nodeId).affinities.push_back(tmp);
        }
    }
    int matrixIndexSeed = 0;
    int matrixIndexNonSeed = 0;
    for(int nodeId = 0; nodeId < mNumVertices; nodeId++) {
        auto &node = mNodeAttributes.at(nodeId);
        if(node.isSeed) {
            node.matrixIndex = matrixIndexSeed++;
            mSeedNodes.push_back(nodeId);
        }
        else {
            node.matrixIndex = matrixIndexNonSeed++;
        }
    }
}

void Graph::writeCommunities(std::string filenameCommunities){
    cout << "writing communities to file: " << filenameCommunities << endl;
    ofstream osCommunities(filenameCommunities.c_str());
    if(!osCommunities.is_open())
        throw std::invalid_argument("Cannot write to community file");
    writeCommunities(osCommunities);
}

void Graph::writeCommunities(std::ostream &osCommunities) {
    osCommunities << mNumVertices << " " << mNumCommunities << endl;
    for(int i = 0; i < mNumVertices; i++) {
        osCommunities << i << " ";
        for(int j = 0; j < mNumCommunities; j++) {
            osCommunities << getAffinities(i).at(j) << " ";
        }
        osCommunities << endl;
    }
}
