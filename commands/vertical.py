import numpy as np

def do_vertical_flip(img: np.ndarray, args: dict) -> np.ndarray:
    return np.flip(img, axis=0)