import numpy as np

def do_max_difference(original_img: np.ndarray, other_img: np.ndarray):
    if original_img.shape != other_img.shape:
        raise ValueError("The images must have the same sizes.")
    md = np.max(np.abs(original_img.astype('float') - other_img.astype('float')))
    return md