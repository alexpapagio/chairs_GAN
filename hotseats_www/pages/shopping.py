from serpapi import GoogleSearch
import os
import streamlit as st
import whereami


def get_static_img_url(image_filename):
    """
    Return the URL of the given image in the app's static folder.

    e.g. local forwarded through ngrok
    default_a.png -> http://55cd-37-157-32-162.ngrok-free.app/app/static/default_a.png
    or on streamlit cloud
    default_a.png -> https://nruth-hotseats-hotseats-wwwapp-nruthstreamlit-cloud-n8hkl1.streamlit.app/app/static/default_a.png
    """
    return os.path.join(whereami.get_url(), "app/static/", image_filename)


# st.write(get_static_img_url("default_a.png"))

params = {
    "engine": "google_lens",
    "url": "https://github.com/alexpapagio/test1/blob/main/intepolation-3.png?raw=true",
    "api_key": st.secrets["SERPAPI_KEY"],
}

search = GoogleSearch(params)
results = search.get_dict()
knowledge_graph = results

for match in knowledge_graph["visual_matches"][0:3]:
    st.image(match["thumbnail"], caption=match["title"])
    st.write(match["source"])
    st.write(match["link"])

#st.write(knowledge_graph["visual_matches"][0:3])
