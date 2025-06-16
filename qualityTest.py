import os
import cv2
import numpy as np
import pandas as pd
from skimage.color import rgb2gray
from skimage.measure import shannon_entropy
import warnings

warnings.filterwarnings("ignore")

def extract_image_info(image_path):
    """Extract key image quality metrics from an image."""
    try:
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            raise Exception("Unable to load the image.")

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray = rgb2gray(img_rgb)

        height, width, _ = img_rgb.shape
        aspect_ratio = round(width / height, 2)
        brightness = img_gray.mean()
        Gx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0)
        Gy = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1)
        sharpness = np.mean(Gx**2 + Gy**2)
        noise_level = shannon_entropy(img_gray)
        # noise_level = np.std(img_gray)
        color_depth = img_rgb.dtype.itemsize * 8


        return {
            "Image_Name": os.path.basename(image_path),
            "Width": width,
            "Height": height,
            "Aspect_Ratio": aspect_ratio,
            "Brightness": brightness,
            "Sharpness_Sobel": sharpness,
            "Noise_Level": noise_level,
            "Color_Depth": color_depth
        }

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return {
            "Image_Name": os.path.basename(image_path),
            "Width": None,
            "Height": None,
            "Aspect_Ratio": None,
            "Brightness": None,
            "Sharpness_Sobel": None,
            "Noise_Level": None,
            "Color_Depth": None
        }

def main():
    image_dir = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\1024nb\Big\90%n"  # Image directory
    order_csv = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\order.csv"   # Path to order.csv
    output_csv = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\image_quality.csv"

    # Read the image filenames in order
    try:
        ordered_df = pd.read_csv(order_csv)
        image_list = ordered_df['Img_ID'].tolist()
    except Exception as e:
        print(f"Failed to read order.csv: {e}")
        return

    results = []

    for filename in image_list:
        image_path = os.path.join(image_dir, filename)
        if os.path.exists(image_path):
            info = extract_image_info(image_path)
        else:
            print(f"File not found: {image_path}")
            info = {
                "Image_Name": filename,
                "Width": None,
                "Height": None,
                "Aspect_Ratio": None,
                "Brightness": None,
                "Sharpness": None,
                "Noise_Level": None,
                "Color_Depth": None,
            }
        results.append(info)

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"\nImage quality data saved to: {output_csv}")

if __name__ == "__main__":
    main()
