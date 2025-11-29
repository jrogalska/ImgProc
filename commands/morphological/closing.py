import numpy as np
from commands.morphological.erosion import do_erosion
from commands.morphological.dilation import do_dilation

def do_closing(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:
    after_dilation = do_dilation(img, struct_elem, args)
    output = do_erosion(after_dilation, struct_elem, args)
    return output