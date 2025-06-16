import cv2
import sys
import os
import numpy as np

def apply_gaussian_blur(image_path, blur_percent, output_folder):
    """Apply Gaussian blur to an image and save it to a new directory."""
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read the image {image_path}")
        return
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Determine max reasonable kernel size (10% of smaller dimension, must be odd)
    max_kernel = (min(height, width) // 10) | 1  # Ensure odd number
    
    # Compute kernel size based on blur percentage
    kernel_size = int((blur_percent / 100) * max_kernel)
    kernel_size = max(3, kernel_size | 1)  # Ensure minimum size of 3 and odd number
    
    print(f"Processing: {image_path}")
    print(f"Original Image Size: {width}x{height}")
    print(f"Using Kernel Size: {kernel_size}x{kernel_size}")
    
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Save blurred image to the "blur" folder
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, blurred_image)

    print(f"Blurred image saved as {output_path}\n")

def process_images_in_folder(folder_path, blur_percent):
    """Process all images in a given folder and save them to 'blur' directory."""
    if not os.path.exists(folder_path):
        print(f"Error: The provided folder '{folder_path}' does not exist.")
        return

    output_folder = os.path.join(folder_path, "blur")  # Create "blur" directory inside the original folder

    files_found = False  # Track if images are found
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            apply_gaussian_blur(image_path, blur_percent, output_folder)
            files_found = True
        else:
            print(f"Skipping: {filename}")  # Debugging line

    if not files_found:
        print("No valid image files found in the folder.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python gaussian.py <image_directory> <blur_percentage>")
    else:
        folder_path = sys.argv[1]
        blur_percentage = float(sys.argv[2])
        process_images_in_folder(folder_path, blur_percentage)

# Way to run: python gaussian.py path/to/image_folder 50

