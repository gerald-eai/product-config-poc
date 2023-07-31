import streamlit as st 
import pandas as pd 
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

def aggrid_component(df: pd.DataFrame): 
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True)
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    gridOptions = gb.build()
    
    return AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.MODEL_CHANGED, enable_enterprise_modules=True, theme='streamlit', width=560)