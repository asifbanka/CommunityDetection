
CC=g++
<<<<<<< HEAD
CFLAGS=-I../../../libraries -lrt
=======
CFLAGS=-I../../libraries/Eigen -lrt
>>>>>>> ab35a581890a3e116e123ebdab8abc902ec550aa


my_program: graphReader.h graphReader.cpp matrixBuilder.cpp matrix_solver.cpp seedNode.h seedNode.cpp
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean
clean:
	rm -rf graphReader matrixBuilder matrix__solver seedNode


