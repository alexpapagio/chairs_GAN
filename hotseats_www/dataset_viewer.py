import os
from PIL import Image
import streamlit as st


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


def render_image_dataset_viewer(
    num_images_to_display: int = DATASET_VIEWER_NUM_IMAGES,
    image_directory: str = DATASET_VIEWER_DEFAULT_IMAGE_DIRECTORY,
):
    """
    Add the image dataset viewer to the Streamlit app.
    """
    st.header("_PNG_ Image Dataset Viewer")

    # Let the user choose between default values or providing their own
    input_choice = st.radio(
        "Choose your input method:", ("Use default settings", "Enter custom inputs")
    )

    if input_choice == "Enter custom inputs":
        # User inputs for directory path and number of images
        image_directory = st.text_input(
            "Enter the directory path containing PNG images", ""
        )
        num_images_to_display = st.number_input(
            "Number of images to display", min_value=1, value=5, max_value=10, step=1
        )

    if image_directory:
        images = image_dataset.load_png_images_from_directory(
            directory_path=image_directory, num_images=num_images_to_display
        )
        if images:
            st.image(
                images,
                caption=[f"Image {i+1}" for i in range(len(images))],
                use_column_width=True,
            )
        else:
            st.write("No PNG images found in the specified directory.")
    else:
        st.error("No image directory provided, and no default set.")

    # Gradient divider
    st.markdown(
        """
    <hr style="height: 2px; border: none; background: linear-gradient(to right, red, gray, white);"/>
    """,
        unsafe_allow_html=True,
    )
