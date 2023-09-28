# use this for connecting to the ADF APIs
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_adf_pipelines_service
from api.requests.adf_requests import TriggerPipelineRequest, PipelineRunFiltersRequest
from services.adf_pipelines_service import DataFactoryService
from typing import Optional
from datetime import datetime, timedelta


router = APIRouter(prefix="/data-factory", tags=["ADF Query Endpoints"])


@router.get("/pipelines")
def list_adf_pipelines(
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    response = adf_service.list_by_factory()
    if response is None:
        raise HTTPException(status_code=404, detail="No pipelines found")
    print(f"Response: {response}")
    for item in response:
        print(f"Pipeline: {item}")
    return response


@router.get("/pipelines/{pipeline_name}")
def get_adf_pipeline(
    pipeline_name: str,
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    response = adf_service.get_pipeline(pipeline_name=pipeline_name)
    if response is None:
        raise HTTPException(status_code=404, detail="No pipelines with that name found")
    print(f"Response: {response}")
    return response


@router.get("/pipelines/runs/{run_id}")
def get_adf_pipeline_run(
    run_id: str, adf_service: DataFactoryService = Depends(get_adf_pipelines_service)
):
    response = adf_service.get_pipeline_run(run_id=run_id)
    if response is None:
        raise HTTPException(
            status_code=404, detail="No pipeline run with that id found"
        )
    print(f"Response: {response}")
    return response


@router.post("/pipelines/runs/{pipeline_name}/trigger")
def trigger_adf_pipeline_run(
    pipeline_name: str,
    query_params: Optional[TriggerPipelineRequest] = None,
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    response = adf_service.create_job_run(pipeline_name, query_params)
    print(f"Response of triggering the pipeline: {response}")
    if response is None:
        raise HTTPException(status_code=400, detail="Pipeline could not be triggered.")
    return response


@router.post("/pipelines/runs/most-recent")
def get_recent_pipeline_runs(
    filters_request: PipelineRunFiltersRequest,
    adf_service: DataFactoryService = Depends(get_adf_pipelines_service),
):
    most_recent_runs = adf_service.most_recent_runs(
        filters_request.pipelineName, filters_request.startDate, filters_request.endDate
    )
    if most_recent_runs is None:
        raise HTTPException(
            status_code=404, detail="Pipeline Runs could not be obtained"
        )
    return most_recent_runs
