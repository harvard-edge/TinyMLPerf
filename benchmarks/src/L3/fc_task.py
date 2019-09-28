import sys
import argparse
from task import Task
import tensorflow as tf
import numpy as np
from pathlib import Path


RELU_MAIN_FILE = """
#include "model.hpp"
#include "uTensor/util/uTensor_util.hpp"
#include <stdio.h>

#ifndef __ON_PC
#include <mbed.h>
#endif

// Set up the serial connections
#ifndef __ON_PCe
Serial pc(USBTX, USBRX, 9600);   // baud rate of our MCUs
#endif

#define NUM_IMAGES 10 

int main(int argc, char *argv[]) {
	printf("Starting the timer!\\n");
	us_ticker_init();
	uint32_t begin_time = us_ticker_read();
	static float test_image[NUM_IMAGES][%d];
	Tensor *input_tensor; 
	for (int i = 0; i < NUM_IMAGES; i++) {
    	Context ctx;
		input_tensor = new WrappedRamTensor<float>({1, %d}, &(test_image[i][0]));
		get_model_ctx(ctx, input_tensor);
		// printf("Evaluating\\n\\r");
		ctx.eval();
		// S_TENSOR prediction = ctx.get({"y_pred:0"});
		// int result = *(prediction->read<int>(0,0));
	}
	uint32_t end_time = us_ticker_read();
	float fps = (float) ((end_time - begin_time)) / NUM_IMAGES;
	printf("Total microseconds elapsed per inf: %%f\\n", fps);
    return 0;
}
"""

class FullyConnectedTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--param1", default=None, type=int)
        self.parser.add_argument("--param2", default=None, type=int)

    def generate_task(self, output_path, args):
        pass

    def task_name(self):
        return "FullyConnectedTask"

    def get_parser(self):
        return self.parser
    

class ReluTask(Task):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--input-size", required=True, type=int,
                                 help="Input dimension to relu")

    def generate_task(self, output_path, args):
        input_size = args.input_size
        output_folder = Path(output_path) / 'input{}'.format(args.input_size)
        output_folder.mkdir(parents=True, exist_ok=True)
        with tf.Session() as sess:
            x = tf.placeholder(tf.float32, [None, input_size], name='input')
            output = tf.nn.relu(x, name='output')
            _ = output.eval(feed_dict={x: np.random.randn(1, input_size)})
            tf.train.write_graph(sess.graph_def, str(output_folder), 'model.pb',
                                 as_text=False)
        
        # Print out and save our fake main program to file.
        main_file_text = RELU_MAIN_FILE % (input_size, input_size)
        (output_folder / 'main.cpp').write_text(main_file_text)

    def task_name(self):
        return "ReluTask"

    def get_parser(self):
        return self.parser
 

if __name__ == '__main__':
    relu = ReluTask()
    args = relu.parser.parse_args()
    output_folder = Path('artifacts/relu')
    relu.generate_task(str(output_folder), args)
