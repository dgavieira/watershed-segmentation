import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # Importar tqdm para barras de progresso
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Função para garantir que o diretório de saída existe
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def imread(filename):
    # Carregar imagem RGB
    logging.info(f"Carregando imagem: {filename}")
    return plt.imread(filename)

def rgb2gray(image):
    # Converter imagem para escala de cinza usando média ponderada
    logging.info("Convertendo imagem para escala de cinza")
    return np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])

def medianBlur(image, ksize):
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

def threshold(image, thresh, maxval):
    # Aplicar limiarização
    logging.info(f"Aplicando limiarização com valor de thresh={thresh} e maxval={maxval}")
    return np.where(image > thresh, maxval, 0)

def morphologyEx(image, op, kernel):
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

def distanceTransform(image):
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

def connectedComponents(image):
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

# Função principal para executar o processo completo
def main(filename):
    # Carregar imagem
    logging.info(f"Iniciando processamento da imagem: {filename}")
    rgb_image = imread(filename)

    # Criar diretório para salvar imagens, se não existir
    output_dir = 'python/images/'
    ensure_dir(output_dir)

    # Salvar a imagem original
    original_path = os.path.join(output_dir, 'original.jpg')
    plt.imsave(original_path, rgb_image)
    logging.info(f"Imagem original salva em: {original_path}")

    # Converter para escala de cinza
    gray_image = rgb2gray(rgb_image)

    # Salvar a imagem em escala de cinza
    gray_path = os.path.join(output_dir, 'gray_image.jpg')
    plt.imsave(gray_path, gray_image, cmap='gray')
    logging.info(f"Imagem em escala de cinza salva em: {gray_path}")

    # Aplicar filtro de mediana para suavização
    blurred_image = medianBlur(gray_image, 5)

    # Salvar a imagem suavizada
    blurred_path = os.path.join(output_dir, 'blurred_image.jpg')
    plt.imsave(blurred_path, blurred_image, cmap='gray')
    logging.info(f"Imagem suavizada salva em: {blurred_path}")

    # Aplicar limiarização para obter a máscara de fundo
    thresh = threshold(blurred_image, 100, 255)

    # Salvar a imagem da máscara de fundo
    mask_path = os.path.join(output_dir, 'background_mask.jpg')
    plt.imsave(mask_path, thresh, cmap='gray')
    logging.info(f"Máscara de fundo salva em: {mask_path}")

    # Aplicar operações morfológicas para melhorar a máscara de fundo
    kernel = np.ones((3, 3), dtype=np.uint8)
    opening = morphologyEx(thresh, 'opening', kernel)

    # Salvar a imagem da área de fundo melhorada
    sure_bg_path = os.path.join(output_dir, 'sure_bg.jpg')
    plt.imsave(sure_bg_path, opening, cmap='gray')
    logging.info(f"Área de fundo melhorada salva em: {sure_bg_path}")

    # Aplicar a transformação de distância para a área segura
    dist_transform = distanceTransform(opening)

    # Salvar a imagem da transformação de distância
    dist_transform_path = os.path.join(output_dir, 'distance_transform.jpg')
    plt.imsave(dist_transform_path, dist_transform, cmap='gray')
    logging.info(f"Transformação de distância salva em: {dist_transform_path}")

    # Aplicar limiarização na transformação de distância para obter marcadores
    markers = threshold(dist_transform, 20, 255)

    # Salvar a imagem dos marcadores
    markers_path = os.path.join(output_dir, 'markers.jpg')
    plt.imsave(markers_path, markers, cmap='gray')
    logging.info(f"Marcadores salvos em: {markers_path}")

    # Aplicar algoritmo watershed com base nos marcadores
    result = watershed(rgb_image, markers)

    # Salvar a imagem do resultado do watershed
    watershed_result_path = os.path.join(output_dir, 'watershed_result.jpg')
    plt.imsave(watershed_result_path, result)
    logging.info(f"Resultado do watershed salvo em: {watershed_result_path}")
    logging.info("Processamento concluído!")

    # Retornar os caminhos das imagens geradas
    return {
        'original': original_path,
        'gray_image': gray_path,
        'blurred_image': blurred_path,
        'background_mask': mask_path,
        'sure_background': sure_bg_path,
        'distance_transform': dist_transform_path,
        'markers': markers_path,
        'watershed_result': watershed_result_path
    }

def generate_html(images_paths):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Resultado do Processamento de Imagem</title>
    <style>
    .image-container {
        display: inline-block;
        margin: 10px;
    }
    </style>
    </head>
    <body>
    <h1>Resultado do Processamento de Imagem</h1>
    """

    for name, path in images_paths.items():
        html_content += f"<div class='image-container'><h3>{name}</h3><img src='{path}'></div>"

    html_content += """
    </body>
    </html>
    """

    with open('python/images/result.html', 'w') as file:
        file.write(html_content)

# Executar o processo principal
if __name__ == "__main__":
    images_paths = main('python/images/water_coins.jpg')
    generate_html(images_paths)
    print("Arquivo HTML gerado com sucesso: python/images/result.html")