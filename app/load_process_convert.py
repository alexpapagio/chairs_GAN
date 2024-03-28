import streamlit as st
from PIL import Image
import numpy as np
import base64
from io import BytesIO


# Function to load and process the image
@st.cache
def load_image(image_data, new_img_width=256, remove_top_pixels=0):
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

# Function to convert image to base64 for HTML embedding
def image_to_base64(im, format="PNG"):
    buffered = BytesIO()
    im.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
