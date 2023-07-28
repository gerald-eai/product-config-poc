from pydantic import BaseModel
from datetime import datetime 


class RequestAll(BaseModel): 
    skip: int = 0 
    limit: int = 100 
    
class SresRequestById(BaseModel): 
    odmt_sres_id: int
    
class ContactTanksRequestById(BaseModel): 
    odmt_contact_tank_id: int 
    
class SystemMapRequestById(BaseModel): 
    hydraulic_system_name: str  

# staging schemas
class CreateEntrySchema(BaseModel): 
    hydraulic_system_name: str 

class CreateContactTankRequest(CreateEntrySchema):
    odmt_contact_tank_id: int
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
    


class CreateSresUpdate(CreateEntrySchema):
    odmt_sres_id: int
    sres_name: str
    cell_name: str
    pi_tag_name: str
    engineering_unit: str
    
    operating_level: float | None = None 
    bwl: float | None = None 
    twl: float | None = None 
    capacity: float | None = None 
    include_exclude: str | None = None
    comments: str | None = None 
    include_in_dv: int | None = None
    turnover_target_lower: float | None = None
    turnover_target_upper: float | None = None 
    sm_record_id: str | None = None 
    validated_tag: str | None = None
    date_updated: datetime | None = None
    
class CreateSystemMapUpdate(CreateEntrySchema): 
    area_name: str
    region_name: str
    comments: str | None = None
    odmt_area_id: int
    date_updated: datetime | None = None
    