import matplotlib as mp
import matplotlib.pyplot as pyplot
import numpy as np
from collections import OrderedDict
from scipy.interpolate import interp1d

palette = mp.pyplot.get_cmap('Set1')
mp.rcParams['figure.autolayout'] = True
mp.rcParams['font.size'] = 12

# A map from 
# <tnum_op> : [<tnum op name in graph>, <graph line style>, <graph line color>, <graph line transparency>]
ops = OrderedDict([
	("kern_mul", ["kern_mul", "-", "black", 0.5]), 
	("bitwise_mul_opt", ["bitwise_mul", ":", "black", 1]), 
	("our_mul", ["our_mul", "--", "black", 1])
	])

# ensure that output files are named perf_<op>.log
fp = "./perf_{}.log"

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

	# fix the xlimit of graph at the 99th and 1st percentile
	xmax = max(np.percentile(data_ops["kern_mul"], 99.9), 
	    np.percentile(data_ops["bitwise_mul_opt"], 99.9),
	    np.percentile(data_ops["our_mul"], 99.9))
	xmin = min(np.percentile(data_ops["kern_mul"], 0.1), 
	    np.percentile(data_ops["bitwise_mul_opt"], 0.1),
	    np.percentile(data_ops["our_mul"], 0.1))

	fig = mp.pyplot.figure(1)
	axis = fig.add_subplot(111)

	for op in data_ops:
		# plot ops one-by-one
		plot_cdf_data(op, data_ops[op], axis, "solid")

	legend_label = "$\\bf{bitwidth:}$" +\
			" " + "$\\bf{64}$"+ " " +"$\\bf{(sampling)}$"
	axis.grid(b=True, which='both', color='silver')
	axis.set_xlabel("number of cycles (min)")
	axis.set_ylabel("probability (at or below value)")
	# axis.set_xscale('log')
	# axis.set_xticks(np.array([200, 300, 400, 500, 600, 700, 800, 900]))
	# axis.set_xticklabels(np.array([200, 300, 400, 500, 600, 700, 800, 900]))
	axis.legend(title=legend_label)
	pyplot.xlim(right=xmax)
	pyplot.xlim(left=xmin)
	mp.pyplot.savefig("./perf_fig.png", dpi=300)
