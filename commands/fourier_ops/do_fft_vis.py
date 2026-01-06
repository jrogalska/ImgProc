import numpy as np
from commands.fourier_ops.do_fft import do_fft
import matplotlib.pyplot as plt
from commands.fourier_ops.helpers import _pad_to_pow2_2d, _fftshift2, fft2_custom

def do_fft_vis(gray2d: np.ndarray, args: dict) -> np.ndarray:
    mag = np.abs(fft2_custom(_pad_to_pow2_2d(gray2d)[0]))
    mag_shifted = _fftshift2(mag)
    mag_spectrum = np.log1p(mag_shifted)  

    plt.figure()
    plt.imshow(mag_spectrum, cmap="gray")
    plt.title("FFT Magnitude Spectrum (log, shifted)")
    plt.axis("off")
    plt.show()


    