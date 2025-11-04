import numpy as np

def extract_channel(img: np.ndarray, channel: str) -> np.ndarray:
    if img.dtype != np.uint8:
        raise TypeError("Oczekuję uint8.")
    if img.ndim == 2:  
        return img
    if img.ndim != 3 or img.shape[2] < 3:
        raise ValueError("Expected an image with at least 3 channels.")

    ch = channel.lower()
    R, G, B = img[...,0], img[...,1], img[...,2]
    if ch == "r": return R
    if ch == "g": return G
    if ch == "b": return B
    if ch in ("y","gray"):
        R32, G32, B32 = R.astype(np.uint32), G.astype(np.uint32), B.astype(np.uint32)
        Y = (77*R32 + 150*G32 + 29*B32) >> 8
        return Y.astype(np.uint8)
    raise ValueError("Kanał: 'r','g','b','y','gray'.")
