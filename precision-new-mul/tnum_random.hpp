#ifndef _TNUM_RANDOM
#define _TNUM_RANDOM

#include "tnum.h"
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/random.hpp>
#include <iostream>

// https://www.boost.org/doc/libs/1_61_0/libs/multiprecision/doc/html/boost_multiprecision/tut/random.html
// 3**64 == (12491668968477870238 << 38 | 53577956609)

typedef struct tnum tnum_t;

tnum_t generate_random_tnum(int width);

#endif