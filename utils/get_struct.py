import numpy as np

def get_binary_struct(struct_elem):
    raw_shape = struct_elem["shape"]
    return (raw_shape == 1).astype(np.uint8)