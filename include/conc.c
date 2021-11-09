#include "conc.h"

u64 conc_lshift(u64 a, u8 shift){
	return a << shift;
}

u64 conc_rshift(u64 a, u8 shift){
	return a >> shift;
}

s64 conc_arshift(s64 a, u8 shift){
	return a >> shift;
}

u64 conc_add(u64 a, u64 b){
	return a + b;
}

u64 conc_sub(u64 a, u64 b){
	return a - b;
}

u64 conc_and(u64 a, u64 b){
	return a & b;
}

u64 conc_or(u64 a, u64 b){
	return a | b;
}

u64 conc_xor(u64 a, u64 b){
	return a ^ b;
}

u64 conc_mul(u64 a, u64 b){
	return a * b;
}

