import numpy as np
def do_negative(img: np.ndarray, args: dict) -> np.ndarray:
    newImg = (255-img).clip(0, 255)
    return newImg