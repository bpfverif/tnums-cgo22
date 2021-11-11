#!/bin/bash

rm -f ./*.log
rm -f ./*.png
make clean
make all

NUM_TNUM_PAIRS=40000000

./perf_kern_mul.out 10 5 ${NUM_TNUM_PAIRS} > perf_kern_mul.log &&
./perf_bitwise_mul_opt.out 10 5 ${NUM_TNUM_PAIRS} > perf_bitwise_mul_opt.log  &&
./perf_our_mul.out 10 5 ${NUM_TNUM_PAIRS} > perf_our_mul.log &&

python3 graph_performance.py


