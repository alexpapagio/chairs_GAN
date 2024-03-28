import os
from PIL import Image

def load_png_images_from_directory(directory_path, num_images=10):
    images = []
    for filename in os.listdir(directory_path)[:num_images]:
        if filename.endswith(".png"):
            img_path = os.path.join(directory_path, filename)
            try:
                img = Image.open(img_path)
                images.append(img)
            except Exception as e:
                print(f"Error loading image {filename}: {e}")
    return images
