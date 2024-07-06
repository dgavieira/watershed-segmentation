function bw = fillHoles(bw)
    % Preenchimento de buracos em objetos binarizados
    bw = imfill(bw, 'holes');
end
