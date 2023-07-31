import streamlit as st 
from services.api import ApiConsumer
import pandas as pd 
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

import schemas.system_mapping_request as SystemMappingRequests
import schemas.sres_request as SresRequests
import schemas.contact_tank_request as ContactTankRequest
    
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

def sres_form_component(default_vals: dict, api_session: ApiConsumer): 
    st.info(f"You are editing data for the following SRES: {default_vals['sres_name']}")
    # render our form widget
    form = st.form(key='sres_form', clear_on_submit=False)
    # create keys required for the form component
    keys = list(default_vals.keys())
    form_inputs = dict.fromkeys(keys, None) # create emtpy dict to store the user's input
    print("Dictionary is this: \n", default_vals)
    form_inputs['sres_name'] = form.text_input("SRES Name", default_vals['sres_name'])
    form_inputs['hydraulic_system_name'] = form.text_input("Hydraulic System Name", default_vals['hydraulic_system_name'])
    form_inputs['odmt_sres_id'] = form.number_input("ODMT SRES ID", default_vals['odmt_sres_id'])
    form_inputs['cell_name'] = form.text_input("Cell Name", default_vals['cell_name'])
    form_inputs["pi_tag_name"] = form.text_input("PI Tag Name", default_vals["pi_tag_name"])
    form_inputs['operating_level'] = form.number_input("Operating Level", default_vals['operating_level'])
    form_inputs['bwl'] = form.number_input("BWL", default_vals['bwl'])
    form_inputs['twl'] = form.number_input("TWL", default_vals['twl'])
    form_inputs['capacity'] = form.number_input("Capacity", default_vals['capacity'])
    form_inputs['include_exclude'] = form.selectbox("Include/Exclude", ['Include', 'Exclude'], index=0)
    form_inputs['comments'] = form.text_area("Comments", default_vals['comments'])
    form_inputs['include_in_dv'] = form.selectbox("Include in DV", ['Yes', 'No'], index=0)
    form_inputs['turnover_target_lower'] = form.number_input("Turnover Target Lower", default_vals['turnover_target_lower'])
    form_inputs['turnover_target_upper'] = form.number_input("Turnover Target Upper", default_vals['turnover_target_upper'])
    form_inputs['sm_record_id'] = form.text_input("SM Record ID", default_vals['sm_record_id'])
    form_inputs['validated_tag'] = form.text_input("Validated Tag", default_vals['validated_tag'])
    form_inputs['engineering_unit'] = form.text_input("Engineering Unit", default_vals['engineering_unit'])

    submit_form = form.form_submit_button("Update Entry")
    if submit_form: 
        try: 
            form_inputs['include_in_dv'] = 1 if form_inputs['include_in_dv'] == 'Yes' else 0
            create_sres_update = SresRequests.CreateNewStagedEntry(**form_inputs)
            print('Newly Created SRES Model\n', create_sres_update)
            for key, value in form_inputs.items(): 
                print(f"{key}:{value}")
            # run the API that creates the entry
            response = api_session.update_existing_entry(endpoint='sres/updates/new-entry', req_body=create_sres_update)
            print(f"Here is your response: {response}")
        except Exception as E: 
            print(f"Error: {E}")
            st.error(f"Error Occurred: {E}")

def system_map_form_component(default_vals: dict, api_session: ApiConsumer): 
    st.info(f"You are editing data for the following Hydraulic System: {default_vals['hydraulic_system_name']}")
    # render our form widget
    form = st.form(key='system_map_form', clear_on_submit=False)
    # create keys required for the form component
    keys = list(default_vals.keys())
    form_inputs = dict.fromkeys(keys, None) # create emtpy dict to store the user's input
    
    form_inputs['hydraulic_system_name'] = form.text_input("Hydraulic System Name", default_vals['hydraulic_system_name'])
    form_inputs['area_name'] = form.text_input("Area Name", default_vals['area_name'])
    form_inputs['region_name'] = form.text_input("Region Name", default_vals['region_name'])
    form_inputs['odmt_area_id'] = form.number_input("ODMT Area ID", default_vals['odmt_area_id'])
    form_inputs['comments'] = form.text_area("Comments", default_vals['comments'])
    
    submit_form = form.form_submit_button("Submit Data")
    
    if submit_form: 
        #  try to write the data over the request
        try: 
            st.write("Submitting Data")
            # :TODO: Let's make a comparison of the data and only update the necessary fields
            create_sys_map_update = SystemMappingRequests.CreateNewStagedUpdate(**form_inputs)
            
            print(f"Create Update Request: {create_sys_map_update}")
            st.info("Refresh to view updated data")
            # make a request to post the data 
            response = api_session.update_existing_entry('system-mapping/updates/', req_body=create_sys_map_update)
            print(f"Here is your damned response! {response}")
        
        except Exception as e:
            st.error(f"Unable to submit the form! Issue is {e}")
    

