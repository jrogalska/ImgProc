import numpy as np

def  do_signal_to_noise(original_img: np.ndarray, other_img: np.ndarray):
    if original_img.shape != other_img.shape:
        raise ValueError("The images must have the same sizes.")
    signal = np.sum(np.square(original_img.astype('float')))
    noise = np.sum(np.square(original_img.astype('float') - other_img.astype('float')))
    if noise == 0:
        snr = np.inf
    else:
        snr = 10 * np.log10(signal / noise)    
    return snr