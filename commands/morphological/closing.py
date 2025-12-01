import numpy as np
from commands.morphological.erosion_optimized import do_erosion_optimized
from commands.morphological.dilation_optimized import do_dilation_optimized

def do_closing(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:
    after_dilation = do_dilation_optimized(img, struct_elem, args)
    output = do_erosion_optimized(after_dilation, struct_elem, args)
    return output