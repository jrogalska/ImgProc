import numpy as np
# this function computes the histogram of a given image channel
def compute_histogram(img: np.ndarray,  num_bins: int = 256) -> tuple[np.ndarray, np.ndarray, int]:

    if img.ndim != 2:
        raise ValueError("Input must be a 2D array representing a single image channel.")
    h = np.bincount(img.ravel(), minlength=num_bins).astype(np.int64) #zlicza wystąpienia wartości pikseli
    h = h[:num_bins]  # histogram ma mieć dokładnie num_bins elementów
    cdf = np.cumsum(h) # skumulowana suma histogramu
    n = int(h.sum()) # całkowita liczba pikseli
    cdf = cdf/n if n > 0 else cdf # normalizacja CDF
    return h, cdf, n