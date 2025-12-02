import numpy as np
from commands.morphological.erosion_optimized import do_erosion_optimized
from commands.morphological.dilation_optimized import do_dilation_optimized

def do_opening(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:
    after_erosion = do_erosion_optimized(img, struct_elem, args)
    output = do_dilation_optimized(after_erosion, struct_elem, args)
    return output