#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <Eigen/Sparse>
#include <vector>

typedef Eigen::SparseMatrix<int> SmatI; //column-major sparse matrix
typedef Eigen::Triplet<int> T;

bool getCommunityInfo(const char* file_name, SmatI& commMat);

// ALERT! the matrix is stored in column major format!!
bool display(const SmatI& commMat);

int main(){
	SmatI commMat;
	getCommunityInfo("comm1.dat", commMat);
	display(commMat);
		
	return 0;
}
