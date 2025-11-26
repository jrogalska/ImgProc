import numpy as np
import time 

K1 = np.array([[0, -1,  0],
               [-1, 5, -1],
               [0, -1,  0]], dtype=np.float32)

K2 = np.array([[-1, -1, -1],
               [-1,  9, -1],
               [-1, -1, -1]], dtype=np.float32)

K3 = np.array([[ 1, -2,  1],
               [-2,  5, -2],
               [ 1, -2,  1]], dtype=np.float32)

K_MAP = {"K1": K1, "K2": K2, "K3": K3}

def do_sedghesharp_opt(image: np.ndarray, args: dict[str, str]) -> np.ndarray:
    kernel_key = args.get("-kernel", "K1").upper()
    if kernel_key not in K_MAP:
        raise ValueError("Kernel not defined ('K1' | 'K2' | 'K3')")
    K = K_MAP[kernel_key]

    x = image.astype(np.float32)

    if x.ndim == 2:
        start = time.time()

        y = _do_sedghesharp_single_channel(x, K)
        end = time.time()
        print(f"Czas: {end-start:.4f}")

        return np.clip(np.rint(y), 0, 255).astype(np.uint8)

    if x.ndim == 3 and x.shape[2] == 3:
        start = time.time()

        chans = [_do_sedghesharp_single_channel(x[..., c], K) for c in range(3)]
        y = np.stack(chans, axis=-1)
        end = time.time()
        print(f"Czas: {end-start:.4f}")
        return np.clip(np.rint(y), 0, 255).astype(np.uint8)

    raise ValueError("Expecting 2D or RGB images")

def _do_sedghesharp_single_channel(img2d: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    H, W = img2d.shape
        
    if H < 3 or W < 3:
        return img2d.copy()

    out = img2d.copy()  
    for h in range(1, H-1):
        for w in range(1, W-1):
                patch = img2d[h-1:h+2, w-1:w+2]   # 3x3
                patch_sum = np.sum(patch)
                out_num = 10 * img2d[h, w] - patch_sum
                out[h,w] = out_num

    return out
