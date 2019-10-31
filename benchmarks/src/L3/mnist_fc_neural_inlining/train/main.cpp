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

#include "mbed.h"
#include "baseline.c"
#define NUM_IMAGES 10

#define H1_SIZE {{h1}}
#define H2_SIZE {{h2}}
#define ACCURACY {{accuracy}}
#define SPARSITY {{sparsity}}

int main() {

    register_task("MnistFCSparsity");
    register_kv("h1", to_string(H1_SIZE));
    register_kv("h2", to_string(H2_SIZE));
    register_kv("accuracy", to_string(ACCURACY));
    register_kv("sparsity", to_string(SPARSITY));
    printf("MnistFCSparsity Task\n");

    //float in[784], out[10];
    float *in = (float *)malloc(sizeof(float)*(784/4));
    float *out = (float *)malloc(sizeof(float)*10);
    for (int i = 0; i < 784/4; i++) in[i] = i;
    memset(out, 0, sizeof(float)*10);
    
    tick();
    //inference_baseline(in, out);
    inference_inlined(in, out);
    tock();

    for (int i = 0; i < 10; i++) {
        printf("%f ", out[i]);
    }
    printf("\n");

    print_stats_as_json();
}
