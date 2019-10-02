#ifndef UTILS
#define UTILS

#include <stdio.h>
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <ctime>
#include "mbed.h"
#include "platform/mbed_assert.h"
#include "platform/mbed_debug.h"
#include "platform/mbed_error.h"
#include "platform/mbed_stats.h"

#define MAX_THREAD_INFO 10

void tick();
void tock();
void print_stats_as_json();

#endif
