import numpy as np

from commands.fourier_ops.do_fft import do_fft

def do_ifft(data: np.ndarray) -> np.ndarray:
    """
    Inverse Fast Fourier Transform (IFFT)
    Implemented using FFT via conjugation.
    Wynika to ze wzoru:
    IFFT(X) = 1/N * ∑ X[k] * exp(j*2πkn/N) for n=0 to N-1
    Czyli to samo co FFT ale z dodatnim wykładnikiem w exp i podzielone przez N.
    """
    data = np.asarray(data, dtype=complex)
    N = data.shape[0]
    data_conj = np.conj(data) # ZAMIANA NP: 2-3j -> 2+3j 
    temp = do_fft(data_conj)
    return np.conj(temp) / N
    ""
