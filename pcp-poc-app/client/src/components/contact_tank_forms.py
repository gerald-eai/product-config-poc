# Form Components for Sres
import streamlit as st
import schemas.contact_tank_request as ContactTankRequest
from services.api import ApiConsumer


class ContactTankForm:
    def __init__(self, base_url):
        self.api_session = ApiConsumer(base_url=base_url)

    def validate_input(self, input_type, val):
        pass

    def base_form(sele, default_vals: dict):
        pass

    def create_staged_entry_form(self, default_vals: dict):
        pass

    def create_live_entry_form(self, default_vals: dict):
        pass

    def edit_staged_entry_form(self, default_vals: dict):
        pass
