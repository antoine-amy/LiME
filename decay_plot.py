import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Read data from file
data = np.genfromtxt('run_20230117.txt')
# Create histogram
n, bins, patches=plt.hist(data, bins=29, density=False)

# calculate standard deviation of the data
std_dev = np.std(data)
# create error bars with standard deviation
error = std_dev * np.ones_like(n)

# Define exponential function
def exponential_func(x, a, b, c):
    return a*np.exp(-b*x) + c
# Fit exponential function to histogram
popt, pcov = curve_fit(exponential_func, bins[:-1], n)

# Create string representation of equation
equation='y={:.2f}*exp(-{:.2f}t)+{:.2f}'.format(*popt)
tau="τ=",round(1/popt[1],2)

# Plot histogram and fitted function with error bars
plt.plot(bins[:-1], exponential_func(bins[:-1], *popt), 'r-', label='fit')
plt.errorbar(bins[:-1], n, yerr=error, fmt='o', label='data')
plt.legend()
plt.text(0.4,0.8,equation, transform=plt.gca().transAxes)
plt.text(0.4,0.7,tau, transform=plt.gca().transAxes)
plt.show()