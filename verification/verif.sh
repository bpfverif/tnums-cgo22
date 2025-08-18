#!/bin/bash 

# Script to run verification of tnum operations. By default all tnum operations 
# (except multiplication) are verified for input tnums of bitwidth 64. 
# Verification for tnum multiplication (kern_mul and our_mul) is done for input 
# tnums of witdh 8, so that the solver can finish in a reasonable time.

python3 tnum.py --bitwidth=64 --op=tnum_add ;
python3 tnum.py --bitwidth=64 --op=tnum_sub ;
python3 tnum.py --bitwidth=64 --op=tnum_and ;
python3 tnum.py --bitwidth=64 --op=tnum_or ;
python3 tnum.py --bitwidth=64 --op=tnum_xor ;
python3 tnum.py --bitwidth=64 --op=tnum_lshift ; 
python3 tnum.py --bitwidth=64 --op=tnum_rshift ;
python3 tnum.py --bitwidth=64 --op=tnum_arshift ;
python3 tnum.py --bitwidth=8 --op=tnum_kern_mul ;
python3 tnum.py --bitwidth=8 --op=tnum_our_mul ;
python3 tnum.py --bitwidth=64 --op=tnum_intersect ;
python3 tnum.py --bitwidth=64 --op=tnum_union ;
