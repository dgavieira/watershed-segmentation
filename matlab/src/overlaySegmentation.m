function segmented_img = overlaySegmentation(img, L)
    % Sobreponha as linhas de segmentação à imagem original
    segmented_img = imoverlay(img, L == 0, [1 0 0]); % L == 0 são as linhas de divisão do watershed
end

