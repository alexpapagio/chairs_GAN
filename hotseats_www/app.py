import streamlit as st
import uploaded_images, autoencoder
import numpy as np
import tensorflow as tf

def playback_uploaded_image(col, img_ref: str, default: str = None):
    with col:
        uploaded_file = st.file_uploader(f"Choose file {img_ref}", type=["png", "jpg", "jpeg"], key=img_ref)
        if uploaded_file is None:
            if default is not None:
                st.image(default, caption=f"Default image {img_ref}")
                return default
            else:
                return None
        else:
            if uploaded_images.is_image(uploaded_file):
                st.image(uploaded_file, caption=f"Uploaded image {img_ref}")
                return uploaded_file
            else:
                st.error("Uploaded file is unsupported.")
    return None

def main():
    st.set_page_config(page_title="Hot Seats", page_icon=":chair:")
    st.title("_Hot_ Seats :fire: :seat:")
    
    col1, col2 = st.columns(2)
    img_a = playback_uploaded_image(col1, "one", default="static/default_a.png")
    img_b = playback_uploaded_image(col2, "two", default="static/default_b.png")

    if img_a is None or img_b is None:
        st.warning("Please upload two chair images.")
    else:
        encoder = autoencoder.encoder_model()
        decoder = autoencoder.decoder_model()

        _, _, img_a_latent_vector = encoder.predict(np.array([uploaded_images.preprocess_image(img_a)]))
        _, _, img_b_latent_vector = encoder.predict(np.array([uploaded_images.preprocess_image(img_b)]))

        interpolated_latent_vectors = autoencoder.interpolate_latent_vectors(img_a_latent_vector, img_b_latent_vector, steps=10)

        cols = st.columns(len(interpolated_latent_vectors))
        for index, (col, interpolated_encoding) in enumerate(zip(cols, interpolated_latent_vectors), start=1):
            with col:
                interpolated_encoding_reshaped = interpolated_encoding.reshape((1, 100))
                reconstructed_image = decoder.predict(interpolated_encoding_reshaped)
                col.image(reconstructed_image, caption=f"Image {index}", use_column_width=True)

        with st.expander("Choose image for e-commerce search"):
            image_options = [f"Image {i+1}" for i in range(len(interpolated_latent_vectors))]
            selected_image = st.selectbox("Choose an image to use in the API call:", options=image_options, key="image_selection")
            
            # Simulate an API call based on the selected image
            image_index = image_options.index(selected_image) + 1
            # Simulated URL - replace with actual API call result
            simulated_url = f"https://example.com/selected_image/{image_index}"
            st.write(f"Simulated URL for {selected_image}: {simulated_url}")

if __name__ == "__main__":
    main()
