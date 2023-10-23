import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from typing import Optional


def aggrid_component(df: pd.DataFrame, table_key: Optional[str] = None) -> AgGrid:
    """_summary_
    The function uses the GridOptionsBuilder class from the st_aggrid library to configure and return an AG Grid component.

    Args:
        df (pd.DataFrame): data to display in the AG Grid component
        table_key (Optional[str], optional): Table name. Defaults to None.

    Returns:
        AgGrid: AgGrid component
    """
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationPageSize=25, paginationAutoPageSize=False)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gridOptions = gb.build()

    return AgGrid(
        df,
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        enable_enterprise_modules=True,
        theme="streamlit",
        width=560,
        key=table_key,
    )
