import streamlit as st 
from services.api import ApiConsumer
import pandas as pd 
from components.sres_forms import SresForm
from components.system_mapping_forms import SystemMapForm
from components.contact_tank_forms import ContactTankForm
import components.global_components as Global

desired_order = [
            "odmt_sres_id",
            "hydraulic_system_name",
            "sres_name",
            "cell_name",
            "pi_tag_name",
            "sm_record_id",
            "operating_level",
            "bwl",
            "twl",
            "capacity",
            "engineering_unit",
            "validated_tag",
            "turnover_target_lower",
            "turnover_target_upper",
            "comments",
            "include_in_dv",
            "include_exclude",
            "production_state",
            "last_modified",
        ]

def page_startup(): 
    st.set_page_config(layout="wide")

def save_session_state(data:dict):
    keys = list(data.keys())
    print(keys)
    if 'sres' in keys and isinstance(data['sres'], pd.DataFrame): 
        st.session_state['sres'] = data['sres']
    if 'system_mapping' in keys and isinstance(data['system_mapping'], pd.DataFrame): 
        st.session_state['system_mapping'] = data['system_mapping'] 
    if 'contact_tanks' in keys and isinstance(data['contact_tanks'], pd.DataFrame): 
        st.session_state['contact_tanks'] = data['contact_tanks']
        
@st.cache_data
def load_data(prefix: str, base_url: str, params: dict) -> pd.DataFrame: 
    api_session = ApiConsumer(base_url)
    # we're only loading the live data of whatever is requested
    data = api_session.get_all(prefix, params)
    return data


def main(): 
    st.title("Create New Entries in Service Reservoir")
    base_url = "http://localhost:8000/"
    
    # sres_tab, tanks_tab, sysmap_tab = st.tabs(["SRES", "Contact Tanks", "System Mapping"]) 
    # our data is obtained from a dataframe
    
    st.markdown("## Current SRES Data")
    refresh_btn = st.button('Refresh SRES Data :arrows_counterclockwise:')
    live_sres_data = load_data("sres/", base_url=base_url, params={'skip': 0, 'limit': 500})
    save_session_state({'sres': live_sres_data})
    
    if refresh_btn: 
        st.session_state['sres'] = None
        live_sres_data = load_data("sres/", base_url=base_url, params={'skip': 0, 'limit': 500})
        live_sres_data = live_sres_data[desired_order]
        save_session_state({'sres': live_sres_data})

    st.dataframe(live_sres_data[desired_order]) 
    st.divider()
    # include a new form for creating the data
    cols = list(live_sres_data.columns)
    new_form_keys = dict.fromkeys(cols, None)
    sres_form = SresForm(base_url)
    sres_form.create_current_entry_form(new_form_keys)
        
        
if __name__ == "__main__": 
    page_startup()
    main()