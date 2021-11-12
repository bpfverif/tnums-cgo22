CC=g++
CFLAGS=-I../include/ 
CMD=$(CC) -g -O2 -w $(CFLAGS) ../include/conc.c ../include/tnum.c performance.cpp tnum_random.cpp

all: kern_mul bitwise_mul_opt our_mul
	
kern_mul:
	$(CMD) -o perf_kern_mul.out -DKERN_MUL

bitwise_mul_opt:
	$(CMD) -o perf_bitwise_mul_opt.out -DBITWISE_MUL_OPT

our_mul:
	$(CMD) -o perf_our_mul.out -DOUR_MUL

clean:
	rm -f ./*.out