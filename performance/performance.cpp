#include <cmath>
#include <vector>
#include <sched.h>
#include <iostream>
#include <algorithm>
#include <numeric>
#include "tnum.h" 
#include "tnum_random.hpp"

#define CPUFREQ_MHZ (2200.0)
static const float one_cycle_ns = ((float)1000 / CPUFREQ_MHZ);

int bitvec_width = 64;
size_t num_trials = 10;
int cpu_id = 15;
int num_tnum_pairs = 40000000; // default to 4 million

// http://www.intel.com/content/www/us/en/embedded/training/ia-32-ia-64-benchmark-code-execution-paper.html
static inline
uint64_t RDTSC_START ( void )
{

	unsigned cycles_low, cycles_high;

	asm volatile ( "CPUID\n\t"
				   "RDTSC\n\t"
				   "mov %%edx, %0\n\t"
				   "mov %%eax, %1\n\t"
				   : "=r" (cycles_high), "=r" (cycles_low)::
				   "%rax", "%rbx", "%rcx", "%rdx");

	return ((uint64_t) cycles_high << 32) | cycles_low;
}

static inline
uint64_t RDTSCP ( void )
{
	unsigned cycles_low, cycles_high;

	asm volatile( "RDTSCP\n\t"
				  "mov %%edx, %0\n\t"
				  "mov %%eax, %1\n\t"
				  "CPUID\n\t": "=r" (cycles_high), "=r" (cycles_low)::
				  "%rax", "%rbx", "%rcx", "%rdx");
	
	return ((uint64_t) cycles_high << 32) | cycles_low;
}

void calc_cycles() {
	tnum_t tnum_res;
	u64 start, end, total_cycles;

    tnum_t t1 = generate_random_tnum(bitvec_width);
    tnum_t t2 = generate_random_tnum(bitvec_width);

    std::vector<u64> cycles_ij;

    for (size_t k = 0; k < num_trials; k++){
        start = RDTSC_START();

// perform the operation
#ifdef KERN_MUL
	   tnum_res = kern_mul(t1, t2);
#elif BITWISE_MUL_OPT
	   tnum_res = bitwise_mul_opt(t1, t2);
#elif OUR_MUL
	   tnum_res = our_mul(t1, t2);
#else
       std::cerr << "Tnum operation not '-D' defined at compile time. Exiting." << std::endl;
       exit(0) ;
#endif
        end = RDTSCP();
        total_cycles = end - start;
        cycles_ij.push_back(total_cycles);
    }
    
    // get mininum of all trials
    std::sort(cycles_ij.begin(), cycles_ij.end());
	std::cout << cycles_ij.front() << std::endl;
}

void start(){
	// pin thread to cpuid
	cpu_set_t cpuset;
	CPU_ZERO(&cpuset);
	CPU_SET(cpu_id, &cpuset);
	sched_setaffinity(0, sizeof(cpu_set_t), &cpuset);

    while(num_tnum_pairs--){
        calc_cycles();
    }
}

int main(int argc, char** argv)
{
	const char *usage = "Usage: \tthis_binary"\
	"<num_trials> <cpu_id> <num_random_tnum_pairs>\n";

	if (argc < 4){
		fprintf(stderr, "Missing arguments\n");
		fprintf(stderr, "%s", usage);
		exit(-1);
	}

	num_trials = atoi(argv[1]);
	cpu_id = atoi(argv[2]);
	num_tnum_pairs = atoi(argv[3]);
	start();

   return 0;
}


