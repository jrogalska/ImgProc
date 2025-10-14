import numpy as np

# | [1, 2] | -> | [1, 2] | -> | [1, 1, 2, 2] |
# | [3, 4] | -> | [1, 2] | -> | [1, 1, 2, 2] |
#               | [3, 4] | -> | [3, 3, 4, 4] |
#               | [3, 4] | -> | [3, 3, 4, 4] |

def do_enlargement(img: np.ndarray, args: dict) -> np.ndarray:
    factor = int(args.get('-factor'))
    return np.repeat(np.repeat(img, factor, 0), factor, 1)


