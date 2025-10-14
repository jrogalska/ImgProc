import numpy as np

# | [A, B, C] | ->   | [A, E, I] |
# | [E, F, G] | ->   | [B, F, J] |
# | [I, J, K] | ->   | [C, G, K] |
def do_diagonal_flip(img: np.ndarray, args: dict) -> np.ndarray:
    return np.flip(img, (0,1))