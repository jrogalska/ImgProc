import numpy as np
from commands.fourier_ops.do_fft import do_fft
from commands.fourier_ops.do_ifft import do_ifft
from commands.fourier_ops.helpers import _pad_to_pow2_2d, _fftshift2, _ifftshift2, fft2_custom, ifft2_custom
from utils.to_luminance import as_gray
from commands.fourier_ops.helpers import resize
from input_output import load_image

def directional_highpass(gray2d: np.ndarray, mask: np.ndarray) -> np.ndarray:
    if gray2d.ndim != 2:
        raise ValueError("Expected 2D array.")

    padded, (h, w) = _pad_to_pow2_2d(gray2d)
    F = fft2_custom(padded)
    Fs = _fftshift2(F)

    H, W = Fs.shape

    if mask.ndim == 3:
        mask = as_gray(mask)
    
    if mask.shape != (H, W):
        mask = resize(mask, (H, W))

    mask_float = mask.astype(np.float32) / 255.0

    Fs_filtered = Fs * mask_float

    F_filtered = _ifftshift2(Fs_filtered)
    out = ifft2_custom(F_filtered)

    return out[:h, :w]


def do_dir_highpass(image: np.ndarray, args: dict) -> np.ndarray:
    mask = args.get("-mask", "images/F5mask1.bmp")
    try:
        mask_array = load_image(mask)
    except Exception:
        print("Error: could not load the mask.")
        return image

    if image.ndim == 3:
        gray_img = as_gray(image)
    else:
        gray_img = image

    out = directional_highpass(gray_img, mask_array)
    out = np.abs(out)
    treshold = 0.15 * np.max(out)
    out[out < treshold] = 0

    return out