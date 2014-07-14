#include "communityClassifier.h"

void CommunityClassifier::read(const char* file_name){
	std::ifstream aff_data(file_name);
	if ( !aff_data().is_open() ){
		std::cout << "Cannot open affinity file" << std::endl;
		return;
	}

	// first read numV and numC
	aff_data >> numV >> numC;

	// allocate space for a matrix with dimensions numV * numC
	nodeAff.resize(numV, numC);

	for (int i = 0; i != numV; ++i){
		int vert_id;
		aff_data >> vert_id;
		for (int k = 0; k != numC; ++k){
			double aff;
			aff_data >> aff;
			nodeAff(vert_id, k) = aff; 
		}
			
	}

	return;
}
