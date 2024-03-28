import streamlit as st
import os
from PIL import Image
from image_loader import load_png_images_from_directory
from save_upload import save_uploadedfile
from load_process_convert import load_image, image_to_base64


DEFAULT_IMAGE_DIRECTORY = "/Users/luketomlinson/Desktop/RC_Chairs"
NUM_IMAGES_TO_DISPLAY = 10
UPLOAD_DIRECTORY = "/Users/luketomlinson/Desktop/Streamlit_folder"

# If you're using constants.py
# from constants import DEFAULT_IMAGE_DIRECTORY, NUM_IMAGES_TO_DISPLAY


def main():

    st.set_page_config(
        page_title="Hot Seats",
        page_icon=":fire: :seat: :chair:",
        layout="centered",
        initial_sidebar_state="expanded",
        menu_items={"About": "# This is a header. This is a hot seats app!"},
    )

    st.image(
        "https://storage.googleapis.com/chairs-gan-images/Hotseats-logo.webp",
        caption="Hot Seats Logo",
        use_column_width=True,
    )

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
        num_images = st.number_input("Number of images to display", min_value=1, value=5, max_value=10, step=1)
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

    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Chair one :fire: :seat:")
        uploaded_file_one = st.file_uploader("Choose file one", type=["png"])
        if uploaded_file_one is not None:
            st.image(uploaded_file_one)
            file_path_one = save_uploadedfile(UPLOAD_DIRECTORY, uploaded_file_one)

            if file_path_one:
                st.success(f"File saved at {file_path_one}")
                # Load, process, and convert the image
                processed_image = load_image(file_path_one)
                base64_img = image_to_base64(processed_image)

                # Display the image using base64 encoding
                st.markdown(f"### Processed Image Display :fire: :seat:")
                st.markdown(f'<img src="data:image/png;base64,{base64_img}" alt="Processed image" style="display:block; margin-left:auto; margin-right:auto;"/>', unsafe_allow_html=True)

            #  # Convert the PIL Image to a base64 string
            # base64_str_one = get_image_base64(uploaded_file_one)
            # # Generate the HTML img tag
            # img_html_one = generate_img_html(base64_str_one)
            # # Display the HTML image in Streamlit
            # st.markdown(img_html_one, unsafe_allow_html=True)
            # # Optionally, you can display the raw HTML code to the user
            # st.text_area("Copy the HTML code below:", img_html_one, height=100)

            # # Gradient divider
            # st.markdown(
            # """
            # <hr style="height: 2px; border: none; background: linear-gradient(to right, red, gray, white);"/>
            # """,
            # unsafe_allow_html=True
            # )

            # st.header('HTML :fire: :chair: Image Display')




    with col2:
        st.subheader("Chair two :fire: :seat: :seat:")
        uploaded_file_two = st.file_uploader("Choose file two", type=["png"])
        if uploaded_file_two is not None:
            st.image(uploaded_file_two)
            file_path_two = save_uploadedfile(UPLOAD_DIRECTORY, uploaded_file_two)

            if file_path_two:
                st.success(f"File saved at {file_path_two}")
                # Load, process, and convert the image
                processed_image = load_image(file_path_two)
                base64_img = image_to_base64(processed_image)

                # Display the image using base64 encoding
                st.markdown(f"### Processed Image Display :fire: :seat: :seat:")
                st.markdown(f'<img src="data:image/png;base64,{base64_img}" alt="Processed image" style="display:block; margin-left:auto; margin-right:auto;"/>', unsafe_allow_html=True)

            #  # Convert the PIL Image to a base64 string
            # base64_str_two = get_image_base64(uploaded_file_two)
            # # Generate the HTML img tag
            # img_html_two = generate_img_html(base64_str_two)
            # # Display the HTML image in Streamlit
            # st.markdown(img_html_two, unsafe_allow_html=True)
            # # Optionally, you can display the raw HTML code to the user
            # st.text_area("Copy the HTML code below:", img_html_two, height=100)

            # # Gradient divider
            # st.markdown(
            # """
            # <hr style="height: 2px; border: none; background: linear-gradient(to right, red, gray, white);"/>
            # """,
            # unsafe_allow_html=True
            # )

            # st.header('HTML :fire: :chair: :chair: Image Display')




if __name__ == "__main__":
    main()
