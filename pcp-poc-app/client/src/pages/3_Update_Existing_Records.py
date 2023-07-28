import streamlit as st 
from services.api import ApiConsumer
import pandas as pd 
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def check_for_none(data, data_type): 
    if data is None and isinstance(data_type, str): 
        return ''
    else: 
        return 0

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

def aggrid_component(df: pd.DataFrame): 
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True)
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    gridOptions = gb.build()
    
    return AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.MODEL_CHANGED, enable_enterprise_modules=True, theme='streamlit', width=560)

def sres_form_component(): 
    form = st.form(key='sres_form')
    # numeric entry for the odmt sres id
    st.write('Form Component')
    
    pass 

def system_map_form_component(default_vals: dict): 
    st.info(f"You are editing data for the following Hydraulic System: {default_vals['hydraulic_system_name']}")

    form = st.form(key='system_map_form')
    # numeric entry for the odmt sres id
    st.write('Form Component')
    form.text_input("Hydraulic System Name", default_vals['hydraulic_system_name'])
    form.text_input("Area Name", default_vals['area_name'])
    form.text_input("Region Name", default_vals['region_name'])
    form.number_input("ODMT Area ID", default_vals['odmt_area_id'])
    form.text_area("Comments", default_vals['comments'])
    form.form_submit_button("Submit Data")

def contact_tanks_form_component(default_vals: dict): 
    pass


def form_component(key: str,  default_vals: dict): 
    form = st.form(key=key)
    if key == 'sres_form': 
        form.text_input("Hydraulic System Name", default_vals['name'])
        
    # we know what we're editing
    
    pass 


def main(): 
    st.title("Let's talk about Creating a new entry to our live data!")
    base_url = "http://localhost:8000/"
    
    sres_tab, tanks_tab, sysmap_tab = st.tabs(["SRES", "Contact Tanks", "System Mapping"]) 
    # our data is obtained from a dataframe
    with sres_tab: 
        st.markdown("## Current SRES Data")
        live_sres_data = load_data("sres/live", base_url=base_url, params={'skip': 0, 'limit': 450})
        save_session_state({'sres': live_sres_data})
        
        st.write(live_sres_data)
        
    
    with tanks_tab: 
        
        st.markdown("## Current Contact Tank Data")
        live_tanks_data = load_data("contact-tanks/live", base_url=base_url, params={'skip': 0, 'limit': 50})
        save_session_state({'contact_tanks': live_tanks_data})
        
        st.write(live_tanks_data)
        
    with sysmap_tab: 
        st.markdown("## Current System Mapping Data")
        live_sysmap_data = load_data("system-mapping/live", base_url=base_url, params={'skip': 0, 'limit': 50})
        save_session_state({'system_mapping': live_sysmap_data})
        # visualise the ag grid component
        ag_grid = aggrid_component(live_sysmap_data)
        # ag_grid
        
        ag_df = ag_grid['data']
        selected_row = ag_grid['selected_rows']
        if len(selected_row) > 0: 
            print(type(selected_row[0]))
            st.write(selected_row)
            print(selected_row[0])
            system_map_form_component(selected_row[0])
        
        # if the row has been selected then create a form for the user to fill in
        
        
    
    
if __name__ == "__main__": 
    main()
