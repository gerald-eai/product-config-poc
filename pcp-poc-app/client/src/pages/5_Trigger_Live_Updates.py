import streamlit as st
from services.adf import DataFactoryAPIClient
from services.api import DatabaseAPIClient
from datetime import datetime, timedelta
from schemas.adf_schemas import QueryPipelineRunsByFactory, TriggerPipelineRun, PipelineRun
import components.global_components as Global
from schemas.request_models import RequestAll
import pandas as pd
from data.data_processor import col_order


# session state functions
def set_run_id(run_id: str): 
    if "run_id" not in st.session_state: 
        st.session_state["run_id"] = "" 
    st.session_state["run_id"] = run_id
    
def set_active_runs(run_flag: bool): 
    if "active_runs" not in st.session_state: 
        st.session_state["active_runs"] = False
    st.session_state["active_runs"] = run_flag


def set_pending_updates(updates: pd.DataFrame): 
    if "pending_updates" not in st.session_state: 
        st.session_state["pending_updates"] = updates
    st.session_state["pending_updates"] = updates
    

# helper functions
def check_running_pipelines(
    api_client: DataFactoryAPIClient, pipeline_name: str,
) -> bool:
    """_summary_ 
    using an adf client connection, the function checks if there are any running pipeline runs
    return True if at least one run is active 
    False if no active runs
    
    Args:
        api_client (DataFactoryAPIClient): _description_
        pipeline_name (str): _description_
    
    Returns:
        bool: _description_
    
    Raises:
        Exception: _description_
    
    >>> check_running_pipelines(api_client, "POC_UpdateFunctionSet")
    True
    >>> check_running_pipelines(api_client, "POC_UpdateFunctionSet")
    False
    """
    start_date = datetime.now() - timedelta(days=5)
    end_date = datetime.now()
    pipeline_runs = api_client.get_most_recent_pipeline_run(
        QueryPipelineRunsByFactory(
            pipelineName=pipeline_name,
            startDate=start_date.isoformat(),
            endDate=end_date.isoformat(),
        )
    )
    st.write(pipeline_runs)
    for run in pipeline_runs: 
        if run.status == "InProgress":
            return (True, run.runId)
    return (False, None)

# need a function that gets all of the updates in the table
def get_pending_updates(db_client: DatabaseAPIClient):
    """_summary_ 
    using a database client connection, the function gets all of the updates in the table
    and returns them as a dataframe
    
    Args:
        db_client (DatabaseAPIClient): _description_
    
    Returns:
        pd.DataFrame: _description_
    
    >>> get_pending_updates(db_client)
    """
    sres_data = db_client.get_all("/sres", params=RequestAll(skip=0, limit=500))
    group = sres_data.groupby("production_state")
    sres_updates = group.get_group("pending")
    set_pending_updates(sres_updates[col_order])


def main():
    st.title("Update the records in the table.")
    st.caption(
        "Use this page to update the records from 'pending' to 'live' so that it can be pushed to production."
    )
    adf_client = DataFactoryAPIClient(base_url="http://localhost:8000")
    db_client = DatabaseAPIClient(base_url="http://localhost:8000")
    check_runs_tab, trigger_updates_tab= st.tabs(
        [
            "Check Pipeline Run Activity",
            "Trigger Updates Pipeline"
        ]
    )

    with check_runs_tab:
        check_pipelines = st.button("Check Pipeline Run Activity")
        if check_pipelines:
            # get the list of pipelines in the datafactory
            pipelines = adf_client.get_pipelines_list()
            st.write(pipelines)

        st.divider()
        check_most_recent_runs = st.button("Check for Active Pipeline Runs")
        
        if check_most_recent_runs:
            active_runs,active_run_id= check_running_pipelines(adf_client, "POC_UpdateFunctionSet")
            if active_runs: 
                st.error("Cannot Trigger New Pipeline when there are already running pipelines")
                st.text(f"Running Pipeline ID: {active_run_id}")
                set_run_id(active_run_id)
                set_active_runs(active_runs)
            else: 
                set_active_runs(False)
                set_run_id("")
                st.success("There are no active pipeline runs!")
    
    with trigger_updates_tab: 
        if "active_runs" not in st.session_state: 
            st.error("Check for the most recent Pipeline run!")
        else: 
            if st.session_state["active_runs"]:
                st.error("Cannot Trigger New Pipeline when there are already running pipelines")
            else: 
                st.markdown("**Pending SRES Updates**")
                get_pending_updates(db_client=db_client)
                ag_grid = Global.aggrid_component(st.session_state["pending_updates"])
                st.divider()
                # approve changes and trigger the updates
                approve_changes = st.checkbox("Approve Changes?")  
                if approve_changes:
                    st.info("You can trigger the ADF Pipeline")
                    trigger_adf_btn = st.button("Trigger the ADF Pipeline")
                    st.warning("Ensure you are satisfied with all pending updates before triggering the pipeline")
                    if trigger_adf_btn:
                        req_body = TriggerPipelineRun(pipelineName="POC_UpdateFunctionSet")
                        pipeline_run = adf_client.trigger_pipeline_run(request_body=req_body)
                        new_run_id = pipeline_run.runId
                        print(f"The new pipeline run id: \n{new_run_id}")
                        set_run_id(new_run_id)


if __name__ == "__main__":
    main()
