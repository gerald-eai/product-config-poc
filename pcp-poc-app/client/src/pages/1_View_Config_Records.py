import streamlit as st
from services.api import DatabaseAPIClient
from data.data_processor import col_order
from core.utils import page_startup


@st.cache_data(show_spinner="Request Data from Api...")
def render_current_tables(_api_session: DatabaseAPIClient, endpoint: str, params: dict):
    """_summary_
    Request the current configuration data from the API server

    Args:
        _api_session (DatabaseAPIClient): API client responsible for the requests
        endpoint (str): endpoint url
        params (dict): parameters for the API request
    """
    live_data = _api_session.get_all(f"{endpoint}/", params=params)
    live_data = live_data[col_order]
    st.write(live_data)


def main():
    """Renders the Current Data in the SRES Table"""
    st.title("View Service Reservoir Storage Config Records")
    st.divider()
    api_consumer = DatabaseAPIClient("http://localhost:8000/")
    st.markdown("## SRES")
    render_current_tables(api_consumer, "sres", {"skip": 0, "limit": 500})
    st.divider()


if __name__ == "__main__":
    page_startup()
    main()
