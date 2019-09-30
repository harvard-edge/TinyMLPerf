#include <stdio.h>

#ifndef __ON_PC
#include <mbed.h>
#endif

// Set up the serial connections
#ifndef __ON_PCe
Serial pc(USBTX, USBRX, 9600);   // baud rate of our MCUs
#endif

#define PARAM1 {{PARAM1}}
#define PARAM2 {{PARAM2}}

int main(int argc, char *argv[]) {
    printf("Hello World %d %d\n", PARAM1, PARAM2);
    return 0;
}
