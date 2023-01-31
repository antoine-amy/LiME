import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#Open files
with open("data/run_20230117.txt", "r") as data:
    data = [float(x) for x in data.read().split()]
with open("data/run_20230126_bckgrd.txt", "r") as bckgrd:
    bckgrd = [float(x) for x in bckgrd.read().split()]

mean_coincid=0

#define exponential_fit
def exponential_fit(x, a, b):
    return a * np.exp(b * x)

#create the histogram and the error bars
n, bins, patches = plt.hist(data, bins=29, edgecolor='black', density=True)
n=n-mean_coincid
bin_centers = (bins[:-1] + bins[1:]) / 2
#To start at the second bin
#bin_centers=bin_centers[1:]
#n=n[1:]
error = 5*np.sqrt(n)/np.sqrt(len(data))
plt.errorbar(bin_centers, n, yerr=[error, error], fmt='none', ecolor='gray', capsize=5)

#create the fit and the confidence interval
popt, pcov = curve_fit(exponential_fit, bin_centers, n)
x_fit = np.linspace(min(bin_centers), max(bin_centers), 1000)
y_fit = exponential_fit(x_fit, *popt)
y_fit_upper = exponential_fit((x_fit-0.0001-0.078-(x_fit*(5/100))), *(popt + np.sqrt(np.diag(pcov)) * 5)) #errors for x and y are taken into account
y_fit_lower = exponential_fit((x_fit+0.0001+0.078+(x_fit*(5/100))), *(popt - np.sqrt(np.diag(pcov)) * 5))
plt.fill_between(x_fit, y_fit_lower, y_fit_upper, color='red', alpha=0.2)

#plot everything
plt.plot(x_fit, y_fit, 'r', label='Exponential fit')
fit_equation = f"y = {popt[0]:.0f}*exp{{{popt[1]:.3f}t}}"
tau=-1/popt[1]
taubas=-1/(popt[1]-5*np.sqrt(pcov[1,1]))
tauhaut=-1/(popt[1]+5*np.sqrt(pcov[1,1]))
print("τ=",tau,"±",-1/(pcov[1,1]*5),"μs")
print(tauhaut)
print(taubas)
plt.plot(x_fit, y_fit, 'r', label=fit_equation)
num_values = len(data)
plt.annotate(f"Number of values: {num_values}", xy=(0.05, 0.95), xycoords='axes fraction',
             fontsize=14, color='black', horizontalalignment='left', verticalalignment='top')
plt.legend()
plt.show()
