import numpy as np
from collections import deque

CRITERIA = ["local", "global", "mean"]

def do_region_growing(img: np.ndarray, args: dict) -> np.ndarray:
    #Działamy na obrazach grayscale | binary
    if len(img.shape) > 2:
        img = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140]) 
        print("img shape" , img.shape)

    
    imgMax = np.max(img)
    if imgMax <= 1.0: #Binary detection scaling
        img = (img * 255).astype(np.float32)
    else:
        img = img.astype(np.float32)

    isBinary = len(np.unique(img)) <= 2
    
    #Seed (punkty startowe)
    # Oczekiwany format: "y1,x1;y2,x2;..."
    seeds_arg = args.get("-seeds", "")
    seeds = []
    if seeds_arg:
        try:
            parts = [s for s in seeds_arg.split(";") if s]
            seeds = [tuple(map(int, seed.split(","))) for seed in parts]
        except ValueError:
            print("Error: Invalid seed format. Expected 'y,x;y,x'")
            return img
    
    if not seeds:
        print("Error: No seeds provided.")
        return img

    threshold = int(args.get("-threshold", 7)) # Domyślny próg to 10
    criterion = args.get("-criterion", "local") # Kryterium podobieństwa
    
    if criterion not in CRITERIA:
        print(f"Error: Invalid criterion '{criterion}'. Choose from {CRITERIA}.")
        return img
        
    h, w = img.shape
    img_float = img
    
    # Nowy obraz:0 tło 1 obiekt
    segmentation_mask = np.zeros((h, w), dtype=np.uint8)
    
    # vistied[x, y] = odwiedzony piksel jeżeli True
    visited = np.zeros((h, w), dtype=bool)
    
    queue = deque()
    seed_values = [] #Dla global 
    region_sum = 0.0 #Dla mean
    region_count = 0 #Dla mean
    print("Seeds:", seeds)
    print("Criterion:", criterion)
    print("Threshold:", threshold)
    
    for seed in seeds:
        y, x = seed
        # Sprawdzenie, czy ziarno mieści się w obrazie
        if 0 <= y < h and 0 <= x < w:
            queue.append((y, x))
            visited[y, x] = True
            segmentation_mask[y, x] = 1
            region_sum += img_float[y, x]
            region_count += 1
            seed_values.append(img_float[y, x])
        else:
            print(f"Warning: Seed point {seed} is out of image bounds.")
            continue

    # Sąsiedzi (krzyż)
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    base_seed_value = sum(seed_values) / len(seed_values) if seed_values else 0.0

    while queue:
            cy, cx = queue.popleft()
        
            current_val = img_float[cy, cx]

            for dy, dx in neighbors:
                ny = cy + dy
                nx = cx + dx

                if 0 <= ny < h and 0 <= nx < w:
                    if not visited[ny, nx]:
                        neighbor_val = img_float[ny, nx]
                        diff = 0.0
                        
                        if criterion == "local":
                            diff = abs(neighbor_val - current_val)
                        elif criterion == "global":
                            diff = abs(base_seed_value - neighbor_val)
                        elif criterion == "mean":
                            region_mean = region_sum / region_count if region_count > 0 else 0.0
                            diff = abs(neighbor_val - region_mean)
                        
                        if diff <= threshold:
                            # Jeśli sąsiad jest podobny  dodajemy do regionu
                            segmentation_mask[ny, nx] = 1
                            visited[ny, nx] = True
                            queue.append((ny, nx))
                            if criterion == "mean":
                                region_sum += neighbor_val
                                region_count += 1
    if isBinary:
        return segmentation_mask
    else:
        return segmentation_mask * 255