#include "uTensor/util/uTensor_util.hpp"
#include "mbed.h"
#include "deep_mlp.hpp"
#define NUM_IMAGES 10

Serial pc(USBTX, USBRX, 9600);

int main()
{
    printf("uTensor deep learning character recognition demo\n");
    printf("https://github.com/uTensor/utensor-mnist-demo\n");
    printf("Draw a number (0-9) on the touch screen, and press the button...\r\n");

    printf("Starting the timer!\n");
    static float test_image[NUM_IMAGES][28 * 28];
    Tensor *input_tensor; 
    for (int i = 0; i < NUM_IMAGES; i++) {
    Context ctx;
    input_tensor = new WrappedRamTensor<float>({1, 784}, &(test_image[i][0]));
    get_deep_mlp_ctx(ctx, input_tensor);
    // printf("Evaluating\n\r");
    ctx.eval();
    // S_TENSOR prediction = ctx.get({"y_pred:0"});
    // int result = *(prediction->read<int>(0,0));
    // printf("Number guessed %d\n\r", result);
    // printf("Step\n");
    }
    return 0;
}
