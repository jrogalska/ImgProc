import numpy as np 
from utils.compute_histogram import compute_histogram
from commands.image_characteristics.cvariance import do_cvariance
def do_cstdev(image: np.ndarray, args:dict[str, str]) -> float:
    cvar = do_cvariance(image, args)
    if np.isnan(cvar):
        return float("nan")
    return float(np.sqrt(cvar))
