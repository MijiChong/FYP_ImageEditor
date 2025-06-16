from PIL import Image
import os

# --- Settings ---
input_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\pixel\1024\pie'
output_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\pixel\128'

resize_to = 128           # The size you want to resize (applied to width or height)
resize_side = 'width'      # Choose 'width' or 'height' to apply resizing on

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Supported image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        original_width, original_height = img.size
        aspect_ratio = original_width / original_height  # width-to-height ratio

        if resize_side == 'width':
            new_width = resize_to
            new_height = int(new_width / aspect_ratio)
        elif resize_side == 'height':
            new_height = resize_to
            new_width = int(new_height * aspect_ratio)
        else:
            raise ValueError("resize_side must be either 'width' or 'height'")

        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save to output folder
        output_path = os.path.join(output_folder, filename)
        resized_img.save(output_path)

        print(f"{filename} resized to: {new_width}x{new_height} (original ratio preserved)")
