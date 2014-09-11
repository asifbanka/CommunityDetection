#ifndef GUARD_matrixBuilder_h
#define GUARD_matrixBuilder_h
#include <iostream>
#include <Eigen/Sparse>
#include "graphReader.h"
#include "seedNode.h"


																	 // the triplet: row index, column index, value.
//param: graph and seed node class
void initMatrices(Graph& g, SeedNode& seed, Eigen::SparseMatrix<double>& D, Eigen::SparseMatrix<double>& A, Eigen::SparseMatrix<double>& R);


#endif
