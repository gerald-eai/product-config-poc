import streamlit as st 
from services.api import ApiConsumer

def page_startup(): 
    st.set_page_config(layout="wide")
    
@st.cache_data(show_spinner="Request Data from Api...")
def render_live_updates_tables(_api_session: ApiConsumer, endpoint: str, params: dict): 
    # make a request to get live and staged updates data
    st.markdown("## Live")
    live_data =  _api_session.get_all(f"{endpoint}/live/", params=params)
    st.write(live_data)
    
    st.markdown("## Pending Updates")
    staging_data = _api_session.get_all(f"{endpoint}/updates/", params=params)
    st.write(staging_data)

    
def main(): 
    st.title("View Config Records")
    st.divider()
    api_consumer = ApiConsumer("http://localhost:8000/")
    sres_tab, tanks_tab, sys_map_tab = st.tabs(["Sres", "Contact Tanks", "System Mapping"])
    
    with sres_tab: 
        st.markdown("## SRES Data")
        # render the Sres Dataframe
        render_live_updates_tables(api_consumer, "sres", {'skip': 0, 'limit': 375})
            
            
    with tanks_tab: 
        st.markdown("## Contact Tanks")
        # if request_contact_tanks_button: 
        render_live_updates_tables(api_consumer, "contact-tanks", {'skip': 0, 'limit':50})
            
    with sys_map_tab: 
        st.markdown("## System Mapping")
        # if request_sys_maps_button:
        render_live_updates_tables(api_consumer, "system-mapping", {'skip': 0, 'limit':60})
    
    st.divider()
    
    
if __name__ == "__main__": 
    page_startup()
    main()
