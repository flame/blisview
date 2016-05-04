# BLIS Performance graphs project
# The University of Texas at Austin
# Author(s): Barrett Hinson

import matplotlib.pyplot as plt
import numpy as np

# this file can be sued to manually generate the graphs and is just a general hands on test tool
def create_test_files(name):
	results_file = open("static/graph/blis/testsuite/"+str(name)+".m", "r")
	x = [0]
	y = [0]
	peak = [59.2]
	for line in results_file:
		if "%" not in line:
			lineP = line.split()
			if len(lineP) > 0 and "blis" in lineP[0]:
				x.append(float(lineP[1]))
				y.append(float(lineP[4]))
				peak.append(59.2)
	performance, = plt.plot(x, y, "g-", linewidth=2.0, label = "Performance")
	peak, = plt.plot(x, peak, "r--", linewidth=2.0, label = "Theoretical Peak")
	plt.xlabel("Problem Size (m = n = k)")
	plt.ylabel("GFLOPS")
	plt.grid()
	plt.legend(loc=4)
	plt.savefig(str(name)+".png", dpi=70)
	plt.close()
	results_file.close()
	

create_test_files(10)
