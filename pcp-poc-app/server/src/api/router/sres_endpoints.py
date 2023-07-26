# API Endpoints for SRES based requests
from fastapi import APIRouter, Depends
from api.dependencies import (
    get_sres_service,
    get_sres_update_service,
    get_audit_log_service,
)
from services.sres_service import SresService, SresUpdatesService
from services.audit_log_service import AuditLogService
from schemas.sres_schema import SresBase, SresUpdateBase
from api.requests import sres_requests
from api.requests.audit_log_requests import CreateAuditRequest


router = APIRouter(prefix="/sres", tags=["Sres endpoints"])


# Read Operations
@router.get("/live", response_model=list[SresBase])
def get_sres_home(
    skip: int = 0,
    limit: int = 100,
    sres_service: SresService = Depends(get_sres_service),
):
    sres_data = sres_service.get_all(skip, limit)
    return sres_data


@router.get("/live/{odmt_sres_id}", response_model=SresBase)
def get_sres_by_id(
    odmt_sres_id: int, sres_service: SresService = Depends(get_sres_service)
):
    sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
    return sres_data


# read from the updates table
@router.get("/updates", response_model=list[SresUpdateBase])
def fetch_all_updates(
    skip: int = 0,
    limit: int = 100,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
):
    sres_data = sres_service.get_all(skip, limit)
    return sres_data


@router.get("/updates/{odmt_sres_id}", response_model=list[SresUpdateBase])
def get_update_by_sres_id(
    odmt_sres_id: int,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
):
    sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
    return sres_data


# @router.get("/updates/{update_id}", response_model=list[SresUpdateBase])
# def get_update_by_update_id(odmt_sres_id: int, sres_service: SresUpdatesService = Depends(get_sres_update_service)):
#     sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
#     return sres_data


# Create new update entry
@router.post("/updates/new-entry", response_model=SresUpdateBase)
def create_sres_update(
    create_sres_update: sres_requests.CreateSresUpdate,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    new_sres_update = sres_service.create_new_update(create_sres_update)
    # create an event based on this
    new_audit_event = CreateAuditRequest(
        table_altered="pcp_poc_sres_updates",
        event_type="New SRES Update",
        previous_value="None",
        updated_value="updated",
        actor="test@testuser.com",
        event_date=new_sres_update.date_updated,
    )
    audit_service.create_new_event(new_audit_event)
    return new_sres_update


# Update updates entry
@router.put("/updates/{update_id}", response_model=SresUpdateBase)
def update_sres_update(
    update_id: int,
    update_sres_update: sres_requests.UpdateSresUpdate,
    sres_service: SresUpdatesService = Depends(get_sres_update_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    modified_sres_update = sres_service.modify_update(update_id, update_sres_update)
    print(f"Endpoint new update: {modified_sres_update}")
    # create an audit log event based on the update
    update_audit_event = CreateAuditRequest(
        table_altered="pcp_poc_sres_updates",
        event_type="Modified SRES Update Entry",
        previous_value="previous",
        updated_value="updated",
        actor="modifier@testdomain.com",
        event_date=modified_sres_update.date_updated,
    )
    audit_service.create_new_event(update_audit_event)

    return modified_sres_update
