#ifndef _RDTSC_UTIL_H
#define _RDTSC_UTIL_H

#include "types.h"

// http://www.intel.com/content/www/us/en/embedded/training/ia-32-ia-64-benchmark-code-execution-paper.html
static inline u64 RDTSC_START(void) {

  unsigned cycles_low, cycles_high;

  asm volatile("CPUID\n\t"
               "RDTSC\n\t"
               "mov %%edx, %0\n\t"
               "mov %%eax, %1\n\t"
               : "=r"(cycles_high), "=r"(cycles_low)::"%rax", "%rbx", "%rcx",
                 "%rdx");

  return ((u64)cycles_high << 32) | cycles_low;
}

static inline u64 RDTSCP(void) {
  unsigned cycles_low, cycles_high;

  asm volatile("RDTSCP\n\t"
               "mov %%edx, %0\n\t"
               "mov %%eax, %1\n\t"
               "CPUID\n\t"
               : "=r"(cycles_high), "=r"(cycles_low)::"%rax", "%rbx", "%rcx",
                 "%rdx");

  return ((u64)cycles_high << 32) | cycles_low;
}

#endif /* _RDTSC_UTIL_H */