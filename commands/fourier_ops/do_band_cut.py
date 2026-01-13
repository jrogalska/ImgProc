import numpy as np
from commands.fourier_ops.do_fft import do_fft
from commands.fourier_ops.do_ifft import do_ifft
from commands.fourier_ops.helpers import _pad_to_pow2_2d, _fftshift2, _ifftshift2, fft2_custom, ifft2_custom

def band_cut_filter(gray2d: np.ndarray, low_cut: float, high_cut: float) -> np.ndarray:
    if gray2d.ndim !=2:
        raise ValueError("Expected 2D array.")
    
    low_cut = float(low_cut)
    high_cut = float(high_cut)

    if not (0.0 < low_cut < high_cut <= 0.5):
        raise ValueError("Need 0.0 < low_cut < high_cut <= 0.5")
    
    padded, (h,w) = _pad_to_pow2_2d(gray2d)

    F = fft2_custom(padded)
    Fs = _fftshift2(F)

    H, W = Fs.shape
    cy, cx = H//2, W//2

    R1 = low_cut * min(H, W)
    R2 = high_cut * min(H, W)

    y = np.arange(H)[:, None] - cy
    x = np.arange(W)[None, :] - cx

    dist = np.sqrt(y*y + x*x)

    mask = 1.0 - ((dist >= R1) & (dist <= R2)).astype(np.float32)

    Fs_f = Fs * mask

    F_f = _ifftshift2(Fs_f)
    out = ifft2_custom(F_f)

    return out[:h, :w]

def do_band_cut(image: np.ndarray, args: dict) -> np.ndarray:
    low_cut = float(args.get("-low_cut", 0.05))
    high_cut = float(args.get("-high_cut", 0.15))

    if image.ndim == 3:
        out = np.empty(image.shape, dtype=np.float32)
        for c in range(image.shape[2]):
            out[..., c] = band_cut_filter(image[..., c], low_cut, high_cut)
        return out
    return band_cut_filter(image, low_cut, high_cut)