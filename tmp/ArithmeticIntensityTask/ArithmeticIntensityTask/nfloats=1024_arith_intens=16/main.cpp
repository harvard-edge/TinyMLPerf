#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

#ifndef __ON_PC
#include <mbed.h>
#endif

// Set up the serial connections
#ifndef __ON_PCe
Serial pc(USBTX, USBRX, 9600);   // baud rate of our MCUs
#endif

#define NFLOATS 1024
#define AI 10
#define N_REPS 16.0

int main(int argc, char *argv[]) {
    register_task("ArithmeticIntensityTask");
    register_kv("NFLOATS", to_string(NFLOATS));
    register_kv("AI", to_string(AI));
    register_kv("N_REPS", to_string(N_REPS));
    printf("Arithmetic intensity task nfloats = %d, arithmetic intensity = %d, nreps = %d\n", NFLOATS, AI, N_REPS);

    assert(AI >= .5);
    
    // Create float array
    float *a = (float *)malloc(sizeof(float) * NFLOATS * 4);
    for (int i = 0; i < NFLOATS*16; i++) {
        a[i] = rand() % 255;
    }
    float result = rand() % 255;
    
    tick();

    // Do computation
    for (int i = 0; i < NFLOPS/2; i++) {
        for (int j = 0; j < AI*2; j++) {
            result += result * a[i*(16)+0];
            result += result * a[i*(16)+1];
            result += result * a[i*(16)+2];
            result += result * a[i*(16)+3];
        }
    }

    tock();

    printf("%f\n", result);

    float flop = (NFLOPS/2) * (AI*2) * 8;
    register_kv("FLOP", to_string(flop));

    print_stats_as_json();
}
