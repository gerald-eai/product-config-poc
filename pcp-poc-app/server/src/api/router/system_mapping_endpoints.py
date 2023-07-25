from fastapi import APIRouter, Depends
from api.dependencies import get_sys_map_service, get_sys_map_update_service
from schemas.system_mapping_schema import SystemMappingBase, SystemMappingUpdatesBase
from api.requests import system_mapping_requests
from services.system_mapping_service import SystemMappingService, SystemMappingUpdateService


router = APIRouter(prefix="/system_mapping", tags=["system_mapping endpoints"])

# read operations 
@router.get("/live", response_model=list[SystemMappingBase])
def get_all_current(skip:int=0, limit:int=100, sys_map_service: SystemMappingService=Depends(get_sys_map_service)):
    sys_map_data = sys_map_service.get_all(skip=skip, limit=limit)
    return sys_map_data 

@router.get("/live/{hydraulic_system_name}", response_model=SystemMappingBase)
def get_current_by_name(hydraulic_system_name:str, sys_map_service: SystemMappingService=Depends(get_sys_map_service)):
    sys_map_data = sys_map_service.get_by_hydraulic_name(hydraulic_system_name)
    return sys_map_data
    
# read from updates 
@router.get("/updates", response_model=list[SystemMappingUpdatesBase])
def get_all_updates(skip:int=0, limit:int=100, sys_map_update_service: SystemMappingUpdateService=Depends(get_sys_map_update_service)):
    sys_map_data = sys_map_update_service.get_all(skip=skip, limit=limit)
    return sys_map_data

@router.get("/updates/{hydraulic_system_name}", response_model=SystemMappingUpdatesBase)
def get_update_by_name(hydraulic_system_name:str, sys_map_update_service: SystemMappingUpdateService=Depends(get_sys_map_update_service)):
    sys_map_data = sys_map_update_service.get_by_hydraulic_name(hydraulic_system_name)
    return sys_map_data

# create in updates 
@router.post("/updates", response_model=SystemMappingUpdatesBase)
def create_update_entry(create_request: system_mapping_requests.CreateSystemMapUpdate, sys_map_update_service: SystemMappingUpdateService=Depends(get_sys_map_update_service)):
    sys_map_data = sys_map_update_service.create_new_update(create_request)
    return sys_map_data

# update in updates
@router.put("/updates/{update_id}", response_model=SystemMappingUpdatesBase)
def update_existing_entry(update_id:int, update_request: system_mapping_requests.UpdateSystemMapUpdate,sys_map_update_service: SystemMappingUpdateService=Depends(get_sys_map_update_service)):
    sys_map_data = sys_map_update_service.update_existing_entry(update_id, update_request)
    return sys_map_data