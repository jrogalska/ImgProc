import numpy as np
from commands.fourier_ops.do_fft import do_fft
from commands.fourier_ops.do_ifft import do_ifft


def _next_pow_2(x: int) -> int:
    p = 1
    while p < x:
        p *= 2
    return p

def _pad_to_pow2_2d(data: np.ndarray) -> np.ndarray:
    #RGB -> Grayscale
    if data.ndim == 3:
        data = data[:,:,0] * 0.2989 + data[:,:,1] * 0.5870 + data[:,:,2] * 0.1140
    h, w = data.shape
    H = _next_pow_2(h)
    W = _next_pow_2(w)
    out = np.zeros((H, W), dtype=data.dtype)
    out[:h, :w] = data.astype(np.float32, copy=False)
    return out, (h, w)

def fft2_custom(img2d: np.ndarray) -> np.ndarray:
    # FFT rows
    rows = np.array([do_fft(row.astype(np.complex64)) for row in img2d], dtype=np.complex64)
    # FFT cols
    cols_in = rows.T
    cols = np.array([do_fft(col) for col in cols_in], dtype=np.complex64)
    return cols.T

def ifft2_custom(freq2d: np.ndarray) -> np.ndarray:
    # IFFT rows
    rows = np.array([do_ifft(row) for row in freq2d], dtype=np.complex64)
    # IFFT cols
    cols_in = rows.T
    cols = np.array([do_ifft(col) for col in cols_in], dtype=np.complex64)
    out = cols.T
    return np.real(out).astype(np.float32)


def _fftshift2(x: np.ndarray) -> np.ndarray:
    return np.roll(np.roll(x, x.shape[0] // 2, axis=0), x.shape[1] // 2, axis=1)

def _ifftshift2(x: np.ndarray) -> np.ndarray:
    return np.roll(np.roll(x, -(x.shape[0] // 2), axis=0), -(x.shape[1] // 2), axis=1)

def resize(image: np.ndarray, new_shape: tuple) -> np.ndarray:
    new_h, new_w = new_shape
    old_h, old_w = image.shape

    row_indices = (np.arange(new_h) * (old_h/new_h)).astype(int)
    col_indices = (np.arange(new_w) * (old_w/new_w)).astype(int)

    return image[row_indices[:, None], col_indices]