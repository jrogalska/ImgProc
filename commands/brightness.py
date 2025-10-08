import numpy as np

def do_brightness(img: np.ndarray, const: int) -> np.ndarray:
    if not (-255 <= const <= 255):
        print("Constant must be between -255 and 255. \n")
        return
    else:
        newImg = img + const
        newImg = np.clip(newImg, 0, 255)
        return newImg