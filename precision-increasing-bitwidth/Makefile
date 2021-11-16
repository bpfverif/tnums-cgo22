CC=g++
INCLUDE_DIR=../include
FILES=conc.c tnum.c
SOURCES=$(FILES:%.c=$(INCLUDE_DIR)/%.c)
CMD=$(CC) -g -O2 -w -I$(INCLUDE_DIR) $(SOURCES) precision_increasing_bitwidth.cpp 

precision_increasing_bitwidth:
	$(CMD) -o precision_increasing_bitwidth.out

clean:
	rm -f ./*.out

