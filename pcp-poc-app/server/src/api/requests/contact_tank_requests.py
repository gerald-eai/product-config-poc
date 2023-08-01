from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel

class CreateContactTankLive(BaseModel): 
    hydraulic_system_name: str # foreign key
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str

    validated_tag: str | None = None
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    comments: str | None = None
    include_SDSR: int | None = None
    include_SRV: int | None = None
    include_WPRO: int | None = None
    last_modified: datetime | None = None
    
class CreateContactTankRequest(BaseModel):
    odmt_contact_tank_id: int
    hydraulic_system_name: str
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str

    validated_tag: str | None = None
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    comments: str | None = None
    include_SDSR: int | None = None
    include_SRV: int | None = None
    include_WPRO: int | None = None
    date_updated: datetime | None = None


class UpdateContactTankRequest(BaseModel):
    id: int
    odmt_contact_tank_id: int | None = None
    hydraulic_system_name: str | None = None
    sres_name: str | None = None
    cell_name: str | None = None
    pi_tag_name: str | None = None
    engineering_unit: str | None = None
    validated_tag: str | None = None
    operating_level: float | None = None
    bwl: float | None = None
    twl: float | None = None
    capacity: float | None = None
    comments: str | None = None
    include_SDSR: int | None = None
    include_SRV: int | None = None
    include_WPRO: int | None = None
    date_updated: datetime | None = None
