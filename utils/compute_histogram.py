import numpy as np
# this function computes the histogram of a given image channel
def compute_histogram(img: np.ndarray,  num_bins: int = 256) -> tuple[np.ndarray, np.ndarray, int]:
    """
    Computes the histogram of the given image channel (2D numpy array).
    Args:
        img (np.ndarray): 2D array representing the image channel.
        num_bins (int): Number of bins for the histogram (default is 256).
    Returns:
        tuple[np.ndarray, np.ndarray, int]: A tuple containing:
            - h (np.ndarray): Histogram array of shape (num_bins,).
            - cdf (np.ndarray): Cumulative distribution function array of shape (num_bins,).
            - n (int): Total number of pixels in the channel.
    """
    if img.ndim != 2:
        raise ValueError("Input must be a 2D array representing a single image channel.")
    h = np.bincount(img.ravel(), minlength=num_bins).astype(np.int64) #zlicza wystąpienia wartości pikseli
    h = h[:num_bins]  # histogram ma mieć dokładnie num_bins elementów
    cdf = np.cumsum(h) # skumulowana suma histogramu
    n = int(h.sum()) # całkowita liczba pikseli
    cdf = cdf/n if n > 0 else cdf # normalizacja CDF
    return h, cdf, n