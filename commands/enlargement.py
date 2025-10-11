import numpy as np

def do_enlargement(img: np.ndarray, args: dict) -> np.ndarray:
    factor = int(args.get('-factor'))
    return np.repeat(np.repeat(img, factor, 0), factor, 1)


