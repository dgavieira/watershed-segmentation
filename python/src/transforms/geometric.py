import logging
from tqdm import tqdm
import numpy as np

def distance_transform(image):
    # Aplicar transformação de distância
    logging.info("Aplicando transformação de distância")
    rows, cols = image.shape
    dist_transform = np.zeros((rows, cols))
    for i in tqdm(range(rows), desc='Aplicando transformação de distância'):
        for j in range(cols):
            if image[i, j] == 0:
                min_dist = np.inf
                for k in range(rows):
                    for l in range(cols):
                        if image[k, l] > 0:
                            dist = np.sqrt((k - i)**2 + (l - j)**2)
                            if dist < min_dist:
                                min_dist = dist
                dist_transform[i, j] = min_dist
    return dist_transform