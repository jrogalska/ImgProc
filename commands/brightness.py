import numpy as np

def do_brightness(img: np.ndarray, args: dict) -> np.ndarray:
    const = int(args.get('-const'))
    if const is None:
        print("No constant given. \n")
        return
    if not (-255 <= const <= 255):
        print("Constant must be between -255 and 255. \n")
        return
    else:
        newImg = img + const
        newImg = np.clip(newImg, 0, 255).astype(np.uint8)
        return newImg