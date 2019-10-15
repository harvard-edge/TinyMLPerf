#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

#ifndef __ON_PC
#include <mbed.h>
#endif

#include "uTensor/util/uTensor_util.hpp"
#include "mbed.h"
#include "deep_mlp.hpp"
#define NUM_IMAGES 10

Serial pc(USBTX, USBRX, 9600);

int main()
{
    register_task("MnistFC");
    printf("MnistFC Task\n");

    static float test_image[NUM_IMAGES][28 * 28];
    Tensor *input_tensor; 
    tick();
    for (int i = 0; i < NUM_IMAGES; i++) {
        Context ctx;
        input_tensor = new WrappedRamTensor<float>({1, 784}, &(test_image[i][0]));
        get_deep_mlp_ctx(ctx, input_tensor);
        ctx.eval();
        // S_TENSOR prediction = ctx.get({"y_pred:0"});
        // int result = *(prediction->read<int>(0,0));
        // printf("Number guessed %d\n\r", result);
        // printf("Step\n");
    }
    tock();
    return 0;
}
