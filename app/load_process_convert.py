"""
This module contains functions to load and process images sent to the server by the
user's browser.
"""

import imghdr
from PIL import Image
import numpy as np


def resize_image(image_data, new_img_width=256, remove_top_pixels=0):
    """Load and process the image"""
    # Load the image
    im = Image.open(image_data)
    if remove_top_pixels > 0:
        im = np.array(im)[remove_top_pixels:, :, :]
        im = Image.fromarray(im)

    # Resize the image
    old_img_width, old_img_height = im.size
    new_img_height = (old_img_height * new_img_width) // old_img_width
    im = im.resize((new_img_width, new_img_height), Image.LANCZOS)
    return im


def is_image(file):
    """Check if the given file is a PNG, JPEG, GIF, or WebP image."""
    try:
        return imghdr.what(file) in {"png", "jpeg", "gif", "webp"}
    except (TypeError, OSError):
        return False
