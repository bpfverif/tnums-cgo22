CC=g++
SOURCES=conc.c tnum.c tnum_util.cpp tnum_random.cpp
CMD=$(CC) -g -O2 -w -I$(INCLUDE_DIR) $(SOURCES) precision.cpp 

all: our_mul_v_new_mul

our_mul_v_new_mul:
	$(CMD) -o precision

clean:
	rm -f ./*.out

