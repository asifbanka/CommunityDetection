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

Graph createTestGraph() {

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
    ssSeed << "0 1 0" << endl;
    ssSeed << "4 0 1" << endl;

    Graph g; 
    g.readGraph(ssGraph, ssSeed);
    return g;

}

TEST_CASE( "test basic graph functionality" ) {

    Graph g = createTestGraph();

    REQUIRE(g.numEdges() == 8);
    REQUIRE(g.numVertices() == 5);
    REQUIRE(g.numCommunities() == 2);
    REQUIRE(g.numSeed() == 2);

    REQUIRE_THROWS(g.getDegree(-1));
    REQUIRE(g.getDegree(0) == 1);
    REQUIRE(g.getDegree(1) == 2);
    REQUIRE(g.getDegree(2) == 2);
    REQUIRE(g.getDegree(3) == 2);
    REQUIRE(g.getDegree(4) == 1);
    REQUIRE_THROWS(g.getDegree(5));

    REQUIRE(g.getNeighbors(0).at(0) == 1);
    REQUIRE(g.getNeighbors(0).size() == 1);
    REQUIRE(g.getNeighbors(1).at(0) == 2);
    REQUIRE(g.getNeighbors(1).size() == 2);
    REQUIRE_THROWS(g.getNeighbors(5));

    REQUIRE(g.isSeed(0));
    REQUIRE(!g.isSeed(1));
    REQUIRE(!g.isSeed(2));
    REQUIRE(!g.isSeed(3));
    REQUIRE(g.isSeed(4));
    REQUIRE_THROWS(g.isSeed(5));

    REQUIRE(g.getAffinities(0).at(0) == 1);
    REQUIRE(g.getAffinities(0).at(1) == 0);
    REQUIRE(g.getAffinities(4).at(0) == 0);
    REQUIRE(g.getAffinities(4).at(1) == 1);

    REQUIRE_THROWS(g.getMatrixIndex(-1));
    REQUIRE(g.getMatrixIndex(0) == 0);
    REQUIRE(g.getMatrixIndex(1) == 0);
    REQUIRE(g.getMatrixIndex(2) == 1);
    REQUIRE(g.getMatrixIndex(3) == 2);
    REQUIRE(g.getMatrixIndex(4) == 1);
    REQUIRE_THROWS(g.getMatrixIndex(5));

    REQUIRE_THROWS(g.getVertexId(-1));
    REQUIRE(g.getVertexId(0) == 0);
    REQUIRE(g.getVertexId(1) == 4);
    REQUIRE_THROWS(g.getVertexId(2));
}

TEST_CASE( "test the matrix creation" ) {

    Graph g = createTestGraph();

    Eigen::SparseMatrix<double> D;
    Eigen::SparseMatrix<double> A;
    Eigen::SparseMatrix<double> R;

    buildMatrices(g, D, A, R);

    REQUIRE( D.rows() == 3 );
    REQUIRE( D.cols() == 3 );
    REQUIRE( A.rows() == 3 );
    REQUIRE( A.cols() == 3 ); 
    REQUIRE( R.rows() == 3 );
    REQUIRE( R.cols() == 2 ); 

    REQUIRE( D.coeff(0, 0) == 2 );
    REQUIRE( D.coeff(0, 1) == 0 );
    REQUIRE( D.coeff(0, 2) == 0 );

    REQUIRE( D.coeff(1, 0) == 0 );
    REQUIRE( D.coeff(1, 1) == 2 );
    REQUIRE( D.coeff(1, 2) == 0 );

    REQUIRE( D.coeff(2, 0) == 0 );
    REQUIRE( D.coeff(2, 1) == 0 );
    REQUIRE( D.coeff(2, 2) == 2 );

    //------

    REQUIRE( A.coeff(0, 0) == 0 );
    REQUIRE( A.coeff(0, 1) == 1 );
    REQUIRE( A.coeff(0, 2) == 0 );

    REQUIRE( A.coeff(1, 0) == 1 );
    REQUIRE( A.coeff(1, 1) == 0 );
    REQUIRE( A.coeff(1, 2) == 1 );

    REQUIRE( A.coeff(2, 0) == 0 );
    REQUIRE( A.coeff(2, 1) == 1 );
    REQUIRE( A.coeff(2, 2) == 0 );

    //-------

    REQUIRE( R.coeff(0, 0) == 1 );
    REQUIRE( R.coeff(0, 1) == 0 );

    REQUIRE( R.coeff(1, 0) == 0 );
    REQUIRE( R.coeff(1, 1) == 0 );

    REQUIRE( R.coeff(2, 0) == 0 );
    REQUIRE( R.coeff(2, 1) == 1 );

}

TEST_CASE( "test the solver" ) {

    Graph g = createTestGraph();

    Eigen::SparseMatrix<double> D;
    Eigen::SparseMatrix<double> A;
    Eigen::SparseMatrix<double> R;

    buildMatrices(g, D, A, R);
    solveMatrices(g, D, A, R);

    REQUIRE(g.getAffinities(0).at(0) == Approx(1.0));
    REQUIRE(g.getAffinities(0).at(1) == Approx(0.0));

    REQUIRE(g.getAffinities(1).at(0) == Approx(0.75));
    REQUIRE(g.getAffinities(1).at(1) == Approx(0.25));

    REQUIRE(g.getAffinities(2).at(0) == Approx(0.5));
    REQUIRE(g.getAffinities(2).at(1) == Approx(0.5));

    REQUIRE(g.getAffinities(3).at(0) == Approx(0.25));
    REQUIRE(g.getAffinities(3).at(1) == Approx(0.75));

    REQUIRE(g.getAffinities(4).at(0) == Approx(0.0));
    REQUIRE(g.getAffinities(4).at(1) == Approx(1.0));
}
