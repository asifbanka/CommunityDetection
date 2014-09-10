
CC=g++
CFLAGS=-I../../../libraries -lrt

my_program: graphReader.h graphReader.cpp matrixBuilder.cpp matrix_solver.cpp seedNode.h seedNode.cpp algorithm.cpp
	$(CC) -o $@ $^ $(CFLAGS)


.PHONY: clean
clean:
	rm -rf graphReader matrixBuilder matrix__solver seedNode


