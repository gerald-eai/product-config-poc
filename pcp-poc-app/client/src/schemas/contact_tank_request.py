from pydantic import BaseModel 
from datetime import datetime 


class BaseRequest(BaseModel): 
    # provide the required params to create a new current entry
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

class CreateNewLiveEntry(BaseRequest):  
    last_modified: datetime | None = None
    
class CreateNewStagedEntry(BaseRequest): 
    # add in required entries
    odmt_contact_tank_id: int # required foreign key
    date_updated: datetime | None = None
    
# Base Class
class EditStagedEntry(BaseModel): 
    id: int # required primary key
    odmt_contact_tank_id: int 
    hydraulic_system_name: str
    sres_name: str | None = None 
    cell_name: str | None = None 
    pi_tag_name: str | None = None 
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
    engineering_unit: str | None = None