import cv2
import numpy as np
import os

# Paths
base_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\overlay\g1'
overlay_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\overlay\g2'
output_folder = r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\overlay\composited'
os.makedirs(output_folder, exist_ok=True)

# Define HSV range for white
lower = np.array([0, 0, 200])
upper = np.array([180, 30, 255])

# Transparency level (0 = fully transparent, 1 = fully visible)
overlay_opacity = 0.7 # 0 < level < 1

image_names = sorted(set(os.listdir(base_folder)).intersection(os.listdir(overlay_folder)))

for name in image_names:
    if not name.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    base_path = os.path.join(base_folder, name)
    overlay_path = os.path.join(overlay_folder, name)
    output_path = os.path.join(output_folder, os.path.splitext(name)[0] + '.png')

    base = cv2.imread(base_path)
    overlay = cv2.imread(overlay_path)

    if base is None or overlay is None:
        print(f"Skipping {name}, could not load both images.")
        continue

    # Resize
    overlay = cv2.resize(overlay, (base.shape[1], base.shape[0]))

    # Create mask for non-white areas in overlay
    hsv = cv2.cvtColor(overlay, cv2.COLOR_BGR2HSV)
    white_mask = cv2.inRange(hsv, lower, upper)
    non_white_mask = cv2.bitwise_not(white_mask)

    # Normalize the mask to float in [0, 1] range
    mask_float = non_white_mask.astype(np.float32) / 255.0
    mask_float = cv2.merge([mask_float, mask_float, mask_float])  # 3-channel

    # Convert images to float for blending
    base_float = base.astype(np.float32)
    overlay_float = overlay.astype(np.float32)

    # Apply partial transparency only where overlay is not white
    blended = base_float * (1 - mask_float * overlay_opacity) + overlay_float * (mask_float * overlay_opacity)

    # Convert back to 8-bit and save
    result = np.clip(blended, 0, 255).astype(np.uint8)
    cv2.imwrite(output_path, result)
    print(f"Composited with transparent overlay: {name}")

print("All images composited successfully.")
