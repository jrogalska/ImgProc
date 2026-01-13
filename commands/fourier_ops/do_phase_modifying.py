import numpy as np
from commands.fourier_ops.helpers import _pad_to_pow2_2d, fft2_custom, ifft2_custom

def phase_modifying_filter(gray2d: np.ndarray, k: int, l: int) -> np.ndarray:
    padded, original_shape = _pad_to_pow2_2d(gray2d)

    F = fft2_custom(padded)
    N, M = F.shape

    n = np.arange(N).reshape(-1, 1)
    m = np.arange(M).reshape(1, -1)

    term_n = -n * k * 2 * np.pi / N
    term_m = -m * l * 2 * np.pi / M
    term_const = (k + l) * np.pi

    phase_angle = term_n + term_m + term_const

    mask = np.exp(1j * phase_angle)

    F_modified = F * mask

    out = ifft2_custom(F_modified)

    h, w = original_shape
    return out[:h, :w]

def do_phase_modifying(image: np.ndarray, args: dict) -> np.ndarray:
    try:
        k = int(args.get("-k", 0))
        l = int(args.get("-l", 0))
    except ValueError:
        print("Error: parameters k and l must be integers")
        return image
    
    return phase_modifying_filter(image, k, l)