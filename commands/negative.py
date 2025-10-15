import numpy as np
def do_negative(img: np.ndarray, args: dict) -> np.ndarray:
    x = np.arange(256, dtype=np.float32)
    lut = 255 - x
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    idx = img.astype(np.uint8, copy = False)
    return np.take(lut, idx)