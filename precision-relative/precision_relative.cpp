#include <boost/multiprecision/cpp_int.hpp>
#include <cstdlib>
#include <cmath>
#include <cfenv>
#include <vector>
#include "conc.h"
#include "tnum.h" 

typedef struct tnum tnum_t;

int bitvec_width = 8; // default bitvec witdh
std::vector<tnum_t> all_tnums; // all possible n-bit tnums

namespace bmp = boost::multiprecision;

u64 other_mul_better = 0;
u64 our_mul_better = 0;

std::vector<tnum_t> generate_all_tnums(){

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

u64 get_number_of_concrete_values_in_tnum(tnum_t t) {
	int z =  0;
	for(auto i = 0; i< bitvec_width; i++) {
		if ((t.mask & 1ULL) == 1ULL) {
			z++;
		}
		t.mask = t.mask >> 1;
	}
	return static_cast<u64> (bmp::pow(bmp::cpp_int(2), z));
}

void calc_precision_diff_helper(tnum_t t1, tnum_t t2)
{
#ifdef KERN_MUL_V_OUR_MUL
	tnum_t abs_res_1 = kern_mul(t1, t2);
	tnum_t abs_res_2 = our_mul(t1, t2);
#elif BITWISE_MUL_V_OUR_MUL
	tnum_t abs_res_1 = bitwise_mul(t1, t2);
	tnum_t abs_res_2 = our_mul(t1, t2);
#else
	std::cerr << "Tnum operation not '-D' defined at compile time. Exiting." << std::endl;
	exit(0) ;
#endif

	abs_res_1.value = abs_res_1.value & ((1ULL << bitvec_width) - 1);
	abs_res_1.mask = abs_res_1.mask & ((1ULL << bitvec_width) - 1);
	
	abs_res_2.value = abs_res_2.value & ((1ULL << bitvec_width) - 1);
	abs_res_2.mask = abs_res_2.mask & ((1ULL << bitvec_width) - 1);

	bool diff = (abs_res_1.value != abs_res_2.value) && (abs_res_1.mask != abs_res_2.mask);

	if (diff) {
		u64 num_conc_in_abs_res_1 = get_number_of_concrete_values_in_tnum(abs_res_1);
		u64 num_conc_in_abs_res_2 = get_number_of_concrete_values_in_tnum(abs_res_2);

		if (num_conc_in_abs_res_1 > num_conc_in_abs_res_2)
			our_mul_better++;
		else
			other_mul_better++;

		double rel_precision = (double)num_conc_in_abs_res_1/(double)num_conc_in_abs_res_2;

		std::cout << std::setprecision(4) << rel_precision;
		std::cout << std::endl;
	}
}

void calc_precision_diff() {

	for(size_t i = 0; i< all_tnums.size(); i++){
		tnum_t t1 = all_tnums[i];
		for(size_t j = 0; j < all_tnums.size(); j++) {
			tnum_t t2 = all_tnums[j];
			calc_precision_diff_helper(t1, t2);

		}
	}
}

int main(int argc, char** argv)
{
	const char *usage = "Usage: \tthis_binary <bitvec_width>\n"\
	"\twhere bitvec_width: bit-vector width\n";

	if (argc < 2){
		fprintf(stderr, "Missing arguments\n");
		fprintf(stderr, "%s", usage);
		exit(-1);
	}

	bitvec_width = atoi(argv[1]);

	// generate all n bit tnum
	all_tnums = generate_all_tnums();

	calc_precision_diff();

	std::cout << "number of input tnum pairs where our_mul had better precision: " 
		<< our_mul_better << std::endl;
	std::cout << "number of input tnum pairs where other_mul had better precision: " 
	 	<< other_mul_better << std::endl;
	std::cout << "total number of input tnum pairs where output from our_mul != other_mul : " 
		<< our_mul_better + other_mul_better;

   return 0;
}

