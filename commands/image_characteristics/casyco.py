import numpy as np
from utils.compute_histogram import compute_histogram
from utils.extract_channel import extract_channel
def do_casyco(image: np.ndarray, args:dict[str, str]) -> float:
    ch = args.get('-channel', 'y')
    image = extract_channel(image, channel=ch)
    h, cdf, n = compute_histogram(image)
    if n == 0:
        return float("nan")
    m = np.arange(256, dtype=np.float64)
    s1 = float(np.sum(h * m))
    s2 = float(np.sum(h * (m ** 2)))
    s3 = float(np.sum(h * (m ** 3)))
    mean = s1 / n
    var = (s2 / n) - (mean ** 2)
    sigma = np.sqrt(var)

    ex3 = s3 / n
    ex2 = s2 / n
    y = ex3 - 3.00 * mean * ex2 + 2.00 * (mean ** 3)
    if sigma == 0:
        return float("nan")
    
    casyco = y / (sigma ** 3)
    return float(casyco)