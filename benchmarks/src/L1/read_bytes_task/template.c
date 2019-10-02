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

#define NBYTES {{NBYTES}}

int main(int argc, char *argv[]) {
    printf("Read bytes task nbytes = %d\n", NBYTES);
    char *arr1 = (char *)malloc(NBYTES);
    char *arr2 = (char *)malloc(NBYTES);
    memset(arr1, 0xff, NBYTES);
    memcpy(arr2, arr1, NBYTES);
    printf("Done\n");

    print_memory_stats();
}
