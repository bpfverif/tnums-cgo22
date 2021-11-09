#include "tnum_random.hpp"

namespace bmp = boost::multiprecision;
namespace brand = boost::random;

// https://www.boost.org/doc/libs/1_61_0/libs/multiprecision/doc/html/boost_multiprecision/tut/random.html
// https://www.boost.org/doc/libs/1_62_0/libs/multiprecision/doc/html/boost_multiprecision/tut/ints/cpp_int.html
brand::mt19937 mt;
brand::uniform_int_distribution<bmp::cpp_int> ui(0, bmp::pow(bmp::cpp_int(3), 64));

std::string to_base_3(bmp::cpp_int n){
   char digits[] = {'0', '1', '2'};
   std::string s;
   do {
      bmp::cpp_int r = n % bmp::cpp_int(3);
      int idx = static_cast<int>(r); 
      s = s + digits[idx];
      n = n / bmp::cpp_int(3);
    } while(n > 0);

    reverse(s.begin(), s.end());
    s.insert(s.begin(), 64 - s.size(), '0');
    return s;
}

tnum_t to_tnum(std::string base3) {
   u64 value = 0;
   u64 mask = 0;
   for (int i = 0; i<64; i++) {
      char c = base3[i];
      if (c == '0') {
         value = value << 1;
         mask = mask << 1;
      } else if (c == '1') {
         value = (value << 1) + 1;
         mask = mask << 1;
      } else if (c == '2') {
         value = value << 1;
         mask = (mask << 1) + 1;
      }
   }
   assert((value & mask) == 0);
   tnum_t t = {.value = value, .mask = mask};
   return t;
}

tnum_t generate_random_tnum(int width) {
   tnum_t t = to_tnum(to_base_3(ui(mt)));
   if (width == 64){
    return t;    
  } else {
   t.value = t.value & ((1ULL << width) - 1);
   t.mask = t.mask & ((1ULL << width) - 1);
   return t;    
  }

}


