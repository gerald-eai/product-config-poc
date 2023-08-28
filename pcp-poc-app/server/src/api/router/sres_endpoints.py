# API Endpoints for SRES based requests
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import (
    get_sres_service,
    get_sres_update_service,
    get_audit_log_service,
)
from services.sres_service import SresService, SresUpdatesService
from services.audit_log_service import AuditLogService
# from schemas.sres_schema import SresBase, SresUpdateBase
from schemas.sres_schema import SresCurrent, SresUpdate
from api.requests import sres_requests
from api.requests.audit_log_requests import CreateAuditRequest
from datetime import datetime


router = APIRouter(prefix="/sres", tags=["Sres endpoints"])


# Read Operations
@router.get("/live", response_model=list[SresCurrent])
def get_sres_home(
    skip: int = 0,
    limit: int = 100,
    sres_service: SresService = Depends(get_sres_service),
):
    sres_data = sres_service.get_all(skip, limit)
    return sres_data


# @router.get("/live/{odmt_sres_id}", response_model=SresBase)
@router.get("/live/{odmt_sres_id}", response_model=SresCurrent)
def get_sres_by_id(
    odmt_sres_id: int, sres_service: SresService = Depends(get_sres_service)
):
    sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
    return sres_data


# create new entry in the current table
@router.post("/live", response_model=SresCurrent)
def create_new_sres(
    create_sres_request: sres_requests.CreateNewSresLive,
    sres_service: SresService = Depends(get_sres_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    print(f"Create New Sres Request: \n{create_sres_request}")
    try:
        new_sres_obj = sres_service.create_new_entry(create_sres_request)
        print(f"New Sres Object: \n{new_sres_obj}")
        new_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_sres",
            columns_altered="odmt_sres_id;hydraulic_system_name;sres_name;cell_name;pi_tag_name;engineering_unit",
            event_type="New SRES Entry",
            previous_value="None;None;None;None;None;None",
            updated_value=f"{new_sres_obj.odmt_sres_id};{new_sres_obj.hydraulic_system_name};{new_sres_obj.sres_name};{new_sres_obj.cell_name};{new_sres_obj.pi_tag_name};{new_sres_obj.engineering_unit}",
            actor="test@testuser.com",
            event_date=datetime.now(),
            status="Added to Live",
            pushed_to_live_date=datetime.now(),
            row_altered=str(new_sres_obj.odmt_sres_id),   
        )
        print(f"New Audit Event: \n{new_audit_event}")
        audit_service.create_new_event(new_audit_event)
        return new_sres_obj
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")


# read from the updates table
@router.get("/updates", response_model=list[SresUpdate])
def fetch_all_updates(
    skip: int = 0,
    limit: int = 100,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
):
    sres_data = sres_service.get_all(skip, limit)
    print("sres data: \n", sres_data)
    return sres_data


@router.get("/updates/{odmt_sres_id}", response_model=SresUpdate)
def get_update_by_sres_id(
    odmt_sres_id: int,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
):
    sres_data = sres_service.get_by_sres_id(sres_id=odmt_sres_id)
    return sres_data


# leave this endpoint omitted for now
# @router.get("/updates/{update_id}", response_model=list[SresUpdateBase])
# def get_update_by_update_id(odmt_sres_id: int, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
#     sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
#     return sres_data


# Create new update entry
@router.post("/updates/new-entry", response_model=SresUpdate)
def create_sres_update(
    create_sres_update: sres_requests.CreateSresUpdate,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    print(f"Create New Sres Request: \n{create_sres_update}")
    try:
        new_sres_update = sres_service.create_new_update(create_sres_update)
        # create an event based on this
        new_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_sres_updates",
            columns_altered="col1;col2;",
            event_type="New SRES Update",
            previous_value="None;None;",
            updated_value="updated;updated;",
            actor="test@testuser.com",
            event_date=new_sres_update.date_updated,
            status="pending",
            pushed_to_live_date=None,
            row_altered=str(new_sres_update.odmt_sres_id)
        )
        audit_service.create_new_event(new_audit_event)
        return new_sres_update
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update updates entry
@router.put("/updates/{update_id}", response_model=SresUpdate)
def modify_sres_update_entry(
    update_id: int,
    update_sres_update: sres_requests.UpdateSresUpdate,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    try: 
        modified_sres_update = sres_service.modify_update(update_id, update_sres_update)
        print(f"Endpoint new update: {modified_sres_update}")
        # create an audit log event based on the update
        update_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_sres_updates",
            columns_altered="col1;col2;",
            event_type="Modified SRES Update Entry",
            previous_value="prev1;prev2;",
            updated_value="updated1;updated2;",
            actor="modifier@testdomain.com",
            event_date=modified_sres_update.date_updated,
            status="pending",
            pushed_to_live_date=None,
            row_altered=str(modified_sres_update.id)
        )
        audit_service.create_new_event(update_audit_event)

        return modified_sres_update
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
