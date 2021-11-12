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

## Claims to validate/reproduce.

In this artifact, we provide instructions to reproduce and validate the
following claims in the paper.

1. Verification of tnum operations using the Z3 SMT solver

2. Precision improvements in our tnum multiplication algorithm compared 
   to the Linux kernel's tnum multiplication.

3. Performance improvements in our tnum multiplication algorithm compared to
   Linux kernel's tnum multiplication.

4. Precision of tnum multiplication compared to the Linux kernel's tnum 
   multiplication as a function of increasing bitwidth of input tnums. 
 
`Note`. To make it feasible to run the artifact quickly, we have reduced the
sample sizes used for the performance experiment. The experiments for the paper
were performed without using any containers, and on larger inputs sizes. Hence,
there will be small differences in the results but the overall trends will be
similar. We also make a note in the explantion section of each experiment, of
any other differences when compared to the paper. It should take roughly 30
minutes to evaluate this artifact.

--------------------------------------------------------------------------------

## Instructions to run the artifact.

### Downloading prebuilt Docker Image

1. Install docker if it is not installed already by following the
documentation [here](https://docs.docker.com/install/). You might need to follow the post installation steps 
for managing docker as a non-root user [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

2.  Run the docker image:
```
docker load < cgo22_artifact.tar.gz
docker run -it cgo22_artifact
cd cgo22-artifact
```

### Known issues. 
We have tested the docker image on different architectures (`x86_64`, `amd64`)
and have no known issues to report.

--------------------------------------------------------------------------------

## Automated Verfication with Z3
In this experiment, we verify the correctness of all tnum operations. For all
operations except the multiplication operations, `mul` and `our_mul`, we perform
automated verification with bitvectors (i.e. input tnums) of width `64` . For
multiplication, since the automated verification takes a long time to complete,
we perform automated verification with `8` bits. This experiment should take
roughly 5 minutes.


### Run
```
cd verification
bash verif.sh
```

### Expected Result 

```
Verifying correctness of [tnum_add] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_sub] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_and] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_or] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_xor] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_lshift] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_rshift] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_arshift] for tnums of width [64] ...  SUCCESS.

Verifying correctness of [tnum_kern_mul] for tnums of width [8] ...  SUCCESS.

Verifying correctness of [tnum_our_mul] for tnums of width [8] ...  SUCCESS.
```

### Explanation
The automated verification is done using
[z3py](https://ericpony.github.io/z3py-tutorial/guide-examples.htm). Note that
the actual python script containing the encoding of tnum operations is in
`tnum.py`. 

The linux kernel uses 64-bit numbers for tnum operations. The output of this
experiment, should show that we successfully verify the correctness of
`tnum_lshift`, `tnum_rshift`, `tnum_arshift`, `tnum_and`, `tnum_or`, `tnum_xor`,
`tnum_add`, and `tnum_sub` with bitvectors of width 64. For the multiplication
operations `kern_mul`, and `our_mul`, here, we verify correctness with
bitvectors of width 8, since the verification for 64-bits cannot be completed in
a reasonable amount of time. As mentioned in the paper, we have verified the
correctness of multiplication for bitvectors of width 14, which took around 1
day. 

### Source code structure
The only source file related to this experiment is `tnum.py`, which
accepts switches for `--bitwidth`, the bitvector width and `--op` for
the tnum operation that we perform the verification for. The `Tnum`
class contains the `z3` encoding of tnum operations from the Linux
kernel. For instance `Tnum.tnum_add` returns a formula containing the
z3 encoding of the `tnum_add` from the Linux kernel. The
`TnumOpsVerifier` class contains methods which encode the
verification condition for the similarly named tnum operations, and verify 
them using z3 (by checking if the solver returns `unsat`).

--------------------------------------------------------------------------------

## Relative precision of `our_mul` compared to `kern_mul` and `bitwise_mul` (_Fig 4. in the paper submission_)
In this experiment, we compare the relative precision of our new tnum
multiplication algorithm `our_mul` with the Linux kernel's algorithm `kern_mul`
and the algorithm by Regehr and Duongsaa which we call `bitwise_mul`. We
generate two binaries for each comparison: (i) `kern_mul` vs. `our_mul` and
(ii). `bitwise_mul` vs `our_mul`. The generated binaries after compilation
accept a switch for bitwidth as their only command line argument. To finish this
experiment in a reasonable amount of time, we propose using a bitwidth of `8`.
To run this evaluation, you can run the bash script `pres.sh` (which uses a
bitwidth of `8`). This experiment should take roughly 5 minutes.

### 1. Run the bash script
```
cd ../precision-relative
bash pres.sh
```

### 2. Extract figure from docker
1. Open a new terminal to find docker image ID
```
$ docker ps -a

CONTAINER ID   IMAGE             COMMAND     CREATED        STATUS         PORTS    NAMES
30e20b7c68d7   cgo22_artifact   "/bin/bash" 4 hours ago    Up 20 minutes           elegant_tu
```
2. Copy cgo22_artifact `CONTAINER ID` to clipboard (your ID may be different).

3. Copy the .png file to your local machine
```
docker cp <insert CONTAINER_ID here>:/home/cgo22-artifact/precision-relative/pres_fig.png <insert destination directory>
```
4. Open the png in your favourite image viewer. 

### Explanation
The graph depicts the cumulative distribution of the ratio of set sizes of the
tnums (after concretization) produced by (a) `kern_mul` to `our_mul` (dotted
black line) and (b) `bitwise_mul to our_mul` (solid grey line). The graph thus
generated should be exactly the same as the one in the paper, where we also use
a bitwidth of `8`. For (a), we ignore the cases where `kern_mul` and `our_mul`
produce the same exact output tnum: for those particular input tnum pairs,
`kern_mul` and `our_mul` are equally precise. Similarly, for (b) we ignore the
cases where `bitwise_mul` and `our_mul` produce the exact same output tnum.
Since we use a log2 scale for the x-axis: each tick on the x-axis to the right
of 0 is a point where `our_mul` produces a tnum that is more precise in exactly
one trit position when compared to the other multiplication algorithm. The
figure should show that for 80% of the cases, `our_mul` produces a more precise
tnum than both `kern_mul` and `bitwise_mul` (the data to the right of 0). This
indicates that our new multiplication algorithm is more precise than both the
Linux kernel's implementation and the algorithm by Regehr and Duongsaa.

### Source code structure
The main source file for this evaluation is `precision_relative.cpp` and all the
files in the `include` directory. The `include` directory contains `tnum.c`
which contains the source code of the tnum algorithms pulled from the Linux
kernel. This file contains the code for `our_mul` and `bitwise_mul` algorithms,
along with `kern_mul`.  Coming to `precision_relative.cpp`, the function
`calc_precision_diff_helper` takes as input two tnums `t1` and `t2` and performs
tnum multiplication on them using two algorithms. Which two algorithms to use is
defined at compile time using a `-D` flag: `KERN_MUL_V_OUR_MUL` would use
`kern_mul` as the first multiplication algorithm and `our_mul` as the second.
Finally, the necessary calculations related to computing precision are
performed. If using a bitwidth of 8, we zero out the top 56 bits from the output
tnum's value and mask, to effectively produce an 8-bit tnum. The function
`generate_all_tnums` generates all possible tnums of a particular bitwidth. 

To compare `kern_mul` to `our_mul`:

```
$ g++ -g -O2 -w -I../include/  ../include/conc.c ../include/tnum.c precision_relative.cpp  -o pres_kern_mul_v_our_mul.out -DKERN_MUL_V_OUR_MUL
$ ./pres_kern_mul_v_our_mul.out 8 > pres_kern_mul_v_our_mul.log
```
To compare `bitwise_mul` to `our_mul`:

```
$ g++ -g -O2 -w -I../include/  ../include/conc.c ../include/tnum.c precision_relative.cpp  -o pres_bitwise_mul_v_our_mul.out -DBITWISE_MUL_V_OUR_MUL
$ ./pres_bitwise_mul_v_our_mul.out 8 > pres_bitwise_mul_v_our_mul.log && 
```

For the comparison of `kern_mul` and `our_mul` every line in the output file
`pres_kern_mul_v_our_mul.log` corresponds to a unique input tnum pair, and is
the ratio of the set size of the output tnum produced by `kern_mul` to that of
the set size of the output tnum produced by `our_mul`. 

To produce the figure:
```
python3 graph_precision_relative.py --bitwidth=8 --infile1=pres_kern_mul_v_our_mul.log --infile2=pres_bitwise_mul_v_our_mul.log --outfile=pres_fig.png --op1=kern_mul --op2=bitwise_mul --op=our_mul
```
The command line switches to the python file `graph_precision_relative.py`
should be self-explanatory. 

--------------------------------------------------------------------------------


### Performance of `mul` vs `our_mul` (_Fig 6. in the paper submission_)
In this experiment we prepare a graph depicting the difference in performance
(cycles) between our multiplication algorithm `our_mul` and the Linux kernel's
multiplication algorithm `mul`. We randomly sample 4 million 64-bit tnum pairs,
and provide them as input to these algorithms. The experiment should take
roughly 15 minutes.


#### Compile code for `mul` and `our_mul`
```
cd ../performance

g++ -g -O2 -w -I../include/ ../include/conc.c ../include/tnum.c performance.cpp tnum_random.cpp -o performance_mul.o -DTNUM_OP_MUL && g++ -g -O2 -w -I../include/ ../include/conc.c ../include/tnum.c performance.cpp tnum_random.cpp -o performance_our_mul.o -DTNUM_OP_OUR_MUL
```

#### Run 
Note that the 2nd command line argument is for cpu-id, to pin the thread to a particular cpu.
In the following exmaple, the thread is pinned to a cpu-id 5. 
Please change this flag according to your cpu architecture, if necessary.
```
./performance_mul.o 10 5 > perf_mul.log && ./performance_our_mul.o 10 5 > perf_our_mul.log
```

#### Produce graph
```
python3 graph_performance.py
```

#### Extract graph from docker
1. Open a new terminal to find docker image ID
```
$ docker ps -a

CONTAINER ID   IMAGE             COMMAND     CREATED        STATUS         PORTS    NAMES
30e20b7c68d7   cgo22_artifact1   "/bin/bash" 4 hours ago    Up 20 minutes           elegant_tu
```
2. Copy cgo22_artifact `CONTAINER ID` to clipboard (your ID may be different).

3. Copy the .png file to your local machine
```
docker cp <insert CONTAINER_ID here>:/home/cgo22-artifact/performance/perf.png <insert destination directory>
```
4. Open the png in your favourite image viewer. 

#### Explanation
The graph depicts a cumulative distribution of the number of CPU cycles taken by
`mul` and `our_mul` for all the 4M randomly sampled tnum pairs. For the paper 
submission we did this for 400M randomly sample tnum pairs. For each tnum
pair we perform 10 trials, to eliminate noise, and chose the _minimum_. 
The results should indicate that `our_mul` is faster on average than `mul`.

#### Source code structure
`performance.cpp` contains the source for the performance
calculations. Here, we use preprocessor macros for performing the
specific tnum operation `mul` or `our_mul` and avoid if-branches. For
measuring performance, we check the `RDTSC` time stamp counter
register. We also provide an option for pinning the thread to a cpu,
to avoid cache-related issues. The other relevant file here is
`tnum_random.cpp`. This contains the source for generating the random
64-bit tnums we use in the experiment. The function
`generate_random_tnum` uses a randomly distributed value from 0 to
3^64 to produce a 64 bit tnum. 

--------------------------------------------------------------------------------
_Fin._

[1] J. Regehr and U. Duongsaa, “Deriving abstract transfer functions for
analyzing embedded software,” ACM SIGPLAN Notices, vol. 41, no. 7,
pp. 34–43, 2006.