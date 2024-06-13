# Rocket core

According to Chipyard's documentation:
*[Rocket](https://chipyard.readthedocs.io/en/stable/Generators/Rocket.html) is a 5-stage in-order scalar processor core generator, originally developed at UC Berkeley and SiFive, and now maintained by Chips Alliance. The Rocket core is used as a component within the Rocket Chip SoC generator. A Rocket core combined with L1 caches (data and instruction caches) form a Rocket tile. The Rocket tile is the replicable component of the Rocket Chip SoC generator*.

<p align='center'>
<img src="./screenshots/rocketchip diagram.png" alt="rocket chip" width="500"/>
</p>

## Table of Contents

- [Build your first rocket core](#build-your-first-rocket-core) explains how to generate RTL files for your first rocket core.
    * [Setting up TutorialConfig](#setting-up-tutorialconfig)
    * [Run a binary test](#run-a-binary-test)
- [Assessing the performance of the designed core](#assessing-the-performance-of-the-designed-core) demonstrates how to assess the performance of your rocket core.
    * [Benchmark](#benchmark)
    * [Customized project](#customized-project)
    * [Impact of core size on performance](#impact-of-core-size-on-performance)

## Build your first rocket core

Chipyard offers several flavours of rocket cores. You can easily customise the number of cores you want, their size, as well as cache parameters such as way association or even cache size. 
Feel free to set up your preferred configuration.

### Setting up TutorialConfig

Before compiling a custom configuration, it is strongly recommended that you understand how ``TutorialConfigs`` works.

1. Have a look at the file

```shell
cd chipyard/generators/chipyard/src/main/scala/config
```
![Tutorial config](./screenshots/tutorial%20config.png)

The default architecture can be customised. Uncomment the line to activate the desired feature.

:warning: ``WithInclusiveCache(nBanks=1, nWays=4, capacityKB=128)`` **seems to produce an error since** ``nBanks`` **is not recognised as a known parameter.**


2. Start the Verilator RTL build 
```shell
cd chipyard/sims/verilator
make CONFIG=TutorialStarterConfig
```

This builds the RTL files associated with your ``TutorialStarterConfig``.

### Run a binary test

Once the RTL files for rocket's default core have been generated, it's time to check whether or not your architecture works, and to evaluate the corresponding performance.

1. Navigate to the Verilator directory

```shell
cd chipyard/sims/verilator
```

2. Run a basic RISC-V binary test

```shell
export BINARY=$RISCV/riscv64-unknown-elf/share/riscv-tests/isa/rv64ui-p-simple
make CONFIG=TutorialStarterConfig run-binary
```

3. Look at the output file
```shell
cd chipyard/sims/verilator/output/chipyard.harness.TestHarness.RocketConfig
```
![out binary](./screenshots/out%20rv-64-ui-simple.png)

and the number of simulation cycles

![out passed](./screenshots/out%20rv-64-ui-simple%20passed.png)

Of course, not all tests are relevant to all architectures.
It is possible for two completely different architectures to produce the same results for the same test, simply because the test is not adapted to compare what needs to be compared. Ask a dog and a cat to multiply two numbers, and the result won't help you work out which one eats its bowl faster. This twisted analogy shows that choosing the right test is not so trivial...
To solve this problem, you can either run all the binary tests available and then compare several output files, or implement your own custom project.

## Assessing the performance of the designed core

Not all rocket cores are equivalent, and you may wonder how your modifications will affect the performance of your design. To do this, you usually want to perform a benchmark of your core, or even make a custom design.

### Benchmark

Chipyard, by default, offers [benchmarks tests](https://chipyard.readthedocs.io/en/stable/Simulation/Software-RTL-Simulation.html#custom-benchmarks-tests)

```shell
cd chipyard/.conda-env/riscv-tools/riscv64-unknown-elf/share/riscv-tests/benchmarks
```

You run them by adding the make target ``run-bmark-tests``

```shell
cd chipyard/sims/verilator
make CONFIG=YourRocketConfig run-bmark-tests
```

and the output file resembles the initial binary test files, except that a summary of performance is displayed in the console window

```shell
cd chipyard/sims/verilator/output/chipyard.harness.TestHarness.YourRocketConfig
```
```shell
[ PASSED ] chipyard/sims/verilator/output/chipyard.harness.TestHarness.YourRocketConfig/median.riscv.out
Completed after             589916 simulation cycles
```

Some of the generated ``.riscv.log`` files can be used to draw comparisons between your architectures, as the number of ``mcycle`` may differ

![mcycle example](./screenshots/mcycle%20example.png)

### Customized project

Chipyard also offers the option of running your core on [custom project](https://chipyard.readthedocs.io/en/stable/Simulation/Software-RTL-Simulation.html#custom-benchmarks-tests).

1. Create your C program (for example [helloworld.c](./custom%20projects/helloworld.c))

```C
#include <stdio.h>

int main() {
    printf("Hello world!\n");
    return 0;
}
```

2. Add it to Chipyard's ``test`` directory, then add its name to the list of ``PROGRAMS`` inside the ``Makefile``

```Makefile
PROGRAMS = pwm blkdev accum charcount nic-loopback big-blkdev pingd \
           streaming-passthrough streaming-fir nvdla spiflashread spiflashwrite fft gcd \
           hello mt-hello symmetric helloworld
```

3. Generate all the ``.riscv`` ELF binaries

```shell
cd chipyard/tests
make
```

4. Enter Verilator and run the generated binary

```shell
cd chipyard/sims/verilator
make CONFIG=YourRocketConfig run-binary BINARY=../../tests/helloworld.riscv
```

After a while, it should be displayed in the console 
> Hello world!

5. Performance is evaluated in the output file

```shell
cd chipyard/sims/verilator/output/chipyard.harness.TestHarness.YourRocketConfig
```

![out helloworld](./screenshots/out%20helloworld.png)

### Impact of core size on performance

The following section illustrates how custom projects can be used to monitor the impact of core size on the performance of your setups. Suppose, two configurations:

| WithNSmallCores(1)  | WithNBigCores(1) |
|     :---:      |     :---:      |
| 16KiB cache size | 4KiB cache size |
| 4-way set associative Icache and Dcache  | direct-mapped Icache and Dcache  |

1. Add them to the ``RocketConfigs`` file

```shell
cd chipyard/generators/chipyard/src/main/scala/config
```

![small and big rocket config](./screenshots/small%20and%20big%20rocket%20config.png)

Note that the ``RocketConfig`` is a default configuration.

2. As in the tutorial, generate the correspondig RTL files

```shell
cd chipyard/sims/verilator
make CONFIG=RocketConfig
make CONFIG=SmallCoreRocketConfig
```

They should appear in the ``generated-src`` directory.

3. Create your C program (for instance [matmul.c](./custom%20projects/matmul.c)). 
The proposed script implements matrix multiplication, with the performance read function and the size defined as a macro

```C
// Read the performance register
#define read_csr(reg) ({ unsigned long __temp; \
  asm volatile ("csrr %0, " #reg : "=r"(__temp)); \
  __temp; })

// Matrix size
#define SIZE 40
```

4. Add it to Chipyard's ``test`` directory, then add its name to the list of ``PROGRAMS`` inside the ``Makefile``

```Makefile
PROGRAMS = pwm blkdev accum charcount nic-loopback big-blkdev pingd \
           streaming-passthrough streaming-fir nvdla spiflashread spiflashwrite fft gcd \
           hello mt-hello symmetric matmul
```

5. Generate all the ``.riscv`` ELF binaries

```shell
cd chipyard/tests
make
```

6. Enter Verilator and run the generated binary for both configurations

```shell
cd chipyard/sims/verilator
make CONFIG=RocketConfig run-binary BINARY=../../tests/matmul.riscv
make CONFIG=SmallCoreRocketConfig run-binary BINARY=../../tests/matmul.riscv
```

This should result in a ``matmul.riscv.log`` file which can be used to assess the impact of core size on performance

```shell
cd chipyard/sims/verilator/output/chipyard.harness.TestHarness.RocketConfig
cd chipyard/sims/verilator/output/chipyard.harness.TestHarness.SmallCoreRocketConfig
```

:warning: **Increasing the size of the matrix too much seems to produce an error. It is suspected that the maximum permitted simulation cycle has been reached. Feel free to dig into the configuration files to increase this limit beyond the current value.**

7. Repeat steps 3 to 6, changing the size of the matrix.
Don't forget to save the various ``matmul.riscv.log`` files in an appropriate folder, as the new files generated will overwrite the existing ones.

8. Use the proposed python script [performance.py](./custom%20projects/performance.py) to display the simulation results

![simulation results](./screenshots/CLK%20cycles%20for%20different%20matrix%20sizes.png)