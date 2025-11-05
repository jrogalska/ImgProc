import numpy as np
from utils.compute_histogram import compute_histogram
from utils.extract_channel import extract_channel


def do_cflattening(image, args:dict[str, str]) :
    ch = args.get('-channel', 'y')
    image = extract_channel(image, channel=ch)
    h, cdf, n = compute_histogram(image)
    if n == 0:
        return float("nan")
    m = np.arange(256, dtype=np.float64)
    s1 = float(np.sum(h * m))
    s2 = float(np.sum(h * (m ** 2)))
    s3 = float(np.sum(h * (m ** 3)))
    s4 = float(np.sum(h * (m ** 4)))

    mean = s1 / n
    ex2 = s2 / n
    ex3 = s3 / n
    ex4 = s4 / n
    var = ex2 - mean ** 2
    if var == 0:
        return float("nan")
    sigma = np.sqrt(var)
    
    mu_final = ex4 - 4.00 * mean * ex3 + 6.00 * (mean ** 2) * ex2 - 3.00 * (mean ** 4)

    denum = sigma ** 4

    return float(mu_final / denum - 3.00)