def contact_tanks_form_component(default_vals: dict, api_session: ApiConsumer): 
    st.info(f"You are editing data for the following SRES: {default_vals['sres_name']}")
    # render our form widget
    form = st.form(key='sres_form', clear_on_submit=False)
    # create keys required for the form component
    keys = list(default_vals.keys())
    form_inputs = dict.fromkeys(keys, None) # create emtpy dict to store the user's input
    print("Dictionary is this: \n", default_vals)
    form_inputs['sres_name'] = form.text_input("SRES Name", default_vals['sres_name'])
    form_inputs['hydraulic_system_name'] = form.text_input("Hydraulic System Name", default_vals['hydraulic_system_name'], disabled=True)
    form_inputs['odmt_contact_tank_id'] = form.number_input("ODMT Contact Tank ID", default_vals['odmt_contact_tank_id'], disabled=True)
    form_inputs['cell_name'] = form.text_input("Cell Name", default_vals['cell_name'])
    form_inputs['pi_tag_name'] = form.text_input("PI Tag Name", default_vals["pi_tag_name"])
    form_inputs['validated_tag'] = form.text_input("Validated Tag", default_vals['validated_tag'])
    form_inputs['engineering_unit'] = form.text_input("Engineering Unit", default_vals['engineering_unit'])
    form_inputs['operating_level'] = form.number_input("Operating Level", default_vals['operating_level'])
    form_inputs['bwl'] = form.number_input("BWL", default_vals['bwl'])
    form_inputs['twl'] = form.number_input("TWL", default_vals['twl'])
    form_inputs['capacity'] = form.number_input("Capacity", default_vals['capacity'])
    form_inputs['comments'] = form.text_area("Comments", default_vals['comments'])
    form_inputs['include_SDSR'] = form.selectbox("Include in SDSR", ['Yes', 'No'], index=0)
    form_inputs['include_WPRO'] = form.selectbox("Include in WPRO", ['Yes', 'No'], index=0)
    form_inputs['include_SRV'] = form.selectbox("Include in SRV", ['Yes', 'No'], index=0)
    

    submit_form = form.form_submit_button("Update Entry")
    if submit_form: 
        try: 
            form_inputs['include_SDSR'] = 1 if form_inputs['include_SDSR'] == 'Yes' else 0
            form_inputs['include_WPRO'] = 1 if form_inputs['include_WPRO'] == 'Yes' else 0
            form_inputs['include_SRV'] = 1 if form_inputs['include_SRV'] == 'Yes' else 0
            
            create_ctanks_update = ContactTankRequest.CreateNewStagedEntry(**form_inputs)
            print('Newly Created Contacts Model\n', create_ctanks_update)
            # run the API that creates the entry
            response = api_session.update_existing_entry(endpoint='contact-tanks/updates/', req_body=create_ctanks_update)
            print(f"Here is your response: {response}")
        except Exception as E: 
            print(f"Error: {E}")
            st.error(f"Error Occurred: {E}")
    pass

def main(): 
    st.title("Update one of the entries in the Live Table")
    base_url = "http://localhost:8000/"
    api_client = ApiConsumer(base_url=base_url)
    
    sres_tab, tanks_tab, sysmap_tab = st.tabs(["SRES", "Contact Tanks", "System Mapping"]) 
    # our data is obtained from a dataframe
    with sres_tab: 
        st.markdown("## Current SRES Data")
        refresh_btn = st.button('Refresh SRES Data :arrows_counterclockwise:')
        live_sres_data = load_data("sres/live", base_url=base_url, params={'skip': 0, 'limit': 450})
        save_session_state({'sres': live_sres_data})
        
        if refresh_btn: 
            live_sres_data = load_data("sres/live", base_url=base_url, params={'skip': 0, 'limit': 500})
            save_session_state({'sres': live_sres_data})
            
        # visualise the ag grid component
        ag_grid = aggrid_component(live_sres_data)
        # ag_grid
        selected_row = ag_grid['selected_rows']
        if len(selected_row) > 0: 
            print(type(selected_row[0]))
            st.write(selected_row)
            print(selected_row[0])
            # render our form component to edit the data in the current table
            sres_form_component(selected_row[0],api_session=api_client)
            
    with tanks_tab: 
        st.markdown("## Current Contact Tank Data")
        live_tanks_data = load_data("contact-tanks/live", base_url=base_url, params={'skip': 0, 'limit': 50})
        save_session_state({'contact_tanks': live_tanks_data})
        ctanks_refresh = st.button('Refresh Contact Tanks :arrows_counterclockwise:')
        
        if ctanks_refresh: 
            live_tanks_data = load_data("contact-tanks/live", base_url=base_url, params={'skip': 0, 'limit': 150})
            save_session_state({'contact_tanks': live_tanks_data})
        
        ag_grid = aggrid_component(live_tanks_data)
        selected_row = ag_grid['selected_rows']
        if len(selected_row) > 0: 
            print(type(selected_row[0]))
            contact_tanks_form_component(selected_row[0], api_session=api_client)
        
        
    with sysmap_tab: 
        refresh_btn = st.button('Refresh Sys Map Data :arrows_counterclockwise:')
        st.markdown("## Current System Mapping Data")
        live_sysmap_data = load_data("system-mapping/live", base_url=base_url, params={'skip': 0, 'limit': 52})
        save_session_state({'system_mapping': live_sysmap_data})
        
        if refresh_btn: 
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
            # render our form component to edit the data in the current table
            system_map_form_component(selected_row[0], api_session=api_client)
                    
 
if __name__ == "__main__": 
    main()
