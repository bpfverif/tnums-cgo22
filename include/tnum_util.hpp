#ifndef TNUM_UTIL_H
#define TNUM_UTIL_H

#include "tnum.h" 
#include <boost/multiprecision/cpp_int.hpp>

typedef struct tnum tnum_t;

namespace bmp = boost::multiprecision;

std::vector<tnum_t> generate_all_tnums(int bitvec_width){

	std::vector<tnum_t> all_tnums;
	for (u64 i =0 ; i<std::pow(2,bitvec_width); i++ ) {
		for (u64 j =0; j < std::pow(2, bitvec_width); j++) {
			if ((i & j) == 0) {
				tnum_t t = {.value = i, .mask = j};
				all_tnums.push_back(t);
			}
		}
	}	
	return all_tnums;
}

u64 get_number_of_concrete_values_in_tnum(tnum_t t, int bitvec_width) {
	int z =  0;
	for(auto i = 0; i< bitvec_width; i++) {
		if ((t.mask & 1ULL) == 1ULL) {
			z++;
		}
		t.mask = t.mask >> 1;
	}
	return static_cast<u64> (bmp::pow(bmp::cpp_int(2), z));
}

std::string tnum_to_string(tnum_t t, int bitvec_width) {
	char tnum_string[65];
	tnum_sbin(tnum_string, 65, t);
	return std::string(tnum_string).substr(64-bitvec_width) + std::string(" (") +\
		std::to_string(t.value) + std::string(":") + \
		std::to_string(t.mask) + std::string(")");
}

#endif /* TNUM_UTIL_H*/