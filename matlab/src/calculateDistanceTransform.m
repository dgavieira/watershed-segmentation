function D = calculateDistanceTransform(bw)
    % Calcule a transformação de distância
    D = bwdist(~bw);
end