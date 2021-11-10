CC=g++
CFLAGS=-I../include/ 
CMD=$(CC) -g -O2 -w $(CFLAGS) ../include/conc.c ../include/tnum.c precision_increasing_bitwidth.cpp 

precision_increasing_bitwidth:
	$(CMD) -o precision_increasing_bitwidth.out

clean:
	rm -f ./*.out

