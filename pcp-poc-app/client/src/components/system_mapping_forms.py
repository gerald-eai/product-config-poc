# Form Components for Sres 
import streamlit as st 
import schemas.system_mapping_request as SystemMapRequest
from services.api import ApiConsumer


class SystemMapForm(): 
    
    def __init__(self, base_url): 
        self.api_session = ApiConsumer(base_url=base_url)
    
    def base_form(self, default_vals: dict): 
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
        
        return form, form_inputs
                        
    def create_staged_entry_form(self, default_vals: dict): 
        form, form_inputs = self.base_form(default_vals=default_vals)
        submit_form = form.form_submit_button("Edit Sres Entry")
        
        if submit_form: 
            #  try to write the data over the request
            try: 
                st.write("Submitting Data")
                # :TODO: Let's make a comparison of the data and only update the necessary fields
                create_sys_map_update = SystemMapRequest.CreateNewStagedEntry(**form_inputs)
                
                print(f"Create Update Request: {create_sys_map_update}")
                st.info("Refresh to view updated data")
                # make a request to post the data 
                response = self.api_session.create_staged_entry('system-mapping/updates/', req_body=create_sys_map_update)
                print(f"Here is your damned response! {response}")
            
            except Exception as e:
                st.error(f"Unable to submit the form! Issue is {e}")

    def create_current_entry_form(self, default_vals: dict): 
        form, form_inputs = self.base_form(default_vals=default_vals)
        submit_form = form.form_submit_button("Create New Sres Entry")
        
        if submit_form: 
            #  try to write the data over the request
            try: 
                st.write("Submitting Data")
                # :TODO: Let's make a comparison of the data and only update the necessary fields
                create_live_sys_map = SystemMapRequest.CreateNewLiveEntry(**form_inputs)
                
                print(f"Create Update Request: {create_live_sys_map}")
                st.info("Refresh to view updated data")
                # make a request to post the data 
                response = self.api_session.create_new_entry('system-mapping/live/', req_body=create_live_sys_map)
                print(f"Here is your damned response! {response}")
            
            except Exception as e:
                st.error(f"Unable to submit the form! Issue is {e}")

    def edit_staged_entry_form(self, default_vals: dict): 
        form, form_inputs = self.base_form(default_vals=default_vals)
        submit_form = form.form_submit_button("Edit Staged Data")
        
        if submit_form: 
            #  try to write the data over the request
            try: 
                # :TODO: Let's make a comparison of the data and only update the necessary fields
                form_inputs['id'] = default_vals['id']
                for key, value in form_inputs.items(): 
                    if key == 'id' or key == 'hydraulic_system_name':
                        continue
                    elif value == default_vals[key]:
                        form_inputs[key] = None
                edit_staged_sys_map  = SystemMapRequest.EditStagedEntry(**form_inputs)
                print(f"Edit Staged Sys Map Entry: {edit_staged_sys_map}")
                st.info("Refresh to view updated data")
                # make a request to post the data 
                response = self.api_session.edit_staged_entry(f'system-mapping/updates/{edit_staged_sys_map.id}', req_body=edit_staged_sys_map)
                print(f"Here is your damned response! {response}")
            
            except Exception as e:
                st.error(f"Unable to submit the form! Issue is {e}")