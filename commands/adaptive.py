import numpy as np

#np.stack():
#mamy tablice odnoisowanych r:[1 2 3] g:[4 5 6] b:[7 8 9] 
#stack uklada nam je kolumnami w jedna tablice:
# | [1, 4, 7] |
# | [2, 5, 8] |
# | [3, 6, 9] |
#Time complexity:
#  O(N x M) iteracja po pikselach w grayscale, w rgb O(NxMx3)
# Iteracja w pętli: S^2 dla każdegogo okna
# Opcjonalnie calosc * 4 w najgorszym przypadku dla ciagle zwiekszajacego sie okna
# + Operacje typu stack




def do_adaptive_noise_filter(img:np.array, args:dict):
    sMax = args.get("sMax", 9)
    sMin = args.get("sMin", 3)

    if img.ndim == 3:
        channels = []
        for ch in range(img.shape[2]): #3
            filtered_channel = _adaptive_noise_filter_single_channel(img[:, :, ch])
            channels.append(filtered_channel, sMax, sMin)
        return np.stack(channels , axis = 2)  
    else:
        return _adaptive_noise_filter_single_channel(img, sMax, sMin)


def _adaptive_noise_filter_single_channel(img: np.array, sMax:int, sMin:int):
    sMax = 9
    sMin = 3
    rows, cols = img.shape[0], img.shape[1]
    new_img = np.zeros((rows, cols), dtype=np.int16)

    for r in range(rows):
        for c in range(cols):
            s = sMin
            while True:
                zxy = img[r, c]
                window = _create_window(img, r, c, s)
                min = np.min(window).astype(np.int32)
                max = np.max(window).astype(np.int32)
                med = np.median(window).astype(np.int64)
                A1 = med - min
                A2 = med - max
                if A1 > 0 and A2 < 0:
                    B1 = zxy - min
                    B2 = zxy - max
                    if B1 > 0 and B2 < 0:
                        new_img[r, c] = zxy
                    else:
                        new_img[r, c] = med
                    break
                else:
                    s+=2
                    if s > sMax:
                        new_img[r, c] = med
                        break
    return new_img

    



def _create_window(arr: np.array, row, col, size: int) -> np.array:
    half = size // 2 
    r_min = max(0, row - half)
    r_max = min(arr.shape[0], row + half + 1)
    c_min = max(0, col - half)
    c_max = min(arr.shape[1], col + half + 1)
    #for size: 3, half = 1, so we want arr[r-1:r+2, c-1:c+2] r+2 not inclusive c+2 not inclusiveS
    return arr[r_min:r_max, c_min:c_max]

