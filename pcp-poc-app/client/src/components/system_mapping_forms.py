# Form Components for System Mapping
# Component isn't required for POC, but is kept for future implementations
import streamlit as st 
import schemas.system_mapping_request as SystemMapRequest
from services.api import DatabaseAPIClient
import datetime as datetime 

class SystemMapForm(): 
    
    def __init__(self, base_url): 
        self.api_session = DatabaseAPIClient(base_url=base_url)
    
    def base_form(self, default_vals: dict): 
        pass
    
    def validate_input(self, input_type, val):
        pass
            
    def create_current_entry_form(self, default_vals: dict): 
        pass

    def create_staged_entry_form(self, default_vals: dict): 
        pass
                
    def edit_staged_entry_form(self, default_vals: dict): 
        pass