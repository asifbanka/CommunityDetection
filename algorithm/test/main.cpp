// This line tells Catch to provide a main() - only do this in one cpp file
#define CATCH_CONFIG_MAIN

#include <iostream>

#include <Eigen/Sparse>
#include "catch.hpp"

#include "graph.hpp"
#include "matrixBuilder.hpp"
#include "matrixSolver.hpp"

using namespace std;
using namespace Eigen;

Graph createTestGraph1() {
    stringstream ssGraph;
    ssGraph << "5 8" << endl;
    ssGraph << "0 1" << endl;
    ssGraph << "1 2" << endl;
    ssGraph << "2 3" << endl;
    ssGraph << "3 4" << endl;
    ssGraph << "4 3" << endl;
    ssGraph << "3 2" << endl;
    ssGraph << "2 1" << endl;
    ssGraph << "1 0" << endl;

    stringstream ssSeed;
    ssSeed << "2 2" << endl;
    ssSeed << "0 1.0 0.0" << endl;
    ssSeed << "4 0.0 1.0" << endl;

    Graph g; 
    g.readGraph(ssGraph, ssSeed);
    return g;

}

//TEST_CASE( "test basic graph functionality" ) {

    //Graph g = createTestGraph1();

    //REQUIRE(g.numEdges() == 8);
    //REQUIRE(g.numVertices() == 5);
    //REQUIRE(g.numCommunities() == 2);
    //REQUIRE(g.numSeed() == 2);

    //REQUIRE_THROWS(g.getDegree(-1));
    //REQUIRE(g.getDegree(0) == 1);
    //REQUIRE(g.getDegree(1) == 2);
    //REQUIRE(g.getDegree(2) == 2);
    //REQUIRE(g.getDegree(3) == 2);
    //REQUIRE(g.getDegree(4) == 1);
    //REQUIRE_THROWS(g.getDegree(5));

    //REQUIRE(g.getNeighbors(0).at(0) == 1);
    //REQUIRE(g.getNeighbors(0).size() == 1);
    //REQUIRE(g.getNeighbors(1).at(0) == 2);
    //REQUIRE(g.getNeighbors(1).size() == 2);
    //REQUIRE_THROWS(g.getNeighbors(5));

    //REQUIRE(g.isSeed(0));
    //REQUIRE(!g.isSeed(1));
    //REQUIRE(!g.isSeed(2));
    //REQUIRE(!g.isSeed(3));
    //REQUIRE(g.isSeed(4));
    //REQUIRE_THROWS(g.isSeed(5));

    //REQUIRE(g.getAffinities(0).at(0) == 1);
    //REQUIRE(g.getAffinities(0).at(1) == 0);
    //REQUIRE(g.getAffinities(4).at(0) == 0);
    //REQUIRE(g.getAffinities(4).at(1) == 1);

    //REQUIRE_THROWS(g.getMatrixIndex(-1));
    //REQUIRE(g.getMatrixIndex(0) == 0);
    //REQUIRE(g.getMatrixIndex(1) == 0);
    //REQUIRE(g.getMatrixIndex(2) == 1);
    //REQUIRE(g.getMatrixIndex(3) == 2);
    //REQUIRE(g.getMatrixIndex(4) == 1);
    //REQUIRE_THROWS(g.getMatrixIndex(5));

    //REQUIRE_THROWS(g.getVertexId(-1));
    //REQUIRE(g.getVertexId(0) == 0);
    //REQUIRE(g.getVertexId(1) == 4);
    //REQUIRE_THROWS(g.getVertexId(2));
//}

