#!/bin/bash

rm -f ./*.log
make clean
make kern_mul_v_our_mul
make bitwise_mul_v_our_mul

printf "\n---------------------\n"
printf "kern_mul v our_mul\n"
./pres_kern_mul_v_our_mul.out 8 > pres_kern_mul_v_our_mul.log && 
tail -3 pres_kern_mul_v_our_mul.log && 
printf "\n---------------------\n"
printf "bitwise_mul v our_mul\n"
./pres_bitwise_mul_v_our_mul.out 8 > pres_bitwise_mul_v_our_mul.log && 
tail -3 pres_bitwise_mul_v_our_mul.log && 
printf "\n---------------------\n"
printf "preparing graph ..."
python3 graph_precision_relative.py --bitwidth=8 --infile1=pres_kern_mul_v_our_mul.log --infile2=pres_bitwise_mul_v_our_mul.log --outfile=pres_fig.png --op1=kern_mul --op2=bitwise_mul --op=our_mul 
printf " done.\n\n"


