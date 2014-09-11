#pragma once 

#include <Eigen/Sparse>
#include "graph.hpp"

void buildMatrices(const Graph &g,
                   Eigen::SparseMatrix<double> &D,
                   Eigen::SparseMatrix<double> &A,
                   Eigen::SparseMatrix<double> &R);
