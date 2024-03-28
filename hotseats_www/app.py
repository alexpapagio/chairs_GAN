"""
Streamlit app for Hot Seats project. The user can upload 2 images, and we will generate
and display a new image combining the two images.
"""

import os

import streamlit as st

import image_dataset, uploaded_images

# set to a local path as needed
DATASET_VIEWER_DEFAULT_IMAGE_DIRECTORY = None
DATASET_VIEWER_NUM_IMAGES = 10


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


def playback_uploaded_image(img_ref: str):
    """img_ref is e.g. 'one' or 'A'"""
    uploaded_file = st.file_uploader(
        f"Choose file {img_ref}", type=["png", "jpg", "jpeg", "gif", "webp"]
    )
    if uploaded_file is not None:
        # Streamlit base64 encodes the images for us, we can give it the in-memory
        # image data.
        # Let's check it's really an image first, not a renamed text file etc.
        # Streamlit only checks the file extension.
        if uploaded_images.is_image(uploaded_file):
            st.markdown(f"### Uploaded image {img_ref}")
            st.image(uploaded_file)
        else:
            st.error("Uploaded file is unsupported.")


def main():
    """
    Main function of the Streamlit app.
    """

    # Check Streamlit version
    if st.__version__ != "1.29.0":
        st.warning(
            "File upload may not work with this version of Streamlit. Please install version 1.29.0."
        )

    st.set_page_config(
        page_title="Hot Seats",
        page_icon=":chair:",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={"About": "# This is a header. This is a hot seats app!"},
    )

    col1, col2 = st.columns(2)
    with col1:
        st.title("_Hot_ Seats :fire: :seat:")
    with col2:
        st.image(
            "https://storage.googleapis.com/chairs-gan-images/Hotseats-logo.webp",
            use_column_width="auto",
        )

    # Gradient divider
    st.markdown(
        """
    <hr style="height: 2px; border: none; background: linear-gradient(to right, red, gray, white);"/>
    """,
        unsafe_allow_html=True,
    )

    # render_image_dataset_viewer()

    st.header("_PNG_ Chair Image Uploader")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chair one :fire: :seat:")
        playback_uploaded_image("Choose file one")

    with col2:
        st.subheader("Chair two :fire: :seat: :seat:")
        playback_uploaded_image("Choose file two")


if __name__ == "__main__":
    main()
