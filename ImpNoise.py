import cv2
import numpy as np
import os

def add_impulse_noise(image, amount=0.25, strength=0.25, random_rgb=True):
    """
    Adds impulse noise to an image with specified amount and strength.

    Args:
        image: Input image (numpy array).
        amount: Fraction of pixels to be replaced with noise (0-1).
        strength: Intensity of noise (0-1) for RGB range.
        random_rgb: If True, adds random RGB noise instead of just salt-pepper.

    Returns:
        Noisy image (numpy array).
    """
    noisy_image = np.copy(image)
    total_pixels = image.shape[0] * image.shape[1]
    num_pixels = int(amount * total_pixels)  # Total noisy pixels

    # Generate random coordinates for noise
    coords = [np.random.randint(0, i - 1, num_pixels) for i in image.shape[:2]]

    if random_rgb:
        # Random RGB values within strength range
        noise_range = int(255 * strength)
        noisy_image[coords[0], coords[1]] = np.random.randint(0, noise_range, (num_pixels, 3))
    else:
        # Traditional Salt & Pepper noise (limited by strength)
        salt_pepper = np.random.choice([0, 255 * strength], num_pixels)
        noisy_image[coords[0], coords[1]] = np.column_stack([salt_pepper] * 3)  # Make it RGB

    return noisy_image

def process_images(input_folder, output_folder, noise_amount=0.25, noise_strength=0.25):
    """
    Processes all images in a folder by adding impulse noise and saving to another folder.

    Args:
        input_folder: Folder containing input images.
        output_folder: Folder to save noisy images.
        noise_amount: Percentage of pixels to add noise (0-1).
        noise_strength: Intensity of noise (0-1).
    """
    os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Only process image files
            img_path = os.path.join(input_folder, filename)
            image = cv2.imread(img_path)

            if image is None:
                print(f"Skipping {filename}, unable to read.")
                continue

            # Apply impulse noise with amount and strength
            noisy_image = add_impulse_noise(image, amount=noise_amount, strength=noise_strength, random_rgb=True)

            # Save image with the same name in the output folder
            save_path = os.path.join(output_folder, filename)
            cv2.imwrite(save_path, noisy_image)
            print(f"Saved {save_path}")

# Example usage:
input_directory = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\edit"  # Folder with original images
output_directory = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\Noised"      # Folder to save noisy images

# Apply 50% noise amount and 50% noise strength
process_images(input_directory, output_directory, noise_amount=0.17, noise_strength=0.17)
