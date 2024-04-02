"""
Streamlit app for Hot Seats project. The user can upload 2 images, and we will generate
and display a new image combining the two images.
"""

import os

import streamlit as st
import numpy as np
import tensorflow as tf

import uploaded_images, autoencoder


# set to a local path as needed
DATASET_VIEWER_DEFAULT_IMAGE_DIRECTORY = None
DATASET_VIEWER_NUM_IMAGES = 10


def playback_uploaded_image(img_ref: str, default: str = None):
    """img_ref is e.g. 'one' or 'A'"""
    uploaded_file = st.file_uploader(
        f"Choose file {img_ref}", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file is None:
        if default is not None:
            st.markdown(f"### Default image {img_ref}")
            st.image(default)
            return default
        else:
            return None
    else:
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
    st.markdown(f"<p style='font-size:12px;'>TensorFlow version: {tf.__version__}</p>", unsafe_allow_html=True)


    st.markdown("""
    <style>
    .main {
      background colour: white;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.title(" ")
    with col2:
        st.image(
            "https://storage.googleapis.com/chairs-gan-images/Hotseats-logo.webp",
            use_column_width=True,
        )
    with col3:
        st.title(" ")

    # Gradient divider
    st.markdown(
        """
    <hr style="height: 2px; border: none; background: linear-gradient(to right,  gray, white);"/>
    """,
        unsafe_allow_html=True,
    )

    # import dataset_viewer
    # dataset_viewer.render_image_dataset_viewer()

    st.header("_PNG_ Chair Image Uploader")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(current_dir, "static")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chair one :fire: :seat:")
        img_a = playback_uploaded_image(
            "Choose file one"#, default=os.path.join(static_dir, "default_a.png")
        )

    with col2:
        st.subheader("Chair two :fire: :seat: :seat:")
        img_b = playback_uploaded_image(
            "Choose file two"#, default=os.path.join(static_dir, "default_b.png")
        )

    if img_a is None or img_b is None:
        st.warning("Please upload two chair images.")
        return

    st.header("Generated Chair")
    encoder = autoencoder.encoder_model()
    decoder = autoencoder.decoder_model()

    # TODO: preprocess the uploads
    _, _, img_a_latent_vector = encoder.predict(
        np.array([uploaded_images.preprocess_image(img_a)])
    )
    _, _, img_b_latent_vector = encoder.predict(
        np.array([uploaded_images.preprocess_image(img_b)])
    )

    # st.markdown("### Latent vector A")
    # st.write(img_a_latent_vector)
    # st.markdown("### Latent vector B")
    # st.write(img_b_latent_vector)

    # Interpolate the latent vectors
    interpolated_latent_vectors = autoencoder.interpolate_latent_vectors(
        img_a_latent_vector, img_b_latent_vector, steps=10
    )
    # st.write(interpolated_latent_vectors[0])

    # Displaying images in one row
    cols = st.columns(len(interpolated_latent_vectors))
    for i, (col, interpolated_encoding) in enumerate(zip(cols, interpolated_latent_vectors)):
        interpolated_encoding_reshaped = interpolated_encoding.reshape(
            (1, 100)
        )  # Reshape to (1, 100)
        reconstructed_image = decoder.predict(interpolated_encoding_reshaped)
        col.image(reconstructed_image, use_column_width=True)
        col.caption(str(i+1))

    #create dropdown menu and show image based on selection
    selected_image = st.selectbox("Select an image", range(1, len(interpolated_latent_vectors)+1), key="image_selection")
    selected_image_index = selected_image - 1
    selected_image_encoding = interpolated_latent_vectors[selected_image_index]
    selected_image_encoding_reshaped = selected_image_encoding.reshape((1, 100))
    selected_image_reconstructed = decoder.predict(selected_image_encoding_reshaped)
    st.image(selected_image_reconstructed, use_column_width=True)



if __name__ == "__main__":
    main()
