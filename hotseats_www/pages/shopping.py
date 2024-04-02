import streamlit as st
from serpapi import GoogleSearch

def shopping_page():
    st.set_page_config(page_title="Shopping", page_icon=":shopping_bags:")
    st.title("Online Shopping - Search")

    # Display the two default images side by side at the top of the page
    st.header("Default Chair Images")
    default_image_paths = [
        "https://github.com/alexpapagio/chairs_GAN/blob/master/hotseats_www/static/3846.jpg?raw=true",
        "https://github.com/alexpapagio/chairs_GAN/blob/master/hotseats_www/static/3920.jpg?raw=true"
    ]
    col1, col2 = st.columns(2)
    with col1:
        st.image(default_image_paths[1], caption="Chair Image 1")
    with col2:
        st.image(default_image_paths[0], caption="Chair Image 2")

    # Display GAN Interpolations in one row
    st.header("GAN Interpolations")
    interpolation_paths = [
        f"https://github.com/alexpapagio/chairs_GAN/blob/master/hotseats_www/static/interpolations/intepolation-{i}.png?raw=true"
        for i in range(10)  # Assuming 10 interpolations
    ]
    cols = st.columns(len(interpolation_paths))  # Create as many columns as there are images
    for col, path in zip(cols, interpolation_paths):
        col.image(path, use_column_width=True)  # Adjust usage of use_column_width as needed

    # Dropdown for selecting an interpolation to enlarge
    interpolation_options = [f"Interpolation {i + 1}" for i in range(10)]  # Assuming 10 interpolations
    selected_interpolation = st.selectbox("Select an interpolation to view:", interpolation_options)
    selected_index = interpolation_options.index(selected_interpolation)

    # Display the selected interpolated image larger
    st.image(interpolation_paths[selected_index], caption=f"Enlarged {selected_interpolation}", width=500)

    # Create a dictionary with interpolation options and filenames
    select = {
        'Interpolation 1': 'static/interpolations/intepolation-0.png',
        'Interpolation 2': 'static/interpolations/intepolation-1.png',
        'Interpolation 3': 'static/interpolations/intepolation-2.png',
        'Interpolation 4': 'static/interpolations/intepolation-3.png',
        'Interpolation 5': 'static/interpolations/intepolation-4.png',
        'Interpolation 6': 'static/interpolations/intepolation-5.png',
        'Interpolation 7': 'static/interpolations/intepolation-6.png',
        'Interpolation 8': 'static/interpolations/intepolation-7.png',
        'Interpolation 9': 'static/interpolations/intepolation-8.png',
        'Interpolation 10': 'static/interpolations/intepolation-9.png'
    }


    # Get the filename of the selected interpolation
    selected_filename = select[selected_interpolation]

    # Perform SerpAPI search for the selected interpolation details using the specific filename
    params = {
        "engine": "google_lens",
        "url": f"https://github.com/alexpapagio/chairs_GAN/blob/master/hotseats_www/{selected_filename}?raw=true",
        "api_key": st.secrets["SERPAPI_KEY"],  # Use your actual SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    if "visual_matches" in results:
        st.header(f"Shopping results for {selected_interpolation}:")
        for match in results["visual_matches"][0:3]:  # Display details for the first 3 matches
            st.image(match["thumbnail"], caption=match["title"])
            st.markdown(f"Source: {match['source']}")
            st.markdown(f"[View Source]({match['link']})")
    else:
        st.error(f"No visual matches found for {selected_interpolation}.")



if __name__ == "__main__":
    shopping_page()
