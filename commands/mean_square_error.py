import numpy as np

def do_mean_square_error(orignal_img: np.ndarray, other_img: np.ndarray):
    if orignal_img.shape != other_img.shape:
        raise ValueError("The images must have the same sizes.")
    
    difference = orignal_img.astype("float") - other_img.astype("float")
    squared = np.square(difference)
    mse = np.mean(squared)
    return mse
