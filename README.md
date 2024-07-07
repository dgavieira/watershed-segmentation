# Watershed Segmentation

- Autor: Diego Giovanni de Alcântara Vieira

- PGENE523 - Digital Image Processing

- PPGEE - Post Graduate Program in Electrical Engineering

- UFAM - Federal University of Amazonas

# Repository Structure

- `matlab` - MATLAB code using Image Processing Toolbox functions
    - `examples`
      - `main.m` - example applying watershed segmentation to a given image.
      - `watershed_high_level_2d.m` - example applying watershed segmentation to a 2-dimensional binary image written on the file.
      - `watershed_high_level_3d.m` - example applying watershed segmentation to a 3-dimensional figure written on the file.
    - `src` - each function needed on the watershed segmentation process.
      - `applyWatershed` - apply watershed segmentation
      - `binarizeImage` - apply binarization using Otsu Method
      - `calculateComplementeDistanceTransform` - computes the complement of the distance transform
      - `calculateDistanceTransform` - computes distance transform
