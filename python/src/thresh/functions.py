import logging
import numpy as np

def threshold(image, thresh, maxval):
    # Aplicar limiarização
    logging.info(f"Aplicando limiarização com valor de thresh={thresh} e maxval={maxval}")
    return np.where(image > thresh, maxval, 0)