import numpy as np
from commands.fourier_ops.do_fft import do_fft
from commands.fourier_ops.do_ifft import do_ifft
from commands.fourier_ops.helpers import _pad_to_pow2_2d, _fftshift2, _ifftshift2, fft2_custom, ifft2_custom

def high_pass_filter_image_custom(gray2d: np.ndarray, cutoff_ratio: float) -> np.ndarray:
    if gray2d.ndim != 2:
        raise ValueError("Expected 2D array (grayscale image).")
    if not (0.0 < cutoff_ratio <= 0.5):
        raise ValueError("cutoff_ratio must be in (0, 0.5].")
    
    padded, original_shape = _pad_to_pow2_2d(gray2d)
    F = fft2_custom(padded)
    Fs = _fftshift2(F)
    H, W = Fs.shape
    # Promien odciecia, wszystko powyzej tego promienia bedzie odciete. Zakladamny srodek w (H/2,W/2) jako kolo 
    # najmniejszy wymiar * cutoff_ratio
    R = cutoff_ratio * min(H, W) 

    cx, cy = W // 2, H // 2
    y = np.arange(H)[:, None] - cy  # tablica odleglosci od srodka w pionie
    x = np.arange(W)[None, :] - cx  # tablica odleglosci od srodka w poziomie
    dist = np.sqrt(y**2 + x**2)
    mask = (dist <= R).astype(np.float32)  # Maska kołowa (True wewnątrz koła, False na zewnątrz)
    mask = 1 - mask  # Inwersja maski dla filtru górnoprzepustowego
    Fs_f = Fs * mask
    #Odwracamy przesunięcie
    F_f = _ifftshift2(Fs_f)
    # Odwracamy FFT
    out = ifft2_custom(F_f)
    #usuwamy padding
    out_cropped = out[:original_shape[0], :original_shape[1]]
    return out_cropped


def do_low_cut(image: np.ndarray, args: dict) -> np.ndarray:
    cutoff_ratio = args.get("-cutoff_ratio", 0.1)
    cutoff_ratio = float(cutoff_ratio)
    if (image.ndim ==3):
        out = np.empty_like(image)
        for c in range(image.shape[2]):
            out[:, :, c] = high_pass_filter_image_custom(image[:, :, c], cutoff_ratio)
        return out
    else:
        return high_pass_filter_image_custom(image, cutoff_ratio)
    
