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

#define NBYTES 10

int dont_optimize = 0;

int main(int argc, char *argv[]) {
    register_task("ReadBytesTask");
    printf("Read bytes task nbytes = %d\n", NBYTES);
    char* arr1 = (char *)malloc(NBYTES);
    char* arr2 = (char *)malloc(NBYTES);
    
    for (int i = 0; i < NBYTES; i++)
        arr1[i] = rand() % 128;

    tick();
    memcpy(arr2, arr1, NBYTES);
    tock();
    printf("Done\n");
    
    // Don't optimize results
    for (int i = 0; i < NBYTES; i++)
        dont_optimize += arr2[i];
    printf("%d\n", dont_optimize);

    print_stats_as_json();
}
