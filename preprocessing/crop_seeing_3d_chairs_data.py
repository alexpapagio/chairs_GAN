"""
This script crops the images from the Seeing 3D Chairs dataset to remove the white background.

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
from PIL import Image, ImageOps
from multiprocessing import Pool, cpu_count

raw_data_dir = "raw_data/"
source_dir = raw_data_dir + "/source/seeing_3d_chairs_rendered_chairs/"


def make_white_transparent(img):
    # Get the image data
    data = img.getdata()

    # Create a new image data
    new_data = []
    for item in data:
        # Change all white (also shades of whites)
        # pixels to transparent
        if item[0] in list(range(200, 256)):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    # Update the image data
    img.putdata(new_data)
    return img


def process_image(file_path, output_dir, padding=10):
    # get the image name, it's the second to last directory, above "renders"
    image_name = file_path.split("/")[-3]
    output_path = os.path.join(
        output_dir, f"{image_name}-{os.path.basename(file_path)}"
    )
    print("processing ", file_path, "output_path", output_path)

    # Open the image
    img = Image.open(file_path).convert("RGBA")

    # Make white pixels transparent
    img = make_white_transparent(img)

    # Get the bounding box
    bbox = img.getbbox()

    # Check if the bounding box is None
    if bbox is None:
        print(f"No non-transparent pixels found in image {file_path}. Skipping.")
        # Append the filename to a failure file
        with open("failure.txt", "a", encoding="utf-8") as f:
            f.write(file_path + "\n")
        return

    # Add padding to the bounding box
    bbox = (bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding)

    # Crop the image
    cropped_img = img.crop(bbox)

    # Resize the image, preserving aspect ratio.
    # Scale down to 100x100, do not scale up.
    cropped_img.thumbnail((100, 100), Image.ANTIALIAS)

    # Pad to 100x100 with transparency
    # Calculate padding
    width, height = cropped_img.size
    padding_width = (100 - width) // 2
    padding_height = (100 - height) // 2
    # Add transparent padding
    padded_img = ImageOps.expand(
        cropped_img,
        (padding_width, padding_height, padding_width, padding_height),
        fill=(255, 255, 255, 0),
    )

    # Save the cropped image
    padded_img.save(output_path)


def process_images(file_paths, output_dir):
    with Pool() as p:
        p.starmap(process_image, [(file_path, output_dir) for file_path in file_paths])


if __name__ == "__main__":
    # Define the source and output directories
    source_dir = raw_data_dir + "source/seeing_3d_chairs_rendered_chairs/"
    output_dir = raw_data_dir + "processed_data/"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all PNG files in the source directory
    file_paths = glob.glob(source_dir + "/**/*.png", recursive=True)
    # Split the list of file paths into chunks
    chunks = [
        file_paths[i : i + cpu_count()] for i in range(0, len(file_paths), cpu_count())
    ]
    for chunk in chunks:
        process_images(chunk, output_dir)
