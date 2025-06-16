from PIL import Image
import os

# --- Settings ---
input_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\pixel\1024\pie'       # Folder with original images
output_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\pixel\1024'    # Folder to save resized images
target_size = (800, 800)            # Desired size (width, height)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Resize the image using LANCZOS (high-quality resampling)
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Save to output folder
        output_path = os.path.join(output_folder, filename)
        resized_img.save(output_path)

        print(f"Resized and saved: {filename}")
