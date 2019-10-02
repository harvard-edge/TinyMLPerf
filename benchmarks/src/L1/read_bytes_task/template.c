#include <stdio.h>

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
    char *arr1 = malloc(NBYTES);
    char *arr2 = malloc(NBYTES);
    memset(arr1, 0xff, NBYTES);
    memcpy(arr2, arr1, NBYTES);
    print("Done\n");
}
