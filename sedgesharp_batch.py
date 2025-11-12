from input_output import load_image, save_image
import csv
from pathlib import Path

import numpy as np
from commands.sedghesharp import do_sedghesharp

from commands.image_characteristics.cmean import do_cmean
from commands.image_characteristics.cvariance import do_cvariance
from commands.image_characteristics.cstdev import do_cstdev
from commands.image_characteristics.cvarcoi import do_cvarcoi
from commands.image_characteristics.cvarcoii import do_cvarcoii
from commands.image_characteristics.casyco import do_casyco
from commands.image_characteristics.cflattening import do_cflattening
from commands.image_characteristics.centropy import do_centropy

IMG_PATH = "./images/lenac.bmp"
OUT_DIR = Path("./test_folder/")
CSV_PATH = OUT_DIR / "metrics_sedghesharp.csv"

KERNELS = ["K1", "K2", "K3"]  


METRICS = [
    ("cmean",      do_cmean),
    ("cvariance",  do_cvariance),
    ("cstdev",     do_cstdev),
    ("cvarcoi",    do_cvarcoi),
    ("cvarcoii",   do_cvarcoii),
    ("casyco",     do_casyco),
    ("cflattening",do_cflattening),
    ("centropy",   do_centropy),
]

def compute_all_metrics(img) -> dict[str, float]:
    """Liczy wszystkie metryki dla obrazu i zwraca dict {nazwa: wartosc}."""
    out = {}
    for name, fn in METRICS:
        try:
            v = float(fn(img, {}))
        except Exception as e:
            # Jak coś padnie (np. dzielenie przez 0), nie wywracaj batcha
            v = float("nan")
        out[name] = v
    return out

def main():
    original = load_image(IMG_PATH)
    base_metrics = compute_all_metrics(original)
    print("DEBUG")

    # przygotuj CSV
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "kernel",
            "metric",
            "original",
            "sharpened",
            "delta(sharp-original)"
        ])

        for k in KERNELS:
            sharpened = do_sedghesharp(original, {"kernel": k})

            sharp_metrics = compute_all_metrics(sharpened)

            for metric_name, _ in METRICS:
                orig_v = base_metrics[metric_name]
                sharp_v = sharp_metrics[metric_name]
                delta = (sharp_v - orig_v
                         if not (np.isnan(sharp_v) or np.isnan(orig_v))
                         else float("nan"))
                writer.writerow([k, metric_name, orig_v, sharp_v, delta])
    print(f"\n== Base (original) metrics for: {IMG_PATH} ==")
    for m in METRICS:
        name = m[0]
        print(f"{name:>12}: {base_metrics[name]: .6f}")

    from collections import defaultdict
    per_kernel = defaultdict(dict)
    with open(CSV_PATH, "r", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            per_kernel[row["kernel"]][row["metric"]] = (
                float(row["original"]),
                float(row["sharpened"]),
                float(row["delta(sharp-original)"])
            )

    for k in KERNELS:
        print(f"\n== Kernel {k} ==")
        for metric_name, _ in METRICS:
            o, s, d = per_kernel[k][metric_name]
            print(f"{metric_name:>12}: orig={o: .6f}  sharp={s: .6f}  Δ={d: .6f}")

    print(f"\nCSV zapisany: {CSV_PATH}")

if __name__ == "__main__":
    main()
