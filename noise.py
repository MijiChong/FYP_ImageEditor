import cv2
import numpy as np

def apply_gaussian_blur(image, ksize=15):
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def apply_box_blur(image, ksize=15):
    return cv2.blur(image, (ksize, ksize))

def apply_motion_blur(image, ksize=15):
    kernel = np.zeros((ksize, ksize))
    kernel[int((ksize-1)/2), :] = np.ones(ksize)
    kernel = kernel / ksize
    return cv2.filter2D(image, -1, kernel)

def apply_radial_blur(image, iterations=15):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    result = np.zeros_like(image, dtype=np.float32)
    for i in range(1, iterations+1):
        M = cv2.getRotationMatrix2D(center, angle=i * 360 / iterations, scale=1.0)
        rotated = cv2.warpAffine(image, M, (w, h))
        result += rotated.astype(np.float32)
    result /= iterations
    return result.astype(np.uint8)

def add_label(image, label):
    labeled = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2
    color = (255, 0, 0)
    cv2.putText(labeled, label, (10, 30), font, scale, color, thickness, cv2.LINE_AA)
    return labeled

def resize_to_same(images, height=300):
    return [cv2.resize(img, (int(img.shape[1] * height / img.shape[0]), height)) for img in images]

def stack_images_grid(images, grid_shape):
    rows = []
    idx = 0
    for r in range(grid_shape[0]):
        row_imgs = images[idx:idx + grid_shape[1]]
        if len(row_imgs) < grid_shape[1]:
            # Pad with black image if not enough images
            h, w = row_imgs[0].shape[:2]
            for _ in range(grid_shape[1] - len(row_imgs)):
                row_imgs.append(np.zeros((h, w, 3), dtype=np.uint8))
        rows.append(cv2.hconcat(row_imgs))
        idx += grid_shape[1]
    return cv2.vconcat(rows)

# Load your image
image = cv2.imread(r'C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\model.png')  # Replace with your image path

# Apply different blurs
original = add_label(image, "Original")
gaussian = add_label(apply_gaussian_blur(image), "Gaussian Blur")
box = add_label(apply_box_blur(image), "Box Blur")
motion = add_label(apply_motion_blur(image), "Motion Blur")
radial = add_label(apply_radial_blur(image), "Radial Blur")

# Resize all to same height
resized_images = resize_to_same([original, gaussian, box, motion, radial], height=300)

# Combine into 2x3 grid
combined_image = stack_images_grid(resized_images, grid_shape=(2, 3))

# Show or save
cv2.imshow("Blur Comparison with Labels", combined_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Optionally save the result
cv2.imwrite('blur_comparison.jpg', combined_image)
