import sys
import matplotlib.pyplot as plt
import glob
import json

def insert_AI_and_flops(x):
    #nfloats = min(float(x["NFLOPS"])*2, float(x["NFLOATS"]))
    nfloats = x["NFLOATS"]
    arithmetic_intensity = float(x["AI"])
    print(arithmetic_intensity)
    flops_seconds = float(x["FLOP"]) / float(x["time_elapsed"])
    retval = dict(x)
    retval["ai"] = arithmetic_intensity
    retval["flops_seconds"] = flops_seconds
    return retval

filenames = glob.glob("arithmetic_intensity_output/*")

data = []
for f in filenames:
    print(f)
    try:
        with open(f, "r") as fr:
            data.append(json.load(fr))
    except:
        pass

data = [insert_AI_and_flops(x) for x in data]

by_floats = {}
for d in data:
    nfloats = d["NFLOATS"]
    if nfloats not in by_floats:        
        by_floats[nfloats] = []
    by_floats[nfloats].append(d)

for nfloats, data in by_floats.items():
    print(nfloats)
    set_size = nfloats*8
    data = sorted(data, key=lambda x: float(x["ai"]))
    xs = [x["ai"] for x in data]
    ys = [x["flops_seconds"] for x in data]
    plt.plot(xs, ys, label="working-set-size=%d bytes" % set_size, marker="o")

plt.legend(loc="best")
plt.xscale("log", basex=2)
plt.yscale("log", basey=2)
plt.xlabel("Arithmetic Intensity")
plt.ylabel("INTOPS")
plt.savefig("roofline.png")


