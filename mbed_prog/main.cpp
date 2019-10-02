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

#define NBYTES 100000

int main(int argc, char *argv[]) {
    printf("Read bytes task nbytes = %d\n", NBYTES);
    char arr1[NBYTES];
    char arr2[NBYTES];
    memset(arr1, 0xff, NBYTES);
    tick();
    memcpy(arr2, arr1, NBYTES);
    tock();
    printf("Done\n");
    
    print_stats_as_json();
}
