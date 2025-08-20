#include "tnum.h"
#include "tnum_random.hpp"
#include "tnum_util.hpp"
#include <boost/multiprecision/cpp_int.hpp>
#include <cfenv>
#include <cmath>
#include <cstdlib>
#include <vector>

typedef struct tnum tnum_t;

u64 new_mul_better = 0;
u64 our_mul_better = 0;
u64 both_mul_same = 0;
u64 incomparable = 0;

void calc_precision_diff(tnum_t t1, tnum_t t2, int bitvec_width) {
  tnum_t our_mul_res = our_mul(t1, t2);
  tnum_t new_mul_res = new_mul(t1, t2);

  assert((our_mul_res.value & our_mul_res.mask) == 0);
  assert((new_mul_res.value & new_mul_res.mask) == 0);

  bool diff = (our_mul_res.value != new_mul_res.value) ||
              (our_mul_res.mask != new_mul_res.mask);

  if (diff) {
    if (tnum_in(our_mul_res, new_mul_res)) {
      new_mul_better++;
    } else if (tnum_in(new_mul_res, our_mul_res)) {
      our_mul_better++;
    } else {
      incomparable++;
    }
  } else {
    both_mul_same++;
  }
}

void calc_precision_diff_exhaustive(const int bitvec_width) {

  std::vector<tnum_t> all_tnums = generate_all_tnums(bitvec_width);
  for (size_t i = 0; i < all_tnums.size(); i++) {
    tnum_t t1 = all_tnums[i];
    for (size_t j = 0; j < all_tnums.size(); j++) {
      tnum_t t2 = all_tnums[j];
      calc_precision_diff(t1, t2, bitvec_width);
    }
  }
}

void calc_precision_diff_sampled(const int bitvec_width, int num_samples) {

  for (int i = 0; i < num_samples; i++) {
    struct tnum t1 = generate_random_tnum(bitvec_width);
    struct tnum t2 = generate_random_tnum(bitvec_width);
    calc_precision_diff(t1, t2, bitvec_width);
  }
}

void reset() {
  new_mul_better = 0;
  our_mul_better = 0;
  both_mul_same = 0;
  incomparable = 0;
}

int main(int argc, char **argv) {
  const char *usage = "Usage: \tthis_binary <bitvec_width_exhaustive> "
                      "<bitvec_width_sampled> <num_samples>\n";

  if (argc < 4) {
    fprintf(stderr, "Missing arguments\n");
    fprintf(stderr, "%s", usage);
    exit(-1);
  }

  int bitvec_width_exhaustive = atoi(argv[1]);
  int bitvec_width_sampled = atoi(argv[2]);
  int num_samples = atoi(argv[3]);

  reset();
  calc_precision_diff_exhaustive(bitvec_width_exhaustive);

  std::cout << "exhaustive at bitwidth " << bitvec_width_exhaustive
            << std::endl;
  std::cout << "number of input tnum pairs where our_mul had better precision: "
            << our_mul_better << std::endl;
  std::cout << "number of input tnum pairs where new_mul had better precision: "
            << new_mul_better << std::endl;
  std::cout << "number of input tnum pairs where output was the same: "
            << both_mul_same << std::endl;
  std::cout << "number of input tnum pairs where output was incomparable: "
            << incomparable << std::endl;
  std::cout << std::endl;

  reset();
  calc_precision_diff_sampled(bitvec_width_sampled, num_samples);

  std::cout << "sampled at bitwidth " << bitvec_width_sampled << std::endl;
  std::cout << "number of input tnum pairs where our_mul had better precision: "
            << our_mul_better << std::endl;
  std::cout << "number of input tnum pairs where new_mul had better precision: "
            << new_mul_better << std::endl;
  std::cout << "number of input tnum pairs where output was the same: "
            << both_mul_same << std::endl;
  std::cout << "number of input tnum pairs where output was incomparable: "
            << incomparable << std::endl;

  return 0;
}
