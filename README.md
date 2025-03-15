# GPU-Accelerated Batch Image Blurring Using CUDA  

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

Note: Images taken from https://sipi.usc.edu/database/database.php?volume=aerials
