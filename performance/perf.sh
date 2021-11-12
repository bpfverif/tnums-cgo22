#!/bin/bash

rm -f ./*.log
rm -f ./*.png
make clean
make all

CPU_ID=5
NUM_TRIALS=10
NUM_TNUM_PAIRS=40000

./perf_kern_mul.out ${NUM_TRIALS} ${CPU_ID} ${NUM_TNUM_PAIRS} > perf_kern_mul.log &&
./perf_bitwise_mul_opt.out ${NUM_TRIALS} ${CPU_ID} ${NUM_TNUM_PAIRS} > perf_bitwise_mul_opt.log  &&
./perf_our_mul.out ${NUM_TRIALS} ${CPU_ID} ${NUM_TNUM_PAIRS} > perf_our_mul.log &&

python3 graph_performance.py


