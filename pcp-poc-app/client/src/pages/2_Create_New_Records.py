import streamlit as st
import pandas as pd
from components.sres_forms import SresForm
from data.data_processor import col_order
from core.utils import load_data, get_api_client, page_startup


def save_session_state(data: dict):
    """Saves the sres data to the session state"""
    keys = list(data.keys())
    if "sres" in keys and isinstance(data["sres"], pd.DataFrame):
        st.session_state["sres"] = data["sres"]


def main():
    """_summary_
    Renders the table to visualise the  Current data in the SRES table
    Creates a form to create a new entry in the SRES table
    """
    st.title("Create New Entries in Service Reservoir")
    api_consumer = get_api_client("http://localhost:8000/")

    st.markdown("## Current SRES Data")
    refresh_btn = st.button("Refresh SRES Data :arrows_counterclockwise:")
    live_sres_data = load_data(api_consumer, "sres/", params={"skip": 0, "limit": 500})
    save_session_state({"sres": live_sres_data})

    if refresh_btn:
        st.session_state["sres"] = None
        live_sres_data = load_data(
            api_consumer, "sres/", params={"skip": 0, "limit": 500}
        )
        save_session_state({"sres": live_sres_data})

    st.dataframe(live_sres_data[col_order])
    st.divider()
    # include a new form for creating the data
    cols = list(live_sres_data.columns)
    new_form_keys = dict.fromkeys(cols, None)
    sres_form = SresForm(api_consumer.base_url)
    sres_form.create_current_entry_form(new_form_keys)


if __name__ == "__main__":
    page_startup()
    main()
