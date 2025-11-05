from PIL import Image, ImageDraw
import numpy as np
from math import log10
from utils.extract_channel import extract_channel
from utils.compute_histogram import compute_histogram

def _parse_bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    v = str(v).strip().lower()
    return v in ("1", "true", "t", "yes", "y")

def do_histogram(
    img: np.ndarray,
    args: dict[str, str]
) -> Image.Image:
    # --- args ---
    ch = args.get('-channel', 'y').lower()
    num_bins = int(args.get('-bins', '256'))
    plot_h = int(args.get('-height', '200'))
    plot_w = int(args.get('-width', str(num_bins)))
    bar_color = args.get('-color', 'black')
    bg_color = args.get('-bgcolor', 'white')
    margin = int(args.get('-border', '10'))
    bar_w_arg = int(args.get('-barwidth', '10'))

    

    chan = extract_channel(img, ch)  # powinien zwrócić 2D ndarray
    h, cdf, n = compute_histogram(chan.astype(np.uint8),  num_bins)
    h = np.asarray(h, dtype=np.float64)

    vmax = float(h.max()) if h.size else 0.0


    W = plot_w + 2 * margin
    H = plot_h + 2 * margin
    img_out = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img_out)

    bins = len(h)
    plot_left = margin
    plot_top = margin
    plot_right = W - margin
    plot_bottom = H - margin
    plot_width = plot_right - plot_left
    plot_height = plot_bottom - plot_top

    ideal_bin_w = plot_width / max(1, bins)
  
    bar_w = bar_w_arg

    step = 1
    total_needed = bar_w * bins
    if total_needed > plot_width:
        step = max(1, int(np.ceil(total_needed / plot_width)))
        
    for i in range(0, bins, step):
        v = float(h[i])
        if v <= 0.0:
            continue
        hpx = int((v / vmax) * plot_height)
        if hpx <= 0:
            continue

        x_center = plot_left + i * ideal_bin_w + ideal_bin_w / 2.0
        x0 = int(round(x_center - bar_w / 2.0))
        x1 = int(round(x_center + bar_w / 2.0))
        x0 = max(plot_left, min(x0, plot_right - 1))
        x1 = max(x0 + 1, min(x1, plot_right))

        y1 = plot_bottom
        y0 = max(plot_top, y1 - hpx)
        draw.rectangle([x0, y0, x1, y1], fill=bar_color)

    return img_out
