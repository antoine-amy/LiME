import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# Define exponential fit function
def exponential_fit(time: np.ndarray, amplitude: float, rate: float) -> np.ndarray:
    return amplitude * np.exp(rate * time)


# Load data from files
def load_data(file_path: str) -> list:
    with open(file_path, "r") as file:
        return [float(value) for value in file.read().split()]


data = load_data("data/run_20230117.txt")
background_data = load_data("data/run_20230126_bckgrd.txt")

mean_background = 0.0  # Adjust if necessary from background studies
best_difference = 1e10
best_bin_number = 0

# plt.style.use("seaborn")
for bin_count in range(10, 40):
    counts, bin_edges = np.histogram(data, bins=bin_count, density=True)
    counts -= mean_background
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    popt, pcov = curve_fit(exponential_fit, bin_centers, counts)
    tau = -1 / popt[1]
    tau_lower = -1 / (popt[1] - 5 * np.sqrt(pcov[1, 1]))
    tau_upper = -1 / (popt[1] + 5 * np.sqrt(pcov[1, 1]))
    difference = tau_upper - tau_lower

    if difference < best_difference:
        best_difference = difference
        best_bin_number = bin_count

# Final histogram with the best number of bins
counts, bin_edges = np.histogram(data, bins=best_bin_number, density=True)
counts -= mean_background
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
errors = 5 * np.sqrt(counts) / np.sqrt(len(data))

# Error bars
plt.errorbar(
    bin_centers, counts, yerr=[errors, errors], fmt="none", ecolor="gray", capsize=5
)

# Fit and confidence interval
popt, pcov = curve_fit(exponential_fit, bin_centers, counts)
time_fit = np.linspace(min(bin_centers), max(bin_centers), 1000)
fit_values = exponential_fit(time_fit, *popt)
fit_upper = exponential_fit(
    time_fit - 0.0001 - 0.078 - (time_fit * 0.05), *(popt + np.sqrt(np.diag(pcov)) * 5)
)
fit_lower = exponential_fit(
    time_fit + 0.0001 + 0.078 + (time_fit * 0.05), *(popt - np.sqrt(np.diag(pcov)) * 5)
)

plt.fill_between(time_fit, fit_lower, fit_upper, color="red", alpha=0.2)
plt.plot(time_fit, fit_values, "r", label="Exponential fit (5σ CI)")

# Tau calculations
tau = -1 / popt[1]
tau_lower_bound = -1 / (popt[1] - 5 * np.sqrt(pcov[1, 1]))
tau_upper_bound = -1 / (popt[1] + 5 * np.sqrt(pcov[1, 1]))

# Annotations and labels
plt.annotate(
    f"τ={tau:.3f}$_{{-{tau - tau_lower_bound:.3f}}}^{{+{tau_upper_bound - tau:.3f}}}$ μs",
    xy=(0.95, 0.80),
    xycoords="axes fraction",
    fontsize=14,
    color="black",
    horizontalalignment="right",
    verticalalignment="top",
)

plt.title("Muon decay distribution")
plt.xlabel("Decay time (μs)")
plt.ylabel(f"Normalized distribution ({len(data)} events)")

plt.legend()
plt.show()

print(f"Optimal number of bins: {best_bin_number}")
print(f"Tau lower bound: {tau_lower_bound}")
print(f"Tau upper bound: {tau_upper_bound}")
