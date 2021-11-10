#!/bin/bash

make --silent clean 
make --silent precision_increasing_bitwidth && 

printf -- "bitwidth, number of, output kern_mul, output kern_mul, kern_mul, our_mul\n"
printf -- " , tnum pairs, ==, !=, more precise , more precise\n"
printf -- " , , output our_mul, output_our_mul, , \n"
printf -- "--------, ----------, -----------------, -----------------, --------------, ---------------\n"
./precision_increasing_bitwidth.out 5  
./precision_increasing_bitwidth.out 6 
./precision_increasing_bitwidth.out 7 
./precision_increasing_bitwidth.out 8  
./precision_increasing_bitwidth.out 9

