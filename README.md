
# User guide to help you get started with Chipyard

[Chipyard](https://github.com/ucb-bar/chipyard) repository provides HW generators for in-order cores, HW accelerators and simple SoCs.
The aim of this guide is to help students familiarise themselves with Chipyard's Github, and to explain the first steps to be taken to install it correctly.
Finally, students will be able to generate a simple core and an SoC (multi-core version) using Rocket in-order core at least.

## Table of Contents

- [Quick installation](#quick-installation) is a short set of instructions for those who want to dive straight into installation. For more information, please refer to [Chipyard's initial repository setup](https://chipyard.readthedocs.io/en/stable/Chipyard-Basics/Initial-Repo-Setup.html).
  * [Windows Subsystem for Linux](#windows-subsystem-for-linux)
  * [Setting up your Conda environment](#setting-up-your-conda-environment)
  * [Setting up the Chipyard repository](#setting-up-the-chipyard-repository)

## Quick installation

The firsts steps of this configuration are OS-dependent.

**Machine info:**
  - **OS**: OS Name	Microsoft Windows 10 Pro
  - **RAM**: 32GB
  - **CPU**: i7-1265U

*As this tutorial is dedicated to Windows users, MacOS and Linux owners are strongly encouraged to find out about the different alternatives on the various suggested sites*.


### Windows Subsystem for Linux

If you're familiar with Linux, you'll notice that the following commands are intended to be copied and pasted into a Linux-based shell.
Try these same commands in Windows Powershell and nothing good will happen.
To do this, you first need to install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install).
After installation, a new tab appears in your file explorer

![ubuntu](./screenshots/Screenshot%202024-04-29%20162355.png)


### Setting up your Conda environment

Chipyard uses **Conda** to help manage system dependencies.
Conda requires the [Miniforge](https://github.com/conda-forge/miniforge/?tab=readme-ov-file#download) installer to be running on your system.

1. Download the latest installer running the following commands 
```shell
curl -L -O "https://github.com/conda-forge/miniforge/releases latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

2. **Miniforge** must be on your system path (default for Linux and MacOs) for **Conda** and **Mamba** programs to be used at any command prompt.
For Windows user, Miniforge is not added to your system path by default... 2 solutions are available to you:
    - Access Conda and Mamba via the Miniforge prompt
    - Add the folder to the path environment variable [manually](https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)#to-add-a-path-to-the-path-environment-variable)

  > file://wsl.localhost/Ubuntu/home/myusername/miniforge3/condabin

  ![path Miniforge](./screenshots/Screenshot%202024-04-29%20173310.png)

3. Next, [libmamba](https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community) is installed for faster dependency solving
```shell
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

4. Finally, install ```conda lock``` into the ```base``` conda environment
```shell
conda install -n base conda-lock==1.4.0
conda activate base
```

```(base)``` must appear in front of your username at the Linux prompt.

5. Check that Conda is correctly installed
```shell
conda --version
```

### Setting up the Chipyard repository

1. Copy the repository directly from Github into your project directory and type in
```shell
git clone https://github.com/ucb-bar/chipyard.git
cd chipyard
```

2. Setup Chipyard with the correct ```riscv-tools``` toolchain.
```shell
./build-setup.sh riscv-tools 
```
If an error occurs during the execution of a given step, you can always skip this step (please check its purpose first) using the command
```shell
./build-setup.sh riscv-tools -s ...
```
 For the context of this project, only RTL files are concerned, the command ``-s 9`` has been used to skip the *pre-compilation of FireMarshal default buildroot Linux sources* step as a recurring error seems to be correlated to this step.
However, if you are interested in FPGA/ASICS implementation, please refer to [FireSim](https://chipyard.readthedocs.io/en/stable/Simulation/FPGA-Accelerated-Simulation.html#firesim) and [FireMarshal](https://chipyard.readthedocs.io/en/stable/Software/FireMarshal.html) before skipping this step.

3. Before going any further, you can check the conda environment listed
```shell
conda env list
```

4. When completed, an ```env.sh``` file should exist in the top-level directory.
**This file must be created before running any** ```make``` **commands**, as it activates the conda environment created in ```build-setup.sh``` and sets up any necessary environment variables that may be needed later.
```shell
source ./env.sh
```