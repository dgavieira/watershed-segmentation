import cv2
import numpy as np

if __name__ == '__main__':
    # Carregar a imagem

    image = cv2.imread('python/images/water_coins.jpg')
    rgb_image = image.copy()
    # Salvar a imagem original
    cv2.imwrite('python/images/original.jpg', rgb_image)

    # Converter para escala de cinza
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Salvar a imagem em escala de cinza
    cv2.imwrite('python/images/gray_image.jpg', gray_image)

    # Aplicar um filtro de suavização para reduzir o ruído
    gray_image = cv2.medianBlur(gray_image, 5)

    # Gerar a máscara de fundo utilizando a detecção de bordas
    ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Salvar a imagem da máscara de fundo
    cv2.imwrite('python/images/background_mask.jpg', thresh)

    # Aplicar o algoritmo de transformação morfológica para melhorar a máscara de fundo
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Encontrar a área certa da máscara de fundo
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Salvar a imagem do fundo certo
    cv2.imwrite('python/images/sure_bg.jpg', sure_bg)

    # Aplicar a transformação de distância para a área certa
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)

    # Aplicar o limite para encontrar a área de segurança
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

    # Salvar a imagem da área de segurança
    cv2.imwrite('python/images/sure_fg.jpg', sure_fg)

    # Encontrar a área desconhecida
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Salvar a imagem da área desconhecida
    cv2.imwrite('python/images/unknown.jpg', unknown)

    # Marcadores de localização para o watershed
    ret, markers = cv2.connectedComponents(sure_fg)

    # Adicionar um para todas as marcas para garantir que o fundo seja marcado com 0
    markers = markers + 1

    # Marcar a área desconhecida com 0
    markers[unknown == 255] = 0

    # Aplicar o algoritmo watershed
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255, 0, 0]

    # Salvar a imagem do resultado do watershed
    cv2.imwrite('python/images/watershed_result.jpg', image)