#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <Eigen/Sparse>
#include <vector>

typedef Eigen::SparseMatrix<int> SmatI; //column-major sparse matrix
typedef Eigen::Triplet<int> T;

bool getCommunityInfo(const char* file_name, SmatI& commMat){
	std::ifstream comm_file(file_name);
	if ( !comm_file.is_open() ){
		std::cout << "Cannot open community file." << std::endl;
		return 0;
	}

	// for parsing the file line by line
	std::string line;
	std::getline(comm_file, line);
	std::istringstream iss(line);
	
	// First read the number of vertices, the number 
	// of communities, and maximum number of overlaps
	int num_v = 0, num_c = 0, max_overlap = 0;
	iss >> num_v >> num_c >> max_overlap;
	
	// next resize the sparse matrix to store this info
	commMat.resize(num_v, num_c);
	std::vector<T> tripletListCM;
	const int numberOfNonZeroesCM = num_v * max_overlap; // calculate number of non-zero entries
	tripletListCM.reserve(numberOfNonZeroesCM);

	while ( std::getline(comm_file, line) ){
    	std::istringstream iss(line);
		int vert_id = 0;
		iss >> vert_id; 
		
		int comm_no = 0;
		while ( iss >> comm_no ) // this is actually the community number
			tripletListCM.push_back( T(vert_id - 1, comm_no - 1, 1) );		
	}
	
	commMat.setFromTriplets(tripletListCM.begin(), tripletListCM.end());
	return 1;
}

// ALERT! the matrix is stored in column major format!!
bool display(const SmatI& commMat){
	if (commMat.rows() == 0){
		std::cout << "Matrix not yet filled in!" << std::endl;
		return 0;
	}

	for (int num_cols = 0; num_cols != commMat.outerSize(); ++num_cols){
		std::cout << "The nodes that belong to community " << num_cols << ": ";
		for ( Eigen::SparseMatrix<int>::InnerIterator it( commMat, num_cols ); it; ++it){
			std::cout << it.index() << ", ";
			//it.index(); // inner index, here it is equal to it.row()
		}
		std::cout << std::endl;
	}

	return 1;
}

int main(){
	SmatI commMat;
	getCommunityInfo("comm1.dat", commMat);
	display(commMat);
		
	return 0;
}
