# API Endpoints for SRES based requests 
from fastapi import APIRouter, Depends
from api.dependencies import get_sres_service, get_sres_update_service
from services.sres_service import SresService, SresUpdatesService
from schemas.sres_schema import SresBase, SresUpdateBase
from api.requests import sres_requests

router = APIRouter(prefix="/sres", tags=["sres endpoints"])

# Read Operations
@router.get("/live", response_model=list[SresBase])
def get_sres_home(skip:int=0, limit:int=100, sres_service: SresService = Depends(get_sres_service)):
    sres_data = sres_service.get_all(skip, limit)
    return sres_data

@router.get("/live/{odmt_sres_id}", response_model=SresBase)
def get_sres_by_id(odmt_sres_id: int, sres_service: SresService=Depends(get_sres_service)): 
    sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
    return sres_data

# read from the updates table
@router.get("/updates", response_model=list[SresUpdateBase])
def fetch_all_updates(skip:int=0, limit:int=100, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
    sres_data = sres_service.get_all(skip, limit)
    return sres_data

@router.get("/updates/{odmt_sres_id}", response_model=list[SresUpdateBase])
def get_update_by_sres_id(odmt_sres_id: int, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
    sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
    return sres_data

# @router.get("/updates/{update_id}", response_model=list[SresUpdateBase])
# def get_update_by_update_id(odmt_sres_id: int, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
#     sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
#     return sres_data

# Create new update entry
@router.post("/updates/new-entry", response_model=SresUpdateBase)
def create_sres_update(create_sres_update: sres_requests.CreateSresUpdate, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
    new_sres_update = sres_service.create_new_update(create_sres_update)
    return new_sres_update

# Update updates entry
@router.put("/updates/{update_id}", response_model=SresUpdateBase)
def update_sres_update(update_id:int, update_sres_update: sres_requests.UpdateSresUpdate, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
    updated_sres_update = sres_service.modify_update(update_id, update_sres_update)
    print(f"API Endpoints: Updated SRES Update Entry: \n{updated_sres_update}")
    print(f"Updated Entry type: {type(updated_sres_update)}\n")
    return updated_sres_update