//TEST_CASE( "test the matrix creation" ) {

    //Graph g = createTestGraph1();

    //Eigen::SparseMatrix<double> D;
    //Eigen::SparseMatrix<double> A;
    //Eigen::SparseMatrix<double> R;

    //buildMatrices(g, D, A, R);

    //REQUIRE( D.rows() == 3 );
    //REQUIRE( D.cols() == 3 );
    //REQUIRE( A.rows() == 3 );
    //REQUIRE( A.cols() == 3 ); 
    //REQUIRE( R.rows() == 3 );
    //REQUIRE( R.cols() == 2 ); 

    //REQUIRE( D.coeff(0, 0) == 2 );
    //REQUIRE( D.coeff(0, 1) == 0 );
    //REQUIRE( D.coeff(0, 2) == 0 );

    //REQUIRE( D.coeff(1, 0) == 0 );
    //REQUIRE( D.coeff(1, 1) == 2 );
    //REQUIRE( D.coeff(1, 2) == 0 );

    //REQUIRE( D.coeff(2, 0) == 0 );
    //REQUIRE( D.coeff(2, 1) == 0 );
    //REQUIRE( D.coeff(2, 2) == 2 );

    ////------

    //REQUIRE( A.coeff(0, 0) == 0 );
    //REQUIRE( A.coeff(0, 1) == 1 );
    //REQUIRE( A.coeff(0, 2) == 0 );

    //REQUIRE( A.coeff(1, 0) == 1 );
    //REQUIRE( A.coeff(1, 1) == 0 );
    //REQUIRE( A.coeff(1, 2) == 1 );

    //REQUIRE( A.coeff(2, 0) == 0 );
    //REQUIRE( A.coeff(2, 1) == 1 );
    //REQUIRE( A.coeff(2, 2) == 0 );

    ////-------

    //REQUIRE( R.coeff(0, 0) == 1 );
    //REQUIRE( R.coeff(0, 1) == 0 );

    //REQUIRE( R.coeff(1, 0) == 0 );
    //REQUIRE( R.coeff(1, 1) == 0 );

    //REQUIRE( R.coeff(2, 0) == 0 );
    //REQUIRE( R.coeff(2, 1) == 1 );

//}

//TEST_CASE( "test the solver" ) {

    //Graph g = createTestGraph1();

    //Eigen::SparseMatrix<double> D;
    //Eigen::SparseMatrix<double> A;
    //Eigen::SparseMatrix<double> R;

    //buildMatrices(g, D, A, R);
    //solveMatrices(g, D, A, R);

    //REQUIRE(g.getAffinities(0).at(0) == Approx(1.0));
    //REQUIRE(g.getAffinities(0).at(1) == Approx(0.0));

    //REQUIRE(g.getAffinities(1).at(0) == Approx(0.75));
    //REQUIRE(g.getAffinities(1).at(1) == Approx(0.25));

    //REQUIRE(g.getAffinities(2).at(0) == Approx(0.5));
    //REQUIRE(g.getAffinities(2).at(1) == Approx(0.5));

    //REQUIRE(g.getAffinities(3).at(0) == Approx(0.25));
    //REQUIRE(g.getAffinities(3).at(1) == Approx(0.75));

    //REQUIRE(g.getAffinities(4).at(0) == Approx(0.0));
    //REQUIRE(g.getAffinities(4).at(1) == Approx(1.0));
//}

//-------------------------------------------------------

// create a graph consistiting of numberOfNodes nodes, where node 0 and 1 are
// seed nodes of community 0 and 1 respectively and all other nodes belong to
// both communities equally.
Graph createTestGraph2(int numberOfNodes) {

    // nodes 0 and 1 are seed nodes
    stringstream ssSeed;
    ssSeed << "2 2" << endl;
    ssSeed << "0 1.0 0.0" << endl;
    ssSeed << "1 0.0 1.0" << endl;

    stringstream ssGraph;
    ssGraph << numberOfNodes << " " << (6 * (numberOfNodes - 2)) << endl;

    // connect all non-seed nodes to both seed nodes
    for(int i = 2; i < numberOfNodes; i++) {
        ssGraph << "0 " << i << endl;
        ssGraph << "1 " << i << endl;
        ssGraph << i << " 0" << endl;
        ssGraph << i << " 1" << endl;
    }

    // add some random edges between non-seed nodes
    for(int i = 2; i < numberOfNodes; i++) {
        int j = ((i + 13374242) % (numberOfNodes - 2)) + 2;
        ssGraph << i << " " << j << endl;
        ssGraph << j << " " << i << endl;
    }

    Graph g; 
    g.readGraph(ssGraph, ssSeed);
    return g;
}

