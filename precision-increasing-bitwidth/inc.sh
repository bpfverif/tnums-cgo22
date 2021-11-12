#!/bin/bash

rm -rf *.log
make --silent clean 
make --silent precision_increasing_bitwidth && 

./precision_increasing_bitwidth.out 5 > pres_bw_5.log 
./precision_increasing_bitwidth.out 6 > pres_bw_6.log 
./precision_increasing_bitwidth.out 7 > pres_bw_7.log 
./precision_increasing_bitwidth.out 8 > pres_bw_8.log 
./precision_increasing_bitwidth.out 9 > pres_bw_9.log 

cat header.txt pres_bw_5.log pres_bw_6.log pres_bw_7.log pres_bw_8.log pres_bw_9.log | column -ts,
 

