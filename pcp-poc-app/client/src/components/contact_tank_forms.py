# Form Components for Sres
import streamlit as st
import schemas.contact_tank_request as ContactTankRequest
from services.api import ApiConsumer
from datetime import datetime


class ContactTankForm:
    def __init__(self, base_url):
        self.api_session = ApiConsumer(base_url=base_url)

    def validate_input(self, input_type, val):
        if isinstance(val, str):
            # can we check that this is not ""
            if val == "" or val == None:
                raise ValueError(f"Input {input_type} cannot be empty")
        else:
            if val == None:
                raise ValueError(f"Input {input_type} cannot be empty")

    def base_form(sele, default_vals: dict):
        form = st.form(key="contact_tank_form", clear_on_submit=False)
        # create keys required for the form component
        keys = list(default_vals.keys())
        form_inputs = dict.fromkeys(
            keys, None
        )  # create emtpy dict to store the user's input

        form_inputs["hydraulic_system_name"] = form.text_input(
            "Hydraulic System Name", default_vals["hydraulic_system_name"]
        )
        form_inputs["sres_name"] = form.text_input(
            "SRES Name", default_vals["sres_name"]
        )
        # form_inputs['odmt_contact_tank_id'] = form.number_input("ODMT Contact Tank ID", default_vals['odmt_contact_tank_id'])
        form_inputs["cell_name"] = form.text_input(
            "Cell Name", default_vals["cell_name"]
        )
        form_inputs["pi_tag_name"] = form.text_input(
            "PI Tag Name", default_vals["pi_tag_name"]
        )
        form_inputs["engineering_unit"] = form.text_input(
            "Engineering Unit", default_vals["engineering_unit"]
        )
        form_inputs["validated_tag"] = form.text_input(
            "Validated Tag", default_vals["validated_tag"]
        )
        form_inputs["operating_level"] = form.number_input(
            "Operating Level", default_vals["operating_level"]
        )
        form_inputs["bwl"] = form.number_input("BWL", default_vals["bwl"])
        form_inputs["twl"] = form.number_input("TWL", default_vals["twl"])
        form_inputs["capacity"] = form.number_input(
            "Capacity", default_vals["capacity"]
        )
        form_inputs["comments"] = form.text_area(
            "Comments", default_vals["comments"])
        form_inputs["include_SDSR"] = form.selectbox(
            "Include in SDSR", ["Yes", "No"], index=0
        )
        form_inputs["include_WPRO"] = form.selectbox(
            "Include in WPRO", ["Yes", "No"], index=0
        )
        form_inputs["include_SRV"] = form.selectbox(
            "Include in SRV", ["Yes", "No"], index=0
        )

        return form, form_inputs

    def create_live_entry_form(self, default_vals: dict):
        st.info(f"You are creating a new entry in the Live Contact Tank Table")
        edit_staged_entry_form, form_inputs = self.base_form(
            default_vals=default_vals)
        submit_form = edit_staged_entry_form.form_submit_button(
            "Create New Contact Tank Entry"
        )
        if submit_form:
            try:
                # compare the default values vs the user input values, if they are different then leave as is, if not then set to None
                form_inputs["include_SDSR"] = (
                    1 if form_inputs["include_SDSR"] == "Yes" else 0
                )
                form_inputs["include_WPRO"] = (
                    1 if form_inputs["include_WPRO"] == "Yes" else 0
                )
                form_inputs["include_SRV"] = (
                    1 if form_inputs["include_SRV"] == "Yes" else 0
                )
                form_inputs["last_modified"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                for key, value in form_inputs.items():
                    if key == "last_modified" or key == "odmt_contact_tank_id":
                        continue
                    else:
                        print(f"{key}:{value}")
                        self.validate_input(input_type=key, val=value)

                create_live_tank_entry = ContactTankRequest.CreateNewLiveEntry(
                    **form_inputs
                )
                print("Updated Contact Tanks Model\n", create_live_tank_entry)
                # run the API that creates the entry
                response = self.api_session.create_new_entry(
                    endpoint="contact-tanks/live", req_body=create_live_tank_entry
                )
                print(f"Here is your response: {response}")
            except Exception as E:
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")

    def create_staged_entry_form(self, default_vals: dict):
        st.info(
            f"You are editing data for the following SRES: {default_vals['sres_name']}"
        )
        staged_entry_form, form_inputs = self.base_form(
            default_vals=default_vals)
        submit_form = staged_entry_form.form_submit_button("Update Entry")
        if submit_form:
            try:
                form_inputs["include_SDSR"] = (
                    1 if form_inputs["include_SDSR"] == "Yes" else 0
                )
                form_inputs["include_WPRO"] = (
                    1 if form_inputs["include_WPRO"] == "Yes" else 0
                )
                form_inputs["include_SRV"] = (
                    1 if form_inputs["include_SRV"] == "Yes" else 0
                )

                create_ctanks_update = ContactTankRequest.CreateNewStagedEntry(
                    **form_inputs
                )
                print("Newly Created Contacts Model\n", create_ctanks_update)
                # run the API that creates the entry
                response = self.api_session.create_staged_entry(
                    endpoint="contact-tanks/updates/", req_body=create_ctanks_update
                )
                print(f"Here is your response: {response}")
            except Exception as E:
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")

    def edit_staged_entry_form(self, default_vals: dict):
        st.info(
            f"You are editing data for the following Staged Contact Tank Update Id: {default_vals['id']}"
        )
        edit_staged_entry_form, form_inputs = self.base_form(
            default_vals=default_vals)
        submit_form = edit_staged_entry_form.form_submit_button(
            "Update Staged Change")

        if submit_form:
            try:
                # compare the default values vs the user input values, if they are different then leave as is, if not then set to None
                form_inputs["include_SDSR"] = (
                    1 if form_inputs["include_SDSR"] == "Yes" else 0
                )
                form_inputs["include_WPRO"] = (
                    1 if form_inputs["include_WPRO"] == "Yes" else 0
                )
                form_inputs["include_SRV"] = (
                    1 if form_inputs["include_SRV"] == "Yes" else 0
                )
                form_inputs["id"] = default_vals["id"]
                for key, value in form_inputs.items():
                    if (
                        key == "id"
                        or key == "odmt_contact_tank_id"
                        or key == "hydraulic_system_name"
                    ):
                        continue
                    elif value == default_vals[key]:
                        form_inputs[key] = None
                edit_staged_ctanks = ContactTankRequest.EditStagedEntry(
                    **form_inputs)
                # run the API that creates the entry
                response = self.api_session.edit_staged_entry(
                    endpoint=f"contact-tanks/updates/{edit_staged_ctanks.id}",
                    req_body=edit_staged_ctanks,
                )
                print(
                    f"!!!!!!!!!!!!Here is your response!!!!!!!!!!!! \n{response}")
            except Exception as E:
                print(f"Error: {E}")
                st.error(f"Error Occurred: {E}")
