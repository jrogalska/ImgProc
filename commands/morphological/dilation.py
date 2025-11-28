import numpy as np
from utils.get_struct import get_binary_struct

def do_dilation(img: np.ndarray, struct_elem, args: dict) -> np.ndarray:
    h, w = img.shape

    img = (img > 0).astype(np.uint8)

    unique_vals = np.unique(img)

    if(len(unique_vals)>2):
        print("Error: Morphological operations require a BINARY image.")
        return img

    elem_shape = get_binary_struct(struct_elem)
    eh, ew = elem_shape.shape
    oy, ox = struct_elem["origin"]

    output = np.zeros_like(img)

    for y in range(h):
        for x in range(w):
            hit = False
            for ey in range(eh):
                for ex in range(ew):
                        
                    if elem_shape[ey, ex] ==1:
                        neighbor_y = y + (ey - oy)
                        neighbor_x = x + (ex - ox)

                        if(neighbor_y>= 0 and neighbor_y < h and
                        neighbor_x>= 0 and neighbor_x < w):
                            
                            val = img[neighbor_y, neighbor_x]
                            if val == 1:
                                hit = True
                                break
                if hit: break
            if hit: output[y, x] = 1
    return output


