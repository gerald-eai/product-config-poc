import streamlit as st 
from services.api import ApiConsumer


def main(): 
    st.title("View Audit Records")
    api_session = ApiConsumer("http://localhost:8000/audit")
        
    
if __name__ == "__main__": 
    main()