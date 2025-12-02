import numpy as np
from commands.morphological.erosion_optimized import do_erosion_optimized

def do_hmt(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:

    unique_vals = np.unique(img)

    if(len(unique_vals)>2):
        print("Error: Morphological operations require a BINARY image.")
        return img

    img = (img > 0).astype(np.uint8)

    elem_shape = struct_elem["shape"]
    hit_shape  = (elem_shape == 1).astype(np.uint8)
    miss_shape = (elem_shape == 0).astype(np.uint8)

    hit = {
        "shape": hit_shape,
        "origin": struct_elem["origin"]
    }

    miss = {
        "shape": miss_shape,
        "origin": struct_elem["origin"]
    }

    erosion_hit = do_erosion_optimized(img, hit, args)

    inverted_img = 1 - img
    erosion_miss = do_erosion_optimized(inverted_img, miss, args)

    result = np.logical_and(erosion_hit, erosion_miss).astype(np.uint8)

    return result