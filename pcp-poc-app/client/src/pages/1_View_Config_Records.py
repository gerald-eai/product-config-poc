import streamlit as st 
from services.api import ApiConsumer

desired_order = [
            "odmt_sres_id",
            "hydraulic_system_name",
            "sres_name",
            "cell_name",
            "pi_tag_name",
            "sm_record_id",
            "operating_level",
            "bwl",
            "twl",
            "capacity",
            "engineering_unit",
            "validated_tag",
            "turnover_target_lower",
            "turnover_target_upper",
            "comments",
            "include_in_dv",
            "include_exclude",
            "production_state",
            "last_modified",
        ]

def page_startup(): 
    st.set_page_config(layout="wide")
    
@st.cache_data(show_spinner="Request Data from Api...")
def render_live_tables(_api_session: ApiConsumer, endpoint: str, params: dict): 
    # make a request to get live and staged updates data
    live_data =  _api_session.get_all(f"{endpoint}/", params=params)
    live_data = live_data[desired_order]
    st.write(live_data)

    
def main(): 
    st.title("View Service Reservoir Storage Config Records")
    st.divider()
    api_consumer = ApiConsumer("http://localhost:8000/")
    st.markdown("## SRES")
    render_live_tables(api_consumer, "sres", {'skip': 0, 'limit': 500})
    st.divider()
    
    
if __name__ == "__main__": 
    page_startup()
    main()
