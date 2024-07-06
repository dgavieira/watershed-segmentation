% UNIVERSIDADE FEDERAL DO AMAZONAS
% FACULDADE DE TECNOLOGIA
% GPRP&O - GRUPO DE PESQUISA EM RECONHECIMENTO DE PADRÕES E OTIMIZAÇÃO
% PGENE523 - PROCESSAMENTO DIGITAL DE IMAGENS
% SEMNINÁRIO - Watershed Segmentation
% ARQUIVO - watershed_high_level_2d.m
% AUTOR - Diego Giovanni de Alcântara Vieira
%--------------------------------------------------------------------------
% Esse script demonstra o funcionamento da segmentação watershed 2D usando 
% as funções de alto nível do MATLAB
%--------------------------------------------------------------------------
clc; clear; close all;
center1 = -40;
center2 = -center1;
dist = sqrt(2*(2*center1)^2);
radius = dist/2 * 1.4;
lims = [floor(center1-1.2*radius) ceil(center2+1.2*radius)];
[x,y] = meshgrid(lims(1):lims(2));
bw1 = sqrt((x-center1).^2 + (y-center1).^2) <= radius;
bw2 = sqrt((x-center2).^2 + (y-center2).^2) <= radius;
bw = bw1 | bw2;
figure;
imshow(bw)
title('Binary Image with Overlapping Objects')


D = bwdist(~bw);
figure;
imshow(D,[])
title('Distance Transform of Binary Image')

D = -D;
figure;
imshow(D,[])
title('Complement of Distance Transform')

L = watershed(D);
L(~bw) = 0;

rgb = label2rgb(L,'jet',[.5 .5 .5]);
figure;
imshow(rgb)
title('Watershed Transform')