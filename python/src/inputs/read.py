import logging
import matplotlib.pyplot as plt

def imread(filename):
    # Carregar imagem RGB
    logging.info(f"Carregando imagem: {filename}")
    return plt.imread(filename)