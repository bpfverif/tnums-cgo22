CC=g++
INCLUDE_DIR=../include
FILES=conc.c tnum.c
SOURCES=$(FILES:%.c=$(INCLUDE_DIR)/%.c)
CMD=$(CC) -g -O2 -w -I$(INCLUDE_DIR) $(SOURCES) performance.cpp tnum_random.cpp

all: kern_mul bitwise_mul_opt our_mul
	
kern_mul:
	$(CMD) -o perf_kern_mul.out -DKERN_MUL

bitwise_mul_opt:
	$(CMD) -o perf_bitwise_mul_opt.out -DBITWISE_MUL_OPT

our_mul:
	$(CMD) -o perf_our_mul.out -DOUR_MUL

clean:
	rm -f ./*.out