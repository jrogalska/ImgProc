import numpy as np
from utils.compute_histogram import compute_histogram

def _build_lut_from_cdf(cdf: np.ndarray, gmin: int, gmax: int) -> np.ndarray:
    cdf = cdf.astype(np.float32)
    gmin_eff = max(float(gmin), 1e-6)
    ratio = float(gmax) / gmin_eff
    lut = gmin_eff * (ratio ** cdf)
    return np.clip(np.rint(lut), 0, 255).astype(np.uint8)

def do_hhyper(img: np.ndarray, args: dict[str, str]) -> np.ndarray:
    if img.dtype != np.uint8:
        raise ValueError("Expected uint8 image")

    gmin = int(args.get('-gmin', 64))
    gmax = int(args.get('-gmax', 255))

    # Gray
    if img.ndim == 2:
        ch = img
        _, cdf, n = compute_histogram(ch, num_bins=256)
        if n == 0:
            return ch.copy()
        lut = _build_lut_from_cdf(cdf, gmin, gmax)
        return lut[ch]

    if img.ndim == 3:
        R = img[..., 0]
        G = img[..., 1]
        B = img [..., 2]
        Y = 0.299 * R + 0.587* G + 0.114 * B
        Y_u8 = np.clip(np.rint(Y), 0, 255).astype(np.uint8)
        _, cdf, n = compute_histogram(Y_u8)
        if (n==0):
            return img.copy()
        lut = _build_lut_from_cdf(cdf, gmin, gmax)
        Y_new = lut[Y_u8].astype(np.float32)
        eps = 1e-6
        gain = Y_new/(Y+eps)
        Rn = np.clip(np.rint(R*gain), 0, 255).astype(np.uint8)
        Gn = np.clip(np.rint(G*gain), 0, 255).astype(np.uint8)
        Bn = np.clip(np.rint(B*gain), 0, 255).astype(np.uint8)
        out = np.stack([Rn, Gn, Bn], axis = 2)
        return out


    raise ValueError("Expected 2D (gray) or 3D (H,W,C) image")
