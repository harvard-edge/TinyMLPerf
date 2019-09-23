#include "cifar10_cnn.hpp"
#include "uTensor/util/uTensor_util.hpp"
#include <stdio.h>

#ifndef __ON_PC
#include <mbed.h>
#endif


// Set up the serial connections
#ifndef __ON_PCe
Serial pc(USBTX, USBRX, 9600);   // baud rate of our MCUs
#endif


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
	// Create clock to time our neural network
	us_ticker_init();
	uint32_t begin_time = us_ticker_read();

	Context ctx;
	float data[32 * 32 * 3];
	Tensor *input_tensor = new WrappedRamTensor<float>({1, 32, 32, 3}, data);
	get_cifar10_cnn_ctx(ctx, input_tensor);

	// S_TENSOR logits = ctx.get("fully_connect_2/logits:0");
	ctx.eval();

	uint32_t end_time = us_ticker_read();
	printf("HELLO, this is wfu!\n");
	printf("Took %u us to run through the NN\n", end_time - begin_time);
	printf("The answer we got from the NN was\n");
	return 0;
}