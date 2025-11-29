import numpy as np
from commands.morphological.HMT_transformation import do_hmt
from structural_elements import STRUCT_ELEMENTS

def do_m4(img: np.ndarray, args: dict) -> np.ndarray:

    unique_vals = np.unique(img)

    if(len(unique_vals)>2):
        print("Error: Morphological operations require a BINARY image.")
        return img

    img = (img > 0).astype(np.uint8)

    xi_elements = [STRUCT_ELEMENTS["xi[1]"],
                   STRUCT_ELEMENTS["xi[2]"],
                   STRUCT_ELEMENTS["xi[3]"],
                   STRUCT_ELEMENTS["xi[4]"]]
    
    final = np.zeros_like(img)

    for i, struct in enumerate(xi_elements):
        current_img = img.copy()
        
        while True:
            hmt_result = do_hmt(current_img, struct, args)

            next_img = np.logical_or(current_img, hmt_result).astype(np.uint8)

            if np.array_equal(current_img, next_img):
                break

            current_img = next_img
        D_i = current_img
        final = np.logical_or(final, D_i).astype(np.uint8)

    return final * 255