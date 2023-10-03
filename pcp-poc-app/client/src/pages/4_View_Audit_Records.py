import streamlit as st
from services.api import DatabaseAPIClient
import pandas as pd


def page_startup():
    st.set_page_config(layout="wide")


@st.cache_data
def load_data(prefix: str, base_url: str, params: dict) -> pd.DataFrame:
    # we're only loading the live data of whatever is requested
    api_session = DatabaseAPIClient(base_url)
    data = api_session.get_all(prefix, params)
    return data


def main():
    st.title("View Audit Records")
    audit_log_df = load_data(
        "audit/", base_url="http://localhost:8000/", params={"skip": 0, "limit": 450}
    )
    st.dataframe(audit_log_df)


if __name__ == "__main__":
    page_startup()
    main()
