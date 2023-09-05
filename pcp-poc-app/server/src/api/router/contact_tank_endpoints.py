from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import (
    get_contact_tank_service,
    get_contact_tank_update_service,
    get_audit_log_service,
)
from api.requests import contact_tank_requests
from services.contact_tank_service import ContactTankService, ContactTankUpdateService
from schemas.contact_tank_schema import ContactTankCurrent, ContactTankUpdates
from api.requests.audit_log_requests import CreateAuditRequest
from services.audit_log_service import AuditLogService
from datetime import datetime
from typing import List


router = APIRouter(prefix="/contact-tanks", tags=["Contact Tanks Endpoints"])


@router.get("/live", response_model=List[ContactTankCurrent])
def get_all_current(
    skip: int = 0,
    limit: int = 100,
    contact_tank_service: ContactTankService = Depends(get_contact_tank_service),
):
    sys_map_data = contact_tank_service.get_all(skip=skip, limit=limit)
    return sys_map_data


@router.get("/live/{odmt_contact_tank_id}", response_model=ContactTankCurrent)
def get_current_by_name(
    odmt_contact_tank_id: int,
    contact_tank_service: ContactTankService = Depends(get_contact_tank_service),
):
    contact_tank_data = contact_tank_service.get_by_tank_id(odmt_contact_tank_id)
    return contact_tank_data


@router.post("/live", response_model=ContactTankCurrent)
def create_new_entry(
    create_request: contact_tank_requests.CreateContactTankLive,
    create_tank_service: ContactTankService = Depends(get_contact_tank_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    print(f"Here is the request submitted: {create_request}")
    try:
        new_contact_tank_obj = create_tank_service.create_new_entry(create_request)
        new_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_contact_tanks",
            event_type="New Current Contact Tank Entry",
            previous_value="None;None;None;None;None;None",
            actor="GearFourth@raughtale.com",
            event_date=datetime.now(),
            columns_altered="odmt_contact_tank_id;hydraulic_system_name;sres_name;cell_name;pi_tag_name;engineering_unit",
            updated_value=f"{new_contact_tank_obj.odmt_contact_tank_id};{new_contact_tank_obj.hydraulic_system_name};{new_contact_tank_obj.sres_name};{new_contact_tank_obj.cell_name};{new_contact_tank_obj.pi_tag_name};{new_contact_tank_obj.engineering_unit}",
            status="Added to Live",
            pushed_to_live_date=datetime.now(),
            row_altered=str(new_contact_tank_obj.odmt_contact_tank_id),
        )
        audit_service.create_new_event(new_audit_event)
        return new_contact_tank_obj
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# read from updates
@router.get("/updates", response_model=List[ContactTankUpdates])
def get_all_updates(
    skip: int = 0,
    limit: int = 100,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
):
    contact_tank_data = update_tank_service.get_all(skip=skip, limit=limit)
    return contact_tank_data


@router.get("/updates/{odmt_tank_id}", response_model=ContactTankUpdates)
def get_update_tank_id(
    odmt_tank_id: int,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    contact_tank_data = update_tank_service.get_by_tank_id(odmt_tank_id)
    return contact_tank_data


# create in updates
@router.post("/updates", response_model=ContactTankUpdates)
def create_update_entry(
    create_request: contact_tank_requests.CreateContactTankRequest,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    print(f"Here is the request submitted: {create_request}")
    try:
        new_contact_tank_update = update_tank_service.create_new_update(create_request)
        new_audit_event = CreateAuditRequest(
            table_altered="pcp_poc_contact_tank_updates",
            event_type="New Contact Tank Update Entry",
            previous_value="None",
            updated_value="updated",
            actor="CreateTest@testuser.com",
            event_date=new_contact_tank_update.date_updated,
            columns_altered="col1;col2;",
            status="pending",
            pushed_to_live_date=None,
            row_altered=str(new_contact_tank_update.odmt_contact_tank_id)
        )
        audit_service.create_new_event(new_audit_event)
        return new_contact_tank_update
    except ValueError as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# update exsiting in updates
@router.put("/updates/{update_id}", response_model=ContactTankUpdates)
def update_existing_entry(
    update_id: int,
    update_request: contact_tank_requests.UpdateContactTankRequest,
    update_tank_service: ContactTankUpdateService = Depends(get_contact_tank_update_service),
    audit_service: AuditLogService = Depends(get_audit_log_service),
):
    try: 
        contact_tank_data = update_tank_service.\
                                update_existing_entry(update_id, update_request)
        new_audit_event = CreateAuditRequest(
                table_altered="pcp_poc_contact_tank_updates",
                event_type="New Contact Tank Update Entry",
                previous_value="None",
                updated_value="updated",
                actor="CreateTest@testuser.com",
                event_date=contact_tank_data.date_updated,
                columns_altered="col1;col2;",
                status="pending",
                pushed_to_live_date=None,
                row_altered=str(contact_tank_data.odmt_contact_tank_id)
            )
        audit_service.create_new_event(new_audit_event)
        
        return contact_tank_data
    except ValueError as e: 
        raise HTTPException(status_code=400, detail=str(e))
