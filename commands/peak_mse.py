import numpy as np
from commands.mean_square_error import do_mean_square_error

def do_peak_mse(original_img:np.ndarray, other_img: np.ndarray):
    max_value = np.max(original_img)
    if max_value == 0:
        pmse = 0
    else:
        pmse = do_mean_square_error(original_img, other_img)/np.square(max_value)
    return pmse