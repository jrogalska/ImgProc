import numpy as np

def do_fft(data: np.ndarray) -> np.ndarray:
    """
    Perform a Fast Fourier Transform (FFT) on the input data.

    Parameters:
    data (np.ndarray): Input array containing the time-domain signal.

    Returns:
    np.ndarray: The FFT of the input signal.
    """
    N = data.shape[0]
    if (N == 1):
        return data
    
    if not (N & (N - 1) == 0) and N != 0:
        raise ValueError("Input length must be a power of 2")
    
    even = do_fft(data[::2])
    odd = do_fft(data[1::2])

    X = np.zeros(N, dtype=complex)
    W_N = np.exp(-2j * np.pi / N) 
    W = 1.0 # W_N^0 - STart with W_N^0
    for k in range(N // 2):
        t = W * odd[k]
        #BUTTERFLY OPERATION
        X[k] = even[k] + t      # X[k] = E[k] + W_N^k * O[k] // First half
        X[k + N // 2] = even[k] - t  # X[k + N/2] = E[k] - W_N^k * O[k] // Second half
        W *= W_N  # Update W to W_N^(k+1)

    return X