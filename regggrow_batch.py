import os
from input_output import load_image, save_image
from commands.region_growing import do_region_growing
import numpy as np

raw_seeds = [
    (370, 390), (440, 418),  #(351, 441)
]
seeds_string = ";".join([f"{y},{x}" for y, x in raw_seeds])

# Parametry z tabeli w zadaniu
criteria_list = ["local", "global", "mean"]
thresholds_list = [50, 60, 70, 80]

# Folder na wyniki
output_dir = "wyniki_ct"
os.makedirs(output_dir, exist_ok=True)

# Wczytanie obrazu
try:
    original_img = load_image("./images/tomography.bmp") # Ścieżka do Twojego pliku
    print("Obraz załadowany poprawnie.")
except Exception as e:
    print(f"Błąd wczytywania: {e}. Upewnij się, że plik './images/tomography.bmp' istnieje.")
    original_img = np.zeros((512, 512), dtype=np.uint8) 

# --- 4. GŁÓWNA PĘTLA GENERUJĄCA OBRAZY ---

print(f"Generowanie 9 obrazów do folderu '{output_dir}/'...")

for i, crit in enumerate(criteria_list):
    for j, thresh in enumerate(thresholds_list):
        
        # Ustawienia argumentów
        args = {
            "-seeds": seeds_string,
            "-threshold": thresh,
            "-criterion": crit
        }
        
        # Wykonanie segmentacji
        mask = do_region_growing(original_img, args)
        
        # Nazwa pliku: np. global_t7.png
        filename = f"{crit.strip('-')}_t{thresh}.png"
        save_path = os.path.join(output_dir, filename)
        
        # Zapis samego obrazka (maski)
        save_image(save_path, mask)
        print(f"-> Zapisano: {filename}")
        

print("\nGotowe! Obrazy znajdują się w folderze 'wyniki_ct'.")