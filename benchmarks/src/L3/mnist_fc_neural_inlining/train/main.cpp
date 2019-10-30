#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "baseline.h"

#include <stdint.h>

//  Windows
#ifdef _WIN32

#include <intrin.h>
uint64_t rdtsc(){
    return __rdtsc();
}

//  Linux/GCC
#else

uint64_t rdtsc(){
    unsigned int lo,hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}

#endif

int main() {
    float in[784], out[10];
    for (int i = 0; i < 784; i++) in[i] = i;
    memset(out, 0, sizeof(float)*10);
    
    uint64_t start = rdtsc();
    //inference_baseline(in, out);
    inference_inlined((int *)in, (int *)out);
    uint64_t elapsed = rdtsc()-start;

    for (int i = 0; i < 10; i++) {
        printf("%f ", out[i]);
    }
    printf("\n");

    printf("%lld\n", elapsed);
}
