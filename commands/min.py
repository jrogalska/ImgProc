import numpy as np
from commands.adaptive import _create_window

def do_min_filer(img: np.ndarray, args: dict) -> np.ndarray:
    img2 = np.copy(img)
    if img.ndim == 3:
        for c in range(img.shape[2]):
            for i in range(1, img.shape[0] - 1):
                for j in range(1, img.shape[1] - 1):
                    window = img[i-1:i+2, j-1:j+2, c]
                    min_val = np.min(window)
                    img2[i, j, c] = min_val
    else:
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                window = img[i-1:i+2, j-1:j+2]
                min_val = np.min(window)
                img2[i, j] = min_val
    return img2