import streamlit as st 
from services.api import ApiConsumer

def page_startup(): 
    st.set_page_config(layout="wide")
    
@st.cache_data(show_spinner="Request Data from Api...")
def render_live_tables(_api_session: ApiConsumer, endpoint: str, params: dict): 
    # make a request to get live and staged updates data
    live_data =  _api_session.get_all(f"{endpoint}/", params=params)
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
