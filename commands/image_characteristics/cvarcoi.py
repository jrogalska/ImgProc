import numpy as np
from utils.compute_histogram import compute_histogram
from utils.extract_channel import extract_channel

_EPS = 1e-12  # osłona na mean≈0 i szum numeryczny

def do_cvarcoi(image: np.ndarray, args: dict[str, str]) -> float:
    """
    Variation coefficient I: sigma / mean
    Liczone z jednego histogramu (wariancja populacyjna).
    """
    ch = (args.get("-channel", "y") or "y").lower()

    image = extract_channel(image, channel=ch)
    h, cdf, n = compute_histogram(image)
    if n == 0:
        return float("nan")

    h = h.astype(np.float64, copy=False)
    m = np.arange(h.size, dtype=np.float64)

    s1 = (m * h).sum()         # Σ m H(m)
    s2 = (m * m * h).sum()     # Σ m^2 H(m)

    mean = s1 / n
    var  = s2 / n - mean * mean  # E[X^2] - (E[X])^2

    if var < 0 and var > -1e-12:
        var = 0.0

    sigma = np.sqrt(var)
    bz = sigma / (abs(mean) + _EPS)  # CV = sigma/mean

    return float(bz)
