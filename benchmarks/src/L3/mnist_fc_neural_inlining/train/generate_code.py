# TODO: 8 bit quantization

import sys
import pickle 

def generate_inlined(d):
    d = {k:v.T for k,v in d.items()}

    W_1_flattened = (d["W_1"]).flatten()
    W_2_flattened = (d["W_2"]).flatten()
    W_3_flattened = (d["W_3"]).flatten()
    b_1_flattened = (d["b_1"]).flatten()
    b_2_flattened = (d["b_2"]).flatten()
    b_3_flattened = (d["b_3"]).flatten()

    HIDDEN1 = d["W_1"].shape[0]
    INPUT_SHAPE = d["W_1"].shape[1]
    HIDDEN2 = d["W_2"].shape[1]
    OUTPUT_SHAPE = 10

    string = """
        float *o1 = (float *)malloc(sizeof(float) * {{HIDDEN1}}*10);
        float *o2 = (float *)malloc(sizeof(float) * {{HIDDEN2}}*10);
        memset(o1, 0, sizeof(float)*{{HIDDEN1}});
        memset(o2, 0, sizeof(float)*{{HIDDEN2}});
    """
    string = string.replace("{{HIDDEN1}}", str(HIDDEN1))
    string = string.replace("{{HIDDEN2}}", str(HIDDEN2))
    
    for i in range(HIDDEN1):
        sum_string = ""
        for j in range(INPUT_SHAPE):
            if W_1_flattened[i*INPUT_SHAPE+j] != 0:
                if j  != 0:
                    sum_string += " + "
                sum_string += "(%f) * (in[%d]) " % (W_1_flattened[i*INPUT_SHAPE+j], j)
        if sum_string != "":
            string += "o1[%d] += %s;\n" % (i, sum_string)

    for i in range(HIDDEN1):
        string += "o1[%d] += %d;\n" % (i, b_1_flattened[i])
        string += "o1[%d] = o1[%d] < 0 ? 0 : o1[%d];\n" % (i, i, i)

    for i in range(HIDDEN2):
        sum_string = ""
        for j in range(HIDDEN1):
            if W_2_flattened[i*HIDDEN1+j] != 0:
                if j != 0:
                    sum_string += " + "
                sum_string += "(%f) * (o1[%d]) " % (W_2_flattened[i*HIDDEN1+j], j)
        if sum_string != "":
            string += "o2[%d] += %s;\n" % (i, sum_string)

    for i in range(HIDDEN2):
        string += "o2[%d] += %d;\n" % (i, b_2_flattened[i])
        string += "o2[%d] = o2[%d] < 0 ? 0 : o2[%d];\n" % (i, i, i)

    for i in range(OUTPUT_SHAPE):
        sum_string = ""
        for j in range(HIDDEN2):
            if W_3_flattened[i*HIDDEN2+j] != 0:
                if j != 0:
                    sum_string += " + "
                sum_string += "(%f) * (o2[%d]) " % (W_3_flattened[i*HIDDEN2+j], j)
        if sum_string != "":
            string += "out[%d] += %s;\n" % (i, sum_string)

    for i in range(OUTPUT_SHAPE):
        string += "out[%d] += %d;\n" % (i, b_3_flattened[i])

    return """
        #include <stdio.h>
        #include <stdlib.h>
        #include <string.h>
        inline void inference_inlined(float *in, float *out) {
            %s
        }
    """ % string

def generate_baseline(d):

    d = {k:v.T for k,v in d.items()}

    W_1_flattened = d["W_1"].flatten()
    W_2_flattened = d["W_2"].flatten()
    W_3_flattened = d["W_3"].flatten()
    b_1_flattened = d["b_1"].flatten()
    b_2_flattened = d["b_2"].flatten()
    b_3_flattened = d["b_3"].flatten()
    W_1_string = "const float W_1[%d] = {%s}" % (W_1_flattened.shape[0], ",".join([str(x) for x in W_1_flattened])) + ";"
    W_2_string = "const float W_2[%d] = {%s}" % (W_2_flattened.shape[0],",".join([str(x) for x in W_2_flattened])) + ";"
    W_3_string = "const float W_3[%d] = {%s}" % (W_3_flattened.shape[0],",".join([str(x) for x in W_3_flattened])) + ";"
    b_1_string = "const float b_1[%d] = {%s}" % (b_1_flattened.shape[0],",".join([str(x) for x in b_1_flattened])) + ";"
    b_2_string = "const float b_2[%d] = {%s}" % (b_2_flattened.shape[0],",".join([str(x) for x in b_2_flattened])) + ";"
    b_3_string = "const float b_3[%d] = {%s}" % (b_3_flattened.shape[0],",".join([str(x) for x in b_3_flattened])) + ";"
    
    string = """
        %s
        %s
        %s
        %s
        %s
        %s
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    void inference_baseline(float *in, float *out) {
        float o1[{{HIDDEN1}}], o2[{{HIDDEN2}}];
        //memset(o1, 0, sizeof(float)*{{HIDDEN1}});
        //memset(o2, 0, sizeof(float)*{{HIDDEN2}});
        for (int i = 0; i < {{HIDDEN1}}; i++) {
            for (int j = 0; j < {{INPUT_SHAPE}}; j++) {
                o1[i] += W_1[i*{{INPUT_SHAPE}}+j] * in[j];
            }
        }
        for (int i = 0; i < {{HIDDEN1}}; i++) {
            o1[i] += b_1[i];
            o1[i] = o1[i] < 0 ? 0 : o1[i];
        }
        for (int i = 0; i < {{HIDDEN2}}; i++) {
            for (int j = 0; j < {{HIDDEN1}}; j++) {
                o2[i] += W_2[i*{{HIDDEN1}}+j] * o1[j];
            }
        }
        for (int i = 0; i < {{HIDDEN2}}; i++) {
            o2[i] += b_2[i];
            o2[i] = o2[i] < 0 ? 0 : o2[i];
        }
        for (int i = 0; i < {{OUTPUT_SHAPE}}; i++) {
            for (int j = 0; j < {{HIDDEN2}}; j++) {
                out[i] += W_3[i*{{HIDDEN2}}+j] * o2[j];
            }
        }
        for (int i = 0; i < {{OUTPUT_SHAPE}}; i++) {
           out[i] += b_3[i];
        }
    }
    """ % (W_1_string, W_2_string, W_3_string, b_1_string, b_2_string, b_3_string)
    
    string = string.replace("{{INPUT_SHAPE}}", str(d["W_1"].shape[1]))
    string = string.replace("{{HIDDEN1}}", str(d["W_1"].shape[0]))
    string = string.replace("{{HIDDEN2}}", str(d["W_2"].shape[0]))
    string = string.replace("{{OUTPUT_SHAPE}}", str(10))

    return string
    
with open("weights", "rb") as f:
    d = pickle.load(f)

print(generate_baseline(d))
print(generate_inlined(d))
