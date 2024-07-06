clc; clear; close all;

% Leia a imagem
img = imread('water_coins.jpg');

% Converta para escala de cinza
gray_img = rgb2gray(img);

% Binarize a imagem
bw = binarizeImage(gray_img);

% Preenchimento de buracos
bw = fillHoles(bw);

% Remova pequenos objetos
bw = removeSmallObjects(bw, 50);

% Mostre a imagem binária
figure;
imshow(bw);
title('Imagem Binária com Objetos Sobrepostos');

% Calcule a transformação de distância
D = calculateDistanceTransform(bw);
figure;
imshow(D, []);
title('Transformação de Distância da Imagem Binária');

% Calcule o complemento da transformação de distância
D = calculateComplementDistanceTransform(D);
figure;
imshow(D, []);
title('Complemento da Transformação de Distância');

% Aplique a segmentação watershed
L = applyWatershed(D, bw);

% Converta a imagem rotulada para RGB
rgb = label2rgb(L, 'jet', [.5 .5 .5]);
figure;
imshow(rgb);
title('Transformação Watershed');

% Sobreponha as linhas de segmentação à imagem original
segmented_img = overlaySegmentation(img, L);

% Mostre a imagem segmentada final
figure;
imshow(segmented_img);
title('Imagem Original com Linhas de Segmentação Watershed');

