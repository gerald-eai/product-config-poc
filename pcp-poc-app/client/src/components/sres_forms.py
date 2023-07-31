# Form Components for Sres 
import streamlit as st 
from pydantic import BaseModel 
import schemas.sres_request as SresRequest 
from services.api import ApiConsumer


class SresForm(): 
    
    def __init__(self, base_url): 
        self.api_session = ApiConsumer(base_url=base_url)
    def base_form(self, default_vals: dict):
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
        
        return form, form_inputs
        
    def create_staged_entry_form(self, default_vals: dict): 
        form, form_inputs = self.base_form(default_vals=default_vals)
        
        submit_form = form.form_submit_button("Update Entry")
        if submit_form: 
            try: 
                form_inputs['include_in_dv'] = 1 if form_inputs['include_in_dv'] == 'Yes' else 0
                create_sres_update = SresRequest.CreateNewStagedEntry(**form_inputs)
                print('Newly Created SRES Model\n', create_sres_update)
                for key, value in form_inputs.items(): 
                    print(f"{key}:{value}")
                # run the API that creates the entry
                response = self.api_session.create_staged_entry(endpoint='sres/updates/new-entry', req_body=create_sres_update)
                print(f"Here is your response: {response}")
            except Exception as E: 
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")

    def create_current_entry_form(self, default_vals: dict): 
        form, form_inputs = self.base_form(default_vals=default_vals)
        
        submit_form = form.form_submit_button("Update Entry")
        if submit_form: 
            try: 
                form_inputs['include_in_dv'] = 1 if form_inputs['include_in_dv'] == 'Yes' else 0
                create_sres_update = SresRequest.CreateNewLiveEntry(**form_inputs)
                print('Newly Created SRES Model\n', create_sres_update)
                for key, value in form_inputs.items(): 
                    print(f"{key}:{value}")
                # run the API that creates the entry
                response = self.api_session.create_new_entry(endpoint='sres/live/', req_body=create_sres_update)
                print(f"Here is your response: {response}")
            except Exception as E: 
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")

    def edit_staged_entry_form(self, default_vals: dict): 
        form, form_inputs = self.base_form(default_vals=default_vals)
        
        submit_form = form.form_submit_button("Update Entry")
        if submit_form: 
            try: 
                form_inputs['include_in_dv'] = 1 if form_inputs['include_in_dv'] == 'Yes' else 0
                for key, value in form_inputs.items(): 
                    if key == 'id' or key == 'odmt_sres_id' or key == 'hydraulic_system_name':
                        continue
                    elif value == default_vals[key]:
                        form_inputs[key] = None
                        
                edit_staged_entry = SresRequest.UpdateStagedEntry(**form_inputs)
                print('Updated SRES Model\n', edit_staged_entry)
                
                # run the API that creates the entry
                # response = self.api_session.edit_staged_entry(endpoint=f'sres/updates/{edit_staged_entry.id}', req_body=edit_staged_entry)
                # print(f"Here is your response: {response}")
            except Exception as E: 
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")