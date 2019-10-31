import matplotlib.pyplot as plt
import sys
import json
import glob
import numpy as np

def load_data_individual(f):
    with open(f, "r") as ff:
        return json.load(ff)

def load_data(p):
    json_files = glob.glob("%s/*json" % p)
    d = {}
    for file in json_files:
        datum = load_data_individual(file)
        (h1, h2) = datum["h2"], datum["h1"]

        # Calculate flops
        flops = 784 * h1 + h2 * h1
        datum["flops"] = flops

        d[(h1, h2)] = datum
    return d

def plot_time_vs_acc(d):
    flops_accs_h1_h2 = [(x["flops"], x["accuracy"], x["h2"], x["h1"], x["time_elapsed"]) for x in d.values()]
    flops = [x[0] for x in flops_accs_h1_h2]
    time = [x[4] for x in flops_accs_h1_h2]
    accs = [x[1] for x in flops_accs_h1_h2]
    dims = [(x[2],x[3]) for x in flops_accs_h1_h2]

    fig, ax = plt.subplots()
    ax.scatter(time, accs)

    for i, txt in enumerate(dims):
        ax.annotate(str(txt), (time[i], accs[i]))

    plt.xlabel("Inference Time (s)")
    plt.ylabel("Test Accuracy")
    plt.title("MNIST 2 Layer FC Accuracy vs Time (h1 size, h2 size)")
    plt.tight_layout()
    plt.savefig("MnistComplete.png")

def plot_time_vs_flop(d):
    flops_accs_h1_h2 = [(x["flops"], x["accuracy"], x["h2"], x["h1"], x["time_elapsed"]) for x in d.values()]
    flops = [x[0] for x in flops_accs_h1_h2]
    time = [x[4] for x in flops_accs_h1_h2]
    accs = [x[1] for x in flops_accs_h1_h2]
    dims = [(x[2],x[3]) for x in flops_accs_h1_h2]

    fig, ax = plt.subplots()
    ax.scatter(flops, accs)

    for i, txt in enumerate(dims):
        ax.annotate(str(txt), (flops[i], accs[i]))

    plt.xlabel("# FLOP")
    plt.ylabel("Test Accuracy")
    plt.title("MNIST 2 Layer FC Accuracy vs FLOP (h1 size, h2 size)")
    plt.tight_layout()
    plt.savefig("MnistCompleteAccVsFLOP.png")

def plot_avg_energy_vs_acc(d):
    flops_accs_h1_h2 = [(x["flops"], x["accuracy"], x["h2"], x["h1"], x["time_elapsed"], x["avg_power"]) for x in d.values()]
    energy = [x[4]*x[5] for x in flops_accs_h1_h2]
    accs = [x[1] for x in flops_accs_h1_h2]
    dims = [(x[2],x[3]) for x in flops_accs_h1_h2]

    fig, ax = plt.subplots()
    ax.scatter(energy, accs)

    for i, txt in enumerate(dims):
        ax.annotate(str(txt), (energy[i], accs[i]))
        
    plt.xlabel("Avg Energy (avg power * time)")
    plt.ylabel("Test Accuracy")
    plt.title("MNIST 2 Layer FC Avg Energy vs Acc (h1 size, h2 size)")
    plt.tight_layout()
    plt.savefig("MnistCompleteEnergyVsAcc.png")    

d = load_data(sys.argv[1])
plot_time_vs_acc(d)
plot_time_vs_flop(d)
plot_avg_energy_vs_acc(d)
