import logging
import numpy as np
from tqdm import tqdm

def median_blur(image, ksize):
    # Aplicar filtro de mediana para suavização
    logging.info(f"Aplicando filtro de mediana com tamanho do kernel {ksize}")
    padded = np.pad(image, ((ksize // 2, ksize // 2), (ksize // 2, ksize // 2)), mode='constant')
    output = np.zeros_like(image)
    with tqdm(total=image.shape[0]*image.shape[1], desc='Aplicando filtro de mediana') as pbar:
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                output[i, j] = np.median(padded[i:i + ksize, j:j + ksize])
                pbar.update(1)
    return output