# API Endpoints for SRES based requests
from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import (
    get_sres_service,
    get_audit_log_service,
)
from services.sres_service import SresService
from services.audit_log_service import AuditLogService

from schemas.sres_schema import SresCurrent
from api.requests import sres_requests
from api.requests.audit_log_requests import CreateAuditRequest
from datetime import datetime
from typing import List


router = APIRouter(prefix="/sres", tags=["SRes Endpoints"])


# Read Operations
@router.get("/", response_model=List[SresCurrent])
def get_sres_home(
    skip: int = 0,
    limit: int = 100,
    sres_service: SresService = Depends(get_sres_service),
):
    sres_data = sres_service.get_all(skip, limit)
    return sres_data


@router.get("/{odmt_sres_id}", response_model=SresCurrent)
def get_sres_by_id(
    odmt_sres_id: int, sres_service: SresService = Depends(get_sres_service)
):
    sres_data = sres_service.get_by_id(sres_id=odmt_sres_id)
    return sres_data


# create new entry in the current table
@router.post("/", response_model=SresCurrent)
def create_new_sres(
    create_sres_request: sres_requests.CreateNewSres,
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
            status="Pending",
            pushed_to_live_date=datetime.now(),
            row_id_altered=str(new_sres_obj.odmt_sres_id),
        )
        print(f"New Audit Event: \n{new_audit_event}")
        audit_service.create_new_event(new_audit_event)
        return new_sres_obj

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")


# perform an update of the data
@router.put("/{odmt_sres_id}", response_model=SresCurrent)
def update_sres_by_id(
    sres_request: sres_requests.UpdateSres,
    sres_service: SresService = Depends(get_sres_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    # use the update service
    try:
        updated_sres_obj = sres_service.update_existing_entry(sres_request)
        print(f"Updated Sres Object: \n{updated_sres_obj}")
        # enter a new audit log record/entry
        update_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_sres",
            columns_altered="odmt_sres_id;hydraulic_system_name;sres_name;cell_name;pi_tag_name;engineering_unit",
            event_type="Update SRES Entry",
            previous_value=f"{updated_sres_obj.odmt_sres_id};{updated_sres_obj.hydraulic_system_name};{updated_sres_obj.sres_name};{updated_sres_obj.cell_name};",
            updated_value=f"{updated_sres_obj.odmt_sres_id};{updated_sres_obj.hydraulic_system_name};{updated_sres_obj.sres_name};{updated_sres_obj.cell_name};",
            actor="megumi@shadowgarden.jjk",
            event_date=datetime.now(),
            status="Pending",
            row_id_altered=str(updated_sres_obj.odmt_sres_id),
        )
        print(f"New Audit Event: \n{update_audit_event}")
        audit_service.create_new_event(update_audit_event)
        return updated_sres_obj
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")
