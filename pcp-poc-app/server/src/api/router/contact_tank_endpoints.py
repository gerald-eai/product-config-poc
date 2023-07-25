from fastapi import APIRouter, Depends
from api.dependencies import get_contact_tank_service, get_contact_tank_update_service
from api.requests import contact_tank_requests
from services.contact_tank_service import ContactTankService, ContactTankUpdateService
from schemas.contact_tank_schema import ContactTankCurrentBase, ContactTankUpdateBase


router = APIRouter(prefix="/contact-tanks", tags=["Contact Tanks Endpoints"])


@router.get("/live", response_model=list[ContactTankCurrentBase])
def get_all_current(
    skip: int = 0,
    limit: int = 100,
    contact_tank_service: ContactTankService = Depends(get_contact_tank_service),
):
    sys_map_data = contact_tank_service.get_all(skip=skip, limit=limit)
    return sys_map_data


@router.get("/live/{odmt_contact_tank_id}", response_model=ContactTankCurrentBase)
def get_current_by_name(
    odmt_contact_tank_id: int,
    contact_tank_service: ContactTankService = Depends(get_contact_tank_service),
):
    contact_tank_data = contact_tank_service.get_by_tank_id(odmt_contact_tank_id)
    return contact_tank_data


# read from updates
@router.get("/updates", response_model=list[ContactTankUpdateBase])
def get_all_updates(
    skip: int = 0,
    limit: int = 100,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
):
    contact_tank_data = update_tank_service.get_all(skip=skip, limit=limit)
    return contact_tank_data


@router.get("/updates/{odmt_tank_id}", response_model=ContactTankUpdateBase)
def get_update_tank_id(
    odmt_tank_id: int,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
):
    contact_tank_data = update_tank_service.get_by_tank_id(odmt_tank_id)
    return contact_tank_data


# create in updates
@router.post("/updates", response_model=ContactTankUpdateBase)
def create_update_entry(
    create_request: contact_tank_requests.CreateContactTankRequest,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
):
    contact_tank_data = update_tank_service.create_new_update(create_request)
    return contact_tank_data


# update exsiting in updates
@router.put("/updates/{update_id}", response_model=ContactTankUpdateBase)
def update_existing_entry(
    update_id: int,
    update_request: contact_tank_requests.UpdateContactTankRequest,
    update_tank_service: ContactTankUpdateService = Depends(
        get_contact_tank_update_service
    ),
):
    contact_tank_data = update_tank_service.update_existing_entry(
        update_id, update_request
    )
    return contact_tank_data
