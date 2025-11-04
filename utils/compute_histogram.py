import numpy as np
# this function computes the histogram of a given image channel
def compute_histogram(img: np.ndarray, channel: str, num_bins: int = 256) -> tuple[np.ndarray, np.ndarray, int]:
    if img.ndim != 2:
        raise ValueError("Input must be a 2D array representing a single image channel.")
    h = np.bincount(img.ravel(), minlength=num_bins).astype(np.int64)
    cdf = np.cumsum(h)
    n = int(h.sum())
    return h, cdf, n