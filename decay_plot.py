import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#define exponential_fit
def exponential_fit(x, a, b):
    return a * np.exp(b * x)

#Open files
with open("data/run_20230117.txt", "r") as data:
    data = [float(x) for x in data.read().split()]
with open("data/run_20230126_bckgrd.txt", "r") as bckgrd:
    bckgrd = [float(x) for x in bckgrd.read().split()]

mean_coincid=0.0 #0.006295208412458375
diff=10000000000


#get the best number of bins
plt.style.use('seaborn')
for x in range(10,40):
    n, bins, patches = plt.hist(data, bins=x, edgecolor='white', alpha=0, histtype='step', density=True)
    n=n-mean_coincid
    bin_centers = (bins[:-1] + bins[1:]) / 2
    #To start at the second bin
    #bin_centers=bin_centers[1:]
    #n=n[1:]

    popt, pcov = curve_fit(exponential_fit, bin_centers, n)
    x_fit = np.linspace(min(bin_centers), max(bin_centers), 1000)
    y_fit_upper = exponential_fit((x_fit-0.0001-0.078-(x_fit*(5/100))), *(popt + np.sqrt(np.diag(pcov)) * 5)) #errors for x and y are taken into account
    y_fit_lower = exponential_fit((x_fit+0.0001+0.078+(x_fit*(5/100))), *(popt - np.sqrt(np.diag(pcov)) * 5))

    tau=-1/popt[1]; taubas=-1/(popt[1]-5*np.sqrt(pcov[1,1])); tauhaut=-1/(popt[1]+5*np.sqrt(pcov[1,1]))
    if tauhaut-taubas<diff:
        diff=tauhaut-taubas
        bin_nbr=x
    
x=bin_nbr
n, bins, patches = plt.hist(data, bins=x, edgecolor='black', histtype='step', density=True)
print(bins)
print(n)
n=n-mean_coincid
bin_centers = (bins[:-1] + bins[1:]) / 2
#diff=plt.step(bins, n) 

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
plt.plot(x_fit, y_fit, 'r', label='Exponential fit (5σ CI)')
fit_equation = f"y = {popt[0]:.0f}*exp{{{popt[1]:.3f}t}}"
tau=-1/popt[1]
taubas=-1/(popt[1]-5*np.sqrt(pcov[1,1]))
tauhaut=-1/(popt[1]+5*np.sqrt(pcov[1,1]))


#plt.plot(x_fit, y_fit, 'r', label=fit_equation) #show equation of fit
num_values = len(data)
plt.annotate(f'τ={round(tau,3)}$_{{-{round(tau-taubas,3)}}}^{{+{round(tauhaut-tau,3)}}}$ μs', xy=(0.95, 0.80), xycoords='axes fraction',
             fontsize=14, color='black', horizontalalignment='right', verticalalignment='top')

plt.title(r'Muon decay distribution')
plt.xlabel(r'Decay time (μs)')
plt.ylabel(f'Normalized distribution ({num_values} events)')
print("x=",x)
print(taubas)
print(tauhaut)
print(n)
plt.legend()
plt.show()
