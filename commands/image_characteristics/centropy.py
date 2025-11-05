import numpy as np
from utils.compute_histogram import compute_histogram
from utils.extract_channel import extract_channel
def do_centropy(image: np.ndarray, args: dict[str, str]) -> float:
    channel = args.get('-channel', 'y')
    image = extract_channel(image, channel=channel)
    h, cdf, n = compute_histogram(image)
    if n == 0:
        return float("nan")
    p = h / n
    p_nonzero = p[p > 0]
    ent = -np.sum(p_nonzero * np.log2(p_nonzero))
    return float(ent)
    