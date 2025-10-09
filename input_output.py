from PIL import Image
import numpy as np

def load_image(path: str) -> np.ndarray:
    try:
        img = Image.open(path)
        if img.mode == "P":
            img = img.convert("RGB") # paletted image
        elif img.mode == "LA": #grayscale with alpha
            img = img.convert("L")
        elif img.mode == "RGBA": #rgb with alpha
            img = img.convert("RGB") #drop alpha channel
        elif img.mode not in ("L", "RGB"):
            img = img.convert("RGB") #convert to RGB if in unknown mode
    except Exception as e:
        print("Error loading image. Check the file path and format. \n")
        raise SystemExit(2)
    
    arr = np.array(img.getdata())
    if arr.ndim == 1:
        numColorChannels = 1
        arr = arr.reshape(img.size[1], img.size[0])
    else:
        numColorChannels = arr.shape[1]
        arr = arr.reshape(img.size[1], img.size[0], numColorChannels)
    arr = arr.astype(np.float32)
    return arr 


def save_image(path: str, arr: np.ndarray):
    try:
        newImg = Image.fromarray(arr.astype(np.uint8))
        #newImg.show() opcjonalna podgladarka
        newImg.save(path)
    except Exception as e:
        print("Error saving image. Check the file path. \n")
        print(e)
        raise SystemExit(3)