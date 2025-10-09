import numpy as np
def do_contrast(img: np.ndarray, args: dict) -> np.ndarray:
    factor = float(args.get('-factor'))
    if factor is None:
        print("No factor given. \n")
        return
    PIVOT = 128
    newImg = (img - PIVOT) * factor + PIVOT
    newImg = np.clip(newImg, 0, 255).astype(np.uint8)
    return newImg