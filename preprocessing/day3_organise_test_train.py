"""
This script renames the files in place, so backup the files in another dir or archive
before running this script.

- create new directory raw_data/source/day-3-kaggle-cherrypicked-flattened
    - error if it already exists
- for the files in day_images_root/train/chair/*.jpg rename them to train-chair-n.jpg where n is the original filename
- for the files in day_images_root/test-chairs-cherrypicked/*.jpg rename them to test-chair-n.jpg where n is the original filename
- store in a new directory
"""

import os

day3_images_root = "raw_data/source/day-3-kaggle-cherrypicked"
target_dir_name = "raw_data/source/day-3-kaggle-cherrypicked-flattened"

# make the target directory
os.makedirs(target_dir_name, exist_ok=False)

train_chair_directory = os.path.join(day3_images_root, "train/chair")
test_chair_directory = os.path.join(day3_images_root, "test-chairs-cherrypicked")


def rename_files(directory, prefix):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            new_filename = f"{prefix}-{filename}"
            os.rename(
                os.path.join(directory, filename),
                os.path.join(day3_images_root, new_filename),
            )


rename_files(train_chair_directory, "train-chair")
rename_files(test_chair_directory, "test-chair")

print("Files renamed")
