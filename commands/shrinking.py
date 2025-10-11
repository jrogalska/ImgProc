import numpy as np

def do_shrinking(img: np.ndarray, args:dict) -> np.ndarray:
    factor = int(args.get('-factor'))
    return img[::factor,::factor]