"""
This module contains functions to load and process images sent to the server by the
user's browser.
"""

import imghdr
from PIL import Image
import numpy as np


def preprocess_image(image_data):
    """Load and process the image ready for model.predict"""
    # Load the image
    img = Image.open(image_data)
    img = img.convert("RGB")
    img = img.resize((100, 100))

    result = np.array(img)
    result = result / 255.0
    return result


def is_image(file):
    """Check if the given file is a PNG, JPEG, GIF, or WebP image."""
    try:
        return imghdr.what(file) in {"png", "jpeg", "gif", "webp"}
    except (TypeError, OSError):
        return False
