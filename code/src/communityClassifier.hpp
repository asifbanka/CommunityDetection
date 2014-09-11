#ifndef GUARD_communityClassifier_h
#define GUARD_communityClassifier_h
#include <iostream>
#include <vector>
#include <list>
#include <fstream>
#include <Eigen/Core>

class CommunityClassifier{
	private:
		Eigen::MatrixXd nodeAff;
		Eigen::MatrixXd groundTruth;
		int numV;
		int numC;
	
	public:
		CommunityClassifier() : numV(0), numC(0) {}
		CommunityClassifier(const char* file_name) { read(file_name); }

		void read(const char* file_name);
		void classify_simple();
			
};

#endif
