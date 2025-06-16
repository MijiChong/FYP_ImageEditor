import os
import pandas as pd
from PIL import Image
import numpy as np

# Set your paths
image_dir = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\pixel\ori'  # directory where images are stored
order_csv_path = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\newOrder.csv'  # the CSV containing Img_ID column
output_csv_path = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\image_pixels.csv'  # output file

# Load the image order
order_df = pd.read_csv(order_csv_path)

# Function to get image dimensions as a string
def get_image_size_string(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return f"{width}X{height}"

# Collect image sizes
pixel_info = []

for img_name in order_df['Img_ID']:
    full_path = os.path.join(image_dir, img_name)
    if os.path.exists(full_path):
        size_str = get_image_size_string(full_path)
        pixel_info.append({'Img_ID': img_name, 'PIXEL': size_str})
    else:
        print(f"Image not found: {full_path}")
        pixel_info.append({'Img_ID': img_name, 'PIXEL': ''})  # blank if missing

# Create final DataFrame
output_df = pd.DataFrame(pixel_info)

# Save to CSV
output_df.to_csv(output_csv_path, index=False)
print(f"CSV saved to: {output_csv_path}")

