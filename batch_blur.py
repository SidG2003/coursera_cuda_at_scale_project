# -*- coding: utf-8 -*-
"""gpu3_proj.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1klLQIwQo5HdnCfA47cNb0JwGMo6BvMbT

##GPU-Accelerated Batch Image Blurring Using CUDA

Readme.md:
## Project Overview  
This project demonstrates **GPU-accelerated image processing** by applying a **Gaussian blur** to a batch of images using **CUDA and Numba**. The program loads images from a folder, processes them in parallel on the GPU, and saves the blurred images to an output folder.  

## Features  
Uses **CUDA GPU parallelization** via **Numba**  
Applies **Gaussian blur** to multiple images efficiently  
Processes **100s of small or 10s of large images**  
Saves the output images automatically  

## Requirements  
- Python 3.x  
- Numba  
- OpenCV  
- CUDA-enabled GPU  

## Installation  
1. Install dependencies:  
   ```bash
   pip install numpy opencv-python numba

2. Ensure CUDA is installed and properly configured.

## Usage
1. Prepare input images
Place images inside the input_images/ folder.

2. Run the script
   ```bash
   python batch_blur.py

3. Check output images
Processed images will be saved in output_images/ folder.
"""

import numpy as np
import cv2
import os
from numba import cuda

# CUDA Kernel for Gaussian Blur
@cuda.jit
def gaussian_blur_kernel(input_image, output_image, width, height):
    x, y = cuda.grid(2)
    if x >= width or y >= height:
        return

    kernel_size = 3
    kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16.0
    half_k = kernel_size // 2
    pixel_value = 0.0

    for ky in range(-half_k, half_k + 1):
        for kx in range(-half_k, half_k + 1):
            nx, ny = x + kx, y + ky
            if 0 <= nx < width and 0 <= ny < height:
                pixel_value += input_image[ny, nx] * kernel[ky + half_k, kx + half_k]

    output_image[y, x] = pixel_value

# Function to process a single image
def process_image(image_path, output_folder):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Failed to load {image_path}")
        return

    height, width = img.shape
    d_input = cuda.to_device(img.astype(np.float32))
    d_output = cuda.device_array((height, width), dtype=np.float32)

    threads_per_block = (16, 16)
    blocks_per_grid_x = (width + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (height + threads_per_block[1] - 1) // threads_per_block[1]
    gaussian_blur_kernel[(blocks_per_grid_x, blocks_per_grid_y), threads_per_block](d_input, d_output, width, height)

    blurred_image = d_output.copy_to_host().astype(np.uint8)

    # Ensure the output is saved as JPG
    base_filename = os.path.splitext(os.path.basename(image_path))[0]  # Remove extension
    output_path = os.path.join(output_folder, base_filename + ".jpg")

    cv2.imwrite(output_path, blurred_image)
    print(f"Processed: {image_path} -> {output_path}")

# Batch process all images in a folder
def batch_process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".png", ".bmp", ".tiff", ".tif")):  # Accept all formats
            input_path = os.path.join(input_folder, filename)
            process_image(input_path, output_folder)

# Run batch processing
input_folder = "input_images"
output_folder = "output_images"
batch_process_images(input_folder, output_folder)