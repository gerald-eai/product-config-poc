import pandas as pd 
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from typing import Optional

def aggrid_component(df: pd.DataFrame, table_key:Optional[str]=None): 
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationPageSize=25, paginationAutoPageSize=False)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True)
    gb.configure_selection(selection_mode='single', use_checkbox=True)
    gridOptions = gb.build()
    
    return AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.MODEL_CHANGED, enable_enterprise_modules=True, theme='streamlit', width=560, key=table_key)