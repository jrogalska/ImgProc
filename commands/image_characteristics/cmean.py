import numpy as np
from typing import Dict

def do_cmean(image: np.ndarray, args: Dict[str, str]) -> float:
    if image.size == 0:
        return float("nan")
    if image.ndim not in (2, 3):
        raise ValueError("Expected 2D (gray) or 3D (RGB/RGBA) image")

    channel = args.get("-channel", "y").upper()
    if image.ndim == 2:
        return float(np.mean(image.astype(np.float64)))


    imgf = image[..., :3].astype(np.float64) 

    if channel in ("R", "G", "B"):
        idx = {"R": 0, "G": 1, "B": 2}[channel]
        return float(np.mean(imgf[..., idx]))

    if channel == "Y":
        means = imgf.mean(axis=(0, 1))  # [meanR, meanG, meanB]
        y_mean = 0.299 * means[0] + 0.587 * means[1] + 0.114 * means[2]
        return float(y_mean)

    raise ValueError("Expected channel r|g|b|y")
