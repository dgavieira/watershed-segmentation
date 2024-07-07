import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import logging

# Adicionando o diretório pai ao path para permitir importações relativas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.inputs.read import imread
from src.channel.convert import rgb2gray
from src.filters.median import median_blur
from src.thresh.functions import threshold
from src.morph.functions import morphology_ex
from src.transforms.geometric import distance_transform
from src.segmentation.morphologic import watershed


# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Função para garantir que o diretório de saída existe
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


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
    blurred_image = median_blur(gray_image, 5)

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
    opening = morphology_ex(thresh, 'opening', kernel)

    # Salvar a imagem da área de fundo melhorada
    sure_bg_path = os.path.join(output_dir, 'sure_bg.jpg')
    plt.imsave(sure_bg_path, opening, cmap='gray')
    logging.info(f"Área de fundo melhorada salva em: {sure_bg_path}")

    # Aplicar a transformação de distância para a área segura
    dist_transform = distance_transform(opening)

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