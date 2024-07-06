function bw = removeSmallObjects(bw, min_size)
    % Remova pequenos objetos manualmente
    bw = bwareaopen(bw, min_size);
end

