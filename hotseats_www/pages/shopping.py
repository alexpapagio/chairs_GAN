from serpapi import GoogleSearch
import os
import streamlit as st
import whereami

def get_static_img_url(image_filename):
    """
    Return the URL of the given image in the app's static folder.
    """
    return os.path.join(whereami.get_url(), "app/static/", image_filename)

def shopping_page():
    st.set_page_config(page_title="Shopping", page_icon=":shopping_bags:")

    st.title("Shopping")

    params = {
        "engine": "google_lens",
        "url": "https://github.com/alexpapagio/test1/blob/main/intepolation-3.png?raw=true",
        "api_key": st.secrets["SERPAPI_KEY"],
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    knowledge_graph = results

    if "visual_matches" in knowledge_graph:
        # Prepare image options for the dropdown
        image_options = [f"Image {i+1}: {match['title']}" for i, match in enumerate(knowledge_graph["visual_matches"][0:3])]
        # Create a dropdown for image selection
        selected_image_option = st.selectbox("Choose an image for more details:", options=image_options, key="image_selection_shopping")

        # Extract the index of the selected image
        selected_index = image_options.index(selected_image_option)
        selected_image_info = knowledge_graph["visual_matches"][selected_index]

        # Display selected image and information
        st.image(selected_image_info["thumbnail"], caption=selected_image_info["title"])
        st.write(f"Source: {selected_image_info['source']}")
        st.write(f"Link: {selected_image_info['link']}")

    else:
        st.error("No visual matches found. Please try again with a different image.")

if __name__ == "__main__":
    shopping_page()
