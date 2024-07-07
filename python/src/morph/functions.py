import logging
from tqdm import tqdm
import numpy as np


def morphology_ex(image, op, kernel):
    # Aplicar operações morfológicas
    logging.info(f"Aplicando operação morfológica: {op}")
    if op == 'opening':
        return dilation(erode(image, kernel), kernel)
    elif op == 'dilation':
        return dilation(image, kernel)

def erode(image, kernel):
    # Erosão
    logging.info("Realizando erosão")
    output = np.zeros_like(image)
    kernel_size = kernel.shape[0]
    padded = np.pad(image, ((kernel_size // 2, kernel_size // 2), (kernel_size // 2, kernel_size // 2)), mode='constant')
    with tqdm(total=image.shape[0]*image.shape[1], desc='Realizando erosão') as pbar:
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                output[i, j] = np.min(padded[i:i + kernel_size, j:j + kernel_size] * kernel)
                pbar.update(1)
    return output

def dilation(image, kernel):
    # Dilatação
    logging.info("Realizando dilatação")
    output = np.zeros_like(image)
    kernel_size = kernel.shape[0]
    padded = np.pad(image, ((kernel_size // 2, kernel_size // 2), (kernel_size // 2, kernel_size // 2)), mode='constant')
    with tqdm(total=image.shape[0]*image.shape[1], desc='Realizando dilatação') as pbar:
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                output[i, j] = np.max(padded[i:i + kernel_size, j:j + kernel_size] * kernel)
                pbar.update(1)
    return output