CC=g++
CFLAGS=-I../include/ 
CMD=$(CC) -g -O2 -w $(CFLAGS) ../include/conc.c ../include/tnum.c precision_relative.cpp 

kern_mul_v_our_mul:
	$(CMD) -o pres_kern_mul_v_our_mul.out -DKERN_MUL_V_OUR_MUL

bitwise_mul_v_our_mul:
	$(CMD) -o pres_bitwise_mul_v_our_mul.out -DBITWISE_MUL_V_OUR_MUL

clean:
	rm -f ./*.out

