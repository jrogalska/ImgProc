import numpy as np
from utils.get_struct import get_binary_struct
from utils.translate_img import translate_image

def do_dilation_optimized(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:
    img = (img > 0).astype(np.uint8)

    unique_vals = np.unique(img)

    if(len(unique_vals)>2):
        print("Error: Morphological operations require a BINARY image.")
        return img

    elem_shape = get_binary_struct(struct_elem)
    oy, ox = struct_elem["origin"]

    y_coords, x_coords = np.where(elem_shape == 1)

    output = np.zeros_like(img)

    for ey, ex in zip(y_coords, x_coords):
        shift_y = - (ey - oy)
        shift_x = - (ex - ox)

        shifted = translate_image(img, shift_y, shift_x)

        output = np.logical_or(output, shifted)

    return output.astype(np.uint8)


