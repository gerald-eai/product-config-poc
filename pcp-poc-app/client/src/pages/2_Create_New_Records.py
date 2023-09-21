import streamlit as st
from services.api import ApiConsumer
import pandas as pd
from components.sres_forms import SresForm
import components.global_components as Global
from data.data_processor import col_order


def page_startup():
    st.set_page_config(layout="wide")


def save_session_state(data: dict):
    keys = list(data.keys())
    print(keys)
    if "sres" in keys and isinstance(data["sres"], pd.DataFrame):
        st.session_state["sres"] = data["sres"]


@st.cache_data
def load_data(prefix: str, base_url: str, params: dict) -> pd.DataFrame:
    api_session = ApiConsumer(base_url)
    data = api_session.get_all(prefix, params)
    return data


def main():
    st.title("Create New Entries in Service Reservoir")
    base_url = "http://localhost:8000/"

    st.markdown("## Current SRES Data")
    refresh_btn = st.button("Refresh SRES Data :arrows_counterclockwise:")
    live_sres_data = load_data(
        "sres/", base_url=base_url, params={"skip": 0, "limit": 500}
    )
    save_session_state({"sres": live_sres_data})

    if refresh_btn:
        st.session_state["sres"] = None
        live_sres_data = load_data(
            "sres/", base_url=base_url, params={"skip": 0, "limit": 500}
        )
        save_session_state({"sres": live_sres_data})

    st.dataframe(live_sres_data[col_order])
    st.divider()
    # include a new form for creating the data
    cols = list(live_sres_data.columns)
    new_form_keys = dict.fromkeys(cols, None)
    sres_form = SresForm(base_url)
    sres_form.create_current_entry_form(new_form_keys)


if __name__ == "__main__":
    page_startup()
    main()
