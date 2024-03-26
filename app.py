import streamlit as st

from PIL import Image
from image_loader import load_png_images_from_directory
from utils import DEFAULT_IMAGE_DIRECTORY, NUM_IMAGES_TO_DISPLAY


# If you're using constants.py
# from constants import DEFAULT_IMAGE_DIRECTORY, NUM_IMAGES_TO_DISPLAY

def main():

    image = Image.open('/Users/luketomlinson/Downloads/Hotseats_logo.webp')
    st.image(image=image, caption='Hotseats Logo', use_column_width=True)



    st.title('_Hot_ Seats :fire: :seat:')

    # Gradient divider
    st.markdown(
    """
    <hr style="height: 2px; border: none; background: linear-gradient(to right, red, gray, white);"/>
    """,
    unsafe_allow_html=True
    )

    st.header('_PNG_ Image Dataset Viewer')

    # Let the user choose between default values or providing their own
    input_choice = st.radio("Choose your input method:", ("Use default settings", "Enter custom inputs"))

    if input_choice == "Enter custom inputs":
        # User inputs for directory path and number of images
        directory_path = st.text_input("Enter the directory path containing PNG images", "")
        num_images = st.number_input("Number of images to display", min_value=1, max_value=10, step=1)
    else:
        # Use constants
        directory_path = DEFAULT_IMAGE_DIRECTORY
        num_images = NUM_IMAGES_TO_DISPLAY



    # # Use constants or define directly
    # directory_path = st.text_input("Enter the directory path containing PNG images", "/path/to/your/images")
    # num_images = st.number_input("Number of images to display", min_value=1, value=10, step=1)

    if directory_path:
        images = load_png_images_from_directory(directory_path=DEFAULT_IMAGE_DIRECTORY, num_images=NUM_IMAGES_TO_DISPLAY)
        if images:
            st.image(images, caption=[f"Image {i+1}" for i in range(len(images))], use_column_width=True)
        else:
            st.write("No PNG images found in the specified directory.")

     # Gradient divider
    st.markdown(
    """
    <hr style="height: 2px; border: none; background: linear-gradient(to right, red, gray, white);"/>
    """,
    unsafe_allow_html=True
    )

    st.header('_PNG_ Chair Image Uploader')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chair one :fire: :seat:")
        uploaded_file_one = st.file_uploader("Choose file one", type=["png"])
        if uploaded_file_one is not None:
            st.image(uploaded_file_one)

    with col2:
        st.subheader("Chair two :fire: :seat: :seat:")
        uploaded_file_two = st.file_uploader("Choose file two", type=["png"])
        if uploaded_file_two is not None:
            st.image(uploaded_file_two)



if __name__ == "__main__":
    main()
