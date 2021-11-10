# Artifact for submission "Sound, Precise, and Fast Abstract Interpretation with Tristate Numbers"

## Abstract of the paper.

Extended Berkeley Packet Filter (BPF) is a language and run-time system that allows non-superusers to extend the Linux and Windows operating systems by downloading user code into the kernel. To ensure that user code is safe to run in kernel context, BPF relies on a static analyzer that proves properties about the code, such as bounded memory access and the absence of operations that might crash. The BPF static analyzer checks safety using abstract interpretation with several abstract domains. Among these, the domain of tnums (tristate numbers) is a key domain used to reason about uncertainty in values at the bit level. This paper formally specifies the tnum abstract domain and its arithmetic operators. We provide the first proofs of soundness and optimality of the abstract arithmetic operators for tnum addition and subtraction used in the BPF analyzer. Further, we describe a novel sound algorithm for multiplication of tnums that is more precise and efficient (runs 33% faster on average) than the Linux kernel's algorithm. Our tnum multiplication is now merged in the Linux kernel.

--------------------------------------------------------------------------------

## Claims to validate/reproduce.

In this artifact, we provide instructions to reproduce and validate the
following claims in the paper.

1. Semantics and verification of tnum operations using the Z3 SMT solver

2. Computation of observed imprecision from operational imprecision and
   representational imprecision

3. Precision improvements in our tnum multiplication algorithm compared 
   to the Linux kernel's tnum multiplication.

4. Performance improvements in our tnum multiplication algorithm compared to
   Linux kernel's tnum multiplication.

`Note`. To make it feasible to run the artifact quickly, we have reduced the sample
sizes used for the performance experiment. The experiments for the paper were
performed without using any containers, and on larger inputs sizes. 
Hence, there will be small differences in the results but the overall trends
will be similar. We also note any other when compared to the paper, 
if present, in the explantion section of each experiment. 
It should take roughly 30 minutes to evaluate this artifact.

--------------------------------------------------------------------------------

## Instructions to run the artifact.

### Downloading prebuilt Docker Image

