% UNIVERSIDADE FEDERAL DO AMAZONAS
% FACULDADE DE TECNOLOGIA
% GPRP&O - GRUPO DE PESQUISA EM RECONHECIMENTO DE PADRÕES E OTIMIZAÇÃO
% PGENE523 - PROCESSAMENTO DIGITAL DE IMAGENS
% SEMNINÁRIO - Watershed Segmentation
% ARQUIVO - main.m
% AUTOR - Diego Giovanni de Alcântara Vieira
%--------------------------------------------------------------------------
% Esse script demonstra o funcionamento da segmentação watershed 2D usando 
% as funções de alto nível do MATLAB em uma imagem de 3 canais
%--------------------------------------------------------------------------
clc; clear; close all;

% Leia a imagem
img = imread('water_coins.jpg');
% Converta para escala de cinza
gray_img = rgb2gray(img);

% Binarize a imagem usando um limiar automático
bw = imbinarize(gray_img);

% Preenchimento de buracos em objetos binarizados
bw = imfill(bw, 'holes');

% Remova pequenos objetos
bw = bwareaopen(bw, 50);

% Mostre a imagem binária
figure;
imshow(bw);
title('Imagem Binária com Objetos Sobrepostos');

% Calcule a transformação de distância
D = bwdist(~bw);
figure;
imshow(D, []);
title('Transformação de Distância da Imagem Binária');

% Calcule o complemento da transformação de distância
D = -D;
figure;
imshow(D, []);
title('Complemento da Transformação de Distância');

% Aplique a segmentação watershed
L = watershed(D);
L(~bw) = 0;

% Converta a imagem rotulada para RGB
rgb = label2rgb(L, 'jet', [.5 .5 .5]);
figure;
imshow(rgb);
title('Transformação Watershed');

% Sobreponha as linhas de segmentação à imagem original
segmented_img = imoverlay(img, L == 0, [1 0 0]); % L == 0 são as linhas de divisão do watershed

% Mostre a imagem segmentada final
figure;
imshow(segmented_img);
title('Imagem Original com Linhas de Segmentação Watershed');
