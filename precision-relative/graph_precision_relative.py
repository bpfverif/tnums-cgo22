import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import argparse
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches

palette = plt.get_cmap('Set1')
mp.rcParams['figure.autolayout'] = True
mp.rcParams['font.size'] = 12

def log2cdf(data):
	# y = P(imprecision < x)
	data = np.log2(data)
	n = len(data)
	x = np.sort(data) # sort data
	y = np.arange(1, n + 1) / n # calculate cumulative probability
	return x, y

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--bitwidth", help="bitvector width", type=int, 
		required=True)
	parser.add_argument("--infile1", help="input file", type=str, 
		required=True)
	parser.add_argument("--infile2", help="input file", type=str, 
		required=True)
	parser.add_argument("--outfile", help="output file", type=str, 
		required=True)
	parser.add_argument("--op1", help="op1", type=str, 
		required=True)
	parser.add_argument("--op2", help="op2", type=str, 
		required=True)
	parser.add_argument("--op", help="op", type=str, 
		required=True)

	args=parser.parse_args()

	args.op1 = args.op1.replace("_", "\\_")
	args.op2 = args.op2.replace("_", "\\_")
	args.op = args.op.replace("_", "\\_")

	data1 = np.loadtxt(open(args.infile1).readlines()[:-3], delimiter=",", skiprows=1)
	data2 = np.loadtxt(open(args.infile2).readlines()[:-3], delimiter=",", skiprows=1)

	fig = plt.figure(1)
	axis = fig.add_subplot(111)

	legend_label = "$\\bf{bitwidth:}$" + " " + "$\\bf{8}$"+ " " +"$\\bf{(exhaustive)}$"

	# labeling
	data1_label = "$log_{{2}} \\frac{{\\vert{{}} {0} \\vert{{}} }}{{\\vert{{}} {{{1}}} \\vert{{}} }}$".format(
		args.op1, args.op)
	data2_label = "$log_{{2}} \\frac{{\\vert{{}} {0} \\vert{{}} }}{{\\vert{{}} {{{1}}} \\vert{{}} }}$".format(
		args.op2, args.op)
	x_label =\
	"$log_{{2}} \\frac{{\\vert{{}} {0} \\vert{{}} }}{{\\vert{{}} {{{1}}} \\vert{{}} }}$".format(
		args.op1, args.op)
	x_label += "  OR   "
	x_label +=\
	"$log_{{2}} \\frac{{\\vert{{}} {0} \\vert{{}} }}{{\\vert{{}} {{{1}}} \\vert{{}} }}$".format(
		args.op2, args.op)

	# plot
	x1, y1 = log2cdf(data1)           
	x2, y2 = log2cdf(data2)           
	axis.plot(x1, y1, 
		label = data1_label, marker='', linewidth=3, 
		color = "black",
		linestyle = "dotted", alpha = 1)
	axis.plot(x2, y2, 
		label = data2_label, marker='', linewidth=3, 
		color = "black",
		linestyle = "solid", alpha=0.5)

	# axis.set_xlabel(x_label, fontsize = 15)
	axis.set_ylabel("probability (at or below value)")
	axis.grid()
	axis.legend(title=legend_label, prop={'size': 15})
	fig.tight_layout()
	plt.savefig("./{}".format(args.outfile), dpi=300)