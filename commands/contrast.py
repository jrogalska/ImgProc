import numpy as np

def do_contrast(img: np.ndarray, args: dict) -> np.ndarray:
    val = args.get('--factor')
    if val is None:
        raise ValueError("No factor given.\n")
    try:
        factor = float(val)
    except:
        raise Exception("Factor must be a floating point number")
    if factor < 0:
        raise ValueError("Factor must be higher than 0")
    

    x = np.arange(256, dtype=np.float32)
    lut = np.floor((x - 128.0) * factor + 128.0)
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    idx = img.astype(np.uint8, copy=False)
    out = np.empty_like(idx, dtype=np.uint8)
    np.take(lut, idx, out=out)
    return out
