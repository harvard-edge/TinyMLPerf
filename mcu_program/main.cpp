#include "model.hpp"
#include "cifar_img_data.h"
#include "uTensor/util/uTensor_util.hpp"
#include <stdio.h>

#ifndef __ON_PC
#include <mbed.h>
#endif

// Set up the serial connections
#ifndef __ON_PCe
Serial pc(USBTX, USBRX, 9600);   // baud rate of our MCUs
#endif

#define NUM_IMAGES 3

static size_t argmax(S_TENSOR logits) {
	float max_logit = *(logits->read<float>(0, 0));
	size_t max_label = 0;
	for (size_t i = 0; i < logits->getSize(); i++) {
		float logit = *(logits->read<float>(i, 0));
		if (logit > max_logit) {
			max_label = i;
			max_logit = logit;
		}
	}
	return max_label;
}


int main(int argc, char *argv[]) {
	printf("Starting the timer!\n");
	us_ticker_init();
	uint32_t begin_time = us_ticker_read();
	static float test_image[NUM_IMAGES][3072];
	Tensor *input_tensor; 
	for (int i = 0; i < NUM_IMAGES; i++) {
    	Context ctx;
		input_tensor = new WrappedRamTensor<float>({1, 3072}, &(test_image[i][0]));
		get_model_ctx(ctx, input_tensor);
		// printf("Evaluating\n\r");
		ctx.eval();
		// S_TENSOR prediction = ctx.get({"y_pred:0"});
		// int result = *(prediction->read<int>(0,0));
		// printf("Number guessed %d\n\r", result);
		// printf("Step\n");
	}
	uint32_t end_time = us_ticker_read();
	float fps = (float) ((end_time - begin_time)) / NUM_IMAGES;
	printf("Total microseconds elapsed per inf: %f\n", fps);
    return 0;
}


/*
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
	us_ticker_init();
	uint32_t begin_time = us_ticker_read();
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
	uint32_t end_time = us_ticker_read();
	float fps = (float) ((end_time - begin_time)) / NUM_IMAGES;
	printf("Total microseconds elapsed per inf: %f\n", fps);
    return 0;
}*/
