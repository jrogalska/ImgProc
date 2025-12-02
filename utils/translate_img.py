import numpy as np

def translate_image(img: np.ndarray, shift_y, shift_x):
    h, w = img.shape
    translated = np.zeros_like(img)

    if shift_y > 0:
        in_top, in_bottom = 0, h - shift_y
        out_top, out_bottom = shift_y, h

    elif shift_y < 0:
        in_top, in_bottom = -shift_y, h
        out_top, out_bottom = 0, h + shift_y

    else:
        in_top, in_bottom = 0, h
        out_top, out_bottom = 0, h

    if shift_x > 0:
        in_left, in_right = 0, w - shift_x
        out_left, out_right = shift_x, w

    elif shift_x < 0:
        in_left, in_right = -shift_x, w
        out_left, out_right = 0, w + shift_x

    else:
        in_left, in_right = 0, w
        out_left, out_right = 0, w

    translated[out_top:out_bottom, out_left:out_right] = img[in_top:in_bottom, in_left:in_right]

    return translated