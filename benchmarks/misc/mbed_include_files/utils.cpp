#include "utils.h"

using namespace std;

double time_elapsed = -1;
clock_t begin_time, end_time;
const char *task_name = "NULL";

void tick() {
    begin_time = clock();
}

void tock() {
    end_time = clock();
    time_elapsed = (double)(end_time - begin_time) / CLOCKS_PER_SEC;
}

void register_task(const char *name) {
    task_name = name;
}

void print_stats_as_json() {

    mbed_stats_heap_t heap_info;
    mbed_stats_stack_t stack_info[MAX_THREAD_INFO];

    debug("\nThis message is from debug function");
    debug_if(1,"\nThis message is from debug_if function");
    debug_if(0,"\nSOMETHING WRONG!!! This message from debug_if function shouldn't show on bash");
    
    // Add heap info to map
    map<string, string> data = {
        {"task_name", string(task_name)},
        {"time_elapsed", to_string(time_elapsed)},
        {"heap_info.current_size", to_string(heap_info.current_size)},
        {"heap_info.max_size", to_string(heap_info.max_size)},
        {"heap_info.total_size", to_string(heap_info.total_size)},
        {"heap_info.reserved_size", to_string(heap_info.reserved_size)},
        {"heap_info.alloc_cnt", to_string(heap_info.alloc_cnt)},
        {"heap_info.alloc_fail_cnt", to_string(heap_info.alloc_fail_cnt)}
    };

    // Add per-thread stack info
    for (int i = 0 ; i < MAX_THREAD_INFO; i++) {
        if (stack_info[i].thread_id != 0) {
            string stack_id = "stack_info[" + to_string(i) + "]";
            data[stack_id + ".thread_id"] = to_string(stack_info[i].thread_id);
            data[stack_id + ".max_size"] = to_string(stack_info[i].max_size);
            data[stack_id + ".reserved_size"] = to_string(stack_info[i].reserved_size);
            data[stack_id + ".stack_cnt"] = to_string(stack_info[i].stack_cnt);
        }
    }
    
    // Output as json
    map<string, string>::iterator it;
    cout << endl << "{";
    int first = 1;        
    for (it = data.begin(); it != data.end(); it++) {
        if (!first) cout << ", ";
        first = 0;
        cout << "\"" << it->first << "\"" << " : " << it->second;
    }
    cout << "}" << endl;
}

void print_memory_stats() {
    mbed_stats_heap_t heap_info;
    mbed_stats_stack_t stack_info[MAX_THREAD_INFO];

    debug("\nThis message is from debug function");
    debug_if(1,"\nThis message is from debug_if function");
    debug_if(0,"\nSOMETHING WRONG!!! This message from debug_if function shouldn't show on bash");
    
    printf("\nMemoryStats:");
    mbed_stats_heap_get( &heap_info );
    printf("\n\tBytes allocated currently: %d", heap_info.current_size);
    printf("\n\tMax bytes allocated at a given time: %d", heap_info.max_size);
    printf("\n\tCumulative sum of bytes ever allocated: %d", heap_info.total_size);
    printf("\n\tCurrent number of bytes allocated for the heap: %d", heap_info.reserved_size);
    printf("\n\tCurrent number of allocations: %d", heap_info.alloc_cnt);
    printf("\n\tNumber of failed allocations: %d", heap_info.alloc_fail_cnt);
    
    mbed_stats_stack_get( &stack_info[0] );
    printf("\nCumulative Stack Info:");
    printf("\n\tMaximum number of bytes used on the stack: %d", stack_info[0].max_size);
    printf("\n\tCurrent number of bytes allocated for the stack: %d", stack_info[0].reserved_size);
    printf("\n\tNumber of stacks stats accumulated in the structure: %d", stack_info[0].stack_cnt);
    
    mbed_stats_stack_get_each( stack_info, MAX_THREAD_INFO );
    printf("\nThread Stack Info:");
    for(int i=0;i < MAX_THREAD_INFO; i++) {
        if(stack_info[i].thread_id != 0) {
            printf("\n\tThread: %d", i);
            printf("\n\t\tThread Id: 0x%08X", stack_info[i].thread_id);
            printf("\n\t\tMaximum number of bytes used on the stack: %d", stack_info[i].max_size);
            printf("\n\t\tCurrent number of bytes allocated for the stack: %d", stack_info[i].reserved_size);
            printf("\n\t\tNumber of stacks stats accumulated in the structure: %d", stack_info[i].stack_cnt); 
        }        
    }
}
