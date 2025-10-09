import numpy as np

def do_diagonal_flip(img: np.ndarray, args: dict) -> np.ndarray:
    return np.flip(img, (0,1))