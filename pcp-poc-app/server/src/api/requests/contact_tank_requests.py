from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CreateContactTankLive(BaseModel): 
    hydraulic_system_name: str # foreign key
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str

    validated_tag: Optional[str]
    operating_level: Optional[float]
    bwl: Optional[float]
    twl: Optional[float]
    capacity: Optional[float]
    comments: Optional[str]
    include_SDSR: Optional[int]
    include_SRV: Optional[int]
    include_WPRO: Optional[int]
    last_modified: Optional[datetime]
    
class CreateContactTankRequest(BaseModel):
    odmt_contact_tank_id: int
    hydraulic_system_name: Optional[str]
    sres_name: Optional[str]
    cell_name: Optional[str]
    pi_tag_name: Optional[str]
    engineering_unit: Optional[str]

    validated_tag: Optional[str]
    operating_level: Optional[float]
    bwl: Optional[float]
    twl: Optional[float]
    capacity: Optional[float]
    comments: Optional[str]
    include_SDSR: Optional[int]
    include_SRV: Optional[int]
    include_WPRO: Optional[int]
    date_updated: Optional[datetime]


class UpdateContactTankRequest(BaseModel):
    id: int
    odmt_contact_tank_id: Optional[int]
    hydraulic_system_name: Optional[str]
    sres_name: Optional[str]
    cell_name: Optional[str]
    pi_tag_name: Optional[str]
    engineering_unit: Optional[str]
    validated_tag: Optional[str]
    operating_level: Optional[float]
    bwl: Optional[float]
    twl: Optional[float]
    capacity: Optional[float]
    comments: Optional[str]
    include_SDSR: Optional[int]
    include_SRV: Optional[int]
    include_WPRO: Optional[int]
    date_updated: Optional[datetime]
