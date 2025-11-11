import numpy as np

def _parse_kernel3x3(kernel_str: str) -> np.ndarray:
    if not isinstance(kernel_str, str) or not kernel_str.strip():
        raise ValueError("Missing 'kernel'  '0,-1,0; -1,5,-1; 0,-1,0'")
    rows = [r.strip() for r in kernel_str.split(";") if r.strip()]
    if len(rows) != 3:
        raise ValueError("Kernel must have 3 rows separated by ';'")
    vals = []
    for r in rows:
        parts = [p for p in r.replace(",", " ").split() if p]
        if len(parts) != 3:
            raise ValueError("Each kernel row must have exactly 3 numbers")
        vals.extend(float(p) for p in parts)
    return np.array(vals, dtype=np.float32).reshape(3, 3)

def do_mask_filter(image: np.ndarray, args: dict[str, str]) -> np.ndarray:
    kernel_str = args.get("kernel", "K1")
    K = _parse_kernel3x3(kernel_str)

    x = image.astype(np.float32)

    if x.ndim == 2:
        y = _do_mask_filter_single_channel(x, K)
        return np.clip(np.rint(y), 0, 255).astype(np.uint8)

    if x.ndim == 3 and x.shape[2] == 3:
        chans = [_do_mask_filter_single_channel(x[..., c], K) for c in range(3)]
        y = np.stack(chans, axis=-1)
        return np.clip(np.rint(y), 0, 255).astype(np.uint8)

    raise ValueError("Expecting 2D or RGB images")

def _do_mask_filter_single_channel(img2d: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    H, W = img2d.shape
    if H < 3 or W < 3:
        return img2d.copy()

    out = img2d.copy()
    for h in range(1, H-1):
        for w in range(1, W-1):
            patch = img2d[h-1:h+2, w-1:w+2]   # 3x3
            out[h, w] = float((patch * kernel).sum())
    return out