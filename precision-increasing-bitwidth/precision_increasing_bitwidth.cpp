#include "conc.h"
#include "tnum.h"
#include "tnum_util.hpp" 
#include <boost/multiprecision/cpp_int.hpp>
#include <cfenv>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <vector>

typedef struct tnum tnum_t;

int bitvec_width = 8; // default bitvec witdh
std::vector<tnum_t> all_tnums; // all possible n-bit tnums
u64 num_output_equal = 0;
u64 num_output_unequal = 0;
u64 num_kern_mul_better = 0;
u64 num_our_mul_better = 0;

void calc_precision_helper(tnum_t t1, tnum_t t2) {
  tnum_t abs_res_1 = kern_mul(t1, t2);
  tnum_t abs_res_2 = our_mul(t1, t2);

  abs_res_1.value = abs_res_1.value & ((1ULL << bitvec_width) - 1);
  abs_res_1.mask = abs_res_1.mask & ((1ULL << bitvec_width) - 1);

  abs_res_2.value = abs_res_2.value & ((1ULL << bitvec_width) - 1);
  abs_res_2.mask = abs_res_2.mask & ((1ULL << bitvec_width) - 1);

  bool diff = (abs_res_1.value != abs_res_2.value) &&
              (abs_res_1.mask != abs_res_2.mask);

  if (diff) {
    num_output_unequal += 1;
    u64 num_conc_in_abs_res_1 =
        get_number_of_concrete_values_in_tnum(abs_res_1, bitvec_width);
    u64 num_conc_in_abs_res_2 =
        get_number_of_concrete_values_in_tnum(abs_res_2, bitvec_width);

    if (num_conc_in_abs_res_1 > num_conc_in_abs_res_2) {
      num_our_mul_better += 1;
    } else {
      num_kern_mul_better += 1;
    }

  } else {
    num_output_equal += 1;
  }
}

void calc_precision() {

  for (size_t i = 0; i < all_tnums.size(); i++) {
    tnum_t t1 = all_tnums[i];
    for (size_t j = 0; j < all_tnums.size(); j++) {
      tnum_t t2 = all_tnums[j];
      calc_precision_helper(t1, t2);
    }
  }
}

int main(int argc, char **argv) {
  const char *usage = "Usage: \tthis_binary <bitvec_width>\n"
                      "\twhere bitvec_width: bit-vector width\n";

  if (argc < 2) {
    fprintf(stderr, "Missing arguments\n");
    fprintf(stderr, "%s", usage);
    exit(-1);
  }

  bitvec_width = atoi(argv[1]);

  // generate all n bit tnums
  all_tnums = generate_all_tnums(bitvec_width);
  calc_precision();

  double num_tnum_pairs = std::pow(all_tnums.size(), 2);
  double perc_equal = (double)num_output_equal * 100.0 / (double)num_tnum_pairs;
  double perc_unequal =
      (double)num_output_unequal * 100.0 / (double)num_tnum_pairs;
  double perc_kern_mul_better =
      (double)num_kern_mul_better * 100 / (double)num_output_unequal;
  double perc_our_mul_better =
      (double)num_our_mul_better * 100 / (double)num_output_unequal;

  std::cout << std::fixed;
  std::cout << std::setprecision(0);
  std::cout << bitvec_width << ", ";
  std::cout << num_tnum_pairs << ", ";
  std::cout << num_output_equal;
  std::cout << std::setprecision(3);
  std::cout << " (" << perc_equal << "%), ";
  std::cout << num_output_unequal;
  std::cout << " (" << perc_unequal << "%), ";
  std::cout << num_kern_mul_better;
  std::cout << " (" << perc_kern_mul_better << "%), ";
  std::cout << num_our_mul_better;
  std::cout << " (" << perc_our_mul_better << "%)";
  std::cout << std::endl;

  return 0;
}
