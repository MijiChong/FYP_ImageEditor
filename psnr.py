import cv2
import numpy as np
import os
import csv
import pandas as pd
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
from skimage import img_as_float

class ImageQualityMetrics:
    def __init__(self, table_path: str, original_dir: str, blurred_dir: str):
        self.table_path = table_path
        self.original_dir = original_dir
        self.blurred_dir = blurred_dir
        self.results = []
        self.image_order = pd.read_csv(table_path)["Img_ID"].tolist()

    def load_image(self, path: str) -> np.ndarray:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")
        img = cv2.imread(path)
        if img is None:
            raise ValueError(f"Failed to load image: {path}")
        return img

    def calculate_psnr(self, img1: np.ndarray, img2: np.ndarray) -> float:
        mse = np.mean((img1 - img2) ** 2)
        if mse == 0:
            return 100.0
        max_pixel = 255.0
        return 20 * np.log10(max_pixel / np.sqrt(mse))

    def calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        img1_float = img_as_float(img1)
        img2_float = img_as_float(img2)
        win_size = min(img1_float.shape[:2]) // 8
        win_size = win_size if win_size % 2 == 1 else win_size - 1
        return ssim(img1_float, img2_float, data_range=img2_float.max() - img2_float.min(),
                    channel_axis=2, win_size=win_size)

    def process_images(self):
        for img_name in self.image_order:
            orig_path = os.path.join(self.original_dir, img_name)
            blur_path = os.path.join(self.blurred_dir, img_name)

            if not os.path.exists(orig_path) or not os.path.exists(blur_path):
                print(f"Skipping {img_name}: Missing file.")
                continue

            print(f"Processing: {img_name}")
            orig_img = self.load_image(orig_path)
            blur_img = self.load_image(blur_path)

            if orig_img.shape != blur_img.shape:
                blur_img = cv2.resize(blur_img, (orig_img.shape[1], orig_img.shape[0]))

            psnr_val = self.calculate_psnr(orig_img, blur_img)
            ssim_val = self.calculate_ssim(orig_img, blur_img)

            self.results.append({
                'image': img_name,
                'psnr': psnr_val,
                'ssim': ssim_val
            })

        self.save_results_csv()

    def save_results_csv(self, output_dir: str = "results"):
        os.makedirs(output_dir, exist_ok=True)
        csv_filename = f"image_quality_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_filepath = os.path.join(output_dir, csv_filename)

        with open(csv_filepath, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Image Name", "PSNR", "SSIM"])
            for result in self.results:
                csv_writer.writerow([result['image'], result['psnr'], result['ssim']])

        print(f"\nResults saved to: {csv_filepath}")

# Example usage
if __name__ == "__main__":
    table_path = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\order.csv"
    original_directory = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\FYP_NewORI"
    blurred_directory = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\800nb\pic\10%n"

    metrics = ImageQualityMetrics(table_path, original_directory, blurred_directory)
    metrics.process_images()
