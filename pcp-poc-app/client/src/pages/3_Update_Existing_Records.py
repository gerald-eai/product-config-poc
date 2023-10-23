import streamlit as st
import pandas as pd
from components.sres_forms import SresForm
import components.global_components as Global
from data.data_processor import col_order
from core.utils import load_data, get_api_client, page_startup


def save_session_state(data: dict):
    keys = list(data.keys())
    if "sres" in keys and isinstance(data["sres"], pd.DataFrame):
        st.session_state["sres"] = data["sres"]


def main():
    st.title("Update Existing Records")
    api_client = get_api_client("http://localhost:8000/")

    # our data is obtained from a dataframe
    st.markdown("## Current SRES Data")
    refresh_btn = st.button("Refresh SRES Data :arrows_counterclockwise:")
    live_sres_data = load_data(api_client, "sres/", params={"skip": 0, "limit": 450})
    save_session_state({"sres": live_sres_data})

    if refresh_btn:
        st.session_state["sres"] = None
        live_sres_data = load_data(
            api_client, "sres/", params={"skip": 0, "limit": 450}
        )
        save_session_state({"sres": live_sres_data})

    # visualise the ag grid component, in the ideal column order
    ag_grid = Global.aggrid_component(live_sres_data[col_order])
    selected_row = ag_grid["selected_rows"]
    if len(selected_row) > 0:
        sres_form = SresForm(api_client.base_url)
        sres_form.edit_entry_form(selected_row[0])


if __name__ == "__main__":
    page_startup()
    main()
