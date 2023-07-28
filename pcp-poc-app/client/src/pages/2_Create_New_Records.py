import streamlit as st 
from services.api import ApiConsumer
import pandas as pd 
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

@st.cache_data
def load_data(prefix: str, base_url: str): 
    api_session = ApiConsumer(base_url)
    # we're only loading the live data of whatever is requested

def form_component(): 
    pass 


def main(): 
    st.title("Let's talk about Creating a new entry to our live data!")
    
    sres_tab, tanks_tab, sysmap_tab = st.tabs(["SRES", "Contact Tanks", "System Mapping"])
    
    
    # our data is obtained from a dataframe
    
    
if __name__ == "__main__": 
    main()