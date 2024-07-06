function L = applyWatershed(D, bw)
    % Aplique a segmentação watershed
    L = watershed(D);
    L(~bw) = 0;
end