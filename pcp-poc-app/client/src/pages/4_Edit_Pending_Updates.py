import streamlit as st 
from services.api import ApiConsumer
import pandas as pd 
from components.sres_forms import SresForm
from components.system_mapping_forms import SystemMapForm
from components.contact_tank_forms import ContactTankForm
import components.global_components as Global

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
    st.title("Edit Staged Entries in the table!")
    base_url = "http://localhost:8000/"
    
    sres_tab, tanks_tab, sysmap_tab = st.tabs(["SRES", "Contact Tanks", "System Mapping"]) 
    # our data is obtained from a dataframe
    with sres_tab: 
        st.markdown("## Staged SRES Updates ")
        refresh_btn = st.button('Refresh SRES Data :arrows_counterclockwise:')
        staged_sres_data = load_data("sres/updates", base_url=base_url, params={'skip': 0, 'limit': 450})
        save_session_state({'sres': staged_sres_data})
        
        if refresh_btn: 
            st.session_state['sres'] = None
            staged_sres_data = load_data("sres/updates", base_url=base_url, params={'skip': 0, 'limit': 500})
            save_session_state({'sres': staged_sres_data})

        # visualise the ag grid component
        ag_grid = Global.aggrid_component(staged_sres_data)
        selected_row = ag_grid['selected_rows']
        if len(selected_row) > 0: 
            sres_form = SresForm(base_url)
            sres_form.edit_staged_entry_form(selected_row[0])
            
    with tanks_tab: 
        st.markdown("## Staged Contact Tank Updates")
        staged_tanks_data = load_data("contact-tanks/updates", base_url=base_url, params={'skip': 0, 'limit': 50})
        save_session_state({'contact_tanks': staged_tanks_data})
        ctanks_refresh = st.button('Refresh Contact Tanks :arrows_counterclockwise:')
        
        if ctanks_refresh: 
            st.session_state['contact_tanks'] = None
            staged_tanks_data = load_data("contact-tanks/updates", base_url=base_url, params={'skip': 0, 'limit': 150})
            save_session_state({'contact_tanks': staged_tanks_data})
        
        ag_grid = Global.aggrid_component(staged_tanks_data)
        selected_row = ag_grid['selected_rows']
        if len(selected_row) > 0: 
            ctank_form = ContactTankForm(base_url=base_url)
            ctank_form.edit_staged_entry_form(selected_row[0])
        
    with sysmap_tab: 
        refresh_btn = st.button('Refresh Sys Map Data :arrows_counterclockwise:')
        st.markdown("## Staged System Mapping Updates")
        staged_sysmap_data = load_data("system-mapping/updates", base_url=base_url, params={'skip': 0, 'limit': 52})
        save_session_state({'system_mapping': staged_sysmap_data})
        
        if refresh_btn: 
            staged_sysmap_data = load_data("system-mapping/updates", base_url=base_url, params={'skip': 0, 'limit': 50})
            save_session_state({'system_mapping': staged_sysmap_data})
        
        # visualise the ag grid component
        ag_grid = Global.aggrid_component(staged_sysmap_data)
        selected_row = ag_grid['selected_rows']
        if len(selected_row) > 0: 
            # render our form component to edit the data in the current table
            system_map_form = SystemMapForm(base_url=base_url)
            system_map_form.edit_staged_entry_form(selected_row[0])
    
if __name__ == "__main__": 
    main()