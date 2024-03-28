"""
This module uses image perceptual hashing to help us detect duplicate and
similar images.

See also the average hashing module for a quicker approach that should find
fewer similarities.

https://pypi.org/project/ImageHash/
https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
"""

import os
import shutil
import sys
from PIL import Image
import imagehash


def main():
    """
    For each jpg file in passed directory, calculate the perceptual hash
    and move observed clusters to new subdirectories for manual review.
    """
    print("Starting image hashing")
    if len(sys.argv) != 2:
        print("Usage: python3 perceptual_hash.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"{directory} is not a directory")
        sys.exit(1)

    image_hash_images = {}

    print(f"Processing images in {directory}")
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            file_path = os.path.join(directory, filename)
            img_hash = imagehash.phash(Image.open(file_path))
            # print(f"Hash for {file_path} is {img_hash}")

            # store the hash in a dictionary
            # and group any images with the same hash together
            if img_hash in image_hash_images:
                image_hash_images[img_hash].append(file_path)
            else:
                image_hash_images[img_hash] = [file_path]

    # once all images are processed, find any clusters
    # in the dictionary with more than 1 image, and move them
    # to a subdirectory named after the hash
    print(f"Checking {len(image_hash_images)} hashes")
    for img_hash, files in image_hash_images.items():
        if len(files) > 1:
            print(
                f"Cluster of {len(files)} found for hash {img_hash}, moving to new directory"
            )
            hash_dir = os.path.join(directory, str(img_hash))
            if not os.path.exists(hash_dir):
                os.mkdir(hash_dir)
            for file in files:
                shutil.move(file, hash_dir)


if __name__ == "__main__":
    main()
