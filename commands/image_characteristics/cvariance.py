import numpy as np
from utils.compute_histogram import compute_histogram
from utils.extract_channel import extract_channel


def do_cvariance(image: np.ndarray, args:dict[str, str]) -> float:
    ch = args.get('-channel', 'y')
    image = extract_channel(image, channel=ch)

    h, cdf, n = compute_histogram(image)
    if n == 0:
        return float("nan")
    m = np.arange(256, dtype=np.float64)
    s1 = float(np.sum(h * m)) 
    s2 = float(np.sum(h * (m ** 2))) 

    mean = s1 / n
    variance = (s2 / n) - (mean ** 2)

    return float(variance)
