import numpy as np



def do_psnr(original: np.array, new:np.array):
    original = original.astype(np.float64)
    new = new.astype(np.float64)
    if new.shape!=original.shape:
        raise ValueError("Images need to be the same type and size!")
    if original.ndim==3:
        channels = []
        for ch in range(new.shape[2]):
            calculated = _do_psnr_per_channel(original[:, :, ch], new[:, :, ch])
            channels.append(calculated)
        return channels
    else:
        return _do_psnr_per_channel(original, new)


def _do_psnr_per_channel(original:np.array, new:np.array) -> np.float64:
    max_square = np.max(original)**2
    numerator = original.shape[0] * original.shape[1] * max_square
    denominator = np.sum((original - new)**2)
    if denominator == 0 and numerator > 0:
        return float('inf')
    if denominator == 0 and numerator < 0:
        return float("-inf")
    if numerator == 0 and denominator ==0:
        return float('nan')
    return 10* np.log10(numerator/denominator)