from commands.fourier_ops.do_fft import do_fft
from commands.fourier_ops.do_ifft import do_ifft
from commands.fourier_ops.helpers import _pad_to_pow2_2d, _fft
from commands.fourier_ops.helpers import _ifftshift2, fft2_custom, ifft2_customshift2, _fftshift2, ifft2_custom
import numpy as np
def band_pass_filter_image_custom(gray2d: np.ndarray, low_cut: float, high_cut: float) -> np.ndarray:
    """
    Band-pass filter in frequency domain:
    - removes frequencies below low_cut (high-pass)
    - removes frequencies above high_cut (low-pass)
    Keeps only a ring: [R1, R2].

    low_cut, high_cut: ratios in (0, 0.5], with low_cut < high_cut
    returns float32 (may contain negatives, normalize for display if needed)
    """
    if gray2d.ndim != 2:
        raise ValueError("Expected 2D array.")
    low_cut = float(low_cut)
    high_cut = float(high_cut)
    if not (0.0 < low_cut < high_cut <= 0.5):
        raise ValueError("Need 0.0 < low_cut < high_cut <= 0.5")

    padded, (h, w) = _pad_to_pow2_2d(gray2d)

    F = fft2_custom(padded)
    Fs = _fftshift2(F)

    H, W = Fs.shape
    cy, cx = H // 2, W // 2

    R1 = low_cut * min(H, W)
    R2 = high_cut * min(H, W)

    y = np.arange(H)[:, None] - cy
    x = np.arange(W)[None, :] - cx
    dist = np.sqrt(y * y + x * x)

    mask = ((dist >= R1) & (dist <= R2)).astype(np.float32)

    Fs_f = Fs * mask
    F_f = _ifftshift2(Fs_f)

    out = ifft2_custom(F_f)
    return out[:h, :w]


def do_band_pass(image: np.ndarray, args: dict) -> np.ndarray:
    low_cut = float(args.get("-low_cut", 0.05))
    high_cut = float(args.get("-high_cut", 0.15))

    if image.ndim == 3:
        out = np.empty(image.shape, dtype=np.float32)
        for c in range(image.shape[2]):
            out[..., c] = band_pass_filter_image_custom(image[..., c], low_cut, high_cut)
        return out
    return band_pass_filter_image_custom(image, low_cut, high_cut)
