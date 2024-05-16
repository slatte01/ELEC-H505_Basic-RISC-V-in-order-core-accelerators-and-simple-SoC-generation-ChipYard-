# Rocket core

According to Chipyard's documentation:
*[Rocket](https://chipyard.readthedocs.io/en/stable/Generators/Rocket.html) is a 5-stage in-order scalar processor core generator, originally developed at UC Berkeley and SiFive, and now maintained by Chips Alliance. The Rocket core is used as a component within the Rocket Chip SoC generator. A Rocket core combined with L1 caches (data and instruction caches) form a Rocket tile. The Rocket tile is the replicable component of the Rocket Chip SoC generator*.

<p align='center'>
<img src="./screenshots/rocketchip-diagram.png" alt="rocket chip" width="500"/>
</p>

## Table of Contents

- [Build your first rocket core](#build-your-first-rocket-core) explains how to generate RTL files for your first rocket core.
    * [Setting up TutorialConfig](#setting-up-tutorialconfig)
    * [Run a binary test](#run-a-binary-test)
- [Assessing the performance of the designed core](#assessing-the-performance-of-the-designed-core) demonstrates how to assess the performance of your rocket core
    * [Benchmark](#benchmark)
    * [Customized project](#customized-project)

## Build your first rocket core

Chipyard offers several flavours of rocket cores. You can easily customise the number of cores you want, their size, as well as cache parameters such as way association or even cache size. 
Feel free to set up your preferred configuration.

### Setting up TutorialConfig

Before compiling a custom configuration, it is strongly recommended that you understand how ``TutorialConfigs`` works.

1. Have a look at the file

```shell
cd chipyard\generators\chipyard\src\main\scala\config
```
![Tutorial config](./screenshots/Tutorial%20config.png)

The default architecture can be customised. Uncomment the line to activate the desired feature.

:warning: ``WithInclusiveCache(nBanks=1, nWays=4, capacityKB=128)`` **seems to produce an error since**``nBanks``**is not recognised as a known parameter.**


2. Start the Verilator RTL build 
```shell
cd chipyard\sims\verilator
make CONFIG=TutorialStarterConfig
```

This builds the RTL files associated with your ``TutorialStarterConfig``.

### Run a binary test

Once the RTL files for rocket's default core have been generated, it's time to check whether or not your architecture works, and to evaluate the corresponding performance.

1. Navigate to the Verilator directory

```shell
cd chipyard\sims\verilator
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

![out passed ](./screenshots/out%20passed.png)

Of course, not all tests are relevant to all architectures.
It is possible for two completely different architectures to produce the same results for the same test, simply because the test is not adapted to compare what needs to be compared. Ask a dog and a cat to multiply two numbers, and the result won't help you work out which one eats its bowl faster. This twisted analogy shows that choosing the right test is not so trivial...
To solve this problem, you can either run all the binary tests available and then compare several output files, or implement your own custom project.

## Assessing the performance of the designed core

### Benchmark

### Customized project