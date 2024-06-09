#include <stdint.h>
#include <stdio.h>

// Read the performance register
#define read_csr(reg) ({ unsigned long __temp; \
  asm volatile ("csrr %0, " #reg : "=r"(__temp)); \
  __temp; })

// Matrix size
#define SIZE 40


// Test matrices
int A[SIZE][SIZE];
int B[SIZE][SIZE];
int C[SIZE][SIZE];

// Initialise the matrices
void initialize_matrices() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            A[i][j] = i + j;
            B[i][j] = i - j;
            C[i][j] = 0;
        }
    }
}

// Multiply the matrices
void multiply_matrices() {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            for (int k = 0; k < SIZE; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main() {
    // Call the function to initialise the matrices
    initialize_matrices();

    // Read initial values of the performance metrics
    uint64_t start_cycles = read_csr(mcycle);
    uint64_t start_instructions = read_csr(minstret);

    // Call the function to multiply the matrices
    multiply_matrices();

    // Read the final values of the performance metrics
    uint64_t end_cycles = read_csr(mcycle);
    uint64_t end_instructions = read_csr(minstret);

    // Estimate the performance
    uint64_t cycles = end_cycles - start_cycles;
    uint64_t instructions = end_instructions - start_instructions;

    // Print the results
    printf("mcycle = %lu\n", cycles);
    printf("minstret = %lu\n", instructions);

    return 0;
}
