import numpy as np
from utils.extract_channel import extract_channel
from utils.compute_histogram import compute_histogram

def do_cvarcoii(image: np.ndarray, args: dict[str, str]) -> float:
    channel = args.get('-channel', 'y')
    image = extract_channel(image, channel=channel)
    h, cdf, n = compute_histogram(image)
    if n == 0:
        return float("nan")
    
    h = h.astype(np.float64, copy=False)
    num = float(np.dot(h,h))
    val = num / (n*n)
    return float(val) 