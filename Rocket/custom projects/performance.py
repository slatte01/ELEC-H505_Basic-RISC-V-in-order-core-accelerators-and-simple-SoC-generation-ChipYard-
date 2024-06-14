import re
import matplotlib.pyplot as plt

# Extract data from the file
def extract_data(file_path):
    mcycle = None
    minstret = None
    with open(file_path, 'r') as file:
        for line in file:
            match_mcycle = re.search(r'mcycle = (\d+)', line)
            if match_mcycle:
                mcycle = int(match_mcycle.group(1))
            match_minstret = re.search(r'minstret = (\d+)', line)
            if match_minstret:
                minstret = int(match_minstret.group(1))
            if mcycle is not None and minstret is not None:
                break
    return mcycle, minstret


# File paths
file_paths_small = ['Path to the folder were your results are stored']
file_paths_large = ['Path to the folder were your results are stored']

# Matrix sizes
matrix_sizes = ['Add the different matrix sizes']

# Data extraction
data_small = [extract_data(file) for file in file_paths_small]
data_large = [extract_data(file) for file in file_paths_large]

# Get cycles and instrcutions
mcycle_small, minstret_small = zip(*data_small)
mcycle_large, minstret_large = zip(*data_large)

# Plot options
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Cycles
axs[0].plot(matrix_sizes, mcycle_small, marker='o', label='small')
axs[0].plot(matrix_sizes, mcycle_large, marker='o', label='large')
axs[0].set_title('Clock cycles for different matrix sizes')
axs[0].set_ylabel('mcycle')
axs[0].legend()

# Instructions
axs[1].plot(matrix_sizes, minstret_small, marker='o', label='small')
axs[1].plot(matrix_sizes, minstret_large, marker='o', label='large')
axs[1].set_title('Instructions for different matrix sizes')
axs[1].set_ylabel('minstret')
axs[1].legend()

# Common parameters
for ax in axs:
    ax.set_xlabel('Matrix sizes')
    ax.grid(True)

plt.tight_layout()
plt.show()
