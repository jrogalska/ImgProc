import numpy as np
def do_contrast(img: np.ndarray, args: dict) -> np.ndarray:
    factor = float(args.get('-factor'))
    if factor is None:
        print("No factor given. \n")
        return
    PIVOT = 128
    x = np.arrange(256, dtype=np.float32)
    lut = (x-PIVOT)*factor + PIVOT
    
    out = np.empty_like(img, dtype=np.float32)
    np.take(lut, img, out=out) #przepisywanie wartosci do tabeli out

    return out