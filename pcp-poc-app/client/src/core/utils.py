import streamlit as st 
from services.api import DatabaseAPIClient
from services.adf import DataFactoryAPIClient
import pandas as pd

def page_startup(): 
    st.set_page_config(layout="wide")

@st.cache_resource
def get_api_client(url: str) -> DatabaseAPIClient:
    """
    Creates a new API client

    Args:
        url (str): the base url for the API server

    Returns:
        DatabaseAPIClient: the API client
    """
    return DatabaseAPIClient(base_url=url)


@st.cache_data(show_spinner="Requesting Data from Api...")
def load_data(
    _api_client: DatabaseAPIClient, prefix: str, params: dict
) -> pd.DataFrame:
    """
    Request the data from API

    Args:
        _api_client (DatabaseAPIClient): Api client responsible for making requests to the API server
        prefix (str): the table to read from
        params (dict): parameters for the API request

    Returns:
        pd.DataFrame: The data from the database
    """
    data = _api_client.get_all(prefix, params)
    return data