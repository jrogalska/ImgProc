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
        H, W, C = img.shape
        out = np.empty_like(img)
        for c in range(C):
            ch = img[..., c]
            _, cdf, n = compute_histogram(ch, num_bins=256)
            if n == 0:
                out[..., c] = ch
                continue
            lut = _build_lut_from_cdf(cdf, gmin, gmax)
            out[..., c] = lut[ch]
        return out

    raise ValueError("Expected 2D (gray) or 3D (H,W,C) image")
