import logging
import numpy as np


def rgb2gray(image):
    # Converter imagem para escala de cinza usando média ponderada
    logging.info("Convertendo imagem para escala de cinza")
    return np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])