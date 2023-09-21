# Form Components for Sres 
import streamlit as st 
import schemas.sres_request as SresRequest 
from services.api import ApiConsumer
from data.data_processor import load_hydraulic_systems

class SresForm(): 
    
    def __init__(self, base_url): 
        self.api_session = ApiConsumer(base_url=base_url)
    
    def validate_input(self, input_type, val):
        if isinstance(val, str): 
            # can we check that this is not ""
            if val == "" or val == None or val=="None": 
                st.markdown('<style>input[type="text"] {border: 2px solid red;}</style>', unsafe_allow_html=True)
                st.warning("Please enter a value.")
                raise ValueError(f"Input {input_type} cannot be empty")
            
        else: 
            if val == None: 
                st.markdown('<style>input[type="text"] {border: 2px solid red;}</style>', unsafe_allow_html=True)
                st.warning("Please enter a value.")
                raise ValueError(f"Input {input_type} cannot be empty")

    def base_form(self, default_vals: dict):
        
        # render our form widget
        form = st.form(key='sres_form', clear_on_submit=False)
        # create keys required for the form component
        hydraulic_names = load_hydraulic_systems()
        keys = list(default_vals.keys())
        form_inputs = dict.fromkeys(keys, None) # create emtpy dict to store the user's input
        
        form_inputs['hydraulic_system_name'] = form.selectbox("Hydraulic System Names", options=hydraulic_names, placeholder="Select...")
        form_inputs['sres_name'] = form.text_input("SRES Name", default_vals['sres_name']).strip()
        form_inputs['cell_name'] = form.text_input("Cell Name", default_vals['cell_name']).strip()
        form_inputs['pi_tag_name'] = form.text_input("PI Tag Name", default_vals["pi_tag_name"]).strip()
        form_inputs['operating_level'] = form.number_input("Operating Level", default_vals['operating_level'])
        form_inputs['bwl'] = form.number_input("BWL", default_vals['bwl'])
        form_inputs['twl'] = form.number_input("TWL", default_vals['twl'])
        form_inputs['capacity'] = form.number_input("Capacity", default_vals['capacity'])
        form_inputs['include_exclude'] = form.selectbox("Include/Exclude", ['Include', 'Exclude'], index=0)
        form_inputs['comments'] = form.text_area("Comments", default_vals['comments']).strip()
        form_inputs['include_in_dv'] = form.selectbox("Include in DV", ['Yes', 'No'], index=0)
        form_inputs['turnover_target_lower'] = form.number_input("Turnover Target Lower", default_vals['turnover_target_lower'])
        form_inputs['turnover_target_upper'] = form.number_input("Turnover Target Upper", default_vals['turnover_target_upper'])
        form_inputs['sm_record_id'] = form.text_input("SM Record ID", default_vals['sm_record_id']).strip()
        form_inputs['validated_tag'] = form.text_input("Validated Tag", default_vals['validated_tag']).strip()
        form_inputs['engineering_unit'] = form.text_input("Engineering Unit", default_vals['engineering_unit']).strip()
        
        return form, form_inputs

    def create_current_entry_form(self, default_vals: dict): 
        st.info(f"You are creating a new entry in the live SRES Table")
        form, form_inputs = self.base_form(default_vals=default_vals)
        
        submit_form = form.form_submit_button("Create New Sres Entry")
        if submit_form: 
            try: 
                form_inputs['include_in_dv'] = 1 if form_inputs['include_in_dv'] == 'Yes' else 0
                form_inputs['production_state'] = "pending"
                # print(f"DateTime Object: {type(form_inputs['last_modified'])}")
                create_new_entry = SresRequest.CreateNewSres(**form_inputs)
                print('Newly Created SRES Model\n', create_new_entry)
               
                for key, value in form_inputs.items(): 
                    print(f"{key}:{value}")
                    if key == 'odmt_sres_id' or key == 'last_modified' or key == 'comments': 
                        continue 
                    else: 
                        self.validate_input(input_type=key, val=value)
                
                # run the API that creates the entry
                response = self.api_session.create_new_entry(endpoint='sres/', req_body=create_new_entry)
                print(f"Here is your response: {response}")
                if (not response.empty): 
                    st.success("Successfully created a new Pending entry in the SRES table!")
            
            except Exception as E: 
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")
                
                
    def edit_entry_form(self, default_vals: dict): 
        st.info(f"You are editing data for the following SRES: {default_vals['sres_name']}, SRES ID: {default_vals['odmt_sres_id']}, {default_vals['include_exclude']}")
        form, form_inputs = self.base_form(default_vals=default_vals)
        
        submit_form = form.form_submit_button("Update Entry")
        if submit_form: 
            try: 
                # :TODO: validate the inputs
                form_inputs['include_in_dv'] = 1 if form_inputs['include_in_dv'] == 'Yes' else 0
                form_inputs['include_exclude'] = 1 if form_inputs['include_in_dv'] == 'Include' else 0
                form_inputs['odmt_sres_id'] = default_vals['odmt_sres_id']
                form_inputs['production_state'] = "pending"
                for key, value in form_inputs.items(): 
                    print(f"{key}, {value}")
                    if key == 'odmt_sres_id' or key == 'hydraulic_system_name':
                        continue
                    elif value == default_vals[key]:
                        form_inputs[key] = None
                print(f"Trimmed Form Input: {form_inputs}")      
                edit_staged_entry = SresRequest.UpdateSres(**form_inputs)
                print('Updated SRES Model\n', edit_staged_entry)
                
                # run the API that creates the entry
                response = self.api_session.edit_entry(endpoint=f'sres/{str(int(edit_staged_entry.odmt_sres_id))}', req_body=edit_staged_entry)
                print(f"Here is your response: {response}")
                if (not response.empty): 
                    st.success("Successfully edited the staged entry!")
                
            except Exception as E: 
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")