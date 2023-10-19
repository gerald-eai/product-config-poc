import streamlit as st
from core.utils import load_data, get_api_client, page_startup


def main():
    """Renders the table required to view the Audit Log records."""
    st.title("View Audit Records")
    api_client = get_api_client("http://localhost:8000/")

    refresh_btn = st.button("Load Audit Records")
    if refresh_btn:
        audit_log_df = load_data(
            api_client,
            "audit/",
            params={"skip": 0, "limit": 450},
        )
        st.dataframe(audit_log_df)


if __name__ == "__main__":
    page_startup()
    main()
