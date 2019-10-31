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
        print(datum)
        print(file)
        sp = datum["sparsity"]
        d[sp] = datum
    return d

def plot_speedup_vs_acc(dlarge, dsmall):
    ddlarge = [(x["accuracy"], x["h2"], x["h1"], x["time_elapsed"], x["sparsity"]) for x in dlarge.values()]
    ddlarge = sorted(ddlarge, key=lambda x:x[4])
    ddsmall = [(x["accuracy"], x["h2"], x["h1"], x["time_elapsed"], x["sparsity"]) for x in dsmall.values()]
    ddsmall = sorted(ddlarge, key=lambda x:x[4])

    baseline_time = ddlarge[0][3]
    speedups = [baseline_time/x[3] for x in ddlarge]
    sparsity = [x[-1] for x in ddlarge]
    accuracies = [x[0] for x in ddlarge]

    baseline_time_small = ddsmall[0][3]
    speedups_small = [baseline_time_small/x[3] for x in ddsmall]
    sparsity_small = [x[-1] for x in ddsmall]
    accuracies_small = [x[0] for x in ddsmall]

    fig, ax = plt.subplots()
    ax.plot(speedups, accuracies, marker="o", label="F767 (large)")
    ax.plot(speedups_small, accuracies_small, marker="o", label="F446 (small)")

    for i, txt in enumerate(sparsity):
        ax.annotate("sparsity="+str(txt), (speedups[i], accuracies[i]))

    plt.xlabel("Speedup")
    plt.ylabel("Test Accuracy")
    plt.title("MNIST 2 Layer FC Accuracy vs Time (h1=8, h2=64)")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("MnistCompleteSparsity.png")

def plot_sparsity_vs_speedup(dlarge, dsmall):
    plt.cla()
    ddlarge = [(x["accuracy"], x["h2"], x["h1"], x["time_elapsed"], x["sparsity"]) for x in dlarge.values()]
    ddlarge = sorted(ddlarge, key=lambda x:x[4])
    ddsmall = [(x["accuracy"], x["h2"], x["h1"], x["time_elapsed"], x["sparsity"]) for x in dsmall.values()]
    ddsmall = sorted(ddlarge, key=lambda x:x[4])

    baseline_time = ddlarge[0][3]
    speedups = [baseline_time/x[3] for x in ddlarge]
    sparsity = [x[-1] for x in ddlarge]
    accuracies = [x[0] for x in ddlarge]    

    baseline_time_small = ddsmall[0][3]
    speedups_small = [baseline_time_small/x[3] for x in ddsmall]
    sparsity_small = [x[-1] for x in ddsmall]
    accuracies_small = [x[0] for x in ddsmall]    

    ideal_speedups = [100/(100-x) for x in sparsity]

    cpu_times = [0.172852,0.125977,0.092041,0.067871,0.059082,0.021973]
    cpu_baseline = cpu_times[0]
    cpu_speedups = [cpu_baseline/x for x in cpu_times]
    
    fig, ax = plt.subplots()
    ax.plot(sparsity, speedups, marker="o", label="F767 (large)")
    ax.plot(sparsity, speedups_small, marker="o", label="F446 (small)")
    ax.plot(sparsity, ideal_speedups, marker="x", label="ideal")
    ax.plot(sparsity, cpu_speedups, marker="x", label="CPU")

    for i, txt in enumerate(sparsity):
        ax.annotate("sparsity="+str(txt), (sparsity[i], speedups[i]))

    plt.ylabel("Speedup")
    plt.xlabel("Sparsity")
    plt.title("MNIST 2 Layer FC Speedup vs Sparsity Comparison (h1=8, h2=64)")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("MnistCompleteSparsityVsSpeedup.png")

d_large = load_data(sys.argv[1])
d_small = load_data(sys.argv[2])
plot_speedup_vs_acc(d_large, d_small)
plot_sparsity_vs_speedup(d_large, d_small)