1. Install docker if it is not installed already by following the
documentation [here](https://docs.docker.com/install/). You might need to follow the post installation steps 
for managing docker as a non-root user [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

2.  Run the docker image:
```
docker load < sas21_artifact.tar.gz
docker run -it sas21_artifact
cd sas2021-artifact
```

### Known issues. 
We have tested the docker image on different architectures (`x86_64`, `amd64`)
and have no known issues to report.

--------------------------------------------------------------------------------

### Automated Verfication with Z3
In this experiment, we verify the correctness of all tnum operations. For all
operations except the multiplication operations, `mul` and `our_mul`, we perform
automated verification with bitvectors of width `64`. For multiplication, since
the automated verification takes a long time to complete, we perform automated
verification with 8-bits. This experiment should take roughly 5 minutes.


#### Run
```
cd verification
bash veri.sh
```

#### Expected Result 

```
Verifying tnum_add...
========> verification completed for <64>-bits tnum_add operation

Verifying tnum_sub...
========> verification completed for <64>-bits tnum_sub operation

Verifying tnum_and...
========> verification completed for <64>-bits tnum_and operation

Verifying tnum_or...
========> verification completed for <64>-bits tnum_or operation

Verifying tnum_xor...
========> verification completed for <64>-bits tnum_xor operation

Verifying tnum_lshift...
========> verification completed for <64>-bits tnum_lshift operation

Verifying tnum_rshift...
========> verification completed for <64>-bits tnum_rshift operation

Verifying tnum_arshift...
========> verification completed for <64>-bits tnum_arshift operation

Verifying tnum_mul...
========> verification completed for <8>-bits tnum_mul operation

Verifying our_mul...
========> verification completed for <8>-bits our_mul operation
```

#### Explanation
The automated verification is done using
[z3py](https://ericpony.github.io/z3py-tutorial/guide-examples.htm). Note that
the actual python script containing the encoding of tnum operations is in
`tnum.py`. 

The linux kernel uses 64-bit numbers for tnum operations. The output of this
experiment, should show that we successfully verify the correctness of
`tnum_lshift`, `tnum_rshift`, `tnum_arshift`, `tnum_and`, `tnum_or`, `tnum_xor`,
`tnum_add`, and `tnum_sub` with bitvectors of width 64. For the multiplication
operations `tnum_mul`, and `our_mul`, here, we verify correctness with
bitvectors of width 8, since the verification for 64-bits cannot be completed in
a reasonable amount of time. As mentioned in the paper, we have verified the
correctness of multiplication for bitvectors of width 14, which took around 1
day.  

#### Source code structure
The only source file related to this experiment is `tnum.py`, which
accepts switches for `--bitwidth`, the bitvector width and `--op` for
the tnum operation that we perform the verification for. The `Tnum`
class contains the `z3` encoding of tnum operations from the Linux
kernel. For instance `Tnum.tnum_add` returns a formula containing the
z3 encoding of the `tnum_add` from the Linux kernel. The
`TnumOpsVerifier` class contains methods which encode the
verification condition for the similarly name tnum operations, and verify 
them in a solver (by checking if the solver returns `unsat`).

--------------------------------------------------------------------------------

### Generating observed imprecision data for tnum operations (_Table 1. in the paper submission_ )
In this experiment, we measure the observed imprecision `Iobs`, representational
imprecision `I_repr` and operational imprecision `I_oper`, of all the tnum
operations. We present how these are defined and computed in the paper. The
generated binary after compilation (`precision_all_table.o`) accepts a switch
for bitwidth as its only command line argument. To finish this experiment in a
reasonable amount of time, we propose using a bitwidth of `6`. This experiment
should take roughly 5 minutes.


#### Compile
```
cd ../precision-all

g++ -g -w -I../include/ ../include/conc.c ../include/tnum.c precision_all_table.cpp -o precision_all_table.o
```

#### Run
```
./precision_all_table.o 6 | column -t -s,
```

#### Expected Result 

```
tnum op   |Iobs|    |Irepr|   |Ioper|
lshift    1         1         1
rshift    1         1         1
arshift   1         1         1
and       1         1         1
or        1         1         1
xor       1         1         1
add       2.15946   2.15946   1
sub       2.15946   2.15946   1
mul       2.63867   2.35783   1.12473
our_mul   2.63527   2.35783   1.12365
```

#### Explanation
The data produced from this experiment shows the different kinds of imprecision
a tnum operation can contribute to. The actual table thus generated won't be
exactly the same as the one in the paper, where use a bitwidth of `8`. However,
the claim we make about the classification of tnum operations according to
`Iobs`, `I_repr`, and `I_oper`precision still holds. The results should show
that the shift operations and bitwise operations, `lshift`, `rshift`, `arshift`,
`and`, `or`, and `xor` are _maximally precise_. `Iobs`, `I_repr`, and `I_oper`
should all be `1`. Next, we have `add` and `sub`, these operations are
_maximally operationally precise_: `I_oper` should be `1` for these operations,
however `Irepr` should be greater than `1`. `I_obs` should be equal to `I_repr`,
which says that the observed imprecision is purely representational. Finally, we
have `mul` and `our_mul`, these operations have both operational and
representational imprecision, and `I_obs` should be  `I_repr * I_oper`. 

#### Source code structure
The main source file related to this file is `precision_all_table.cpp`
and all the files in the `include` directory. The `include` directory
contains source code from the Linux kernel, and basic wrappers for
concrete operations.  In `precision_all_table.cpp`, the function
`calc_precision_helper` does the main work. It performs the tnum
operation on two input tnums `t1` and `t2` for a given tnum operation
`op` provided from the command line, and does the other necessary
calculations related to computing imprecision. The function
`generate_all_tnums` generates all possible tnums of a particular
bitwidth, `get_shared_bits_tnum` returns a tnum which is the most
concise tnum-representation of a given set of concrete values (using
the algorithm from section 2.3 in the paper). If using a bitwidth of
8, when performing the tnum operation, we zero out the top 56 bits
from the output tnum's value and mask, to effectively produce an 8-bit
tnum. 

--------------------------------------------------------------------------------

### Relative precision of `our_mul` vs. `mul` (_Fig 5. in the paper submission_)
In this experiment, we compare the relative precision of our new tnum
multiplication algorithm `our_mul` with the Linux kernel's `tnum_mul` . The
generated binary after compilation (`precision_relative.o`) accepts a switch
for bitwidth as its only command line argument. To finish this experiment in a
reasonable amount of time, we propose using a bitwidth of `8`. This experiment
should take roughly 5 minutes.

#### Compile
```
cd ../precision-relative

g++ -g -w -I../include/ ../include/conc.c ../include/tnum.c precision_relative.cpp -o precision_relative.o
```

#### Run 
```
./precision_relative.o 8 > pres_rel.log
```

#### Produce graph
```
python3 graph_precision_relative.py --bitwidth=8 --file=pres_rel.log
```

#### Extract graph from docker
1. Open a new terminal to find docker image ID
```
$ docker ps -a

CONTAINER ID   IMAGE             COMMAND     CREATED        STATUS         PORTS    NAMES
30e20b7c68d7   sas21_artifact1   "/bin/bash" 4 hours ago    Up 20 minutes           elegant_tu
```
2. Copy sas21_artifact `CONTAINER ID` to clipboard (your ID may be different).

3. Copy the .png file to your local machine
```
docker cp <insert CONTAINER_ID here>:/home/sas2021-artifact/precision-relative/pres_rel.png <insert destination directory>
```
4. Open the png in your favourite image viewer. 

#### Explanation
The graph depicts the cumulative distribution of the ratio of the size of the
set represented by the output tnum produces `mul` to that of `our_mul`.  The
graph thus generated should be exactly the same as the one in the paper,
where also use a bitwidth of `8`. We ignore the cases where `mul` and `our_mul`
produce the same exact output tnum: for those particular input tnum pairs, `mul`
and `our_mul` are equally precise. Each tick on the x-axis to the right of 0 is
a point where `our_mul` produces a tnum that is more precise in exactly one bit
position when compared to `mul`. The figure should show that for 80% of the
cases, `our_mul` produces a more precise tnum than `mul` (the data to the right
of 0), indicating that our new multiplication algorithm is more precise than the
Linux kernel's implementation.

#### Source code structure
The source file `precision_relative.cpp` is very similar to the
previous experiment, and uses similar function calls. 

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
30e20b7c68d7   sas21_artifact1   "/bin/bash" 4 hours ago    Up 20 minutes           elegant_tu
```
2. Copy sas21_artifact `CONTAINER ID` to clipboard (your ID may be different).

3. Copy the .png file to your local machine
```
docker cp <insert CONTAINER_ID here>:/home/sas2021-artifact/performance/perf.png <insert destination directory>
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