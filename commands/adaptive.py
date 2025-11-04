import numpy as np

def do_adaptive_noise_filter(img: np.ndarray, args: dict):
    sMax = int(args.get("-sMax", 9))
    sMin = int(args.get("-sMin", 3))

    if (sMax % 2 == 0 or sMin % 2 == 0):
        raise ValueError("Window size must be an odd number")
    if not (sMax >= sMin >= 3):
        raise ValueError("Window size must be sMax>=sMin>=3")

    orig_dtype = img.dtype

    if img.ndim == 3:
        channels = []
        for ch in range(img.shape[2]):  # np. 3 dla RGB
            filtered_channel = _adaptive_noise_filter_single_channel(img[:, :, ch], sMax, sMin)
            channels.append(filtered_channel)
        out = np.stack(channels, axis=2)
    else:
        out = _adaptive_noise_filter_single_channel(img, sMax, sMin)

    # Przywracamy typ i zakres
    if np.issubdtype(orig_dtype, np.integer):
        info = np.iinfo(orig_dtype)
        out = np.clip(out, info.min, info.max).astype(orig_dtype)
    else:
        out = out.astype(orig_dtype)

    return out


def _adaptive_noise_filter_single_channel(img: np.ndarray, sMax: int, sMin: int):
    rows, cols = img.shape[:2]
    new_img = np.zeros((rows, cols), dtype=np.int32)

    for r in range(rows):
        for c in range(cols):
            s = sMin
            while True:
                zxy = np.int32(img[r, c])
                window = _create_window(img, r, c, s)
                zmin = np.int32(np.min(window))
                zmax = np.int32(np.max(window))
                zmed = np.int32(np.median(window))

                A1 = zmed - zmin
                A2 = zmed - zmax
                if A1 > 0 and A2 < 0:
                    B1 = zxy - zmin
                    B2 = zxy - zmax
                    new_img[r, c] = zxy if (B1 > 0 and B2 < 0) else zmed
                    break
                else:
                    s += 2
                    if s > sMax:
                        new_img[r, c] = zxy
                        break
    return new_img


def _create_window(arr: np.ndarray, row, col, size: int) -> np.ndarray:
    half = size // 2
    r_min = max(0, row - half)
    r_max = min(arr.shape[0], row + half + 1)
    c_min = max(0, col - half)
    c_max = min(arr.shape[1], col + half + 1)
    return arr[r_min:r_max, c_min:c_max]
