#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "utils.h"

#ifndef __ON_PC
#include <mbed.h>
#endif

// Set up the serial connections
#ifndef __ON_PCe
Serial pc(USBTX, USBRX, 9600);   // baud rate of our MCUs
#endif

#define NFLOATS 128
#define AI 0.25
#define N_REPS 100

int main(int argc, char *argv[]) {
    register_task("ArithmeticIntensityTask");
    register_kv("NFLOATS", to_string(NFLOATS));
    register_kv("AI", to_string(AI));
    register_kv("N_REPS", to_string(N_REPS));
    printf("Arithmetic intensity task nfloats = %d, arithmetic intensity = %f, nreps = %d\n", NFLOATS, AI, N_REPS);

    assert(AI >= .25);
    
    // Create int array
    int *a = (int *)malloc(sizeof(int) * NFLOATS);
    for (int i = 0; i < NFLOATS; i++) {
        a[i] = rand() % 255;
    }
    
    tick();
    
    int result = 0;

    // Do computation
    for (int k = 0; k < N_REPS; k++) {
        result = 0;
        for (int i = 0; i < NFLOATS/16; i++) {
            for (int j = 0; j < AI*4; j++) {
                result +=  a[i*(16)+0];
                result +=  a[i*(16)+1];
                result +=  a[i*(16)+2];
                result +=  a[i*(16)+3];
                result +=  a[i*(16)+4];
                result +=  a[i*(16)+5];
                result +=  a[i*(16)+6];
                result +=  a[i*(16)+7];
                result +=  a[i*(16)+8];
                result +=  a[i*(16)+9];
                result +=  a[i*(16)+10];
                result +=  a[i*(16)+11];
                result +=  a[i*(16)+12];
                result +=  a[i*(16)+13];
                result +=  a[i*(16)+14];
                result +=  a[i*(16)+15];
            }
        }
    }

    tock();

    printf("%d\n", result);

    int flop = (N_REPS) * (NFLOATS/16) * (AI*4) * 16;
    register_kv("FLOP", to_string(flop));

    print_stats_as_json();
}
