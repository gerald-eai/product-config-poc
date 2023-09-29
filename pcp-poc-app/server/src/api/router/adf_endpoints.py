# use this for connecting to the ADF APIs
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_adf_pipelines_service
from api.requests.adf_requests import TriggerPipelineRequest, PipelineRunFiltersRequest
from services.adf_pipelines_service import DataFactoryService
import schemas.adf_schema as DataFactory
from typing import Optional, List
from datetime import datetime, timedelta


router = APIRouter(prefix="/data-factory", tags=["ADF Query Endpoints"])


@router.get("/pipelines", response_model=List[DataFactory.Pipeline])
def list_adf_pipelines(
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    """_summary_
    Lists all of the pipelines in the Data Factory
    
    Args:
        adf_service (DataFactoryService, optional): adf service responsible for our ADF methods. Defaults to Depends(get_adf_pipelines_service).

    Raises:
        HTTPException: _description_

    Returns:
        List[DataFactory.Pipeline]: List of pipelines in the datafactory
    """
    pipelines_list = adf_service.list_by_factory()
    if pipelines_list is None:
        raise HTTPException(status_code=404, detail="No pipelines found")
    return pipelines_list


@router.get("/pipelines/{pipeline_name}", response_model=DataFactory.Pipeline)
def get_adf_pipeline(
    pipeline_name: str,
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    """_summary_
    Get Pipeline based on the pipeline name. 

    Args:
        pipeline_name (str): _description_ pipeline to retrieve
        adf_service (DataFactoryService, optional): adf service responsible for our ADF methods. Defaults to Depends(get_adf_pipelines_service).

    Raises:
        HTTPException: _description_

    Returns:
        DataFactory.Pipeline: Pipeline returned
    """
    pipeline_info = adf_service.get_pipeline(pipeline_name=pipeline_name)
    if pipeline_info is None:
        raise HTTPException(status_code=404, detail="No pipelines with that name found")
    return pipeline_info


@router.get("/pipelines/runs/{run_id}", response_model=DataFactory.PipelineRun)
def get_adf_pipeline_run(
    run_id: str, adf_service: DataFactoryService = Depends(get_adf_pipelines_service)
):
    """_summary_
    Endpoint to get an adf pipeline run information. 
    
    Args:
        run_id (str): _description_ ID of the ADF Pipeline Run
        adf_service (DataFactoryService, optional): adf service responsible for our ADF methods. Defaults to Depends(get_adf_pipelines_service).

    Raises:
        HTTPException: _description_

    Returns:
        DataFactory.PipelineRun: Pipeline run information
    """
    pipeline_run_info = adf_service.get_pipeline_run(run_id=run_id)
    if pipeline_run_info is None:
        raise HTTPException(
            status_code=404, detail="No pipeline run with that id found"
        )
    return pipeline_run_info


@router.post("/pipelines/runs/{pipeline_name}/trigger", response_model=DataFactory.CreatePipelineRun)
def trigger_adf_pipeline_run(
    pipeline_name: str,
    query_params: Optional[TriggerPipelineRequest] = None,
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    """_summary_
    Triggers an ADF Pipeline
    
    Args:
        pipeline_name (str): name of the pipeline to trigger
        query_params (Optional[TriggerPipelineRequest], optional): optional pipeline trigger params. Defaults to None.
        adf_service (DataFactoryService, optional): adf service responsible for our ADF methods. Defaults to Depends(get_adf_pipelines_service).

    Raises:
        HTTPException: _description_

    Returns:
        DataFactory.CreatePipelineRun: Run ID of the triggered pipeline run
    """
    response = adf_service.create_job_run(pipeline_name, query_params)
    print(f"Response of triggering the pipeline: {response}")
    if response is None:
        raise HTTPException(status_code=400, detail="Pipeline could not be triggered.")
    return response


@router.post("/pipelines/runs/most-recent", response_model=List[DataFactory.PipelineRunByFactory])
def get_recent_pipeline_runs(
    filters_request: PipelineRunFiltersRequest,
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    """_summary_
    Lists all of the pipeline runs in a data factory
    
    Args:
        filters_request (PipelineRunFiltersRequest): _description_
        adf_service (DataFactoryService, optional): adf service responsible for our ADF methods. Defaults to Depends(get_adf_pipelines_service).

    Raises:
        HTTPException: _description_

    Returns:
        List[DataFactory.PipelineRunByFactory]: List of pipeline runs in the datafactory
    """

    most_recent_runs = adf_service.most_recent_runs(
        filters_request.pipelineName, filters_request.startDate, filters_request.endDate
    )
    if most_recent_runs is None:
        raise HTTPException(
            status_code=404, detail="Pipeline Runs could not be obtained"
        )
    return most_recent_runs