//TEST_CASE( "test the solver on a bigger, more complex graph" ) {

    //int numberOfNodes = 1234;

    //Graph g = createTestGraph2(numberOfNodes);

    //Eigen::SparseMatrix<double> D;
    //Eigen::SparseMatrix<double> A;
    //Eigen::SparseMatrix<double> R;

    //buildMatrices(g, D, A, R);
    //solveMatrices(g, D, A, R);

    //REQUIRE(g.getAffinities(0).at(0) == Approx(1.0));
    //REQUIRE(g.getAffinities(0).at(1) == Approx(0.0));

    //REQUIRE(g.getAffinities(1).at(0) == Approx(0.0));
    //REQUIRE(g.getAffinities(1).at(1) == Approx(1.0));

    //for(int i = 2; i < numberOfNodes; i++) {
        //REQUIRE(g.getAffinities(i).at(0) == Approx(0.5));
        //REQUIRE(g.getAffinities(i).at(1) == Approx(0.5));
    //}
//}

//-------------------------------------------------------

void addEdge(stringstream &ss, int a, int b) {
    ss << a << " " << b << endl;
    ss << b << " " << a << endl;
}

Graph createTestGraph3(int N) {

    // seed nodes (0,1,2) and (3,4,5)
    stringstream ssSeed;
    ssSeed << "6 6" << endl;

    ssSeed << (0) << " 1 0 0 0 0 0" << endl;
    ssSeed << (1) << " 0 1 0 0 0 0" << endl;
    ssSeed << (2) << " 0 0 1 0 0 0" << endl;

    ssSeed << (N+3) << " 0 0 0 1 0 0" << endl;
    ssSeed << (N+4) << " 0 0 0 0 1 0" << endl;
    ssSeed << (N+5) << " 0 0 0 0 0 1" << endl;

    //------------------------

    stringstream ssGraph;
    ssGraph << (2*N + 6) << " " << (18*(N)) << endl;

    for(int i = 0; i < N ; i++) {


        addEdge(ssGraph, 0, i+3);
        addEdge(ssGraph, 1, i+3);
        addEdge(ssGraph, 2, i+3);

        addEdge(ssGraph, N+3, N+i+6);
        addEdge(ssGraph, N+4, N+i+6);
        addEdge(ssGraph, N+5, N+i+6);

        for(int j = 0; j < 3; j++) {
            int k = ((i+j) % N);
            addEdge(ssGraph, i+3, N+k+6);
        }
    }

    Graph g; 
    g.readGraph(ssGraph, ssSeed);
    return g;
}

TEST_CASE( "asdfasdfasdf" ) {

    int N = 70;

    Graph g = createTestGraph3(N);

    Eigen::SparseMatrix<double> D;
    Eigen::SparseMatrix<double> A;
    Eigen::SparseMatrix<double> R;

    buildMatrices(g, D, A, R);

    cout << "D" << endl << D << endl;
    cout << "A" << endl << A << endl;
    cout << "R" << endl << R << endl;

    solveMatrices(g, D, A, R);

    for(int i = 0; i < 3 ; i++) {
        REQUIRE(g.getAffinities(i).at(i) == Approx(1));
    }
    for(int i = 0; i < 3 ; i++) {
        REQUIRE(g.getAffinities(N+3+i).at(i+3) == Approx(1));
    }

    for(int i = 3; i < N+3; i++) {
        for(int j = 0; j < 3; j++) {
            REQUIRE(g.getAffinities(i).at(j) == Approx(2.0/9.0));
        }
        for(int j = 3; j < 6; j++) {
            REQUIRE(g.getAffinities(i).at(j) == Approx(1.0/9.0));
        }
    }
    for(int i = N+6; i < 2*N+6; i++) {
        for(int j = 0; j < 3; j++) {
            REQUIRE(g.getAffinities(i).at(j) == Approx(1.0/9.0));
        }
        for(int j = 3; j < 6; j++) {
            REQUIRE(g.getAffinities(i).at(j) == Approx(2.0/9.0));
        }
    }
}


