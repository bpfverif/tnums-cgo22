# Artifact for submission "Sound, Precise, and Fast Abstract Interpretation with Tristate Numbers"

## Abstract of the paper.

Extended Berkeley Packet Filter (BPF) is a language and run-time system that
allows non-superusers to extend the Linux and Windows operating systems by
downloading user code into the kernel. To ensure that user code is safe to run
in kernel context, BPF relies on a static analyzer that proves properties about
the code, such as bounded memory access and the absence of operations that might
crash. The BPF static analyzer checks safety using abstract interpretation with
several abstract domains. Among these, the domain of tnums (tristate numbers) is
a key domain used to reason about uncertainty in values at the bit level. This
paper formally specifies the tnum abstract domain and its arithmetic operators.
We provide the first proofs of soundness and optimality of the abstract
arithmetic operators for tnum addition and subtraction used in the BPF analyzer.
Further, we describe a novel sound algorithm for multiplication of tnums that is
more precise and efficient (runs 33% faster on average) than the Linux kernel's
algorithm. Our tnum multiplication is now merged in the Linux kernel.

--------------------------------------------------------------------------------


### Performance of `kern_mul` vs `bitwise_mul` vs `our_mul`  (_Fig 5. in the paper submission_)
In this experiment we prepare a graph depicting the difference in performance
(cycles) between our multiplication algorithm `our_mul`, the Linux kernel's
multiplication algorithm `kern_mul`, and the multiplication algorithm by Regehr
et al., `bitwise_mul`. We randomly sample 4 million 64-bit tnum pairs, and
provide them as input to these algorithms. The experiment should take roughly 10
minutes.


#### Run script to compile code and produce graph for multiplication algorithms comparison
```
cd ../performance

./perf.sh
```

#### Extract graph from docker
1. Open a new terminal to find docker image ID
```
$ docker ps -a

CONTAINER ID   IMAGE             COMMAND     CREATED        STATUS         PORTS    NAMES
30e20b7c68d7   cgo_artifact   "/bin/bash" 4 hours ago    Up 20 minutes           elegant_tu
```
2. Copy cgo_artifact `CONTAINER ID` to clipboard (your ID may be different).

3. Copy the .png file to your local machine
```
docker cp <insert CONTAINER_ID here>:/home/cgo-artifact/performance/perf.png <insert destination directory>
```
4. Open the png in your preferred image viewer. 

#### Explanation
The graph depicts a cumulative distribution of the number of CPU cycles taken by
`our_mul`, `kern_mul`, and `bitwise_mul` for all the 4M randomly sampled tnum
pairs. For the paper submission we did this for 40M randomly sample tnum pairs.
For each tnum pair we perform 10 trials, to eliminate noise, and chose the
_minimum_. The results should indicate that `our_mul` is faster on average than
`kern_mul` and `bitwise_mul`.

#### Source code structure
`performance.cpp` contains the source for the performance calculations. Here, we
use preprocessor macros for performing the specific tnum operation `kern_mul`,
`our_mul`, or `bitwise_mul` and avoid if-branches. For measuring performance, we
check the `RDTSC` time stamp counter register. We also provide an option for
pinning the thread to a cpu, to avoid cache-related issues. The other relevant
file here is `tnum_random.cpp`. This contains the source for generating the
random 64-bit tnums we use in the experiment. The function
`generate_random_tnum` uses a randomly distributed value from 0 to 3^64 to
produce a 64 bit tnum. 
 
TODO>>>>Note that the 2nd command line argument is for cpu-id, to pin the thread
to a particular cpu. In the following exmaple, the thread is pinned to a cpu-id
5. Please change this flag according to your cpu architecture, if necessary.

```
./performance_mul.o 10 5 > perf_mul.log && ./performance_our_mul.o 10 5 > perf_our_mul.log
```

```
python3 graph_performance.py
```

--------------------------------------------------------------------------------
_Fin._