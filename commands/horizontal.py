import numpy as np

def do_horizontal_flip(img: np.ndarray, args: dict) -> np.ndarray:
    return np.flip(img, axis=1)