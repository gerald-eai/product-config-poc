import streamlit as st 
from services.api import ApiConsumer
import pandas as pd 
from components.sres_forms import SresForm
from components.system_mapping_forms import SystemMapForm
from components.contact_tank_forms import ContactTankForm
import components.global_components as Global

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
    st.title("Create New Records in our Live Table")
    base_url = "http://localhost:8000/"
    
    sres_tab, tanks_tab, sysmap_tab = st.tabs(["SRES", "Contact Tanks", "System Mapping"]) 
    # our data is obtained from a dataframe
    with sres_tab: 
        st.markdown("## Current SRES Data")
        refresh_btn = st.button('Refresh SRES Data :arrows_counterclockwise:')
        live_sres_data = load_data("sres/live", base_url=base_url, params={'skip': 0, 'limit': 450})
        save_session_state({'sres': live_sres_data})
        
        if refresh_btn: 
            st.session_state['sres'] = None
            live_sres_data = load_data("sres/live", base_url=base_url, params={'skip': 0, 'limit': 500})
            save_session_state({'sres': live_sres_data})

        st.dataframe(live_sres_data) 
        st.divider()
        # include a new form for creating the data
        cols = list(live_sres_data.columns)
        new_form_keys = dict.fromkeys(cols, None)
        sres_form = SresForm(base_url)
        sres_form.create_current_entry_form(new_form_keys)
        
        
    with tanks_tab: 
        st.markdown("## Current Contact Tank Data")
        live_tanks_data = load_data("contact-tanks/live", base_url=base_url, params={'skip': 0, 'limit': 50})
        save_session_state({'contact_tanks': live_tanks_data})
        ctanks_refresh = st.button('Refresh Contact Tanks :arrows_counterclockwise:')
        
        if ctanks_refresh: 
            st.session_state['contact_tanks'] = None
            live_tanks_data = load_data("contact-tanks/live", base_url=base_url, params={'skip': 0, 'limit': 150})
            save_session_state({'contact_tanks': live_tanks_data})
        
        st.dataframe(live_tanks_data)
        st.divider()
        cols = list(live_tanks_data.columns)
        new_form_keys = dict.fromkeys(cols, None)
        ctank_form = ContactTankForm(base_url)
        ctank_form.create_live_entry_form(new_form_keys)

        
    with sysmap_tab: 
        st.markdown("## Current System Mapping Data")
        live_sysmap_data = load_data("system-mapping/live", base_url=base_url, params={'skip': 0, 'limit': 52})
        save_session_state({'system_mapping': live_sysmap_data})
        sysmap_refresh = st.button('Refresh System Mapping :arrows_counterclockwise:')
        
        if sysmap_refresh: 
            st.session_state['system_mapping'] = None
            live_sysmap_data = load_data("system-mapping/live", base_url=base_url, params={'skip': 0, 'limit': 150})
            save_session_state({'system_mapping': live_sysmap_data})

        st.dataframe(live_sysmap_data)
        st.divider()
        cols = list(live_sysmap_data.columns)
        print(cols)
        new_form_keys = dict.fromkeys(cols, None)
        sys_map_form = SystemMapForm(base_url)
        sys_map_form.create_current_entry_form(new_form_keys)
        
        
if __name__ == "__main__": 
    page_startup()
    main()