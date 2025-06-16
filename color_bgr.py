import cv2
import numpy as np
import os

# Input folder with original images
image_folder = 'images'  # Replace with your folder name
output_folder = os.path.join(image_folder, 'output')
os.makedirs(output_folder, exist_ok=True)

# HSV range for light/white backgrounds
lower = np.array([0, 0, 200])
upper = np.array([180, 30, 255])

# Valid image extensions
valid_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

for filename in os.listdir(image_folder):
    if not filename.lower().endswith(valid_exts):
        continue

    image_path = os.path.join(image_folder, filename)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Skipping unreadable file: {filename}")
        continue

    print(f"Processing: {filename}")

    # Remove background
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    fg = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))
    bgra = cv2.cvtColor(fg, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = 255 - mask

    # Save to output folder with same name (as .png)
    base_name = os.path.splitext(filename)[0]
    out_path = os.path.join(output_folder, base_name + '.png')
    cv2.imwrite(out_path, bgra)

print("All images processed and saved in 'output/' folder.")
