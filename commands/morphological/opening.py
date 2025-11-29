import numpy as np
from commands.morphological.erosion import do_erosion
from commands.morphological.dilation import do_dilation

def do_opening(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:
    after_erosion = do_erosion(img, struct_elem, args)
    output = do_dilation(after_erosion, struct_elem, args)
    return output