import numpy as np
_YW = np.array([0.2126, 0.7152, 0.0722], dtype=np.float64)

def as_gray(image: np.ndarray, channel: str="y") -> np.ndarray:
    if image.ndim == 2:
        return image
    
    elif image.ndim == 3:
        rgb = image[..., :3]
        if channel == "y":
            x = np.tensordot(rgb.astype(np.float64), _YW, axes=([-1], [0]))
        else:
            idx = {"r": 0, "g": 1, "b": 2}.get(channel.lower())
            if idx is None:
                raise ValueError("Invalid channel specified. Use 'r', 'g', or 'b'.")
            x = rgb[..., idx].astype(np.float64)

    else:
        raise ValueError("Expected 2D (gray) or 3D (RGB) image")

    return np.clip(x, 0, 255).astype(np.uint8)