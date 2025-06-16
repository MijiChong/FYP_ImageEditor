from PIL import Image
import os

# Mapping image modes to their bit depths
MODE_BIT_DEPTH = {
    '1': 1,      # 1-bit
    'L': 8,      # 8-bit Grayscale
    'P': 8,      # 8-bit Palette
    'RGB': 24,   # 24-bit Truecolor
    'RGBA': 32,  # 32-bit with alpha
    'CMYK': 32,  # 32-bit CMYK
    'I': 32,     # 32-bit integer
    'I;16': 48   # 48-bit high-depth grayscale
}

# Target modes and their folder names
TARGETS = {
    'RGBA': '32bit',
    'RGB': '24bit',
    'L': '8bit_L',
    'P': '8bit_P',
    '1': '1bit'
}

def get_bit_depth(mode):
    return MODE_BIT_DEPTH.get(mode, 'Unknown')

def convert_and_save(image_path, output_folder):
    with Image.open(image_path) as img:
        original_mode = img.mode
        original_depth = get_bit_depth(original_mode)

        for target_mode, folder_name in TARGETS.items():
            target_depth = get_bit_depth(target_mode)
            target_folder = os.path.join(output_folder, folder_name)
            os.makedirs(target_folder, exist_ok=True)
            output_path = os.path.join(target_folder, os.path.basename(image_path))

            try:
                # Skip if already in target mode/depth
                if original_mode == target_mode:
                    print(f"{image_path} already in {target_mode} ({target_depth}-bit), saving as-is.")
                    img.save(output_path)
                    continue

                # Special case for 1-bit conversion (avoid transparency issues)
                if target_mode == '1':
                    print(f"{image_path}: converting to {target_mode} ({target_depth}-bit) [flattening transparency].")
                    img_converted = img.convert("RGB").convert("L").convert("1")
                else:
                    print(f"{image_path}: converting to {target_mode} ({target_depth}-bit).")
                    img_converted = img.convert(target_mode)

                img_converted.save(output_path)

            except Exception as e:
                print(f"Error processing {image_path} for mode {target_mode}: {e}")

def batch_convert_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_folder, filename)
            convert_and_save(input_path, output_folder)

# Example usage
input_folder = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\color\file"
output_folder = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\color\output"
batch_convert_images(input_folder, output_folder)
