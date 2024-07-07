import logging
import numpy as np
from tqdm import tqdm


def watershed(image, markers):
    # Aplicar algoritmo watershed
    logging.info("Aplicando algoritmo watershed")
    rows, cols, _ = image.shape
    result = np.zeros((rows, cols, 3), dtype=np.uint8)
    for i in tqdm(range(rows), desc='Aplicando algoritmo watershed'):
        for j in range(cols):
            if markers[i, j] == -1:
                result[i, j] = [255, 0, 0]
            else:
                result[i, j] = image[i, j]
    return result