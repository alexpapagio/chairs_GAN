import urllib
import streamlit as st


def get_url():
    """
    Return the base URL of the Streamlit app.
    See https://github.com/streamlit/streamlit/issues/798
    """
    import urllib.parse

    session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
    st_base_url = urllib.parse.urlunparse(
        [session.client.request.protocol, session.client.request.host, "", "", "", ""]
    )
    return st_base_url
