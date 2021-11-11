#!/bin/bash 

# Script to run verification of tnum operations. By default all tnum operations 
# (except multiplication) are verified for input tnums of bitwidth 64. 
# Verification for tnum multiplication (kern_mul and our_mul) is done for input 
# tnums of witdh 8, so that the solver can finish in a reasonable time.

python3 tnum.py --bitwidth=64 --op=add ;
python3 tnum.py --bitwidth=64 --op=sub ;
python3 tnum.py --bitwidth=64 --op=and ;
python3 tnum.py --bitwidth=64 --op=or ;
python3 tnum.py --bitwidth=64 --op=xor ;
python3 tnum.py --bitwidth=64 --op=lshift ; 
python3 tnum.py --bitwidth=64 --op=rshift ;
python3 tnum.py --bitwidth=64 --op=arshift ;
python3 tnum.py --bitwidth=8 --op=mul ;
python3 tnum.py --bitwidth=8 --op=our_mul ;
