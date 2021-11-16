CC=g++
INCLUDE_DIR=../include
FILES=conc.c tnum.c
SOURCES=$(FILES:%.c=$(INCLUDE_DIR)/%.c)
CMD=$(CC) -g -O2 -w -I$(INCLUDE_DIR) $(SOURCES) precision_relative.cpp 

all: kern_mul_v_our_mul bitwise_mul_v_our_mul

kern_mul_v_our_mul:
	$(CMD) -o pres_kern_mul_v_our_mul.out -DKERN_MUL_V_OUR_MUL

bitwise_mul_v_our_mul:
	$(CMD) -o pres_bitwise_mul_v_our_mul.out -DBITWISE_MUL_V_OUR_MUL

clean:
	rm -f ./*.out

