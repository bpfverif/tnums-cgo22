import matplotlib as mp
import matplotlib.pyplot as pyplot
import numpy as np
import sys
import os
import argparse
from collections import OrderedDict
from scipy.interpolate import interp1d

palette = mp.pyplot.get_cmap('Set1')
mp.rcParams['figure.autolayout'] = True
mp.rcParams['font.size'] = 12
fp = "./perf_{}.log"

# '-'       solid line style
# '--'      dashed line style
# '-.'      dash-dot line style
# ':'       dotted line style

ops = OrderedDict([
    ("kern_mul", ["kern_mul", "-", "black", 0.5]), 
    ("bitwise_mul_opt", ["bitwise_mul", ":", "black", 1]), 
    ("our_mul", ["our_mul", "--", "black", 1])
    ])

kern_avg = 0

def cdf(data):
    # y = P(imprecision < x)
    n = len(data)
    x = np.sort(data) # sort data
    y = np.arange(1, n + 1) / n # calculate cumulative probability
    return x, y

def plot_cdf_data(op, op_data, axis, linestyle):
    global kern_avg
    if not hasattr(plot_cdf_data, "coloridx"):
        plot_cdf_data.coloridx = 1

    avg = np.mean(op_data)
    if op == "kern_mul":
        kern_avg = avg
    print(op, avg)
    
    x, y = cdf(op_data)
    axis.plot(x, y, 
        label = "{}".format(ops[op][0]), 
        linestyle=ops[op][1],
        color=ops[op][2],
        alpha=ops[op][3], 
        linewidth=3
    )
    plot_cdf_data.coloridx+=1

if __name__ == "__main__":
    data_ops = {}
    for op in ops:
        f = fp.format(op)
        data = np.loadtxt(f, delimiter=",", skiprows=1)
        data_ops[op] = data

    # fix the xlimit of graph at the 99th percentile
    # xmax = max(np.percentile(data_ops["kern"], 99), 
    #     np.percentile(data_ops["ppr"], 99),
    #     np.percentile(data_ops["sr"], 99),
    #     np.percentile(data_ops["popcnt"], 99))
    
    # xmin = min(np.percentile(data_ops["kern"], 1), 
    #     np.percentile(data_ops["ppr"], 1),
    #     np.percentile(data_ops["sr"], 1),
    #     np.percentile(data_ops["popcnt"], 1))

    fig = mp.pyplot.figure(1)
    axis = fig.add_subplot(111)

    for op in data_ops:
        plot_cdf_data(op, data_ops[op], axis, "solid")

    # # plot kern mul
    # plot_cdf_data("kern", data_ops["kern"], axis, "solid")

    # # plot ppr
    # plot_cdf_data("ppr", data_ops["ppr"], axis, "solid")

    # # plot sr
    # plot_cdf_data("sr", data_ops["sr"], axis, "solid")

    # # plot popcount
    # plot_cdf_data("popcnt", data_ops["popcnt"], axis, "solid")

    # # plot popcount
    # plot_cdf_data("choose", data_ops["choose"], axis, "solid")


    """ settings """
    legend_label = "$\\bf{bitwidth:}$" +\
            " " + "$\\bf{64}$"+ " " +"$\\bf{(sampling)}$"

    axis.grid(b=True, which='both', color='silver')
    axis.set_xlabel("number of cycles (min)")
    axis.set_ylabel("probability (at or below value)")
    # axis.set_xscale('log')
    axis.set_xticks(np.array([200, 300, 400, 500, 600, 700, 800, 900]))
    axis.set_xticklabels(np.array([200, 300, 400, 500, 600, 700, 800, 900]))
    axis.legend(title=legend_label)

    # pyplot.xlim(right=xmax)
    mp.pyplot.savefig("./perf_fig.png", dpi=300)
