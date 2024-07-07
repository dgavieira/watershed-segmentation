import numpy as np
import logging
from tqdm import tqdm

def connected_components(image):
    # Encontrar componentes conectados
    logging.info("Encontrando componentes conectados")
    labeled_image = np.zeros_like(image)
    label = 1
    with tqdm(total=image.shape[0]*image.shape[1], desc='Encontrando componentes conectados') as pbar:
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if image[i, j] > 0 and labeled_image[i, j] == 0:
                    stack = [(i, j)]
                    while stack:
                        x, y = stack.pop()
                        if labeled_image[x, y] == 0:
                            labeled_image[x, y] = label
                            for dx in [-1, 0, 1]:
                                for dy in [-1, 0, 1]:
                                    if 0 <= x + dx < image.shape[0] and 0 <= y + dy < image.shape[1]:
                                        if image[x + dx, y + dy] > 0 and labeled_image[x + dx, y + dy] == 0:
                                            stack.append((x + dx, y + dy))
                    label += 1
                pbar.update(1)
    return labeled_image