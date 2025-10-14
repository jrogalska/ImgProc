import numpy as np
def do_snr(original : np.array, new: np.array):
    new = new.astype(np.float64)
    original = original.astype(np.float64)
    if original.shape != new.shape:
        raise ValueError("Images need to be the same type and size!")
    if original.ndim == 3:
        channels = []
        for ch in range(original.shape[2]):
            calculated = _do_snr_per_channel(original[:, :, ch], new[:, :, ch])
            channels.append(calculated)
            
        return np.array(channels)
    else:
        return _do_snr_per_channel(original, new)


def _do_snr_per_channel(original: np.array, new:np.array) -> np.float64:
    
    numerator = np.sum(original**2)
    denominator = np.sum((original - new)**2)
    if denominator == 0 and numerator > 0:
        return float('inf')
    if denominator == 0 and numerator < 0:
        return float("-inf")
    if numerator == 0 and denominator ==0:
        return float('nan')
    return float(10 * np.log10(numerator/denominator))


