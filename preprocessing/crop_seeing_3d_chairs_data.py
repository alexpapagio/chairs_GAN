"""
This script crops the images from the Seeing 3D Chairs dataset to remove the surplus white
background, and make the chairs fill more of the image. This can affect autoencoder
performance.

The output files are flattened to a single directory, with the filenames prefixed
with their unique image directory names (because the filenames are not unique across
different chair images).

Run from the project root directory.
The images should be in
raw_data/source/seeing_3d_chairs_rendered_chairs/
and should be in the structure produced by the tar file from
https://www.di.ens.fr/willow/research/seeing3Dchairs/
e.g. raw_data/source/seeing_3d_chairs_rendered_chairs/1a2b8749a1756a09932a5c2746cd09a4/renders/image_000_p020_t000_r096.png

This script is parallelised with Python 3 stdlib, because processing the images takes
several hours, but has only been tested on Mac OS.
"""

import os
import glob
from multiprocessing import Pool, cpu_count
from PIL import Image, ImageOps
import numpy as np


def process_image(file_path, output_dir, padding=10):
    # get the image name, it's the second to last directory, above "renders"
    image_name = file_path.split("/")[-3]
    output_path = os.path.join(
        output_dir, f"{image_name}-{os.path.basename(file_path)}"
    )
    print("processing ", file_path, "output_path", output_path)

    # Open the image
    img = Image.open(file_path).convert("RGB")

    # Get the bounding box
    # The bounding box is returned as a 4-tuple defining the
    # left, upper, right, and lower pixel coordinate

    # This is the original method, but it doesn't work with a white background
    # bbox = img.getbbox()

    # work from the outside edges in to find the first content pixels
    # the background is white, assume 255,255,255

    # Convert the image to a numpy array
    img_array = np.array(img)

    # Get the image size
    height, width, _ = img_array.shape

    # Find the non-white pixels
    non_white_pixels = np.where(np.any(img_array != [255, 255, 255], axis=-1))

    # Get the bounding box coordinates
    left = np.min(non_white_pixels[1])
    upper = np.min(non_white_pixels[0])
    right = np.max(non_white_pixels[1])
    lower = np.max(non_white_pixels[0])

    # Add padding to the bounding box
    # but make sure the values don't go below 0 or above the image size
    bbox = (
        max(0, left - padding),
        max(0, upper - padding),
        min(width, right + padding),
        min(height, lower + padding),
    )

    # Crop the image
    cropped_img = img.crop(bbox)

    # Resize the image, preserving aspect ratio.
    # Scale down to 256x256, do not scale up.
    cropped_img.thumbnail((256, 256), Image.ANTIALIAS)

    # Pad to 256x256 with new white pixels
    # Calculate padding
    width, height = cropped_img.size
    padding_width = (256 - width) // 2
    padding_height = (256 - height) // 2
    # Add white padding
    padded_img = ImageOps.expand(
        cropped_img,
        (padding_width, padding_height, padding_width, padding_height),
        fill=(255, 255, 255),
    )

    # Save the cropped image
    padded_img.save(output_path)


def process_images(file_paths, output_dir):
    """
    Process the chunk of file-paths in parallel."""
    with Pool() as p:
        p.starmap(process_image, [(file_path, output_dir) for file_path in file_paths])


if __name__ == "__main__":
    # Define the source and output directories
    RAW_DATA_DIR = "raw_data/"
    SOURCE_DIR = RAW_DATA_DIR + "source/seeing_3d_chairs_rendered_chairs/"
    OUTPUT_DIR = RAW_DATA_DIR + "processed_data/seeing_3d_chairs_cropped_256x256/"

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Get a list of all PNG files in the source directory
    all_png_paths = glob.glob(SOURCE_DIR + "/**/*.png", recursive=True)
    # Split the list of file paths into chunks
    chunks = [
        all_png_paths[i : i + cpu_count()]
        for i in range(0, len(all_png_paths), cpu_count())
    ]
    for chunk in chunks:
        process_images(chunk, OUTPUT_DIR)
