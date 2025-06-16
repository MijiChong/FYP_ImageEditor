from PIL import Image
import os

def get_color_depth(image_path):
    with Image.open(image_path) as img:
        mode = img.mode
        if mode == "1":
            return 1  # 1-bit
        elif mode in ["L", "P"]:
            return 8  # 8-bit
        elif mode == "RGB":
            return 24  # 24-bit
        elif mode == "RGBA":
            return 32  # 32-bit
        elif mode == "CMYK":
            return 32  # Usually 32-bit
        else:
            return f"Unknown mode: {mode}"

def check_images_color_depth(folder_path):
    supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(supported_formats):
            file_path = os.path.join(folder_path, file_name)
            depth = get_color_depth(file_path)
            print(f"{file_name}: {depth}-bit")

# Example usage
folder_path = r"C:\Users\Mijiiii MC\OneDrive\Desktop\FYP\color\24bit"  # Change this to your folder
check_images_color_depth(folder_path)
