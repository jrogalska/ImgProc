import numpy as np
from commands.fourier_ops.do_fft import do_fft
from commands.fourier_ops.do_ifft import do_ifft


# Low pass zakłada, że sygnały wysokich częstotliwości są odcięte na obrzeżach obrazu w dziedzinie częstotliwości
#jednak robienie maski na rogach jest niewygodne, więc przesuwamy zero częstotliwości do środka
# (fftshift) i potem z powrotem (ifftshift)
# Takie przesunięcie jest pomocne
def _fftshift2(x: np.ndarray) -> np.ndarray:
    return np.roll(np.roll(x, x.shape[0] // 2, axis=0), x.shape[1] // 2, axis=1)

def _ifftshift2(x: np.ndarray) -> np.ndarray:
    return np.roll(np.roll(x, -(x.shape[0] // 2), axis=0), -(x.shape[1] // 2), axis=1)


def low_pass_filter_image_custom(gray2d: np.ndarray, cutoff_ratio: float) -> np.ndarray:
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
    Fs_f = Fs * mask
    #Odwracamy przesunięcie
    F_f = _ifftshift2(Fs_f)
    # Odwracamy FFT
    out = ifft2_custom(F_f)
    #usuwamy padding
    out_cropped = out[:original_shape[0], :original_shape[1]]
    return out_cropped


def do_high_cut(image: np.ndarray, args: dict) -> np.ndarray:
    cutoff_ratio = args.get("-cutoff_ratio", 0.1)
    cutoff_ratio = float(cutoff_ratio)
    if (image.ndim ==3):
        out = np.empty_like(image)
        for c in range(image.shape[2]):
            out[:, :, c] = low_pass_filter_image_custom(image[:, :, c], cutoff_ratio)
        return out
    else:
        return low_pass_filter_image_custom(image, cutoff_ratio)
    
