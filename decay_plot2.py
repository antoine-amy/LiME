import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#Open files
with open("data/run_20230126_bckgrd.txt", "r") as data:
    data = [float(x)*10 for x in data.read().split() if float(x) > 1.395]
#22.11 pour 99% de muon désintegre
mean_coincid=0

#create the histogram and the error bars
n, bins, patches = plt.hist(data, bins=9, edgecolor='black', density=True)
n=n-mean_coincid
bin_centers = (bins[:-1] + bins[1:]) / 2
#To start at the second bin
#bin_centers=bin_centers[1:]
#n=n[1:]
error = 5*np.sqrt(n)/np.sqrt(len(data))
plt.errorbar(bin_centers, n, yerr=[error, error], fmt='none', ecolor='gray', capsize=5)

#plot everything
num_values = len(data)
plt.annotate(f"Number of values: {num_values}", xy=(0.05, 0.95), xycoords='axes fraction',
             fontsize=14, color='black', horizontalalignment='left', verticalalignment='top')
plt.legend()
plt.show()
