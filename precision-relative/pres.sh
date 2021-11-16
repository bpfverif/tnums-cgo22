#!/bin/bash

rm -f ./*.log
make clean
make all

BITWIDTH=8

printf "\n---------------------\n"
printf "kern_mul v our_mul\n"
./pres_kern_mul_v_our_mul.out ${BITWIDTH} > pres_kern_mul_v_our_mul.log && 
tail -3 pres_kern_mul_v_our_mul.log && 
printf "\n---------------------\n"
printf "bitwise_mul v our_mul\n"
./pres_bitwise_mul_v_our_mul.out ${BITWIDTH} > pres_bitwise_mul_v_our_mul.log && 
tail -3 pres_bitwise_mul_v_our_mul.log && 
printf "\n---------------------\n"
printf "preparing graph ..."
python3 graph_precision_relative.py --bitwidth=${BITWIDTH} --baseop=our_mul --op1=kern_mul --infile1=pres_kern_mul_v_our_mul.log --op2=bitwise_mul --infile2=pres_bitwise_mul_v_our_mul.log --outfile=pres_fig.png
printf " done.\n\n"


