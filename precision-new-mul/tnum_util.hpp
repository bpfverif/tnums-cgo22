#ifndef TNUM_UTIL_H
#define TNUM_UTIL_H

#include "tnum.h"
#include <boost/multiprecision/cpp_int.hpp>
#include <unordered_set>

typedef struct tnum tnum_t;

std::vector<tnum_t> generate_all_tnums(int bitvec_width);

u64 get_number_of_concrete_values_in_tnum(tnum_t t, int bitvec_width);

std::unordered_set<u64> get_concrete_values_contained_in_tnum(tnum_t t,
                                                              int bitvec_width);

bool is_subset_of(const std::unordered_set<u64> &a,
                  const std::unordered_set<u64> &b);

bool tnums_comparable(tnum_t t1, tnum_t t2, int bitvec_width);

std::string tnum_to_string(tnum_t t, int bitvec_width);

#endif /* TNUM_UTIL_H*/