from PIL import Image, ImageDraw
import numpy as np
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
    ch         = args.get('-channel', 'y').lower()
    num_bins   = 256
    plot_h     = int(args.get('-height', '200'))
    plot_w     = int(args.get('-width',  str(num_bins)))
    bar_color  = args.get('-color', 'black')
    axis_color = args.get('-axiscolor', 'red')
    bg_color   = args.get('-bgcolor', 'white')
    margin     = int(args.get('-border', '10'))   #

    chan = extract_channel(img, ch)  # powinien zwrócić 2D ndarray
    if chan.ndim != 2:
        raise ValueError("Channel extraction did not return a 2D array.")

    h, cdf, n = compute_histogram(chan.astype(np.uint8), num_bins)
    if n == 0 or len(h) == 0:
        return Image.new("RGB", (plot_w, plot_h), bg_color)

    inner_w = max(1, plot_w - 2 * margin)
    inner_h = max(1, plot_h - 2 * margin)

    # --- krok i szerokość słupka ---
    bar_w = 1
    auto_step = max(1, inner_w // num_bins)


    h_max = max(int(x) for x in h)
    scale = inner_h / h_max if h_max > 0 else 1.0

    # --- płótno i rysowanie ---
    canvas = Image.new("RGB", (plot_w, plot_h), bg_color)
    draw = ImageDraw.Draw(canvas)

    baseline_y = plot_h - margin  # oś X 
    x = margin

    draw.line([(margin, baseline_y), (plot_w - margin, baseline_y)], fill=axis_color)

    for i in range(min(num_bins, len(h))):
        height_px = int(round(h[i] * scale))
        top_y = baseline_y - height_px

        top_y = max(margin, top_y)

        x1 = min(plot_w - margin, x + bar_w)

        if x < plot_w - margin and height_px > 0:
            draw.rectangle([ (x, top_y), (x1-1, baseline_y-1) ], outline=bar_color)

        x += auto_step
        if x >= plot_w - margin:
            break  

    return canvas
