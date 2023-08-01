from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import (
    get_sys_map_service,
    get_sys_map_update_service,
    get_audit_log_service,
)
from schemas.system_mapping_schema import SystemMappingBase, SystemMappingUpdatesBase
from api.requests import system_mapping_requests
from services.system_mapping_service import (
    SystemMappingService,
    SystemMappingUpdateService,
)
from api.requests.audit_log_requests import CreateAuditRequest
from services.audit_log_service import AuditLogService
from datetime import datetime 


router = APIRouter(prefix="/system-mapping", tags=["System Mapping endpoints"])


# read operations
@router.get("/live", response_model=list[SystemMappingBase])
def get_all_current(
    skip: int = 0,
    limit: int = 100,
    sys_map_service: SystemMappingService = Depends(get_sys_map_service),
):
    sys_map_data = sys_map_service.get_all(skip=skip, limit=limit)
    return sys_map_data


@router.get("/live/{hydraulic_system_name}", response_model=SystemMappingBase)
def get_current_by_name(
    hydraulic_system_name: str,
    sys_map_service: SystemMappingService = Depends(get_sys_map_service),
):
    sys_map_data = sys_map_service.get_by_hydraulic_name(hydraulic_system_name)
    return sys_map_data


@router.post("/live", response_model=SystemMappingBase)
def create_new_system_map(
    create_sysmap_request: system_mapping_requests.CreateNewSystemMapLive,
    sys_map_service: SystemMappingService = Depends(get_sys_map_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    print(f"Create New System Map Request: \n{create_sysmap_request}")
    try:
        new_sysmap_obj = sys_map_service.create_new_entry(create_sysmap_request)
        print(f"New System Map Object: \n{new_sysmap_obj}")
        new_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_system_mapping",
            columns_altered="hydraulic_system_name;area_name;region_name;odmt_area_id",
            event_type="New Current System Map Entry",
            previous_value="None;None;None;None",
            updated_value=f"{new_sysmap_obj.hydraulic_system_name};{new_sysmap_obj.area_name};{new_sysmap_obj.region_name};{new_sysmap_obj.odmt_area_id}",
            actor="Gear5th@Wano.com",
            event_date=datetime.now(),
            status="Added to Live",
            pushed_to_live_date=datetime.now(),
        )
        audit_service.create_new_event(new_audit_event)
        return new_sysmap_obj
    except ValueError as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")


# read from updates
@router.get("/updates", response_model=list[SystemMappingUpdatesBase])
def get_all_updates(
    skip: int = 0,
    limit: int = 100,
    sys_map_update_service: SystemMappingUpdateService = Depends(
        get_sys_map_update_service
    ),
):
    sys_map_data = sys_map_update_service.get_all(skip=skip, limit=limit)
    return sys_map_data


@router.get("/updates/{hydraulic_system_name}", response_model=SystemMappingUpdatesBase)
def get_update_by_name(
    hydraulic_system_name: str,
    sys_map_update_service: SystemMappingUpdateService = Depends(
        get_sys_map_update_service
    ),
):
    sys_map_data = sys_map_update_service.get_by_hydraulic_name(hydraulic_system_name)
    return sys_map_data


# create in updates
@router.post("/updates", response_model=SystemMappingUpdatesBase)
def create_update_entry(
    create_request: system_mapping_requests.CreateSystemMapUpdate,
    sys_map_update_service: SystemMappingUpdateService = Depends(
        get_sys_map_update_service
    ),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    # print(f"System Mapping Update Request: \n{create_request}")
    try:
        print(f"System Mapping Update Request: \n{create_request}")
        new_sys_map_entry = sys_map_update_service.create_new_update(create_request)
        print(f"System Mapping Update Response: \n{new_sys_map_entry}")
        # create an event based on this
        new_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_system_mapping_updates",
            event_type="New System Mapping Update Entry",
            previous_value="None",
            updated_value="updated",
            actor="CreateTest@testuser.com",
            event_date=new_sys_map_entry.date_updated,
            columns_altered="col1;col2;",
            status="Staged",
            pushed_to_live_date=None,
        )
        audit_service.create_new_event(new_audit_event)
        return new_sys_map_entry
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# update in updates
@router.put("/updates/{update_id}", response_model=SystemMappingUpdatesBase)
def update_existing_entry(
    update_id: int,
    update_request: system_mapping_requests.UpdateSystemMapUpdate,
    sys_map_update_service: SystemMappingUpdateService = Depends(
        get_sys_map_update_service
    ),
):
    sys_map_data = sys_map_update_service.update_existing_entry(
        update_id, update_request
    )
    return sys_map_data
