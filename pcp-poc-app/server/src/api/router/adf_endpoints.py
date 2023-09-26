# use this for connecting to the ADF APIs 
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_adf_pipelines_service
from services.adf_pipelines_service import DataFactoryService

router = APIRouter(prefix="/data-factory", tags=["ADF Query Endpoints"])

@router.get("/pipelines")
def list_adf_pipelines(adf_service: DataFactoryService = Depends(get_adf_pipelines_service)):
    response = adf_service.list_by_factory()
    if response is None: 
        raise HTTPException(status_code=404, detail="No pipelines found")
    print(f"Response: {response}")
    for item in response: 
        print(f"Pipeline: {item}")
    return response 

@router.get("/pipelines/{pipeline_name}")
def get_adf_pipeline(pipeline_name: str, adf_service: DataFactoryService = Depends(get_adf_pipelines_service)):
    response = adf_service.get_pipeline(pipeline_name=pipeline_name)
    if response is None: 
        raise HTTPException(status_code=404, detail="No pipelines with that name found")
    print(f"Response: {response}")
    return response


