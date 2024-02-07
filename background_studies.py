import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple


def load_data(file_path: str) -> List[float]:
    """
    Load data from a given file path.

    :param file_path: Path to the data file.
    :return: List of data points as floats.
    """
    with open(file_path, "r") as file:
        data = [float(line.strip()) for line in file]
    return data


def create_histogram_with_error_bars(
    data: List[float], bins: int = 18
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create a histogram with error bars for the given data.

    :param data: List of data points.
    :param bins: Number of bins for the histogram.
    :return: Bin counts, bin edges, and error bars.
    """
    counts, bin_edges, _ = plt.hist(
        data, bins=bins, edgecolor="black", density=True, label="Background"
    )
    # Ensure counts is an ndarray (this should already be the case)
    counts = np.asarray(counts)

    mean_coincid = 0  # Placeholder for mean coincidence value
    adjusted_counts = counts - mean_coincid
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    error = 5 * np.sqrt(adjusted_counts) / np.sqrt(len(data))

    # Ensure error is also returned as an ndarray
    error = np.asarray(error)

    plt.errorbar(
        bin_centers,
        adjusted_counts,
        yerr=[error, error],
        fmt="none",
        ecolor="gray",
        capsize=5,
    )
    return counts, bin_edges, error


def calculate_mean_of_bins(
    counts: np.ndarray, start_bin: int = 2, end_bin: int = 17
) -> float:
    """
    Calculate the mean of a subset of histogram bins.

    :param counts: Array of bin counts.
    :param start_bin: Start index for the bins to include in the mean calculation.
    :param end_bin: End index for the bins to include in the mean calculation.
    :return: Mean of the specified bins.
    """
    subset_sum = np.sum(counts[start_bin:end_bin])
    mean = subset_sum / (end_bin - start_bin)
    return mean


# Load data from file
data_file_path = "data/run_20230126_bckgrd.txt"
data = load_data(data_file_path)

# Create histogram and calculate error bars
counts, bins, error = create_histogram_with_error_bars(data)

print("Mean=", calculate_mean_of_bins(counts))

plt.title("Background distribution")
plt.xlabel("Time (μs)")
plt.ylabel(f"Distribution ({len(data)} events)")
plt.legend()
plt.show()
