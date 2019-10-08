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

#define NFLOATS 100
#define NFLOPS 100

int main(int argc, char *argv[]) {
    register_task("ArithmeticIntensityTask");
    register_kv("NFLOATS", to_string(NFLOATS));
    register_kv("NFLOPS", to_string(NFLOPS));
    printf("Arithmetic intensity task nfloats = %d, NFLOPS = %d\n", NFLOATS, NFLOPS);
    tick();
    
    // Create float array
    float *a = (float *)malloc(sizeof(float) * NFLOATS);
    for (int i = 0; i < NFLOATS; i++) {
        a[i] = rand() % 255;
    }
    float result = rand() % 255;
    
    // Do computation
    for (int i = 0; i < NFLOPS/2; i++) {
        result += result * a[i % NFLOATS];
    }

    tock();
    print_stats_as_json();
}
