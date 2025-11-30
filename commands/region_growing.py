import numpy as np
from collections import deque

def do_region_growing(img: np.ndarray, args: dict) -> np.ndarray:
    #Działamy na obrazach grayscale | binary
    if len(img.shape) != 2:
        print("Error: Region Growing requires a GRAYSCALE | binary image.")
        return img
    isBinary = len(np.unique(img)) <= 2
    #Seed (punkty startowe)
    # Oczekiwany format: "y1,x1;y2,x2;..."
    print("Arguments received for region growing:", args)
    seeds = args.get("-seeds", "")
    seeds = seeds.split(";")
    seeds = [tuple(map(int, seed.split(","))) for seed in seeds]
    threshold = int(args.get("-threshold", 7)) # Domyślny próg to 10
    print(args)
    h, w = img.shape
    
    
    img_float = img.astype(np.float32)
    
    # 0 tło 1 obiekt
    segmentation_mask = np.zeros((h, w), dtype=np.uint8)
    
    # Macierz odwiedzonych punktów, żeby nie zapętlić algorytmu
    visited = np.zeros((h, w), dtype=bool)
    
    # Kolejka do algorytmu BFS
    queue = deque()
    
    # 2. Inicjalizacja ziaren (Seeds)
    for seed in seeds:
        x, y = seed
        # Sprawdzenie, czy ziarno mieści się w obrazie
        if 0 <= y < h and 0 <= x < w:
            queue.append((y, x))
            visited[y, x] = True
            segmentation_mask[y, x] = 1
        else:
            print(f"Warning: Seed point {seed} is out of image bounds.")
            return img

    # Sąsiedzi (krzyż)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 3. Główna pętla (Rozrost)
    while queue:
        cy, cx = queue.popleft()
        
        # Wartość aktualnego piksela (punktu odniesienia)
        current_val = img_float[cy, cx]

        for dy, dx in neighbors:
            ny = cy + dy
            nx = cx + dx

            # Sprawdzenie granic obrazu
            if 0 <= ny < h and 0 <= nx < w:
                if not visited[ny, nx]:
                    neighbor_val = img_float[ny, nx]
                    
                    # 4. Kryterium (Similarity Criterion)
                    # Obliczamy różnicę jasności między aktualnym pikselem a sąsiadem
                    diff = abs(current_val - neighbor_val)
                    
                    if diff <= threshold:
                        # Jeśli sąsiad jest podobny -> dodajemy do regionu
                        segmentation_mask[ny, nx] = 1
                        visited[ny, nx] = True
                        queue.append((ny, nx))
                    else:
                        # Jeśli nie pasuje -> oznaczamy jako odwiedzony, ale nie dodajemy do regionu
                        # (żeby nie sprawdzać go ponownie bez sensu)
                        visited[ny, nx] = True

    # Zwracamy maskę przeskalowaną do 0-255 (standard wyświetlania)

    if isBinary:
        return segmentation_mask
    else:
        return segmentation_mask * 255