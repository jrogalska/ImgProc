import numpy as np

def do_min_filer(img: np.ndarray, args: dict) -> np.ndarray:
    window_size_str = args.get("-window", 3)
    window_size = int(window_size_str)
    if (window_size%2==0 or window_size%2==0):
        raise ValueError("Window size cannot be a number divisible by 2")
    m = int((window_size - 1) / 2)
    img2 = np.copy(img)
    if img.ndim == 3:
        for c in range(img.shape[2]):
            for i in range(m, img.shape[0] - m):
                for j in range(m, img.shape[1] - m):
                    window = img[i-m:i+m+1, j-m:j+m+1, c]
                    min_val = np.min(window)
                    img2[i, j, c] = min_val
    else:
        for i in range(m, img.shape[0] - m):
            for j in range(m, img.shape[1] - m):
                window = img[i-m:i+m+1, j-m:j+m+1]
                min_val = np.min(window)
                img2[i, j] = min_val
    return img2