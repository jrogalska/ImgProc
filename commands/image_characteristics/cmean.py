import numpy as np
from typing import Optional
from utils.to_luminance import as_gray

def do_cmean(image: np.ndarray, args:dict[str, str]) -> float:
    if image.size == 0:
        return float("nan")
    if image.ndim not in (2, 3):
        raise ValueError("Expected 2D (gray) or 3D (RGB) image")
    
    channel: Optional[str] = args.get('-channel', 'y')

    x = as_gray(image, channel=channel)

    return float(np.mean(x))
