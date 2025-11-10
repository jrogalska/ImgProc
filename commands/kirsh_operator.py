import numpy as np

def do_kirsh_operator(img: np.ndarray, args: dict) -> np.ndarray:
    if img.ndim == 2:
        return kirsh(img)
    else:
        R = img[...,0]
        G = img[...,1]
        B = img[...,2]
        Y = 0.299*R + 0.587*G + 0.114*B
        return kirsh(Y)


def kirsh(img:np.ndarray) -> np.ndarray:
    output = np.zeros_like(img, dtype=np.float32)
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            window = img[i-1:i+2, j-1:j+2].astype(np.int32)
            A = [window[0,0], window[0,1], window[0,2], window[1,2], window[2,2], window[2,1], window[2,0], window[1,0]]
            g = [1]
            for n in range(0, 8):
                S = A[n] + A[(n+1)%8] + A[(n+2)%8]
                T = A[(n+3)%8] + A[(n+4)%8] + A[(n+5)%8] + A[(n+6)%8] + A[(n+7)%8]
                result = abs(5*S - 3*T)
                g.append(result)
            output[i,j] = max(g)
    output = np.clip(output, 0, 255).astype(np.uint8)
    return output