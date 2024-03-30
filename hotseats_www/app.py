"""
Streamlit app for Hot Seats project. The user can upload 2 images, and we will generate
and display a new image combining the two images.
"""

import os

import streamlit as st

import uploaded_images, autoencoder
import numpy as np

import tensorflow as tf


# set to a local path as needed
DATASET_VIEWER_DEFAULT_IMAGE_DIRECTORY = None
DATASET_VIEWER_NUM_IMAGES = 10


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
            return uploaded_file
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

    # display the tensorflow keras version
    st.markdown(f"TensorFlow version: {tf.__version__}")

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

    # import dataset_viewer
    # dataset_viewer.render_image_dataset_viewer()

    st.header("_PNG_ Chair Image Uploader")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chair one :fire: :seat:")
        img_a = playback_uploaded_image("Choose file one")

    with col2:
        st.subheader("Chair two :fire: :seat: :seat:")
        img_b = playback_uploaded_image("Choose file two")

    st.header("Generated Chair")
    encoder = autoencoder.encoder_model()
    # TODO: preprocess the uploads
    # img_a_latent_vector = encoder.predict(np.array([img_a]))
    # img_b_latent_vector = encoder.predict(np.array([img_b]))

    # st.markdown("### Latent vector A")
    # st.write(img_a_latent_vector.shape)
    # st.markdown("### Latent vector B")
    # st.write(img_b_latent_vector.shape)

    # Interpolate the latent vectors
    # interpolated_latent_vector = autoencoder.interpolate_latent_vectors(
    #     img_a_latent_vector, img_b_latent_vector
    # )


if __name__ == "__main__":
    main()
