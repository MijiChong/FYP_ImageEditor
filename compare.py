import os
import cv2
import numpy as np
import pandas as pd
from skimage.color import rgb2gray
from skimage.measure import shannon_entropy
import warnings

warnings.filterwarnings("ignore")

def compute_mad(img):
    """Compute the Median Absolute Deviation (MAD) for an image."""
    med = np.median(img)
    mad = np.median(np.abs(img - med))
    return mad

def extract_image_info(image_path):
    """Extract noise-related metrics, MAD, and Shannon Entropy from an image."""
    try:
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            raise Exception("Unable to load the image.")

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray = rgb2gray(img_rgb)

        # Shannon Entropy
        entropy = shannon_entropy(img_gray)
        
        # Median Absolute Deviation (MAD)
        mad = compute_mad(img_gray)
        
        # Calculate the noise level (standard deviation of pixel values)
        noise_level = np.std(img_gray)

        return {
            "Image_Name": os.path.basename(image_path),
            "Noise_Level": noise_level,
            "Shannon_Entropy": entropy,
            "MAD": mad
        }

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return {
            "Image_Name": os.path.basename(image_path),
            "Noise_Level": None,
            "Shannon_Entropy": None,
            "MAD": None
        }

def main():
    image_dir = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\1024nb\Big\85%n"  # Image directory
    order_csv = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\order.csv"   # Path to order.csv
    output_csv = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\image_quality85.csv"

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
                "Noise_Level": None,
                "Shannon_Entropy": None,
                "MAD": None
            }
        results.append(info)

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"\nImage quality data saved to: {output_csv}")

if __name__ == "__main__":
    main()
